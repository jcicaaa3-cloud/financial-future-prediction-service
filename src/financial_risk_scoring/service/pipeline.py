from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.data.io import build_company_quarter_panel
from financial_risk_scoring.evaluation.walk_forward import walk_forward_evaluate
from financial_risk_scoring.features.engineering import make_feature_panel
from financial_risk_scoring.llm.prompt_builder import build_llm_prompt
from financial_risk_scoring.models.predict import predict_company
from financial_risk_scoring.models.train import train_baseline_models
from financial_risk_scoring.monitoring.data_quality import build_data_quality_report
from financial_risk_scoring.monitoring.drift import build_quarter_drift_report
from financial_risk_scoring.reporting.dashboard import render_portfolio_dashboard
from financial_risk_scoring.reporting.report import build_markdown_report
from financial_risk_scoring.service.decision_packet import build_decision_packet
from financial_risk_scoring.utils import ensure_dir, write_json


def _prepare_feature_artifacts(
    *,
    input_dir: str | Path,
    artifact_dir: str | Path,
    test_size_quarters: int = 4,
    generate_sample_if_missing: bool = False,
) -> tuple[Any, list[str], dict[str, Any], dict[str, Any], dict[str, Any]]:
    input_path = Path(input_dir)
    if generate_sample_if_missing and not input_path.exists():
        generate_sample_input(input_path)

    artifact_path = ensure_dir(Path(artifact_dir))
    raw_panel = build_company_quarter_panel(input_path)
    feature_result = make_feature_panel(raw_panel)
    feature_df = feature_result.frame

    data_summary = {
        "input_dir": str(input_path),
        "raw_rows": int(len(raw_panel)),
        "feature_rows": int(len(feature_df)),
        "feature_count": int(len(feature_result.feature_columns)),
        "companies": int(feature_df["company_id"].nunique()),
        "quarters": sorted(feature_df["quarter"].unique().tolist()),
    }
    write_json(artifact_path / "data_summary.json", data_summary)

    data_quality = build_data_quality_report(feature_df, feature_result.feature_columns)
    write_json(artifact_path / "monitoring" / "data_quality_report.json", data_quality)

    drift_report = build_quarter_drift_report(feature_df, feature_result.feature_columns)
    write_json(artifact_path / "monitoring" / "quarter_drift_report.json", drift_report)

    metrics = train_baseline_models(
        feature_df,
        feature_result.feature_columns,
        artifact_dir=artifact_path,
        test_size_quarters=test_size_quarters,
    )
    walk_forward_evaluate(
        feature_df,
        feature_result.feature_columns,
        artifact_dir=artifact_path,
        min_train_quarters=12,
    )
    return feature_df, feature_result.feature_columns, metrics, data_quality, drift_report


def _finalize_single_prediction(
    *,
    feature_df,
    company_id: str,
    request_dir: Path,
    request_id: str,
    metrics: dict[str, Any],
    data_quality: dict[str, Any],
    drift_report: dict[str, Any],
) -> dict[str, Any]:
    prediction = predict_company(feature_df, company_id=company_id, artifact_dir=request_dir)
    report_path = build_markdown_report(prediction, request_dir / "reports")
    prompt_path = build_llm_prompt(prediction, request_dir / "llm_inputs")
    packet = build_decision_packet(
        prediction,
        output_dir=request_dir / "decision_packets",
        request_id=request_id,
        report_path=report_path,
        llm_prompt_path=prompt_path,
    )
    dashboard_path = render_portfolio_dashboard(
        packet,
        metrics=metrics,
        data_quality=data_quality,
        drift_report=drift_report,
        output_path=request_dir / "dashboard" / f"{company_id}_portfolio_dashboard.html",
    )
    packet["dashboard_path"] = str(dashboard_path)
    packet["metrics_path"] = str(request_dir / "metrics" / "time_split_metrics.json")
    packet["walk_forward_metrics_path"] = str(request_dir / "metrics" / "walk_forward_metrics.json")
    packet["data_summary_path"] = str(request_dir / "data_summary.json")
    packet["data_quality_path"] = str(request_dir / "monitoring" / "data_quality_report.json")
    packet["drift_report_path"] = str(request_dir / "monitoring" / "quarter_drift_report.json")
    packet["metrics_preview"] = {
        target: {
            "selected_model": detail["selected_model"],
            "selected_metric": detail["selected_metric"],
        }
        for target, detail in metrics["targets"].items()
    }
    write_json(Path(packet["decision_packet_path"]), packet)
    return packet


def run_prediction_pipeline(
    *,
    input_dir: str | Path,
    company_id: str,
    artifact_dir: str | Path = "artifacts",
    request_id: str | None = None,
    generate_sample_if_missing: bool = False,
) -> dict[str, Any]:
    rid = request_id or str(uuid4())
    request_dir = ensure_dir(Path(artifact_dir) / "requests" / rid)

    feature_df, _, metrics, data_quality, drift_report = _prepare_feature_artifacts(
        input_dir=input_dir,
        artifact_dir=request_dir,
        generate_sample_if_missing=generate_sample_if_missing,
    )

    packet = _finalize_single_prediction(
        feature_df=feature_df,
        company_id=company_id,
        request_dir=request_dir,
        request_id=rid,
        metrics=metrics,
        data_quality=data_quality,
        drift_report=drift_report,
    )
    write_json(request_dir / "result.json", packet)
    return packet


def run_batch_prediction_pipeline(
    *,
    input_dir: str | Path,
    company_ids: list[str],
    artifact_dir: str | Path = "artifacts",
    request_id: str | None = None,
    generate_sample_if_missing: bool = False,
) -> dict[str, Any]:
    """Train once and score multiple companies for API/portfolio demos."""
    rid = request_id or str(uuid4())
    request_dir = ensure_dir(Path(artifact_dir) / "requests" / rid)
    feature_df, _, metrics, data_quality, drift_report = _prepare_feature_artifacts(
        input_dir=input_dir,
        artifact_dir=request_dir,
        generate_sample_if_missing=generate_sample_if_missing,
    )

    packets: list[dict[str, Any]] = []
    for company_id in company_ids:
        packet = _finalize_single_prediction(
            feature_df=feature_df,
            company_id=company_id,
            request_dir=request_dir,
            request_id=f"{rid}-{company_id}",
            metrics=metrics,
            data_quality=data_quality,
            drift_report=drift_report,
        )
        packets.append(packet)

    response = {
        "request_id": rid,
        "status": "completed",
        "company_count": len(packets),
        "companies": [
            {
                "company_id": packet["company_id"],
                "company_name": packet["company_name"],
                "quarter": packet["quarter"],
                "risk_level": packet["risk_level"],
                "scores": packet["scores"],
                "dashboard_path": packet["dashboard_path"],
                "decision_packet_path": packet["decision_packet_path"],
            }
            for packet in packets
        ],
        "metrics_path": str(request_dir / "metrics" / "time_split_metrics.json"),
        "data_quality_path": str(request_dir / "monitoring" / "data_quality_report.json"),
        "drift_report_path": str(request_dir / "monitoring" / "quarter_drift_report.json"),
        "disclaimer": packets[0]["disclaimer"] if packets else "No predictions generated.",
    }
    write_json(request_dir / "batch_result.json", response)
    write_json(request_dir / "result.json", response)
    return response

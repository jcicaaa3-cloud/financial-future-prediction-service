from __future__ import annotations

from pathlib import Path

from app.main import BatchPredictionRequest, get_latest_data_quality, get_latest_feature_importance, get_latest_leaderboard
from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.service.pipeline import run_batch_prediction_pipeline, run_prediction_pipeline


def test_prediction_contains_portfolio_artifacts(tmp_path):
    input_dir = generate_sample_input(tmp_path / "sample", n_companies=6, start_year=2022, end_year=2025)
    packet = run_prediction_pipeline(input_dir=input_dir, company_id="C003", artifact_dir=tmp_path / "artifacts")
    assert packet["feature_snapshot"]
    assert packet["model_explanations"]
    assert Path(packet["dashboard_path"]).exists()
    assert Path(packet["data_quality_path"]).exists()
    assert Path(packet["drift_report_path"]).exists()


def test_batch_pipeline_trains_once_and_scores_multiple_companies(tmp_path):
    input_dir = generate_sample_input(tmp_path / "sample", n_companies=6, start_year=2022, end_year=2025)
    response = run_batch_prediction_pipeline(
        input_dir=input_dir,
        company_ids=["C001", "C003", "C006"],
        artifact_dir=tmp_path / "artifacts",
    )
    assert response["status"] == "completed"
    assert response["company_count"] == 3
    assert all(Path(item["dashboard_path"]).exists() for item in response["companies"])


def test_portfolio_api_endpoint_contracts(tmp_path):
    # Validate the Pydantic request contract without running another full training pipeline.
    payload = BatchPredictionRequest(
        company_ids=["C001", "C003"],
        input_dir="data/input/sample",
        artifact_dir=str(tmp_path / "artifacts"),
    )
    assert payload.company_ids == ["C001", "C003"]

    request_dir = tmp_path / "artifacts" / "requests" / "contract-check"
    (request_dir / "metrics").mkdir(parents=True)
    (request_dir / "models").mkdir(parents=True)
    (request_dir / "monitoring").mkdir(parents=True)
    (request_dir / "metrics" / "time_split_metrics.json").write_text(
        '{"created_at":"test","split":{},"targets":{"target_margin_deterioration":{"selected_model":"dummy","all_models":{"dummy":{"roc_auc":0.5}}}}}',
        encoding="utf-8",
    )
    (request_dir / "models" / "feature_importance.json").write_text(
        '{"targets":{"target_margin_deterioration":[]}}',
        encoding="utf-8",
    )
    (request_dir / "monitoring" / "data_quality_report.json").write_text(
        '{"quality_gates":{"schema_gate":true}}',
        encoding="utf-8",
    )

    artifact_dir = str(tmp_path / "artifacts")
    leaderboard = get_latest_leaderboard(artifact_dir=artifact_dir)
    assert leaderboard["leaderboard"]

    importance = get_latest_feature_importance(artifact_dir=artifact_dir)
    assert importance["targets"]

    quality = get_latest_data_quality(artifact_dir=artifact_dir)
    assert quality["quality_gates"]

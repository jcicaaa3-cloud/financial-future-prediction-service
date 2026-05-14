from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from financial_risk_scoring.service.pipeline import run_batch_prediction_pipeline, run_prediction_pipeline
from financial_risk_scoring.utils import read_json

app = FastAPI(
    title="Quarterly Financial Risk Scoring Service",
    version="0.5.0",
    description="Portfolio-grade baseline ML service for next-quarter financial deterioration risk scoring.",
)


class PredictionRequest(BaseModel):
    company_id: str = Field(..., examples=["C003"])
    input_dir: str = Field("data/input/sample", description="Directory containing the five required CSV files")
    artifact_dir: str = Field("artifacts", description="Where runtime outputs should be written")


class BatchPredictionRequest(BaseModel):
    company_ids: list[str] = Field(..., min_length=1, examples=[["C001", "C003", "C007"]])
    input_dir: str = Field("data/input/sample", description="Directory containing the five required CSV files")
    artifact_dir: str = Field("artifacts", description="Where runtime outputs should be written")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "quarterly-financial-risk-scoring-service", "version": "0.5.0"}


@app.post("/v1/predictions")
def create_prediction(payload: PredictionRequest) -> dict[str, Any]:
    try:
        return run_prediction_pipeline(
            input_dir=payload.input_dir,
            company_id=payload.company_id,
            artifact_dir=payload.artifact_dir,
            generate_sample_if_missing=True,
        )
    except Exception as exc:  # pragma: no cover - FastAPI error boundary
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/batch-predictions")
def create_batch_prediction(payload: BatchPredictionRequest) -> dict[str, Any]:
    try:
        return run_batch_prediction_pipeline(
            input_dir=payload.input_dir,
            company_ids=payload.company_ids,
            artifact_dir=payload.artifact_dir,
            generate_sample_if_missing=True,
        )
    except Exception as exc:  # pragma: no cover - FastAPI error boundary
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/v1/predictions/{request_id}")
def get_prediction(request_id: str, artifact_dir: str = "artifacts") -> dict[str, Any]:
    path = Path(artifact_dir) / "requests" / request_id / "result.json"
    if not path.exists():
        # Batch children are stored as decision packets inside the parent request directory.
        candidates = list((Path(artifact_dir) / "requests").glob(f"*/decision_packets/{request_id}.json")) if (Path(artifact_dir) / "requests").exists() else []
        if candidates:
            return read_json(candidates[0])
        raise HTTPException(status_code=404, detail=f"request_id not found: {request_id}")
    return read_json(path)


@app.get("/v1/models/latest/metrics")
def get_latest_metrics(artifact_dir: str = "artifacts") -> dict[str, Any]:
    path = _latest_path(artifact_dir, "metrics/time_split_metrics.json")
    return read_json(path)


@app.get("/v1/models/latest/leaderboard")
def get_latest_leaderboard(artifact_dir: str = "artifacts") -> dict[str, Any]:
    metrics = read_json(_latest_path(artifact_dir, "metrics/time_split_metrics.json"))
    rows = []
    for target, detail in metrics.get("targets", {}).items():
        for model_name, model_metrics in detail.get("all_models", {}).items():
            rows.append(
                {
                    "target": target,
                    "model": model_name,
                    "selected": model_name == detail.get("selected_model"),
                    "roc_auc": model_metrics.get("roc_auc"),
                    "average_precision": model_metrics.get("average_precision"),
                    "f1_at_0_5": model_metrics.get("f1_at_0_5"),
                    "brier": model_metrics.get("brier"),
                }
            )
    return {"created_at": metrics.get("created_at"), "split": metrics.get("split"), "leaderboard": rows}


@app.get("/v1/models/latest/feature-importance")
def get_latest_feature_importance(artifact_dir: str = "artifacts") -> dict[str, Any]:
    path = _latest_path(artifact_dir, "models/feature_importance.json")
    return read_json(path)


@app.get("/v1/monitoring/latest/data-quality")
def get_latest_data_quality(artifact_dir: str = "artifacts") -> dict[str, Any]:
    path = _latest_path(artifact_dir, "monitoring/data_quality_report.json")
    return read_json(path)


@app.get("/v1/monitoring/latest/drift")
def get_latest_drift(artifact_dir: str = "artifacts") -> dict[str, Any]:
    path = _latest_path(artifact_dir, "monitoring/quarter_drift_report.json")
    return read_json(path)


def _latest_path(artifact_dir: str, relative_path: str) -> Path:
    requests_dir = Path(artifact_dir) / "requests"
    if not requests_dir.exists():
        raise HTTPException(status_code=404, detail="No generated request artifacts found")
    candidates = sorted(requests_dir.glob(f"*/{relative_path}"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise HTTPException(status_code=404, detail=f"No artifact found for {relative_path}")
    return candidates[0]

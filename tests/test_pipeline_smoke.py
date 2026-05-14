from __future__ import annotations

from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.service.pipeline import run_prediction_pipeline


def test_pipeline_smoke(tmp_path):
    input_dir = generate_sample_input(tmp_path / "sample", n_companies=6, start_year=2022, end_year=2025)
    packet = run_prediction_pipeline(input_dir=input_dir, company_id="C003", artifact_dir=tmp_path / "artifacts")
    assert packet["status"] == "completed"
    assert packet["company_id"] == "C003"
    assert packet["risk_level"] in {"low", "medium", "high"}
    assert "financial_health_score" in packet["scores"]

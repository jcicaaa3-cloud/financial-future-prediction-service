from __future__ import annotations

from app.main import PredictionRequest, create_prediction, get_prediction, health
from financial_risk_scoring.data.generate_sample import generate_sample_input


def test_health_endpoint():
    response = health()
    assert response["status"] == "ok"
    assert response["service"] == "quarterly-financial-risk-scoring-service"


def test_prediction_endpoint_contract(tmp_path):
    input_dir = generate_sample_input(tmp_path / "sample", n_companies=6, start_year=2022, end_year=2025)
    body = create_prediction(
        PredictionRequest(
            company_id="C003",
            input_dir=str(input_dir),
            artifact_dir=str(tmp_path / "artifacts"),
        )
    )
    assert body["company_id"] == "C003"
    assert body["status"] == "completed"
    stored = get_prediction(body["request_id"], artifact_dir=str(tmp_path / "artifacts"))
    assert stored["request_id"] == body["request_id"]

from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime, timezone


def _band(score: float, *, high_is_bad: bool = False) -> str:
    if high_is_bad:
        if score >= 70:
            return "red"
        if score >= 40:
            return "yellow"
        return "green"
    if score >= 70:
        return "green"
    if score >= 40:
        return "yellow"
    return "red"


def build_decision_packet(prediction: dict, output_dir: str | Path) -> Path:
    """Convert model prediction into service/API friendly decision packet.

    This packet is intentionally simple. In a production service, this object
    can become the response body of GET /api/companies/{company_id}/diagnosis.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scores = prediction["scores"]
    growth = float(scores["growth_possibility_score"])
    risk = float(scores["risk_signal_score"])
    health = float(scores["financial_health_score"])

    if risk >= 70 or health < 40:
        action = "watchlist"
    elif growth >= 65 and risk < 45 and health >= 55:
        action = "growth_candidate"
    elif risk >= 55:
        action = "monitor"
    else:
        action = "neutral_review"

    packet = {
        "schema_version": "diagnosis_packet.v0.3",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "company": {
            "company_id": prediction["company_id"],
            "company_name": prediction.get("company_name"),
            "sector": prediction.get("sector"),
            "as_of_quarter": prediction.get("quarter"),
        },
        "scores": scores,
        "traffic_lights": {
            "growth": _band(growth),
            "financial_health": _band(health),
            "risk": _band(risk, high_is_bad=True),
        },
        "recommended_action": action,
        "evidence": {
            "positive_factors": prediction.get("positive_factors", []),
            "risk_factors": prediction.get("risk_factors", []),
            "top_growth_model_features": prediction.get("top_growth_model_features", [])[:5],
            "top_risk_model_features": prediction.get("top_risk_model_features", [])[:5],
        },
        "disclaimer": "Synthetic-data MVP output. Not investment advice.",
    }

    out_path = output_dir / f"{prediction['company_id']}_decision_packet.json"
    out_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    import json
    sample = json.loads(Path("outputs/predictions/C003_prediction.json").read_text(encoding="utf-8"))
    build_decision_packet(sample, "outputs/decision_packets")

from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from financial_risk_scoring.utils import ensure_dir, utc_now_iso, write_json

DISCLAIMER = (
    "Synthetic/sample or user-supplied data output. Not investment, lending, credit, "
    "trading, or corporate-rating advice. Human review is required."
)


def build_decision_packet(
    prediction: dict[str, Any],
    *,
    output_dir: str | Path,
    request_id: str | None = None,
    report_path: str | Path | None = None,
    llm_prompt_path: str | Path | None = None,
) -> dict[str, Any]:
    rid = request_id or str(uuid4())
    packet = {
        "request_id": rid,
        "status": "completed",
        "created_at": utc_now_iso(),
        "company_id": prediction["company_id"],
        "company_name": prediction["company_name"],
        "sector": prediction["sector"],
        "quarter": prediction["quarter"],
        "feature_available_at": prediction["feature_available_at"],
        "scores": prediction["scores"],
        "risk_level": prediction["risk_level"],
        "top_risk_factors": prediction.get("top_risk_factors", []),
        "positive_factors": prediction.get("positive_factors", []),
        "selected_models": prediction.get("selected_models", {}),
        "feature_snapshot": prediction.get("feature_snapshot", {}),
        "model_explanations": prediction.get("model_explanations", {}),
        "model_created_at": prediction.get("model_created_at"),
        "report_path": str(report_path) if report_path else None,
        "llm_prompt_path": str(llm_prompt_path) if llm_prompt_path else None,
        "disclaimer": DISCLAIMER,
    }
    out = ensure_dir(Path(output_dir)) / f"{rid}.json"
    write_json(out, packet)
    packet["decision_packet_path"] = str(out)
    return packet

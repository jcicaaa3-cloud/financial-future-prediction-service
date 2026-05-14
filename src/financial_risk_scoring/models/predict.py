from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from financial_risk_scoring.explainability.importance import build_feature_snapshot, build_prediction_explanations
from financial_risk_scoring.models.train import load_model_bundle

RISK_LABELS = {
    "target_margin_deterioration": "margin_deterioration_risk",
    "target_market_drawdown_proxy": "market_drawdown_proxy_risk",
    "target_liquidity_stress": "liquidity_stress_risk",
}


def _probability(model: Any, x: pd.DataFrame) -> float:
    proba = model.predict_proba(x)
    if proba.shape[1] == 1:
        return 1.0 if getattr(model, "classes_", [0])[0] == 1 else 0.0
    return float(proba[0, 1])


def _risk_level(avg_risk: float) -> str:
    if avg_risk >= 0.67:
        return "high"
    if avg_risk >= 0.38:
        return "medium"
    return "low"


def _factor_lists(row: pd.Series) -> tuple[list[str], list[str]]:
    risk_factors: list[str] = []
    positive_factors: list[str] = []

    if row.get("debt_ratio", 0) >= 0.65:
        risk_factors.append("High debt ratio")
    if row.get("current_ratio", 9) < 1.2:
        risk_factors.append("Weak current ratio")
    if row.get("operating_margin", 1) < 0.05:
        risk_factors.append("Weak operating margin")
    if row.get("volatility_3m", 0) >= 0.35:
        risk_factors.append("High recent volatility")
    if row.get("disclosure_risk_score", 0) >= 0.65:
        risk_factors.append("Elevated disclosure risk score")
    if row.get("major_event_flag", 0) >= 1:
        risk_factors.append("Recent major event flag")

    if row.get("current_ratio", 0) >= 1.5:
        positive_factors.append("Healthy current ratio")
    if row.get("operating_margin", 0) >= 0.12:
        positive_factors.append("Strong operating margin")
    if row.get("ocf_margin", 0) >= 0.08:
        positive_factors.append("Solid operating cash-flow margin")
    if row.get("debt_ratio", 1) <= 0.40:
        positive_factors.append("Conservative debt ratio")
    if row.get("revenue_growth_qoq", 0) >= 0.05:
        positive_factors.append("Positive revenue growth")

    return risk_factors[:5], positive_factors[:5]


def predict_company(
    feature_df: pd.DataFrame,
    *,
    company_id: str,
    artifact_dir: str | Path,
) -> dict[str, Any]:
    bundle = load_model_bundle(artifact_dir)
    feature_columns = bundle["feature_columns"]
    company_rows = feature_df.loc[feature_df["company_id"] == company_id].copy()
    if company_rows.empty:
        available = sorted(feature_df["company_id"].unique().tolist())[:10]
        raise ValueError(f"Unknown company_id={company_id!r}. Available examples: {available}")

    latest = company_rows.sort_values("quarter_index").iloc[-1]
    x = latest[feature_columns].to_frame().T

    scores: dict[str, float] = {}
    for target, model in bundle["models"].items():
        scores[RISK_LABELS[target]] = round(_probability(model, x), 4)

    avg_risk = float(np.mean(list(scores.values())))
    scores["financial_health_score"] = round(1.0 - avg_risk, 4)
    risk_factors, positive_factors = _factor_lists(latest)

    model_explanations = build_prediction_explanations(
        latest, bundle["metrics"].get("targets", {}), top_n=5
    )
    feature_snapshot = build_feature_snapshot(latest)

    return {
        "company_id": str(latest["company_id"]),
        "company_name": str(latest["company_name"]),
        "sector": str(latest["sector"]),
        "quarter": str(latest["quarter"]),
        "feature_available_at": str(latest["feature_available_at"]),
        "scores": scores,
        "risk_level": _risk_level(avg_risk),
        "top_risk_factors": risk_factors,
        "positive_factors": positive_factors,
        "model_created_at": bundle["created_at"],
        "selected_models": {
            target: bundle["metrics"]["targets"][target]["selected_model"]
            for target in bundle["models"]
        },
        "feature_snapshot": feature_snapshot,
        "model_explanations": model_explanations,
    }

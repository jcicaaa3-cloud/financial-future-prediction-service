from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.pipeline import Pipeline

RISK_DIRECTION_HINTS = {
    "debt_ratio": "higher values usually increase balance-sheet risk",
    "debt_to_equity": "higher values usually increase leverage risk",
    "current_ratio": "lower values usually increase liquidity risk",
    "interest_coverage": "lower values usually increase liquidity and debt-service risk",
    "operating_margin": "lower values usually increase profitability risk",
    "net_margin": "lower values usually increase profitability risk",
    "ocf_margin": "lower values usually increase cash-flow risk",
    "volatility_3m": "higher values usually increase market risk",
    "disclosure_risk_score": "higher values usually increase disclosure/event risk",
    "major_event_flag": "flagged values usually increase event risk",
    "revenue_growth_qoq": "negative values usually increase growth risk",
}


def extract_feature_importance(estimator: Any, feature_columns: list[str], *, top_n: int = 20) -> list[dict[str, Any]]:
    """Extract simple global importance values from sklearn estimators.

    This intentionally avoids SHAP so the portfolio project stays lightweight.
    For tree models, it uses feature_importances_. For linear models, it uses
    absolute coefficient magnitude. Dummy baselines return an empty list.
    """
    final_estimator = estimator.steps[-1][1] if isinstance(estimator, Pipeline) else estimator

    if hasattr(final_estimator, "feature_importances_"):
        raw_values = list(final_estimator.feature_importances_)
        source = "feature_importances_"
    elif hasattr(final_estimator, "coef_"):
        coef = final_estimator.coef_[0] if getattr(final_estimator, "coef_").ndim == 2 else final_estimator.coef_
        raw_values = [abs(float(value)) for value in coef]
        source = "absolute_coefficient"
    else:
        return []

    rows = []
    total = sum(abs(float(value)) for value in raw_values) or 1.0
    for feature, value in zip(feature_columns, raw_values, strict=False):
        normalized = abs(float(value)) / total
        rows.append(
            {
                "feature": feature,
                "importance": round(float(normalized), 6),
                "raw_importance": round(float(value), 6),
                "source": source,
                "interpretation_hint": interpretation_hint(feature),
            }
        )
    return sorted(rows, key=lambda item: item["importance"], reverse=True)[:top_n]


def interpretation_hint(feature_name: str) -> str:
    for token, hint in RISK_DIRECTION_HINTS.items():
        if token in feature_name:
            return hint
    return "model-used feature; inspect with domain context"


def build_prediction_explanations(
    row: pd.Series,
    target_metrics: dict[str, Any],
    *,
    top_n: int = 5,
) -> dict[str, list[dict[str, Any]]]:
    """Attach current feature values to global top features for each target.

    The output is not a causal explanation and not a SHAP value. It is a compact
    explanation packet that tells reviewers which features the selected baseline
    relied on globally and what the current company-quarter values look like.
    """
    explanations: dict[str, list[dict[str, Any]]] = {}
    for target, detail in target_metrics.items():
        rows = []
        for item in detail.get("top_features", [])[:top_n]:
            feature = item["feature"]
            value = row.get(feature)
            try:
                value_out: float | str | None = round(float(value), 6)
            except (TypeError, ValueError):
                value_out = None if pd.isna(value) else str(value)
            rows.append(
                {
                    "feature": feature,
                    "current_value": value_out,
                    "global_importance": item["importance"],
                    "interpretation_hint": item.get("interpretation_hint", interpretation_hint(feature)),
                }
            )
        explanations[target] = rows
    return explanations


def build_feature_snapshot(row: pd.Series) -> dict[str, float | int | str | None]:
    preferred = [
        "operating_margin",
        "net_margin",
        "current_ratio",
        "debt_ratio",
        "interest_coverage",
        "ocf_margin",
        "revenue_growth_qoq",
        "stock_return_3m",
        "volatility_3m",
        "disclosure_risk_score",
        "major_event_flag",
        "macro_rate",
        "macro_growth",
    ]
    snapshot: dict[str, float | int | str | None] = {}
    for col in preferred:
        if col not in row:
            continue
        value = row[col]
        if pd.isna(value):
            snapshot[col] = None
        elif isinstance(value, (int, str)):
            snapshot[col] = value
        else:
            snapshot[col] = round(float(value), 6)
    return snapshot

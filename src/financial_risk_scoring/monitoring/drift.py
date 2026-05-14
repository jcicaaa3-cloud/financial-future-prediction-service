from __future__ import annotations

from typing import Any

import pandas as pd


def build_quarter_drift_report(frame: pd.DataFrame, feature_columns: list[str], *, latest_quarter: str | None = None) -> dict[str, Any]:
    """Compare the latest quarter with prior quarters using simple standardized deltas."""
    if latest_quarter is None:
        latest_quarter = str(frame.sort_values("quarter_index")["quarter"].iloc[-1])

    latest = frame.loc[frame["quarter"] == latest_quarter, feature_columns]
    reference = frame.loc[frame["quarter"] != latest_quarter, feature_columns]
    if latest.empty or reference.empty:
        return {"latest_quarter": latest_quarter, "features": [], "note": "insufficient quarters for drift check"}

    rows = []
    for col in feature_columns:
        latest_mean = float(latest[col].mean())
        reference_mean = float(reference[col].mean())
        reference_std = float(reference[col].std()) or 0.0
        standardized_delta = 0.0 if reference_std == 0 else (latest_mean - reference_mean) / reference_std
        rows.append(
            {
                "feature": col,
                "latest_mean": round(latest_mean, 6),
                "reference_mean": round(reference_mean, 6),
                "standardized_delta": round(float(standardized_delta), 6),
                "severity": _severity(abs(float(standardized_delta))),
            }
        )
    rows = sorted(rows, key=lambda item: abs(item["standardized_delta"]), reverse=True)
    return {
        "latest_quarter": latest_quarter,
        "reference_quarters": sorted(frame.loc[frame["quarter"] != latest_quarter, "quarter"].unique().tolist()),
        "features": rows[:20],
        "quality_gate": {
            "max_abs_standardized_delta": max(abs(row["standardized_delta"]) for row in rows) if rows else 0.0,
            "severe_feature_count": sum(1 for row in rows if row["severity"] == "high"),
        },
    }


def _severity(abs_delta: float) -> str:
    if abs_delta >= 2.5:
        return "high"
    if abs_delta >= 1.5:
        return "medium"
    return "low"

from __future__ import annotations

from typing import Any

import pandas as pd


def build_data_quality_report(frame: pd.DataFrame, feature_columns: list[str]) -> dict[str, Any]:
    """Create a small data-quality packet suitable for API responses and dashboards."""
    numeric = frame[feature_columns]
    missing_rates = numeric.isna().mean().sort_values(ascending=False)
    constant_features = [col for col in feature_columns if numeric[col].nunique(dropna=True) <= 1]

    return {
        "row_count": int(len(frame)),
        "company_count": int(frame["company_id"].nunique()),
        "quarter_count": int(frame["quarter"].nunique()),
        "feature_count": int(len(feature_columns)),
        "date_range": {
            "first_quarter": str(frame["quarter"].min()),
            "last_quarter": str(frame["quarter"].max()),
        },
        "missing_rate_top10": [
            {"feature": str(feature), "missing_rate": round(float(rate), 6)}
            for feature, rate in missing_rates.head(10).items()
        ],
        "constant_features": constant_features[:20],
        "quality_gates": {
            "has_minimum_rows": bool(len(frame) >= 100),
            "has_multiple_companies": bool(frame["company_id"].nunique() >= 5),
            "has_multiple_quarters": bool(frame["quarter"].nunique() >= 8),
            "no_constant_feature_overflow": bool(len(constant_features) <= 5),
        },
    }

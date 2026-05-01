from __future__ import annotations

import numpy as np
import pandas as pd


def add_future_labels(df: pd.DataFrame, horizon: int = 1) -> pd.DataFrame:
    """Create future growth/risk/health labels.

    Labels are shifted by company so that row t uses information from t+horizon
    as the training target.
    """
    out = df.copy().sort_values(["company_id", "quarter"])
    group = out.groupby("company_id", group_keys=False)

    future_cols = [
        "revenue_growth_qoq",
        "operating_margin",
        "ocf_margin",
        "debt_ratio",
        "current_ratio",
        "interest_coverage",
        "net_margin",
        "volatility_3m",
        "disclosure_risk_score",
    ]
    for col in future_cols:
        out[f"future_{col}"] = group[col].shift(-horizon)

    out["target_growth"] = (
        (out["future_revenue_growth_qoq"] > out["revenue_growth_qoq"].fillna(0))
        & (out["future_operating_margin"] >= out["operating_margin"].fillna(0) - 0.01)
        & (out["future_ocf_margin"] >= -0.02)
    ).astype(int)

    out["target_risk"] = (
        (out["future_debt_ratio"] > out["debt_ratio"].fillna(0) * 1.08)
        | (out["future_interest_coverage"] < 1.5)
        | (out["future_ocf_margin"] < -0.03)
        | (out["future_net_margin"] < -0.04)
        | (out["future_disclosure_risk_score"] > 0.68)
    ).astype(int)

    raw_health = (
        35 * np.tanh(out["future_operating_margin"].fillna(0) * 5)
        + 25 * np.tanh(out["future_ocf_margin"].fillna(0) * 5)
        + 20 * np.tanh((out["future_current_ratio"].fillna(1) - 1.0) / 2.0)
        + 20 * np.tanh(out["future_interest_coverage"].fillna(0) / 6.0)
        - 25 * np.tanh(out["future_debt_ratio"].fillna(1) / 2.5)
        - 10 * out["future_disclosure_risk_score"].fillna(0.5)
    )
    out["target_health_score"] = np.clip(50 + raw_health, 0, 100)

    out = out.dropna(subset=[f"future_{c}" for c in future_cols]).reset_index(drop=True)
    return out

from __future__ import annotations

import numpy as np
import pandas as pd


def add_latent_proxy_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create lightweight latent proxy features.

    In a later research version this file can be replaced by PCA, AutoEncoder,
    TabTransformer embeddings, or disclosure text embeddings.
    """
    out = df.copy()

    out["growth_cashflow_gap"] = out["revenue_growth_qoq"].fillna(0) - out["ocf_margin"].fillna(0)
    out["profitability_leverage_pressure"] = out["debt_ratio"].fillna(0) * (1 - out["operating_margin"].fillna(0))
    out["quality_of_growth"] = out["revenue_growth_qoq"].fillna(0) + out["operating_margin"].fillna(0) + out["ocf_margin"].fillna(0)
    out["market_financial_mismatch"] = out["stock_return_3m"].fillna(0) - out["quality_of_growth"].fillna(0)
    out["macro_pressure"] = (
        out["macro_rate"].fillna(out["macro_rate"].median()) * 0.35
        + out["inflation"].fillna(out["inflation"].median()) * 0.35
        + (out["fx_rate"].fillna(out["fx_rate"].median()) / 1000.0) * 0.30
    )
    out["risk_composite_proxy"] = (
        out["profitability_leverage_pressure"].fillna(0)
        + out["volatility_3m"].fillna(0)
        + out["disclosure_risk_score"].fillna(0)
        + np.maximum(out["growth_cashflow_gap"].fillna(0), 0)
    )

    return out

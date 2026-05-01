from __future__ import annotations

import numpy as np
import pandas as pd

EPS = 1e-9


def add_financial_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Add profitability, stability, liquidity, and market features."""
    out = df.copy()
    out = out.sort_values(["company_id", "quarter"])

    out["operating_margin"] = out["operating_income"] / (out["revenue"] + EPS)
    out["net_margin"] = out["net_income"] / (out["revenue"] + EPS)
    out["roe"] = out["net_income"] / (out["total_equity"].abs() + EPS)
    out["roa"] = out["net_income"] / (out["total_assets"].abs() + EPS)
    out["debt_ratio"] = out["total_debt"] / (out["total_equity"].abs() + EPS)
    out["current_ratio"] = out["current_assets"] / (out["current_liabilities"].abs() + EPS)
    out["ocf_margin"] = out["operating_cash_flow"] / (out["revenue"] + EPS)
    out["interest_coverage"] = out["operating_income"] / (out["interest_expense"].abs() + EPS)
    out["market_to_sales"] = out["market_cap"] / (out["revenue"] + EPS)

    group = out.groupby("company_id", group_keys=False)
    out["revenue_growth_qoq"] = group["revenue"].pct_change()
    out["op_income_growth_qoq"] = group["operating_income"].pct_change()
    out["market_cap_growth_qoq"] = group["market_cap"].pct_change()

    rolling_cols = [
        "revenue_growth_qoq",
        "operating_margin",
        "debt_ratio",
        "ocf_margin",
        "stock_return_3m",
        "volatility_3m",
    ]
    for col in rolling_cols:
        out[f"{col}_rolling4_mean"] = group[col].rolling(4, min_periods=2).mean().reset_index(level=0, drop=True)
        out[f"{col}_rolling4_std"] = group[col].rolling(4, min_periods=2).std().reset_index(level=0, drop=True)

    numeric_cols = out.select_dtypes(include=[np.number]).columns
    out[numeric_cols] = out[numeric_cols].replace([np.inf, -np.inf], np.nan)
    return out

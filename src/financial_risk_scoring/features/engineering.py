from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from financial_risk_scoring.utils import safe_divide

TARGET_COLUMNS = [
    "target_margin_deterioration",
    "target_market_drawdown_proxy",
    "target_liquidity_stress",
]

EXCLUDED_MODEL_COLUMNS = {
    "company_id",
    "company_name",
    "sector",
    "quarter",
    "quarter_index",
    "quarter_end_date",
    "feature_available_at",
    "disclosure_summary_ko",
    *TARGET_COLUMNS,
}


@dataclass(frozen=True)
class FeatureBuildResult:
    frame: pd.DataFrame
    feature_columns: list[str]
    target_columns: list[str]


def _quarter_end_date(quarter: str) -> str:
    year = int(quarter[:4])
    q = int(quarter[-1])
    month_day = {1: (3, 31), 2: (6, 30), 3: (9, 30), 4: (12, 31)}[q]
    return datetime(year, month_day[0], month_day[1]).date().isoformat()


def make_feature_panel(panel: pd.DataFrame) -> FeatureBuildResult:
    df = panel.copy().sort_values(["company_id", "quarter_index"]).reset_index(drop=True)

    # Current-quarter financial ratios. These are allowed features because they are derived
    # from the same quarter's reported financials, not from future labels.
    df["operating_margin"] = safe_divide(df["operating_income"], df["revenue"])
    df["net_margin"] = safe_divide(df["net_income"], df["revenue"])
    df["debt_ratio"] = safe_divide(df["total_debt"], df["total_assets"])
    df["equity_ratio"] = safe_divide(df["total_equity"], df["total_assets"])
    df["current_ratio"] = safe_divide(df["current_assets"], df["current_liabilities"], default=99.0)
    df["ocf_margin"] = safe_divide(df["operating_cash_flow"], df["revenue"])
    df["interest_coverage"] = safe_divide(df["operating_income"], df["interest_expense"], default=99.0)
    df["market_to_assets"] = safe_divide(df["market_cap"], df["total_assets"])
    df["debt_to_equity"] = safe_divide(df["total_debt"], df["total_equity"], default=99.0)

    group = df.groupby("company_id", group_keys=False)
    df["revenue_growth_qoq"] = group["revenue"].pct_change().replace([np.inf, -np.inf], np.nan)
    df["operating_margin_change_qoq"] = group["operating_margin"].diff()
    df["debt_ratio_change_qoq"] = group["debt_ratio"].diff()
    df["stock_return_3m_lag1"] = group["stock_return_3m"].shift(1)
    df["volatility_3m_lag1"] = group["volatility_3m"].shift(1)
    df["disclosure_risk_lag1"] = group["disclosure_risk_score"].shift(1)

    rolling_cols = ["revenue_growth_qoq", "operating_margin", "stock_return_3m", "volatility_3m"]
    for col in rolling_cols:
        df[f"{col}_roll4_mean"] = group[col].transform(lambda s: s.rolling(4, min_periods=2).mean())
        df[f"{col}_roll4_std"] = group[col].transform(lambda s: s.rolling(4, min_periods=2).std())

    # Future values are used only to build labels. All future columns are dropped before modeling.
    next_operating_margin = group["operating_margin"].shift(-1)
    next_stock_return = group["stock_return_3m"].shift(-1)
    next_current_ratio = group["current_ratio"].shift(-1)
    next_interest_coverage = group["interest_coverage"].shift(-1)

    df["target_margin_deterioration"] = (next_operating_margin < (df["operating_margin"] - 0.03)).astype(int)
    df["target_market_drawdown_proxy"] = ((next_stock_return < -0.10) | (df["volatility_3m"] > 0.55)).astype(int)
    df["target_liquidity_stress"] = ((next_current_ratio < 1.10) | (next_interest_coverage < 2.0)).astype(int)

    # Last quarter for each company has no next-quarter label. Remove it from training/evaluation.
    has_next = group["quarter_index"].shift(-1).notna()
    df = df.loc[has_next].copy()

    df["quarter_end_date"] = df["quarter"].map(_quarter_end_date)
    df["feature_available_at"] = pd.to_datetime(df["quarter_end_date"]) + pd.to_timedelta(45, unit="D")
    df["feature_available_at"] = df["feature_available_at"].dt.date.astype(str)

    # Replace infinities and impute lightly at feature level. Model pipelines still include imputers.
    df = df.replace([np.inf, -np.inf], np.nan)

    feature_columns = [
        col
        for col in df.columns
        if col not in EXCLUDED_MODEL_COLUMNS
        and not col.startswith("target_")
        and not col.startswith("next_")
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    # Fill initial lag/rolling missing values using conservative cross-sectional medians.
    for col in feature_columns:
        df[col] = df[col].fillna(df[col].median())

    return FeatureBuildResult(frame=df.reset_index(drop=True), feature_columns=feature_columns, target_columns=TARGET_COLUMNS.copy())


def assert_no_future_label_leakage(feature_columns: list[str]) -> None:
    forbidden_tokens = ("next_", "future_", "target_")
    offenders = [col for col in feature_columns if any(token in col for token in forbidden_tokens)]
    if offenders:
        raise ValueError(f"Feature columns contain possible future-label leakage: {offenders}")

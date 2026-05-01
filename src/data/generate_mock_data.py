from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def generate_mock_financial_data(
    output_path: str | Path,
    n_companies: int = 40,
    n_quarters: int = 16,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic company-quarter financial data for local MVP testing.

    This is not investment data. It exists only to make the ML pipeline runnable
    without DART/KRX/API credentials.
    """
    rng = np.random.default_rng(seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    quarters = pd.period_range("2021Q1", periods=n_quarters, freq="Q")
    rows: list[dict] = []

    for i in range(n_companies):
        company_id = f"C{i+1:03d}"
        company_name = f"MockCompany_{i+1:03d}"
        sector = rng.choice(["IT", "Manufacturing", "Bio", "Retail", "Finance"])

        base_revenue = rng.uniform(80, 800)
        growth_trend = rng.normal(0.025, 0.035)
        margin_base = rng.uniform(0.03, 0.22)
        leverage_base = rng.uniform(0.25, 1.8)
        liquidity_base = rng.uniform(0.8, 3.0)
        market_cap = base_revenue * rng.uniform(1.2, 6.0)

        revenue = base_revenue
        total_assets = base_revenue * rng.uniform(1.0, 3.0)
        equity = total_assets / (1 + leverage_base)
        debt = total_assets - equity

        for t, quarter in enumerate(quarters):
            macro_rate = 2.0 + 0.25 * np.sin(t / 2.5) + rng.normal(0, 0.08)
            fx_rate = 1200 + 35 * np.sin(t / 3.0) + rng.normal(0, 12)
            inflation = 2.2 + 0.35 * np.cos(t / 4.0) + rng.normal(0, 0.15)
            business_cycle = 100 + 3.0 * np.sin(t / 3.5) + rng.normal(0, 0.8)

            shock = rng.normal(0, 0.05)
            revenue_growth = growth_trend + shock - max(macro_rate - 2.2, 0) * 0.01
            revenue = max(10, revenue * (1 + revenue_growth))

            op_margin = np.clip(margin_base + rng.normal(0, 0.035) - leverage_base * 0.012, -0.20, 0.35)
            net_margin = np.clip(op_margin - rng.uniform(0.01, 0.06) - max(macro_rate - 2.0, 0) * 0.01, -0.30, 0.30)

            operating_income = revenue * op_margin
            net_income = revenue * net_margin
            cfo = operating_income * rng.uniform(0.55, 1.35) - revenue * rng.uniform(0.00, 0.08)

            assets_growth = np.clip(revenue_growth + rng.normal(0.01, 0.03), -0.15, 0.20)
            total_assets = max(20, total_assets * (1 + assets_growth))
            debt = max(1, debt * (1 + rng.normal(0.015, 0.05) + max(macro_rate - 2.2, 0) * 0.015))
            equity = max(1, total_assets - debt)
            current_assets = total_assets * np.clip(liquidity_base / 3 + rng.normal(0.0, 0.08), 0.18, 0.75)
            current_liabilities = max(1, current_assets / np.clip(liquidity_base + rng.normal(0.0, 0.25), 0.25, 4.5))
            interest_expense = max(0.1, debt * (macro_rate / 100) * rng.uniform(0.45, 1.25))

            stock_return = revenue_growth * rng.uniform(0.8, 2.0) + op_margin * 0.10 - leverage_base * 0.015 + rng.normal(0, 0.09)
            volatility = np.clip(abs(rng.normal(0.20, 0.08)) + max(leverage_base - 1.0, 0) * 0.05, 0.04, 0.80)
            volume_change = rng.normal(0, 0.25) + abs(stock_return) * 0.35
            market_cap = max(10, market_cap * (1 + stock_return))

            disclosure_risk_score = np.clip(
                rng.normal(0.35, 0.15)
                + max(debt / max(equity, 1) - 1.0, 0) * 0.12
                + (1 if net_income < 0 else 0) * 0.15,
                0,
                1,
            )
            rnd_ratio = np.clip(rng.normal(0.035, 0.025) + (sector in ["IT", "Bio"]) * 0.035, 0, 0.20)

            rows.append(
                {
                    "company_id": company_id,
                    "company_name": company_name,
                    "sector": sector,
                    "quarter": str(quarter),
                    "revenue": revenue,
                    "operating_income": operating_income,
                    "net_income": net_income,
                    "total_assets": total_assets,
                    "total_debt": debt,
                    "total_equity": equity,
                    "current_assets": current_assets,
                    "current_liabilities": current_liabilities,
                    "operating_cash_flow": cfo,
                    "interest_expense": interest_expense,
                    "market_cap": market_cap,
                    "stock_return_3m": stock_return,
                    "volatility_3m": volatility,
                    "volume_change_3m": volume_change,
                    "macro_rate": macro_rate,
                    "fx_rate": fx_rate,
                    "inflation": inflation,
                    "business_cycle_index": business_cycle,
                    "disclosure_risk_score": disclosure_risk_score,
                    "rnd_ratio": rnd_ratio,
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    generate_mock_financial_data(Path("data/raw/financial_panel_mock.csv"))

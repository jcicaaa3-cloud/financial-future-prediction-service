from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from financial_risk_scoring.utils import ensure_dir

SECTORS = ["IT", "Retail", "Bio", "Manufacturing", "Finance"]


def make_quarters(start_year: int = 2021, end_year: int = 2025) -> list[str]:
    return [f"{year}Q{q}" for year in range(start_year, end_year + 1) for q in range(1, 5)]


def generate_sample_input(
    output_dir: str | Path,
    *,
    n_companies: int = 40,
    start_year: int = 2021,
    end_year: int = 2025,
    seed: int = 42,
) -> Path:
    """Generate synthetic CSVs that satisfy the project data contract.

    The data is intentionally synthetic. It is designed to create stable class balance for
    tests and demos, not to simulate a real financial market.
    """

    rng = np.random.default_rng(seed)
    output_path = ensure_dir(Path(output_dir))
    quarters = make_quarters(start_year, end_year)

    company_rows = []
    financial_rows = []
    market_rows = []
    disclosure_rows = []

    macro_rows = []
    for i, quarter in enumerate(quarters):
        cycle = np.sin(i / 2.5)
        macro_rows.append(
            {
                "quarter": quarter,
                "macro_rate": round(2.0 + 0.12 * i + rng.normal(0, 0.05), 4),
                "fx_rate": round(1120 + 11 * i + rng.normal(0, 12), 4),
                "inflation": round(2.2 + 0.3 * cycle + rng.normal(0, 0.08), 4),
                "business_cycle_index": round(100 + 4.0 * cycle + rng.normal(0, 0.7), 4),
            }
        )

    for company_no in range(1, n_companies + 1):
        company_id = f"C{company_no:03d}"
        sector = str(rng.choice(SECTORS))
        company_rows.append(
            {"company_id": company_id, "company_name": f"SampleCompany_{company_no:03d}", "sector": sector}
        )

        base_revenue = rng.uniform(60_000, 400_000)
        revenue_trend = rng.uniform(-0.015, 0.055)
        base_margin = rng.uniform(0.03, 0.22)
        debt_preference = rng.uniform(0.15, 0.75)
        event_pressure = rng.uniform(0.0, 0.20)

        last_revenue = base_revenue
        for idx, quarter in enumerate(quarters):
            cycle = np.sin(idx / 2.5)
            shock = rng.normal(0, 0.035)
            revenue_growth = revenue_trend + 0.012 * cycle + shock
            revenue = max(5_000, last_revenue * (1 + revenue_growth))
            margin_noise = rng.normal(0, 0.02)
            operating_margin = np.clip(base_margin + 0.012 * cycle - 0.035 * event_pressure + margin_noise, -0.08, 0.34)
            operating_income = revenue * operating_margin
            net_income = operating_income * rng.uniform(0.55, 0.90) - rng.uniform(100, 1600)
            total_assets = revenue * rng.uniform(1.2, 2.9)
            total_debt = total_assets * np.clip(debt_preference + rng.normal(0, 0.06), 0.05, 0.90)
            total_equity = max(total_assets - total_debt, 1000)
            current_assets = total_assets * rng.uniform(0.25, 0.62)
            current_liabilities = max(total_debt * rng.uniform(0.18, 0.55), 100)
            operating_cash_flow = operating_income * rng.uniform(0.55, 1.25) + rng.normal(0, revenue * 0.02)
            interest_expense = max(total_debt * rng.uniform(0.003, 0.018), 10)
            market_cap = max(total_equity * rng.uniform(0.7, 2.4), 1000)
            stock_return_3m = np.clip(0.20 * revenue_growth + 0.45 * operating_margin - 0.10 * debt_preference + rng.normal(0, 0.13), -0.55, 0.65)
            volatility_3m = np.clip(0.12 + 0.30 * debt_preference + 0.12 * event_pressure + rng.normal(0, 0.035), 0.05, 0.85)
            volume_change_3m = np.clip(rng.normal(0.04, 0.22) + 0.25 * event_pressure, -0.65, 1.25)
            disclosure_risk_score = np.clip(0.20 + 0.55 * debt_preference + 0.25 * event_pressure - 0.45 * operating_margin + rng.normal(0, 0.08), 0, 1)
            major_event_flag = int(rng.random() < (0.06 + event_pressure * 0.20 + disclosure_risk_score * 0.06))
            rnd_ratio = np.clip(rng.normal(0.035, 0.018) + (0.035 if sector in {"IT", "Bio"} else 0), 0, 0.20)

            financial_rows.append(
                {
                    "company_id": company_id,
                    "quarter": quarter,
                    "revenue": round(revenue, 2),
                    "operating_income": round(operating_income, 2),
                    "net_income": round(net_income, 2),
                    "total_assets": round(total_assets, 2),
                    "total_debt": round(total_debt, 2),
                    "total_equity": round(total_equity, 2),
                    "current_assets": round(current_assets, 2),
                    "current_liabilities": round(current_liabilities, 2),
                    "operating_cash_flow": round(operating_cash_flow, 2),
                    "interest_expense": round(interest_expense, 2),
                }
            )
            market_rows.append(
                {
                    "company_id": company_id,
                    "quarter": quarter,
                    "market_cap": round(market_cap, 2),
                    "stock_return_3m": round(float(stock_return_3m), 5),
                    "volatility_3m": round(float(volatility_3m), 5),
                    "volume_change_3m": round(float(volume_change_3m), 5),
                }
            )
            disclosure_rows.append(
                {
                    "company_id": company_id,
                    "quarter": quarter,
                    "disclosure_risk_score": round(float(disclosure_risk_score), 5),
                    "rnd_ratio": round(float(rnd_ratio), 5),
                    "major_event_flag": major_event_flag,
                    "disclosure_summary_ko": (
                        "합성 데이터: 공시 위험 신호 높음" if disclosure_risk_score > 0.65 else "합성 데이터: 특이 공시 없음"
                    ),
                }
            )
            last_revenue = revenue

    pd.DataFrame(company_rows).to_csv(output_path / "company_master.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(financial_rows).to_csv(output_path / "financial_statement_quarterly.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(market_rows).to_csv(output_path / "market_quarterly.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(macro_rows).to_csv(output_path / "macro_quarterly.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(disclosure_rows).to_csv(output_path / "disclosure_features_quarterly.csv", index=False, encoding="utf-8-sig")
    return output_path


if __name__ == "__main__":
    generate_sample_input(Path("data/input/sample"))

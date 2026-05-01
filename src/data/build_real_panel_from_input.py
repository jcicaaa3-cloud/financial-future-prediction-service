from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.data.validate_input_schema import validate_input_directory, NUMERIC_COLUMNS


def _read(input_dir: Path, filename: str) -> pd.DataFrame:
    return pd.read_csv(input_dir / filename, encoding="utf-8-sig")


def _coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in set(out.columns).intersection(NUMERIC_COLUMNS):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def build_real_panel_from_input(input_dir: str | Path, output_path: str | Path) -> pd.DataFrame:
    """Merge business-facing input CSVs into the internal raw panel schema."""
    input_dir = Path(input_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    validation = validate_input_directory(input_dir, write_report=True)
    if not validation["ok"]:
        raise ValueError(f"Input validation failed. See {validation.get('report_path')}: {validation['errors']}")

    company = _read(input_dir, "company_master.csv")
    financial = _read(input_dir, "financial_statement_quarterly.csv")
    market = _read(input_dir, "market_quarterly.csv")
    macro = _read(input_dir, "macro_quarterly.csv")
    disclosure = _read(input_dir, "disclosure_features_quarterly.csv")

    df = financial.merge(company, on="company_id", how="left")
    df = df.merge(market, on=["company_id", "quarter"], how="left")
    df = df.merge(macro, on="quarter", how="left")
    df = df.merge(disclosure, on=["company_id", "quarter"], how="left")

    df["company_name"] = df["company_name"].fillna(df["company_id"])
    df["sector"] = df["sector"].fillna("unknown")
    df["disclosure_risk_score"] = df["disclosure_risk_score"].fillna(0.50)
    df["rnd_ratio"] = df["rnd_ratio"].fillna(0.0)

    expected_order = [
        "company_id", "company_name", "sector", "quarter", "revenue", "operating_income", "net_income",
        "total_assets", "total_debt", "total_equity", "current_assets", "current_liabilities",
        "operating_cash_flow", "interest_expense", "market_cap", "stock_return_3m", "volatility_3m",
        "volume_change_3m", "macro_rate", "fx_rate", "inflation", "business_cycle_index",
        "disclosure_risk_score", "rnd_ratio",
    ]
    missing_after_merge = [c for c in expected_order if c not in df.columns]
    if missing_after_merge:
        raise ValueError(f"Merged panel missing required columns: {missing_after_merge}")

    df = _coerce_numeric(df[expected_order])
    df = df.sort_values(["company_id", "quarter"]).reset_index(drop=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/input/sample")
    parser.add_argument("--output-path", default="data/raw/financial_panel_from_input.csv")
    args = parser.parse_args()
    panel = build_real_panel_from_input(args.input_dir, args.output_path)
    print(f"saved {args.output_path} rows={len(panel):,} cols={len(panel.columns):,}")

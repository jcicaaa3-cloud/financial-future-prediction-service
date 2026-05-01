from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

SCHEMAS: dict[str, list[str]] = {
    "company_master.csv": ["company_id", "company_name", "sector"],
    "financial_statement_quarterly.csv": [
        "company_id", "quarter", "revenue", "operating_income", "net_income",
        "total_assets", "total_debt", "total_equity", "current_assets",
        "current_liabilities", "operating_cash_flow", "interest_expense"
    ],
    "market_quarterly.csv": [
        "company_id", "quarter", "market_cap", "stock_return_3m", "volatility_3m", "volume_change_3m"
    ],
    "macro_quarterly.csv": ["quarter", "macro_rate", "fx_rate", "inflation", "business_cycle_index"],
    "disclosure_features_quarterly.csv": ["company_id", "quarter", "disclosure_risk_score", "rnd_ratio"],
}

NUMERIC_COLUMNS = {
    "revenue", "operating_income", "net_income", "total_assets", "total_debt", "total_equity",
    "current_assets", "current_liabilities", "operating_cash_flow", "interest_expense",
    "market_cap", "stock_return_3m", "volatility_3m", "volume_change_3m",
    "macro_rate", "fx_rate", "inflation", "business_cycle_index", "disclosure_risk_score", "rnd_ratio",
    "major_event_flag",
}


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def validate_input_directory(input_dir: str | Path, write_report: bool = True) -> dict:
    """Validate the business-facing CSV input directory before model execution."""
    input_dir = Path(input_dir)
    result: dict = {
        "input_dir": str(input_dir),
        "ok": True,
        "files": {},
        "errors": [],
        "warnings": [],
    }

    for filename, required_cols in SCHEMAS.items():
        path = input_dir / filename
        file_result = {"exists": path.exists(), "rows": 0, "missing_columns": []}
        if not path.exists():
            result["ok"] = False
            result["errors"].append(f"missing required file: {filename}")
            result["files"][filename] = file_result
            continue

        df = _read_csv(path)
        file_result["rows"] = int(len(df))
        missing = [c for c in required_cols if c not in df.columns]
        file_result["missing_columns"] = missing
        if missing:
            result["ok"] = False
            result["errors"].append(f"{filename} missing columns: {missing}")

        if len(df) == 0:
            result["ok"] = False
            result["errors"].append(f"{filename} has no rows")

        if "quarter" in df.columns:
            bad_quarters = df["quarter"].astype(str).str.match(r"^\d{4}Q[1-4]$").eq(False).sum()
            if bad_quarters:
                result["ok"] = False
                result["errors"].append(
                    f"{filename} has {int(bad_quarters)} invalid quarter values. Use YYYYQn, e.g. 2025Q1"
                )

        for col in set(df.columns).intersection(NUMERIC_COLUMNS):
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.isna().sum() > df[col].isna().sum():
                result["warnings"].append(f"{filename}.{col} contains non-numeric values that will become NaN")

        result["files"][filename] = file_result

    if write_report:
        report_path = input_dir / "validation_report.json"
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["report_path"] = str(report_path)

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/input/sample")
    args = parser.parse_args()
    report = validate_input_directory(args.input_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["ok"]:
        raise SystemExit(1)

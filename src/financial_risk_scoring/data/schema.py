from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class CsvContract:
    file_name: str
    required_columns: tuple[str, ...]


CONTRACTS: dict[str, CsvContract] = {
    "company_master": CsvContract(
        file_name="company_master.csv",
        required_columns=("company_id", "company_name", "sector"),
    ),
    "financial": CsvContract(
        file_name="financial_statement_quarterly.csv",
        required_columns=(
            "company_id",
            "quarter",
            "revenue",
            "operating_income",
            "net_income",
            "total_assets",
            "total_debt",
            "total_equity",
            "current_assets",
            "current_liabilities",
            "operating_cash_flow",
            "interest_expense",
        ),
    ),
    "market": CsvContract(
        file_name="market_quarterly.csv",
        required_columns=(
            "company_id",
            "quarter",
            "market_cap",
            "stock_return_3m",
            "volatility_3m",
            "volume_change_3m",
        ),
    ),
    "macro": CsvContract(
        file_name="macro_quarterly.csv",
        required_columns=(
            "quarter",
            "macro_rate",
            "fx_rate",
            "inflation",
            "business_cycle_index",
        ),
    ),
    "disclosure": CsvContract(
        file_name="disclosure_features_quarterly.csv",
        required_columns=(
            "company_id",
            "quarter",
            "disclosure_risk_score",
            "rnd_ratio",
            "major_event_flag",
            "disclosure_summary_ko",
        ),
    ),
}

NUMERIC_COLUMNS = {
    "revenue",
    "operating_income",
    "net_income",
    "total_assets",
    "total_debt",
    "total_equity",
    "current_assets",
    "current_liabilities",
    "operating_cash_flow",
    "interest_expense",
    "market_cap",
    "stock_return_3m",
    "volatility_3m",
    "volume_change_3m",
    "macro_rate",
    "fx_rate",
    "inflation",
    "business_cycle_index",
    "disclosure_risk_score",
    "rnd_ratio",
    "major_event_flag",
}


def quarter_to_index(value: str) -> int:
    text = str(value).strip().upper()
    if len(text) != 6 or text[4] != "Q" or text[5] not in "1234":
        raise ValueError(f"Invalid quarter format: {value!r}. Expected format like 2025Q1.")
    return int(text[:4]) * 4 + int(text[5])


def validate_dataframe(name: str, df: pd.DataFrame) -> None:
    if name not in CONTRACTS:
        raise KeyError(f"Unknown contract name: {name}")
    contract = CONTRACTS[name]
    missing = [col for col in contract.required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"{contract.file_name} is missing required columns: {missing}")

    if "quarter" in df.columns:
        invalid = []
        for value in df["quarter"].dropna().astype(str).unique():
            try:
                quarter_to_index(value)
            except ValueError:
                invalid.append(value)
        if invalid:
            raise ValueError(f"{contract.file_name} has invalid quarter values: {invalid[:5]}")

    for col in NUMERIC_COLUMNS.intersection(df.columns):
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.isna().any():
            bad_count = int(converted.isna().sum())
            raise ValueError(f"{contract.file_name}.{col} has {bad_count} non-numeric or missing values")


def validate_input_dir(input_dir: Path) -> dict[str, Path]:
    missing_files = []
    paths = {}
    for name, contract in CONTRACTS.items():
        path = input_dir / contract.file_name
        paths[name] = path
        if not path.exists():
            missing_files.append(contract.file_name)
    if missing_files:
        raise FileNotFoundError(f"Missing input files in {input_dir}: {missing_files}")
    return paths

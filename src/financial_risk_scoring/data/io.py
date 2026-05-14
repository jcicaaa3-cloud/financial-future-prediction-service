from __future__ import annotations

from pathlib import Path

import pandas as pd

from financial_risk_scoring.data.schema import NUMERIC_COLUMNS, validate_dataframe, validate_input_dir, quarter_to_index


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_input_directory(input_dir: str | Path) -> dict[str, pd.DataFrame]:
    input_path = Path(input_dir)
    paths = validate_input_dir(input_path)
    frames: dict[str, pd.DataFrame] = {}
    for name, path in paths.items():
        df = _read_csv(path)
        validate_dataframe(name, df)
        for col in NUMERIC_COLUMNS.intersection(df.columns):
            df[col] = pd.to_numeric(df[col], errors="raise")
        frames[name] = df
    return frames


def build_company_quarter_panel(input_dir: str | Path) -> pd.DataFrame:
    frames = load_input_directory(input_dir)

    panel = frames["financial"].merge(frames["company_master"], on="company_id", how="left")
    panel = panel.merge(frames["market"], on=["company_id", "quarter"], how="left")
    panel = panel.merge(frames["macro"], on="quarter", how="left")
    panel = panel.merge(frames["disclosure"], on=["company_id", "quarter"], how="left")

    if panel["company_name"].isna().any():
        missing = panel.loc[panel["company_name"].isna(), "company_id"].unique().tolist()
        raise ValueError(f"company_id values missing from company_master.csv: {missing[:10]}")

    required_after_merge = [
        "market_cap",
        "stock_return_3m",
        "macro_rate",
        "disclosure_risk_score",
    ]
    missing_cols = panel[required_after_merge].isna().any()
    if missing_cols.any():
        offenders = missing_cols[missing_cols].index.tolist()
        raise ValueError(f"Merged panel has missing values in columns: {offenders}")

    panel["quarter_index"] = panel["quarter"].map(quarter_to_index)
    panel = panel.sort_values(["company_id", "quarter_index"]).reset_index(drop=True)
    return panel

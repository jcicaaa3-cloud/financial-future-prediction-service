from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.features.financial_ratios import add_financial_ratios
from src.features.latent_features import add_latent_proxy_features
from src.features.label_builder import add_future_labels


def build_panel_dataset(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    df["quarter_order"] = pd.PeriodIndex(df["quarter"], freq="Q").astype(str)
    df = df.sort_values(["company_id", "quarter_order"])

    df = add_financial_ratios(df)
    df = add_latent_proxy_features(df)
    df = add_future_labels(df, horizon=1)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan)

    # Conservative imputation for MVP. In research version, use train-only imputers.
    for col in numeric_cols:
        median = df[col].median()
        df[col] = df[col].fillna(0 if pd.isna(median) else median)

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    build_panel_dataset("data/raw/financial_panel_mock.csv", "data/processed/feature_panel.csv")

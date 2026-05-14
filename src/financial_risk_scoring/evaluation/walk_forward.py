from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from financial_risk_scoring.evaluation.metrics import classification_metrics
from financial_risk_scoring.features.engineering import TARGET_COLUMNS, assert_no_future_label_leakage
from financial_risk_scoring.utils import ensure_dir, utc_now_iso, write_json


def walk_forward_evaluate(
    feature_df: pd.DataFrame,
    feature_columns: list[str],
    *,
    artifact_dir: str | Path | None = None,
    min_train_quarters: int = 8,
    random_state: int = 42,
) -> dict[str, Any]:
    assert_no_future_label_leakage(feature_columns)
    quarters = sorted(feature_df["quarter_index"].unique().tolist())
    folds = []

    for test_quarter in quarters[min_train_quarters:]:
        train_df = feature_df.loc[feature_df["quarter_index"] < test_quarter]
        test_df = feature_df.loc[feature_df["quarter_index"] == test_quarter]
        if train_df.empty or test_df.empty:
            continue

        fold_result: dict[str, Any] = {
            "test_quarter_index": int(test_quarter),
            "test_quarter": str(test_df["quarter"].iloc[0]),
            "train_rows": int(len(train_df)),
            "test_rows": int(len(test_df)),
            "targets": {},
        }
        for target in TARGET_COLUMNS:
            model = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    (
                        "classifier",
                        RandomForestClassifier(
                            n_estimators=8,
                            max_depth=3,
                            min_samples_leaf=5,
                            class_weight="balanced_subsample",
                            random_state=random_state,
                            n_jobs=1,
                        ),
                    ),
                ]
            )
            model.fit(train_df[feature_columns], train_df[target].astype(int))
            proba = model.predict_proba(test_df[feature_columns])[:, 1]
            fold_result["targets"][target] = classification_metrics(test_df[target].astype(int), proba)
        folds.append(fold_result)

    result = {"created_at": utc_now_iso(), "fold_count": len(folds), "folds": folds}
    if artifact_dir is not None:
        write_json(ensure_dir(Path(artifact_dir) / "metrics") / "walk_forward_metrics.json", result)
    return result

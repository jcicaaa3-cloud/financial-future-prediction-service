from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from financial_risk_scoring.evaluation.metrics import classification_metrics
from financial_risk_scoring.explainability.importance import extract_feature_importance
from financial_risk_scoring.features.engineering import TARGET_COLUMNS, assert_no_future_label_leakage
from financial_risk_scoring.utils import ensure_dir, utc_now_iso, write_json


def _make_estimators(random_state: int = 42) -> dict[str, Pipeline | DummyClassifier]:
    return {
        "dummy_prior": DummyClassifier(strategy="prior", random_state=random_state),
        "logistic_regression": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=300,
                        solver="liblinear",
                        class_weight="balanced",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=10,
                        max_depth=4,
                        min_samples_leaf=5,
                        n_jobs=1,
                        class_weight="balanced_subsample",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }

def _predict_probability(estimator: Any, x: pd.DataFrame) -> np.ndarray:
    if hasattr(estimator, "predict_proba"):
        proba = estimator.predict_proba(x)
        if proba.shape[1] == 1:
            return np.zeros(len(x)) if estimator.classes_[0] == 0 else np.ones(len(x))
        return proba[:, 1]
    return estimator.predict(x)


def _time_split(df: pd.DataFrame, test_size_quarters: int = 4) -> tuple[pd.DataFrame, pd.DataFrame]:
    unique_quarters = sorted(df["quarter_index"].unique().tolist())
    if len(unique_quarters) <= test_size_quarters + 2:
        raise ValueError("Not enough quarters for chronological train/test split")
    test_quarters = set(unique_quarters[-test_size_quarters:])
    train_df = df.loc[~df["quarter_index"].isin(test_quarters)].copy()
    test_df = df.loc[df["quarter_index"].isin(test_quarters)].copy()
    return train_df, test_df


def train_baseline_models(
    feature_df: pd.DataFrame,
    feature_columns: list[str],
    *,
    artifact_dir: str | Path,
    test_size_quarters: int = 4,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train and persist one selected model per target.

    The persisted model is the best baseline by ROC-AUC when available, otherwise by F1.
    """

    assert_no_future_label_leakage(feature_columns)
    artifact_path = ensure_dir(Path(artifact_dir))
    model_path = ensure_dir(artifact_path / "models")

    train_df, test_df = _time_split(feature_df, test_size_quarters=test_size_quarters)
    x_train = train_df[feature_columns]
    x_test = test_df[feature_columns]

    metrics: dict[str, Any] = {
        "created_at": utc_now_iso(),
        "split": {
            "type": "chronological",
            "train_quarters": sorted(train_df["quarter"].unique().tolist()),
            "test_quarters": sorted(test_df["quarter"].unique().tolist()),
            "train_rows": int(len(train_df)),
            "test_rows": int(len(test_df)),
        },
        "targets": {},
    }

    selected_models = {}
    for target in TARGET_COLUMNS:
        y_train = train_df[target].astype(int)
        y_test = test_df[target].astype(int)
        estimator_metrics = {}
        trained_estimators = {}

        for estimator_name, estimator in _make_estimators(random_state).items():
            estimator.fit(x_train, y_train)
            probability = _predict_probability(estimator, x_test)
            m = classification_metrics(y_test, probability)
            estimator_metrics[estimator_name] = m
            trained_estimators[estimator_name] = estimator

        def score_for_selection(item: tuple[str, dict[str, float | None]]) -> float:
            _, m = item
            if m.get("roc_auc") is not None:
                return float(m["roc_auc"])
            if m.get("f1_at_0_5") is not None:
                return float(m["f1_at_0_5"])
            return -1.0

        selected_name, selected_metric = max(estimator_metrics.items(), key=score_for_selection)
        selected_estimator = trained_estimators[selected_name]
        selected_models[target] = selected_estimator
        top_features = extract_feature_importance(selected_estimator, feature_columns, top_n=20)
        metrics["targets"][target] = {
            "selected_model": selected_name,
            "selected_metric": selected_metric,
            "all_models": estimator_metrics,
            "class_balance_train": float(y_train.mean()),
            "class_balance_test": float(y_test.mean()),
            "top_features": top_features,
        }

    bundle = {
        "created_at": utc_now_iso(),
        "feature_columns": feature_columns,
        "target_columns": TARGET_COLUMNS.copy(),
        "models": selected_models,
        "metrics": metrics,
    }
    joblib.dump(bundle, model_path / "model_bundle.joblib")
    write_json(artifact_path / "metrics" / "time_split_metrics.json", metrics)
    feature_importance_payload = {
        "created_at": bundle["created_at"],
        "method": "tree feature_importances_ or absolute linear coefficients, depending on selected model",
        "targets": {
            target: metrics["targets"][target].get("top_features", [])
            for target in TARGET_COLUMNS
        },
        "caution": "Global baseline importance for portfolio/debugging. Not causal evidence.",
    }
    write_json(model_path / "feature_importance.json", feature_importance_payload)
    write_json(
        model_path / "metadata.json",
        {
            "created_at": bundle["created_at"],
            "feature_count": len(feature_columns),
            "targets": TARGET_COLUMNS.copy(),
            "model_bundle_path": str(model_path / "model_bundle.joblib"),
            "feature_importance_path": str(model_path / "feature_importance.json"),
        },
    )
    return metrics


def load_model_bundle(artifact_dir: str | Path) -> dict[str, Any]:
    path = Path(artifact_dir) / "models" / "model_bundle.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model bundle not found: {path}")
    return joblib.load(path)

from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from src.models.train_model import _feature_columns


def _safe_auc(y_true, y_prob) -> float | None:
    try:
        return float(roc_auc_score(y_true, y_prob))
    except ValueError:
        return None


def _pipeline(model):
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", model),
        ]
    )


def run_time_split_validation(
    feature_path: str | Path,
    output_path: str | Path = "outputs/evaluation/time_split_metrics.json",
    test_quarters: int = 3,
    n_estimators: int = 50,
) -> dict:
    """Evaluate with chronological split to reduce future-information leakage risk.

    This function is not automatically treated as final research evidence. It is
    a lightweight protocol stub showing how formal validation should be framed.
    """
    feature_path = Path(feature_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(feature_path).sort_values(["quarter", "company_id"])
    quarters = sorted(df["quarter"].unique())
    if len(quarters) <= test_quarters:
        raise ValueError("Not enough quarters for time split validation.")

    cutoff_quarters = set(quarters[-test_quarters:])
    train_df = df[~df["quarter"].isin(cutoff_quarters)]
    test_df = df[df["quarter"].isin(cutoff_quarters)]

    feature_cols = _feature_columns(df)
    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]

    yg_train = train_df["target_growth"].astype(int)
    yg_test = test_df["target_growth"].astype(int)
    yr_train = train_df["target_risk"].astype(int)
    yr_test = test_df["target_risk"].astype(int)
    yh_train = train_df["target_health_score"].astype(float)
    yh_test = test_df["target_health_score"].astype(float)

    common_classifier = dict(
        n_estimators=n_estimators,
        random_state=42,
        min_samples_leaf=4,
        class_weight="balanced",
        n_jobs=1,
    )
    growth_model = _pipeline(RandomForestClassifier(**common_classifier))
    risk_model = _pipeline(RandomForestClassifier(**common_classifier))
    health_model = _pipeline(RandomForestRegressor(n_estimators=n_estimators, random_state=42, min_samples_leaf=4, n_jobs=1))

    growth_model.fit(X_train, yg_train)
    risk_model.fit(X_train, yr_train)
    health_model.fit(X_train, yh_train)

    growth_pred = growth_model.predict(X_test)
    risk_pred = risk_model.predict(X_test)
    growth_prob = growth_model.predict_proba(X_test)[:, 1]
    risk_prob = risk_model.predict_proba(X_test)[:, 1]
    health_pred = health_model.predict(X_test)

    growth_auc = _safe_auc(yg_test, growth_prob)
    risk_auc = _safe_auc(yr_test, risk_prob)

    metrics = {
        "split_type": "time_based_holdout",
        "train_quarter_min": str(train_df["quarter"].min()),
        "train_quarter_max": str(train_df["quarter"].max()),
        "test_quarters": sorted([str(x) for x in cutoff_quarters]),
        "n_train_rows": int(len(train_df)),
        "n_test_rows": int(len(test_df)),
        "growth_accuracy": round(float(accuracy_score(yg_test, growth_pred)), 4),
        "growth_f1": round(float(f1_score(yg_test, growth_pred, zero_division=0)), 4),
        "growth_auc": None if growth_auc is None else round(growth_auc, 4),
        "risk_accuracy": round(float(accuracy_score(yr_test, risk_pred)), 4),
        "risk_f1": round(float(f1_score(yr_test, risk_pred, zero_division=0)), 4),
        "risk_auc": None if risk_auc is None else round(risk_auc, 4),
        "health_mae": round(float(mean_absolute_error(yh_test, health_pred)), 4),
        "warning": "Synthetic-data metric. This is protocol demonstration, not real financial evidence.",
    }

    output_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    result = run_time_split_validation("data/processed/feature_panel.csv")
    print(json.dumps(result, ensure_ascii=False, indent=2))

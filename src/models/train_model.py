from __future__ import annotations

from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

EXCLUDE_COLUMNS = {
    "company_id",
    "company_name",
    "sector",
    "quarter",
    "quarter_order",
    "target_growth",
    "target_risk",
    "target_health_score",
}


def _feature_columns(df: pd.DataFrame) -> list[str]:
    future_cols = [c for c in df.columns if c.startswith("future_")]
    exclude = EXCLUDE_COLUMNS.union(future_cols)
    cols = [c for c in df.columns if c not in exclude and pd.api.types.is_numeric_dtype(df[c])]
    return cols


def _safe_auc(y_true, y_prob) -> float | None:
    try:
        return float(roc_auc_score(y_true, y_prob))
    except ValueError:
        return None


def _model_pipeline(model):
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", model),
        ]
    )


def train_all_models(feature_path: str | Path, model_dir: str | Path, n_estimators: int = 60) -> dict:
    feature_path = Path(feature_path)
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(feature_path)
    feature_cols = _feature_columns(df)
    X = df[feature_cols]
    y_growth = df["target_growth"].astype(int)
    y_risk = df["target_risk"].astype(int)
    y_health = df["target_health_score"].astype(float)

    X_train, X_test, yg_train, yg_test, yr_train, yr_test, yh_train, yh_test = train_test_split(
        X,
        y_growth,
        y_risk,
        y_health,
        test_size=0.25,
        random_state=42,
        stratify=y_risk,
    )

    common_classifier = dict(
        n_estimators=n_estimators,
        random_state=42,
        min_samples_leaf=4,
        class_weight="balanced",
        n_jobs=1,
    )

    growth_model = _model_pipeline(RandomForestClassifier(**common_classifier))
    risk_model = _model_pipeline(RandomForestClassifier(**common_classifier))
    health_model = _model_pipeline(
        RandomForestRegressor(n_estimators=n_estimators, random_state=42, min_samples_leaf=4, n_jobs=1)
    )

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
        "split_type": "random_split_baseline",
        "growth_accuracy": round(float(accuracy_score(yg_test, growth_pred)), 4),
        "growth_f1": round(float(f1_score(yg_test, growth_pred, zero_division=0)), 4),
        "growth_auc": None if growth_auc is None else round(growth_auc, 4),
        "risk_accuracy": round(float(accuracy_score(yr_test, risk_pred)), 4),
        "risk_f1": round(float(f1_score(yr_test, risk_pred, zero_division=0)), 4),
        "risk_auc": None if risk_auc is None else round(risk_auc, 4),
        "health_mae": round(float(mean_absolute_error(yh_test, health_pred)), 4),
    }

    joblib.dump(growth_model, model_dir / "growth_model.joblib")
    joblib.dump(risk_model, model_dir / "risk_model.joblib")
    joblib.dump(health_model, model_dir / "health_model.joblib")

    metadata = {
        "feature_columns": feature_cols,
        "metrics": metrics,
        "model_type": "RandomForest baseline MVP",
        "n_estimators": n_estimators,
        "label_horizon": "next_quarter",
        "data_unit": "company-quarter panel",
        "warning": "Synthetic data only. Do not use for investment decisions.",
        "note": "For formal evaluation, use time-based split and real DART/KRX/macro/disclosure data.",
    }
    (model_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    train_all_models("data/processed/feature_panel.csv", "outputs/models")

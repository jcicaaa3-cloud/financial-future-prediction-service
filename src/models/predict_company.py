from __future__ import annotations

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd


def _load_metadata(model_dir: Path) -> dict:
    return json.loads((model_dir / "metadata.json").read_text(encoding="utf-8"))


def _top_model_features(model_pipeline, feature_cols: list[str], top_n: int = 8) -> list[dict]:
    model = model_pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        return []
    order = np.argsort(model.feature_importances_)[::-1][:top_n]
    return [
        {"feature": feature_cols[i], "importance": round(float(model.feature_importances_[i]), 6)}
        for i in order
    ]


def _diagnostic_flags(row: pd.Series) -> dict[str, list[str]]:
    positives: list[str] = []
    risks: list[str] = []

    if row.get("revenue_growth_qoq", 0) > 0.03:
        positives.append("최근 분기 매출 성장률이 양호합니다.")
    if row.get("operating_margin", 0) > 0.08:
        positives.append("영업이익률이 안정적인 수준입니다.")
    if row.get("ocf_margin", 0) > 0.05:
        positives.append("영업현금흐름률이 긍정적입니다.")
    if row.get("current_ratio", 0) > 1.5:
        positives.append("유동비율이 비교적 안정적입니다.")
    if row.get("rnd_ratio", 0) > 0.05:
        positives.append("R&D 비중이 높아 잠재 성장 특성이 관측됩니다.")

    if row.get("debt_ratio", 0) > 1.5:
        risks.append("부채비율이 높아 재무 부담이 관측됩니다.")
    if row.get("interest_coverage", 999) < 2.0:
        risks.append("이자보상배율이 낮아 이자 부담 위험이 있습니다.")
    if row.get("ocf_margin", 0) < 0:
        risks.append("영업현금흐름률이 음수로 현금창출력에 주의가 필요합니다.")
    if row.get("volatility_3m", 0) > 0.35:
        risks.append("최근 시장 변동성이 높습니다.")
    if row.get("disclosure_risk_score", 0) > 0.65:
        risks.append("공시 기반 위험 점수가 높습니다.")
    if row.get("growth_cashflow_gap", 0) > 0.08:
        risks.append("매출 성장과 현금흐름 사이의 괴리가 큽니다.")

    if not positives:
        positives.append("명확한 강한 긍정 신호는 제한적이며, 추가 데이터 확인이 필요합니다.")
    if not risks:
        risks.append("즉각적인 강한 위험 신호는 제한적으로 관측됩니다.")

    return {"positive_factors": positives[:5], "risk_factors": risks[:5]}


def predict_company(
    company_id: str,
    feature_path: str | Path,
    model_dir: str | Path,
    output_dir: str | Path,
) -> dict:
    feature_path = Path(feature_path)
    model_dir = Path(model_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(feature_path)
    metadata = _load_metadata(model_dir)
    feature_cols = metadata["feature_columns"]

    company_df = df[df["company_id"] == company_id].sort_values("quarter")
    if company_df.empty:
        available = sorted(df["company_id"].unique())[:10]
        raise ValueError(f"company_id={company_id} not found. examples={available}")

    latest = company_df.iloc[-1]
    X = latest[feature_cols].to_frame().T

    growth_model = joblib.load(model_dir / "growth_model.joblib")
    risk_model = joblib.load(model_dir / "risk_model.joblib")
    health_model = joblib.load(model_dir / "health_model.joblib")

    growth_prob = float(growth_model.predict_proba(X)[:, 1][0])
    risk_prob = float(risk_model.predict_proba(X)[:, 1][0])
    health_score = float(np.clip(health_model.predict(X)[0], 0, 100))

    flags = _diagnostic_flags(latest)
    prediction = {
        "company_id": company_id,
        "company_name": latest.get("company_name", company_id),
        "sector": latest.get("sector", "unknown"),
        "quarter": latest.get("quarter", "unknown"),
        "scores": {
            "growth_possibility_score": round(growth_prob * 100, 2),
            "risk_signal_score": round(risk_prob * 100, 2),
            "financial_health_score": round(health_score, 2),
        },
        "positive_factors": flags["positive_factors"],
        "risk_factors": flags["risk_factors"],
        "top_growth_model_features": _top_model_features(growth_model, feature_cols),
        "top_risk_model_features": _top_model_features(risk_model, feature_cols),
        "model_metrics": metadata.get("metrics", {}),
        "disclaimer": "This MVP uses synthetic data and is not investment advice.",
    }

    out_path = output_dir / f"{company_id}_prediction.json"
    out_path.write_text(json.dumps(prediction, ensure_ascii=False, indent=2), encoding="utf-8")
    return prediction


if __name__ == "__main__":
    predict_company("C003", "data/processed/feature_panel.csv", "outputs/models", "outputs/predictions")

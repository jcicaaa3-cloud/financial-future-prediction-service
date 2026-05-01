from __future__ import annotations

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd


def _load_model_bundle(model_dir: Path):
    metadata = json.loads((model_dir / "metadata.json").read_text(encoding="utf-8"))
    return {
        "metadata": metadata,
        "growth_model": joblib.load(model_dir / "growth_model.joblib"),
        "risk_model": joblib.load(model_dir / "risk_model.joblib"),
        "health_model": joblib.load(model_dir / "health_model.joblib"),
    }


def _score_row(row: pd.Series, feature_cols: list[str], bundle: dict) -> dict:
    X = row[feature_cols].to_frame().T
    growth = float(bundle["growth_model"].predict_proba(X)[:, 1][0] * 100)
    risk = float(bundle["risk_model"].predict_proba(X)[:, 1][0] * 100)
    health = float(np.clip(bundle["health_model"].predict(X)[0], 0, 100))
    return {
        "growth_possibility_score": round(growth, 2),
        "risk_signal_score": round(risk, 2),
        "financial_health_score": round(health, 2),
    }


def _apply_scenario(row: pd.Series, name: str) -> pd.Series:
    stressed = row.copy()

    if name == "interest_rate_up":
        stressed["macro_rate"] = stressed.get("macro_rate", 0) + 1.0
        stressed["interest_expense"] = stressed.get("interest_expense", 0) * 1.25
        stressed["interest_coverage"] = stressed.get("operating_income", 0) / (abs(stressed.get("interest_expense", 0)) + 1e-9)
        stressed["macro_pressure"] = stressed.get("macro_pressure", 0) + 0.35

    elif name == "revenue_slowdown":
        stressed["revenue_growth_qoq"] = stressed.get("revenue_growth_qoq", 0) - 0.08
        stressed["operating_margin"] = stressed.get("operating_margin", 0) - 0.03
        stressed["net_margin"] = stressed.get("net_margin", 0) - 0.025
        stressed["ocf_margin"] = stressed.get("ocf_margin", 0) - 0.04
        stressed["quality_of_growth"] = (
            stressed.get("revenue_growth_qoq", 0)
            + stressed.get("operating_margin", 0)
            + stressed.get("ocf_margin", 0)
        )

    elif name == "market_volatility_up":
        stressed["volatility_3m"] = stressed.get("volatility_3m", 0) + 0.15
        stressed["stock_return_3m"] = stressed.get("stock_return_3m", 0) - 0.10
        stressed["risk_composite_proxy"] = stressed.get("risk_composite_proxy", 0) + 0.20

    else:
        raise ValueError(f"Unknown scenario: {name}")

    return stressed


def run_stress_test(
    company_id: str,
    feature_path: str | Path,
    model_dir: str | Path,
    output_dir: str | Path,
) -> Path:
    feature_path = Path(feature_path)
    model_dir = Path(model_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(feature_path)
    company_df = df[df["company_id"] == company_id].sort_values("quarter")
    if company_df.empty:
        raise ValueError(f"company_id={company_id} not found")

    latest = company_df.iloc[-1]
    bundle = _load_model_bundle(model_dir)
    feature_cols = bundle["metadata"]["feature_columns"]

    baseline = _score_row(latest, feature_cols, bundle)
    scenarios = {}
    for name in ["interest_rate_up", "revenue_slowdown", "market_volatility_up"]:
        stressed = _apply_scenario(latest, name)
        scenario_score = _score_row(stressed, feature_cols, bundle)
        scenarios[name] = {
            "scores": scenario_score,
            "delta_vs_baseline": {
                k: round(float(scenario_score[k] - baseline[k]), 2)
                for k in baseline
            },
        }

    result = {
        "company_id": company_id,
        "quarter": latest.get("quarter", "unknown"),
        "baseline_scores": baseline,
        "scenarios": scenarios,
        "disclaimer": "Synthetic-data stress test for system demonstration only.",
    }

    out_path = output_dir / f"{company_id}_stress_test.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    run_stress_test("C003", "data/processed/feature_panel.csv", "outputs/models", "outputs/stress_tests")

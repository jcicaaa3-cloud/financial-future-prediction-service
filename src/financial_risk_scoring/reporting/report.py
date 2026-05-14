from __future__ import annotations

from pathlib import Path
from typing import Any

from financial_risk_scoring.utils import ensure_dir


def _markdown_table(values: dict[str, object]) -> str:
    if not values:
        return "No feature snapshot available."
    rows = ["| Feature | Value |", "|---|---:|"]
    for key, value in values.items():
        rows.append(f"| {key} | {value} |")
    return "\n".join(rows)


def _explanation_section(explanations: dict[str, list[dict[str, object]]]) -> str:
    if not explanations:
        return "No model-used explanation signals available."
    sections: list[str] = []
    for target, rows in explanations.items():
        sections.append(f"### {target}")
        sections.append("| Feature | Current value | Global importance | Interpretation hint |")
        sections.append("|---|---:|---:|---|")
        for row in rows:
            sections.append(
                f"| {row.get('feature')} | {row.get('current_value')} | "
                f"{row.get('global_importance')} | {row.get('interpretation_hint')} |"
            )
    return "\n".join(sections)


def build_markdown_report(prediction: dict[str, Any], output_dir: str | Path) -> Path:
    output_path = ensure_dir(Path(output_dir))
    scores = prediction["scores"]
    risk_factors = prediction.get("top_risk_factors") or ["No major risk factor identified by simple rules"]
    positive_factors = prediction.get("positive_factors") or ["No major positive factor identified by simple rules"]

    text = f"""
# Quarterly Financial Risk Report

## Company

- Company: {prediction['company_name']} ({prediction['company_id']})
- Sector: {prediction['sector']}
- Quarter: {prediction['quarter']}
- Feature available at: {prediction['feature_available_at']}
- Risk level: **{prediction['risk_level']}**

## Scores

| Signal | Score |
|---|---:|
| Margin deterioration risk | {scores['margin_deterioration_risk']:.4f} |
| Market drawdown proxy risk | {scores['market_drawdown_proxy_risk']:.4f} |
| Liquidity stress risk | {scores['liquidity_stress_risk']:.4f} |
| Financial health score | {scores['financial_health_score']:.4f} |

## Top risk factors

{chr(10).join(f'- {item}' for item in risk_factors)}

## Positive factors

{chr(10).join(f'- {item}' for item in positive_factors)}

## Feature snapshot

{_markdown_table(prediction.get('feature_snapshot', {}))}

## Model-used explanation signals

{_explanation_section(prediction.get('model_explanations', {}))}

## Model note

This is a baseline ML risk-scoring output generated from synthetic or user-supplied CSV data. Feature importance is a debugging and portfolio explanation aid, not causal evidence. It is not investment advice, lending advice, credit screening, or corporate-rating advice.
""".strip()

    path = output_path / f"{prediction['company_id']}_risk_report.md"
    path.write_text(text, encoding="utf-8")
    return path

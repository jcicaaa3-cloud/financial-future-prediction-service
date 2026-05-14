from __future__ import annotations

from pathlib import Path
from typing import Any

from financial_risk_scoring.utils import ensure_dir


def build_llm_prompt(prediction: dict[str, Any], output_dir: str | Path) -> Path:
    output_path = ensure_dir(Path(output_dir))
    scores = prediction["scores"]
    prompt = f"""
You are a financial risk analyst. Write a cautious Korean-language memo based only on the structured information below.
Do not provide investment advice, lending advice, stock recommendations, or credit decisions.

Company: {prediction['company_name']} ({prediction['company_id']})
Sector: {prediction['sector']}
Quarter: {prediction['quarter']}
Risk level: {prediction['risk_level']}

Scores:
- Margin deterioration risk: {scores['margin_deterioration_risk']:.4f}
- Market drawdown proxy risk: {scores['market_drawdown_proxy_risk']:.4f}
- Liquidity stress risk: {scores['liquidity_stress_risk']:.4f}
- Financial health score: {scores['financial_health_score']:.4f}

Risk factors:
{chr(10).join(f'- {item}' for item in prediction.get('top_risk_factors', []))}

Positive factors:
{chr(10).join(f'- {item}' for item in prediction.get('positive_factors', []))}

Feature snapshot:
{prediction.get('feature_snapshot', {})}

Model-used explanation signals:
{prediction.get('model_explanations', {})}

Required sections:
1. Executive summary
2. Risk interpretation
3. Positive factors
4. Data and model limitations
5. Human review checklist
6. What additional evidence would be needed before a real decision
""".strip()
    path = output_path / f"{prediction['company_id']}_llm_prompt.md"
    path.write_text(prompt, encoding="utf-8")
    return path

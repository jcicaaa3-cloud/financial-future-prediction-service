from __future__ import annotations

from pathlib import Path
import json


def build_llm_report_prompt(prediction: dict, output_dir: str | Path) -> Path:
    """Build a model-agnostic LLM prompt from the numeric prediction JSON.

    This module does not call a local toy language model. In a real deployment,
    this prompt can be sent to an approved enterprise LLM API. The prediction
    itself still comes from the audited tabular ML pipeline; the LLM only turns
    structured evidence into a readable memo.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    company_id = prediction.get("company_id", "UNKNOWN")
    payload = json.dumps(prediction, ensure_ascii=False, indent=2)
    prompt = f"""# LLM Report Generation Prompt

You are a financial risk analysis assistant.
Use only the structured JSON below. Do not invent facts.
Do not provide investment advice. Write a concise Korean decision-support memo.

Required sections:
1. 기업 개요
2. 성장 가능성 판단
3. 위험 신호 판단
4. 재무 건전성 판단
5. 추가 확인이 필요한 데이터
6. 면책 문구

Structured prediction JSON:
```json
{payload}
```
"""
    path = output_dir / f"{company_id}_llm_report_prompt.md"
    path.write_text(prompt, encoding="utf-8")
    return path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction-json", default="outputs/predictions/C003_prediction.json")
    parser.add_argument("--output-dir", default="outputs/llm_inputs")
    args = parser.parse_args()
    prediction = json.loads(Path(args.prediction_json).read_text(encoding="utf-8"))
    print(build_llm_report_prompt(prediction, args.output_dir))

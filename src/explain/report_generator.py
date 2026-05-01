from __future__ import annotations

from pathlib import Path


def _score_level(score: float, inverse: bool = False) -> str:
    if inverse:
        if score >= 70:
            return "높음"
        if score >= 40:
            return "보통"
        return "낮음"
    if score >= 70:
        return "높음"
    if score >= 40:
        return "보통"
    return "낮음"


def generate_company_report(prediction: dict, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    company_id = prediction["company_id"]
    company_name = prediction["company_name"]
    sector = prediction.get("sector", "unknown")
    quarter = prediction.get("quarter", "unknown")
    scores = prediction["scores"]

    growth = scores["growth_possibility_score"]
    risk = scores["risk_signal_score"]
    health = scores["financial_health_score"]

    positive_lines = "\n".join([f"- {x}" for x in prediction.get("positive_factors", [])])
    risk_lines = "\n".join([f"- {x}" for x in prediction.get("risk_factors", [])])

    if growth >= 65 and risk < 45:
        summary = "성장 가능성이 비교적 높고 단기 위험 신호는 제한적인 기업으로 분류됩니다."
    elif risk >= 65 and health < 55:
        summary = "재무 부담과 위험 신호가 동시에 관측되어 보수적인 모니터링이 필요한 기업으로 분류됩니다."
    elif growth >= 55 and risk >= 55:
        summary = "성장 가능성과 위험 신호가 동시에 존재하는 고변동성 유형으로 분류됩니다."
    else:
        summary = "뚜렷한 강한 방향성보다는 추가 관찰이 필요한 중립적 유형으로 분류됩니다."

    growth_features = "\n".join(
        [f"- `{x['feature']}`: importance {x['importance']}" for x in prediction.get("top_growth_model_features", [])]
    )
    risk_features = "\n".join(
        [f"- `{x['feature']}`: importance {x['importance']}" for x in prediction.get("top_risk_model_features", [])]
    )

    report = f"""# 기업 미래 상태 진단 리포트

## 1. 분석 대상

- 기업 ID: `{company_id}`
- 기업명: {company_name}
- 섹터: {sector}
- 분석 기준 분기: {quarter}

## 2. 예측 점수

| 항목 | 점수 | 해석 |
|---|---:|---|
| 성장 가능성 점수 | {growth:.2f} / 100 | {_score_level(growth)} |
| 재무 안정성 점수 | {health:.2f} / 100 | {_score_level(health)} |
| 위험 신호 점수 | {risk:.2f} / 100 | {_score_level(risk, inverse=True)} |

## 3. 종합 판단

{summary}

## 4. 주요 긍정 요인

{positive_lines}

## 5. 주요 위험 요인

{risk_lines}

## 6. 모델이 중요하게 본 성장 관련 특성

{growth_features}

## 7. 모델이 중요하게 본 위험 관련 특성

{risk_features}

## 8. 주의 사항

현재 리포트는 MVP 구조 검증을 위한 샘플입니다. 현재 ZIP은 synthetic mock data를 사용하므로 실제 투자 판단이나 재무 의사결정에 사용하면 안 됩니다. 실제 프로젝트에서는 DART/OPEN DART, KRX, 거시경제 데이터, 공시 텍스트 데이터를 연결한 뒤 시간 기반 검증을 수행해야 합니다.
"""

    output_path = output_dir / f"{company_id}_report.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path

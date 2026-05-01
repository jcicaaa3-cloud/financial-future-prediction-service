# LLM report generation prompt

You are a financial risk analysis assistant.
Use the structured JSON below and avoid unsupported facts.
Do not provide investment advice. Write a concise Korean decision-support memo.

Required sections:

1. 기업 개요
2. 성장 가능성 판단
3. 위험 신호 판단
4. 재무 건전성 판단
5. 추가 확인이 필요한 데이터
6. 면책 문구

Structured prediction JSON:

{
  "company_id": "C003",
  "company_name": "SampleCompany_003",
  "sector": "Retail",
  "quarter": "2024Q3",
  "scores": {
    "growth_possibility_score": 19.58,
    "risk_signal_score": 10.01,
    "financial_health_score": 98.33
  },
  "positive_factors": [
    "최근 분기 매출 성장률이 양호합니다.",
    "영업이익률이 안정적인 수준입니다.",
    "영업현금흐름률이 긍정적입니다.",
    "유동비율이 비교적 안정적입니다."
  ],
  "risk_factors": [
    "즉각적인 고위험 신호는 제한적으로 관측되었습니다."
  ],
  "model_metrics": {
    "split_type": "random_split_baseline",
    "growth_accuracy": 0.64,
    "growth_f1": 0.2703,
    "growth_auc": 0.6601,
    "risk_accuracy": 0.72,
    "risk_f1": 0.5116,
    "risk_auc": 0.699,
    "health_mae": 7.7231
  },
  "disclaimer": "This MVP uses artificial sample data and is not investment advice."
}

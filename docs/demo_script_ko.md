# 데모 스크립트

## 1. 프로젝트 포지셔닝 설명

“이 프로젝트는 실제 투자 추천 모델이 아니라, 금융 도메인 ML 서비스를 어떻게 구조화하고 검증하고 API로 제공하는지 보여주는 포트폴리오입니다.”

## 2. 실행

```bash
python run_demo.py --company-id C003
```

확인할 출력:

- request_id
- risk_level
- decision_packet path
- report path
- dashboard path

## 3. 대시보드 확인

```bash
python scripts/build_portfolio_snapshot.py --company-id C003
```

브라우저에서 열기:

```text
examples/portfolio_snapshot/portfolio_dashboard.html
```

## 4. API 실행

```bash
uvicorn app.main:app --reload
```

단일 예측:

```bash
curl -X POST http://127.0.0.1:8000/v1/predictions \
  -H "Content-Type: application/json" \
  -d '{"company_id":"C003","input_dir":"data/input/sample"}'
```

배치 예측:

```bash
curl -X POST http://127.0.0.1:8000/v1/batch-predictions \
  -H "Content-Type: application/json" \
  -d '{"company_ids":["C001","C003","C007"],"input_dir":"data/input/sample"}'
```

## 5. 면접관에게 보여줄 포인트

- `docs/data_contract.md`: 입력 데이터 계약
- `src/financial_risk_scoring/features/engineering.py`: feature/target 분리
- `src/financial_risk_scoring/models/train.py`: baseline leaderboard와 selected model
- `app/main.py`: API endpoints
- `src/financial_risk_scoring/monitoring/`: data quality / drift
- `examples/portfolio_snapshot/`: 사람이 볼 수 있는 결과물

# Reviewer Walkthrough

## 30초 버전

이 저장소는 분기 재무 데이터를 입력받아 다음 분기 재무 악화 리스크를 산출하는 ML 백엔드 서비스입니다. 핵심은 모델 하나가 아니라 **입력 계약, feature pipeline, time-based validation, FastAPI serving, monitoring artifacts, dashboard**까지 이어지는 end-to-end 구조입니다.

## 3분 버전

1. `README.md`의 hero와 pipeline 그림으로 전체 구조를 확인합니다.
2. `python scripts/build_portfolio_snapshot.py --company-id C003`를 실행합니다.
3. `examples/portfolio_snapshot/portfolio_dashboard.html`을 브라우저에서 확인합니다.
4. `uvicorn app.main:app --reload`로 API를 실행합니다.
5. `/docs`에서 FastAPI 문서를 확인합니다.
6. `/v1/models/latest/leaderboard`로 baseline 비교 결과를 확인합니다.
7. `/v1/monitoring/latest/data-quality`와 `/v1/monitoring/latest/drift`로 운영 관점을 확인합니다.

## 코드 리뷰 포인트

| Area | Files |
|---|---|
| Schema / contract | `src/financial_risk_scoring/data/schema.py`, `docs/data_contract.md` |
| Feature engineering | `src/financial_risk_scoring/features/engineering.py` |
| Model training | `src/financial_risk_scoring/models/train.py` |
| Prediction | `src/financial_risk_scoring/models/predict.py` |
| API | `app/main.py` |
| Monitoring | `src/financial_risk_scoring/monitoring/` |
| Dashboard | `src/financial_risk_scoring/reporting/dashboard.py` |
| Tests | `tests/` |

## 면접 답변 포인트

### 왜 synthetic data인가?

공개 저장소에서 저작권, 개인정보, API key 문제를 피하면서 전체 파이프라인을 재현 가능하게 만들기 위해 synthetic sample을 넣었습니다. 실제 데이터 확장은 OpenDART/KRX adapter template과 CSV contract로 열어두었습니다.

### 왜 RandomForest baseline인가?

성능 경쟁이 목적이 아니라 서비스 구조, 검증 방식, artifact design을 보여주는 것이 목적입니다. 그래서 dummy prior, logistic regression, random forest를 비교하고 leaderboard로 노출했습니다.

### 가장 중요한 기술적 포인트는?

금융 시계열성 데이터에서 미래 label이 feature에 섞이지 않도록 feature/label 생성 시점을 분리했고, random split 대신 chronological split과 walk-forward evaluation을 사용했습니다.

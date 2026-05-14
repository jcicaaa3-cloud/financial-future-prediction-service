# 면접/포트폴리오 설명 포인트

## 1. 왜 만들었나

기존 금융 예측 프로젝트는 노트북에서 모델을 학습하고 점수를 출력하는 데서 끝나는 경우가 많습니다. 이 프로젝트는 그 다음 단계를 보여주기 위해 만들었습니다. 즉, 모델 결과를 API, 검증, 모니터링, 리포트, 대시보드로 연결하는 서비스형 ML 구조를 보여줍니다.

## 2. 문제 정의

목표는 “주가를 맞히는 AI”가 아닙니다. 분기 단위 기업 데이터를 기반으로 다음 분기 재무 악화 리스크 신호를 산출하는 것입니다. 그래서 프로젝트명도 future prediction이 아니라 risk scoring으로 낮췄습니다.

## 3. 기술적으로 신경 쓴 부분

- 입력 데이터 계약을 명확히 정의했습니다.
- feature engineering과 target 생성 흐름을 분리했습니다.
- random split만 쓰지 않고 chronological / walk-forward validation을 넣었습니다.
- dummy, logistic regression, random forest baseline을 비교했습니다.
- FastAPI로 single/batch prediction endpoint를 만들었습니다.
- decision packet, markdown report, LLM prompt, dashboard, monitoring artifact를 생성합니다.

## 4. 한계도 명확히 말하기

샘플 데이터는 synthetic입니다. 따라서 모델 성능 숫자는 실제 금융 성능 주장이 아닙니다. 이 프로젝트의 가치는 실서비스형 ML 산출물 구조, 검증 위생, API 설계, 포트폴리오 스토리텔링에 있습니다.

## 5. 질문 받으면 답할 방향

### Q. 왜 RandomForest인가요?

처음부터 복잡한 모델을 쓰기보다 baseline comparison과 서비스 구조를 먼저 보여주는 것이 목표였습니다. 동일한 input/output contract 위에 LightGBM, CatBoost, XGBoost 등을 추가할 수 있게 구조를 분리했습니다.

### Q. 실제 서비스로 가려면 뭐가 필요하죠?

OpenDART/KRX real-data ingestion, available-at-time 검증, label 재정의, calibration, drift monitoring, security hardening, compliance review, human approval workflow가 필요합니다.

### Q. 이 프로젝트의 핵심은 뭔가요?

모델 하나보다 전체 ML product surface입니다. 데이터 계약, feature pipeline, validation, API, monitoring, explanation, dashboard까지 연결한 점이 핵심입니다.

# Interview defense notes

## Q1. 이거 실제 금융 예측 모델인가요?

아니요. 이 프로젝트는 실제 투자 판단용 모델이라고 주장하지 않습니다. synthetic sample data로 실행 흐름을 보여주는 포트폴리오형 ML 백엔드 프로젝트입니다. 핵심은 모델 성능 주장보다 데이터 계약, 누수 방지, 시간 기준 검증, API, 모니터링, 리포트 산출까지 이어지는 서비스화 구조입니다.

## Q2. 왜 RandomForest 같은 baseline을 썼나요?

포트폴리오 목적상 먼저 재현 가능한 baseline과 비교 구조를 만들었습니다. dummy, logistic regression, random forest를 leaderboard로 비교하고, 향후 real data가 붙었을 때 LightGBM, CatBoost, calibration, sector-specific model로 확장하기 쉬운 구조를 목표로 했습니다.

## Q3. 장난감 프로젝트와 다른 점은 뭔가요?

노트북에서 점수 하나 뽑고 끝나는 구조가 아니라 FastAPI endpoint, batch scoring, request artifact, model card, data contract, chronological validation, walk-forward metrics, monitoring report, LLM-ready prompt, dashboard까지 연결했습니다. 포트폴리오 리뷰어가 코드를 깊게 보지 않아도 시스템 경계를 이해할 수 있게 README와 visual assets도 정리했습니다.

## Q4. 금융 데이터에서 가장 조심한 점은 무엇인가요?

미래 정보 누수입니다. 이 프로젝트는 company-quarter panel을 기준으로 feature와 target을 분리하고, 평가도 시간 순서를 유지하도록 구성했습니다. 실제 데이터로 확장할 때는 `feature_available_date`와 `report_release_date` 기준으로 예측 시점에 사용 가능한 정보만 넣는 게 다음 단계입니다.

## Q5. 실서비스로 가려면 무엇을 더 해야 하나요?

OpenDART/KRX 기반 real-data ingestion, 데이터 품질 SLA, 모델 calibration, drift monitoring 강화, 인증/권한, audit log, human approval workflow, 도메인 전문가 검증, compliance review가 필요합니다. 이 저장소는 그 전 단계의 ML engineering portfolio prototype입니다.

## 20초 요약

이 프로젝트는 “주가를 맞히는 AI”가 아니라 “분기 단위 회사 데이터에서 재무 악화 리스크 신호를 산출하는 ML 백엔드 서비스”입니다. 데이터 계약, 시간 기준 검증, baseline comparison, FastAPI, monitoring, dashboard까지 구성해 실제 서비스형 ML 프로젝트의 감각을 보여주는 데 초점을 뒀습니다.

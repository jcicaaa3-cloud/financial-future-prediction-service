# 포트폴리오 케이스 스터디: Quarterly Financial Risk Scoring Service

## 문제 정의

기존 프로젝트는 “financial future prediction”이라는 이름 때문에 범위가 너무 커 보였고, synthetic data 기반 데모라서 장난감처럼 보일 위험이 있었다. V4에서는 GitHub 첫 화면과 포트폴리오 리뷰 경험까지 강화했고, 목표를 “미래 예측”이 아니라 **다음 분기 재무 악화 리스크 스코어링을 위한 ML 서비스 구조**로 재정의했다.

## 핵심 설계 결정

### 1. 예측보다 리스크 스코어링으로 포지셔닝

금융 도메인에서 “미래를 예측한다”는 표현은 방어하기 어렵다. 그래서 margin deterioration, market drawdown proxy, liquidity stress처럼 명확한 risk signal을 target으로 정의했다.

### 2. Notebook이 아니라 API 서비스로 구성

FastAPI를 붙여 단일 예측, 배치 예측, model metrics, leaderboard, feature importance, monitoring endpoints를 제공한다. 이 구조는 ML 결과물을 백엔드 서비스로 배포하는 감각을 보여준다.

### 3. Leakage-aware feature engineering

다음 분기 값을 label 생성에만 사용하고, feature column에는 `next_`, `future_`, `target_`이 들어가지 않도록 guard를 둔다. 또한 chronological split과 walk-forward evaluation을 사용한다.

### 4. 채용자 친화적 artifact 생성

리뷰어가 코드를 전부 읽지 않아도 결과를 볼 수 있도록 정적 HTML dashboard와 markdown report를 생성한다.

## 산출물

- `decision_packet.json`: API가 반환하는 structured decision packet
- `risk_report.md`: 사람이 읽는 markdown 리포트
- `llm_prompt.md`: 안전한 분석 메모 생성을 위한 LLM prompt packet
- `portfolio_dashboard.html`: 브라우저에서 열 수 있는 정적 대시보드
- `time_split_metrics.json`: chronological split baseline leaderboard
- `walk_forward_metrics.json`: walk-forward evaluation 결과
- `data_quality_report.json`: 데이터 품질 gate
- `quarter_drift_report.json`: 간단한 drift smoke check

## 면접 답변 예시

> 이 프로젝트는 실제 투자 모델이라고 주장하지 않습니다. 대신 금융 데이터 프로젝트에서 중요한 data contract, leakage 방지, time-based validation, baseline comparison, API serving, monitoring artifact, model card 작성까지 한 번에 보여주는 포트폴리오입니다. synthetic sample data를 사용했기 때문에 성능 주장은 하지 않고, 서비스화와 검증 구조를 강조했습니다.

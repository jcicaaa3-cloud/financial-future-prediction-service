# 포트폴리오 제출용 설명서

## 한 줄 소개

분기 재무제표, 시장 지표, 거시 지표, 공시 기반 위험 신호를 입력받아 다음 분기 재무 악화 리스크를 산출하는 **ML 기반 FastAPI 백엔드 서비스**입니다.

## 면접에서 강조할 포인트

1. **장난감 예측 모델이 아니라 서비스 구조로 바꿨다**
   - CSV data contract
   - FastAPI inference endpoint
   - batch scoring endpoint
   - Docker / GitHub Actions CI
   - runtime artifact 관리

2. **금융 도메인에서 중요한 leakage 문제를 의식했다**
   - target은 next-quarter 값으로 만들지만 feature column에서는 `next_`, `future_`, `target_` 패턴을 차단한다.
   - random split만 쓰지 않고 chronological split과 walk-forward evaluation을 사용한다.

3. **모델 성능을 과장하지 않는다**
   - sample data는 synthetic이라고 명시한다.
   - real investment/credit decision에 쓰면 안 된다고 model card에 적는다.
   - 대신 ML engineering, validation hygiene, API design을 보여준다.

4. **리뷰어가 바로 볼 수 있는 산출물을 만든다**
   - `examples/portfolio_snapshot/portfolio_dashboard.html`
   - `decision_packet.json`
   - `risk_report.md`
   - `llm_prompt.md`
   - `time_split_metrics.json`
   - `data_quality_report.json`
   - `quarter_drift_report.json`

5. **GitHub 첫인상을 정리했다**
   - README hero image
   - animated pipeline flow GIF
   - architecture diagram
   - dashboard preview
   - GitHub social preview image

## GitHub README 상단에 넣기 좋은 문장

> Leakage-aware financial risk scoring service with FastAPI, walk-forward validation, model leaderboard, monitoring artifacts, and portfolio dashboard.

## 이 프로젝트로 보여주는 역량

- Python package 구조화
- pandas 기반 tabular feature engineering
- scikit-learn baseline modeling
- chronological validation / walk-forward evaluation
- FastAPI API contract 설계
- Docker / CI / pytest
- model card / data contract / monitoring artifact 작성
- LLM report prompt를 안전하게 decision-support 형태로 연결
- GitHub README storytelling과 visual asset 구성

## 피해야 할 말

- “실제 기업 미래를 예측합니다.”
- “투자 판단에 사용할 수 있습니다.”
- “정확도가 높습니다.”

## 추천하는 말

- “실제 금융 의사결정 모델이 아니라, 금융 도메인에서 필요한 ML 서비스 구조와 검증 방식을 보여주는 포트폴리오입니다.”
- “성능 주장이 아니라 leakage-aware validation, API, monitoring, artifact design을 보여주는 데 초점을 뒀습니다.”
- “GitHub에서 첫 화면만 봐도 서비스 구조와 산출물을 이해할 수 있도록 README visual을 구성했습니다.”

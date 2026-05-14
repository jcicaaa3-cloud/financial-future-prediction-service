# Quarterly Financial Risk Scoring Service — 한국어 소개

이 프로젝트는 “금융 미래 예측 AI”라고 과장하기보다, **금융 도메인의 ML 결과물을 서비스 형태로 설계하고 검증하고 보여주는 포트폴리오**로 정리한 버전입니다.

## 한 줄 설명

분기 재무제표, 시장 지표, 거시 지표, 공시 기반 위험 신호를 입력받아 다음 분기 재무 악화 리스크를 산출하는 **FastAPI 기반 ML 리스크 스코어링 서비스**입니다.

## 왜 장난감처럼 보이지 않게 바꿨는가

| 약해 보이는 포인트 | 보강한 방식 |
|---|---|
| 단순 모델 실행처럼 보임 | FastAPI API, batch scoring, Docker, CI 추가 |
| 성능 주장 근거가 약함 | chronological split, walk-forward evaluation, baseline leaderboard 추가 |
| 출력물이 단순함 | decision packet, markdown report, LLM prompt, static dashboard 생성 |
| 운영 감각이 안 보임 | data quality report, quarter drift smoke check 추가 |
| GitHub 첫 화면이 밋밋함 | README hero, dashboard preview, architecture diagram, pipeline GIF 추가 |


## GitHub Pages 사이트까지 포함

이번 버전은 저장소만 보는 게 아니라, 리뷰어가 브라우저에서 바로 눌러볼 수 있는 정적 사이트를 포함합니다.

```text
site/index.html
site/styles.css
site/app.js
.github/workflows/pages.yml
```

예상 공개 주소:

```text
https://jcicaaa3-cloud.github.io/financial-future-prediction-service/
```

GitHub Pages는 FastAPI 서버를 실행할 수 없기 때문에, 사이트 데모는 synthetic sample과 설명 가능한 휴리스틱 scoring으로 decision packet을 즉시 생성합니다. 실제 CSV 검증, feature engineering, 모델 학습/평가, artifact 생성은 로컬 또는 별도 서버에서 FastAPI로 실행합니다.

브라우저 데모 구성:

- 회사 샘플 선택
- margin, debt ratio, current ratio, volatility, disclosure risk 조정
- risk score와 risk factor 즉시 갱신
- decision packet JSON 복사/다운로드
- pipeline GIF, architecture image, dashboard preview 표시

## 실행 순서

```bash
pip install -r requirements.txt
python run_demo.py --company-id C003
python scripts/build_portfolio_snapshot.py --company-id C003
pytest -q
```

브라우저에서 아래 파일을 열면 포트폴리오용 대시보드를 바로 볼 수 있습니다.

```text
examples/portfolio_snapshot/portfolio_dashboard.html
```

## 면접에서 이렇게 설명하면 좋습니다

> 이 프로젝트는 실제 투자 판단 모델이 아니라, 금융 도메인에서 ML 서비스를 만들 때 필요한 데이터 계약, 누수 방지형 feature engineering, 시간 기준 검증, API serving, monitoring artifact, model card, dashboard 산출물을 한 번에 보여주기 위한 포트폴리오입니다.

## 피해야 할 표현

- 실제 기업 미래를 예측합니다.
- 투자 판단에 사용할 수 있습니다.
- 모델 정확도가 높습니다.

## 추천 표현

- 금융 도메인 ML 서비스를 안전하게 구조화한 포트폴리오입니다.
- synthetic data 기반이므로 실제 성능 주장이 아니라 engineering flow를 보여줍니다.
- leakage-aware validation, API boundary, monitoring artifact, dashboard storytelling에 초점을 맞췄습니다.

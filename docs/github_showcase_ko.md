# GitHub Showcase Guide

이 문서는 저장소를 GitHub에 올렸을 때 첫 화면이 포트폴리오답게 보이도록 정리한 가이드입니다.

## 1. README 상단에서 보여줄 이미지

README는 아래 이미지를 사용합니다.

```text
docs/assets/github_hero.png
docs/assets/pipeline_flow.gif
docs/assets/architecture_diagram.png
docs/assets/dashboard_preview.png
docs/assets/api_contract_preview.png
docs/assets/github_social_preview.png
```

이미지를 같이 커밋하지 않으면 README가 깨져 보이므로 `docs/assets/` 폴더를 반드시 포함하세요.

## 2. Repository About 추천

```text
Leakage-aware quarterly financial risk scoring service with FastAPI, batch scoring, chronological validation, model leaderboard, monitoring artifacts, and portfolio dashboard.
```

## 3. Topics 추천

```text
python
fastapi
machine-learning
financial-analytics
risk-scoring
mlops
portfolio-project
tabular-data
time-series
model-validation
```

## 4. GitHub Social Preview 추천

GitHub 저장소 `Settings → Social preview`에 아래 이미지를 넣으면 포트폴리오 링크 공유 시 첫인상이 좋아집니다.

```text
docs/assets/github_social_preview.png
```

## 5. 면접 시 설명 순서

1. README 상단 hero image로 프로젝트 범위를 설명합니다.
2. `docs/assets/pipeline_flow.gif`를 보며 CSV부터 dashboard까지의 end-to-end 흐름을 설명합니다.
3. `examples/portfolio_snapshot/portfolio_dashboard.html`을 브라우저에서 열어 결과물을 보여줍니다.
4. `app/main.py`에서 FastAPI endpoint를 보여줍니다.
5. `docs/evaluation_protocol.md`에서 time-based validation과 leakage-aware framing을 설명합니다.

## 6. 강조할 문장

> 이 프로젝트는 real-world investment model이라고 주장하지 않습니다. 대신 금융 도메인 데이터를 다루는 ML 결과물을 API, 검증, 모니터링, 문서, 대시보드까지 서비스 형태로 구조화한 포트폴리오입니다.

## 7. 피해야 할 표현

- “주가 예측 AI”
- “실제 투자 판단 가능”
- “정확하게 기업 미래를 예측”
- “논문급 성능”

대신 아래 표현을 사용하세요.

- “분기 재무 악화 리스크 스코어링”
- “leakage-aware validation”
- “service-style ML pipeline”
- “reviewer-friendly decision packet”
- “synthetic sample data based engineering demonstration”

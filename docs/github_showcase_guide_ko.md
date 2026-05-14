# GitHub 쇼케이스 가이드

V4는 기능 추가보다 **GitHub 첫 화면에서 포트폴리오 완성도가 보이도록** 정리한 버전입니다.

## 1. Repository description

GitHub repository 오른쪽 About 영역에는 아래 문장을 추천합니다.

```text
Leakage-aware financial risk scoring service with FastAPI, walk-forward validation, model leaderboard, monitoring artifacts, and portfolio dashboard.
```

## 2. Topics

```text
python
fastapi
machine-learning
mlops
financial-analysis
risk-scoring
portfolio-project
tabular-data
```

## 3. Social preview 이미지

GitHub Settings → Social preview에서 아래 파일을 업로드하세요.

```text
docs/assets/github_social_preview.png
```

이 이미지는 저장소를 공유했을 때 링크 미리보기에서 보이는 용도입니다.

## 4. README에서 바로 보이는 이미지

README에는 아래 시각 자료가 들어갑니다.

| 파일 | 용도 |
|---|---|
| `docs/assets/github_hero.png` | README 최상단 hero banner |
| `docs/assets/dashboard_preview.png` | 포트폴리오 대시보드 preview |
| `docs/assets/pipeline_flow.gif` | 데이터 → feature → model → API → dashboard 흐름 animation |
| `docs/assets/architecture_diagram.png` | 전체 시스템 아키텍처 |
| `docs/assets/github_social_preview.png` | GitHub social preview |

## 5. 포트폴리오 리뷰어에게 보여줄 순서

1. README 상단 hero와 한 줄 설명
2. `What this project proves` 표
3. `pipeline_flow.gif` 흐름도
4. `architecture_diagram.png` 아키텍처
5. `examples/portfolio_snapshot/portfolio_dashboard.html`
6. API endpoint table
7. `docs/model_card.md`와 `docs/evaluation_protocol.md`

## 6. 면접용 30초 설명

> 금융 예측 성능을 과장하는 프로젝트가 아니라, 금융 ML 결과물을 서비스 형태로 만들 때 필요한 데이터 계약, 누수 방지형 feature engineering, 시간 기준 검증, API serving, monitoring artifact, model card, dashboard까지 묶은 포트폴리오입니다. Synthetic data라 실제 투자 성능을 주장하지 않고, 대신 engineering flow와 안전한 framing을 보여줍니다.

## 7. 커밋 메시지 추천

```text
Upgrade GitHub showcase with visual README assets and portfolio review flow
```

# 프로젝트 카드: Quarterly Financial Risk Scoring Service

## 프로젝트 목적

분기 재무제표, 시장 지표, 거시 지표, 공시 기반 위험 신호를 입력받아 다음 분기 재무 악화 가능성을 점수화하는 **ML 기반 FastAPI 백엔드 서비스**입니다.

이 프로젝트는 실제 투자/대출 판단 모델이 아니라, **금융 도메인 ML 프로젝트를 서비스 형태로 설계하고 검증하고 문서화하고 GitHub에서 보기 좋게 보여주는 역량**을 보여주기 위한 포트폴리오입니다.

## 핵심 기능

- CSV data contract 및 schema validation
- company-quarter panel 생성
- leakage-aware feature engineering
- chronological split / walk-forward evaluation
- dummy, logistic regression, random forest baseline leaderboard
- FastAPI single prediction API
- FastAPI batch prediction API
- model-used feature explanation packet
- data quality report
- quarter drift smoke check
- markdown risk report
- LLM analysis prompt packet
- static HTML portfolio dashboard
- Docker / GitHub Actions CI / pytest
- GitHub README hero image, pipeline GIF, architecture diagram, social preview asset

## 실행 방법

```bash
pip install -r requirements.txt
python run_demo.py --company-id C003
pytest -q
```

포트폴리오 스냅샷 생성:

```bash
python scripts/build_portfolio_snapshot.py --company-id C003
```

브라우저에서 열기:

```text
examples/portfolio_snapshot/portfolio_dashboard.html
```

README 이미지 재생성:

```bash
python scripts/render_github_assets.py
```

## 면접에서 강조할 부분

- “성능 좋은 금융 예측 모델”이 아니라 “금융 ML 서비스를 안전하게 구조화한 프로젝트”라고 설명한다.
- synthetic data를 사용했기 때문에 real-world accuracy를 주장하지 않는다.
- 대신 leakage 방지, time-based validation, API, monitoring, model card, artifact design, GitHub storytelling을 강조한다.
- README 이미지와 대시보드는 채용자가 코드를 실행하지 않아도 프로젝트 구조를 빠르게 이해하도록 만든 장치라고 설명한다.

## 한 줄 설명

> Leakage-aware financial risk scoring service with FastAPI inference, batch scoring, chronological validation, walk-forward evaluation, baseline leaderboard, monitoring artifacts, and a GitHub-ready portfolio dashboard.

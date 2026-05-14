# GitHub 포트폴리오 polish guide

이 문서는 저장소를 GitHub에 올렸을 때 첫 화면이 포트폴리오처럼 보이도록 정리한 체크리스트입니다.

## 1. Repository description

GitHub 우측 About 설명은 아래 문장으로 넣는 것을 추천합니다.

```text
Leakage-aware quarterly financial risk scoring service with FastAPI, batch scoring, chronological validation, model leaderboard, monitoring artifacts, and portfolio dashboard.
```

## 2. Topics

아래 topic을 넣으면 검색성과 포트폴리오 맥락이 좋아집니다.

```text
python
fastapi
machine-learning
financial-analysis
risk-scoring
tabular-data
mlops
portfolio-project
docker
model-monitoring
```

## 3. 첫 커밋 이후 권장 commit order

한 번에 다 올려도 되지만, 면접자가 commit history를 볼 가능성을 고려하면 아래 순서가 더 자연스럽습니다.

```bash
git add README.md docs/assets docs/github_polish_guide_ko.md docs/reviewer_walkthrough.md docs/interview_defense_ko.md CHANGELOG_V4.md
git commit -m "Polish portfolio README with visual architecture and dashboard assets"

git add app src tests scripts examples docs pyproject.toml Makefile .github Dockerfile docker-compose.yml requirements.txt
git commit -m "Package financial risk scoring service with API, validation, monitoring, and CI"
```

이미 ZIP 전체를 한 번에 덮어써야 한다면 아래 커밋 메시지를 쓰면 됩니다.

```bash
git add .
git commit -m "Refactor project into portfolio-grade financial risk scoring service"
```

## 4. README 이미지 관련

README에는 로컬 이미지 파일을 사용합니다.

```text
docs/assets/github_hero.png
docs/assets/pipeline_flow.gif
docs/assets/architecture_diagram.png
docs/assets/dashboard_preview.png
docs/assets/api_contract_preview.png
```

외부 이미지 호스팅을 쓰지 않기 때문에 GitHub에 올리면 바로 렌더링됩니다. PNG와 SVG를 둘 다 넣어둔 이유는 PNG는 GitHub README에서 가장 안정적으로 보이고, SVG는 수정이 쉬운 원본 역할을 하기 때문입니다.

## 5. Pin repo용 한 줄 소개

GitHub 프로필 pinned repository 설명에는 이 문장을 쓰면 좋습니다.

```text
FastAPI 기반 금융 리스크 스코어링 ML 백엔드. 시간 기준 검증, 모델 leaderboard, 모니터링, 정적 대시보드까지 포함한 포트폴리오 프로젝트.
```

## 6. 면접에서 방어해야 하는 포인트

이 프로젝트는 논문형 성능 경쟁 프로젝트가 아니라 서비스형 ML 엔지니어링 포트폴리오입니다. 따라서 설명 초점은 아래 순서가 좋습니다.

1. 문제 정의를 “미래 예측”이 아니라 “다음 분기 재무 악화 리스크 신호”로 좁혔다.
2. synthetic data 한계를 명시하고, real-data adapter template을 분리했다.
3. random split이 아니라 chronological/walk-forward 검증을 사용했다.
4. 모델 하나만 쓰지 않고 baseline leaderboard를 만들었다.
5. FastAPI, Docker, CI, monitoring, dashboard까지 연결해 서비스화 감각을 보여줬다.

## 7. 제출 전 확인

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python run_demo.py --company-id C003
python scripts/build_portfolio_snapshot.py --company-id C003
```

브라우저로 아래 파일을 열어 시각적으로 깨지는 부분이 없는지 확인합니다.

```text
examples/portfolio_snapshot/portfolio_dashboard.html
```

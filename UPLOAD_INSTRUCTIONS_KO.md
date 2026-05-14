# GitHub 업로드 방법 — V4 GitHub Showcase Edition

## 1. ZIP 풀기

```bash
unzip financial-future-prediction-service-v4-github-showcase.zip
cd financial-future-prediction-service-v4
```

## 2. 로컬 검증

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
python run_demo.py --company-id C003
python scripts/build_portfolio_snapshot.py --company-id C003
```

README 이미지 asset을 다시 만들고 싶으면:

```bash
python scripts/render_github_assets.py --force
```

## 3. 기존 저장소에 반영

기존 repo 루트에서 새 브랜치를 만든 뒤 파일을 덮어쓰는 방식을 추천합니다.

```bash
git checkout -b portfolio-v4-github-showcase
# ZIP 내부 파일 복사
pytest -q
python scripts/build_portfolio_snapshot.py --company-id C003
git add .
git commit -m "Upgrade GitHub showcase for financial risk scoring portfolio"
git push origin portfolio-v4-github-showcase
```

## 4. GitHub repository description 추천

```text
Leakage-aware financial risk scoring service with FastAPI, walk-forward validation, model leaderboard, monitoring artifacts, and portfolio dashboard.
```

## 5. GitHub topics 추천

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

## 6. Social preview 설정

GitHub Settings → Social preview에 아래 파일을 업로드하세요.

```text
docs/assets/github_social_preview.png
```

## 7. README 첫 화면에서 보여줄 것

- 프로젝트가 투자 추천이 아니라 포트폴리오용 ML service engineering 프로젝트임을 명시
- `docs/assets/github_hero.png`로 첫 화면을 시각화
- `pipeline_flow.gif`로 데이터 → feature → model → API → dashboard 흐름을 보여줌
- `architecture_diagram.png`로 시스템 설계를 한눈에 보여줌
- `examples/portfolio_snapshot/portfolio_dashboard.html`로 실행 결과를 바로 확인하게 함

## 8. PR 설명 추천

```text
This update turns the repository into a GitHub-ready portfolio showcase. It adds visual README assets, an animated pipeline flow, a dashboard preview, a social preview image, a Korean README, and a GitHub showcase guide while preserving the FastAPI/ML validation pipeline.
```

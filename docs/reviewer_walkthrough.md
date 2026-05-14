# 5-minute reviewer walkthrough

This walkthrough is for a hiring manager or reviewer who wants to understand the project quickly.

## 1. Read the first screen

Start with `README.md`. The hero image, badge row, and architecture diagram should communicate that this is an ML backend/service project rather than a notebook-only demo.

## 2. Open the static dashboard

```bash
python scripts/build_portfolio_snapshot.py --company-id C003
```

Then open:

```text
examples/portfolio_snapshot/portfolio_dashboard.html
```

This shows the generated risk scores, validation preview, feature snapshot, and monitoring output.

## 3. Inspect the API boundary

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Key endpoints:

- `POST /v1/predictions`
- `POST /v1/batch-predictions`
- `GET /v1/models/latest/leaderboard`
- `GET /v1/monitoring/latest/data-quality`
- `GET /v1/monitoring/latest/drift`

## 4. Check validation and model discipline

Look at:

```text
src/financial_risk_scoring/evaluation/walk_forward.py
src/financial_risk_scoring/models/train.py
docs/evaluation_protocol.md
docs/model_card.md
```

The point is not to claim real financial alpha from synthetic data. The point is to show validation hygiene and baseline comparison.

## 5. Check portfolio narrative

Useful files:

```text
PROJECT_CARD_KO.md
PORTFOLIO_PLAYBOOK_KO.md
docs/portfolio_case_study_ko.md
docs/interview_defense_ko.md
docs/github_polish_guide_ko.md
```

These files explain how to present the project without overclaiming.

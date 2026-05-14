# Hiring Manager Brief

## What this project demonstrates

This project is designed to show practical ML engineering rather than research novelty.

It demonstrates:

- backend-aware ML pipeline design
- data contract validation
- tabular feature engineering
- time-based validation
- baseline model comparison
- FastAPI inference service
- batch scoring
- static dashboard generation
- monitoring artifact design
- honest model-card limitations

## Why it is not framed as a research paper

The included data is synthetic, so the project should not claim real forecasting accuracy. The value is in the structure: how data flows from CSV contracts into features, models, API responses, reports, dashboards, and monitoring packets.

## Best review path

1. Read `README.md`.
2. Run `python scripts/build_portfolio_snapshot.py --company-id C003`.
3. Open `examples/portfolio_snapshot/portfolio_dashboard.html`.
4. Inspect `app/main.py` and `src/financial_risk_scoring/service/pipeline.py`.
5. Run `pytest -q`.

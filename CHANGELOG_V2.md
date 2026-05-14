# V2 Changelog

## Changed

- Repositioned the project from vague financial future prediction to quarterly financial risk scoring.
- Rewrote README for portfolio review and reviewer clarity.
- Moved generated artifacts to `artifacts/` and added `.gitignore` rules.

## Added

- FastAPI application with prediction, retrieval, metrics, and health endpoints.
- Dockerfile and docker-compose configuration.
- GitHub Actions CI workflow.
- Pytest tests for data contract, feature engineering, pipeline smoke, and API contract.
- Chronological split and walk-forward evaluation utilities.
- Baseline comparison across Dummy, Logistic Regression, and RandomForest classifiers.
- Data-source adapter templates for OpenDART and KRX-style ingestion.
- Korean project card and portfolio positioning notes.

# Architecture

<p align="center">
  <img src="assets/architecture_diagram.png" alt="System architecture diagram" width="100%" />
</p>

This project is intentionally structured as a small ML service rather than a notebook-only demo.

## Flow

1. **Input layer** accepts five CSV files from one input directory.
2. **Feature factory** validates schema, builds a company-quarter panel, creates ratios/trend features, and keeps labels separate from prediction-time fields.
3. **Model layer** trains and compares dummy, logistic regression, and random forest baselines with chronological and walk-forward validation.
4. **Service layer** exposes single-company prediction, batch scoring, metrics, leaderboard, feature-importance, and monitoring endpoints.
5. **Reviewer layer** writes decision packets, markdown reports, LLM prompt packets, dashboard HTML, chronological metrics, walk-forward metrics, data-quality reports, and drift reports.

## Current service boundary

The FastAPI service runs the pipeline synchronously for portfolio clarity. A production version would normally separate this into:

- async job queue,
- persistent model registry,
- database-backed request tracking,
- scheduled retraining jobs,
- monitoring dashboards,
- audit logs,
- access control,
- model-risk approval workflow.

## GitHub rendering note

The README uses committed PNG/GIF/SVG assets in `docs/assets/` so the GitHub landing page has clean diagrams and animated flow visuals instead of relying only on ASCII arrows or code blocks.

Regenerate visual assets with:

```bash
python scripts/render_github_assets.py
```

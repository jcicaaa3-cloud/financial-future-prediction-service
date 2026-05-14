# API Contract

Base service: `Quarterly Financial Risk Scoring Service` version `0.4.0`.

## `GET /health`

Returns service status.

```json
{"status":"ok","service":"quarterly-financial-risk-scoring-service","version":"0.4.0"}
```

## `POST /v1/predictions`

Run a single-company prediction pipeline.

Request:

```json
{
  "company_id": "C003",
  "input_dir": "data/input/sample",
  "artifact_dir": "artifacts"
}
```

Response includes:

- `request_id`
- `scores`
- `risk_level`
- `top_risk_factors`
- `positive_factors`
- `feature_snapshot`
- `model_explanations`
- `decision_packet_path`
- `report_path`
- `llm_prompt_path`
- `dashboard_path`
- `metrics_path`
- `data_quality_path`
- `drift_report_path`

## `POST /v1/batch-predictions`

Train once and score multiple companies.

Request:

```json
{
  "company_ids": ["C001", "C003", "C007"],
  "input_dir": "data/input/sample",
  "artifact_dir": "artifacts"
}
```

Response includes compact company-level summaries and paths to generated dashboards.

## `GET /v1/predictions/{request_id}`

Fetch a saved result packet. For batch child packets, the API also searches nested `decision_packets/` directories.

## `GET /v1/models/latest/metrics`

Fetch latest chronological time-split metrics.

## `GET /v1/models/latest/leaderboard`

Fetch baseline leaderboard rows across targets and models.

## `GET /v1/models/latest/feature-importance`

Fetch global feature-importance packet for selected models. This is a debugging and portfolio explanation aid, not causal evidence.

## `GET /v1/monitoring/latest/data-quality`

Fetch data quality gates from the latest generated request.

## `GET /v1/monitoring/latest/drift`

Fetch latest-quarter drift smoke check from the latest generated request.

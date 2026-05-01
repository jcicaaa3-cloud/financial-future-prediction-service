# Service API contract

## Purpose

This document describes a possible API shape for serving model results.

## Endpoint: create prediction

Method: POST

Path: /api/financial-predictions/run

Request fields:

- company_id
- input_dir
- model_version

Response fields:

- request_id
- company_id
- status
- created_at

## Endpoint: get prediction result

Method: GET

Path: /api/financial-predictions/{request_id}

Response fields:

- company_id
- company_name
- quarter
- growth_possibility_score
- risk_signal_score
- financial_health_score
- positive_factors
- risk_factors
- model_metrics
- report_path
- decision_packet_path
- disclaimer

## Endpoint: get stress test

Method: GET

Path: /api/financial-predictions/{request_id}/stress-test

Response fields:

- base_scores
- scenario_name
- changed_inputs
- scenario_scores
- score_delta

## Notes

The current repository exports files instead of running a web server. The output format was prepared so a backend service can adopt it with minimal conversion work.

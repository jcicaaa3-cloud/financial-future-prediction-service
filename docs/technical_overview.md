# Technical overview

## Purpose

The project builds a financial forecasting pipeline at company-quarter level. It converts multi-source tabular data into model-ready features, trains baseline models, and exports results in formats that can be served through an API or dashboard.

## Data units

The main key is company_id and quarter. Each row represents one company at one quarter.

Input sources:

- Company master data
- Quarterly financial statements
- Quarterly market indicators
- Quarterly macro indicators
- Quarterly disclosure-derived fields

## Processing flow

1. Validate required CSV files and columns.
2. Merge inputs into a company-quarter panel.
3. Create financial ratios and growth variables.
4. Create rolling variables across previous quarters.
5. Create future labels for growth, risk, and health.
6. Train baseline models.
7. Generate company-level prediction JSON.
8. Build decision packet JSON and stress test JSON.
9. Create Markdown report and LLM prompt packet.

## Model outputs

The system exports three score groups.

- Growth possibility score from 0 to 100
- Risk signal score from 0 to 100
- Financial health score from 0 to 100

## Service output

The decision packet is designed for API usage. It includes company identity, quarter, score values, factor lists, model metrics, and disclaimer text.

## Current limits

The sample data is artificial. The included metrics verify execution flow, file formats, and model training behavior. They do not verify market performance or investment value.

For research or production evaluation, the next step is chronological validation with real company filings, market data, macro data, and disclosure text.

# financial-future-prediction-service

Company-quarter financial forecasting pipeline for portfolio review.

This repository shows a full path from CSV input files to machine learning predictions, risk scoring, report output, and an LLM-ready memo packet. The project is written as a service-oriented financial AI prototype rather than a notebook demo.

## Project scope

The system receives company-quarter data and estimates three signals for the next quarter.

- Growth possibility score
- Risk signal score
- Financial health score

The pipeline combines financial statements, market indicators, macro indicators, and disclosure-derived risk fields. It then builds a panel dataset, creates ratios and rolling fields, trains baseline models, and exports results in JSON and Markdown formats.

## Repository layout

- src/data: input validation, sample data generation, panel construction
- src/features: financial ratios, rolling variables, proxy variables, future labels
- src/models: model training and company-level prediction
- src/evaluation: time-based validation script
- src/service: decision packet and stress test output
- src/llm: prompt packet builder for report generation
- docs: data contract, evaluation plan, model card, API contract, portfolio notes
- data/input/sample: artificial sample CSV files for execution checks
- data/input/templates: empty input templates for real data collection
- outputs: example outputs generated from the sample data
- tests: smoke test and input schema test

## Input files

The default input path expects five CSV files.

- company_master.csv
- financial_statement_quarterly.csv
- market_quarterly.csv
- macro_quarterly.csv
- disclosure_features_quarterly.csv

Column details are documented in docs/input_data_format.md and docs/data_contract.md.

## Run locally

Create a virtual environment and install dependencies.

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

On Windows PowerShell, activate with this command.

.venv\Scripts\Activate.ps1

Run the default demo.

python run_demo.py

Run with CSV input files.

python run_with_input.py --input-dir data/input/sample --company-id C003

Run the smoke test.

python tests/smoke_test.py
python tests/test_input_schema.py

## Output files

A normal run creates these result groups.

- outputs/predictions: company-level prediction JSON
- outputs/decision_packets: API-style decision packet JSON
- outputs/stress_tests: scenario response JSON
- outputs/reports: Korean decision-support report
- outputs/llm_inputs: structured prompt packet for LLM report writing
- outputs/evaluation: time-split validation metrics

## Model design

The current implementation uses RandomForest models as a baseline. The value of the project is in the data contract, feature pipeline, label design, validation flow, and service output format. The same input and output layout can support LightGBM, XGBoost, CatBoost, temporal models, or tabular transformer models.

## Data notice

This repository does not include private financial records, account data, API keys, credentials, or proprietary datasets. The sample CSV files are artificial and are included to demonstrate the expected schema and execution flow.

The example scores in outputs are pipeline validation results. They are not investment advice and should not be used for trading, lending, credit screening, or real corporate evaluation.

## Portfolio summary

This project was prepared to show backend-aware AI engineering for financial analysis. It covers input contracts, feature engineering, baseline modeling, evaluation, report output, and an LLM integration point that can be connected to a dashboard or API service.

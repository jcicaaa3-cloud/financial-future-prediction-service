# Input CSV guide

This folder contains artificial CSV files used to test the execution flow.

## Required files

- company_master.csv
- financial_statement_quarterly.csv
- market_quarterly.csv
- macro_quarterly.csv
- disclosure_features_quarterly.csv

## Sample folder

data/input/sample contains filled example files. They are artificial and are included for local execution checks.

## Template folder

data/input/templates contains empty templates with the required columns.

## How to run

python run_with_input.py --input-dir data/input/sample --company-id C003

## Data policy

Do not place private company records, credentials, API tokens, or confidential files in this repository. Real data should be stored outside GitHub and loaded through a controlled input directory.

## LLM layer

The LLM layer receives structured prediction results and writes a decision-support memo. It does not replace the numeric model. It receives fields such as company name, score values, positive factors, risk factors, model metrics, and disclaimers.

# Input data format

## Overview

The pipeline expects five CSV files in one input directory. Each file must keep the column names listed below.

## company_master.csv

Columns:

- company_id
- company_name
- sector

Example row:

C003, SampleCompany_003, Retail

## financial_statement_quarterly.csv

Columns:

- company_id
- quarter
- revenue
- operating_income
- net_income
- total_assets
- total_debt
- total_equity
- current_assets
- current_liabilities
- operating_cash_flow
- interest_expense

## market_quarterly.csv

Columns:

- company_id
- quarter
- market_cap
- stock_return_3m
- volatility_3m
- volume_change_3m

## macro_quarterly.csv

Columns:

- quarter
- macro_rate
- fx_rate
- inflation
- business_cycle_index

## disclosure_features_quarterly.csv

Columns:

- company_id
- quarter
- disclosure_risk_score
- rnd_ratio
- major_event_flag
- disclosure_summary_ko

## Execution example

python run_with_input.py --input-dir data/input/sample --company-id C003

## Real data extension

For Korean listed companies, financial statement data can be collected from DART or Open DART, market data from KRX or a market data vendor, macro data from public economic sources, and disclosure text from company filings.

The disclosure_summary_ko field can store a cleaned Korean summary created by a separate preprocessing step.

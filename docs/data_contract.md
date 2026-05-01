# Data contract

## Goal

This document defines the input files required by the financial forecasting pipeline.

## Required files

company_master.csv

Required columns:

- company_id
- company_name
- sector

financial_statement_quarterly.csv

Required columns:

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

market_quarterly.csv

Required columns:

- company_id
- quarter
- market_cap
- stock_return_3m
- volatility_3m
- volume_change_3m

macro_quarterly.csv

Required columns:

- quarter
- macro_rate
- fx_rate
- inflation
- business_cycle_index

disclosure_features_quarterly.csv

Required columns:

- company_id
- quarter
- disclosure_risk_score
- rnd_ratio
- major_event_flag
- disclosure_summary_ko

## Validation rules

- company_id must match across company, financial, market, and disclosure files.
- quarter must use a consistent format such as 2024Q3.
- Numeric columns should not contain text labels.
- Missing values should be handled before model training.
- Real data should be loaded from a controlled storage path outside public GitHub.

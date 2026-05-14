# Data contract

The service expects five CSV files in one directory. All files should be UTF-8 or UTF-8-SIG encoded.

## `company_master.csv`

Required columns:

- `company_id`
- `company_name`
- `sector`

## `financial_statement_quarterly.csv`

Required columns:

- `company_id`
- `quarter`
- `revenue`
- `operating_income`
- `net_income`
- `total_assets`
- `total_debt`
- `total_equity`
- `current_assets`
- `current_liabilities`
- `operating_cash_flow`
- `interest_expense`

## `market_quarterly.csv`

Required columns:

- `company_id`
- `quarter`
- `market_cap`
- `stock_return_3m`
- `volatility_3m`
- `volume_change_3m`

## `macro_quarterly.csv`

Required columns:

- `quarter`
- `macro_rate`
- `fx_rate`
- `inflation`
- `business_cycle_index`

## `disclosure_features_quarterly.csv`

Required columns:

- `company_id`
- `quarter`
- `disclosure_risk_score`
- `rnd_ratio`
- `major_event_flag`
- `disclosure_summary_ko`

## Validation rules

- `quarter` must use `YYYYQn`, for example `2025Q1`.
- Numeric columns must be numeric and non-empty.
- `company_id` values must match across company, financial, market, and disclosure files.
- Macro data must contain all quarters used by company-quarter rows.
- Real/private data should be stored outside public GitHub.

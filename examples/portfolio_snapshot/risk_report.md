# Quarterly Financial Risk Report

## Company

- Company: SampleCompany_003 (C003)
- Sector: IT
- Quarter: 2025Q3
- Feature available at: 2025-11-14
- Risk level: **low**

## Scores

| Signal | Score |
|---|---:|
| Margin deterioration risk | 0.3618 |
| Market drawdown proxy risk | 0.2000 |
| Liquidity stress risk | 0.0000 |
| Financial health score | 0.8127 |

## Top risk factors

- No major risk factor identified by simple rules

## Positive factors

- Healthy current ratio
- Strong operating margin
- Solid operating cash-flow margin
- Positive revenue growth

## Feature snapshot

| Feature | Value |
|---|---:|
| operating_margin | 0.150828 |
| net_margin | 0.086896 |
| current_ratio | 5.534034 |
| debt_ratio | 0.46634 |
| interest_coverage | 18.133627 |
| ocf_margin | 0.150374 |
| revenue_growth_qoq | 0.074277 |
| stock_return_3m | 0.02297 |
| volatility_3m | 0.27428 |
| disclosure_risk_score | 0.23154 |
| major_event_flag | 0.0 |
| macro_rate | 4.114 |

## Model-used explanation signals

### target_margin_deterioration
| Feature | Current value | Global importance | Interpretation hint |
|---|---:|---:|---|
| operating_margin_change_qoq | -0.015179 | 0.212815 | lower values usually increase profitability risk |
| operating_margin | 0.150828 | 0.056073 | lower values usually increase profitability risk |
| operating_income | 55045.17 | 0.051732 | model-used feature; inspect with domain context |
| net_income | 31713.09 | 0.04864 | model-used feature; inspect with domain context |
| ocf_margin | 0.150374 | 0.046521 | lower values usually increase cash-flow risk |
### target_market_drawdown_proxy
| Feature | Current value | Global importance | Interpretation hint |
|---|---:|---:|---|
### target_liquidity_stress
| Feature | Current value | Global importance | Interpretation hint |
|---|---:|---:|---|
| debt_to_equity | 0.873853 | 0.116977 | higher values usually increase leverage risk |
| operating_income | 55045.17 | 0.088397 | model-used feature; inspect with domain context |
| operating_margin_roll4_mean | 0.149767 | 0.069188 | lower values usually increase profitability risk |
| ocf_margin | 0.150374 | 0.061388 | lower values usually increase cash-flow risk |
| interest_coverage | 18.133627 | 0.059747 | lower values usually increase liquidity and debt-service risk |

## Model note

This is a baseline ML risk-scoring output generated from synthetic or user-supplied CSV data. Feature importance is a debugging and portfolio explanation aid, not causal evidence. It is not investment advice, lending advice, credit screening, or corporate-rating advice.
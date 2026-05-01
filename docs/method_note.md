# Method note

## Data preparation

The pipeline merges company master, financial statement, market, macro, and disclosure feature files into a company-quarter panel.

## Feature engineering

Financial variables are converted into ratios and growth variables. Rolling statistics are created when multiple quarters are available.

Example groups:

- Profitability ratios
- Liquidity ratios
- Leverage ratios
- Market movement variables
- Macro variables
- Disclosure-derived risk score

## Label design

Future labels are created by shifting target values to the next quarter. This lets the model learn from current and past information while predicting a future state.

## Baseline model

The baseline uses RandomForest models. This choice gives a stable starting point for tabular data and supports feature importance output.

## Reporting

The final step writes machine-readable JSON and human-readable Markdown. The same result packet can be passed to an API, a dashboard, or an LLM memo writer.

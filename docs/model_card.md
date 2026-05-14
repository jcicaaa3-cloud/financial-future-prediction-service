# Model Card

## Model type

Baseline tabular classifiers for quarterly financial risk signals. The training utility compares:

- Dummy prior baseline
- Logistic regression
- Random forest

For each target, the selected model is the baseline with the strongest available validation score, prioritizing ROC-AUC when possible.

## Targets

- `target_margin_deterioration`
- `target_market_drawdown_proxy`
- `target_liquidity_stress`

Targets are built from next-quarter values and are used only as labels.

## Validation

- Chronological train/test split
- Walk-forward evaluation utility
- Baseline leaderboard
- Data quality report
- Simple latest-quarter drift report

## Explainability

The project includes lightweight global feature importance and a model-used explanation packet for portfolio review. It uses sklearn feature importances or absolute linear coefficients depending on the selected model.

This is not SHAP, not causal inference, and not a guarantee that a feature caused a risk outcome.

## Intended use

Portfolio demonstration of ML engineering and service design.

## Out-of-scope use

- Investment recommendation
- Lending decision
- Credit screening
- Trading signal
- Corporate rating

## Limitations

The included sample data is synthetic. Therefore, validation metrics demonstrate execution flow and evaluation structure, not real financial forecasting accuracy.

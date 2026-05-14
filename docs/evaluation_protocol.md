# Evaluation Protocol

## Goal

Show evaluation hygiene for a financial ML service portfolio project. The goal is not to claim real market performance from synthetic data.

## Splits

The project avoids random-only evaluation. It uses:

- chronological train/test split
- walk-forward evaluation

## Leakage guard

Feature columns are checked for obvious future-label tokens:

- `next_`
- `future_`
- `target_`

Target columns are produced from next-quarter values, but those next-quarter values are not allowed into the model feature list.

## Baselines

The training pipeline compares:

- dummy prior baseline
- logistic regression
- random forest

The leaderboard is exposed both as JSON artifact and API endpoint.

## Metrics

Per target:

- ROC-AUC
- average precision
- F1 at 0.5
- Brier score
- positive rate

## Portfolio caveat

Because bundled data is synthetic, these metrics are not evidence of real financial forecasting performance. They are evidence that the project has a reproducible validation and artifact flow.

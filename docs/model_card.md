# Model card

## Model family

RandomForest baseline models for tabular financial data.

## Prediction targets

- Next-quarter growth signal
- Next-quarter risk signal
- Next-quarter financial health score

## Intended use

- Portfolio demonstration
- Pipeline validation
- Analyst support prototype
- Backend integration prototype

## Not intended for

- Investment advice
- Credit approval
- Automated lending decisions
- Real company rating without verified data and compliance review

## Data used in this repository

The public sample data is artificial. It is included to test schema validation, training, prediction, and report output.

## Evaluation status

The repository includes a time-split evaluation script and example metric output. Real-world evaluation requires verified historical data and chronological holdout testing.

## Known limits

- Sample data does not represent real market behavior.
- RandomForest is a baseline, not the final modeling ceiling.
- Small datasets can produce unstable metrics.
- Real deployment requires monitoring, audit logs, model versioning, and human review.

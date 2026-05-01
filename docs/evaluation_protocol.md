# Evaluation protocol

## Evaluation goal

The evaluation checks whether the model can predict next-quarter signals from past and current-quarter information.

## Recommended split

Use chronological validation. Training data should come from earlier quarters and validation data from later quarters.

Example:

- Train: 2020Q1 to 2023Q4
- Validation: 2024Q1 to 2024Q4

## Metrics

Growth model:

- Accuracy
- F1 score
- ROC AUC

Risk model:

- Accuracy
- F1 score
- ROC AUC

Health model:

- MAE
- RMSE

## Required checks

- Confirm that future labels are not leaked into input features.
- Confirm that the same company-quarter row does not appear in both train and validation sets.
- Compare random split results with chronological split results.
- Report sector-level performance when enough data is available.
- Save metrics in outputs/evaluation.

## Current package status

The included metrics come from artificial sample data. They confirm execution flow and metric generation. They do not support claims about real financial forecasting accuracy.

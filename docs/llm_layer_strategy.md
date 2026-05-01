# LLM layer strategy

## Positioning

The LLM layer writes a memo from structured model outputs. It does not create the numeric scores.

## Input to the LLM layer

The prompt packet contains:

- Company profile
- Target quarter
- Growth score
- Risk score
- Health score
- Positive factor list
- Risk factor list
- Top model features
- Model metrics
- Disclaimer

## Guardrails

The prompt should instruct the model to use the provided JSON fields and avoid unsupported facts. The memo should include a disclaimer and avoid investment advice.

## Reason for separation

Separating numeric prediction and text generation makes the system easier to audit. The machine learning model produces the score values. The LLM writes a readable memo from the locked result packet.

## Upgrade path

The LLM provider can be changed without changing the feature pipeline or prediction output format. The adapter can call an external LLM API, a local model, or a rule-based report writer.

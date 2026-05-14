# ADR-002: Use chronological and walk-forward validation

## Decision

The evaluation flow uses chronological splitting and walk-forward evaluation rather than relying only on random train/test splits.

## Rationale

Company-quarter data has temporal ordering. Random splits can leak future distribution information and overstate apparent performance. Chronological validation better matches the intended inference setting.

## Consequences

- Metrics are presented as engineering demonstration metrics on synthetic data.
- The pipeline stores `time_split_metrics.json` and `walk_forward_metrics.json`.
- The README highlights validation hygiene instead of performance overclaiming.

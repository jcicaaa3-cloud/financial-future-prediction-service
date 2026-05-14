# ADR-001: Position the project as risk scoring, not future prediction

## Decision

The project is framed as a quarterly financial risk scoring service rather than a generic future prediction product.

## Rationale

“Future prediction” creates an unrealistic expectation in financial domains. A portfolio project should show careful problem framing, evidence boundaries, and service design. Risk scoring is more defensible because the output is a decision-support signal, not an investment claim.

## Consequences

- README and docs emphasize synthetic sample data and non-investment use.
- Output is a decision packet with risk signals, confidence context, monitoring files, and reports.
- The model card avoids claiming real-world predictive accuracy.

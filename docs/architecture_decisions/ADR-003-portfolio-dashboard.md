# ADR-003: Generate a static dashboard artifact

## Decision

The pipeline generates a dependency-free HTML dashboard for each prediction request.

## Rationale

A portfolio reviewer may not run the full API during first review. A static dashboard makes the output inspectable immediately while still being generated from the same service pipeline.

## Consequences

- `examples/portfolio_snapshot/portfolio_dashboard.html` can be opened directly in a browser.
- README includes dashboard preview images.
- The dashboard is explicitly labeled as a portfolio artifact, not a production financial advisory UI.

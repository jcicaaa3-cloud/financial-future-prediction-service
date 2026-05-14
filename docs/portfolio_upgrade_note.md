# Portfolio upgrade note

The original repository looked toy-like because the name and README implied broad financial future prediction while the implementation was a synthetic-data MVP. V2 fixes this by narrowing the claim and increasing engineering evidence.

## Better framing

Use:

> Quarterly financial risk scoring service

Avoid:

> AI that predicts the future of companies

## Strong reviewer signals

- API server exists and can be run.
- Tests exist and run in CI.
- Artifacts are generated, not committed as source.
- Model card admits limitations.
- Chronological validation is used.
- Data contract is explicit.
- Real-data adapters have a clear integration path.

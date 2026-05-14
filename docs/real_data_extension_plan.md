# Real-data extension plan

## Goal

Move from synthetic sample execution to a limited, reproducible real-data portfolio version.

## Suggested scope

- 30 to 100 listed companies
- 12 to 20 quarters
- OpenDART-style financial statement ingestion
- KRX or vendor-based market data ingestion
- Public macro indicators
- Disclosure-derived risk text summaries

## Engineering steps

1. Implement `OpenDartClient.normalize_financial_statement` account mapping.
2. Implement market data normalization in `KrxClient`.
3. Store real input CSVs outside public GitHub.
4. Commit only schema, adapter code, anonymized sample, and evaluation report.
5. Add a `feature_available_at` audit for every feature group.
6. Evaluate with chronological and walk-forward validation.

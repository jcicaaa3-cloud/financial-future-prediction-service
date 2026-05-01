# Real data extension plan

## Goal

Replace the artificial sample data with verified financial and market data while keeping the existing input contract.

## Data sources to connect

Financial statements:

- DART or Open DART
- Company quarterly reports

Market data:

- KRX
- Market data vendor API

Macro data:

- Interest rate
- Exchange rate
- Inflation
- Business cycle index

Disclosure data:

- Company filings
- Event flags
- Disclosure risk score
- Korean summary text

## Steps

1. Collect company list and sector metadata.
2. Collect quarterly financial statement fields.
3. Collect market indicators by company and quarter.
4. Collect macro indicators by quarter.
5. Create disclosure risk fields from filing text.
6. Save files in the required CSV format.
7. Run schema validation.
8. Run chronological validation.
9. Compare baseline and upgraded models.
10. Save metrics and model cards for each version.

## Data governance

Real company data should be stored outside public GitHub. API keys and credentials should be managed through environment variables or a secure secret store.

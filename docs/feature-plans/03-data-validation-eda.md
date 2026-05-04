# Feature 03: Data Validation and EDA

## Goal

Validate the normalized event dataset and decide whether it can support the MVP liquidation label.

## Scope

Included:

- Dataset validation.
- Basic EDA report.
- Class balance analysis.
- Missing-value analysis.

Not included:

- Feature engineering.
- Model training.
- Dashboard.

## Files

Create or update:

```text
src/defi_risk_advisor/data/validate_events.py
notebooks/01-eda.ipynb
reports/eda-summary.md
tests/test-data-validation.py
```

## EDA Questions

Answer these:

```text
How many rows?
How many wallets?
How many protocols?
How many chains?
How many events by type?
How many liquidation events?
How many wallets have liquidation?
What is the timestamp range?
Which fields are missing?
Which assets dominate?
Is class imbalance severe?
```

## Implementation Steps

1. Load `data/interim/normalized-events.csv`.
2. Validate required fields.
3. Count total rows and unique wallets.
4. Count event types.
5. Count liquidation rows.
6. Count wallets with liquidation.
7. Check missing values by column.
8. Check duplicate tx hash plus event fields.
9. Check timestamp min and max.
10. Write `reports/eda-summary.md`.

## Report Template

Use this structure:

```text
# EDA Summary
## Dataset Source
## Row Counts
## Wallet Counts
## Event Type Distribution
## Liquidation Label Feasibility
## Missing Data
## Known Limitations
## Decision
## Unresolved Questions
```

## Review Checklist

- EDA is generated from real normalized data.
- Label feasibility is explicit.
- Class imbalance is not hidden.
- Dataset source is cited.
- No model quality claims appear here.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-data-validation.py
```

Optional EDA command after implemented:

```bash
uv run python -m defi_risk_advisor.data.validate_events data/interim/normalized-events.csv
```

## Done Criteria

- `reports/eda-summary.md` explains whether MVP training can proceed.
- Data problems are documented before feature engineering.

## Unresolved Questions

1. What minimum liquidation count is acceptable for MVP?
2. Should wallets with only deposits and no borrows stay in training data?
3. Should protocol and chain be included in first EDA even if only Aave/Ethereum is present?

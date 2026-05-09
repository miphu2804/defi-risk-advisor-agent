# Feature 03: Data Validation and EDA

## Status: DONE (raw-data EDA completed, normalized-event EDA deferred)

## Goal

Validate the dataset and decide whether it can support the MVP liquidation label.

## What Was Done

EDA was performed directly on raw Aave V3 parquet data (`notebooks/eda.ipynb`) rather than on normalized events, since Features 01-02 haven't been implemented yet. This gave early insight into the dataset.

## Key EDA Findings (from raw data)

| Question | Answer |
|---|---|
| How many rows? | 379,784 |
| How many wallets? | 41,844 unique `From` addresses |
| How many protocols? | 1 (Aave V3 only) |
| How many chains? | 1 (Ethereum mainnet) |
| Event type distribution | `borrow`: 127,498 — `supply`: 111,341 — `withdraw`: 65,099 — `repay`: 53,025 — `flashLoanSimple`: 14,249 — `setUserEMode`: 5,208 — `setUserUseReserveAsCollateral`: 2,626 — `repayWithATokens`: 1,544 — `deposit`: 561 — others: 156 |
| Liquidation events | **21 rows** (`liquidationCall`) |
| Wallets with liquidation | TBD (need to check unique `From` for liquidation rows) |
| Timestamp range | 2023-01-27 to 2024-11-29 (~22 months) |
| Missing values | None (all 20 columns have 0 nulls) |
| Duplicate rows | None |
| Failed transactions | 3,699 (`isError=1`, 0.97%) |
| Columns | 20 after dropping duplicate `timeStamp` |

### Critical Finding: Extreme Class Imbalance

Only **21 out of 379,784 rows** are `liquidationCall` events (~0.006%). This means:
- `hasLiquidation` binary label will be extremely imbalanced.
- At most ~21 wallets have ever been liquidated (likely fewer if some wallets were liquidated multiple times).
- For the MVP `hasLiquidation` label to be meaningful, we need enough positive class wallets.
- **Alternative**: Consider using a richer dataset with more liquidation events, or broadening the label definition.

### Raw Dataset Issues Identified

1. **Amounts not directly available** — `InputData` contains ABI-encoded parameters. Asset and amount extraction requires decoding.
2. **No USD values** — Price oracle integration needed for USD-denominated features.
3. **Single protocol/chain** — Dataset is Aave V3 Ethereum only; multi-protocol features won't vary.
4. **No health factor / LTV data** — These are available on-chain but not in this Kaggle export.
5. **`To` address is constant** — All txs target the same Aave V3 pool proxy.

## Scope

Included:

- Dataset validation.
- Basic EDA report (from notebook).
- Class balance analysis.
- Missing-value analysis.
- Liquidation feasibility assessment.

Not included:

- Feature engineering.
- Model training.
- Dashboard.

## Files

Actual:
```text
notebooks/eda.ipynb                         # EDA on raw parquet data
data/raw/Ethereum_V3_Transactions.parquet   # input data
reports/eda-summary.md                      # formal EDA summary and decision artifact
```

Still to create:
```text
test/test_data_validation.py                # data validation tests
```

## Remaining Work

1. Determine exact number of unique borrower wallets liquidated by decoding `InputData` instead of relying on `From`.
2. Decide: is 21 liquidation events enough? Options:
   - Proceed with extreme class imbalance (use PR-AUC, not accuracy).
   - Add data from other chains (Polygon, Arbitrum) via Kaggle dataset.
   - Source additional liquidation data from Dune/Flipside.
3. Re-run EDA on normalized events once Feature 01-02 are done.

## Report Template

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

- [x] EDA findings documented in `reports/eda-summary.md`.
- [x] Liquidation class size is explicitly stated.
- [x] Class imbalance is not hidden.
- [x] Dataset source is cited.
- [x] Decision on MVP feasibility is explicit.

## Verification

```bash
uv run pytest test/test_data_validation.py
```

## Done Criteria

- `reports/eda-summary.md` explains whether MVP training can proceed.
- Decision documented: proceed with 21 liquidation events, or source more data.

## Unresolved Questions

1. ~~What minimum liquidation count is acceptable for MVP?~~ 21 is very low — needs decision.
2. Should a dataset with more liquidation events be sourced before proceeding?
3. Should wallets with only deposits and no borrows stay in training data?
4. Should the Kaggle dataset's Polygon/Arbitrum chains be included to increase liquidation count?

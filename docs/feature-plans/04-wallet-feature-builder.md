# Feature 04: Wallet Feature Builder

## Goal

Convert normalized lending events into one wallet-level feature row per wallet.

## Scope

Included:

- Aggregation features.
- Ratio features.
- Time features.
- Label creation.
- Feature export.
- Tests for edge cases.

Not included:

- Model training.
- SHAP explanations.
- API endpoints.

## Files

Create or update:

```text
src/defi_risk_advisor/features/feature_schema.py
src/defi_risk_advisor/features/wallet_feature_builder.py
tests/test-wallet-feature-builder.py
data/processed/wallet-features.csv
```

## Feature Groups

Counts:

```text
depositCount
withdrawCount
borrowCount
repayCount
liquidationCount
uniqueAssetCount
uniqueProtocolCount
uniqueChainCount
activeDayCount
```

Amounts:

```text
totalDepositAmountUsd
totalWithdrawAmountUsd
totalBorrowAmountUsd
totalRepayAmountUsd
avgBorrowAmountUsd
maxBorrowAmountUsd
```

Ratios:

```text
repayToBorrowCountRatio
repayToBorrowAmountRatio
borrowToDepositAmountRatio
withdrawToDepositAmountRatio
liquidationToBorrowRatio
```

Labels:

```text
hasLiquidation
```

## Implementation Steps

1. Load normalized events.
2. Group by `walletAddress`.
3. Build count features.
4. Build amount features.
5. Build ratio features with `safeDivide`.
6. Build activity duration features.
7. Build diversity features for protocol, chain, and asset counts.
8. Create `hasLiquidation`.
9. Remove `inf`, `-inf`, and invalid nulls.
10. Save `data/processed/wallet-features.csv`.

## Edge Cases

Test:

- Wallet with zero borrow events.
- Wallet with borrow but no repay.
- Wallet with liquidation.
- Wallet with missing optional `amountUsd`.
- Empty dataset.
- Multi-protocol wallet.

## Review Checklist

- One row equals one wallet.
- Label is excluded from model feature columns.
- Safe division handles zero denominator.
- Feature names are stable and documented.
- No future-window leakage exists for MVP label.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-wallet-feature-builder.py
```

Optional command after implemented:

```bash
uv run python -m defi_risk_advisor.features.wallet_feature_builder --input data/interim/normalized-events.csv --output data/processed/wallet-features.csv
```

## Done Criteria

- Wallet features can be regenerated from normalized events by command.
- Output has no invalid infinite values.

## Unresolved Questions

1. Should first model use USD-only features or fallback token amount features?
2. Should inactive deposit-only wallets be filtered?
3. Should feature names use camelCase in CSV or snake_case for Python ergonomics?

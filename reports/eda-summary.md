# EDA Summary

## Dataset Source

- Source file: `data/raw/Ethereum_V3_Transactions.parquet`
- Scope: Aave V3 transactions on Ethereum mainnet
- Analysis artifact: `notebooks/eda.ipynb`

## Row Counts

- Total rows: `379,784`
- Total columns after dropping duplicate `timeStamp`: `20`
- Duplicate rows: `0`
- Missing values: `0` across all columns

## Wallet Counts

- Unique `From` addresses: `41,844`
- Unique `To` addresses: `1`

Interpretation:

- The dataset spans many sender wallets.
- All transactions route to a single destination contract address, so `To` is not behaviorally informative for broad destination analysis.

## Time Coverage

- Earliest timestamp: `2023-01-27 08:24:47`
- Latest timestamp: `2024-11-29 16:01:59`
- Coverage: `672` days

## Event Type Distribution

- `borrow(...)`: `127,498`
- `supply(...)`: `96,025`
- `withdraw(...)`: `65,099`
- `repay(...)`: `47,580`
- `supplyWithPermit(...)`: `15,316`
- `flashLoanSimple(...)`: `14,249`
- `setUserEMode(...)`: `5,208`
- `repayWithPermit(...)`: `3,901`
- `setUserUseReserveAsCollateral(...)`: `2,626`
- `repayWithATokens(...)`: `1,544`
- `deposit(...)`: `561`
- `mintToTreasury(...)`: `78`
- `flashLoan(...)`: `51`
- `liquidationCall(...)`: `21`
- Empty `FunctionName`: `18`
- Remaining technical/admin calls: `7`

Interpretation:

- Core lending actions dominate the dataset: borrow, supply, withdraw, and repay.
- Liquidation events exist but are extremely rare.
- A small number of rows have empty or technical function signatures and should not drive modeling decisions.

## Liquidation Label Feasibility

- Liquidation transaction rows: `21`
- Liquidation share of total rows: `0.0055%`
- Unique `From` addresses among liquidation rows: `3`

Important caveat:

- `Liquidation rows` count liquidation transactions, not confirmed unique borrower wallets liquidated.
- The true liquidated borrower is likely encoded inside `InputData` and requires ABI decoding.

Assessment:

- A liquidation-based MVP label is severely class-imbalanced in the raw dataset.
- Using transaction rows directly for a liquidation target is not robust.
- Even at wallet level, the positive class is likely too small for a stable MVP without either richer data or broader label design.

## Failed Transactions

- `isError = 1` rows: `3,699`
- Failed transaction share: `0.974%`

Interpretation:

- Failed transactions are present but rare.
- `isError` is useful as a validation signal, but it is not a substitute for liquidation labeling.

## Distribution Findings

- `GasPrice` and `GasUsed` are strongly right-skewed on the raw scale.
- `log1p` views make their central distributions much easier to inspect.
- `GasUsed` remains more heterogeneous than `GasPrice` after transformation, which suggests different transaction complexity across function types.
- `Value` is concentrated near zero and is less informative on a raw histogram alone.

## Known Limitations

- Amounts and semantic borrower fields are not directly decoded from `InputData`.
- USD-denominated values are not available in the raw export.
- Dataset covers only one protocol and one chain.
- Health factor and LTV are not present in this raw Kaggle export.
- `To` is constant, so routing diversity is not represented.
- Empty `FunctionName` rows (`18`) indicate a small parsing or data-quality edge case.

## Decision

- Proceed with the dataset for early exploratory validation and pipeline development.
- Do not treat this raw dataset as sufficient evidence that an MVP liquidation model is viable without augmentation.
- Before model training, either:
  - source additional liquidation-rich data, or
  - redesign the target label to be less sparse than raw liquidation events.

## Unresolved Questions

1. Should liquidation labels be derived only after ABI decoding identifies the true borrower address?
2. Should additional chains or external datasets be added before MVP model training?
3. Should the target be broadened beyond liquidation events to reduce class sparsity?

# Feature 02: Aave Adapter

## Status: NOT STARTED (dataset validated, adapter not implemented)

## Goal

Implement Aave as the first protocol adapter while keeping all Aave-specific logic outside the core risk engine.

## Context

The dataset and download infrastructure already exist:
- **Source**: Kaggle `abcd334/aave-transactions-across-different-blockchains`
- **File**: `Ethereum_V3_Transactions.parquet` (379,784 rows, 21 columns)
- **Chain**: Ethereum mainnet, Aave V3 pool
- **Date range**: 2023-01-27 to 2024-11-29
- **Downloader**: `src/downloader/kaggle.py` (KaggleDownloader class)
- **CLI script**: `scripts/download_dataset.py`
- **Config**: `DATASET_NAME` and `DATASET_FILE` in `.env` via `app_config.py`
- **Raw data**: `data/raw/Ethereum_V3_Transactions.parquet`
- **EDA report**: `reports/eda-summary.md`

Key challenge: the raw dataset does not have explicit asset/amount columns. These are encoded in `InputData` (calldata hex) and need ABI decoding. For MVP, event type mapping + wallet activity counts may suffice without decoded amounts.

## Scope

Included:

- Aave raw data loader (parquet, using existing downloader).
- FunctionName → normalized event type mapping.
- Wallet/timestamp/txHash normalization.
- Normalized event output.
- Adapter tests with sample rows.
- Dataset notes.

Not included:

- ABI decoding of InputData (deferred to follow-up).
- Live blockchain indexing.
- Multi-protocol joins.
- ML training.

## Files

Create or update:

```text
src/adapters/base_adapter.py
src/adapters/aave_adapter.py
src/data/load_events.py
test/test_aave_adapter.py
reports/dataset-notes.md
data/interim/                    # normalized event output
```

Current state:

```text
src/adapters/                    # does not exist yet
src/data/load_events.py          # does not exist yet
test/test_aave_adapter.py        # does not exist yet
reports/dataset-notes.md         # does not exist yet
data/interim/                    # does not exist yet
```

Already exist (no change needed):
```text
src/downloader/kaggle.py         # KaggleDownloader
scripts/download_dataset.py      # CLI download script
src/app_config.py                # DATASET_NAME, DATASET_FILE config
data/raw/Ethereum_V3_Transactions.parquet
```

## Adapter Contract

Adapter public API:

```text
load_raw(source) -> raw records
normalize(raw records) -> normalized lending events
validate(normalized events) -> valid events or errors
```

Aave V3 FunctionName mapping (from actual dataset):

```text
supply / supplyWithPermit / depositETH          → deposit
withdraw                                         → withdraw
borrow                                           → borrow
repay / repayWithPermit / repayWithATokens       → repay
liquidationCall                                  → liquidation
setUserUseReserveAsCollateral                    → collateral_enabled / collateral_disabled
flashLoanSimple / flashLoan                      → transfer
setUserEMode / mintToTreasury / others           → unknown
```

## Raw Dataset Fields

| Column | Used for |
|---|---|
| TxHash | eventId / txHash |
| Timestamp | timestamp |
| From | walletAddress |
| FunctionName | rawEventType → eventType mapping |
| BlockNumber | blockNumber |
| isError | filter out failed txs (3,699 rows / 0.97%) |

Fields NOT directly available (in InputData):
- assetSymbol, assetAddress
- amount, amountUsd
- collateralAssetSymbol, collateralAmount
- debtAssetSymbol, debtAmount

## Implementation Steps

1. Load existing `data/raw/Ethereum_V3_Transactions.parquet` with pandas.
2. Filter `isError == 0` (remove failed transactions).
3. Create `BaseProtocolAdapter` interface.
4. Implement `AaveAdapter`:
   - Map `FunctionName` → normalized `eventType`.
   - Map `From` → lowercase `walletAddress`.
   - Map `TxHash` → `txHash`.
   - Map `Timestamp` → `timestamp`.
   - Set `chain = "ethereum"`, `protocol = "aave_v3"`.
   - Set `amount = None` (not extractable without ABI decoding).
5. Preserve `rawEventType` (original FunctionName) and `source`.
6. Export normalized events to `data/interim/normalized-events.parquet`.
7. Add tests with a tiny inline fixture (5-10 sample rows).
8. Write `reports/dataset-notes.md` documenting source, limitations, and known issues.

## Data Quality Checks

Check:

- Missing wallet address (`From` is null).
- Missing timestamp.
- Unknown FunctionName → map to `unknown`.
- Failed txs (`isError == 1`) → filter out.
- Duplicate TxHash rows.
- Liquidation count (expected: only 21 `liquidationCall` rows).
- `To` address concentration (expected: 1 unique destination address in raw dataset).
- Empty `FunctionName` rows (expected: 18).

## Review Checklist

- Aave logic is only in adapter files.
- Normalized output matches Feature 01 schema.
- Missing required fields fail clearly.
- Dataset limitations are documented.
- Tests use small fixtures, not large raw files.

## Verification

```bash
uv run python -m compileall src test
uv run pytest test/test_aave_adapter.py
```

Optional script command after implemented:

```bash
uv run python -m src.data.load_events --protocol aave --input data/raw/Ethereum_V3_Transactions.parquet --output data/interim/normalized-events.parquet
```

## Done Criteria

- Aave raw records transform into normalized lending events.
- Downstream EDA can read one normalized events file.

## Unresolved Questions

1. ~~Which Aave data source should be first?~~ → Kaggle `abcd334/aave-transactions-across-different-blockchains`, Ethereum V3.
2. ~~Which chain should first adapter target?~~ → Ethereum mainnet.
3. Should we ABI-decode InputData for amounts, or proceed with count-only features for MVP? → Count-only for MVP.
4. FlashLoan events: map to `transfer` or keep as separate event type? → Map to `transfer` for now.
5. Should liquidation sender addresses be preserved separately from future decoded borrower addresses? → Likely yes.

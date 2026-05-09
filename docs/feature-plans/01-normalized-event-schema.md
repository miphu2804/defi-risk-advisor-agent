# Feature 01: Normalized Event Schema

## Status: NOT STARTED (raw-data EDA completed first)

## Goal

Define one protocol-agnostic lending event contract. Every protocol adapter must output this contract.

## Context

The project currently has:
- Raw Aave V3 Ethereum dataset in `data/raw/Ethereum_V3_Transactions.parquet` (379,784 rows, 20 effective columns after dropping duplicate `timeStamp`).
- Source: Kaggle `abcd334/aave-transactions-across-different-blockchains`.
- EDA notebook (`notebooks/eda.ipynb`) that works directly on raw parquet data.
- EDA summary report (`reports/eda-summary.md`) with class-imbalance findings.

The normalized schema step was deferred. EDA was done on raw data to understand the dataset first. This is a pragmatic choice — the schema should now be designed with the actual Aave V3 field structure in mind.

## Actual Raw Dataset Fields

The raw Aave V3 dataset columns:

| Column | Type | Description |
|---|---|---|
| BlockNumber | str | Block number |
| BlockHash | str | Block hash |
| timeStamp | int64 | Unix timestamp (seconds) |
| TxHash | str | Transaction hash (unique, 379,784 values) |
| Nonce | str | Transaction nonce |
| TransactionIndex | str | Index within block |
| From | str | Sender wallet address (41,844 unique) |
| To | str | Contract address (1 unique — Aave V3 pool) |
| Value | float64 | ETH value (mostly 0) |
| gas | str | Gas limit |
| GasPrice | int64 | Gas price in wei |
| InputData | str | Raw calldata |
| MethodID | str | Function selector (23 unique) |
| FunctionName | str | Human-readable function signature (20 unique) |
| ContractAddress | str | Contract address (1 unique) |
| CumulativeGasUsed | str | Cumulative gas used |
| TxReceiptStatus | str | Transaction status |
| GasUsed | int64 | Gas used |
| Confirmations | str | Block confirmations |
| isError | int64 | Error flag (3,699 errors / 0.97%) |
| Timestamp | datetime64 | Parsed datetime (2023-01-27 to 2024-11-29) |

Key observations for schema design:
- **No asset/amount fields directly** — `InputData` contains encoded parameters that need ABI decoding to extract asset, amount, etc.
- **`FunctionName`** maps to event types: `supply`, `borrow`, `withdraw`, `repay`, `liquidationCall`, `setUserUseReserveAsCollateral`, `flashLoanSimple`, etc.
- **21 liquidation transactions** total (`liquidationCall`) — very rare class.
- **No USD amounts** — amounts are encoded in `InputData`.
- **Only 1 `To` address** — all transactions target the same Aave V3 pool proxy.
- **Chain is always Ethereum mainnet** for this dataset.

## Scope

Included:

- Event type enum (mapped from Aave `FunctionName` values).
- Event schema (adapted to actual available fields).
- Validation helpers.
- Wallet normalization.
- Timestamp normalization.
- Small tests.

Not included:

- ABI decoding of `InputData` (may be needed for amount extraction).
- Aave adapter (Feature 02).
- Feature aggregation.

## Files

Create or update:

```text
src/data/event_schema.py
src/data/validate_events.py
test/test_event_schema.py
```

Current state:

```text
src/data/                     # does not exist yet
test/test_event_schema.py     # does not exist yet
```

## Data Contract (revised for actual dataset)

Required MVP fields (matching available data):

```text
txHash          → from TxHash
timestamp       → from Timestamp
chain           → hardcoded "ethereum" for this dataset
protocol        → hardcoded "aave_v3"
walletAddress   → from From
eventType       → mapped from FunctionName
assetSymbol     → needs ABI decoding from InputData (TBD)
amount          → needs ABI decoding from InputData (TBD)
```

Optional fields (when extractable):

```text
blockNumber     → from BlockNumber
rawEventType    → original FunctionName
source          → "kaggle:abcd334/aave-transactions-across-different-blockchains"
amountUsd       → not available in raw data (needs price oracle)
healthFactor    → not available (needs ABI decoding or separate data source)
```

## Event Type Mapping (for Aave V3)

Based on actual `FunctionName` values in the dataset:

```text
supply / supplyWithPermit              → deposit
withdraw                               → withdraw
borrow                                 → borrow
repay / repayWithPermit / repayWithATokens → repay
liquidationCall                        → liquidation
setUserUseReserveAsCollateral          → collateral_enabled / collateral_disabled
flashLoanSimple / flashLoan            → transfer (or keep as separate type)
setUserEMode                           → unknown (protocol config)
depositETH                             → deposit
mintToTreasury                         → unknown (protocol internal)
```

## Implementation Steps

1. Add `pydantic` if direct model usage beyond `pydantic-settings` is needed.
2. Define `LendingEventType` enum (map FunctionName values to normalized types).
3. Define `LendingEvent` model with required + optional fields.
4. Normalize wallet addresses to lowercase.
5. Parse timestamps into timezone-aware datetime values.
6. Validate `amount >= 0` once amounts become extractable.
7. Preserve `rawEventType` (original FunctionName) for debugging.
8. Write tests for valid event, invalid event type, invalid wallet, and timestamp parse.
9. Document schema assumptions and explicit nullability for undecoded fields.

## Design Rules

- Schema must not mention only Aave.
- Use camelCase field names in external JSON contracts.
- Unknown raw protocol events should map to `unknown`, not crash.
- Amount extraction from `InputData` is a separate concern — schema should accept `None` for amount initially.

## Open Design Decision: InputData Decoding

The raw dataset does not have explicit asset/amount columns. Options:

1. **ABI-decode `InputData`** using contract ABIs to extract `(asset, amount, ...)` from calldata.
2. **Skip amount for MVP** — use event counts and wallet activity patterns only.
3. **Find an enriched dataset** that already includes decoded parameters.

Decision: **Option 2 for MVP** (event counts + activity patterns), then Option 1 as follow-up.

## Review Checklist

- Required fields are enforced.
- Optional fields do not break minimal datasets.
- Validation errors are clear.
- Tests cover bad input.
- No protocol-specific logic leaks into core schema.

## Verification

```bash
uv run python -m compileall src test
uv run pytest test/test_event_schema.py
```

## Done Criteria

- Raw Aave V3 rows can be mapped to normalized lending events (even with null amounts).
- Downstream feature builder can depend on this stable contract.

## Unresolved Questions

1. Should flash-loan activity remain a separate normalized event type instead of mapping to `transfer`?
2. Should collateral toggles be modeled as one event type plus a boolean flag rather than two normalized labels?
3. Should `assetSymbol` and `amount` stay nullable for MVP, or should ABI decoding become part of Feature 02?

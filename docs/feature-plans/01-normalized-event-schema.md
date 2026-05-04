# Feature 01: Normalized Event Schema

## Goal

Define one protocol-agnostic lending event contract. Every protocol adapter must output this contract.

## Scope

Included:

- Event type enum.
- Event schema.
- Validation helpers.
- Wallet normalization.
- Timestamp normalization.
- Small tests.

Not included:

- Aave adapter.
- CSV ingestion.
- Feature aggregation.

## Files

Create or update:

```text
src/defi_risk_advisor/data/event_schema.py
src/defi_risk_advisor/data/validate_events.py
tests/test-event-schema.py
docs/feature-plans/01-normalized-event-schema.md
```

## Data Contract

Required MVP fields:

```text
txHash
timestamp
chain
protocol
walletAddress
eventType
assetSymbol
amount
```

Optional fields:

```text
eventId
blockNumber
market
assetAddress
amountUsd
collateralAssetSymbol
collateralAmount
debtAssetSymbol
debtAmount
healthFactor
ltv
liquidationThreshold
rawEventType
source
```

Event types:

```text
deposit
withdraw
borrow
repay
liquidation
collateral_enabled
collateral_disabled
transfer
unknown
```

## Implementation Steps

1. Add Pydantic dependency when this feature starts:

   ```bash
   uv add pydantic
   ```

2. Define `LendingEventType` enum.
3. Define `LendingEvent` model.
4. Normalize wallet addresses to lowercase.
5. Parse timestamps into timezone-aware datetime values.
6. Validate `amount >= 0`.
7. Allow optional `amountUsd`, but validate it if present.
8. Preserve `rawEventType` for debugging.
9. Write tests for valid event, invalid event type, invalid wallet, invalid amount, and timestamp parse.
10. Document schema assumptions in `docs/overview.md` only if contract changes.

## Design Rules

- Schema must not mention only Aave.
- Use camelCase field names in external JSON contracts.
- Keep Python internals simple; aliases can map Python snake_case to API camelCase later if needed.
- Unknown raw protocol events should map to `unknown`, not crash the whole import.

## Review Checklist

- Required fields are enforced.
- Optional fields do not break minimal datasets.
- Validation errors are clear.
- Tests cover bad input.
- No protocol-specific logic leaks into core schema.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-event-schema.py
```

## Done Criteria

- Any protocol adapter can create validated normalized lending events.
- Downstream feature builder can depend on this stable contract.

## Unresolved Questions

1. Should wallet validation enforce EVM addresses only for MVP?
2. Should non-EVM protocols be explicitly out of scope until later?
3. Should decimal precision use `Decimal` immediately, or float for MVP CSV processing?

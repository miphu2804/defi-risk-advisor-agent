# Feature 02: Aave Adapter

## Goal

Implement Aave as the first protocol adapter while keeping all Aave-specific logic outside the core risk engine.

## Scope

Included:

- Aave raw data loader.
- Event name mapping.
- Normalized event output.
- Adapter tests with sample rows.
- Dataset notes.

Not included:

- Live blockchain indexing.
- Multi-protocol joins.
- ML training.

## Files

Create or update:

```text
src/defi_risk_advisor/adapters/base_adapter.py
src/defi_risk_advisor/adapters/aave_adapter.py
src/defi_risk_advisor/data/load_events.py
tests/test-aave-adapter.py
reports/dataset-notes.md
data/raw/
data/interim/
```

## Adapter Contract

Adapter public API:

```text
load_raw(source) -> raw records
normalize(raw records) -> normalized lending events
validate(normalized events) -> valid events or errors
```

Aave mapping:

```text
Supply or Deposit -> deposit
Withdraw -> withdraw
Borrow -> borrow
Repay -> repay
LiquidationCall -> liquidation
```

## Implementation Steps

1. Pick first Aave dataset source.
2. Document source, chain, date range, and columns in `reports/dataset-notes.md`.
3. Add pandas dependency when CSV loading starts:

   ```bash
   uv add pandas
   ```

4. Create `BaseProtocolAdapter` interface.
5. Implement `AaveAdapter`.
6. Normalize event type names.
7. Normalize wallet, asset, amount, timestamp, tx hash.
8. Preserve `rawEventType` and `source`.
9. Export normalized CSV to `data/interim/normalized-events.csv`.
10. Add tests with a tiny inline fixture, not full data.

## Data Quality Checks

Check:

- Missing wallet address.
- Missing timestamp.
- Unknown event type.
- Negative amount.
- Duplicate tx/event rows.
- Empty liquidation class.

## Review Checklist

- Aave logic is only in adapter files.
- Normalized output matches Feature 01 schema.
- Missing required fields fail clearly.
- Dataset limitations are documented.
- Tests use small fixtures, not large raw files.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-aave-adapter.py
```

Optional script command after implemented:

```bash
uv run python -m defi_risk_advisor.data.load_events --protocol aave --input data/raw/aave.csv --output data/interim/normalized-events.csv
```

## Done Criteria

- Aave raw records can be transformed into normalized lending events.
- Downstream EDA can read one normalized events file.

## Unresolved Questions

1. Which Aave data source should be first?
2. Which chain should first adapter target?
3. Do we need USD amounts in MVP, or can token amounts be enough for first baseline?

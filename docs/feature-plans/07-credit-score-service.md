# Feature 07: Credit Score Service

## Goal

Convert model liquidation probability into a deterministic DeFi credit score and risk level.

## Scope

Included:

- Probability validation.
- Score mapping.
- Risk-level mapping.
- Boundary tests.

Not included:

- Model training.
- Feature explanation.
- Recommendation logic.

## Files

Create or update:

```text
src/defi_risk_advisor/scoring/credit_score.py
src/defi_risk_advisor/scoring/risk_level.py
tests/test-credit-score.py
```

## Score Formula

```python
score = int(850 - p_liquidation * 550)
score = max(300, min(850, score))
```

Bands:

```text
750-850 = Excellent
650-749 = Good
550-649 = Medium
450-549 = Risky
300-449 = Very Risky
```

## Implementation Steps

1. Implement probability validation.
2. Reject probability below `0` or above `1`.
3. Implement score calculation.
4. Clamp score to 300-850.
5. Implement score band function.
6. Add tests for `0`, `1`, and midpoints.
7. Add tests for invalid probabilities.
8. Keep functions pure and dependency-free.

## Review Checklist

- Mapping is deterministic.
- Function names are clear.
- Invalid model output fails instead of silently creating bad score.
- Score band labels match API docs.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-credit-score.py
```

## Done Criteria

- Any valid model probability returns score and risk level.
- Boundary tests pass.

## Unresolved Questions

1. Should score formula be configurable later?
2. Should band names be user-facing or API-only constants?
3. Should score mapping use calibrated probability only?

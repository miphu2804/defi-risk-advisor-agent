# Feature 09: Recommendation Engine

## Goal

Recommend safer borrowing behavior based on score, risk level, and wallet features.

## Scope

Included:

- LTV band rules.
- Collateral guidance.
- Avoid-asset guidance.
- Risk-reducing actions.
- Deterministic tests.

Not included:

- Portfolio optimization.
- Transaction execution.
- Live protocol APY ranking.

## Files

Create or update:

```text
src/defi_risk_advisor/recommender/ltv_rules.py
src/defi_risk_advisor/recommender/recommendation_service.py
tests/test-recommendation-engine.py
reports/sample-recommendations.md
```

## Recommendation Inputs

```text
creditScore
riskLevel
walletFeatures
protocols
optional market metadata
```

## Recommendation Outputs

```text
recommendedLtvRange
recommendedCollateralTypes
avoidAssets
actions
explanation
disclaimer
```

## LTV Bands

```text
Score >= 750 -> 65-70%
Score >= 650 -> 50-60%
Score >= 550 -> 35-45%
Score >= 450 -> 25-35%
Score < 450  -> 15-25%
```

## Implementation Steps

1. Implement pure `recommendLtv(score)`.
2. Implement collateral guidance by risk level.
3. Implement avoid-asset guidance.
4. Implement action list generator.
5. Add extra warning for previous liquidation.
6. Add extra warning for low repay ratio.
7. Return deterministic response object.
8. Add tests for each score band.
9. Add tests for high-risk feature overrides.
10. Save sample recommendations.

## Review Checklist

- Output is not financial advice.
- Rules are not Aave-only.
- No transaction execution language.
- Each score band has tests.
- High-risk flags affect action text.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-recommendation-engine.py
```

## Done Criteria

- Given score, risk level, and features, service returns a complete recommendation.
- Recommendation output is stable enough for API and agent use.

## Unresolved Questions

1. Should protocol-specific LTV thresholds be added before dashboard?
2. Should collateral guidance use token symbols or categories first?
3. Should recommendations include confidence level?

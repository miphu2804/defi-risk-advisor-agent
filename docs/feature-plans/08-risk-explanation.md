# Feature 08: Risk Explanation

## Goal

Explain wallet risk output in clear user-facing language without overstating model certainty.

## Scope

Included:

- Rule-based explanation fallback.
- Feature display names.
- Top risk factor selection.
- Optional model feature importance.

Not included:

- SHAP as a hard MVP dependency.
- LLM-written explanations.
- Dashboard visualizations.

## Files

Create or update:

```text
src/defi_risk_advisor/explainability/risk_explainer.py
reports/sample-explanations.md
tests/test-risk-explainer.py
```

## Explanation Strategy

Start with rules:

```text
low repay ratio -> Low repayment relative to borrowing
previous liquidation -> Wallet has historical liquidation
high borrow count -> Frequent borrowing behavior
short wallet age -> Limited lending history
volatile exposure -> Higher volatility collateral or debt exposure
```

Add model importances only after model artifact exists.

## Implementation Steps

1. Define feature-to-message mapping.
2. Define risk thresholds for important features.
3. Implement rule-based `explainRiskFactors(features)`.
4. Return top 3 to 5 reasons.
5. Add fallback message when no strong factor exists.
6. Add optional model importance support.
7. Save sample explanations.
8. Add tests for known feature patterns.

## Writing Rules

- Use "associated with risk", not "caused risk".
- Do not claim future liquidation certainty.
- Keep explanations short.
- Include disclaimer in API or agent response, not every low-level function.

## Review Checklist

- Technical feature names are translated.
- Explanation works without SHAP.
- No causality overclaim.
- Tests cover high-risk and low-risk examples.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-risk-explainer.py
```

## Done Criteria

- `/analyze-wallet` can include top risk factors.
- Explanations are deterministic without LLM dependency.

## Unresolved Questions

1. Should SHAP be added in MVP or after API demo?
2. Should explanations be generated from model importance or rules first?
3. Should low-risk wallets show positive factors too?

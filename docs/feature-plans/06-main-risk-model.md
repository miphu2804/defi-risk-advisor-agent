# Feature 06: Main Risk Model

## Goal

Upgrade from baseline to one stronger tabular model after the end-to-end product works.

## Scope

Included:

- One stronger model.
- Small hyperparameter search.
- Baseline comparison.
- Updated model artifact.

Not included:

- Multiple advanced models at once.
- Deep learning.
- Graph neural networks.
- Production model registry.

## Files

Create or update:

```text
src/defi_risk_advisor/models/train_model.py
src/defi_risk_advisor/models/evaluate_model.py
models/main-risk-model.joblib
reports/model-comparison.md
reports/metrics.json
tests/test-predict-risk.py
```

## Model Choice

Choose one:

```text
XGBoost
LightGBM
```

Default recommendation:

```text
Use XGBoost if install is smooth. Use LightGBM only if XGBoost creates environment issues.
```

## Implementation Steps

1. Confirm baseline metrics exist.
2. Add one model dependency:

   ```bash
   uv add xgboost
   ```

3. Reuse the same feature columns.
4. Train main model.
5. Tune small set of hyperparameters only.
6. Evaluate with same metric function as baseline.
7. Compare against baseline in `reports/model-comparison.md`.
8. Save `models/main-risk-model.joblib`.
9. Ensure prediction utility can load selected model.
10. Add model load and feature-order tests.

## Review Checklist

- Main model uses same train/test policy as baseline.
- Metrics are comparable.
- Upgrade is justified by metric or explainability improvement.
- Feature mismatch fails clearly.
- No overcomplicated registry is added.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-predict-risk.py
```

Optional command after implemented:

```bash
uv run python -m defi_risk_advisor.models.train_model --model xgboost --input data/processed/wallet-features.csv
```

## Done Criteria

- Main model predicts liquidation probability.
- Comparison report explains whether it replaces baseline.

## Unresolved Questions

1. Should this feature run before or after API if baseline quality is weak?
2. Should calibration be required before credit score mapping?
3. Should model selection optimize PR-AUC or recall at fixed precision?

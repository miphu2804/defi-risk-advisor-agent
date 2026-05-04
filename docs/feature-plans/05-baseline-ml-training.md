# Feature 05: Baseline ML Training

## Goal

Train simple baseline models to validate feature usefulness and data quality before adding stronger models.

## Scope

Included:

- Train/test split.
- Logistic Regression.
- Random Forest.
- Metrics report.
- Baseline artifact.

Not included:

- XGBoost or LightGBM.
- Hyperparameter tuning beyond minimal defaults.
- Agent or API integration.

## Files

Create or update:

```text
src/defi_risk_advisor/models/train_model.py
src/defi_risk_advisor/models/evaluate_model.py
src/defi_risk_advisor/models/predict_risk.py
models/baseline-model.joblib
models/feature-columns.json
reports/metrics.json
reports/model-baseline.md
tests/test-model-training.py
```

## Dependencies

Add when training starts:

```bash
uv add scikit-learn joblib
```

## Implementation Steps

1. Load `data/processed/wallet-features.csv`.
2. Separate label `hasLiquidation`.
3. Remove non-feature columns such as wallet address.
4. Save ordered feature columns.
5. Split train/test data.
6. Train Logistic Regression with class weighting if needed.
7. Train Random Forest.
8. Evaluate ROC-AUC, PR-AUC, precision, recall, F1, and confusion matrix.
9. Save metrics to `reports/metrics.json`.
10. Save best baseline to `models/baseline-model.joblib`.

## Evaluation Rules

- Accuracy alone is not acceptable.
- PR-AUC matters because liquidation is likely imbalanced.
- Recall matters because missing risky wallets is costly.
- Metrics must mention class distribution.

## Review Checklist

- Label is not in features.
- Wallet address is not in features.
- Feature order is saved.
- Model artifact can be loaded.
- Report states data limitations.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-model-training.py
```

Optional command after implemented:

```bash
uv run python -m defi_risk_advisor.models.train_model --input data/processed/wallet-features.csv
```

## Done Criteria

- At least one baseline model trains.
- Metrics and artifact are saved.
- Baseline limitations are documented.

## Unresolved Questions

1. What minimum PR-AUC is acceptable for portfolio MVP?
2. Should train/test split be random for MVP or time-based immediately?
3. Should baseline use class weights by default?

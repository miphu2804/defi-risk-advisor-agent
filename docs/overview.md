# DeFi Risk Advisor Agent Overview

## 1. Review Summary

The previous overview had a strong ML project shape, but it was too tightly coupled to Aave. Aave should be the first data adapter, not the product boundary. The updated plan makes the system protocol-agnostic by defining a normalized lending event schema and then adding protocol adapters such as Aave, Compound, and Morpho over time.

Main fixes:

- Replace "Aave-only MVP" with "general lending protocol core, Aave first adapter".
- Make UV by Astral the only Python dependency and runtime workflow.
- Remove `requirements.txt` as a default deliverable.
- Break large stages into smaller feature tickets with review gates.
- Keep the agent layer late in the roadmap so the ML scoring core exists before the LLM explains it.
- Add explicit safety, validation, testing, and documentation checks per feature.

External docs used:

- Astral UV project workflow: https://docs.astral.sh/uv/
- UV dependency management: https://docs.astral.sh/uv/concepts/projects/dependencies/
- UV locking and syncing: https://docs.astral.sh/uv/concepts/projects/sync/
- UV project layout and lockfile: https://docs.astral.sh/uv/concepts/projects/layout/

---

## 2. Project Definition

### 2.1 Project Name

**DeFi Risk Advisor Agent**

Full name:

**DeFi Risk Advisor Agent: Protocol-Agnostic Wallet Risk Scoring and Safer Borrowing Recommendations**

Alternative names:

- DeFi Lending Risk Advisor
- On-Chain Credit Risk Advisor
- DeFi Wallet Risk Scoring Agent
- Liquidation-Aware Wallet Credit Score

### 2.2 One-Line Pitch

An AI-powered DeFi risk system that normalizes lending protocol activity, predicts wallet liquidation risk, converts risk into an explainable credit score, and recommends safer borrowing behavior through an API and agent interface.

### 2.3 Core Principle

The system should not be hardcoded for one protocol.

Use this boundary:

```text
Protocol adapters handle protocol-specific data.
Core risk engine handles normalized wallet behavior.
```

Aave is the first supported protocol because it has rich lending and liquidation events, but the architecture must allow Compound, Morpho, Spark, Euler, and other lending protocols later.

---

## 3. Product Goal

Build a side project that proves end-to-end AI engineering skill:

1. Ingest DeFi lending events from one or more protocols.
2. Normalize events into a shared protocol-agnostic schema.
3. Build wallet-level behavioral features.
4. Train a machine learning model for liquidation risk.
5. Convert liquidation probability into a DeFi credit score.
6. Recommend safer borrowing actions.
7. Expose the system through FastAPI.
8. Add an LLM agent that calls tools and explains results.
9. Keep the project reproducible with UV, tests, and clear docs.

Short flow:

```text
Protocol events
  -> protocol adapter
  -> normalized lending events
  -> wallet features
  -> liquidation risk model
  -> DeFi credit score
  -> risk recommendation
  -> API and agent explanation
```

---

## 4. Problem Statement

Traditional credit scoring uses identity, income, repayment history, and credit records. DeFi users act through wallet addresses, so borrower risk must be inferred from on-chain behavior.

Main question:

```text
Based on a wallet's lending protocol behavior, how risky is this wallet as a borrower?
```

MVP target:

```text
Has this wallet ever been liquidated, or does it behave like wallets that were liquidated?
```

Advanced target:

```text
Will this wallet be liquidated in the next 7 or 30 days?
```

---

## 5. Scope

### 5.1 MVP Scope

MVP supports one real protocol adapter first, likely Aave, while keeping the core schema protocol-agnostic.

Included:

- UV-managed Python project.
- Normalized lending event schema.
- Aave adapter or imported Aave-compatible dataset.
- Wallet-level feature engineering.
- Binary liquidation risk model.
- Credit score mapping.
- Rule-based recommendation engine.
- FastAPI endpoints.
- Deterministic agent fallback if no LLM key is configured.
- Tests for core scoring and recommendation logic.

Not included in MVP:

- Smart contract deployment.
- Real-time blockchain indexing.
- Trade or transaction execution.
- Financial advice guarantees.
- Graph neural networks.
- Multi-wallet identity clustering.
- Fully automated data vendor integration.
- Full production monitoring.

### 5.2 Protocol Expansion Scope

After the first adapter works, add protocols by implementing the same adapter contract.

Candidate protocols:

- Aave
- Compound
- Morpho
- Spark
- Euler

Expansion rule:

```text
Do not change model or API contracts for every new protocol.
Map new protocol data into the normalized schema instead.
```

---

## 6. Technical Stack

### 6.1 Python Runtime and Package Management

Use **UV by Astral** for project management.

Rules:

- Use `pyproject.toml` as the dependency source of truth.
- Commit `uv.lock` when dependencies exist.
- Use `uv add` and `uv remove` for dependencies.
- Use `uv sync` to create and sync the environment.
- Use `uv run` for scripts, tests, API, and notebooks.
- Do not maintain `requirements.txt` unless a deployment target explicitly requires an exported file.
- Do not manually edit `uv.lock`.

Core commands:

```bash
uv python pin 3.11
uv sync
uv add pandas scikit-learn fastapi uvicorn pydantic pydantic-settings joblib
uv add --dev pytest pytest-cov ruff mypy httpx
uv run python main.py
uv run pytest
uv run ruff check .
```

Optional deployment export only if needed:

```bash
uv export --format requirements.txt -o requirements.txt
```

### 6.2 Backend

- Python 3.11+
- FastAPI
- Pydantic
- pydantic-settings for configuration
- pandas for tabular processing
- scikit-learn for baseline models
- XGBoost or LightGBM after baseline
- joblib for model artifacts

### 6.3 Agent

Start simple:

- Deterministic parser for wallet addresses.
- Tool wrappers around internal score, explain, and recommend services.
- Optional LLM provider later.

Agent guardrails:

- No transaction execution.
- No profit guarantee.
- No liquidation certainty claims.
- Always present model limitations.

### 6.4 Optional UI

Use Streamlit for the fastest portfolio demo. Consider Next.js only after the API and ML core are stable.

---

## 7. Architecture

```text
defi-risk-advisor-agent
├── protocol adapters
│   ├── aave adapter
│   ├── compound adapter
│   └── future adapters
│
├── normalized data layer
│   ├── lending events
│   ├── wallet snapshots
│   └── protocol metadata
│
├── feature engineering
│   ├── event counts
│   ├── amount aggregates
│   ├── repay and borrow ratios
│   ├── activity windows
│   └── liquidation labels
│
├── ML risk engine
│   ├── baseline model
│   ├── main model
│   ├── evaluation
│   └── model registry
│
├── scoring layer
│   ├── liquidation probability
│   ├── credit score
│   └── risk band
│
├── recommendation layer
│   ├── safe LTV rules
│   ├── collateral guidance
│   └── risk-reducing actions
│
├── explainability layer
│   ├── feature importance
│   ├── rule fallback
│   └── user-facing reasons
│
├── API layer
│   ├── score wallet
│   ├── recommend
│   ├── analyze wallet
│   └── agent chat
│
└── optional dashboard
    ├── wallet input
    ├── score display
    └── recommendation display
```

---

## 8. Normalized Data Contract

### 8.1 Lending Event Schema

Every protocol adapter should output this schema.

```text
eventId
txHash
blockNumber
timestamp
chain
protocol
market
walletAddress
eventType
assetSymbol
assetAddress
amount
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

Useful optional fields:

```text
amountUsd
healthFactor
ltv
liquidationThreshold
blockNumber
market
```

### 8.2 Event Type Enum

Normalize protocol-specific events into these values:

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

Examples:

```text
Aave Supply -> deposit
Aave Withdraw -> withdraw
Aave Borrow -> borrow
Aave Repay -> repay
Aave LiquidationCall -> liquidation
Compound Mint -> deposit
Compound Redeem -> withdraw
Compound Borrow -> borrow
Compound RepayBorrow -> repay
Compound LiquidateBorrow -> liquidation
```

### 8.3 Protocol Adapter Contract

Each adapter should do four jobs:

1. Load raw protocol data.
2. Validate required raw fields.
3. Map protocol-specific fields into the normalized schema.
4. Preserve raw metadata for debugging.

Adapter output rule:

```text
The rest of the app should never need to know whether the event came from Aave, Compound, or another protocol.
```

---

## 9. Feature Engineering

### 9.1 Wallet-Level Count Features

```text
depositCount
withdrawCount
borrowCount
repayCount
liquidationCount
uniqueAssetCount
uniqueProtocolCount
uniqueChainCount
activeDayCount
```

### 9.2 Amount Features

```text
totalDepositAmountUsd
totalWithdrawAmountUsd
totalBorrowAmountUsd
totalRepayAmountUsd
avgBorrowAmountUsd
maxBorrowAmountUsd
avgDepositAmountUsd
maxDepositAmountUsd
```

If `amountUsd` is unavailable, keep token amount features but mark the dataset as limited.

### 9.3 Ratio Features

Use safe division everywhere.

```text
repayToBorrowCountRatio
repayToBorrowAmountRatio
borrowToDepositAmountRatio
withdrawToDepositAmountRatio
liquidationToBorrowRatio
stablecoinBorrowRatio
stablecoinCollateralRatio
```

Safe division behavior:

```text
safeDivide(numerator, denominator) = 0 when denominator is 0
```

### 9.4 Time Features

```text
walletAgeDays
daysSinceFirstEvent
daysSinceLastEvent
eventsPerActiveDay
borrowEventsLast30Days
repayEventsLast30Days
liquidationsLast90Days
```

### 9.5 Risk-Oriented Flags

```text
previousLiquidationFlag
lowRepayRatioFlag
highBorrowFrequencyFlag
shortWalletAgeFlag
multiProtocolBorrowerFlag
volatileAssetExposureFlag
stablecoinHeavyFlag
```

---

## 10. Modeling Plan

### 10.1 MVP Label

Use binary target:

```text
hasLiquidation
```

Definition:

```text
0 = wallet has no liquidation events in observed history
1 = wallet has at least one liquidation event in observed history
```

This target is simple and suitable for MVP, but it is not a true future prediction.

### 10.2 Advanced Label

Use time-window target:

```text
willBeLiquidatedNext30Days
```

This requires:

- Point-in-time feature windows.
- Future label windows.
- Time-based train/test split.
- Leakage checks.

### 10.3 Baseline Models

Start with:

```text
Logistic Regression
Random Forest
```

Reason:

- Fast to train.
- Easy to debug.
- Good enough for feature validation.
- Helps detect data leakage before stronger models.

### 10.4 Main Models

After baseline:

```text
XGBoost
LightGBM
```

Use one main model first. Do not add model complexity until baseline metrics and data quality are understood.

### 10.5 Evaluation

Because liquidation labels are usually imbalanced, do not rely on accuracy.

Use:

```text
ROC-AUC
PR-AUC
precision
recall
F1
confusion matrix
calibration curve
```

Review questions:

- Is liquidation class too rare?
- Does the model predict only the majority class?
- Are any features direct leakage from the label?
- Does the train/test split leak future behavior?

---

## 11. Credit Score Design

Model output:

```text
pLiquidation in [0, 1]
```

Credit score:

```python
creditScore = int(850 - pLiquidation * 550)
creditScore = max(300, min(850, creditScore))
```

Score bands:

```text
750-850 = Excellent
650-749 = Good
550-649 = Medium
450-549 = Risky
300-449 = Very Risky
```

Example output:

```json
{
  "walletAddress": "0xabc...",
  "protocols": ["aave"],
  "liquidationProbability": 0.48,
  "creditScore": 586,
  "riskLevel": "Medium"
}
```

---

## 12. Recommendation Design

### 12.1 Purpose

The score answers:

```text
How risky is this wallet?
```

The recommendation answers:

```text
What should this wallet do to borrow more safely?
```

### 12.2 MVP Recommendation Rules

Use deterministic rules first.

Inputs:

```text
creditScore
riskLevel
walletFeatures
protocol
optional market metadata
```

Outputs:

```text
recommendedLtvRange
recommendedCollateralTypes
avoidAssets
riskReducingActions
explanation
```

### 12.3 Safe LTV Bands

```text
Score >= 750 -> 65-70%
Score >= 650 -> 50-60%
Score >= 550 -> 35-45%
Score >= 450 -> 25-35%
Score < 450  -> 15-25%
```

These are conservative portfolio demo bands. They are not protocol-specific liquidation thresholds.

### 12.4 Recommendation Examples

Low risk:

```text
Keep LTV below 65-70%.
Prefer high-liquidity collateral.
Keep a health factor buffer.
```

Medium risk:

```text
Keep LTV below 35-45%.
Prefer stablecoins and blue-chip collateral.
Repay earlier if collateral volatility increases.
```

High risk:

```text
Avoid new borrowing until debt is reduced.
Keep LTV below 25-35%.
Avoid volatile collateral.
Increase collateral buffer.
```

---

## 13. API Design

### 13.1 Endpoints

```text
GET  /health
POST /score-wallet
POST /recommend
POST /analyze-wallet
POST /agent-chat
```

### 13.2 POST /score-wallet

Input:

```json
{
  "walletAddress": "0xabc...",
  "protocols": ["aave"]
}
```

Output:

```json
{
  "walletAddress": "0xabc...",
  "protocols": ["aave"],
  "liquidationProbability": 0.48,
  "creditScore": 586,
  "riskLevel": "Medium",
  "features": {
    "borrowCount": 8,
    "repayCount": 5,
    "liquidationCount": 0
  }
}
```

### 13.3 POST /recommend

Input:

```json
{
  "walletAddress": "0xabc...",
  "creditScore": 586,
  "riskLevel": "Medium",
  "protocols": ["aave"]
}
```

Output:

```json
{
  "walletAddress": "0xabc...",
  "recommendedLtvRange": "35-45%",
  "recommendedCollateralTypes": ["stablecoin", "blue-chip"],
  "avoidAssets": ["low-liquidity volatile tokens"],
  "actions": [
    "Keep LTV below 40%",
    "Repay earlier if health factor drops",
    "Avoid adding volatile collateral"
  ]
}
```

### 13.4 POST /analyze-wallet

Combines score, explanation, and recommendation.

Input:

```json
{
  "walletAddress": "0xabc...",
  "protocols": ["aave"]
}
```

Output:

```json
{
  "walletAddress": "0xabc...",
  "creditScore": 586,
  "riskLevel": "Medium",
  "liquidationProbability": 0.48,
  "topRiskFactors": [
    "Low repay-to-borrow ratio",
    "High borrow frequency",
    "Volatile collateral exposure"
  ],
  "recommendation": {
    "recommendedLtvRange": "35-45%",
    "recommendedCollateralTypes": ["stablecoin", "blue-chip"],
    "actions": [
      "Keep LTV below 40%",
      "Repay earlier if risk increases"
    ]
  },
  "disclaimer": "Research output only. Not financial advice."
}
```

### 13.5 POST /agent-chat

Input:

```json
{
  "message": "Analyze wallet 0xabc on Aave and recommend a safer borrowing strategy."
}
```

Output:

```json
{
  "answer": "Wallet 0xabc has a Medium risk profile with a score of 586. Main risk factors are low repay-to-borrow ratio and high borrow frequency. A conservative LTV range is 35-45%. This is not financial advice.",
  "toolOutputs": {
    "score": {},
    "recommendation": {},
    "explanation": {}
  }
}
```

---

## 14. Suggested Repository Structure

Use Python package names that are importable. Use kebab-case for docs and external artifact filenames.

```text
defi-risk-advisor-agent/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── docs/
│   ├── overview.md
│   ├── system-architecture.md
│   ├── code-standards.md
│   └── model-limitations.md
│
├── notebooks/
│   ├── 01-eda.ipynb
│   ├── 02-feature-engineering.ipynb
│   └── 03-model-training.ipynb
│
├── src/
│   └── defi_risk_advisor/
│       ├── app_config.py
│       ├── adapters/
│       │   ├── base_adapter.py
│       │   └── aave_adapter.py
│       ├── data/
│       │   ├── event_schema.py
│       │   ├── load_events.py
│       │   └── validate_events.py
│       ├── features/
│       │   ├── feature_schema.py
│       │   └── wallet_feature_builder.py
│       ├── models/
│       │   ├── train_model.py
│       │   ├── evaluate_model.py
│       │   └── predict_risk.py
│       ├── scoring/
│       │   ├── credit_score.py
│       │   └── risk_level.py
│       ├── recommender/
│       │   ├── ltv_rules.py
│       │   └── recommendation_service.py
│       ├── explainability/
│       │   └── risk_explainer.py
│       ├── agent/
│       │   ├── agent_service.py
│       │   ├── prompts.py
│       │   └── tools.py
│       └── api/
│           ├── main.py
│           ├── schemas.py
│           └── routes.py
│
├── models/
│   ├── baseline-model.joblib
│   ├── main-risk-model.joblib
│   └── feature-columns.json
│
├── reports/
│   ├── eda-summary.md
│   ├── metrics.json
│   └── sample-wallet-report.md
│
├── tests/
│   ├── test-adapters.py
│   ├── test-features.py
│   ├── test-scoring.py
│   ├── test-recommender.py
│   └── test-api.py
│
├── .env.example
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 15. Implementation Loop

Use this loop for every feature.

```text
1. Confirm feature goal.
2. Check existing docs and code.
3. Implement the smallest useful slice.
4. Run compile check.
5. Run focused tests.
6. Review for correctness, security, and simplicity.
7. Update docs if behavior changed.
8. Move to next slice only when current slice passes.
```

Default verification commands:

```bash
uv run python -m compileall src tests
uv run pytest
uv run ruff check .
```

If `src/` or `tests/` do not exist yet, use the commands that match the current stage.

---

## 16. Detailed Feature Plan

The detailed per-feature implementation guidelines are split into smaller docs in [feature-plans/README.md](feature-plans/README.md). Use those files while implementing. This section remains the high-level roadmap.

### Feature 0: Project Foundation

Goal:

```text
Create a reproducible UV-managed Python project foundation.
```

Small steps:

1. Confirm `.python-version` is pinned to `3.11`.
2. Update `pyproject.toml` description.
3. Add initial runtime dependencies with `uv add` only when code needs them.
4. Add dev dependencies with `uv add --dev` only when tests/lint are introduced.
5. Create `src/defi_risk_advisor/`.
6. Create `src/defi_risk_advisor/app_config.py`.
7. Add `.env.example` with non-secret placeholders.
8. Add README setup commands using UV.
9. Run `uv sync`.
10. Commit `uv.lock` after dependencies are added.

Review checklist:

- No `requirements.txt` unless exported for a specific deployment need.
- No secrets in `.env.example`.
- Project runs through `uv run`.
- README does not require manual virtualenv activation.

Done criteria:

- A new developer can clone, run `uv sync`, and run the starter command.

### Feature 1: Protocol-Normalized Event Schema

Goal:

```text
Define one event contract that all protocol data maps into.
```

Small steps:

1. Create an event schema model.
2. Define valid event types.
3. Define required fields.
4. Define optional enriched fields.
5. Add wallet address normalization.
6. Add timestamp normalization.
7. Add amount numeric validation.
8. Add tests for valid and invalid events.
9. Document field meanings.

Review checklist:

- Schema does not mention only Aave.
- Unknown raw events can be preserved without crashing.
- Validation errors are useful and do not expose sensitive data.

Done criteria:

- Raw data from any lending protocol can be represented after mapping.

### Feature 2: Aave Adapter as First Protocol Adapter

Goal:

```text
Support Aave as the first real adapter without coupling the core to Aave.
```

Small steps:

1. Choose MVP Aave data source.
2. Document source, chain, date range, and fields.
3. Implement raw CSV loader if using a dataset export.
4. Map Aave event names into normalized event types.
5. Map wallet, asset, amount, timestamp, and tx hash.
6. Preserve raw event type and source.
7. Save normalized events to `data/interim/normalized-events.csv`.
8. Add adapter tests with small sample rows.
9. Add data quality report.

Review checklist:

- Aave names stay inside adapter code.
- Output matches normalized schema.
- Missing required fields fail clearly.
- No fake production data is used to claim model quality.

Done criteria:

- Aave data can be normalized by script and loaded by downstream code.

### Feature 3: Data Validation and EDA

Goal:

```text
Understand whether the selected dataset can support the MVP label.
```

Small steps:

1. Load normalized events.
2. Count rows.
3. Count unique wallets.
4. Count events by event type.
5. Count wallets with liquidation.
6. Count assets and protocols.
7. Check missing required fields.
8. Check duplicate tx/event ids.
9. Check timestamp range.
10. Save `reports/eda-summary.md`.

Review checklist:

- Liquidation class exists.
- Class imbalance is documented.
- Dataset limitations are explicit.
- Any schema workaround is documented.

Done criteria:

- There is enough evidence to decide whether to train the MVP model.

### Feature 4: Wallet Feature Builder

Goal:

```text
Convert normalized events into one row per wallet.
```

Small steps:

1. Group normalized events by wallet.
2. Build count features.
3. Build amount aggregate features.
4. Build ratio features with safe division.
5. Build activity window features.
6. Build protocol and chain diversity features.
7. Add label `hasLiquidation`.
8. Replace null, inf, and invalid values.
9. Export `data/processed/wallet-features.csv`.
10. Add tests for empty, single-wallet, and multi-wallet data.

Review checklist:

- One output row equals one wallet.
- Label is not accidentally included in model features.
- Safe division handles zero denominators.
- Feature names are stable.

Done criteria:

- Feature generation is reproducible by command.

### Feature 5: Baseline ML Training

Goal:

```text
Train simple models to validate data and feature usefulness.
```

Small steps:

1. Load wallet features.
2. Separate features from label.
3. Split train/test data.
4. Train Logistic Regression.
5. Train Random Forest.
6. Evaluate ROC-AUC and PR-AUC.
7. Evaluate precision, recall, F1, and confusion matrix.
8. Save metrics to `reports/metrics.json`.
9. Save best baseline model to `models/baseline-model.joblib`.
10. Document baseline limitations.

Review checklist:

- Metrics are not accuracy-only.
- Imbalance handling is documented.
- No leakage columns are used.
- Model artifact includes feature column order.

Done criteria:

- At least one baseline trains and produces saved metrics.

### Feature 6: Main Risk Model

Goal:

```text
Improve model quality after baseline validation.
```

Small steps:

1. Choose XGBoost or LightGBM, not both initially.
2. Add dependency with `uv add`.
3. Train model using the same feature contract.
4. Tune only a small set of hyperparameters.
5. Compare with baseline metrics.
6. Save model artifact.
7. Save feature columns.
8. Add prediction utility.
9. Add tests for loading model and validating feature order.

Review checklist:

- Stronger model beats or justifies replacing baseline.
- Prediction fails clearly when feature columns mismatch.
- No unnecessary model registry complexity yet.

Done criteria:

- A saved model can predict liquidation probability for a wallet feature row.

### Feature 7: Credit Score Service

Goal:

```text
Convert model probability into a stable credit score and risk band.
```

Small steps:

1. Implement probability validation.
2. Implement probability-to-score mapping.
3. Clamp score to 300-850.
4. Implement score-to-risk-level mapping.
5. Add tests for boundaries.
6. Add tests for invalid probabilities.
7. Document score bands.

Review checklist:

- Mapping is deterministic.
- Invalid model outputs do not silently pass.
- Labels match API docs.

Done criteria:

- Any probability from 0 to 1 returns score and risk level.

### Feature 8: Risk Explanation

Goal:

```text
Explain model output in user-facing language.
```

Small steps:

1. Create feature display-name mapping.
2. Add rule-based explanation fallback.
3. Add model feature importance explanation.
4. Optionally add SHAP later.
5. Return top 3 to 5 risk factors.
6. Avoid overclaiming causality.
7. Add tests for known feature patterns.
8. Add sample explanations report.

Review checklist:

- Explanation is understandable.
- Explanation does not claim certainty.
- Technical feature names do not leak into user response unless useful.

Done criteria:

- Every score response can include top risk factors.

### Feature 9: Recommendation Engine

Goal:

```text
Suggest safer borrowing behavior based on score and wallet profile.
```

Small steps:

1. Implement LTV band rules.
2. Implement collateral type guidance.
3. Implement avoid-asset guidance.
4. Implement risk-reducing actions.
5. Include protocol-specific caveat when needed.
6. Add deterministic tests for each score band.
7. Add tests for high liquidation history.
8. Add sample recommendation outputs.

Review checklist:

- Recommendation is not financial advice.
- Recommendation does not depend on hardcoded Aave only.
- Rules are simple and maintainable.

Done criteria:

- Given score, risk level, and features, the service returns a complete recommendation.

### Feature 10: FastAPI Backend

Goal:

```text
Expose scoring and recommendations through clean API endpoints.
```

Small steps:

1. Create FastAPI app.
2. Create Pydantic request and response schemas.
3. Add `/health`.
4. Add `/score-wallet`.
5. Add `/recommend`.
6. Add `/analyze-wallet`.
7. Load model at startup.
8. Add consistent error responses.
9. Add API tests with `httpx`.
10. Verify Swagger docs.

Review checklist:

- Wallet address input is validated.
- Unknown wallet returns useful error.
- Error logs do not include secrets.
- API response matches docs.

Done criteria:

- API runs locally with `uv run` and tests pass.

### Feature 11: Agent Service

Goal:

```text
Let users ask natural-language wallet risk questions while tools do the real work.
```

Small steps:

1. Define agent tool interfaces.
2. Implement wallet address extraction.
3. Implement scoring tool wrapper.
4. Implement recommendation tool wrapper.
5. Implement explanation tool wrapper.
6. Create deterministic response fallback.
7. Add optional LLM provider only after fallback works.
8. Add guardrail prompt.
9. Add `/agent-chat`.
10. Add sample chat tests.

Review checklist:

- Agent does not replace model logic.
- Agent does not execute transactions.
- Agent does not guarantee returns or safety.
- Agent can respond when LLM key is missing.

Done criteria:

- Agent can analyze a wallet through internal tools and explain the result.

### Feature 12: Optional Dashboard

Goal:

```text
Create a fast visual demo for portfolio review.
```

Small steps:

1. Choose Streamlit unless a custom frontend is required.
2. Add wallet input.
3. Call `/analyze-wallet`.
4. Display credit score.
5. Display risk band.
6. Display liquidation probability.
7. Display top risk factors.
8. Display recommendation.
9. Display disclaimer.
10. Add screenshot to docs.

Review checklist:

- UI calls real API.
- No fake success states.
- Errors are visible and useful.
- Demo can be run from README.

Done criteria:

- Project can be demoed visually in under five minutes.

### Feature 13: Portfolio Polish and Documentation

Goal:

```text
Make the project understandable and credible for GitHub, CV, and interviews.
```

Small steps:

1. Update README overview.
2. Add setup and run commands.
3. Add architecture diagram.
4. Add dataset section.
5. Add model methodology.
6. Add API examples.
7. Add limitations.
8. Add sample outputs.
9. Add model card.
10. Add CV bullets.

Review checklist:

- Docs match actual code.
- Limitations are honest.
- No dataset or model quality claims without evidence.
- Commands use UV.

Done criteria:

- Another developer can understand, run, and evaluate the project.

---

## 17. Recommended Build Order

Build the project in this order:

```text
Feature 0: Project Foundation
Feature 1: Protocol-Normalized Event Schema
Feature 2: Aave Adapter as First Protocol Adapter
Feature 3: Data Validation and EDA
Feature 4: Wallet Feature Builder
Feature 5: Baseline ML Training
Feature 7: Credit Score Service
Feature 9: Recommendation Engine
Feature 10: FastAPI Backend
Feature 8: Risk Explanation
Feature 11: Agent Service
Feature 12: Optional Dashboard
Feature 13: Portfolio Polish and Documentation
Feature 6: Main Risk Model
```

Reason:

- Baseline model should come before stronger model.
- API can use baseline first.
- Agent should call existing tools, not invent results.
- Main model upgrade can happen after the end-to-end product works.

---

## 18. Acceptance Criteria for MVP

MVP is complete when:

1. Project uses UV commands in docs and setup.
2. One real protocol adapter produces normalized events.
3. Wallet feature generation is reproducible.
4. A baseline model trains and saves metrics.
5. Credit score and risk level are deterministic.
6. Recommendation output is deterministic.
7. `/analyze-wallet` returns score, explanation, and recommendation.
8. Agent chat can explain a wallet using tool outputs.
9. Tests cover scoring, recommendations, features, and API basics.
10. README documents setup, usage, limitations, and sample output.

---

## 19. Risk and Limitation Notes

Important limitations:

```text
This project is for research and education only.
The score is not financial advice.
The score does not guarantee future wallet behavior.
Liquidation is only a proxy for borrower risk.
Wallet-level identity is imperfect because one user can control many wallets.
Historical protocol data may not generalize across protocols or market regimes.
Class imbalance can make model evaluation misleading.
Protocol-specific mechanics can affect risk interpretation.
```

---

## 20. Future Work

High-value upgrades:

- Add Compound adapter.
- Add Morpho adapter.
- Add time-window liquidation prediction.
- Add point-in-time feature store.
- Add SHAP explanations.
- Add protocol metadata for real LTV thresholds.
- Add live data fetching from The Graph, Dune, or direct RPC/indexer.
- Add wallet clustering.
- Add graph-based protocol and token features.
- Add PDF wallet risk report export.
- Add production monitoring and drift checks.

---

## 21. CV Bullets

Long version:

```text
Built a protocol-agnostic DeFi Risk Advisor Agent that normalizes lending protocol events, trains ML models for wallet liquidation risk, converts model probabilities into explainable credit scores, and recommends safer borrowing strategies through FastAPI and an agent tool layer.
```

Short version:

```text
Developed an ML-based DeFi wallet risk scoring system with protocol adapters, credit score mapping, risk-aware recommendations, and FastAPI endpoints.
```

---

## 22. Unresolved Questions

1. Which first dataset should be used: Aave subgraph, Dune export, Flipside export, or curated CSV?
2. Which first chain should MVP target: Ethereum mainnet only, or include Polygon/Arbitrum?
3. Should MVP train on `hasLiquidation`, or is there enough timestamped data for `willBeLiquidatedNext30Days`?
4. Which LLM provider should the optional agent use after deterministic fallback works?
5. Should the demo UI be Streamlit, or should the project stay API-only until the ML core is stronger?

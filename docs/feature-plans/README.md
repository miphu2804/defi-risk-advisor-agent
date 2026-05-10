# Feature Implementation Plans

This folder splits the project roadmap into smaller implementation guidelines. Use one file per feature, finish its review checklist, then move to the next feature.

## Current Status

| Feature | Status | Notes |
|---|---|---|
| 00: Project Foundation | DONE (with deviations) | Flat `src/`, not `src/defi_risk_advisor/`; `test/` not `tests/`; black+isort, not ruff |
| 01: Normalized Event Schema | NOT STARTED | Deferred; EDA done on raw data first |
| 02: Aave Adapter | NOT STARTED | Dataset identified, Kaggle downloader exists |
| 03: Data Validation & EDA | DONE | Raw-data EDA notebook and `reports/eda-summary.md` completed; normalized-event EDA deferred |
| 04-13 | NOT STARTED | — |

## Build Order

1. [Feature 00: Project Foundation](00-project-foundation.md) ✅
2. [Feature 01: Normalized Event Schema](01-normalized-event-schema.md)
3. [Feature 02: Aave Adapter](02-aave-adapter.md)
4. [Feature 03: Data Validation and EDA](03-data-validation-eda.md) ✅
5. [Feature 04: Wallet Feature Builder](04-wallet-feature-builder.md)
6. [Feature 05: Baseline ML Training](05-baseline-ml-training.md)
7. [Feature 07: Credit Score Service](07-credit-score-service.md)
8. [Feature 09: Recommendation Engine](09-recommendation-engine.md)
9. [Feature 10: FastAPI Backend](10-fastapi-backend.md)
10. [Feature 08: Risk Explanation](08-risk-explanation.md)
11. [Feature 11: Agent Service](11-agent-service.md)
12. [Feature 12: Dashboard](12-dashboard.md)
13. [Feature 13: Portfolio Documentation](13-portfolio-docs.md)
14. [Feature 06: Main Risk Model](06-main-risk-model.md)

## Key Divergences from Original Plan

1. **Package layout**: Flat `src/` instead of `src/defi_risk_advisor/`. Simpler for early stage; subpackage can be introduced later.
2. **Schema deferred**: Normalized event schema (Feature 01) was skipped initially. EDA was done on raw Aave V3 data to understand the dataset first.
3. **Extra components built**: Kaggle downloader (`src/downloader/`), download CLI script, and path utilities added before the schema layer.
4. **Tooling**: black + isort instead of ruff + mypy.
5. **Dataset**: Aave V3 Ethereum only, 379K rows, only 21 liquidation events — extreme class imbalance is the main risk.

## Why the Original Build Order Still Holds

- Build the protocol-agnostic data contract before adapters.
- Use Aave only as first adapter, not core design.
- Train baseline before advanced model.
- Ship API and deterministic recommendation before LLM agent.
- Upgrade model after the end-to-end product works.

## Per-Feature Loop

```text
Plan -> implement smallest slice -> compile -> focused tests -> review -> docs update -> next slice
```

## Default Commands

```bash
uv sync
uv run python -m compileall src test
uv run pytest
```

Note: `ruff check .` not applicable — project uses black + isort via pre-commit instead.

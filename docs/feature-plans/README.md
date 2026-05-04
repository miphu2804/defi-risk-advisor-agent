# Feature Implementation Plans

This folder splits the project roadmap into smaller implementation guidelines. Use one file per feature, finish its review checklist, then move to the next feature.

Build order:

1. [Feature 00: Project Foundation](00-project-foundation.md)
2. [Feature 01: Normalized Event Schema](01-normalized-event-schema.md)
3. [Feature 02: Aave Adapter](02-aave-adapter.md)
4. [Feature 03: Data Validation and EDA](03-data-validation-eda.md)
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

Why this order:

- Build the protocol-agnostic data contract before adapters.
- Use Aave only as first adapter, not core design.
- Train baseline before advanced model.
- Ship API and deterministic recommendation before LLM agent.
- Upgrade model after the end-to-end product works.

Per-feature loop:

```text
Plan -> implement smallest slice -> compile -> focused tests -> review -> docs update -> next slice
```

Default commands:

```bash
uv sync
uv run python -m compileall src tests
uv run pytest
uv run ruff check .
```

If a command is not valid yet because folders do not exist, run the closest available command and document the gap.

## Unresolved Questions

1. Should these plans become GitHub issues later?
2. Should each feature have a matching branch, or should early docs/setup changes stay on one branch?
3. Which dataset source should become the first adapter target?

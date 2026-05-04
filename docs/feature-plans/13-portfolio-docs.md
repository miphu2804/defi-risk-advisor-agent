# Feature 13: Portfolio Documentation

## Goal

Make the project easy to understand, run, and discuss in interviews.

## Scope

Included:

- README polish.
- Architecture doc.
- Model limitations.
- API examples.
- Sample outputs.
- CV bullets.

Not included:

- Marketing landing page.
- Overstated performance claims.
- Production SLO docs.

## Files

Create or update:

```text
README.md
docs/overview.md
docs/system-architecture.md
docs/model-limitations.md
docs/api-examples.md
docs/code-standards.md
reports/sample-wallet-report.md
reports/metrics.json
```

## README Sections

```text
Overview
Features
Architecture
Dataset
How to Run
API Usage
Sample Output
Model Methodology
Limitations
Roadmap
CV Bullet
```

## Implementation Steps

1. Update README to match actual implemented features.
2. Add architecture diagram in text or Mermaid.
3. Add dataset source and limitations.
4. Add model training summary.
5. Add evaluation metrics.
6. Add API request and response examples.
7. Add sample wallet analysis.
8. Add clear limitations.
9. Add roadmap.
10. Add CV bullets.

## Documentation Rules

- Use UV commands only.
- Do not claim production readiness unless deployed and monitored.
- Do not claim model quality without metrics.
- Keep limitations visible.
- Keep Aave framed as first adapter, not permanent scope.

## Review Checklist

- README commands run.
- Docs match code behavior.
- Metrics match latest report.
- No secrets or private dataset paths.
- Unresolved questions are listed.

## Verification

```bash
uv sync
uv run python main.py
```

If API exists:

```bash
uv run pytest
uv run uvicorn defi_risk_advisor.api.main:app --reload
```

## Done Criteria

- Another developer can clone, run, and understand the project.
- Interviewer can see the AI engineering story quickly.

## Unresolved Questions

1. Should docs include a model card as a separate file?
2. Should dataset license details be included in README or separate docs?
3. Should project roadmap use GitHub issues after MVP docs are done?

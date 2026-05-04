# Feature 12: Dashboard

## Goal

Create a quick portfolio demo that visualizes wallet score, risk factors, and recommendations.

## Scope

Included:

- Wallet input.
- API call to `/analyze-wallet`.
- Score display.
- Risk factor display.
- Recommendation display.
- Disclaimer.

Not included:

- Full frontend app.
- Authentication.
- Chart-heavy analytics.
- Admin panel.

## Files

Option A, recommended:

```text
dashboard/app.py
README.md
docs/screenshots/
```

Option B, defer unless needed:

```text
frontend/
```

## Recommendation

Use Streamlit first. It is enough for a side project demo and avoids spending time on frontend before the ML/API core is credible.

## Dependencies

Add only when dashboard starts:

```bash
uv add streamlit requests
```

## Implementation Steps

1. Create `dashboard/app.py`.
2. Add wallet address input.
3. Add protocol selector.
4. Call FastAPI `/analyze-wallet`.
5. Display credit score.
6. Display risk level.
7. Display liquidation probability.
8. Display top risk factors.
9. Display recommendation actions.
10. Display disclaimer.

## Review Checklist

- Dashboard calls real API.
- No fake success state.
- Error messages are visible.
- UI does not make financial advice claims.
- README has run command.

## Verification

```bash
uv run streamlit run dashboard/app.py
```

Manual check:

```text
Open dashboard.
Enter known test wallet.
Confirm score, risk factors, and recommendation render.
Stop API and confirm dashboard shows useful error.
```

## Done Criteria

- Demo can be run in under five minutes from README.
- Screenshot can be added to docs.

## Unresolved Questions

1. Should dashboard be Streamlit-only for MVP?
2. Should screenshots be committed?
3. Should dashboard support wallet compare in first version?

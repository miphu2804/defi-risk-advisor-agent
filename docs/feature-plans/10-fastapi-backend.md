# Feature 10: FastAPI Backend

## Goal

Expose scoring, recommendation, explanation, and combined wallet analysis through API endpoints.

## Scope

Included:

- FastAPI app.
- Pydantic schemas.
- Health endpoint.
- Score endpoint.
- Recommend endpoint.
- Analyze endpoint.
- Basic API tests.

Not included:

- Authentication.
- Rate limiting.
- Production deployment.
- Agent chat, handled in Feature 11.

## Files

Create or update:

```text
src/defi_risk_advisor/api/main.py
src/defi_risk_advisor/api/schemas.py
src/defi_risk_advisor/api/routes.py
src/defi_risk_advisor/api/errors.py
tests/test-api.py
README.md
```

## Dependencies

Add when API starts:

```bash
uv add fastapi uvicorn pydantic-settings
uv add --dev httpx
```

## Endpoints

```text
GET  /health
POST /score-wallet
POST /recommend
POST /analyze-wallet
```

## Implementation Steps

1. Create FastAPI app factory if useful.
2. Add `/health`.
3. Define request schemas.
4. Define response schemas.
5. Add wallet address validation.
6. Wire `/score-wallet` to model prediction and credit score service.
7. Wire `/recommend` to recommendation service.
8. Wire `/analyze-wallet` to score, explanation, and recommendation.
9. Add consistent error response for unknown wallet or missing model.
10. Add API tests with `TestClient` or `httpx`.

## Error Rules

- Unknown wallet returns 404 or clear 422 based on source.
- Invalid wallet input returns validation error.
- Missing model returns service unavailable style error.
- Never include secret values in logs or responses.

## Review Checklist

- API contracts match docs.
- Wallet input is validated.
- Swagger UI works.
- Tests cover success and validation failure.
- No agent logic is mixed into API core routes.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-api.py
uv run uvicorn defi_risk_advisor.api.main:app --reload
```

## Done Criteria

- Local API can analyze a wallet through `/analyze-wallet`.
- README includes API run command and sample request.

## Unresolved Questions

1. Should API load model at startup or lazily on first request?
2. Should unknown wallet be 404 or 422?
3. Should API support multiple protocols in first route version?

# Feature 11: Agent Service

## Goal

Let users ask natural-language wallet risk questions while deterministic tools perform scoring and recommendations.

## Scope

Included:

- Wallet extraction.
- Tool wrappers.
- Deterministic response fallback.
- Optional LLM provider hook.
- `/agent-chat` endpoint.
- Guardrails.

Not included:

- Autonomous trading.
- Transaction signing.
- Portfolio management.
- RAG over protocol docs.

## Files

Create or update:

```text
src/defi_risk_advisor/agent/tools.py
src/defi_risk_advisor/agent/prompts.py
src/defi_risk_advisor/agent/agent_service.py
src/defi_risk_advisor/api/routes.py
tests/test-agent-service.py
reports/sample-agent-conversations.md
```

## Tool Contract

Agent tools:

```text
scoreWallet(walletAddress, protocols)
recommendStrategy(walletAddress, score, riskLevel, features)
explainRisk(walletAddress, features, scoreResult)
generateWalletReport(walletAddress)
```

## Implementation Steps

1. Implement EVM wallet address extraction.
2. Define tool wrapper functions.
3. Build deterministic response composer.
4. Add guardrail text.
5. Add optional LLM provider interface only after fallback works.
6. Add `/agent-chat`.
7. Return tool outputs for transparency.
8. Add tests for valid wallet prompt.
9. Add tests for no-wallet prompt.
10. Add sample conversations report.

## Guardrails

The agent must:

- Avoid financial advice claims.
- Avoid profit guarantees.
- Avoid liquidation certainty claims.
- Refuse transaction execution.
- Explain that model output is research only.

## Review Checklist

- Agent calls tools instead of inventing scores.
- Agent works when no LLM key is configured.
- Prompt does not contain secrets.
- Refusal behavior exists for transaction requests.
- Tests cover no-wallet and risky wallet prompts.

## Verification

```bash
uv run python -m compileall src tests
uv run pytest tests/test-agent-service.py
```

## Done Criteria

- `/agent-chat` can analyze a wallet and explain score/recommendation.
- Response includes disclaimer and tool outputs.

## Unresolved Questions

1. Which LLM provider should be optional first?
2. Should chat history be stored or stateless for MVP?
3. Should the agent support comparing wallets in MVP?

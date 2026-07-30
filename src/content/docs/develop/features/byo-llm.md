---
title: BYO LLM
---

When the BYO LLM toggle is on, the platform routes LLM calls through your own provider instead of Surogate's bundled endpoints. Surogate charges only for platform usage (storage, compute, sessions); your provider charges for tokens.

## When to enable

- **Existing contract with an LLM provider**: you've already negotiated rates with OpenAI / Anthropic / Together / your-vendor — keep using them.
- **Self-hosted models**: you serve via vLLM in your own cluster.
- **Compliance**: you need LLM calls to stay within your VPC / on-prem.
- **Multi-region routing**: you want to direct traffic to the geographically nearest endpoint.

When BYO LLM is OFF, the platform uses its bundled LLM endpoints. You pay Surogate for everything.

When BYO LLM is ON, you configure providers per-agent (CONFIG → Model) and pay providers directly. Surogate charges only for **platform usage** — storage, compute, sessions.

## Per-agent overrides

The BYO LLM toggle is **org-level** — it enables the option. Each agent then configures its own provider in CONFIG → Model.

Format for a URL-source agent:

```yaml
model:
  source: url
  url: https://api.openai.com/v1
  model_name: gpt-5
  api_key_ref: openai_org_key       # vault reference
```

The platform's `runtime_config.py` handles the routing — for each session, it reads the agent's model config and routes the request accordingly.

## API key management

Provider API keys live in the Vault. Reference them by name in agent configs:

```yaml
api_key_ref: anthropic_prod_key
```

The platform never logs or exposes the actual key. Rotation: update the value in the Vault → agents pick up the new key on next session.

## Cost monitoring

When BYO LLM is on, Surogate doesn't see your provider's bills directly. The platform estimates token cost via per-model rate cards configured in `core/billing/plans.py`. The estimate is shown in the session's METADATA tab.

For exact costs, cross-reference with your provider's billing dashboard.

## Mixing providers

You can mix providers across agents:

- `agent-1` uses Anthropic via BYO
- `agent-2` uses OpenAI via BYO
- `agent-3` uses Surogate's bundled model

The platform doesn't care which provider each agent uses — it routes per-agent based on CONFIG.


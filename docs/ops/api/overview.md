---
title: API overview
sidebar_position: 1
slug: /api/overview
description: How external callers reach Surogate Ops — auth, base URL, request shape, the two surfaces (models, agents).
---

# API overview

Every part of Surogate Ops exposed in the UI is also reachable through an HTTP API. Your own services call it the same way: hit a model directly, hit an agent for chat-shaped traffic, push and pull from the Hub for artifacts, manage the catalog of models and agents from CI.

This page is the entry point — base URL, authentication, request shape, error model. The endpoint-specific reference is in the sub-pages.

## Base URLs

Surogate Ops exposes API surfaces on three distinct hosts, each handling a different traffic shape:

| Surface | Base URL | Use it for |
|---|---|---|
| **Inference proxy** | `https://api.surogate.ai/v1`  | Calling models and agents (the OpenAI-compatible surface). |
| **Hub REST** | `https://hub.studio.internal/api/v1` | Managing repositories: list, create, push, pull metadata. |
| **Hub Git / S3** | `git.studio.internal:3000` (Git over HTTPS), `s3.studio.internal:9000` (S3 protocol) | Cloning, pushing artifacts, large-file transfer (Git LFS). |

The `hub.studio.internal` hosts are the in-cluster names. Your own services running outside the cluster see them under the public alias your admin configured.

## Authentication

Every Surogate API call carries an API key in the `Authorization` header. Three classes of key exist, with different scopes:

- **Model API key** — scoped to one model. Created from the model's detail page; one model can have many keys. Use it when an external service should reach exactly one model and nothing else.
- **Agent API key** — scoped to one agent. Created from the agent's detail page. The agent's underlying model is invoked transparently; the caller doesn't need a model key.
- **Hub access token** — scoped to a Hub user or to a project, with read or read-write rights. Created from Settings → Hub access tokens. Used for `git clone`, `git push`, and Hub REST calls.

Pass the key as a bearer token:

```http
Authorization: Bearer sk-<key-id>-<secret>
```

Keys never expire by default. Rotate them when:

- A team member with access to the key leaves.
- The key has been logged or shared in a place it shouldn't have been.
- You scheduled a rotation date (we recommend ninety days for production keys).

:::warning Rotate before revoke
Always *create-new, point-clients-at-new, then revoke-old.* Failed authentications are negative-cached for about a minute on the inference side, so a wrong key keeps failing briefly even after you've fixed it. Never delete first.
:::

## Request shape

The inference surface is **OpenAI-compatible**. Anything that talks to `https://api.openai.com/v1/chat/completions` talks to Surogate's inference surface with two changes:

1. Swap the base URL.
2. Swap the API key.

Concretely:

```bash
curl https://api.surogate.ai/v1/chat/completions \
  -H "Authorization: Bearer $SUROGATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-model-id-or-agent-slug",
    "messages": [{"role": "user", "content": "hello"}]
  }'
```

The `model` field accepts either a model id (when you're calling a model directly) or an agent slug (when you're calling an agent). For agents, Surogate routes through the agent's configured model and skills under the hood; the response shape stays OpenAI-compatible.

Streaming is supported via `"stream": true`. The response is a sequence of `data:` chunks, each chunk an OpenAI-compatible delta event. The stream terminates with `data: [DONE]`.

## Response shape

A successful response:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1735689600,
  "model": "your-model-id",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "Hi! How can I help?"},
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 9,
    "total_tokens": 21
  }
}
```

Two extra fields Surogate may set:

- `x-surogate-session-id` (header) — when the call is routed through an agent, this is the session id Studio's **Operate → Sessions** uses. Save it client-side if you want to deep-link back into the session for debugging.
- `x-surogate-skill-trace` (header, opt-in) — when an agent's skills fired during the response, this header carries a compact trace. Enable per-call by setting the request header `x-surogate-trace: 1`.

## SDKs

Surogate works with every SDK that supports an OpenAI-compatible base URL.

- **OpenAI Python SDK** — set `OPENAI_BASE_URL` to your Surogate inference base and `OPENAI_API_KEY` to your Surogate key. No code change needed.
- **OpenAI Node SDK** — same.
- **Anthropic / LangChain / LlamaIndex / etc.** — any of these can be configured to use an OpenAI-compatible endpoint; the configuration is library-specific.

There is no Surogate-specific SDK today. The OpenAI clients cover the inference surface; the Hub surface is plain HTTP / Git / S3, which every language already speaks.

## What's where

- **[Inference](./inference.md)** — calling a model or an agent, request and response detail, streaming.
- **[Hub](./hub.md)** — Git, S3, and REST surfaces for the artifact registry.
- **[Errors and rate limits](./errors-and-rate-limits.md)** — what failures look like, what limits apply.

## Where to go next

- **[Models](../features/models.mdx)** — to create and manage models.
- **[Agents](../features/agents.mdx)** — to create and manage agents.
- **[Data Hub](../features/hub.mdx)** — to manage repositories.

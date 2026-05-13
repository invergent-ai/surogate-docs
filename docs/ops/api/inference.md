---
title: Inference API
sidebar_position: 2
slug: /api/inference
description: OpenAI-compatible inference for models and agents. Chat completions, streaming, headers, system prompts.
---

# Inference API

The inference surface is how external callers reach a deployed model or agent. It's OpenAI-compatible — every SDK that targets `api.openai.com/v1/chat/completions` works against Surogate with two changes (base URL, API key).

This page is the endpoint reference. For the conceptual overview and authentication, see **[API overview](./overview.md)**.

## Endpoint

```
POST {base_url}/v1/chat/completions
```

Where `{base_url}` is your Surogate inference host (typically `https://api.surogate.ai`).

## Authentication

```http
Authorization: Bearer sk-<key-id>-<secret>
```

The key must be:

- A **model API key** (scoped to a single model), in which case the `model` field in the body must match that model's id, OR
- An **agent API key** (scoped to a single agent), in which case the `model` field must match the agent's slug.

A model key calling an agent (or vice-versa) returns `401 invalid_scope`.

## Request

```json
{
  "model": "your-model-id-or-agent-slug",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 1024,
  "stream": false
}
```

### Fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `model` | string | required | A model id or an agent slug. |
| `messages` | array | required | List of `{role, content}` pairs. Roles are `system`, `user`, `assistant`. |
| `temperature` | number | model default | Sampling temperature, 0 to 2. |
| `top_p` | number | model default | Nucleus sampling, 0 to 1. |
| `max_tokens` | integer | model default | Cap on completion tokens. |
| `stream` | boolean | `false` | Stream the response as SSE. |
| `tools` | array | unset | OpenAI-format tool definitions. Routed to the underlying model when supported.  |
| `tool_choice` | string \| object | `"auto"` | When tools are passed. |
| `stop` | string \| array | unset | Sequences that terminate generation. |
| `presence_penalty` | number | 0 | -2 to 2. |
| `frequency_penalty` | number | 0 | -2 to 2. |
| `user` | string | unset | Caller-supplied identifier for logging / abuse detection. |

### Agent-specific behaviour

When `model` is an agent slug, three things happen that are invisible in the request shape:

1. The agent's configured system prompt is prepended to your `messages` array.
2. The agent's attached **skills**, **MCP servers**, and **knowledge bases** are available to the underlying model.
3. The call is logged as a session under **Operate → Sessions**, recoverable from the `x-surogate-session-id` response header.

You can pass your own `system` message; the agent's system prompt is layered on top.

## Response

Non-streaming:

```json
{
  "id": "chatcmpl-7q9...",
  "object": "chat.completion",
  "created": 1735689600,
  "model": "your-model-id",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hi! How can I help today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 18,
    "completion_tokens": 9,
    "total_tokens": 27
  }
}
```

### Response headers

- `x-surogate-session-id` — present when `model` was an agent slug. Use it to deep-link to **Operate → Sessions** in Studio.
- `x-surogate-model-version` — the artifact commit the model is currently serving from. Pin this in your tests if you need reproducibility across model redeploys.
- `x-ratelimit-remaining` — remaining requests in your current minute / hour window. See [Errors and rate limits](./errors-and-rate-limits.md).

### `finish_reason` values

- `stop` — model produced a stop sequence or hit a natural end.
- `length` — hit `max_tokens`.
- `tool_calls` — the model wants to call a tool; check the `tool_calls` field on the message.
- `content_filter` — the response was blocked by an output filter.

## Streaming

Pass `"stream": true`. The server returns an event-stream where each event is a JSON delta:

```
data: {"id":"chatcmpl-...","object":"chat.completion.chunk","created":1735689600,"model":"your-model-id","choices":[{"index":0,"delta":{"content":"Hi"},"finish_reason":null}]}

data: {"id":"chatcmpl-...","object":"chat.completion.chunk","created":1735689600,"model":"your-model-id","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: {"id":"chatcmpl-...","object":"chat.completion.chunk","created":1735689600,"model":"your-model-id","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

The terminating `data: [DONE]` is the signal to close the stream.

## Examples

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.surogate.ai/v1",
    api_key="sk-...",
)

resp = client.chat.completions.create(
    model="my-support-agent",
    messages=[{"role": "user", "content": "How do I cancel?"}],
)
print(resp.choices[0].message.content)
print("Session:", resp.response.headers.get("x-surogate-session-id"))
```

### Node (OpenAI SDK)

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.surogate.ai/v1",
  apiKey: process.env.SUROGATE_API_KEY,
});

const resp = await client.chat.completions.create({
  model: "my-support-agent",
  messages: [{ role: "user", content: "How do I cancel?" }],
});
console.log(resp.choices[0].message.content);
```

### curl

```bash
curl https://api.surogate.ai/v1/chat/completions \
  -H "Authorization: Bearer $SUROGATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "my-support-agent",
    "messages": [{"role": "user", "content": "How do I cancel?"}]
  }'
```

## When something fails

Common shapes:

- **`401 invalid_scope`** — the key is valid but not scoped to the requested `model`. Create a new key against the right model or agent.
- **`404 model_not_found`** — the model or agent doesn't exist. Check the slug, and that the model is in **Serving** (not Stopped or Error).
- **`429 rate_limited`** — see [Errors and rate limits](./errors-and-rate-limits.md).
- **`502 upstream_error`** — the underlying model returned a transient failure. Retry with backoff.

## Where to go next

- **[API overview](./overview.md)** — base URL, auth, request shape.
- **[Hub API](./hub.md)** — for managing repositories.
- **[Errors and rate limits](./errors-and-rate-limits.md)** — the full failure / quota surface.

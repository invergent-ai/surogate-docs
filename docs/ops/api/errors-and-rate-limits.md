---
title: Errors and rate limits
sidebar_position: 4
slug: /api/errors-and-rate-limits
description: Error response shape, common codes, retry guidance, per-surface rate limits and quota signals.
---

# Errors and rate limits

This page is the failure surface for every API in Surogate Ops. The response shape is consistent across endpoints; the rate-limit story differs by surface.

## Error response shape

Every failed call returns a JSON body alongside the HTTP status:

```json
{
  "error": {
    "type": "rate_limited",
    "message": "Too many requests. Try again in 30s.",
    "request_id": "req_01HXYZ...",
    "details": {
      "retry_after_seconds": 30
    }
  }
}
```

- `type` — the machine-readable error code. Stable across releases; safe to switch on in your client.
- `message` — human-readable. Don't switch on this; the wording can change.
- `request_id` — the id to quote when filing a support request. Logged on the server alongside the full trace.
- `details` — error-specific structured fields. Optional; only present when there's something useful to say.

## Common errors

### `400 invalid_request`

Your request body or query string failed validation.

```json
{"error": {"type": "invalid_request", "message": "Field 'messages' is required."}}
```

Fix: read the message, fix the request. These are deterministic — retrying without changing the request won't help.

### `401 unauthenticated`

No `Authorization` header, or the header was malformed.

```json
{"error": {"type": "unauthenticated", "message": "Missing Authorization header."}}
```

Fix: pass a valid bearer token.

### `401 invalid_key`

The token in the header isn't recognised. Either revoked, never existed, or you're hitting the wrong host (a model key against the Hub REST surface, say).

```json
{"error": {"type": "invalid_key", "message": "API key not recognised."}}
```

Fix: create a new key from the right surface. Failed authentications are **negative-cached for about a minute** to protect the upstream — a wrong key keeps failing briefly after the fix.

### `401 invalid_scope`

The key is valid but not authorised for what you're calling — for example a model key against a different model, or a read-only Hub token attempting a push.

```json
{"error": {"type": "invalid_scope", "message": "API key not scoped for model 'support-agent-v2'."}}
```

Fix: create a new key scoped to the resource you actually want to call.

### `403 forbidden`

You're authenticated but don't have rights on this resource. Distinct from `invalid_scope` — the resource exists and your account exists, but membership / role doesn't grant access.

Fix: ask the resource owner to add you as a member.

### `404 not_found`

The resource doesn't exist. For inference this typically means the model id or agent slug is wrong, or the model is in **Stopped** / **Error** (Surogate treats unhealthy models as not-found from the inference plane).

```json
{"error": {"type": "model_not_found", "message": "Model 'qwen-3-8b' not found or not serving."}}
```

Fix: confirm the slug, confirm the model is **Serving**, redeploy if necessary.

### `409 conflict`

A state mismatch — for example trying to create a repo whose owner / name already exists, or trying to delete a key while a call is in flight against it.

Fix: usually deterministic; read the message.

### `413 payload_too_large`

The request body exceeded the surface's size limit. Inference messages are capped at the model's context window; Git non-LFS uploads are capped at 100 MB.

Fix: chunk the request, switch to LFS, or use S3.

### `422 validation_error`

Validation that runs deeper than `400`. Most common: the message array's tokens exceed the model's context window even though every individual field is well-formed.

```json
{
  "error": {
    "type": "context_overflow",
    "message": "Prompt token count 12453 exceeds model context window 8192.",
    "details": {"model_context": 8192, "prompt_tokens": 12453}
  }
}
```

Fix: trim the prompt, switch to a longer-context model.

### `429 rate_limited`

You hit a rate limit. The `details` object has the retry hint.

```json
{
  "error": {
    "type": "rate_limited",
    "message": "Too many requests on token 'sk-...'.",
    "details": {
      "retry_after_seconds": 12,
      "limit_window": "minute",
      "limit_max": 600,
      "limit_used": 600
    }
  }
}
```

Fix: back off and retry. Respect `Retry-After` header if present.

### `500 internal_error`

Surogate's fault. The request was syntactically valid but something blew up on the server.

```json
{"error": {"type": "internal_error", "message": "Unexpected error.", "request_id": "req_..."}}
```

Fix: retry with exponential backoff. If it persists, quote the `request_id` in a support request.

### `502 upstream_error`

The underlying model (for **OpenRouter** or **URL** sources) returned an error. Surogate proxied the failure through.

```json
{"error": {"type": "upstream_error", "message": "Upstream returned 429.", "details": {"upstream_status": 429}}}
```

Fix: usually transient. Retry. Persistent `502` usually means the upstream's credentials need refreshing.

### `503 service_unavailable`

Surogate is unhealthy — usually only seen during a controlled rollout. The `Retry-After` header tells you when to come back.

Fix: respect `Retry-After`. Don't tight-loop.

### `504 gateway_timeout`

The model took too long to respond. Streaming requests don't typically see this; non-streaming requests on a large completion can.

Fix: switch to streaming, reduce `max_tokens`, or pick a faster model.

## Retry guidance

A reasonable retry policy:

| Error | Retry? |
|---|---|
| `400`, `401`, `403`, `404`, `409`, `413`, `422` | **No.** Deterministic; fix the request. |
| `429` | **Yes**, after `retry_after_seconds`. |
| `500`, `502`, `503`, `504` | **Yes**, with exponential backoff (1s, 2s, 4s, 8s, max 5 attempts). |

Idempotency: inference requests are not idempotent (the same prompt can produce different responses). The Hub REST endpoints are mostly idempotent for `GET` and `DELETE`; `POST` (create) is not.

## Rate limits

Limits are applied per token, with separate windows per surface:

| Surface | Default per token | Window |
|---|---|---|
| **Inference (proxied model)** | 600 RPM, 50,000 TPM | per minute |
| **Inference (self-hosted serving)** | bounded by the serving container's batch capacity, not by a software limit | per second |
| **Hub REST** | 600 RPM | per minute |
| **Hub Git** | 60 pushes / 600 pulls per hour | per hour |
| **Hub S3** | bounded by S3 endpoint capacity | per second |

Three response headers carry your current state:

- `x-ratelimit-limit` — the maximum for the window.
- `x-ratelimit-remaining` — what you have left.
- `x-ratelimit-reset` — Unix timestamp when the window resets.

When you cross a limit, the response is `429` with `Retry-After` (in seconds). Respecting `Retry-After` is the entire contract — don't tight-loop on `429`.

## Quotas

Distinct from rate limits — quotas are longer-term ceilings.

| Resource | Default quota | Window |
|---|---|---|
| LFS storage per org | 10 TB | n/a |
| Inference tokens (proxied) | configured per org | monthly |
| Compute spend per backend | bounded by your Compute Policy, not a Surogate quota | configurable |
| Concurrent training runs | 5 per project | n/a |

Quota-exhausted responses come back as `403` with `type: quota_exhausted` and a `details.resource` field naming what ran out.

## Debugging a failure

When something fails unexpectedly:

1. **Capture the `request_id`** from the error body or the `x-request-id` response header.
2. **Read the `type` field** — that's what tells you what to do.
3. **Check the per-resource status** in Studio. Inference failures often correlate with the model being in **Error** or **Stopped**; Hub failures correlate with quota.
4. **Search the Operate → Sessions** view by `request_id` for agent calls — the full server-side trace lives there.
5. **Quote the `request_id`** when asking for help.

## Where to go next

- **[API overview](./overview.md)** — base URL, auth, request shape.
- **[Inference API](./inference.md)** — the endpoint reference.
- **[Hub API](./hub.md)** — Git / S3 / REST surfaces.
- **[Reference → Error messages](../reference/errors.md)** — UI-side error reference.

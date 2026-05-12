---
title: Error messages
sidebar_position: 3
slug: /reference/errors
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Error messages

A catalogue of error and notice messages observed in the UI or thrown by the API. Where the symptom is non-obvious, the most likely cause is listed first.

## Sign-in errors

| Message | HTTP | Likely cause | Fix |
|---|---|---|---|
| Please enter both username/email and password | — | Empty field on submit. | Fill both. |
| Wrong password. | 401 | The user exists but the password didn't match. | Re-type or reset. |
| No account exists with this email. | 404 / form | Email isn't registered. | Sign up, or use a different email. |
| No account exists with this username. | 404 / form | Username isn't registered. | Check the spelling or use email instead. |
| Check your email and verify the account, then sign in again. | — | Firebase sign-up completed but email not verified. | Click the link in your inbox. |
| Enter your email address above to reset your password. | — | Forgot-password requires an email, not a username. | Re-enter as email. |
| Enter a valid email address to reset your password. | — | The text doesn't look like an email. | Re-enter. |
| If an account exists for that email, a password reset link is on its way. | — | Forgot-password success notice. | Wait for the email. |
| Auth failed. | — | Generic fallback for unexpected sign-in errors. | Retry; if persistent, report. |
| Firebase login did not return Surogate tokens. | — | Server-side mismatch — Firebase verified but Surogate session creation failed. | Retry. If persistent, this is a server bug — report. |

## API auth errors (Authorization: Bearer ...)

| `detail` | HTTP | Cause |
|---|---|---|
| Invalid token payload | 401 | JWT had no `sub`, or the `sub` doesn't match the encoded payload. |
| Invalid or expired token | 401 | Signature failed or token expired (60-minute access TTL). Refresh via `/api/auth/refresh`. |
| User not found | 401 | The `sub` is a stale username that no longer exists. |
| Invalid API key | 401 | `sk-agent-...` couldn't be verified against the api_keys table. |
| API key not scoped for this model | 403 | The key exists but isn't scoped to the model being called. Create a new key on that model. |
| Password change required | 403 | `must_change_password` is set on your account. Complete `/change-password` first. |

## Page-level empty / error states

| Page | Empty state text | What to do |
|---|---|---|
| `/studio/agents` | **No agents** | Click **Deploy Agent**. |
| `/studio/models` | **No models** | Click **Deploy Model**. |
| `/studio/skills` | **No skills** | Click **New Skill** or **Import skill**. |
| `/studio/knowledge-bases` | **No knowledge** | Click **+ New Knowledge Base**. |
| `/studio/playground` | **No models** | Deploy a model first. |
| `/studio/sessions` | **No agents** | Deploy at least one agent. |
| Knowledge Base in **Error** state | (open the KB) | Inspect per-document errors; usually a source-fetch failure. |
| Model in **Error** state | (open the model) | Check the deploy logs in **Compute → Workload Queue**. |
| Agent in **Error** state | (open the agent) | Underlying Model or Skill is unhealthy. |

## Monitoring alert categories

Filterable from `/studio/monitoring`:

- **5xx** — the agent's serving endpoint returned a server error.
- **Timeout** — the agent didn't respond before the proxy timeout.
- **Guardrail** — a policy violation (compute policy or content guardrail) blocked or modified a response.

## Network / WebSocket

The app keeps a **monitor socket** open (see `useMonitorSocket` in `__root.tsx`). Symptoms of a dropped socket:

- Live counters on `/studio/monitoring` stop updating.
- Newly running jobs don't appear on `/studio/compute/workload-queue` until you refresh.

Fix: reload the page.

## Related

- [Sign in](../getting-started/sign-in)
- [Monitoring](../features/monitoring)
- [Troubleshooting](../troubleshooting)

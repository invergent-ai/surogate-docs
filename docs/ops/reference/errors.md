---
title: Error messages
sidebar_position: 2
slug: /reference/errors
---

# Error messages

A catalogue of error and notice messages, by where you see them.

## Sign-in

| Message | Cause | Fix |
|---|---|---|
| Wrong password. | User exists, password didn't match | Re-type, or reset. |
| No account exists with this email. | Email not registered | Sign up, or use a different email. |
| No account exists with this username. | Username not registered | Check spelling, or use email. |
| Check your email and verify the account, then sign in again. | Firebase signup completed but email unverified | Click the link in your inbox. |
| Enter your email address above to reset your password. | Forgot-password requires an email | Re-enter as email. |
| If an account exists for that email, a password reset link is on its way. | Forgot-password success notice | Wait for the email. |

## API auth (Bearer ...)

| `detail` | HTTP | Cause |
|---|---|---|
| Invalid token payload | 401 | JWT has no `sub` or doesn't match. |
| Invalid or expired token | 401 | Signature failed or token expired (60-min access TTL). Refresh via `/api/auth/refresh`. |
| User not found | 401 | The `sub` is a stale username. |
| Invalid API key | 401 | Surogate Ops couldn't verify the API key. |
| API key not scoped for this model | 403 | The key was created for a different model. Create a new key on this model. |
| Password change required | 403 | Your account is on a temporary password. Complete the password-change flow first. |

## Empty / error states by page

| Where | What you see | What to do |
|---|---|---|
| Agents list with no agents | **No agents** | Click **Deploy Agent**. |
| Models list with no models | **No models** | Click **Deploy Model**. |
| Skills list with no skills | **No skills** | Click **New Skill** or **Import skill**. |
| KBs list with no KBs | **No knowledge** | Click **+ New Knowledge Base**. |
| Playground with no models | **No models** | Deploy a model first. |
| Sessions with no agents | **No agents** | Deploy at least one agent. |
| KB in **Error** | Per-document errors visible on KB open | Most often a source fetch failed; re-enter the credential. |
| Model in **Error** | (open the model) | Check `serving` workload logs in Compute → Workload Queue. |
| Agent in **Error** | (open the agent) | Underlying Model or Skill is unhealthy. |

## Monitoring alert categories

- **5xx** — agent's serving endpoint returned an HTTP 500-series error.
- **Timeout** — agent didn't respond before the proxy timeout. Open the session trajectory to find the slow step.
- **Guardrail** — either a compute policy refused the workload, or a content guardrail intervened.

## WebSocket / live updates

Live counters on Monitoring or the Workload Queue stopping mid-session means the WebSocket dropped. Reload the tab.

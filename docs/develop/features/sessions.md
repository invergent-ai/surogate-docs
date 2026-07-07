---
title: Sessions
sidebar_position: 2
---

# Sessions

Every conversation is a session, fully recorded and inspectable. This chapter is about reading and using session data deliberately — what to look at, what to filter on, what to extract for training and evaluation.

For the operator's lighter walk-through, see [Work mode → Review what your agent did](/work/workflow/review-sessions).

## The six detail tabs

| Tab | Use it for |
|---|---|
| **THREAD** | The conversation as the user saw it. Markdown renders; artifacts display inline; files are downloadable. |
| **EVENTS** | Full ordered log of every event — user messages, LLM responses, tool calls, governance decisions. Your primary debugging surface. |
| **TOOLS** | Filtered to `tool.call` + `tool.result`. Fastest way to answer "what did the agent actually do?" |
| **SKILLS** | Which skills loaded into context, which the LLM invoked. Drift between the two is a signal: the skill loaded but didn't fire = `trigger` keywords don't match, or `description` is wrong. |
| **POLICIES** | Governance decisions — denied / escalated / allowed. Includes prompt-injection-guard hits. |
| **METADATA** | Counters (turns, tokens, cost, duration), the 7 quality flags, the agent's frozen config snapshot at session start. |

The Sessions list page has filters for: agent, status (Active / Completed / Failed / Archived), and chips for each quality flag (Denied, Overridden, Crashed, 👍, 👎). Filters compose into URL params, so you can bookmark a filtered view.

## The 7 quality flags

These flip when corresponding events fire during the session:

| Flag | Set by |
|---|---|
| 👍 / 👎 | User feedback in the THREAD view |
| `policy.denied` | Governance gate blocked a tool call |
| `harness.crash` | The agent's runtime crashed mid-session (rare) |
| `saga.compensated` | A multi-step rollback fired |
| `expert.override` | Base LLM rejected an expert's answer |
| `expert.endorse` | Base LLM accepted an expert's answer |

Use them to slice traffic. Combine on the Sessions list — "sessions in the last 7 days where saga compensated AND the user thumb-downed."

## Reading the EVENTS log

Each row is a typed event with a JSON payload. For the canonical list of event types and what their payloads contain, see [Event types](../reference/event-types.md).

Failure-mode triage:

- **Agent didn't search the KB** → SKILLS tab confirms the relevant skill loaded; if it did, check whether the `trigger` keywords match the user's phrasing.
- **Agent searched but got bad results** → TOOLS tab, expand `tool.result` for `kb_search`. Often the KB content is the problem, not the agent.
- **Agent looped** → check iteration count in METADATA; the last few `llm.response` events usually reveal the repetition pattern.
- **Tool was blocked** → POLICIES tab; the denial reason is recorded.
- **Saga rolled back** → look at `saga.step_failed` (the trigger) and the `saga.compensate` events that followed.

## Export

| Destination | Where |
|---|---|
| **Copy session URL** | Shareable within your tenant |
| **Export events JSON** | Full event log as a `.json` file. Used for audits or offline analysis. |
| **Add to dataset** | Captures the session into a versioned dataset. Used to build training corpora — see [Datasets](./datasets.md). |

## Per-channel sessions

Channel determines who can see / interact with the session:

| Channel | Session boundary |
|---|---|
| **Web** | Each "New chat" click. End user owns it. |
| **Slack DM** | One DM thread = one session. |
| **Slack channel** | Each `@mention` starts a thread-scoped session. |
| **Telegram** | DM thread or forum topic. |
| **Website widget** | One per visitor browser session (resumed via localStorage). Capped by `Session Message Cap` if set. |
| **API channel** | Each `POST /v1/api/prompts` = one session. No SSE — clients poll. |

## API channel sessions are different

They have `channel="api"`, no interactive user (service-account ownership), no inbox surface, and **no SSE streaming**. Pipelines poll for completion:

```python
import requests, time

resp = requests.post(
    "https://ops.surogate.ai/v1/api/prompts",
    headers={"Authorization": f"Bearer {sa_token}"},
    json={"agent_slug": "data-analyst", "prompt": "Analyse Q1.csv"},
)
session_id = resp.json()["session_id"]

while True:
    status = requests.get(
        f"https://ops.surogate.ai/v1/api/sessions/{session_id}",
        headers={"Authorization": f"Bearer {sa_token}"},
    ).json()["status"]
    if status in ("completed", "failed"):
        break
    time.sleep(5)

events = requests.get(
    f"https://ops.surogate.ai/v1/api/sessions/{session_id}/events",
    headers={"Authorization": f"Bearer {sa_token}"},
).json()
final = next(e for e in events if e["type"] == "assistant.final")
print(final["data"]["content"])
```

See [Use cases → API channel for batch jobs](../use-cases.md) for an end-to-end recipe.

## Sub-agent observability

A session can have children (via `spawn_worker` / `delegate_task` / `spawn_task`). The session detail shows:

- The **Running** panel in the sidebar — live sub-agent tree, auto-refreshes every 4s while children are active
- Per-child links — click to drill into the child's own session
- The parent's `delegation.*` events showing what each child did

`GET /api/sessions/{id}/tree` returns the full descendant graph (up to 200 nodes). Use it to build your own dashboards over sub-agent fan-out.

## Retention

Sessions are kept indefinitely by default — they're the source of truth for compliance and training-data extraction. To delete a specific one: METADATA tab → Delete (soft delete; the row stays for audit but disappears from default views).

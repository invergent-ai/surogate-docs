---
title: Sessions
sidebar_position: 2
---

# Sessions

Every conversation is a session. Sessions are the **source of truth** for what the agent did. This chapter is about reading sessions with intent.

## The data model

```
sessions (
  id UUID PRIMARY KEY,
  org_id UUID NOT NULL,
  user_id UUID,                    -- nullable for API channel
  agent_id UUID NOT NULL,
  channel TEXT NOT NULL,           -- web | slack | telegram | website | api | scheduled | worker | task
  parent_id UUID,                  -- for sub-agent/task children
  task_id UUID,                    -- for task-layer-backed sessions
  status session_status,           -- active | completed | failed | archived
  config JSONB,                    -- snapshot of agent config at session start
  cursor_event_id BIGINT,          -- last fully-processed event
  storage_bucket TEXT,
  workspace_path TEXT,
  created_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ
)

events (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL,
  org_id UUID NOT NULL,
  user_id UUID,
  type event_type NOT NULL,        -- ~50 enum values
  data JSONB NOT NULL,
  trace_id UUID, span_id UUID,
  created_at TIMESTAMPTZ
)
```

`org_id` and `user_id` on `events` are populated by an `events_populate_tenant` trigger from the session row — callers never set them. Lets tenant-scoped audit queries filter `events` directly without joining `sessions`.

`config` JSONB captures the agent's configuration at the moment the session started — frozen for the lifetime of the session. This is the **session-start freeze** that makes mid-session prompt injection unable to weaken governance.

## The session detail page

Six tabs:

| Tab | What it shows |
|---|---|
| **THREAD** | Clean chat view of user / assistant messages, inline artifacts, file references |
| **EVENTS** | Full ordered event log |
| **TOOLS** | Filtered events for `tool.call` + `tool.result` only |
| **SKILLS** | Which skills loaded, which the LLM actually invoked |
| **POLICIES** | Governance decisions (denied / escalated / allowed) |
| **METADATA** | Counters, quality flags, attached agent config |

## EVENTS in depth

The event types enum has ~50 values. The major groups:

| Group | Examples |
|---|---|
| Session lifecycle | `session.created`, `session.completed`, `session.failed`, `session.archived`, `session.reset` |
| User interaction | `user.message`, `user.define_outcome`, `clarify.response` |
| LLM | `llm.request`, `llm.response`, `llm.error` |
| Tool execution | `tool.call`, `tool.result`, `tool.error` |
| Assistant | `assistant.final` |
| Sub-agents | `worker.spawned`, `worker.complete`, `worker.failed`, `delegation.start`, `delegation.complete`, `delegation.failed`, `delegation.stale` |
| Tasks | `task.created`, `task.blocked`, `task.failed`, `task.completed`, `task.cancelled` |
| Governance | `policy.denied`, `policy.escalated`, `policy.allowed` |
| Saga | `saga.start`, `saga.step_begin`, `saga.step_committed`, `saga.step_failed`, `saga.compensate`, `saga.complete`, `saga.escalated` |
| Experts | `expert.delegation`, `expert.result`, `expert.override`, `expert.endorse` |
| Skills | `skill.invoked`, `skill.activated` |
| Memory | `memory.added`, `memory.replaced`, `memory.removed` |
| Browser | `browser.provisioned`, `browser.destroyed`, `browser.control_granted`, `browser.control_returned` |
| Outcomes (`/goal`) | `outcome.defined`, `outcome.continuation`, `outcome.paused`, `outcome.cleared`, `span.outcome_evaluation_*` |
| Inbox | `inbox.input_required`, `inbox.action_required`, `inbox.task_complete`, `inbox.governance_gate`, `inbox.progress_checkin` |
| Artifacts | `artifact.created` |
| Context | `context.compact` |
| Harness | `harness.crash`, `harness.recovered` |

Full event-type reference at [Event types](../reference/event-types.md).

## Reading the EVENTS log

Each row:

```
created_at         type                 data (JSONB)
12:43:01.234   user.message         { "content": "What's the refund policy?" }
12:43:01.567   llm.request          { "model": "...", "tokens_in": 1247 }
12:43:04.012   llm.response         { "content": "I'll check...", "tokens_out": 18 }
12:43:04.034   tool.call            { "name": "kb_search", "args": {"query": "refund policy"}, "tool_call_id": "tc_1" }
12:43:05.198   tool.result          { "tool_call_id": "tc_1", "content": "Refunds within 30 days..." }
12:43:06.401   llm.request          { "tokens_in": 1429 }
12:43:08.892   llm.response         { "content": "Our refund policy is...", "tokens_out": 146 }
12:43:08.892   assistant.final      { "content": "..." }
```

Click any row to expand the full JSONB payload.

## Filtering and search

Develop mode adds richer filters:

- **Per-agent picker** (left rail)
- **Status combobox** — All / Active / Completed / Failed / Archived
- **Filter chips** — Denied · Overridden · Crashed · 👍 · 👎
- **Search box** — title, ID, model

URL params persist filters: `/studio/sessions?agentId=<uuid>&status=failed&flag=denied`.

## Sub-agent observability

Sessions can have children (via `spawn_worker` / `delegate_task` / `spawn_task`). The session detail surfaces:

- **Sub-agent tree** in a "Running" panel — recursive children, refreshes every 4s while any child is active
- **Per-child links** — click any sub-agent to drill into its own session
- **Parent's `delegation.*` events** — child outcomes flow back as events in the parent's log

For the full sub-agent / task / mission model, see [the surogates runtime docs](https://github.com/invergent-ai/surogates/blob/main/docs/sub-agents/index.md) and [Reference → Runtime architecture](../reference/runtime-architecture.md).

## Replay

The Replay button forks a session: creates a new session with the same starting conditions, replays user messages one by one, and stops at the first divergence. Use for regression testing after agent config changes.

Programmatic: `POST /v1/sessions/{id}/replay` with optional config override. Returns a new session_id.

## Export

Three options from METADATA:

| Action | What it does |
|---|---|
| **Copy session URL** | Shareable link within your tenant |
| **Export events JSON** | Full event log as a `.json` file. Used for audit / compliance. |
| **Add to dataset** | Adds this session's transcript to a dataset you can use for training or evaluation |

## SQL views — the audit substrate

Three views over `events` projected for analysis:

### `v_session_tree`

Recursive parent/child relationships. Powers `GET /v1/sessions/{id}/tree` and the Running panel.

```sql
SELECT * FROM v_session_tree
WHERE root_id = $1
ORDER BY depth, id
LIMIT 200;
```

### `v_skill_trajectories`

Successful trajectories where a `/skill` command was used. Filters out tainted sessions (`policy.denied`, `harness.crash`, `saga.compensated`, `expert.override`). Powers `collect_for_skill` bootstrap training.

### `v_expert_outcomes`

Expert delegations with success flag (no subsequent override). Powers `collect_for_expert` improve training.

```sql
SELECT date_trunc('day', created_at) AS day,
       expert_name,
       count(*) FILTER (WHERE success) AS successes,
       count(*) AS total,
       count(*) FILTER (WHERE success)::float / count(*) AS rate
FROM v_expert_outcomes
WHERE org_id = $1
GROUP BY day, expert_name
ORDER BY day DESC, rate ASC;
```

See [Event types reference](../reference/event-types.md) for full schemas.

## API channel sessions

API-channel sessions have `channel = 'api'` and `user_id = NULL` (no interactive user). They:

- Use the org's org-wide memory (no per-user)
- Have no inbox (service-account sessions don't push to an inbox)
- Are pulled by clients from the events table — no SSE streaming
- Last until `status='completed'` (which the harness sets when `assistant.final` is the final event)

Pattern for a polling client:

```python
import requests
from time import sleep

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
    sleep(5)

events = requests.get(
    f"https://ops.surogate.ai/v1/api/sessions/{session_id}/events",
    headers={"Authorization": f"Bearer {sa_token}"},
).json()
final = next(e for e in events if e["type"] == "assistant.final")
print(final["data"]["content"])
```

## What's next

[Compute](./compute.md) for the deployment surface, [Skills & Experts](./skills-and-experts.md) for what you attach.

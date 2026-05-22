---
title: Event types
sidebar_position: 3
---

# Event types

The Sessions UI's EVENTS tab and the `GET /v1/sessions/{id}/events` API both return a stream of typed events. This page lists what you'll see and what each event tells you.

## Conversation events

| Type | When | What's useful |
|---|---|---|
| `user.message` | A user sent input | `content`, `source` (web / slack / api / scheduled / …) |
| `assistant.final` | The agent produced a final user-visible response | `content` |
| `llm.request` / `llm.response` | A single LLM call (the agent may make many per turn) | `model`, `tokens_in`, `tokens_out` |
| `clarify.response` | The user answered a `clarify` widget | `tool_call_id`, `responses` |

## Tool execution

| Type | Payload |
|---|---|
| `tool.call` | `name`, `args`, `tool_call_id` |
| `tool.result` | `tool_call_id`, `content`, `duration_seconds`, `status` |
| `tool.error` | `tool_call_id`, `error` |

For most debugging, the EVENTS tab's TOOLS sub-view filters these for you. Programmatically, `GET /v1/sessions/{id}/events?type=tool.call` is the API equivalent.

## Sub-agent / task events

When a session spawns child sessions via `spawn_worker` / `delegate_task` / `spawn_task`, the children's outcomes flow back as events in the parent's log.

| Type | When |
|---|---|
| `worker.spawned` | A child session was created |
| `worker.complete` | Child finished normally; payload includes the truncated result and optional `metadata` |
| `worker.failed` | Child errored or hit its iteration budget |
| `delegation.start` / `delegation.complete` / `delegation.failed` / `delegation.stale` | Detailed observability for `delegate_task` calls |
| `task.blocked` | A task self-paused via `task_block` |
| `task.failed` | A task exhausted its retry budget |

## Governance

| Type | When |
|---|---|
| `policy.denied` | A tool call was blocked by the governance gate. Payload: `tool_name`, `reason`, `args_excerpt` |
| `policy.escalated` | Denied but user-overridable — an inbox `governance_gate` item was raised |

## Saga (multi-step rollback)

When the agent's CONFIG has Saga enabled:

| Type | When |
|---|---|
| `saga.start` | Saga activated at session start |
| `saga.step_begin` / `saga.step_committed` / `saga.step_failed` | Per-step tracking |
| `saga.compensate` | A rollback fired |
| `saga.complete` | Saga finished |
| `saga.escalated` | A compensation step itself failed — operator must intervene |

## Experts

| Type | When |
|---|---|
| `expert.delegation` | Base LLM called `consult_expert` |
| `expert.result` | The expert returned |
| `expert.override` | Base LLM rejected the expert's output (counts against expert success rate) |
| `expert.endorse` | Base LLM used the expert's output verbatim |

## Outcomes (`/goal`)

| Type | When |
|---|---|
| `outcome.defined` | A goal was set on the session |
| `span.outcome_evaluation_end` | The evaluator returned a verdict (`satisfied`, `needs_revision`, `blocked`, `failed`) |
| `outcome.continuation` | A continuation message was queued |

## Inbox

The agent raised something to the user:

| Type | What it surfaces |
|---|---|
| `inbox.input_required` | A `clarify` widget |
| `inbox.action_required` | An external action needed (browser login, MFA, etc.) |
| `inbox.task_complete` | An informational completion |
| `inbox.governance_gate` | A user-overridable policy denial |
| `inbox.progress_checkin` | A long-running-session status update |

## Lifecycle

| Type | When |
|---|---|
| `session.created` / `session.completed` / `session.failed` / `session.archived` | Session-level transitions |
| `session.reset` | The idle-session-reset background job tore down the sandbox (memory was flushed to MEMORY.md/USER.md first) |
| `harness.crash` / `harness.recovered` | Rare — a runtime crash and the subsequent automatic recovery |
| `context.compact` | The session's context window was compressed automatically |
| `artifact.created` | A `create_artifact` call produced an inline chat artifact |

## Querying via the API

```bash
# All events for a session
GET /v1/sessions/{id}/events

# Filter by type
GET /v1/sessions/{id}/events?type=policy.denied

# Stream live (SSE)
GET /v1/sessions/{id}/events?after=<last_id>
```

See the API reference for full schemas. For Slack and Telegram channel sessions, the same events stream is available — channel adapters just translate the user-visible portion into the channel's native format.

## Stability

Event type names and their documented payload keys are a stable contract. **Adding new keys is safe**; renaming or removing requires a deprecation cycle. If you're querying programmatically, prefer reading specific keys (`event.data.tool_name`) over depending on the full payload shape.

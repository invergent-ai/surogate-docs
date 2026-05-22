---
title: Event types
sidebar_position: 3
---

# Event types

The `events` table's `type` column is an enum with ~50 values. Reference for what each event means and what's in its `data` JSONB.

For the table schema, see [Runtime architecture](./runtime-architecture.md).

## Session lifecycle

| Type | When emitted | Payload |
|---|---|---|
| `session.created` | New session row written | `{agent_id, channel, parent_id?}` |
| `session.completed` | Harness emitted `assistant.final` and exits cleanly | `{tokens_in, tokens_out, duration_seconds}` |
| `session.failed` | Harness or sandbox failed beyond recovery | `{reason}` |
| `session.archived` | Session retention policy archived it | `{}` |
| `session.reset` | Idle-session reset job tore down the sandbox | `{memory_flushed: bool}` |

## User interaction

| Type | When | Payload |
|---|---|---|
| `user.message` | User sends a message | `{content, source?, channel?}` |
| `user.define_outcome` | `/goal` set on the session | `{description, rubric?, max_iterations?}` |
| `clarify.response` | User submitted answers to a clarify widget | `{tool_call_id, responses: [{question_index, answer, is_other}]}` |

## LLM

| Type | When | Payload |
|---|---|---|
| `llm.request` | Outbound LLM call | `{model, tokens_in, request_id, ...}` |
| `llm.response` | Successful response | `{content, tokens_out, finish_reason}` |
| `llm.error` | LLM call failed | `{model, error}` |

## Tool execution

| Type | When | Payload |
|---|---|---|
| `tool.call` | LLM requested a tool call | `{name, args, tool_call_id}` |
| `tool.result` | Tool returned | `{tool_call_id, content, duration_seconds, status}` |
| `tool.error` | Tool errored | `{tool_call_id, error}` |

## Assistant

| Type | When | Payload |
|---|---|---|
| `assistant.final` | LLM produced a final response (no tool calls) | `{content}` |

## Sub-agents

| Type | When | Payload |
|---|---|---|
| `worker.spawned` | A child session was created | `{worker_id, goal, agent_type, role, depth}` |
| `worker.complete` | Child session finished normally | `{worker_id, result, task_id?, metadata?}` (truncated to 10 KB) |
| `worker.failed` | Child session raised | `{worker_id, error}` |
| `delegation.start` | `delegate_task` started polling for the child | `{child_session_id, goal, role, depth, agent_type, model}` |
| `delegation.complete` | Child finished successfully | `{child_session_id, goal, duration_seconds, tool_call_count, trace, files_written, files_read}` |
| `delegation.failed` | Child failed | `{child_session_id, goal, reason, duration_seconds}` |
| `delegation.stale` | Child stopped emitting events for longer than threshold | `{child_session_id, idle_seconds, in_tool, threshold_seconds}` |

## Tasks

| Type | When | Payload |
|---|---|---|
| `task.created` | `spawn_task` created a row | `{task_id, goal, parents?, max_attempts}` |
| `task.blocked` | Worker called `task_block` | `{task_id, worker_id, reason}` |
| `task.failed` | Tick observed crash after max_attempts | `{task_id, worker_id, attempt_count}` |
| `task.completed` | Tick saw `WORKER_COMPLETE` | `{task_id, summary, metadata?}` |
| `task.cancelled` | `cancel_task` called | `{task_id, reason}` |

## Governance

| Type | When | Payload |
|---|---|---|
| `policy.denied` | Governance gate blocked a tool call | `{tool_name, reason, args_excerpt}` |
| `policy.escalated` | Gate flagged for user override | `{tool_name, reason, inbox_item_id}` |
| `policy.allowed` | (Rare) explicit ABAC allow log | `{tool_name, rule}` |

## Saga

| Type | When | Payload |
|---|---|---|
| `saga.start` | Saga created at session start | `{}` |
| `saga.step_begin` | Tool call registered as a saga step | `{step_id, tool_name, args_excerpt}` |
| `saga.step_committed` | Step completed successfully | `{step_id, duration_seconds}` |
| `saga.step_failed` | Step failed | `{step_id, error}` |
| `saga.compensate` | Rollback triggered | `{step_id, undo_tool, reason}` |
| `saga.complete` | Saga finished (normally or after compensation) | `{steps_committed, steps_compensated}` |
| `saga.escalated` | Compensation itself failed | `{step_id, error}` |

## Experts

| Type | When | Payload |
|---|---|---|
| `expert.delegation` | Base LLM called `consult_expert` | `{expert_name, task, context?}` |
| `expert.result` | Expert returned | `{expert_name, content}` |
| `expert.override` | Base LLM rejected the expert's output | `{expert_name, reason}` |
| `expert.endorse` | Base LLM used the expert's output verbatim | `{expert_name}` |

## Skills

| Type | When | Payload |
|---|---|---|
| `skill.invoked` | `/<skill>` typed or matched by LLM | `{skill_name, source: "user_command" \| "llm_match"}` |
| `skill.activated` | Skill loaded into session context | `{skill_name, version}` |

## Memory

| Type | When | Payload |
|---|---|---|
| `memory.added` | Entry added to MEMORY.md or USER.md | `{target, text, section_id}` |
| `memory.replaced` | Entry replaced | `{target, old_text, new_text, section_id}` |
| `memory.removed` | Entry removed | `{target, old_text, section_id}` |

## Browser

| Type | When | Payload |
|---|---|---|
| `browser.provisioned` | Browser pod created | `{pod_name, live_view_url}` |
| `browser.destroyed` | Browser pod torn down | `{pod_name}` |
| `browser.control_granted` | User took control of the live browser | `{user_id}` |
| `browser.control_returned` | User released control | `{user_id}` |

## Outcomes (`/goal`)

| Type | When | Payload |
|---|---|---|
| `outcome.defined` | `/goal` or `user.define_outcome` set on session | `{description, rubric?, max_iterations}` |
| `span.outcome_evaluation_start` | Evaluator started grading a final response | `{}` |
| `span.outcome_evaluation_ongoing` | Evaluator is active | `{}` |
| `span.outcome_evaluation_end` | Evaluator returned a verdict | `{verdict: "satisfied"\|"needs_revision"\|"blocked"\|"failed", feedback?}` |
| `outcome.continuation` | Continuation message queued | `{iteration}` |
| `outcome.paused` | User paused or evaluator parse failures | `{reason}` |
| `outcome.cleared` | `/goal clear` | `{}` |

## Inbox

| Type | When | Payload |
|---|---|---|
| `inbox.input_required` | `clarify` tool called | `{questions, tool_call_id}` |
| `inbox.action_required` | Agent needs external user action | `{action_type, target, instructions, context?}` |
| `inbox.task_complete` | Long-running session done | `{summary, outcome, duration_seconds, error?}` |
| `inbox.governance_gate` | Policy denied + user-overridable | `{tool_name, tool_call_id, reason, args_excerpt}` |
| `inbox.progress_checkin` | Long-running session update | `{iteration, elapsed_seconds, last_tool, summary}` |

## Artifacts

| Type | When | Payload |
|---|---|---|
| `artifact.created` | `create_artifact` called | `{artifact_id, kind, name, version, size_bytes}` |

## Context

| Type | When | Payload |
|---|---|---|
| `context.compact` | Context window compressed | `{messages_before, messages_after, summary}` |

## Harness

| Type | When | Payload |
|---|---|---|
| `harness.crash` | Worker died mid-session | `{worker_id, error?}` |
| `harness.recovered` | New worker picked up the session | `{new_worker_id}` |

## Querying patterns

### Per-tool latency

```sql
SELECT
  data->>'name' AS tool,
  count(*),
  avg((data->>'duration_seconds')::float) AS avg_latency
FROM events
WHERE type = 'tool.result'
  AND org_id = $1
  AND created_at > now() - interval '7 days'
GROUP BY tool
ORDER BY avg_latency DESC;
```

### Saga compensation rate

```sql
SELECT date_trunc('day', created_at) AS day,
       count(*) FILTER (WHERE type = 'saga.compensate') AS compensations,
       count(DISTINCT session_id) FILTER (WHERE type = 'saga.compensate') AS sessions_with_rollback
FROM events
WHERE org_id = $1
GROUP BY day
ORDER BY day DESC;
```

### Top denied tools

```sql
SELECT
  data->>'tool_name' AS tool,
  count(*) AS denials,
  array_agg(DISTINCT data->>'reason') AS reasons
FROM events
WHERE type = 'policy.denied'
  AND org_id = $1
  AND created_at > now() - interval '30 days'
GROUP BY tool
ORDER BY denials DESC
LIMIT 20;
```

## What's next

[Glossary](./glossary.md) for terminology. [Runtime architecture](./runtime-architecture.md) for the big picture.

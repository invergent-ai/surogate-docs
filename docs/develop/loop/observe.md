---
title: Observe phase
sidebar_position: 3
---

# Observe phase — what the agent actually does

The Sessions surface is your source of truth. Every conversation, tool call, LLM response, governance decision is in the event log forever. This chapter is about reading that data with intent.

## The events table

Behind the UI is a PostgreSQL table:

```sql
events (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL,
  org_id UUID NOT NULL,            -- populated by trigger
  user_id UUID,                    -- nullable for API channel
  type event_type NOT NULL,        -- enum: ~50 types
  data JSONB NOT NULL,
  trace_id UUID, span_id UUID,     -- OpenTelemetry correlation
  created_at TIMESTAMPTZ
)
```

This is the audit log. Every action the agent took, the user took, or the governance gate made is here. See [Event types reference](../reference/event-types.md) for the full enum.

## Reading a session

The session detail page in Develop mode has the same 6 tabs as Work mode (THREAD, EVENTS, TOOLS, SKILLS, POLICIES, METADATA) but you'll spend more time in EVENTS than the operator does.

### What to look for, by failure mode

| Symptom | Likely cause | Where to look in EVENTS |
|---|---|---|
| Agent didn't call a tool you expected | Skill didn't trigger | SKILLS tab — did the skill load? If yes, why didn't the LLM use it? Tighten triggers or descriptions. |
| Agent called the right tool but got junk | Tool implementation issue | TOOLS tab — inspect args + result. Is the args JSON well-formed? Is the result what you expected? |
| Agent crashed | Runtime issue | `harness.crash` event near the end. Check Compute dashboard for pod health. |
| Tool was denied | Governance | POLICIES tab — `policy.denied` events with reason. Probably the allowlist needs updating, or the agent tried something it shouldn't have. |
| Agent looped indefinitely | Bad LLM, missing tool, or bad prompt | Iteration count in METADATA. If maxed out, check the last few LLM responses for repetition. |
| Tool result was wrong | KB / MCP / external integration issue | `tool.call` then `tool.result` — inspect the result data |
| Saga rolled back the work | Multi-step failure | `saga.compensate` event with reason. Check the failing `saga.step_failed` upstream. |

## Quality flags

Seven flags per session that you can filter on:

| Flag | Meaning | When set |
|---|---|---|
| `thumbs_up` | User clicked 👍 | Manual feedback |
| `thumbs_down` | User clicked 👎 | Manual feedback |
| `policy.denied` | Governance blocked a tool call | When the policy engine returns `deny` |
| `harness.crash` | The runtime crashed mid-session | Worker pod death + recovery |
| `saga.compensated` | A multi-step rollback fired | When a saga step failed and prior steps rolled back |
| `expert.override` | Base LLM rejected an expert's answer | When the base LLM decides to redo expert work |
| `expert.endorse` | Base LLM accepted an expert's answer | When the base LLM uses expert output verbatim |

Use these flags to **slice your traffic**. Examples:

- All sessions where saga rolled back in the last 7 days → systemic multi-step failures
- All sessions where expert was overridden → expert needs retraining
- All sessions thumb-downed with `policy.denied` → governance is too tight OR the agent is trying things it shouldn't

## Sessions list — filters and search

In Develop mode the Sessions surface adds:

- **Per-agent picker** — left rail. Filter to one agent.
- **Status combobox** — All / Active / Completed / Failed / Archived
- **Filter chips** — Denied · Overridden · Crashed · 👍 · 👎
- **Search box** — title, ID, model

For SQL-level queries you'd use the platform's REST API or read directly from the events table (admin access required). See [REST API for sessions](../reference/runtime-architecture.md) and the SQL views in the [event types reference](../reference/event-types.md).

## SQL views for analysis

The platform ships three views over the events table, designed for analysis:

| View | What it projects | Powers |
|---|---|---|
| `v_session_tree` | Recursive parent/child relationships for sub-agent sessions | `GET /v1/sessions/{id}/tree`, the "Running" sidebar |
| `v_skill_trajectories` | Successful trajectories where a `/skill` command was used | Bootstrap expert training data (collect_for_skill) |
| `v_expert_outcomes` | Expert delegations and whether the base LLM endorsed them | Improve expert training data (collect_for_expert) |

You can query these views directly (or via the platform's API) for:

- Per-day expert success rates
- Skill invocation frequency
- Per-agent error rate breakdown
- Sub-agent fan-out patterns

See [Event types reference](../reference/event-types.md) for view schemas.

## Replay

The THREAD view's **Replay** button is more powerful in Develop mode than in Work — it's effectively a regression test. After a config change, replay your worst sessions against the new agent and look at the diff.

Pattern: keep a "regression set" of 10-50 thumb-downed sessions. Before any major change, replay all of them. If the diff is favourable, ship the change. If not, iterate.

For automation, the same mechanism is available via REST: `POST /v1/sessions/{id}/replay` with a config override. The result is a new session you can compare programmatically.

## Build a dataset from sessions

When you have signal you want to use:

1. Sessions list → filter by quality flags → see your candidate set.
2. Datasets → **NEW DATASET** → source type **"From Conversations"** → set filters (agent_id, time range, quality flags).
3. The dataset row appears in the Hub as a versioned repo.

This is one input to expert training. See [Train phase](./train.md).

## What's next

[Train phase](./train.md) — using observed signal to make a better agent.

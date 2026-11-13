---
title: Background jobs
---

Work that outlives a single agent turn — sub-agents running in the background, scheduled runs, and the platform sweepers that keep everything tidy.

There are two families: **agent-initiated background work** (a running agent hands work to children or the future) and **platform maintenance jobs** (periodic sweepers the runtime schedules itself).

## Agent-initiated background work

An agent starts and follows sub-agents with one family of tools:

| Tool | What it does |
|---|---|
| `agent` | Starts one sub-agent from a short `description` and a `prompt` that stands alone, optionally of a pre-configured `agent_type`. |
| `send_message` | Sends a running or finished agent a follow-up: what it should do next, a correction, or an answer to its question. |
| `list_agents` | Lists the agents the session started, or reads one. |
| `stop_agent` | Stops an agent, with the agents it started, or a background command. |
| `monitor` | Runs a command and turns each line it prints into a notification. |

Every sub-agent is a full child session with its own event log and iteration budget, on the `delegation` channel. It shares the parent's workspace: every child session inherits the parent's `storage_bucket`, `storage_key_prefix` and `workspace_path` and resolves to the sandbox of the tree's root, so no `sessions/{child_id}/` prefix is allocated and the whole fan-out reads and writes one `/workspace`. Siblings can overwrite each other's files. See [Runtime architecture](/develop/reference/runtime-architecture/).

### In the background, or in the foreground

- **Background** (the default for a main session): `agent` returns `{"agent_id", "status": "running"}` at once. When the agent ends, an `agent.notification` event is written into the **parent's** event log and the parent is re-enqueued; it reads the report as a notification at its next model request. At most 5 of a session's agents run in the background at a time.
- **Foreground** (`run_in_background=false`, and always for a sub-agent's own agents): the call waits for the report and returns it as its result, for up to 60 minutes. The parent's log gets `delegation.start` and `delegation.complete` or `delegation.failed`, and a one-shot `delegation.stale` if the child goes quiet past a threshold.

Several `agent` calls in one response run in parallel (at most 5 calls a response; any more are dropped, except in a project's coordinator, whose every call starts one thread). Depth is capped at 2 levels: a sub-agent below the limit may start agents of its own, one at the limit may not. A child inherits the parent's `excluded_tools`, and `ask_user_question` is stripped from every child: a child has no path to the user, and asks its parent with `send_message` instead. Artifacts a child creates are propagated up to the parent's chat thread automatically.

### Following up and stopping

`send_message` reaches an agent the caller started, its parent (`to: "parent"`), or a sibling, in the same organisation only. A running agent reads it before its next step; a finished one is resumed with its whole context and the message, and its new report arrives as another notification. `stop_agent` stops an agent and the agents under it; a stopped agent keeps its context, and a message from the agent that stopped it resumes it.

### How results and progress are tracked

- **Events** — outcomes flow back as `delegation.*` and `agent.notification` events on the parent's log. See [Event types → Sub-agent events](/develop/reference/event-types/).
- **Live tree** — a session's detail view shows a Running panel and per-child links; `GET /v1/sessions/{id}/tree` returns the descendant graph. See [Sessions → Sub-agent observability](/develop/features/sessions/).
- **The board** — a fan-out of agents shares a coordination board so siblings reuse each other's findings without routing through the parent. See [Coordination & the board](/develop/reference/coordination/).

## Scheduled sessions and loops

Agents can schedule work for the future. Scheduled prompts are user-owned rows in the database; the platform's scheduled-work ticker (a single leader-elected process across replicas) polls due rows, creates a fresh `channel="scheduled"` session, emits the stored prompt, and enqueues it.

| Tool / command | Effect |
|---|---|
| `cron_create` | Schedule a user-owned prompt or slash command on a 5-field cron cadence (or one-shot) |
| `cron_list` / `cron_delete` | List and remove schedules |
| `/loop [interval] <prompt>` | Create a recurring loop. Fixed-interval loops expire after 3 days |
| `loop_complete` | End a fixed-interval loop early from inside a run, once its stop condition is met |
| `loop_wait` | (Dynamic loops, when no interval is given) choose the next delay, clamped to 1 minute–1 hour; the loop expires after 7 days. Pass `completed: true` to end it |

### Result delivery

Each run executes on its own child session, and its output is surfaced back to the conversation that created it:

- **Channel-origin loops** (Slack, Telegram, Teams) — a run's deliverables resolve to the parent session's channel and routing, so every run posts back into the origin channel.
- **Web / API-origin loops** — a run's final answer is emitted as a `loop.result` event on the parent session and appears inline in the originating conversation (web clients over SSE, API clients by polling `GET /sessions/{id}/events`). A `loop.result` never re-enters the parent agent's context or re-wakes it; a run with no text output delivers nothing.

An expired loop that never fired again is swept to `completed` by the ticker's periodic recovery pass, so it never lingers as a due-but-idle row.

## Platform maintenance jobs

The runtime schedules several sweepers (as Kubernetes CronJobs or long-running loop processes). They are idempotent and operator-invisible in normal operation.

| Job | Cadence | What it does |
|---|---|---|
| Board maintenance | ~5 min | Expires lapsed board claims and purges old/orphaned notes. See [Coordination & the board](/develop/reference/coordination/#lifecycle) |
| Inbox expiry | ~5 min | Marks pending inbox items non-actionable once their owning session is terminal |
| Platform workspace cleanup | ~6 h | Iterates every agent and deletes orphaned session-workspace prefixes in object storage |
| Browser reaper | ~15 s | Probes each agent browser; two failed probes in a row prune it and emit `browser.destroyed`. Skips browsers under 30 s old; never destroys containers |
| Device transfers | ~5 min | Deletes device transfers nothing will read again, and a user's own computer requests once they have been closed for a while |
| Office saves | ~2 s | Lands saves from the document editor, and about once a minute closes editing sessions that were never opened or whose chats are gone. Runs only when the office feature is enabled |
| Training collector | on demand | Exports successful expert-delegation and skill-invocation trajectories from the event log as JSONL to the tenant bucket, for external fine-tuning |

The training collector's responsibility ends at the JSONL file — training strategy, evaluation, and model hosting are the organization's concern.

## Related

- [Coordination & the board](/develop/reference/coordination/) — how parallel background work coordinates.
- [Missions](/work/tools/missions/) — a coordinator that gives a goal out to agents, judged against a rubric.
- [Sessions](/develop/features/sessions/) — reading a session and its sub-agent tree.
- [Event types](/develop/reference/event-types/) — the events every background primitive emits.

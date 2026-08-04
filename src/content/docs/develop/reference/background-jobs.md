---
title: Background jobs
---

Work that outlives a single agent turn — asynchronous sub-agents, durable tasks, scheduled runs, and the platform sweepers that keep everything tidy.

There are two families: **agent-initiated background work** (a running agent hands work to children or the future) and **platform maintenance jobs** (periodic sweepers the runtime schedules itself).

## Agent-initiated background work

An agent has three primitives for offloading work, each with a different durability and result-delivery model.

| Primitive | Blocks the parent? | Survives crash / retries? | Best for |
|---|---|---|---|
| `spawn_worker` | No — returns a `worker_id` immediately | No — single attempt | Fire-and-forget parallel work |
| `delegate_task` | Yes — parent waits for the result | No — single attempt | A sub-task that needs a fresh context window, whose answer the parent needs now |
| `spawn_task` | No — returns a `task_id` | Yes — retries, DAG dependencies, pause/resume | Durable work that must outlive the turn or depend on other tasks |

None of the three gives the child its own workspace: every child session — `spawn_worker`, `delegate_task`, and task attempts alike — inherits the parent's `storage_bucket`, `storage_key_prefix`, and `workspace_path` and resolves to the sandbox of the tree's root, so no `sessions/{child_id}/` prefix is allocated and the whole fan-out reads and writes one `/workspace`. Siblings can overwrite each other's files. See [Runtime architecture](/develop/reference/runtime-architecture/).

### Workers (`spawn_worker`)

A worker is a full child session with its own event log and iteration budget. It runs asynchronously on any worker pod. When it finishes, a `worker.complete` event is emitted into the **parent's** event log and the parent is re-enqueued so it wakes to process the result. The parent can steer a worker with `send_worker_message` (wakes it, even after it completed) or interrupt it with `stop_worker`. Workers cannot spawn their own workers — the coordinator tool family is stripped from a worker's toolset.

### Delegation (`delegate_task`)

Delegation spawns one or more children and **waits** for them, returning their final responses as the tool result. Pass `goals=[...]` to fan out in parallel. The parent polls until each child completes (up to a 60-minute ceiling), emitting `delegation.start` / `delegation.complete` / `delegation.failed` events, and a one-shot `delegation.stale` if a child idles past threshold. Delegation depth is capped (default 2 levels); a `leaf` child cannot delegate further, an `orchestrator` child can. A delegated child inherits the parent's `excluded_tools`, and `ask_user_question`, `spawn_worker`, `send_worker_message`, and `stop_worker` are stripped regardless of preset or of what the parent's own allowlist holds — a child has no path to the user and cannot run its own workers, so design child agents to hand open questions back to the parent. Artifacts a child creates are propagated up to the parent's chat thread automatically.

### Durable tasks (`spawn_task`)

A task is a row in the database, so it survives the parent's crash. Tasks add three things workers and delegation don't have:

- **Fan-in dependencies** — `parents=[task_id, …]` keeps a task in `todo` until every parent reaches `done`, then it is promoted to `ready` and claimed. Cancelled or failed parents do not promote their children.
- **Retries** — `max_attempts` (default 3); the dispatcher gives up after that many consecutive crash/timeout attempts and marks the task `failed`. A retry is not a clean slate: attempt 2 onwards opens with a `## Prior attempts on this task` section (up to the last 5 attempts, each with its completion text, block reason, or a crashed placeholder), and the worker can call `worker_context` for the full structured detail. It also inherits the files its predecessor left in the shared workspace, so write task workers to resume rather than to assume an empty one.
- **Block / unblock** — a worker can `worker_block` to pause and wait for input. Only the session that spawned the task may resume it with `unblock_task` (optionally attaching new context, appended to `task.context` with a timestamp) or stop it with `cancel_task`; both are ownership-checked and reject a call from any other session. Cancelling a running task also interrupts its in-flight child session.

A worker running a task reports back with `worker_complete`, which carries a human-readable `summary` (becomes `task.result`) plus free-form structured `metadata` (e.g. `changed_files`, `tests_run`, `decisions`). Successful completion reuses the `worker.complete` event, carrying the `task_id` so the parent can correlate; `task.blocked` and `task.failed` mark the other transitions.

### How results and progress are tracked

- **Events** — outcomes flow back as `worker.*`, `delegation.*`, and `task.*` events on the parent's log. See [Event types → Sub-agent / task events](/develop/reference/event-types/).
- **Live tree** — a session's detail view shows a Running panel and per-child links; `GET /v1/sessions/{id}/tree` returns the descendant graph. See [Sessions → Sub-agent observability](/develop/features/sessions/).
- **The board** — a fan-out of workers/tasks shares a coordination board so siblings reuse each other's findings without routing through the parent. See [Coordination & the board](/develop/reference/coordination/).

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
| Training collector | on demand | Exports successful expert-delegation and skill-invocation trajectories from the event log as JSONL to the tenant bucket, for external fine-tuning |

The training collector's responsibility ends at the JSONL file — training strategy, evaluation, and model hosting are the organization's concern.

## Related

- [Coordination & the board](/develop/reference/coordination/) — how parallel background work coordinates.
- [Missions](/work/tools/missions/) — a coordinator that decomposes a goal into durable tasks.
- [Sessions](/develop/features/sessions/) — reading a session and its sub-agent tree.
- [Event types](/develop/reference/event-types/) — the events every background primitive emits.

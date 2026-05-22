---
title: Runtime architecture
sidebar_position: 1
---

# Runtime architecture

The Surogate runtime (`invergent-ai/surogates` on GitHub) is what's actually running inside the container when your agent is deployed at `<slug>.cloud.surogate.ai`. This reference summarises its architecture for builders who need to know how things work end-to-end.

For the full runtime documentation, see [`surogates/docs/`](https://github.com/invergent-ai/surogates/tree/main/docs).

## Three components

```
+-----------------------------------------------------------+
| API Server (trusted)                                      |
| - S3 credentials for all tenant-* and agent-* buckets     |
| - DB credentials (sessions, tenants)                      |
| - Serves skills, memory, workspace files to frontend      |
| - Issues scoped tokens to worker pods                     |
+------------------------+----------------------------------+
                         | HTTP API (session-scoped token)
+------------------------v----------------------------------+
| Worker (trusted, but no tenant S3 access)                 |
| - DB + Redis access (session state, event log)            |
| - API token for calling API server (skills, memory)       |
| - Manages sandbox pods via K8s API                        |
| - Does NOT run untrusted code directly                    |
+------------------------+----------------------------------+
                         | K8s exec API / subprocess
+------------------------v----------------------------------+
| Sandbox (untrusted)                                       |
| - S3 credentials scoped to the agent bucket session path  |
| - s3fs-fuse mounts session path as /workspace             |
| - Runs tool commands (terminal, file I/O, code exec)      |
| - No DB access, no API token, no tenant S3 access         |
| - Cannot access other sessions or tenant data             |
+-----------------------------------------------------------+
```

## API Server

FastAPI app. Serves:
- Web SPA static files
- REST API
- SSE event streams to the chat UI

Auth: JWT (HS256, 30-min access tokens, 24-hour refresh tokens).

Storage access: **full** — all `tenant-*` and `agent-*` Garage buckets, all PostgreSQL tables.

## Worker

Stateless Python pod that pops sessions from Redis and runs the `AgentHarness`.

Concurrency: up to 50 sessions per worker (semaphore-bounded).

Storage access: **none directly**. Tenant operations (read skills, write memory) go through the API server via `HarnessAPIClient`.

Database access: sessions, events, leases. Read + write.

Sandbox management: creates/destroys sandbox pods via K8s API.

## Sandbox

K8s pod per session, lazily provisioned on first sandbox-bound tool call.

Storage access: session-scoped only (`{agent_bucket}/sessions/{session_id}/`), mounted at `/workspace` via s3fs-fuse.

Network: K8s NetworkPolicy restricts egress to:
- MCP proxy
- Garage S3 API

Everything else (internet, DB, Redis, API server) is denied.

Lifetime: `activeDeadlineSeconds: 3600`.

## The harness wake cycle

```python
async def wake(session_id):
    1. acquire_lease(session_id)          # exclusive lock; expires after TTL
    2. session = load_session_row(session_id)
    3. events = replay_events_from(cursor)
    4. context = build_context(events, session.config)
    5. while iteration < max_iterations:
        a. response = call_llm(context)
        b. emit(llm.response, content=response)
        c. if response has tool_calls:
            for call in response.tool_calls:
                emit(tool.call, ...)
                result = await tool_router.dispatch(call)
                emit(tool.result, ...)
                context.append(call, result)
        d. else:
            emit(assistant.final, response.content)
            break
    6. update_cursor(last_event_id)
    7. release_lease()
```

Key properties:

- **Stateless** — every state read goes to PostgreSQL/Redis; every write becomes an event
- **Crash-recoverable** — a worker can die at any line; the next worker resumes from the cursor
- **Tool calls are events** — `tool.call` + `tool.result` go into the event log; replay re-executes them by reading from the log (idempotent tools recommended)

## Tool routing

```
+-----------------+
| ToolRouter      |
+--------+--------+
         |
         v
+-----------------+
| GovernanceGate  |   <-- frozen at session start; denies / escalates / allows
+--------+--------+
         |
    +----+----+
    |         |
    v         v
+-------+ +--------+
| Local | | Sandbox|
| Tools | | Tools  |
+-------+ +--------+
              |
              v
        +----------+
        |MCP Proxy |
        +----------+
              |
              v
        External MCP
        Servers
```

Tools live in three locations:

| Location | What's there | Examples |
|---|---|---|
| **Worker-local** | Tools that don't need a sandbox | memory, skills, web_search, browser_*, delegate_task, cron_*, clarify, create_artifact |
| **Sandbox** | Tools that run inside the per-session pod | terminal, read_file, write_file, patch, execute_code |
| **MCP Proxy** | Anything an MCP server exposes | Forwarded through the proxy with credential injection |

## Session-start freeze

When a session starts, the agent's config is snapshotted into `sessions.config` JSONB. This snapshot includes:

- SOUL.md text
- Allowed/denied tool lists
- Skill attachments + versions
- KB attachments + versions
- MCP server attachments
- Network egress rules
- Saga settings
- Model + endpoint

**Mid-session prompt injection cannot weaken this snapshot.** Even if a user tells the agent "ignore your rules," the rules are baked in. The `GovernanceGate` evaluates against the snapshot, not against the current state.

## Sub-agent recursion

A session can spawn child sessions via:

- `spawn_worker(goal, agent_type=)` — fire-and-forget
- `delegate_task(goal, agent_type=)` — synchronous, parent blocks
- `spawn_task(goal, parents=[...], max_attempts=3)` — durable DAG task with retry

Children share the tenant's skills/KBs/MCPs/memory. They can have a narrower governance profile (`policy_profile` in AGENT.md) that **intersects** (never widens) the parent's policy.

Depth limit: 2 (one orchestrator level beneath the root). Prevents runaway delegation trees.

Children emit `worker.complete` / `worker.failed` / `task.blocked` / `task.failed` events into the **parent's** event log, with truncated result attached.

## Saga

When `saga.enabled: true`:

```
Forward execution:
  Step 1: write_file("config.yaml")   --> committed (checkpoint saved)
  Step 2: write_file("main.py")       --> committed (checkpoint saved)
  Step 3: terminal("python test.py")  --> FAILED

Automatic compensation (reverse order):
  Step 2: restore checkpoint           --> main.py reverted
  Step 1: restore checkpoint           --> config.yaml reverted
```

Compensation strategies:

- **Built-in tools** (file writes, patches, terminal): filesystem checkpoints restored
- **MCP tools**: declared undo tool called (e.g. `delete_jira_ticket` for `create_jira_ticket`)

Read-only tools (`read_file`, `search_files`, `web_search`, `skills_list`) are excluded from tracking.

If a compensation step itself fails, the saga enters `escalated` state — an operator must intervene.

## Event log

PostgreSQL append-only:

```sql
events (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL,
  org_id UUID NOT NULL,            -- populated by trigger
  user_id UUID,                    -- nullable for API channel
  type event_type NOT NULL,
  data JSONB NOT NULL,
  trace_id UUID, span_id UUID,
  created_at TIMESTAMPTZ
)
```

The `events_populate_tenant` trigger fills `org_id` and `user_id` from the session row on insert. Lets tenant-scoped audit queries filter `events` directly without joining `sessions`.

See [Event types](./event-types.md) for the full enum.

## Channels

Five first-class channels, each with an adapter:

| Channel | Adapter |
|---|---|
| **Web** | Built into the API server's SPA |
| **Slack** | `surogate_ops/server/channels/slack/` Socket Mode |
| **Telegram** | `surogate_ops/server/channels/telegram/` Bot API |
| **Website widget** | `sdk/website-widget/` (separate npm package) |
| **API** | `POST /v1/api/prompts` — service-account tokens, no SSE |

Shared delivery model: **durable `delivery_outbox` rows + Redis nudges**. Adapters claim rows for their channel, format, send via platform API, mark delivered.

## Storage layout

```
tenant-{org_id}/
  shared/                         # org-wide
    SOUL.md
    memory/{MEMORY.md, USER.md}
    skills/<name>/SKILL.md
    agents/<name>/AGENT.md         # sub-agent definitions
    mcp/servers.json
  users/{user_id}/                # per-user
    skills/<name>/SKILL.md
    memory/{MEMORY.md, USER.md}

{agent_bucket}/
  sessions/{session_id}/workspace/  # FUSE-mounted as /workspace
  sessions/{session_id}/_artifacts/{id}/v{N}.json  # inline chat artifacts
  sessions/{session_id}/browser-screenshots/        # PNG screenshots
```

Sandbox credentials are **session-scoped STS-style tokens** that only permit access to `{agent_bucket}/sessions/{session_id}/*`. The sandbox cannot reach other sessions or tenant data.

## Trust isolation, restated

The structural fix for prompt injection: credentials and tenant data are never reachable from the sandbox where the LLM's generated code runs. Even a perfectly prompt-injected agent has no way to access keys, other sessions' data, or the broader org's storage.

## What's next

[Tool catalog](./tool-catalog.md) for every built-in tool. [Event types](./event-types.md) for the full event enum. [Glossary](./glossary.md) for terminology.

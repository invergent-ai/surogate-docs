---
title: Tool catalog
sidebar_position: 2
---

# Tool catalog

Every built-in tool the runtime ships with. Grouped by **runtime location**.

For full schemas, see the [`surogates/docs/tools/index.md`](https://github.com/invergent-ai/surogates/blob/main/docs/tools/index.md).

## Worker-local tools (no sandbox)

### Memory

| Tool | Purpose |
|---|---|
| `memory` | add/replace/remove against `MEMORY.md` or `USER.md`. Per-session memory updates that persist between sessions. |

### Skills

| Tool | Purpose |
|---|---|
| `skills_list` | List available skills (visible to the LLM as the catalog) |
| `skill_view` | Read a specific skill's content |
| `skill_manage` | Create/update/delete skills from within a session |

### Experts

| Tool | Purpose |
|---|---|
| `consult_expert` | Delegate a task to an active expert. Returns the expert's final response. |

### Sub-agents (fire-and-forget)

| Tool | Purpose |
|---|---|
| `spawn_worker` | Spawn a child session with an optional `agent_type` preset. Returns worker_id immediately. |
| `send_worker_message` | Send a message to a running spawned worker. |
| `stop_worker` | Stop a running spawned worker. |

### Sub-agents (synchronous)

| Tool | Purpose |
|---|---|
| `delegate_task` | Spawn a child session and block until it completes. Supports batched `goals=[...]` for parallel fan-out. Hard depth limit = 2. |

### Tasks (DAG-aware durable layer)

| Tool | Purpose |
|---|---|
| `spawn_task` | Create a durable task. Supports DAG `parents=[...]` for fan-in. Auto-retries on crash. |
| `unblock_task` | Resume a blocked task with optional `additional_context`. |
| `cancel_task` | Abort a non-terminal task. |
| `task_complete` | (Self-tool, only visible when `Session.task_id is not None`) — mark own task `done` with structured `summary` + `metadata`. |
| `task_block` | (Self-tool) — pause without consuming a retry attempt. |
| `task_show` | (Self-tool) — read own task + parents + prior attempt summaries. |

### Scheduling

| Tool | Purpose |
|---|---|
| `cron_create` | Create a recurring scheduled prompt. Cron expression, prompt, recurring/durable, name, timezone. |
| `cron_delete` | Cancel a schedule. |
| `cron_list` | List active schedules for the current user + agent. |
| `loop_wait` | (Dynamic-loop-only) — set next delay in seconds (60-3600). Can also signal `completed: true`. |
| `loop_complete` | (Fixed-cron-loop-only) — mark the loop finished from inside a run. |

### Web & Research

| Tool | Purpose |
|---|---|
| `web_search` | Web search via Tavily / Exa. Respects robots.txt. |
| `web_extract` | Fetch and extract a URL's content. |
| `web_crawl` | Crawl multiple URLs. |

### Vision

| Tool | Purpose |
|---|---|
| `vision_analyze` | Analyze an image (workspace path, HTTPS URL, or `data:image` base64). Returns text describing the image. |

### Session history

| Tool | Purpose |
|---|---|
| `session_search` | Full-text search the session's event history. Filterable by event type. |

### User dialogue

| Tool | Purpose |
|---|---|
| `clarify` | Show the user a tabbed widget with 1-5 questions and up to 4 multiple-choice answers each. Returns the user's selections. 30-min wait cap. |

### Inline output

| Tool | Purpose |
|---|---|
| `create_artifact` | Render a named, versioned artifact inline in the chat. 5 kinds: markdown, table, chart (Chart.js), html (iframe-sandboxed), svg. Max 500 KB / artifact, 200 artifacts / session. |

### Todo

| Tool | Purpose |
|---|---|
| `todo` | Per-session todo list for tracking multi-step tasks. |

### Browser (session-scoped Chromium)

| Tool | Purpose |
|---|---|
| `browser_navigate` | Navigate to a URL |
| `browser_get_state` | Return the page's accessibility tree with stable `@eN` refs |
| `browser_click` | Click an `@eN` ref or viewport coordinates |
| `browser_type` | Type text at the current focus |
| `browser_press_key` | Press a key or chord (e.g. `Enter`, `Control+L`) |
| `browser_scroll` | Scroll at viewport coordinates |
| `browser_drag` | Drag along coordinates |
| `browser_wait` | Wait up to 30s for transitions |
| `browser_screenshot` | Capture PNG to the workspace, optionally with annotations |
| `browser_close` | Close the browser for this session |

Browser tools support **user control handoff** — the user can take over for login/MFA/CAPTCHA, then return control.

## Sandbox-bound tools

### `terminal`

Shell command execution.

| Parameter | Type | Description |
|---|---|---|
| `command` | string | Shell command |
| `workdir` | string | Default `/workspace` |
| `timeout` | integer | Default 180s, max 600 |

Output truncated at 50,000 characters; ANSI escape codes stripped.

### `read_file` / `write_file` / `patch`

| Tool | Purpose |
|---|---|
| `read_file` | Read with optional `offset` and `limit` line ranges |
| `write_file` | Write contents to a path. Denies writes to sensitive paths (SSH keys, shell rc, credential files). |
| `patch` | Apply unified diff or V4A patch format. Fuzzy matching for context lines. |

### `search_files` / `list_files`

| Tool | Purpose |
|---|---|
| `search_files` | Regex search across files. Filter by `include` glob pattern. |
| `list_files` | List directory contents. Optional `recursive`. |

### `execute_code`

Programmatic code execution. Lets the agent call other tools from inside generated code:

| Parameter | Type |
|---|---|
| `language` | `python` / `javascript` / ... |
| `code` | The code to execute |

The code runs inside the sandbox with access to all sandbox-bound tools.

## MCP-proxied tools

Anything registered by an MCP server is forwarded through the MCP proxy. Tools are passed-through to the LLM by name + description, but credentials are injected at the proxy boundary — the sandbox never sees them.

For setting up MCP servers, see [MCP & Vault](../features/mcp-and-vault.md).

## Tool governance

Every tool call passes through the `GovernanceGate` before execution. Three outcomes:

| Outcome | Effect |
|---|---|
| `allow` | Tool executes |
| `deny` | Returns error to LLM; emit `policy.denied` event |
| `escalate` | Pause and ask user; emit `policy.escalated` event + inbox `governance_gate` item |

Tools can be allowlisted/denylisted per-agent in CONFIG. ABAC rules allow fine-grained control (e.g. "allow `refund_user` only if `amount < 1000`").

Read-only tools (`read_file`, `search_files`, `web_search`) are usually safe to allow broadly. Mutating tools (`write_file`, `patch`, `terminal`, MCP tools that create external resources) need careful policy.

## What's next

[Event types](./event-types.md) for what tool calls produce in the log. [Runtime architecture](./runtime-architecture.md) for the bigger picture.

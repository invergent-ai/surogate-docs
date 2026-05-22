---
title: Tool catalog
sidebar_position: 2
---

# Tool catalog

Every built-in tool an agent can call. These are the names you set in an agent's CONFIG → Allowed Tools / Denied Tools.

You don't pick which tool the agent uses for a given turn — the agent does. You decide which tools to **expose**.

## File I/O

| Tool | Use for |
|---|---|
| `read_file` | Read workspace files (with optional offset/limit) |
| `write_file` | Write a file (sensitive paths denied — SSH keys, shell rc, credentials) |
| `patch` | Apply a unified diff or V4A patch |
| `search_files` | Regex across workspace files |
| `list_files` | Directory listing, optionally recursive |

## Shell + code

| Tool | Use for |
|---|---|
| `terminal` | Shell command in the sandbox (180s default timeout, 50K-char output cap) |
| `execute_code` | Run agent-generated code that itself calls other tools |

## Web

| Tool | Use for |
|---|---|
| `web_search` | Public-web search (Tavily / Exa backends) |
| `web_extract` | Fetch and extract a single URL |
| `web_crawl` | Crawl multiple URLs |

## Browser (Chromium)

Session-scoped browser. Supports **user-control handoff** for login / MFA / CAPTCHA.

| Tool | Use for |
|---|---|
| `browser_navigate` | Open a URL |
| `browser_get_state` | Page's accessibility tree with stable element refs |
| `browser_click`, `browser_type`, `browser_press_key` | Interact |
| `browser_scroll`, `browser_drag`, `browser_wait` | Navigate / wait |
| `browser_screenshot` | Save PNG to workspace |
| `browser_close` | Close the session's browser |

## Vision

| Tool | Use for |
|---|---|
| `vision_analyze` | Analyse a workspace image, HTTPS URL, or `data:image` base64 |

## Memory

| Tool | Use for |
|---|---|
| `memory` | add / replace / remove entries in `MEMORY.md` (agent's notes) or `USER.md` (user facts) |

## Skills & experts

| Tool | Use for |
|---|---|
| `skills_list` | List skills attached to this agent (the LLM uses this implicitly) |
| `skill_view` | Read a specific skill's body |
| `skill_manage` | Create / update / delete skills from inside a session |
| `consult_expert` | Delegate to a configured expert (model-backed skill) |

## Sub-agents

| Tool | Use for |
|---|---|
| `spawn_worker` | Fire-and-forget child session. Returns immediately. |
| `delegate_task` | Synchronous child session — parent blocks for the result. Supports parallel fan-out via `goals=[...]`. |
| `spawn_task` | Durable child with DAG dependencies, retries, and mid-run pause. |
| `task_complete`, `task_block`, `task_show` | Self-tools the child uses to report back |
| `unblock_task`, `cancel_task` | Coordinator-side task management |

Hard depth limit: 2 levels of orchestration beneath the root coordinator.

## Scheduling

| Tool | Use for |
|---|---|
| `cron_create` | Create a recurring scheduled prompt (5-field cron expression) |
| `cron_delete`, `cron_list` | Manage schedules |
| `loop_wait` | (Dynamic-loop only) set the next delay in 60-3600s, or signal completion |
| `loop_complete` | (Fixed-cron loop only) mark loop finished from inside a run |

## User interaction

| Tool | Use for |
|---|---|
| `clarify` | Ask the user up to 5 multiple-choice questions in a tabbed widget. 30-min wait cap. |

## Inline output

| Tool | Use for |
|---|---|
| `create_artifact` | Render a markdown / table / chart / HTML / SVG artifact inline in the chat (500KB max per artifact, 200 per session) |

## Other

| Tool | Use for |
|---|---|
| `todo` | Per-session multi-step task tracker |
| `session_search` | Full-text search the session's event history |

## MCP-proxied tools

Any tool an MCP server registers becomes available to attached agents. The MCP proxy injects credentials from the Vault — the agent's sandbox never sees secrets. See [MCP & Vault](../features/mcp-and-vault.md) for setup.

## Allowed vs denied

Configure per-agent in CONFIG → Tool Access:

- **Allowlist** — only these tools are visible to the LLM. Empty allowlist = all tools (subject to denylist).
- **Denylist** — always blocked. Deny beats allow.

Common patterns:

| Agent type | Suggested |
|---|---|
| Customer support | Allow: `kb_*`, `web_search`, `clarify`, `create_artifact`, `memory`. Deny: `terminal`, `execute_code`, `write_file`, `patch` |
| Code assistant | Allow: read tools + `web_search`. Deny: `write_file`, `patch`, `terminal` |
| Data analyst | Allow everything. Deny: `cron_*` if no scheduling |
| Internal automation bot | Start with denylist only, gate the dangerous ones explicitly |

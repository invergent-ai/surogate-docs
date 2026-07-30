---
title: Tool catalog
---

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

## Shell

| Tool | Use for |
|---|---|
| `terminal` | Shell command in the sandbox (180s default timeout, 50K-char output cap, optional `background=true`) |
| `process` | Manage background processes started with `terminal(background=true)` — list / poll / log / wait / kill / write / submit |

## Web

| Tool | Use for |
|---|---|
| `web_search` | Public-web search (Tavily / Exa backends) |
| `web_extract` | Fetch and extract one or more URLs |

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
| `vision_analyze` | Analyse a workspace image path, HTTPS URL, or `data:image` base64 (raster only — PNG/JPEG/WEBP/GIF) |

## Media generation

| Tool | Use for |
|---|---|
| `generate_image` | Generate an image from a text prompt (optional image-to-image); saved to the workspace and shown inline |
| `generate_video` | Generate a video from a text prompt (optional first-frame image-to-video); blocks until rendered, saved to the workspace |

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

## Knowledge base

| Tool | Use for |
|---|---|
| `kb_list_pages` | List all pages in a knowledge base, grouped by page type (index / summary / concept) |
| `kb_read_page` | Read the full markdown content of a single wiki page |

## Channel history

| Tool | Use for |
|---|---|
| `fetch_channel_messages` | Read recent messages posted in this channel (optionally filter by `since` / `user`) |
| `fetch_channel_file` | Fetch a file shared in this channel (by name or Slack file id) into the workspace |

## GitHub & coding

| Tool | Use for |
|---|---|
| `github` | GitHub REST API over the agent's configured repos, without a checkout — read (default) or write issues/PRs/files/labels |
| `run_coding_agent` | Run Claude Code or Codex on a configured repo — checks out a branch, implements, commits, pushes, and opens a PR (the `/code` tool) |

## Sub-agents & coordination

| Tool | Use for |
|---|---|
| `spawn_worker` | Fire-and-forget async worker session. Returns the worker's ID immediately; results arrive as events next turn. |
| `send_worker_message` | Send a message to a running worker |
| `stop_worker` | Stop a running worker |
| `delegate_task` | Synchronous child session — parent blocks for the result. Supports parallel fan-out via `goals=[...]`. |
| `spawn_task` | Durable child task — survives parent crash, supports fan-in dependencies, retries, and block/unblock. |
| `worker_complete` | Worker self-tool: mark your own task attempt done with a structured handoff to the parent |
| `worker_block` | Worker self-tool: pause your own attempt and wait for parent/human context |
| `worker_context` | Worker self-tool: read your own goal, parent context, parent-task results, and prior attempts |
| `unblock_task` | Coordinator-side: resume a blocked child task (optional additional context) |
| `cancel_task` | Coordinator-side: cancel a non-terminal child task |

Coordination board (parallel workers in a group share verified notes):

| Tool | Use for |
|---|---|
| `share_note` | Post a verified FACT / FAIL / CLAIM / RESULT note to the group's board |
| `read_board` | Read the group's consolidated current board state |
| `expand_note` | Expand a board note (by `n<ID>`) into its underlying source content or artifact |

Ambient channel:

| Tool | Use for |
|---|---|
| `mate_ambient_post` | Post a proactive, confidence-gated message into the channel during an ambient review (Surogate Mate) |

Hard depth limit: 2 levels of orchestration beneath the root coordinator.

## Research (Arbor + deep research)

| Tool | Use for |
|---|---|
| `idea_tree` | Read and mutate a research run's Idea Tree (view / add / update / prune / set_meta) |
| `dispatch_experiments` | Dispatch 1–4 pending leaf hypotheses to executor workers in isolated git worktrees |
| `merge_experiment` | Re-run the held-out test eval in a detached worktree, then merge a done experiment into trunk |
| `research_memory` | Curated evidence bank for deep research — add / retrieve / list cited sources |
| `research_outline` | The living research outline (markdown) — set / get |

## Scheduling

| Tool | Use for |
|---|---|
| `cron_create` | Create a recurring scheduled prompt (5-field cron expression) |
| `cron_delete`, `cron_list` | Manage schedules |
| `loop_wait` | (Dynamic-loop only) set the next delay in 60–3600s, or signal completion |
| `loop_complete` | (Fixed-cron loop only) mark loop finished from inside a run |

## User interaction

| Tool | Use for |
|---|---|
| `ask_user_question` | Ask the user up to 5 questions (each up to 4 labeled choices + optional "Other") in a tabbed chat widget, and wait for the batched answers. 30-min wait cap. |

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

Any tool an MCP server registers becomes available to attached agents. The MCP proxy injects credentials from the Vault — the agent's sandbox never sees secrets. See [MCP & Vault](/develop/features/mcp-and-vault/) for setup.

## Allowed vs denied

Configure per-agent in CONFIG → Tool Access:

- **Allowlist** — only these tools are visible to the LLM. Empty allowlist = all tools (subject to denylist).
- **Denylist** — always blocked. Deny beats allow.

Common patterns:

| Agent type | Suggested |
|---|---|
| Customer support | Allow: `kb_*`, `web_search`, `ask_user_question`, `create_artifact`, `memory`. Deny: `terminal`, `write_file`, `patch` |
| Code assistant | Allow: read tools + `web_search` + `github`. Deny: `write_file`, `patch`, `terminal` |
| Data analyst | Allow everything. Deny: `cron_*` if no scheduling |
| Internal automation bot | Start with denylist only, gate the dangerous ones explicitly |

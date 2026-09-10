---
title: Tool catalog
---

Every built-in tool an agent can call. These are exactly the names the Governance policy accepts in **Allowed tools / Denied tools** — the catalog is generated from the runtime's real tool registry, and unknown names are rejected on save. (`execute_code` and `web_crawl` are not tools; the shell entry point is `terminal`.)

You don't pick which tool the agent uses for a given turn — the agent does. You decide which tools to **expose**.

The coordination self-tools (`worker_complete`, `worker_block`, `worker_context`, `share_note`, `read_board`, `expand_note`, `unblock_task`, `cancel_task`) are listed below for completeness but are **not configurable** in the allow/deny lists — denying them could strand blocked work, so the policy API refuses them.

## File I/O

| Tool | Use for |
|---|---|
| `read_file` | Read workspace files with line numbers and pagination (`offset` / `limit`) — parses documents, describes images |
| `write_file` | Write a file (sensitive paths denied — SSH keys, shell rc, credentials) |
| `patch` | Apply a unified diff or V4A patch |
| `search_files` | Regex across workspace files |
| `list_files` | Directory listing, optionally recursive |

`read_file` is not text-only. `.pdf`, Word (`.doc` / `.docx` / `.docm`), Excel (`.xls` / `.xlsx` / `.xlsm`), PowerPoint (`.ppt` / `.pptx` / `.pptm`), OpenDocument (`.odt` / `.ods` / `.odp`) and `.rtf` are parsed to text by the tool itself, and image files are described by a vision model. Calling `read_file` on those paths directly is the intended path — no need to shell out to `pdftotext` or pip-install a parser through `terminal`. Two limits to plan around: `limit` defaults to 500 lines and caps at 2000, and a single read over roughly 100K characters is rejected outright (an operator-tunable default) — page through large files with `offset` / `limit`.

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
| `browser_get_state` | Page as a markdown outline with stable `@eN` refs (`format: "json"` for the raw node tree with coordinates) |
| `browser_evaluate` | Run JavaScript in the page and return its value — a whole table, a hidden input, every option of a `<select>` in one call |
| `browser_click`, `browser_type`, `browser_press_key` | Interact |
| `browser_scroll`, `browser_drag`, `browser_wait` | Navigate / wait |
| `browser_screenshot` | Save PNG to workspace |
| `browser_close` | Close the session's browser |

`browser_evaluate` runs agent-written JavaScript with the page's full privileges, against whatever the browser is currently signed in to. It is governed like any other tool, but it is the widest reach in the browser toolset — deny it explicitly on agents where you allow the rest of `browser_*`. See [Agent browser](/develop/features/browser/).

## Vision

| Tool | Use for |
|---|---|
| `vision_analyze` | Analyse a workspace image path, HTTPS URL, or `data:image` base64 (raster only — PNG/JPEG/WEBP/GIF) |

## Media generation

| Tool | Use for |
|---|---|
| `generate_image` | Generate an image from a text prompt (optional image-to-image); saved to the workspace and shown inline |
| `generate_video` | Generate a video from a text prompt (optional first-frame image-to-video); blocks until rendered, saved to the workspace |

Availability: each tool is **dropped from the agent's toolset entirely** when no model is wired for its role (a per-agent pick under Configure → Model, or a platform preset) — the LLM never sees an unusable tool. Platform-model generation bills the project's **media wallet** (a flat few cents per image; a video bills its reported provider cost); BYO image/video models are not metered by Surogate. When the wallet is empty the tool returns an actionable `media_budget_exhausted` error — nothing is generated or charged — and on monetized agents a buyer without media credits gets `media_credits_exhausted` with their buy link. See [Media generation](/develop/features/media-generation/).

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
| `fetch_channel_messages` | Read recent messages in this Slack channel — `limit` (default 50, max 200), `since` (`24h`, `7d`, or `2026-07-01`), `user` (a Slack user id or `<@U…>` mention). Returns oldest-to-newest |
| `fetch_channel_file` | Fetch a file shared in this Slack channel (by name or Slack file id) into the workspace |

Both are **Slack-only**: on a session whose effective channel isn't Slack (Telegram, WhatsApp, website, web) they return an error rather than a result, so allow-listing them on a non-Slack agent buys nothing. Ambient sessions count as Slack. Inbound attachments on the other channels still reach the workspace through the normal attachment path.

## Check-in Programs

| Tool | Use for |
|---|---|
| `checkin_outcome` | Record how a scheduled check-in ended — `outcome` (`completed` or `declined`), optional `note` for the operator's run history. Closes the check-in; messages nobody |
| `checkin_escalate` | Raise the check-in to the responsible operator — `reason`. Lands in that operator's Inbox as an `action_required` item titled "Check-in needs your attention"; does not end the check-in |

Both are offered on channel sessions only, and only do anything inside a conversation a Program opened: the invitation is looked up by session, and elsewhere they return an error. The agent is told to call them by the synthetic `[Check-in]` message that arrives with the user's reply. See [Programs](/work/tools/programs/).

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

How answers arrive depends on the channel:

| Channel | Widget | Typed reply |
|---|---|---|
| **Web** | Yes | Yes — a plain text message while the question is pending is consumed as the answer |
| **Telegram** | Yes | Yes — same rule |
| **Slack** | Modal | No — a typed reply gets a nudge toward the modal |
| **API service accounts** | Respond route only | Never converted |

Typed-reply mapping: text that exactly matches a choice label (case-insensitive) selects that choice; anything else is recorded as an "Other" answer; a multi-question prompt receives the whole reply against each question. Messages with images or attachments are never converted, and the conversion stops working shortly before the 30-minute cap. Once a response exists for the tool call, later messages are ordinary messages.

## Inline output

| Tool | Use for |
|---|---|
| `create_artifact` | Render a markdown / table / chart / HTML / SVG artifact inline in the chat (500KB max per artifact, 200 per session) |

## Other

| Tool | Use for |
|---|---|
| `todo` | Per-session multi-step task tracker |
| `session_search` | Full-text search the session's event history |
| `user_reports` | Operator-only: read the agent's per-user and cohort reports (overview / get / list) |

## MCP-proxied tools

Any tool an MCP server registers becomes available to attached agents. The MCP proxy injects credentials from the Vault — the agent's sandbox never sees secrets. See [MCP & Vault](/develop/features/mcp-and-vault/) for setup.

MCP tools (`mcp__*`) are **outside the built-in allow/deny lists**: an allowlist doesn't reject them, and a denylist won't accept an `mcp__*` name either. They're governed by which servers you attach (and, on monetized agents, by the buyer's package); egress and sandbox checks still apply, and the approval list below is the one place a single MCP tool can be gated by name.

## Allowed, denied, and approval-required

Three lists govern a tool call. Allowlist and denylist are configured per-agent in CONFIG → Tool Access:

- **Allowlist** — only these built-in tools pass the governance gate. Empty allowlist = all tools (subject to denylist). Note: a tool outside the allowlist is still *advertised* to the LLM — it's blocked at call time with a `Blocked: <reason>` result, not hidden from the schema.
- **Denylist** — always blocked. Deny beats allow, and the two lists can't overlap.
- **Approval-required** (`require_approval` on the agent policy) — the call is held and raised to a human as a `governance_gate` inbox item; approving lets the agent's retry of that exact call through. Evaluation order is **deny → approval → allow**, so a denied tool is never approvable, and this is the only list that accepts `mcp__*` names. Set it through the agents API: the tool-access form doesn't render it, and saving that form drops it. See [Tools that need approval first](/work/workflow/governance/#tools-that-need-approval-first).

Lists take **exact tool names** — there is no prefix or wildcard matching. Common patterns:

| Agent type | Suggested |
|---|---|
| Customer support | Allow: `kb_list_pages`, `kb_read_page`, `web_search`, `ask_user_question`, `create_artifact`, `memory`. Deny: `terminal`, `write_file`, `patch` |
| Code assistant | Allow: read tools + `web_search` + `github`. Deny: `write_file`, `patch`, `terminal` |
| Data analyst | Allow everything. Deny: `cron_create`, `cron_delete`, `cron_list` if no scheduling |
| Internal automation bot | Start with denylist only, gate the dangerous ones explicitly |

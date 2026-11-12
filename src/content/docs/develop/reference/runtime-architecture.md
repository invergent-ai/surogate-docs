---
title: How the runtime behaves
---

The platform handles all the infrastructure — Kubernetes, model serving, sandboxing, policy enforcement. As someone building agents on top of `ops.surogate.ai`, you don't manage any of that, but a few **behavioural guarantees** matter when you design agents:

## Sessions are durable and append-only

Every conversation is recorded as an immutable event log. If the agent crashes mid-turn, it picks up where it left off — no state lost. Tool calls and results are part of the log, so you can replay and audit any session forever.

**What this means for you**: writing tools and skills, you can assume the agent's prior tool calls are visible to subsequent turns. Sessions outlive container restarts. The session ID is stable; share it freely.

## A mid-turn message steers, it doesn't restart

A user message that arrives while a turn is running is neither discarded nor treated as a cancel. The in-flight model response and its tool calls finish, then the message is folded in at the next iteration boundary as a fresh user turn and the **same run continues**. Several messages arriving in the same window are coalesced into one turn. A follow-up that lands just as the final response is emitted keeps the run going instead of completing the session. Synthetic `user.message` events (mission continuations, harness nudges) never steer.

**What this means for you**: a mid-task "also check Z" costs no re-run — the agent adapts without losing the work already done. An explicit **Stop** is a hard cancel and always wins over a steer. Note that the shipped chat composer stops the running turn before sending, so steering from that UI is the Stop button rather than a queued message; a message sent while the agent is waiting on an `ask_user_question` answer goes straight through.

## The agent runs in an isolated sandbox

Code execution, file I/O, and terminal commands run inside a sandbox that has **no access** to your tenant's other data, no credentials, no database. The sandbox only sees its own workspace at `/workspace`. It is keyed to the root of a session tree, so a session and every child it spawns share one sandbox and one workspace.

**What this means for you**: even a fully prompt-injected agent can't exfiltrate credentials or reach other session trees. Files the agent writes are scoped to the tree's workspace; a child writes into the same `/workspace` as its parent.

## Governance is frozen per wake

The governance gate is composed once per wake — a platform floor (workspace path containment, path-argument hygiene; no agent config can relax it) narrowed by the agent's own policy — and frozen for that wake. Mid-turn prompt injection cannot weaken it.

**What this means for you**: policy edits are projected into the agent's runtime config with a version bump and a cache invalidation, so live sessions pick up the new policy at their **next wake** — you don't have to wait for new sessions. Within a wake, nothing moves. Two more scoping rules: built-in tools absent from the catalog fail closed, while `mcp__*` tools bypass the built-in allow-list (they're governed by MCP-server attachment and entitlements instead), and the coordination self-tools can never be denied.

## Tools route to different locations

You don't pick where a tool runs — but knowing helps debug behaviour:

- **In the worker** — fast, no sandbox needed (memory, skill loading, web search, browser, scheduling, sub-agent delegation, `ask_user_question`, `create_artifact`)
- **In the sandbox** — anything that touches files or runs code (`terminal`, `process`, `read_file`, `write_file`, `patch`)
- **Through the MCP proxy** — external systems via the Model Context Protocol; credentials injected by the proxy so the sandbox never sees them
- **In the agent's own editor session** — `office_read` and `office_edit` work through an editor session the platform holds for the agent on each document, so the agent's edits arrive in the same live editor the user has open

See [Tool catalog](/develop/reference/tool-catalog/) for the full list.

## An open document has one writer

While an office document is open in the editor, the editor is its only writer. The agent changes it only through `office_edit`, and a `write_file` or `patch` to it is refused. A call's ops apply all or none, and a target the user changed since the agent read it refuses the call. Every document a turn edited is saved when the turn ends; a save that finds the file changed underneath it lands as a copy beside it and never overwrites.

**What this means for you**: don't build an office file with a script in a chat that has a file pane; the agent's built-in `office` skill does it with `office_edit`, so the user can watch and edit. A skill that must produce a file with scripts, such as a PDF with content, writes a new file. See [Office documents](/work/tools/office-documents/).

## Multi-agent topology

Agents start child agents with the `agent` tool, and follow them up with `send_message`, `list_agents` and `stop_agent`. Each child is its own full session with its own event log and iteration budget, but it shares the root session's workspace and storage prefix — no per-child storage is allocated.

Children inherit the tenant's skills, KBs, MCPs, and memory — and the parent's governance policy **verbatim**. A child is created with the parent's `agent_id`, so its gate is composed from the same policy: same allow-list, same deny-list, same approval requirements. There is no per-sub-agent policy profile.

What actually scopes a child is its [sub-agent](/work/tools/sub-agents/) definition (`AGENT.md`):

| Frontmatter key | Effect on the child |
|---|---|
| `tools` | Becomes the child's allow-list — authoritative, not intersected with the parent's |
| `disallowed_tools` | Dropped from the child's toolset. Only takes effect when the definition sets no `tools`; an allow-list supersedes it |
| `model` | Used unless the `agent` call names a model explicitly |
| `max_iterations` | Narrows the child's budget when smaller than the cap |

Both lists are applied as a **toolset filter**, not a runtime denial — an excluded tool's schema never reaches the child's model, so there is nothing for it to refuse or argue around. The iteration cap is **30**, and a child gets at most what is left of the parent's budget (so a child started late in a long turn starts with less), narrowed by the definition's `max_iterations`.

Hard depth limit: **2** (a sub-agent of the root may start agents of its own; theirs may not). Prevents runaway trees.

**What this means for you**: you can build coordinator agents that fan out work, but you can't build arbitrary-depth agent trees. The 2-level cap is a safety property.

## Saga rollback for multi-step external mutations

When `saga.enabled: true`, sequential state-changing tool calls are tracked. If a later step fails, completed steps roll back via filesystem checkpoints (built-in tools) or declared undo tools (MCP tools).

**What this means for you**: design your MCP servers with explicit undo tools (`delete_ticket` undoes `create_ticket`) so saga can compensate. Without an undo, the saga enters an `escalated` state and a human must intervene.

## Trust boundaries that affect you

| Concern | Where it's enforced |
|---|---|
| Per-session network policy | Sandbox can reach only the MCP proxy + the session tree's storage. Internet, DB, other sessions: denied. |
| Per-tool governance | Synchronous check before every tool call. Denials are always logged (`policy.denied`); allowed calls are logged too when the deployment enables `governance.log_allowed`. |
| Per-session-tree resource isolation | Each session tree has its own storage path and its own sandbox |
| Per-tenant data isolation | Org-scoped storage, JWT auth, never cross-tenant |

You can read every governance decision after the fact in the session's POLICIES tab.

---

That's the runtime behavior you need. Implementation internals — the harness loop, lease semantics, the events table schema, K8s topology — live in the [`invergent-ai/surogates` runtime repo](https://github.com/invergent-ai/surogates) and matter only if you're contributing to the platform itself.

---
title: How the runtime behaves
sidebar_position: 1
---

# How the runtime behaves

The platform handles all the infrastructure — Kubernetes, model serving, sandboxing, policy enforcement. As someone building agents on top of `ops.surogate.ai`, you don't manage any of that, but a few **behavioural guarantees** matter when you design agents:

## Sessions are durable and append-only

Every conversation is recorded as an immutable event log. If the agent crashes mid-turn, it picks up where it left off — no state lost. Tool calls and results are part of the log, so you can replay and audit any session forever.

**What this means for you**: writing tools and skills, you can assume the agent's prior tool calls are visible to subsequent turns. Sessions outlive container restarts. The session ID is stable; share it freely.

## The agent runs in an isolated sandbox

Code execution, file I/O, and terminal commands run inside a per-session sandbox that has **no access** to your tenant's other data, no credentials, no database. The sandbox only sees its own workspace at `/workspace`.

**What this means for you**: even a fully prompt-injected agent can't exfiltrate credentials or reach other sessions. Files the agent writes during a session are scoped to that session.

## Governance is frozen per wake

The governance gate is composed once per wake — a platform floor (workspace path containment, path-argument hygiene; no agent config can relax it) narrowed by the agent's own policy — and frozen for that wake. Mid-turn prompt injection cannot weaken it.

**What this means for you**: policy edits are projected into the agent's runtime config with a version bump and a cache invalidation, so live sessions pick up the new policy at their **next wake** — you don't have to wait for new sessions. Within a wake, nothing moves. Two more scoping rules: built-in tools absent from the catalog fail closed, while `mcp__*` tools bypass the built-in allow-list (they're governed by MCP-server attachment and entitlements instead), and the coordination self-tools can never be denied.

## Tools route to different locations

You don't pick where a tool runs — but knowing helps debug behaviour:

- **In the worker** — fast, no sandbox needed (memory, skill loading, web search, browser, scheduling, sub-agent delegation, `ask_user_question`, `create_artifact`)
- **In the sandbox** — anything that touches files or runs code (`terminal`, `process`, `read_file`, `write_file`, `patch`)
- **Through the MCP proxy** — external systems via the Model Context Protocol; credentials injected by the proxy so the sandbox never sees them

See [Tool catalog](./tool-catalog.md) for the full list.

## Multi-agent topology

Agents can spawn child agents via `spawn_worker`, `delegate_task`, or `spawn_task`. Each child is its own full session with its own event log and storage. Children inherit the tenant's skills, KBs, MCPs, and memory; they can have a narrower governance profile.

Hard depth limit: **2** (one orchestrator level beneath the root). Prevents runaway delegation trees.

**What this means for you**: you can build coordinator agents that fan out work, but you can't build arbitrary-depth agent trees. The 2-level cap is a safety property.

## Saga rollback for multi-step external mutations

When `saga.enabled: true`, sequential state-changing tool calls are tracked. If a later step fails, completed steps roll back via filesystem checkpoints (built-in tools) or declared undo tools (MCP tools).

**What this means for you**: design your MCP servers with explicit undo tools (`delete_ticket` undoes `create_ticket`) so saga can compensate. Without an undo, the saga enters an `escalated` state and a human must intervene.

## Trust boundaries that affect you

| Concern | Where it's enforced |
|---|---|
| Per-session network policy | Sandbox can reach only the MCP proxy + the session's storage. Internet, DB, other sessions: denied. |
| Per-tool governance | Synchronous check before every tool call. Denials are always logged (`policy.denied`); allowed calls are logged too when the deployment enables `governance.log_allowed`. |
| Per-session resource isolation | Each session has its own storage path and its own pod |
| Per-tenant data isolation | Org-scoped storage, JWT auth, never cross-tenant |

You can read every governance decision after the fact in the session's POLICIES tab.

---

That's the runtime behavior you need. Implementation internals — the harness loop, lease semantics, the events table schema, K8s topology — live in the [`invergent-ai/surogates` runtime repo](https://github.com/invergent-ai/surogates) and matter only if you're contributing to the platform itself.

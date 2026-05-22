---
title: Glossary
sidebar_position: 4
---

# Glossary (Develop mode)

Every Surogate term, with builder-flavour definitions.

| Term | Definition |
|---|---|
| **ABAC** | Attribute-Based Access Control. Policy rules that evaluate attributes of the user / session / tool args. Example: "allow `refund_user` only if `amount < 1000`". |
| **AGENT.md** | A sub-agent definition file. YAML frontmatter + body. Frontmatter declares the sub-agent's role preset (tools, model, max_iterations, policy_profile). Body is the system prompt the spawned child session uses. |
| **Agent (deployed)** | A Helm release running on K8s with a URL like `<slug>.cloud.surogate.ai`. Bundles model, skills, KBs, MCPs, persona, channels, config. |
| **Agent (coordinator)** | The role a parent LLM plays inside a session when it spawns sub-agents via `spawn_worker` / `delegate_task` / `spawn_task`. |
| **Agent (sub-agent)** | A child session spawned by a coordinator, applied with an `AGENT.md` preset. |
| **AGT** | [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit). Surogate uses AGT's `PolicyEngine`, `MCPSecurityScanner`, `CapabilityModel`. |
| **API Channel** | Programmatic channel. `POST /v1/api/prompts` with a service-account `surg_sk_...` token. No SSE — pipelines pull from the events table. |
| **Channel** | The user-facing interface. Web, Slack, Telegram, Website widget, API. Each has an adapter. |
| **CLARIFY** | The `clarify` tool. Renders a tabbed widget with up to 5 questions × 4 choices. Returns user selections (or `cancelled: true` after 30 min). |
| **Coordinator** | A session that spawns sub-agents. Any session can be a coordinator — the role is set by `config.coordinator: true`. |
| **Cursor** | The last fully-processed event ID for a session. On crash recovery, the new worker replays events after the cursor. |
| **Delivery Outbox** | PostgreSQL table acting as a durable queue for outbound messages. Channel adapters claim rows, send, mark delivered. Redis nudges are a latency optimisation. |
| **dstack** | The cloud-GPU provisioning library Surogate uses for 8 providers (AWS, Azure, GCP, RunPod, Modal, Nebius, OCI, Vast.ai). |
| **Event** | An immutable record in the session log. ~50 enum types. JSONB `data` column with documented per-type schemas. |
| **Expert** | A skill with `type: expert`. Backed by a model + endpoint. Base LLM delegates via `consult_expert`. |
| **Garage** | Lightweight S3-compatible object storage. One bucket per agent for workspaces; one per tenant for shared assets. |
| **Goal (`/goal`)** | Slash command that defines an outcome. Evaluator runs until `satisfied` / `failed` / `blocked` or 20 iterations. |
| **GovernanceGate** | The policy enforcement point. Wraps AGT's `PolicyEngine`. Frozen at session start. |
| **GRPO** | Group Relative Policy Optimisation. RL training method. RL Mode: Environment / Agent / RULER. |
| **Harness** | The agent loop in the worker. Replays events, calls LLM, dispatches tool calls. Stateless. |
| **Hub** | The lakeFS-backed repository browser. Every artifact (skill, KB, dataset, model, environment) is a versioned repo. |
| **Inbox** | Per-user queue of items needing attention. 5 kinds: input_required, action_required, task_complete, governance_gate, progress_checkin. |
| **lakeFS** | Open-source data versioning system. Backs the Hub. |
| **Lease** | Exclusive lock on a session in PostgreSQL. Default TTL 60s. Renewed every 3 iterations. Expires automatically on worker crash. |
| **MCP** | Model Context Protocol. Open standard for connecting LLMs to external tools. Surogate supports stdio + HTTP transport, OAuth 2.1 PKCE. |
| **MCP Proxy** | K8s service that injects credentials from the Vault as it forwards MCP calls. Sandboxes can only reach the proxy. |
| **Mission (`/mission`)** | Long-running, rubric-judged objective. LLM judge grades the workstream against the rubric. (Backend route exists; UI surface rolling out.) |
| **Modal** | A cloud-GPU provider with native Python deployment. Direct dependency. |
| **Org** | Organization. Top-level tenant boundary. Each org has its own Garage bucket, auth provider config, credential vault. |
| **Policy Profile** | Named bundle of governance rules that **narrows** the tenant's base policy for a sub-agent's child session. Composition is always tightening. |
| **Quality Flags** | Per-session tags: 👍, 👎, `policy.denied`, `harness.crash`, `saga.compensated`, `expert.override`, `expert.endorse`. |
| **Saga** | Tracked sequence of tool calls with automatic rollback. Filesystem checkpoints for builtin tools; declared undo for MCP tools. Sequential when active. |
| **Sandbox** | Per-session K8s pod where LLM-generated code runs. Session-scoped S3 only. No DB, no API token, no tenant storage. |
| **Service Account** | Org-scoped principal for non-interactive API channel clients. `surg_sk_...` token. Only valid on `/v1/api/*` routes. |
| **Session** | One conversation. Backed by append-only event log. Survives crashes. |
| **SFT** | Supervised Fine-Tuning. Most common training method. |
| **SKILL.md** | A skill file. YAML frontmatter + markdown body. `type: skill` (default) or `type: expert` for model-backed. |
| **Slug** | URL-safe name for an agent. Becomes `<slug>.cloud.surogate.ai`. Locked after deployment; use Rename button. |
| **SOUL.md** | The agent's persona file. Up to 20,000 characters. Tenant-wide, not per-user. |
| **SSE** | Server-Sent Events. The protocol the web SPA uses for real-time session updates. |
| **Sub-agent** | A declarative role preset (`AGENT.md`) that a coordinator can apply to a spawned child session. |
| **Surogates (runtime)** | The open-source agent runtime: harness, sessions, sandbox, MCP, governance. GPL-3.0. |
| **Surogate-ops (platform)** | The operator platform: REST API, web UI, billing, hub, training pipeline. AGPL-3.0. |
| **Tenant** | An org and its users. Tenant isolation enforced at every layer. |
| **TenantContext** | Runtime context that flows through every request via Python contextvars. Org ID + user ID + permissions + asset root. |
| **Tool** | A capability the agent can invoke. Worker-local, sandbox-bound, or MCP-proxied. |
| **ToolRouter** | Dispatches tool calls. Governance is checked before dispatch. |
| **v_session_tree** | SQL view exposing recursive parent/child relationships. Powers `GET /v1/sessions/{id}/tree` and the "Running" panel. |
| **v_skill_trajectories** | SQL view for successful skill invocations. Used by `collect_for_skill` to bootstrap experts. |
| **v_expert_outcomes** | SQL view for expert delegations with success/failure flag. Used by `collect_for_expert`. |
| **Vault** | Encrypted (Fernet) credential storage for MCP servers. Secrets never reach the sandbox. |
| **vLLM** | Open-source LLM serving engine. Common choice for hosting fine-tuned experts. |
| **Worker** | Stateless Python pod running the harness. Up to 50 concurrent sessions per worker. Auto-scales. |

## What's next

[Use cases](../use-cases.md) for end-to-end recipes. [Runtime architecture](./runtime-architecture.md) for the big picture.

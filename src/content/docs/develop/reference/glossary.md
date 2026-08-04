---
title: Glossary
---

Every Surogate term you'll encounter as a builder.

| Term | Definition |
|---|---|
| **ABAC** | Attribute-Based Access Control. Policy rules evaluating user / session / tool-arg attributes. Example: "allow `refund_user` only if `amount < 1000`". |
| **AGENT.md** | A sub-agent definition file. YAML frontmatter (`name`, `description`, `tools`, `disallowed_tools`, `model`, `max_iterations`, …) + body that becomes the spawned child's system prompt. |
| **Agent** | A deployed service at `<slug>.cloud.surogate.ai` bundling a model, skills, KBs, MCP servers, persona, and channels. |
| **API Channel** | Programmatic channel. `POST /v1/api/prompts` with a service-account `surg_sk_...` token. Read results off the SSE stream at `/v1/api/sessions/{id}/events` — the JSON `/events/poll` route has no `/v1/api/` alias. |
| **Approval-required tool** | A tool listed in the agent policy's `require_approval`. The call is blocked and raised as a `governance_gate` inbox item; approving grants that exact call for one hour and one use. An explicit denial is never approvable. |
| **Channel** | A user-facing interface — Web (always on), Slack, Telegram, Website widget, API. |
| **CLARIFY** | Legacy name for `ask_user_question`; the response event is `ask_user_question.response`. Renders a tabbed widget with up to 5 questions × 4 choices each; on web/Telegram a typed reply also answers it. 30-min wait cap. |
| **Coordinator** | A session that spawns sub-agents via `spawn_worker` / `delegate_task` / `spawn_task`. |
| **Event** | An immutable record in a session's log. See [Event types](/develop/reference/event-types/). |
| **Expert** | A `SKILL.md` with `type: expert`. Backed by a fine-tuned model + endpoint. The base LLM delegates via `consult_expert`. |
| **Goal (`/goal`)** | Slash command that defines an outcome. The platform's evaluator runs until `satisfied` / `failed` / `blocked` or 20 iterations are spent. |
| **GRPO** | Group Relative Policy Optimisation. RL training method. RL Mode: Environment / Agent / RULER. |
| **Hub** | Versioned (lakeFS-backed) repository browser for every artifact — skills, KBs, datasets, models, environments. Branches, commits, tags. |
| **Inbox** | Per-user queue of items the agent has explicitly raised. Five kinds: `input_required`, `action_required`, `task_complete`, `governance_gate`, `progress_checkin`. |
| **MCP** | Model Context Protocol. Open standard for connecting LLMs to external tools. Surogate supports stdio + HTTP transport, OAuth 2.1 PKCE. |
| **MCP Vault** | Encrypted credential storage. Secrets are injected by the MCP proxy and never reach the agent's sandbox. |
| **Quality flag** | Per-session tag: 👍, 👎, `policy.denied`, `harness.crash`, `saga.compensated`, `expert.override`, `expert.endorse`. Filterable on the Sessions list. |
| **Saga** | Multi-step rollback. When enabled, sequential state-changing tool calls are checkpointed (built-in tools) or undo-declared (MCP tools); failures compensate completed steps in reverse order. |
| **Service account** | Org-scoped principal for non-interactive API clients. `surg_sk_...` token, valid only on `/v1/api/*` routes. |
| **Session** | One conversation. Append-only event log. Durable across crashes. |
| **SFT** | Supervised Fine-Tuning. The default training method. |
| **SKILL.md** | A skill file — YAML frontmatter + markdown body. `type: skill` (prompt-based, default) or `type: expert` (model-backed). |
| **Slug** | URL-safe agent name. Becomes `<slug>.cloud.surogate.ai`. Locked after deployment; use the **Rename** button to change. |
| **SOUL.md** | An agent's persona — up to 20,000 characters. Tenant-wide, not per-user. Lives in CONFIG → SOUL.md. |
| **Sub-agent** | A declarative role preset (`AGENT.md`) that a coordinator applies when spawning a child session. The child inherits its parent's `agent_id` and therefore its governance policy verbatim; `tools` / `disallowed_tools` are what narrow it. See [How the runtime behaves](/develop/reference/runtime-architecture/). |
| **Tool** | A capability the agent can invoke. See [Tool catalog](/develop/reference/tool-catalog/). |

For platform-internal terms (harness loop, sandbox runtime, lease/cursor mechanics, the events table schema), see the [open-source `surogates` repo](https://github.com/invergent-ai/surogates) — they're not relevant to building on the platform.

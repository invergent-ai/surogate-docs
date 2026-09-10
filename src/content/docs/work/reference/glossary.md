---
title: Glossary
---

Every Surogate term you'll see in Work mode, in one place.

| Term | Definition |
|---|---|
| **AI disclosure** | The per-agent EU AI Act (Art. 50) notice telling end users they're talking to an AI — a web banner, or the first message on messaging channels. Levels: Basic / Enhanced / Full / None. |
| **Agent** | A deployed AI service with a URL like `<slug>.cloud.surogate.ai`. Bundles a model, skills, knowledge bases, MCP servers, persona, and channels. |
| **CLARIFY** | A built-in confirmation card the agent (or Copilot) shows before destructive or expensive operations. You click Yes or No. |
| **Allowance (per-user)** | The usage budget one end user draws from on one agent: a period grant (subscription tier, trial, or free-mode cap; resets on cycle) plus a top-up bucket (token packs; never expires). |
| **Browsing time** | Metered wall-clock minutes a buyer's agent browser may stay open. Distinct from the project's own web-browsing wallet. |
| **Buy page** | The hosted storefront at `/buy/<agent-slug>` where buyers sign in, purchase offers, and manage subscriptions. |
| **Buyer** | An end user who purchased access to a monetized agent. |
| **Channel** | The way users reach the agent — Web, Slack, Telegram, Website widget, API. Same agent, different doors. |
| **Channel identity** | A link between a platform-specific user (a Slack user, a Telegram user) and an internal Surogate user. Lets the same person on Slack and Web share sessions. |
| **Copilot** | The platform's built-in AI agent. Press ⌘+/ to open. Runs platform ops on your behalf. |
| **Default package** | The package applied to users with **no** active purchase — set from the Free trial / Per-user limit cards on the Monetize tab. |
| **Develop mode** | The Studio surface (`/studio/*`) — for builders. Adds Models, Compute, Hub, Datasets, Training, Evaluations. |
| **EVENTS tab** | The full ordered log of everything that happened in a session: user messages, LLM responses, tool calls, results, decisions. |
| **Entitlement** | What one buyer holds on one agent: subscription status, balances (usage, browsing, media), and their effective package across the subscription and pack planes. |
| **Free trial** | A one-time usage grant for new users of a monetized agent, advertised on the buy page. Never refills; a lapsed subscriber gets no second trial. |
| **Goal (`/goal`)** | A slash command that defines an outcome. The agent keeps working until an evaluator says satisfied / failed / blocked, or 20 iterations are used. |
| **Governance policy** | An agent's enforced guardrails: tool allow/deny, web & browser egress, and AI disclosure — checked before every tool call, on top of the always-on platform floor. |
| **Inbox** | A per-user queue of items the agent has pushed up for attention — `ask_user_question` prompts, action requests, completion notices. |
| **Knowledge base (KB)** | A curated corpus of documents the agent can browse at runtime via `kb_list_pages` / `kb_read_page`. Sources → Curator → Wiki. |
| **Loop (`/loop`)** | A slash command that schedules a prompt to run on a recurring basis (fixed or dynamic interval). |
| **MCP server** | An external system the agent can use as a tool — GitHub, Slack, your CRM, internal APIs. Follows the open Model Context Protocol. |
| **Media credits** | The prepaid media wallet, in dollars of provider spend for image/video generation. Also sellable to buyers on offers. |
| **Message (usage unit)** | ≈ 1,000 tokens — one question plus the agent's answer. The unit commerce surfaces display; storage stays token-denominated. |
| **Model tier** | Basic or Pro — which platform model class a buyer's package entitles them to. Strongest tier wins across planes. |
| **Offer** | A plan or pack you sell on one agent: price + usage + browsing time + media credits + a package. |
| **Opener (template)** | The one fixed, Meta-approved WhatsApp message a Program sends to start a check-in. The questions are not in it; they live in the Program's skill. |
| **Package** | What a purchase unlocks beyond usage: capabilities, channels, KBs, connected tools, skills, model tier. Snapshotted at purchase. |
| **Persona (SOUL.md)** | The agent's identity, tone, and rules. Up to 20,000 characters. Edited in the CONFIG tab. |
| **Platform floor** | The always-on, non-configurable governance layer: workspace path containment and path-argument hygiene. No agent policy can relax it. |
| **Pricing model** | How an agent charges: Free, Subscription, One-time packs, or Both. |
| **Program (check-in)** | A scheduled check-in: a skill, a cadence (weekdays and local times in a named zone), a WhatsApp sender, an approved opener and a roster of users. Activates only when every user is reachable. |
| **Quality flags** | Per-session tags: 👍 / 👎 (user feedback), `policy.denied`, `harness.crash`, `saga.compensated`, `expert.override`, `expert.endorse`. |
| **Session** | One conversation between a user and an agent. Records everything. Survives crashes. |
| **Skill** | A small markdown file telling the agent how to handle a specific kind of request. Reusable. |
| **Tool** | A capability the agent can invoke — `kb_read_page`, `web_search`, `read_file`, `terminal`, `browser_navigate`, etc. The agent decides which to use. |
| **User (per-agent)** | An end-user account on a specific agent. Different from your operator account. |
| **Vault** | Encrypted credential storage for MCP servers. Secrets never reach the agent's sandbox. |
| **Wallet** | A prepaid consumable balance (tokens, browsing minutes, compute credits, media credits): plan-granted portion resets monthly, top-ups roll over, operations stop at zero. |
| **Work mode** | The operator-facing surface (`/work/*`) — Agents, Sessions, Library. You're here. |

## What's next

[FAQ](/work/reference/faq/) for common questions.

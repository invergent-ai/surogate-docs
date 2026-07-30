---
title: Configure your agent
sidebar_position: 4
---

# Configure your agent

The **Configure** page — reached from an agent's left navigation (`/work/agents/{id}/settings?tab=...`) — is the core agent-building surface: twelve tabs that control who the agent is, what it can do, which model runs it, and where people reach it.

Each tab saves independently. Most tabs surface a **SAVE** button (which flashes a green **Saved** confirmation) or an amber **Unsaved changes** bar with **Save** / **Discard changes** when a field is dirty; a few toggles save the moment you flip them. Where noted, changes apply to **new sessions only** or reach live sessions on their next turn.

| Tab | What you set here |
|---|---|
| **Metrics** | Read-only dashboard: traffic, errors, tokens, deployment, connected resources |
| **Identity** | Name, slug, description, and the SOUL.md persona |
| **Capabilities** | Brainstorming gate, live browser, Saga, and the built-in slash commands |
| **Knowledge Bases** | Attach KBs the agent can search, in grounding or reference mode |
| **Skills** | Attach, write, import, and edit skills |
| **Tools** | Connect MCP servers, Composio toolkits, and manage the key vault |
| **Coding** | GitHub repos and coding-agent plans (only when `/code` is enabled) |
| **Model** | Serving model plus summary / vision / image / video role models |
| **Governance** | Policy enforcement, tool allow/deny, web & browser egress, SSH, EU AI Act AI disclosure |
| **Users** | End-users who can chat with this agent, and self-registration |
| **Channels** | Web, Slack, Telegram, and website-widget connections |
| **Monetize** | Charge for access via Stripe Connect (Pro plan) |

System agents (like the platform copilot) hide the **Identity**, **Capabilities**, and **Governance** tabs, and non-admins see a "managed by platform administrators" notice instead of the tabs. The **Coding** tab appears only when the agent's coding capability (`/code`) is turned on in **Capabilities**.

## Metrics

A read-only overview of the agent's health and footprint — no editable fields. It shows:

- **Key metrics** — Requests/sec, Error Rate, and Tokens (24h) as stat cards with sparklines, backed by the metrics API.
- **Deployment** (dedicated agents only) — replicas (current/desired), model, image, endpoint, and created time.
- **Connected** — a count of attached skills and MCP servers with skill-name chips.
- **Resources** — the agent's CPU and memory requests and limits.
- **Metric charts** — per-second request, error-rate, and token-throughput sparklines.

A **BYO model active** banner appears when the agent runs on your own model, noting that token traffic isn't billed by Surogate.

## Identity

Who the agent is. Two cards, each with its own **SAVE**.

**Basic info**

| Setting | What it does |
|---|---|
| **Name** | Display name shown on the agent card and in the UI |
| **Slug** | The URL/routing identifier. Locked by default — click **Rename** and confirm the dialog to change it, since renaming breaks channel routes, saved URLs, and integrations |
| **Description** | Shown on the agent card and injected into the system prompt |

**Soul (SOUL.md)** — the agent's full persona (tone, rules, what it can and can't do), injected into every session's system prompt. A character counter caps it at **20,000** characters, and a **SoulAnatomyGuide** can drop in a starter template. Changes apply to new sessions only — in-progress sessions keep the old persona.

## Capabilities

Toggle the agent's built-in behaviors. The Brainstorming gate, Live browser, and slash-command switches save the moment you flip them; the Saga card collects its toggle and number fields behind its own **Save** button. Changes reach live sessions on their next turn.

| Capability | What it does |
|---|---|
| **Brainstorming gate** | Forces a short design/brainstorm pass with the user before creative or implementation work. Turn off for an agent that should act immediately |
| **Live browser support** | Lets the agent drive a real browser (navigate, click, type, screenshot). Off removes the browser tools |
| **Saga** | Tracks multi-step tool chains and rolls back completed steps when a later step fails. Exposes **Step timeout (s)**, **Max retries**, and **Retry delay (s)** |

**Slash commands** — a master switch turns all built-in chat commands on or off at once, with individual toggles below:

| Command | What it enables |
|---|---|
| `/compress` | Users manually compress the conversation to free up context |
| `/code` | The coding-agent commands (Claude Code / Codex on the workspace); also reveals the **Coding** tab |
| `/deep-research` | A planner + writer sub-agent that produces a cited markdown report |
| `/auto-research` | An autonomous optimization run (Arbor) over a hypothesis tree |
| `/loop` | Scheduled recurring runs on an interval or self-paced |
| `/mission` | Rubric-judged task orchestration that decomposes an objective |
| `/goal` | A session goal the agent works toward across turns |

## Knowledge Bases

Attach the knowledge bases this agent can search. The header reads **Attach a knowledge base**; from here you can **Create a knowledge base**, **Browse Library** to attach existing ones, or **Detach** attached KBs.

Each attached KB row shows its name, page count, compile status (active / compiling / queued / error), and a **mode** selector:

| Mode | What it does |
|---|---|
| **Grounding** | The KB is treated as authoritative source material for answers |
| **Reference** | The KB is available for lookup but not treated as ground truth |

The **Browse Library** view offers search and multi-select cards; **Attach selected (n)** pulls them in.

## Skills

Attach reusable skills to the agent. The header reads **Attach a skill** with an **Add skill** button. Attached skills list their name and origin (e.g. "Your copy · from template"), an optional **expert** badge, and **Edit** / **Detach** actions.

Adding a skill offers three routes: **Start from a template** (recommended, with a searchable category-filtered browser), **Write from scratch**, or **Import a file** (`.md` / `.zip` drag-and-drop). The scratch and edit forms expose **Name** (slug), **Display name**, **Description**, **Trigger** (comma-separated keywords), **Tags**, an **Is Expert** switch, and the **Content (SKILL.md)** body. **Browse Library** attaches skills you already have.

See [Skills](../library/skills.md) for authoring guidance.

## Tools

Connect external systems (Slack, Stripe, your own APIs) as MCP servers. The heading is **Tools**, with a **Key vault** button for stored credentials. Connected tools list their name, status, and **Manage** / **Disconnect** actions; Composio toolkits add a per-agent OAuth **Connect** control.

Three ways to add a tool:

- **From your Library** — attach an MCP server you already registered.
- **Toolkits** — attach from the searchable Composio catalog.
- **Add an MCP server** (recommended) — the **AddServerForm**: **Name**, **What it does**, and a **Connection type** of *Remote endpoint (HTTP)* (adds **Web address (URL)**, an **API key / OAuth** sign-in choice, and **API key**) or *Local command (stdio)* (adds **Command** and **Environment** KEY=value pairs), plus a **Timeout (seconds)**.

The **Key vault** stores API keys (masked, with **Update** and **Remove**). See [MCP servers](../library/mcp-servers.md).

## Coding

Only visible when the agent's coding capability (`/code`) is enabled in **Capabilities**. Two sections:

- **Repositories** — agent-scoped GitHub repositories the coding agents can work in.
- **Coding agents** — agent-owned Claude Code / Codex plans connected under the agent's own service account.

## Model

Choose which models power the agent. Every chooser except the serving model defaults to **Platform default**; dirty fields glow amber, and a single **SAVE** commits the tab.

| Setting | What it does |
|---|---|
| **Serving model** | The primary model the agent runs on (platform default is labelled "Surogate") |
| **Summary model** | Used for session titles and context compression |
| **Vision model** | Used for image understanding |
| **Image model** | Used by the `generate_image` tool |
| **Video model** | Used by the `generate_video` tool |

## Governance

The agent's guardrails — and they are **enforced**: the composed policy is checked before every tool call the agent makes. An **Unsaved changes** bar collects edits across the cards and clears on a successful save ("Governance settings saved."). Edits reach live sessions on their **next wake** — no redeploy needed.

- **Policy enforcement** — the master switch. When off, the agent's own rules below are dropped, but the platform floor (workspace path containment, path-argument hygiene) still applies, and AI disclosure falls back to the deployment-wide default rather than turning off.
- **Tool access** — **Allowed tools** and **Denied tools** multi-selects, grouped by the built-in tool catalog. Empty "Allowed" means all built-in tools are allowed; the two lists are mutually exclusive, and unknown tool names are rejected on save. MCP tools are **not** governed here — restrict them by detaching the MCP server. A denied tool is still visible to the model and blocked at call time: expect the agent to try, get `Blocked: <reason>`, and report it. The coordination self-tools (`worker_*`, board tools, `unblock_task` / `cancel_task`) are deliberately not offered — denying them would strand blocked work.
- **Web & browser egress** — a **Default action** of *Allow* or *Deny*, plus a rules table. Each **Add rule** row sets a **Domain** (glob patterns like `*.acme.com` work; CIDR ranges don't), **Ports**, **Proto** (tcp/udp), and **Action** (allow/deny). Scope: this governs the URLs the web-fetch and browser tools may open (`web_extract`, `browser_navigate`). It does **not** restrict `web_search` (a search query is not a URL), the terminal, coding agents, or MCP servers — restrict those by denying the tool or detaching the server. See [Governance & AI disclosure](./governance.md) for the full network-controls picture.
- **SSH** — agent-owned SSH keys and remote targets (which hosts the agent can reach and under what credentials). Independent of the policy toggle.
- **EU AI Act transparency** — an **AI disclosure** toggle ("Tell end-users they are talking to an AI. Art. 50 of the EU AI Act requires this from 2 Aug 2026 on every channel.") and a **Disclosure level**: **Basic** (short AI notice before the first interaction), **Enhanced** (adds a capability and limitation summary), **Full** (complete Art. 50 disclosure with legal references), or **None** (no disclosure text — not compliant for end-user chat). How each channel delivers the disclosure is covered in [Governance & AI disclosure](./governance.md).

A denial is returned to the model as a tool error and recorded as a `policy.denied` event, visible per session under **Sessions → POLICIES**.

## Users

Manage the people who can chat with this agent — separate from your Surogate team. A **Let anyone sign up** toggle controls self-registration (available only when the project has Firebase auth configured and is on a paid plan).

A searchable list shows each user's email and auth provider (Email & password / Google / GitHub), with **Edit** and **Delete** row actions. **Add user** opens a form with **Email**, an optional **Display name**, and an optional **Password** (leave empty for SSO). See [Users](../channels/users.md) and [Self-registration](../channels/self-registration.md).

## Channels

Connect the agent to where your people already work. Each channel card shows an **Active** / **Off** status and a **Connect** or **Manage** button.

- **Web** — the always-on hosted chat page; copy its endpoint URL once the agent is deployed. See [Web](../channels/web.md).
- **Slack** — a guided **Connect Slack** wizard (bot scopes, event subscriptions, signing secret, bot token). The **Manage** view auto-saves options: **Require @mention**, **Mode** (Team member / Personal assistant), **Allow Bots** (None / Mentions only / All), **Reply in thread**, **Reply broadcast**, **Free-response channels**, plus **Surogate Mate** follow-the-channel and ambient-mode toggles. See [Slack](../channels/slack.md).
- **Telegram** — a **Connect Telegram** wizard (BotFather token). **Manage** options: **Require @mention**, **Mode**, **Reply Threading** (First chunk only / All chunks / Off), **Message Reactions**, and **Per-User Group Chats**. See [Telegram](../channels/telegram.md).
- **Website** — an embeddable chat bubble. Set **Allowed origins**, copy the **Embed code**, cap **Messages per chat**, and reveal the **Publishable key** under Advanced. See [Website widget](../channels/website-widget.md).

## Monetize

Charge people for access to this agent. Requires the **Pro** plan (lower tiers see an **Upgrade to Pro** gate).

Connect billing via **Stripe Connect** (status pill: Not connected / Onboarding / Active / Restricted / Disconnected), then pick a **Mode**: **Free**, **Subscription**, **Token packs**, or **Both**. Under **Offers** you add plans — a **Name**, **Price USD**, **Tokens included**, and (for subscriptions) a monthly/yearly **Interval**. To change a price, deactivate the offer and add a new one. See the [Monetize](../monetize.md) guide.

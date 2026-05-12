---
title: Skills & Tools
sidebar_position: 3
slug: /features/skills
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Skills & Tools

Two related concepts live under one page:

- **Skills** — functions or workflows defined inside Surogate. The Skill Builder is the visual editor. Skills live in your project, version on save, and ship to the Hub when published.
- **MCP Servers** — external services that speak [Model Context Protocol](https://modelcontextprotocol.io). Surogate doesn't host them; it routes tool calls to the URL you register.

The page header switches between them with two tabs: **Skills** and **MCP Servers**.

## When to choose which

| You have… | Use |
|---|---|
| A specific function ("look up customer by ID", "create a Jira ticket") | Skill |
| A microservice that already speaks MCP | MCP Server |
| A bundle of tools from a vendor that publishes an MCP endpoint | MCP Server |
| A multi-step workflow with branching | Skill (it's easier to read in the editor) |

## Page layout

Common across both tabs:

- **Filter skills…** input. Case-insensitive substring match, scoped to the active tab.
- Tab strip: `Skills · MCP Servers`. Counts in the tab labels (e.g. `MCP Servers 0`).
- Two header actions: **Import skill** (opens the Templates library) and **New Skill** (opens the builder).

The **MCP Servers** tab replaces these with two actions: **Vault** (manage stored MCP credentials) and **Add Server** (register a new MCP endpoint).

## Skill model

Backend field set (`surogate_ops/core/db/models/`): name, description, kind, version, schema (typed I/O), implementation, status. Editing a skill creates a new version row; older versions stay so deployed agents keep working until you re-deploy them.

## Templates library

The **Import skill** action opens the Templates library (header `H2: Templates`). The left rail groups templates by category. The current snapshot ships **72 templates** across 17 categories:

| Category | Count |
|---|---|
| autonomous-ai-agents | 2 |
| blockchain | 2 |
| communication | 1 |
| creative | 5 |
| devops | 3 |
| dogfood | 1 |
| email | 1 |
| finance | 7 |
| health | 2 |
| mcp | 2 |
| migration | 1 |
| mlops | 25 |
| productivity | 7 |
| research | 9 |
| security | 3 |
| web-development | 1 |

(`All categories 72` is the top selector that shows everything.) A **Search templates…** input filters across the full set. Each card carries the template's short description and tags. Picking a card opens the builder with the template's body pre-filled.

## New Skill flow

The **New Skill** action opens the Skill Builder inline (not as a modal — the page switches to the editor). The form has five top-level fields and a markdown body editor below them.

| Field | Type | Notes |
|---|---|---|
| **Name** | text | The internal id. URL-safe. Used in references from agent configs. |
| **Display Name** | text | Shown in lists and agent settings. |
| **Description** | textarea | What the skill does, in one or two lines. Agents read this to decide when to call. Precision pays off here. |
| **Trigger** | text | Optional. Natural-language hint for when an agent should invoke this skill (`when the user asks about pricing`). |
| **Tags** | text | Space-separated. Used by the filter on the Skills list and to group skills in agent settings. |

The body editor is a full markdown editor with the standard formatting shortcuts (`Ctrl+B` bold, `Ctrl+I` italic). It carries the implementation — depending on the kind the skill is, this is a prompt template, a script, or a tool-call definition.

Cancel the form with the **✕** button in the top-right of the editor; the skill is not created until you save.

## Import flow

1. Open `/studio/skills`.
2. Click **Import skill**. The Templates library opens.
3. Browse by category (left rail) or search by name (top input).
4. Pick a template card. The Skill Builder opens with the template pre-filled. Edit name / display name / description if needed, then save.

The skill arrives as a new entry pinned to the version current at import time. To bring in a skill from outside the Templates library (e.g. a `.skill` bundle), use the Data Hub: push the bundle to a `Skill`-kind Hub repo, then import from there.

## MCP Server flow

1. Switch to the **MCP Servers** tab at `/studio/skills/mcp`.
2. Click **Add Server**. (The companion **Vault** action lists stored MCP credentials.)
3. Provide the server's **Endpoint URL** and any auth — credential reference, headers, or a token from the Vault.
4. Save. The server's tools become available in the multi-select on agent settings.

## Versions and pinning

Agents pin to a Skill version at deploy time. Saving a Skill bumps its version row but does not propagate to deployed agents. To push an update:

1. Save the new version.
2. Open each affected agent's settings (`/studio/agents/<id>` → Settings).
3. Re-pick the skill (the dropdown now shows the new version).
4. Re-deploy the agent.

The agent's running sessions complete on the old version. New sessions start on the new one.

## Permissions

| Action | Role |
|---|---|
| List, read | Project `viewer` and above |
| New Skill / Import / Edit / Delete | Project `editor` or `owner`, **or** system `skill_author` |
| New MCP Server / Edit / Delete | Project `editor` or `owner` (TODO(verify whether `skill_author` covers MCP)) |

## Troubleshooting

- **Agent fails after a skill edit.** The agent is pinned to the previous version. Re-deploy the agent to pick up the new one.
- **MCP server timing out.** Open a session that calls it and read the Trajectory tab — the timeout shows there with the offending URL.
- **Skill compiles but the schema rejects inputs.** Re-check the typed schema; common mistake is `string` where the agent sends a number.

## Related

- [Workflow — Add a skill](../workflows/add-a-skill)
- [Agents](./agents)
- [Data Hub](./hub) — Skills publish there.

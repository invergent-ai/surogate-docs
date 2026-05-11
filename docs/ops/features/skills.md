---
title: Skills & Tools
sidebar_position: 3
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

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

- **Filter skills…** input (case-insensitive substring match — search applies only to the active tab).
- Tab strip: `Skills · MCP Servers`. Counts in the tab labels (e.g. `MCP Servers 0`).
- Two header actions: **Import skill** (from the Hub or a file) and **New Skill** (open the builder).

The MCP Servers tab adds a **+ Add MCP Server** action in place of New Skill. TODO(verify the exact label).

## Skill model

Backend field set (`surogate_ops/core/db/models/`): name, description, kind, version, schema (typed I/O), implementation, status. Editing a skill creates a new version row; older versions stay so deployed agents keep working until you re-deploy them.

Skill templates ship inside the codebase at `surogate_ops/core/skills/templates/`. Visible templates include `web-development/page-agent`. TODO(verify the full template list visible in the picker).

## New Skill flow

1. Open `/studio/skills`.
2. Click **New Skill**.
3. _TODO(verify)_ — pick a starter template or "Blank".
4. Provide **name**, **description**, and the typed **inputs**/**outputs** schema.
5. Implement the body. Templates fill this with a working scaffold.
6. Save & publish.

## Import flow

1. Open `/studio/skills`.
2. Click **Import skill**.
3. Paste a Hub repo URL, or upload a `.skill` bundle. TODO(verify the exact source types).
4. The skill arrives as a new entry pinned to the version that was current at import time.

## MCP Server flow

1. Switch to the **MCP Servers** tab.
2. Click **+ Add MCP Server**.
3. Provide **Endpoint URL** and (if the server requires auth) **Auth mode** + a **Credential** reference.
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

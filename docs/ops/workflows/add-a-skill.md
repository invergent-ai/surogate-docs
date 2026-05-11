---
title: Add a skill
sidebar_position: 5
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Workflow — Add a skill (or MCP server)

<video controls width="720" muted>
  <source src="/videos/07-skills-and-mcp.webm" type="video/webm" />
</video>

## Goal

Make a new capability available to agents — either as a Skill (a function or workflow defined in Surogate's Skill Builder) or as an MCP server (an external Model Context Protocol endpoint).

## Decide: Skill or MCP server?

| You have… | Use |
|---|---|
| A clear, narrow function ("look up customer by ID") | **Skill** — fast to write, type-safe, lives in your project. |
| A whole bundle of tools from an existing system (filesystem, database, vendor MCP) | **MCP Server** — connect once, expose many tools. |
| A function that already exists as a microservice | Either. MCP is faster if the service already speaks MCP. |

## Steps — New Skill

1. Switch to **Develop** and open **/studio/skills**.
2. Click **New Skill** (top-right) — or **Import skill** to bring one in from the Hub.
3. _TODO(verify) — pick a starter template (e.g. `web-development/page-agent`)._
4. Name the Skill and add a precise **Description** (agents use it to decide when to call).
5. Define **Inputs** and **Outputs** via the typed schema editor.
6. Implement the body in the visual editor.
7. Save & publish.

## Steps — Connect an MCP server

1. Open **/studio/skills/mcp**.
2. Click **+ Add MCP Server**. _TODO(verify label._
3. Enter the **Endpoint URL** and any **Auth** + **Credential**.
4. Save. The server's tools appear in the agent settings as a multi-select.

## Attach to an agent

1. Open the agent.
2. In Settings, pick the Skill or MCP server.
3. Save. Agents pin to the version available at save time.

## Gotchas

- Agents **pin to a Skill version**. Editing a Skill won't change deployed agents — redeploy them or bump the agent's pinned version.
- The **Filter skills…** input is per-tab. To search MCP servers, switch to the MCP tab first.
- A failing MCP server doesn't usually crash the agent — calls just timeout and the agent recovers, but the session trajectory will show the failure.

## Related

- [Skills & Tools](../features/skills)
- [Agents](../features/agents)
- [Data Hub](../features/hub) — publishing a Skill for reuse.

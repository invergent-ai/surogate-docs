---
title: Work with coding agents
description: Give a coding agent such as Claude Code the portal's tools and skills, with access to how the portal is built and never to its people.
---

A coding agent can build a customer's portal the way a developer does: it composes pages, builds apps, checks its work and hands over a pull request. The portal gives it three things:
- **skills** that teach it how;
- **an MCP server** to look at the portal;
- **an identity** that sees how the portal is built, but never its people.

## Install the skills

```sh
portal skills install
```

This puts three skills in `.claude/skills`, where Claude Code finds them:

| Skill | What it teaches |
| --- | --- |
| `build-a-portal-app` | starting from a working app, the manifest, checking what the portal sends, web components, events, hooks and types |
| `compose-a-page` | the config files: sites, pages, layouts, placements, preferences, and who may view or edit |
| `check-your-work` | `portal check` from the files to rendered pages, the loop until it passes, and the report for the pull request |

Each skill names the version of the developer kit it is for, and its examples are tested against that version. An agent never learns a contract the portal no longer keeps. Run the command again after updating the kit; `--force` replaces the skills already there.

## Give the agent an identity

Make a [service account](/portal/console/service-accounts/) for the agent, with the **Administrator** role and a token that has only the **Read how the portal is built** scope:
- With it, the agent sees the sites, pages, apps, events, and the names of groups and organizations. People named in a page's permissions are only counted.
- It never sees people, members, sessions, preferences or the audit log, and changes nothing.
- Reading the sync history or failed event deliveries needs **Read users, groups and settings** too, and the audit log **Read the audit log**. Each of those shows people, so add them only if the agent needs them.
- To make [previews](/portal/sites/previews/) of its changes, add **Make preview environments**. Previews hold only fake people, so this scope reads no one either.

## Connect the MCP server

`portal mcp` serves the portal's tools to the agent. Register it with Claude Code in your project's `.mcp.json`. Give the server the portal's address and the agent's token in its environment, as the `check-your-work` skill's example shows:

```json
{ "mcpServers": { "portal": { "command": "portal", "args": ["mcp"] } } }
```

| Tool | What the agent gets |
| --- | --- |
| `list_sites` | the sites, their addresses and languages, their pages with layouts, who may view them (people only counted) and what they place; the apps |
| `org_hierarchy` | the organization tree and the groups, by name, with how many people each holds |
| `app_manifest` | an app's manifest, as the portal took it |
| `wireable_events` | the events apps send, and which can be wired to which receivers |
| `read_logs` | the latest syncs and their problems, failed event deliveries, or the audit log |
| `check` | `portal check` on a config folder, with its problems |
| `screenshot` | a picture of a page, as a visitor or signed in as a person |

A tool that cannot answer says why, and which scope its token lacks. The screenshot tool only ever opens the portal's own pages, at the addresses its sites are routed at. The `check` tool reads only folders inside the project the agent works in.

## The loop

The agent reads the skills and looks at the portal with `list_sites` and `app_manifest`. It changes the files or the app, then runs [`portal check`](/portal/sites/check-a-site/) until it passes, on a [local portal](/portal/sites/develop-locally/) with `--render`. It shows the change on a [preview](/portal/sites/previews/), with screenshots as the people who see it, and hands over a pull request with the check's report. A person reviews it, and the change reaches the portal only when it is merged and synced.

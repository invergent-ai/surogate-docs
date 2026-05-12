---
title: Work vs Develop perspectives
sidebar_position: 1
slug: /concepts/work-vs-develop
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Work vs Develop perspectives

Surogate Ops presents two surfaces over one account. The choice is a single field on your user record (`User.perspective`) and a single button in the top bar.

| | Work | Develop (Studio) |
|---|---|---|
| URL prefix | `/work/*` | `/studio/*` |
| Default for | New sign-ups (server default) | Users who switch via the top-bar toggle |
| Sidebar | 4 entries: Agents, Sessions, Skills & Tools, Knowledge Bases | 10 entries across OPERATE, LIBRARY, TRAIN groups |
| Top chrome | Page chrome only; navbar hidden on Work routes | Full Studio navbar |
| Primary task | Run agents someone deployed | Build, deploy, observe agents |
| Settings | `/work/settings` keeps the Work sidebar | `/studio/settings` keeps the Studio sidebar |

## What the toggle does

The **WORK / DEVELOP** buttons sit at the top-right of every Studio page (Work pages hide their top navbar). Clicking the inactive perspective:

1. Posts to `PATCH /api/me` to update `User.perspective`.
2. Navigates to the other home (`/work` or `/studio`).
3. Subsequent sign-ins on this account land on the new home (via `/` → `getPostAuthRoute(perspective)`).

## Resources that are visible in both modes

| Resource | Where in Work | Where in Develop |
|---|---|---|
| Skills | `/work/skills` (read + use) | `/studio/skills` (read + create + edit) |
| MCP Servers | `/work/skills/mcp` | `/studio/skills/mcp` |
| Knowledge Bases | `/work/knowledge-bases` (read) | `/studio/knowledge-bases` (full lifecycle) |
| Profile | `/work/settings` | `/studio/settings` (same form) |
| Hub config | `/work/settings/hub` | `/studio/settings/hub` |
| Notifications prefs | `/work/settings/notifications` | `/studio/settings/notifications` |

The shared pages render the same component; the surrounding navbar is what changes.

## Sessions cross-pollinate

A chat started in `/work/agents/<id>/chat` produces a Session that's visible to builders at `/studio/sessions?agentId=<id>` with the agent's full **Trajectory** (reasoning + tool calls). That's the main loop for triaging an agent failure: end user reports a bad answer → builder opens the session in Studio → trajectory tab reveals the broken Skill call or off-spec response.

## Why two surfaces?

End users running an agent don't need to see Datasets, Training, or Compute. Builders need them in their default layout. Splitting the surfaces keeps the navbar focused without hiding features behind toggles.

## Onboarding and the redirect rule

`/` redirects after sign-in based on `User.perspective`:

- `work` → `/work`
- `develop` → `/studio`

A new user with the `agentOnboardingDone` localStorage flag unset, hitting `/work` or `/studio` (index), is bounced to `/onboarding`. The flag persists per browser, not per server. Clearing site storage replays the welcome.

## Related

- [Core objects](./core-objects)
- [Lifecycle](./lifecycle)
- [Where to find things](../getting-started/where-to-find-things)

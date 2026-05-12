---
title: Where to find things
sidebar_position: 4
slug: /getting-started/where-to-find-things
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Where to find things

A flat route map for the whole app. Internal routes (auth flow) are listed last.

## Work mode

| You want to… | Go to |
|---|---|
| See your dashboard / list your agents | `/work` |
| Browse the templates catalogue | `/work/templates` |
| See all your chat sessions across agents | `/work/sessions` |
| Open a specific agent | `/work/agents/<agent-id>` |
| Start a new chat with an agent | `/work/agents/<agent-id>/chat` |
| Resume a specific chat session | `/work/agents/<agent-id>/chat/<session-id>` |
| Edit an agent's settings | `/work/agents/<agent-id>/settings` |
| See available Skills & MCP servers | `/work/skills` · `/work/skills/mcp` |
| Manage knowledge bases attached to your agents | `/work/knowledge-bases` |
| Profile + password | `/work/settings` |
| Data Hub connection | `/work/settings/hub` |
| Notification preferences | `/work/settings/notifications` |

## Develop mode (Studio)

| You want to… | Go to |
|---|---|
| The Studio overview | `/studio` |
| List / deploy agents | `/studio/agents` |
| Open a single agent | `/studio/agents/<agent-id>` _TODO(verify)_ |
| Sessions across all agents | `/studio/sessions` (filter with `?agentId=…&sessionId=…`) |
| See live metrics for your agents | `/studio/monitoring` |
| Manage Models | `/studio/models` (deep-link with `?modelId=…`) |
| Manage Skills | `/studio/skills` |
| Manage MCP Servers | `/studio/skills/mcp` |
| Manage Knowledge Bases | `/studio/knowledge-bases` |
| The Data Hub | `/studio/hub` (open a repo at `/studio/hub/<namespace>/<repo>`) |
| Datasets | `/studio/datasets` |
| Training runs / experiments | `/studio/training` (deep-link with `?runId=…`) |
| Evaluations, benchmark suites, leaderboards | `/studio/evaluations` |
| Arenas (A/B and experiment runs) | `/studio/arenas` and `/studio/arenas/<arena-id>` |
| Playground for an LLM | `/studio/playground` (deep-link with `?modelId=…`) |
| Compute — cloud backends list | `/studio/compute/cloud` |
| Compute — running / queued workloads | `/studio/compute/workload-queue` (filter with `?filter=…&id=…`) |
| Compute — allocation policies | `/studio/compute/policies` |
| Connect a new cloud account | `/studio/connect-cloud?provider=<name>` where `<name>` ∈ {`aws`, `azure`, `gcp`, `runpod`, `oci`, `nebius`, `vastai`, `modal`} |
| Look up GPU offers for a backend | `/studio/backend-offers?backend=<name>` |
| Your profile | `/studio/settings` |
| Projects & team members (admin) | `/studio/settings/projects` |
| Hub connection | `/studio/settings/hub` |
| Third-party integrations (admin) | `/studio/settings/integrations` |
| Notification preferences (admin) | `/studio/settings/notifications` |

## Auth flow

| You want to… | Go to |
|---|---|
| Sign in | `/login` |
| Welcome (first run) | `/onboarding` |
| Finish a Firebase/Google/GitHub signup | `/complete-signup` |
| Reset / change a temporary password | `/change-password` |

## Internal redirects (you usually don't visit these directly)

- `/` → `/onboarding` if the welcome flow hasn't been completed; otherwise → `/work` or `/studio` depending on your `perspective`.
- `/studio` (index) → `/onboarding` if you haven't completed the welcome AND have zero agents.
- `/studio/compute` (index) → `/studio/compute/cloud`.
- `/login` after sign-in → `/`, which then redirects per the rule above.

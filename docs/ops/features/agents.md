---
title: Agents
sidebar_position: 1
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Agents

An Agent is a deployed conversational workflow that pairs a Model with a fixed set of Skills, MCP servers, and Knowledge Bases. It exposes a chat surface in Work mode and (optionally) an API surface through the `sk-agent-*` proxy.

## Where it lives

| URL | Audience |
|---|---|
| `/work` | Operators. Card grid of agents you can run. |
| `/work/agents/<id>` | Operator agent detail. Tabs: Overview, Chat, Settings. |
| `/work/agents/<id>/chat/<sessionId>` | Resume an earlier session. |
| `/studio/agents` | Builders. Full list with status filters and Deploy Agent. |
| `/studio/agents/<id>` | Builder agent detail (TODO(verify) — not reachable without an agent on the test account). |

## The Studio list

![Agents list with annotations](../assets/screenshots/agents/list-annotated.png)

1. **Agents** header.
2. **Status filter pills**: `All · Running · Deploying · Error`. Each pill has its own count badge. Clicking a non-active pill applies the filter without leaving the page.
3. **Filter agents…** input. Full-text search by agent name. Case-insensitive.
4. **Deploy Agent** button (top-right). Opens the deploy dialog covered below.

The empty state ("No agents") is reached when you've never deployed one. The dashboard at `/studio` will redirect you to `/onboarding` until either the welcome flow is acknowledged or at least one agent exists.

## Deploy flow

The Deploy Agent dialog walks four sections. The video in [Workflow → Deploy an agent](../workflows/deploy-an-agent) shows them in order.

| Section | Required | Notes |
|---|---|---|
| Name | Yes | Becomes the agent's display label across `/work`, `/studio`, and Monitoring. |
| Model | Yes | Pulled from `/studio/models`. Only Models in **Serving** state are useful. |
| Skills + MCP servers | No | Multi-select. Agent pins to the version available at deploy time. |
| Knowledge Bases | No | Multi-select. KBs in **Compiling** or **Error** state can be attached but won't return retrieval results. |
| System prompt | Depends on template | Most templates pre-fill it. |
| Greeting | No | First message shown to end users. Defaults to "How can I help?" if blank. TODO(verify). |
| Channels | No | Per-channel configs (web chat, API). TODO(verify the panel structure). |

Once you click the final **Deploy** action, the agent appears in the **Deploying** filter and moves to **Running** after the serving container is healthy. The first deploy of a given Model can take several minutes; subsequent deploys reuse cached layers.

## Status reference

| Status | What it means | Common cause |
|---|---|---|
| Deploying | Serving container being built or started. | Normal during a first-time deploy. |
| Running | Healthy and accepting traffic. | — |
| Error | The serving container or model is unhealthy. | Underlying Model in Error or Stopped, or a Skill failed to load. |
| Stopped | You manually stopped it. | Agent stays in the list but won't serve. TODO(verify the exact stop control). |

## Reading an agent's runtime

From a deployed agent you can:

- See its **live metrics** at `/studio/monitoring` (RPS, P50/P95/P99, errors, CPU/MEM per agent).
- Browse its **sessions** at `/studio/sessions?agentId=<id>`. Each session has a **Thread** view (messages) and a **Trajectory** view (reasoning + tool calls).
- Run an **evaluation** against it from `/studio/evaluations` → **New Evaluation**.

## API surface

Agents are reachable through the Surogate proxy when their Model has an `sk-agent-*` API key. The key authorizes calls scoped to `model:<model_id>`, not `agent:<id>`. Multiple agents that share a Model share the same key.

Failed auth (401/403) on the proxy hot path is negative-cached for a short interval to protect the upstream — fixing a wrong key takes effect after the cache clears or on a key change.

## Deletion

Deleting an agent stops it from serving and removes it from `/work` and `/studio/agents`. Sessions it produced remain at `/studio/sessions` in read-only form. The agent's row drops out of Monitoring on the next refresh. TODO(verify whether deletion is hard or soft).

## Permissions

| Action | Project role |
|---|---|
| List, open, chat with an agent | `viewer` and above |
| Deploy / edit / stop / delete | `editor` or `owner` (TODO(verify)) |

System role `admin` overrides project-level limits. See [Reference → Permissions matrix](../reference/permissions-matrix).

## Related

- [Workflow — Deploy an agent](../workflows/deploy-an-agent)
- [Models](./models)
- [Skills & Tools](./skills)
- [Knowledge Bases](./knowledge-bases)
- [Monitoring](./monitoring)
- [Sessions](./sessions)

---
title: Templates
sidebar_position: 3
---

# Templates

The Templates page lists prebuilt agents you can deploy with one click. Useful starting points; you'll customise from here.

## The seven templates

| Template | What it does | Pre-attached |
|---|---|---|
| **Customer Support Bot** | Answers customer questions from a KB | `web_search`, `kb_*`, `clarify`, `create_artifact` |
| **Incident Responder** | Triage incidents, summarize alerts, write runbooks | `read_file`, `web_search`, `terminal` |
| **Content Writer** | Drafts, editing, headlines | `read_file`, `write_file`, `web_search`, `vision_analyze` |
| **Data Analyst** | Reads CSVs, makes charts, answers analytics | All read + `execute_code`, `create_artifact` |
| **Code Reviewer** | Reviews code diffs for bugs and security | `read_file`, `search_files`, `list_files`, `web_search` |
| **Sentiment Tagger** | Classifies text sentiment | `create_artifact` |
| **Empty agent** | From scratch — pick your own model, skills, MCPs, prompt | (Nothing) |

## Deploying a template

1. Click a template card → **DEPLOY NEW AGENT** opens.
2. The form is pre-filled with sensible defaults:
   - **Name** — change to something specific (`acme-support-bot`)
   - **Slug** — auto-derived from name, used in the URL
   - **Description** — short summary
   - **Model** — default platform model (you can switch later)
   - **Channels** — Web on by default
3. Click DEPLOY.

Agent goes through `deploying` → `running` in 10-90 seconds.

> 🚧 Known issue: the Data Analyst template sometimes gets stuck in `deploying`. Force-restart via STOP → START.

## After deploy — what to customise

| Step | Where |
|---|---|
| Update SOUL.md | CONFIG → SOUL.md |
| Attach a KB | KNOWLEDGE & TOOLS tab |
| Attach MCP server | KNOWLEDGE & TOOLS tab |
| Adjust tool allowlist | CONFIG → Tool Access |
| Enable Slack | CHANNELS → Slack |
| Adjust scale | SCALE button |
| Enable governance | CONFIG → Governance |

## Why templates?

Templates make the agent's first session work without configuration. After that, every iteration is incremental.

You'll often clone a template for testing — deploy `data-analyst-test` from the template, mess with it, prove the change works, then apply to the production agent.

## Custom templates

The ADD SKILL → Templates panel is for a future per-tenant template library — you'll register your own templates here. Currently the catalog is empty in current builds.

## Empty agent

The "Empty agent" template gives you a deployed agent with nothing attached. Useful for:

- Testing the platform itself (does my agent deploy?)
- Building from scratch when no template fits
- Trying out new models without inheriting any defaults

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/templates` | List templates |
| `GET` | `/v1/templates/{id}` | Template detail |
| `POST` | `/v1/templates/{id}/deploy` | Deploy this template; same effect as DEPLOY NEW AGENT |

## What's next

Back to [Build phase](../loop/build.md) for the deploy flow. Or [Use cases](../use-cases.md) for end-to-end recipes.

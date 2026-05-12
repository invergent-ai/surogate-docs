---
title: Skills & Tools
sidebar_position: 2
slug: /features/skills
---

# Skills & Tools

Skills are how your agents do work outside of generating text. Read a database, write to a ticket tracker, call an API, run a saved workflow. A skill is a small, typed function with a description; the agent picks when to call it based on the conversation.

**MCP Servers** are the externally-hosted alternative. If a vendor (or another team) already exposes a Model Context Protocol endpoint, you register the URL and the agent can call any tool the server offers. You don't host anything.

## When to write a skill vs use an MCP server

| You have… | Use |
|---|---|
| A narrow function ("get_customer", "create_ticket") | **Skill** — fast to write, type-safe, stays in Surogate Ops. |
| A vendor that already exposes an MCP endpoint | **MCP Server** — register once, use everywhere. |
| An internal service you'd like to expose to multiple agents | **MCP Server** — host one and connect to it from every agent. |

## Write a skill

1. Build → Skills & Tools → **New Skill**.
2. The Skill Builder opens inline. Fill the five top-level fields:
   - **Name** — internal id, URL-safe, referenced from agent configs.
   - **Display Name** — what users see in lists.
   - **Description** — what the skill does, in one or two sentences. **Agents read this to decide when to call.** Be precise.
   - **Trigger** — optional natural-language hint ("when the user asks about pricing").
   - **Tags** — space-separated; used by the filter on the Skills list.
3. Write the body in the markdown editor below. The editor supports `Ctrl/⌘ + B` and `Ctrl/⌘ + I`.
4. Save & publish.

## Start from a template

If you don't know where to begin, hit **Import skill**. The Templates library lists 72 starter skills across 17 categories — `autonomous-ai-agents`, `blockchain`, `creative`, `devops`, `email`, `finance`, `health`, `mcp`, `mlops`, `productivity`, `research`, `security`, `web-development`, and more. Pick the card closest to your need; the Skill Builder opens with the template pre-filled. Edit name, description, and body, then save.

The full category breakdown:

- `mlops` ships the most (25 templates) — vector DBs, embeddings, fine-tuning helpers, FAISS, Pinecone, Qdrant, Whisper, PyTorch Lightning.
- `research` has 9 — web search, OSINT, drug discovery, bioinformatics.
- `finance` has 7 — DCF, LBO, comps, merger models, Excel and PowerPoint authors.
- `productivity` has 7 — Shopify, SiYuan notes, Telegram, telephony.
- `creative` has 5 — Blender, hyperframes, kanban video orchestration, meme generation.

## Connect an MCP server

Build → Skills & Tools → **MCP Servers** tab → **Add Server**. Provide the endpoint URL and any auth (a credential reference, headers, or a token from the **Vault**). Save. The server's tools become selectable on every agent's settings page.

## Attach to an agent

Open the agent → **Settings** → multi-select your skills and MCP servers → redeploy.

**Agents pin to the version of each skill that exists at deploy time.** Editing a skill creates a new version row but does not propagate to deployed agents. To push an update: save the new version, open each agent that uses the skill, re-select it from the dropdown (the new version is now top of the list), and redeploy.

## When something fails

- **Agent doesn't call the skill it should.** The Description isn't specific enough. Rewrite it to say exactly when the skill applies; agents are good at following precise descriptions.
- **MCP server times out.** Open a session that called it — the timeout shows up there with the URL it tried.
- **Schema rejects valid inputs.** Mismatched types in the Skill Builder. Common cause: a `string` field that should be a number, or vice versa.

## Where to go next

- **[Agents](./agents.md)** — to attach skills.
- **[Sessions](./sessions.md)** — to inspect tool calls.
- **[Data Hub](./hub.md)** — to publish a skill for reuse.

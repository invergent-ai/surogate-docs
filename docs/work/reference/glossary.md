---
title: Glossary
sidebar_position: 1
---

# Glossary

Every Surogate term you'll see in Work mode, in one place.

| Term | Definition |
|---|---|
| **Agent** | A deployed AI service with a URL like `<slug>.cloud.surogate.ai`. Bundles a model, skills, knowledge bases, MCP servers, persona, and channels. |
| **CLARIFY** | A built-in confirmation card the agent (or Copilot) shows before destructive or expensive operations. You click Yes or No. |
| **Channel** | The way users reach the agent — Web, Slack, Telegram, Website widget, API. Same agent, different doors. |
| **Channel identity** | A link between a platform-specific user (a Slack user, a Telegram user) and an internal Surogate user. Lets the same person on Slack and Web share sessions. |
| **Copilot** | The platform's built-in AI agent. Press ⌘+/ to open. Runs platform ops on your behalf. |
| **Develop mode** | The Studio surface (`/studio/*`) — for builders. Adds Models, Compute, Hub, Datasets, Training, Evaluations. |
| **EVENTS tab** | The full ordered log of everything that happened in a session: user messages, LLM responses, tool calls, results, decisions. |
| **Goal (`/goal`)** | A slash command that defines an outcome. The agent keeps working until an evaluator says satisfied / failed / blocked, or 20 iterations are used. |
| **Inbox** | A per-user queue of items the agent has pushed up for attention — clarify questions, action requests, governance approvals. |
| **Knowledge base (KB)** | A curated corpus of documents the agent can browse at runtime via `kb_list_pages` / `kb_read_page`. Sources → Curator → Wiki. |
| **Loop (`/loop`)** | A slash command that schedules a prompt to run on a recurring basis (fixed or dynamic interval). |
| **MCP server** | An external system the agent can use as a tool — GitHub, Slack, your CRM, internal APIs. Follows the open Model Context Protocol. |
| **Persona (SOUL.md)** | The agent's identity, tone, and rules. Up to 20,000 characters. Edited in the CONFIG tab. |
| **Quality flags** | Per-session tags: 👍 / 👎 (user feedback), `policy.denied`, `harness.crash`, `saga.compensated`, `expert.override`, `expert.endorse`. |
| **Replay** | Fork a session: re-run your user messages against the new agent config to see if the new behaviour is better. |
| **Session** | One conversation between a user and an agent. Records everything. Survives crashes. |
| **Skill** | A small markdown file telling the agent how to handle a specific kind of request. Reusable. |
| **Tool** | A capability the agent can invoke — `kb_read_page`, `web_search`, `read_file`, `terminal`, `browser_navigate`, etc. The agent decides which to use. |
| **User (per-agent)** | An end-user account on a specific agent. Different from your operator account. |
| **Vault** | Encrypted credential storage for MCP servers. Secrets never reach the agent's sandbox. |
| **Work mode** | The operator-facing surface (`/work/*`) — Agents, Sessions, Library. You're here. |

## What's next

[FAQ](./faq.md) for common questions.

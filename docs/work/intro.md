---
slug: /work
title: Welcome to Work mode
sidebar_label: Welcome
sidebar_position: 1
---

# Work mode

Work mode is for the day-to-day of running agents — chatting with them, watching sessions, attaching skills and KBs, publishing to channels. If you write skills in code, train experts, or run evaluations, flip to **Develop mode** in the navbar.

## Mental model

A Surogate **agent** is a deployed service at `<slug>.cloud.surogate.ai` bundling:

- A **model** that thinks
- **Skills** — markdown files telling it how to handle specific request types
- **Knowledge bases** — documents it can search at runtime
- **MCP servers** — connections to external systems (Slack, GitHub, your APIs)
- **Persona** — the agent's identity, tone, and boundaries. In Work mode this is the DESCRIPTION field on the Configure page; Develop mode exposes the underlying SOUL.md textarea.
- **Channels** — Web (always on), Slack, Telegram, Website widget

The improvement loop:

```
Run a chat  →  Review the session  →  Mark good/bad  →  Improve the agent  →  Run more chats
```

Each step has its own chapter:

| Chapter | Answers |
|---|---|
| [Run an agent](./workflow/run-agent.md) | Open a session, chat, watch the workspace |
| [Review what your agent did](./workflow/review-sessions.md) | Session detail, quality flags, replay |
| [Improve your agent](./workflow/improve-agent.md) | Mark sessions, attach skills/KBs, edit persona |

Plus shorter chapters: **Library** (skills, KBs, MCP servers), **Channels** (Web/Slack/Telegram/Website + end-user accounts), **Conversation tools** (`/goal`, the Copilot, the inbox), **Settings**, **Use cases**, **Reference**.

## When to flip to Develop mode

Skip to Develop mode when you need to:

- Write skills in code instead of just attaching existing ones
- Train fine-tuned experts on your traffic
- Run benchmark evaluations or build a custom benchmark
- Connect a cloud GPU provider
- Configure governance policies in detail
- Integrate via the REST API
- Self-host on your own cluster

For everything else, you can run a successful agent for months from Work mode alone.

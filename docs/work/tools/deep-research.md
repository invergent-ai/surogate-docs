---
title: Deep research (`/deep-research`)
sidebar_position: 8
---

# Deep research (`/deep-research`)

`/deep-research <topic>` produces a cited research report on a topic. The agent hands the topic to a dedicated **deep-research sub-agent** that plans the investigation, searches the web, curates an evidence bank, and delegates to a **research-writer** sub-agent for the final write-up.

## Basic use

In any chat with an agent:

```
/deep-research How are EU banks approaching AI Act compliance for customer-facing chatbots?
```

The agent delegates the topic once, and the sub-agents return a cited markdown report. You don't have to tell the agent to "search" or "write it up" — that whole workflow lives inside the sub-agent.

If you send `/deep-research` with no topic, the agent asks what you'd like researched, then runs the workflow on your reply.

## Single-shot semantics

`/deep-research` delegates **exactly once**. It does not retry.

- The topic goes to the sub-agent as a single research goal — it is not split into sub-topics or fanned out into multiple parallel runs.
- If that one delegation fails or times out, the agent reports the failure to you verbatim and stops, rather than launching more attempts that would burn the same budget again.

This keeps a single request from turning into a runaway fleet of research jobs. If a run fails, re-issue the command yourself once you've adjusted the topic.

## When to use it

Reach for `/deep-research` when you want a **thorough, sourced answer** to an open question — market landscapes, regulatory summaries, technical comparisons, background briefs — rather than a quick reply from the agent's own knowledge. The deliverable is a report with citations, not a chat answer.

For it to work, the agent must have the deep-research workflow enabled (the `/deep-research` capability toggle on the CONFIG → **Capabilities** tab; see [Configure an agent](../workflow/configure-agent.md)). When enabled, the agent advertises the `deep-research` sub-agent and knows to delegate to it.

## `/deep-research` vs `/auto-research`

These are different tools that both start with "research":

| Command | What it is |
|---|---|
| `/deep-research` | Single-shot — one investigation that returns a cited report. Best for "tell me everything about X." |
| `/auto-research` | An iterative optimization run (Arbor) that grows a hypothesis tree and improves against a measured baseline over many cycles. Best for "make this metric better." |

If you want a report, use `/deep-research`. If you want an autonomous optimization loop, see `/auto-research` in [Slash commands](./commands.md#auto-research-in-detail).

## Related pages

- [Slash commands](./commands.md) — the full command reference.
- [Configure an agent](../workflow/configure-agent.md) — enabling the deep-research capability.

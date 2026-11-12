---
title: Deep research (`/deep-research`)
---

`/deep-research <topic>` produces a cited research report on a topic. The agent hands the topic to a dedicated **deep-research sub-agent** that plans the investigation, searches the web, curates an evidence bank, and delegates to a **research-writer** sub-agent for the final write-up.

## Basic use

![`/deep-research` in the command palette](../../../../assets/screenshots/work-chat-commands.png)

In any chat with an agent:

```
/deep-research How are EU banks approaching AI Act compliance for customer-facing chatbots?
```

The agent delegates the topic once, and the sub-agents return a cited markdown report. You don't have to tell the agent to "search" or "write it up" — that whole workflow lives inside the sub-agent.

If you send `/deep-research` with no topic, the agent asks what you'd like researched, then runs the workflow on your reply.

## Single-shot semantics

`/deep-research` starts **exactly one** research agent. It does not retry.

- The topic goes to the sub-agent as a single research goal — it is not split into sub-topics or fanned out into multiple parallel runs.
- The research agent runs in the background: its report reaches the agent as a notification, and until then the agent does not guess at the findings.
- If the research agent fails, the agent reports the failure to you verbatim and stops, rather than launching more attempts that would burn the same budget again. The planner's wait for the writer is capped at **60 minutes** — a writer still running then counts as timed out.

This keeps a single request from turning into a runaway fleet of research jobs. If a run fails, re-issue the command yourself once you've adjusted the topic.

## When to use it

Reach for `/deep-research` when you want a **thorough, sourced answer** to an open question — market landscapes, regulatory summaries, technical comparisons, background briefs — rather than a quick reply from the agent's own knowledge. The deliverable is a report with citations, not a chat answer.

For it to work, the agent must have the deep-research workflow enabled (the `/deep-research` capability toggle on the CONFIG → **Capabilities** tab; see [Configure an agent](/work/workflow/configure-agent/)). When enabled, the agent advertises the `deep-research` sub-agent and knows to delegate to it.

## Related pages

- [Slash commands](/work/tools/commands/) — the full command reference.
- [Configure an agent](/work/workflow/configure-agent/) — enabling the deep-research capability.

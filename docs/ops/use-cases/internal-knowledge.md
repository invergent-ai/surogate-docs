---
title: Internal knowledge assistant
sidebar_position: 2
slug: /use-cases/internal-knowledge
---

# Internal knowledge assistant

A Slack or chat bot that answers your team's "how do we…?" questions against your wiki, runbooks, and architecture docs. Cuts the bus-factor problem in half: the answer is in the docs, the bot is the link.

## What you need

- **A model.** A general-purpose chat model is fine. Specialized doesn't help much here.
- **One or more knowledge bases.** One per source you trust: Confluence, Notion, an exported handbook, your engineering runbooks repo. Keep KBs scoped — searching across "everything we've ever written" produces worse answers than searching the right corpus.
- **No skills, or one.** Most internal-KB bots don't need tools. Add a single skill — say, *create_doc_request* — so the bot can flag a question it couldn't answer.

## Set it up

1. **Build a KB per source.** Build → Knowledge Bases → **+ New Knowledge Base**. Point each at one source (one for Confluence, one for Notion, etc.). Wait for each to reach **Active**.
2. **Deploy the agent.** Build → Agents → **Deploy Agent**. Pick the model, name it something like *Engineering Q&A*, save.
3. **Attach the KBs.** Open the agent's **Settings**, multi-select your KBs, redeploy.
4. **Hook it to your chat.** Wire your Slack / Teams bot to call this agent through Surogate's API. The API key for the agent's model authorizes the call.

## Try it

Ask the bot a question whose answer is in your docs. Open the resulting session — it'll show a retrieval step indicating which docs the agent pulled from. If retrieval came back empty, your KB doesn't have the right content yet.

## Iterate

The two things you'll see in the first week:

- **Hot questions that the KB doesn't cover.** Add the missing doc and re-index. Within minutes the bot's answers improve.
- **Stale answers.** A KB based on a wiki you haven't updated since Q1 will tell people the wrong onboarding steps. Schedule the compile to run on a cron so changes propagate without manual intervention.

For very large doc sets, split into multiple KBs and let the agent decide which to query — better than one giant index where everything competes for top-k.

## Where to go next

- **[Knowledge Bases](../features/knowledge-bases.md)** — sources, compile schedules, retrieval.
- **[Skills & Tools](../features/skills.md)** — for the flag-this-question skill.
- **[Sessions](../features/sessions.md)** — to inspect each conversation step by step.

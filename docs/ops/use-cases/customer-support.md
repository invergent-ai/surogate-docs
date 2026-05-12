---
title: Customer support agent
sidebar_position: 1
slug: /use-cases/customer-support
---

# Customer support agent

A first-line support agent that answers product questions from your live chat, knows when to hand off to a human, and writes a follow-up ticket on the way out.

This is the most common Surogate Ops deployment. It's also the easiest to iterate on, because every chat the agent has becomes training data for the next version.

## What you need

- **A model.** Start with a general-purpose model in Surogate Ops. You'll specialize it later (see [Train an expert](#train-an-expert-on-real-traffic) below).
- **A knowledge base.** Your product docs, help-center articles, or a clean export of your existing FAQ. Surogate compiles it once; the agent reads from it at runtime.
- **One or two skills.** At minimum: *create_ticket* in your tracker. Most teams add *search_orders* or *get_customer* against their backend.

## Set it up

1. **Create the knowledge base.** Build → Knowledge Bases → **+ New Knowledge Base**. Point it at your help-center URL or upload the docs. Wait for it to reach **Active**.
2. **Write the ticket-creation skill.** Build → Skills & Tools → **New Skill**. The Skill Builder gives you a markdown body where the skill spec lives; if you've never written one, pick the closest template from the library on the **Import skill** screen.
3. **Deploy the agent.** Build → Agents → **Deploy Agent**. Pick the model, set a display name like *Support Agent*, save.
4. **Attach the skill and the KB.** Open the agent's **Settings** tab, multi-select your new skill and KB, redeploy.

That's the whole thing. About fifteen minutes if you have the docs ready.

## Try it

Switch to **Work** mode and open the agent. Ask it a question your support team gets every week. The reply should come from the KB; if the agent decides it needs to escalate, the *create_ticket* skill fires and your tracker shows the new ticket.

If it doesn't work the first time, the chat's session is visible to you under Operate → Sessions. Open the session to see the agent's full step-by-step reasoning — which skill it tried to call, what came back. That's where you debug.

## Iterate

Open a few sessions after the agent's been running for a couple of days. Two things matter early:

- **Refusals.** The agent declines to answer questions it should have answered — usually because the KB doesn't cover that topic. Add the missing doc and recompile the KB.
- **Hallucinations.** The agent makes up product behavior. Open the session, flag the bad message, and the flagged session goes into your dataset of "things to fix".

After a couple of weeks, you'll have a few hundred flagged sessions. That's enough to train an expert.

## Train an expert on real traffic

This is the loop that justifies running Surogate over just calling a hosted API.

1. **Build a dataset from sessions.** Train → Datasets → **New Dataset** → **From Conversations**. Pick this agent and the date range. Surogate exports the sessions, formatted as supervised fine-tuning examples.
2. **Train a fine-tune.** Train → Training Runs → **New Run** → **SFT**. Pick a smaller base model (an 8B is plenty for support), point it at the dataset, configure precision (`bf16` is the easy default; `qlora` if you're cost-sensitive), pick a GPU offer from your connected backend, hit **Create**.
3. **Serve the result.** When the run completes, promote the weights to a Model from the run detail. Then redeploy your agent on top of the new model.

The new model knows your product and your support team's style better than the original ever did. Your costs drop too — an 8B expert serves orders of magnitude cheaper than a 70B generalist.

## Where to go next

- **[Agents](../features/agents.md)** — the full Agent reference.
- **[Knowledge Bases](../features/knowledge-bases.md)** — sources, compile schedules, retrieval.
- **[Skills & Tools](../features/skills.md)** — the Skill Builder, MCP servers, the templates library.
- **[Datasets](../features/datasets.md)** — the four ways to build one.
- **[Training](../features/training.md)** — SFT and GRPO runs, end-to-end.

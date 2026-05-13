---
title: Build a support bot in 20 minutes
sidebar_position: 1
slug: /tutorials/build-a-support-bot
description: End-to-end walkthrough — sign in, pick a template, talk to your agent, flag a session, attach your real knowledge base, redeploy.
---

# Build a support bot in 20 minutes

This tutorial walks the operator path end to end. You start from a fresh Surogate Ops sign-in, deploy a working support agent from a template, run the first real conversations against it, find what it gets wrong, and attach your team's actual knowledge base to fix the worst of it. Twenty minutes if you have a help-centre URL handy; thirty if you have to chase one down.

It's the right first build because it exercises every part of Surogate Ops you'll use later — the Work / Develop toggle, templates, sessions, flagging, knowledge bases, agent settings — without asking you to write a single skill or train a single model.

## What you'll have at the end

- A deployed agent that answers product questions from your help centre.
- A working understanding of the two surfaces — **Work** (where users chat) and **Develop** (where you build).
- A first flagged session, which is the seed for the iteration loop you'll run for the rest of the project's life.
- A second-pass agent attached to your real knowledge base.

## Before you start

- A Surogate Ops account. The free tier is enough for this tutorial.
- A help-centre URL, an internal docs site, or a folder of FAQ documents. Anything that has answers to the kinds of questions you want the bot to handle.
- About twenty minutes of focused time. The slowest step is the knowledge base compile, which is hands-off — you can read a few sessions while it runs.

## Step 1 — Pick the Operator path

Sign in. You land on the welcome screen with one big button and three smaller cards.

Click **Start**, then pick **Create my first Agent**. This takes you to the **Work** dashboard — the surface end users (your team, your customers) actually see.

If you accidentally pick **Develop and Train Agents**, that's fine. The two surfaces are interchangeable: every page in Studio has a **Work / Develop** toggle in the top-right that remembers your choice for next time.

The Work dashboard is empty by design. The big input in the middle asks *Describe what you need*, and the **Find Templates** button does semantic search across thirty-plus pre-built templates.

## Step 2 — Find the Customer Support template

Type something specific in the input. Bad: *I need a chatbot*. Good: *an agent that answers customer questions from our help centre and creates tickets when it can't*.

Click **Find Templates**. The grid below shows the best matches. The first card should be **Customer Support** — that's the one you want.

Click into the card. A preview opens with:

- The agent's display name and slug.
- A description of what it does out of the box.
- The default skills it ships with (almost always a `create_ticket` placeholder and a `search_orders` placeholder you'll wire to your tracker later).
- The model it'll use by default.

Click **Use this template**. The agent is created, configured, and deployed. About thirty seconds for the first deploy of a fresh model; subsequent deploys reuse cached layers and land in single-digit seconds.

When the status pill flips to **Running**, you're ready to chat.

## Step 3 — Have the first real conversation

Click into the agent. The chat surface opens.

Don't start with a generic test. Start with a real question your support team got this week:

> *How do I cancel my subscription before the next billing cycle?*

The agent reads your initial prompt, decides whether to call a skill (it won't have one wired yet, so it'll fall back to the model), and responds.

Try three kinds of question, in this order:

1. **A question the agent should easily handle from general knowledge.** It'll do fine.
2. **A question that depends on your product specifically.** Without your knowledge base, the agent will improvise — that improvisation is exactly what you don't want shipping to real customers, but it's useful to see it.
3. **A question that should escalate to a human.** Something like *I think your service charged me twice last month, can you check?*. The agent should refuse cleanly and suggest a hand-off path.

Now you have three sessions — one good, one likely hallucinating, one cleanly refused. That's enough material to start iterating.

## Step 4 — Switch to Develop mode

In the top-right of the Work surface, click the **Work / Develop** toggle. You land on the **Studio** dashboard.

This is the builder's surface. Same agent, same sessions, but with full visibility into what the agent did step by step. The sidebar reorganises around **Build / Train / Operate / Distribute** rather than around end-user chat.

Open **Operate → Sessions**. The list of sessions includes everything you just had in Work mode plus everything else the agent has ever served. Find the three sessions from step 3.

## Step 5 — Inspect a session end-to-end

Click into the second session — the one where the agent improvised an answer that depends on your product.

The detail view shows:

- The full chat transcript on the left.
- The agent's step-by-step trace on the right: the prompt it received, the system prompt and context it assembled, every skill call it considered, the tokens it produced, the final response.

Read the trace. The agent decided, on its own, what to say. Without a knowledge base, it had nothing authoritative to ground that decision in. The improvisation might be plausible but wrong.

This is the moment Surogate is built around. Closed-box tools let an agent say something wrong and never let you see why. Surogate's whole proposition is that the trace is visible, the trace becomes data, and the data improves the model. The rest of the tutorial is about closing that loop with the simplest possible move — adding the right knowledge.

## Step 6 — Flag the bad message

Above the trace, every message has a flag control: 👍 (good), 👎 (bad), and a more detailed *Add to dataset* action.

Click 👎 on the improvised answer. A small dialog asks why. Pick the closest reason (*made up a fact*, *missed the right answer*, *should have escalated*) or write a short free-text note.

That session is now flagged. It also lands in the Sessions list with a coloured marker so you can filter back to it later. More importantly — and this is the part that pays off in a month — every flagged session is the seed for a training dataset. Today you flag one to teach yourself the loop. Six weeks from now you flag a few hundred and use them to fine-tune an expert. See [Tutorial: Train and promote an expert](./train-and-promote-an-expert.md) for that step.

## Step 7 — Attach your real knowledge base

The improvising agent improvises because it has no source of truth. Time to give it one.

In Studio, go to **Build → Knowledge Bases → + New Knowledge Base**. Two minimum fields:

- **Name** — pick something readable, like *Support Help Centre*.
- **Source** — pick *URL* and paste your help-centre URL, or pick *Upload* and drop a folder of PDFs / Markdown files. Both work; URLs auto-recompile on a schedule you set, uploads don't.

Submit. The KB lands in state **Compiling**. The curator model (Surogate's default) is reading every source, building a per-source wiki, and writing a cross-source synthesis index that links related material. Expect a few minutes for a small site; an hour for an enterprise wiki.

While it compiles, open your agent's **Settings** tab. There are multi-selects for **Skills**, **MCP Servers**, and **Knowledge Bases**. You can attach the KB now — the agent will simply return empty retrieval results until the KB reaches **Active**, then start citing.

Tick the new KB. Click **Save**. The agent redeploys; a few seconds later it's running on the new attachment.

## Step 8 — Re-run the same conversation

Switch back to **Work** mode (top-right toggle). Open the agent. Ask the same product-specific question from step 3 — the one the agent improvised on.

Two things should be different:

1. The answer should be sourced. The agent's reply now references your actual help-centre content rather than improvising.
2. The session trace (back in Studio → Sessions) shows a **retrieval** step before the response — the agent queried the KB, got back chunks, and grounded its answer on them.

If the answer is still wrong, the source content is wrong (or missing). The fix is upstream — add or correct the help-centre doc, recompile the KB, retry. That cycle is the production loop. The bot is only as good as the source.

## Step 9 — Notice the cost of doing nothing

Before you close the tab, look at the dashboard. The Active Agents tile says **1**; the Serving Models tile says **1**; the Recent Conversations panel shows your test chats.

That's the production state. From here you can:

- Share the agent's URL with your team. Anyone with the link picks up the chat where it left off (sessions persist on a stable id).
- Wire the agent into your real support channel — Intercom, Zendesk, Slack — by giving the channel an API key (see [API overview](../api/overview.md)).
- Watch sessions accumulate; flag the bad ones; let the flagged set grow into your training dataset.

## When this isn't enough

This twenty-minute build is a starting point, not a destination. Three signs you've outgrown it:

- **You hit specific repeatable failures the KB can't fix.** Probably a missing skill — for example, the agent can't read a specific customer's order. Write the skill (see [Skills & Tools](../features/skills.mdx)).
- **Inference cost is climbing.** The default template uses a generalist model. Once you have a few hundred flagged sessions, you can train a smaller expert that does the same job at a fraction of the cost. See [Tutorial: Train and promote an expert](./train-and-promote-an-expert.md).
- **You want the same agent in multiple channels.** Build the routing layer outside Surogate — Intercom → webhook → Surogate API → response — and the agent stays the same. See [Inference API](../api/inference.md).

## What you've learned

In twenty minutes you've:

- Deployed an agent from a template.
- Talked to it through the Work surface.
- Inspected its reasoning in the Develop surface.
- Flagged the kind of session that becomes training data.
- Attached your real knowledge base and watched the agent ground itself.
- Seen the production loop that the rest of the manual builds on.

Every other tutorial in this section is a continuation of this one. The next tutorial wires a cloud and serves your own model behind the agent; the third trains a fine-tuned expert from the sessions this agent produces.

## Where to go next

- **[Tutorial: Connect a cloud and serve a model](./connect-cloud-and-serve-a-model.md)** — when you want to host your own weights instead of proxying a hosted model.
- **[Tutorial: Train and promote an expert](./train-and-promote-an-expert.md)** — the loop from captured sessions to a fine-tuned model.
- **[Knowledge Bases](../features/knowledge-bases.mdx)** — the deep reference for KB sources, schedules, the curator.
- **[Sessions](../features/sessions.mdx)** — the deep reference for session flags, filters, and exports.

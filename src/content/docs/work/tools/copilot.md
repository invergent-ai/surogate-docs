---
title: Copilot (⌘+/)
---

The **Copilot** is an AI agent that drives the platform itself. Press **⌘+/** (Mac) or **Ctrl+/** (Windows/Linux) anywhere in `ops.surogate.ai`.

A drawer opens with a chat composer. Ask in natural language; the Copilot calls the platform's tools and reports back.

## What it can do

![The Surogate Copilot panel, opened over the workspace](../../../../assets/screenshots/work-copilot-panel.png)

Look things up:

- *"What agents do I have running?"*
- *"Which agent had the most sessions this week?"*
- *"Find conversations where people got stuck on pricing."*
- *"Show me the latest training run for sql-writer."*
- *"Show me what's in the support-chats dataset."*
- *"How's the loss going on my last run?"*
- *"Which GPUs can my project train on, and what did training cost in the last 30 days?"*
- *"What skills does my customer-support-bot have attached?"*
- *"What failed this week?"*

Build and change things:

- *"Create a skill called `weekly-summary` that produces 5-bullet summaries."*
- *"Attach the `acme-product` KB to my customer-support-bot."*
- *"Connect this MCP server to my agent."*
- *"Switch customer-support-bot to the `qwen-support` model."*
- *"Start a training run with the conversations dataset."*

The Copilot calls the platform's own tools on your behalf. You see the same effects as if you had clicked through the UI. For the list of tools by area, see [Develop mode → Copilot](/develop/tools/copilot/).

## Building an agent, skill or knowledge base

When you ask it to make something, it does not just start. It interviews you one question at a time (purpose, audience, tone, sources, tools, boundaries), looks at what you already have so it does not duplicate it, and shows a plan for your approval. Only then does it build, one piece at a time, reads each piece back to check it, and ends with links to everything and a few first messages to test with.

It follows a written build guide for each kind of thing: agents, skills, knowledge bases, sub-agents, MCP server connections, Programs, datasets, training runs and model deployments.

## Datasets, training and models

- *"Turn this file into a dataset."* It uploads one JSONL, JSON, CSV or Parquet file you attach in chat (up to 50 MB), reshaping it first when the change is mechanical. Building a dataset from your agents' chats, generating a synthetic one, importing a Hugging Face repository and scrubbing PII are done on the Datasets page; it sends you there.
- *"Fine-tune a model on these support conversations."* It interviews you, plans the run and, after your yes, starts an SFT, DPO or distillation run. It follows the run's loss and can cancel it. A Hugging Face dataset can be trained on directly, without a copy in the project.
- *"Move my saved run to the RTX PRO 6000 and start it."* A refused run stays saved; it can edit that run (settings, GPU, Hugging Face subset), start it, or delete runs you no longer need, each after your yes to the exact change.
- *"Serve my fine-tuned model."* It starts serving a model that is already on the Models page, checks that it serves, stops it, and switches an agent onto it. A finished run is not on Models until you add it (see [Local Hub](/develop/features/models/#local-hub)); it tells you how.

## Asking the docs

You can ask it how the platform works: *"What does the Compute page do?"* It looks the answer up in the product documentation instead of answering from memory. When you ask from a page, it knows which page you have open and, for pages that have one, which doc covers it.

## Programs, people and the team

The Copilot works across these areas:

- **Programs:** run an agent's [Programs](/work/tools/programs/). List and build journeys and their steps, review a journey and dry-run it, send a test, activate or pause it, read its stats, and register WhatsApp templates.
- **People:** find and add people, make a Telegram start link, enrol people, change their follow-up, link their contacts, read their timeline and message them.
- **Team:** set up the team (what each member gets told about, can do and handles, and a Slack channel picked from the workspace as its shared alert place), change the wording and channels on Settings, and claim or resolve escalations.
- **Also:** read and answer your Inbox, read an agent's Insights, manage the plans on Monetize, and build the agent's [landing page](/work/workflow/landing-page/), including formatted text and image framing.

It knows what you are looking at: on the Programs page it is told which tab, journey and person you have open, so *"why didn't this step go out?"* needs no further context.

**`/build-program`** is a playbook for setting a program up end to end. The Copilot interviews you one question at a time (who is followed and why, the date day 0 counts from, the rhythm, what each answer means and which is urgent, the channels, the team, the language of every message), inspects what the agent already has, and writes a plan for you to approve. Only then does it build: the step skills, any missing WhatsApp templates, the journey as a draft, the team and the wording. It reviews and dry-runs the journey and summarises what is live and what is still a draft, with a test script.

Activating a journey, sending a test, enrolling, messaging a person and changing the team need an explicit confirmation step, which the Copilot is instructed to take only after you say yes to that exact action. Called without it, the tool refuses and changes nothing.

## How it asks before acting

It asks with a question in the chat and waits for your answer before it:

- spends GPU time or model usage (training, deploying a model, compiling a knowledge base), deletes anything, starts an agent that is in an error state, or changes an agent's environment variables, policy or browser setting;
- overwrites a skill or sub-agent that already has that name, or connects an MCP server that runs a command on the runtime.

Building a new thing inside a plan you approved does not ask again. The plan was the yes.

Anything that reaches real people or real money is stricter: activating a journey, sending a test, enrolling or messaging a person, changing the team, and changing plans on Monetize. The tool itself refuses to run until the Copilot calls it again with an explicit confirmation, which its instructions allow only after you say yes to that exact action. A yes to the plan does not cover it.

While a question is open, a reply you type in the web chat is taken as your answer. A question that closes unanswered (see [Inbox](/work/tools/inbox/#when-nobody-answers)) is neither a yes nor a no: the Copilot doesn't act, says it is waiting, and asks again when you write.

Governance approvals in the Inbox are never the Copilot's to decide. It sends you to the Inbox page. For the exact tools and how each check works, see [Develop mode → Copilot](/develop/tools/copilot/#how-it-asks-before-acting).

## Conversation history

The Copilot drawer keeps a history menu in its header (the clock/history icon). Open it to switch between past Copilot conversations, rename them, or start a new chat. Each conversation is its own session and resumes where you left off.

## What the Copilot can't do

- **It has no browser.** It works from the platform's own tools, not the open web. If you want to scrape or navigate a site, use a regular agent with `browser_*` tools.
- **It can't make images or videos.** Use a regular agent for media.
- **It won't set up things that need secrets or money for you.** Its instructions have it explain the steps and link the page instead: connecting channels (WhatsApp, Slack, Telegram, Discord, Microsoft Teams), creating or revoking API keys and webhook secrets, Stripe Connect onboarding, your workspace's billing and plan, and inviting workspace members. It can still change an agent's environment variables, where channel keys live; its instructions have it ask you first and never repeat secret values back.
- **It can't change your password** or other account settings. Those go through Settings.
- **It can't scale agents.** Agents run on the shared runtime with no replicas, CPU or memory to set; it can start and stop them.
- **It can't change models beyond starting, stopping and redeploying them.** It can't add, edit, scale or delete one.
- **It can't browse or change the [Data Hub](/develop/features/hub/).**
- **It can't create RL environments or start GRPO runs.**
- **It can't run evaluations.**

For the last four, it tells you where in Studio to go instead; see [Develop mode → Copilot](/develop/tools/copilot/#what-the-copilot-wont-do).

## When the Copilot misbehaves

If the Copilot returns 401 ("Invalid base LLM token"), it's an admin-side config issue. Contact whoever runs your tenant.

If a tool returns an error, it tells you what went wrong instead of retrying blindly. Read the error, fix the cause, and ask again.

## Keyboard shortcuts

- **⌘+/** (or **Ctrl+/**) — open the drawer
- **Esc** — close the drawer
- **Enter** — submit the current message
- **Shift+Enter** — newline in the composer

## What's next

Other tools: [Goals (`/goal`)](/work/tools/goals/), [Inbox](/work/tools/inbox/), [Programs](/work/tools/programs/).

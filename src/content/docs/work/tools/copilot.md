---
title: Copilot (⌘+/)
---

The **Copilot** is an AI agent that drives the platform itself. Press **⌘+/** (Mac) or **Ctrl+/** (Windows/Linux) anywhere in `ops.surogate.ai`.

A drawer opens with a chat composer. Ask in natural language; the Copilot calls the platform's tools and reports back.

## What it can do

![The Surogate Copilot panel, opened over the workspace](../../../../assets/screenshots/work-copilot-panel.png)

Look things up:

- *"What agents do I have running?"*
- *"Which agent had the most sessions yesterday?"*
- *"Find conversations where people got stuck on pricing."*
- *"Show me the latest training run for sql-writer."*
- *"What skills does my customer-support-bot have attached?"*
- *"What failed this week?"*

Build and change things:

- *"Create a skill called `weekly-summary` that produces 5-bullet summaries."*
- *"Attach the `acme-product` KB to my customer-support-bot."*
- *"Connect this MCP server to my agent."*
- *"Scale customer-support-bot to 5 replicas."*
- *"Start a training run with the conversations dataset."*

The Copilot calls the platform's own tools on your behalf. You see the same effects as if you had clicked through the UI. For the list of tools by area, see [Develop mode → Copilot](/develop/tools/copilot/).

## Building an agent, skill or knowledge base

When you ask it to make something, it does not just start. It interviews you one question at a time (purpose, audience, tone, sources, tools, boundaries), looks at what you already have so it does not duplicate it, and shows a plan for your approval. Only then does it build, one piece at a time, reads each piece back to check it, and ends with links to everything and a few first messages to test with.

It follows a written build guide for each kind of thing: agents, skills, knowledge bases, sub-agents, MCP server connections and Programs.

## Asking the docs

You can ask it how the platform works: *"What does the Compute page do?"* It looks the answer up in the product documentation instead of answering from memory. When you ask from a page, it knows which page you have open.

## Programs, people and the team

The Copilot can run an agent's [Programs](/work/tools/programs/) for you: list and build journeys and their steps, review a journey and dry-run it, send a test, activate or pause it, read its stats, and register WhatsApp templates. It can find and add people, make a Telegram start link, enrol people, change their follow-up, link their contacts, read their timeline and message them; set up the team (what each member gets told about, can do and handles, and a Slack channel picked from the workspace as its shared alert place), change the wording and channels on Settings, and claim or resolve escalations. It also reads and answers your Inbox, reads an agent's Insights, manages the plans on Monetize, and builds the agent's [landing page](/work/workflow/landing-page/), including formatted text and image framing.

It knows what you are looking at: on the Programs page it is told which tab, journey and person you have open, so *"why didn't this step go out?"* needs no further context.

**`/build-program`** is a playbook for setting a program up end to end. The Copilot interviews you one question at a time (who is followed and why, the date day 0 counts from, the rhythm, what each answer means and which is urgent, the channels, the team, the language of every message), inspects what the agent already has, and writes a plan for you to approve. Only then does it build: the step skills, any missing WhatsApp templates, the journey as a draft, the team and the wording. It reviews and dry-runs the journey and summarises what is live and what is still a draft, with a test script.

Activating a journey, sending a test, enrolling, messaging a person and changing the team always wait for your yes. It never enrols real people on its own.

## How it asks before acting

It asks with a question in the chat and waits for your answer. Its instructions tell it to ask first for:

- starting training, deploying a model and compiling a knowledge base (they cost GPU time or model usage);
- any delete, naming the resource it is about to delete;
- scaling an agent to more replicas, and starting an agent that is in the `error` state;
- changing an agent's environment variables, its policy or its browser setting;
- connecting an MCP server that runs a command on the runtime;
- overwriting a skill or sub-agent that already has that name.

Building a new thing inside a plan you approved does not ask again. The plan was the yes.

Anything that reaches real people or real money is stricter. The tool itself refuses to run until you have said yes to that exact action, and a yes to the plan does not cover it. That covers:

- activating or pausing a journey, deleting a journey or a step, sending a test, and registering a WhatsApp template;
- enrolling a person, changing their status, changing their contacts, and messaging them (you approve the exact text);
- changing the team and the Programs settings;
- creating, changing or deleting a plan on Monetize, and changing the selling mode.

Governance approvals in the Inbox are never the Copilot's to decide. It sends you to the Inbox page.

## Conversation history

The Copilot drawer keeps a history menu in its header (the clock/history icon). Open it to switch between past Copilot conversations, rename them, or start a new chat. Each conversation is its own session and resumes where you left off.

## What the Copilot can't do

- **It has no browser.** It works from the platform's own tools, not the open web. If you want to scrape or navigate a site, use a regular agent with `browser_*` tools.
- **It can't make images or videos.** Use a regular agent for media.
- **It can't set up things that need secrets or money for you.** It explains the steps and links the page: connecting channels (WhatsApp, Slack, Telegram, Discord, Microsoft Teams), creating or revoking API keys and webhook secrets, Stripe Connect onboarding, your workspace's billing and plan, and inviting workspace members.
- **It can't change your password** or other account settings. Those go through Settings.

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

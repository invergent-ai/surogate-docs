---
title: Copilot (⌘+/)
---

The **Copilot** is an AI agent that drives the platform itself. Press **⌘+/** (Mac) or **Ctrl+/** (Windows/Linux) anywhere in `ops.surogate.ai`.

A drawer opens with a chat composer. Ask in natural language; the Copilot calls the platform's tools and reports back.

## What it can do

![The Surogate Copilot panel, opened over the workspace](../../../../assets/screenshots/work-copilot-panel.png)

Read operations (always enabled):

- *"What agents do I have running?"*
- *"Which agent had the most sessions yesterday?"*
- *"Find sessions where the agent thumb-downed in the last week."*
- *"Show me the latest training run for sql-writer."*
- *"What skills does my customer-support-bot have attached?"*

Write operations (live — with a confirmation step for risky actions, see below):

- *"Create a skill called `weekly-summary` that produces 5-bullet summaries."*
- *"Attach the `acme-product` KB to my customer-support-bot."*
- *"Scale customer-support-bot to 5 replicas."*
- *"Delete the test-summarizer-bot agent."*
- *"Start training run with the conversations dataset."*

The Copilot calls the platform's REST API on your behalf. You see the same effects as if you'd clicked through the UI.

## Programs, people and the team

The Copilot can run an agent's [Programs](/work/tools/programs/) for you: list and build journeys and their steps, review a journey and dry-run it, send a test, activate or pause it, read its stats, and register WhatsApp templates. It can find and add people, make a Telegram start link, enrol people, change their follow-up, link their contacts, read their timeline and message them; set up the team (what each member gets told about, can do and handles), change the wording and channels on Settings, and claim or resolve escalations. It also reads and answers your Inbox, reads an agent's Insights, manages the plans on Monetize, and builds the agent's [landing page](/work/workflow/landing-page/), including formatted text and image framing.

It knows what you are looking at: on the Programs page it is told which tab, journey and person you have open, so *"why didn't this step go out?"* needs no further context.

**`/build-program`** is a playbook for setting a program up end to end. The Copilot interviews you one question at a time (who is followed and why, the date day 0 counts from, the rhythm, what each answer means and which is urgent, the channels, the team, the language of every message), inspects what the agent already has, and writes a plan for you to approve. Only then does it build: the step skills, any missing WhatsApp templates, the journey as a draft, the team and the wording. It reviews and dry-runs the journey and summarises what is live and what is still a draft, with a test script.

Activating a journey, sending a test, enrolling, messaging a person and changing the team always wait for your yes. It never enrols real people on its own.

## The CLARIFY confirmation

For **destructive or expensive operations**, the Copilot is required to ask first. You'll see a Yes/No confirmation card inside the chat:

```
The Copilot wants to delete agent `test-summarizer-bot`. This will:

- Remove the agent's URL (test-summarizer-bot.cloud.surogate.ai)
- Detach 1 skill and 1 knowledge base
- Preserve session history in the audit log

Proceed?

[ Yes, delete ]   [ No, cancel ]
```

Operations that require CLARIFY:

| Operation | Why |
|---|---|
| `delete_*` (any kind) | Irreversible |
| `start_training` | Burns GPU hours |
| `deploy_model` | Burns GPU hours |
| `scale_agent` to higher replicas | Cost increase |
| `start_agent` when current status is `error` | Triggers a re-deploy |

Routine writes (`create_skill`, `update_skill`, `create_dataset`, `create_knowledge_base`, `stop_agent`, `cancel_training`) **don't** require CLARIFY — the Copilot proceeds directly.

## Conversation history

The Copilot drawer keeps a history menu in its header (the clock/history icon). Open it to switch between past Copilot conversations, rename them, or start a new chat — each conversation is its own session and resumes where you left off.

## What the Copilot can't do

- **It has no browser tool**. By design — the Copilot works from the platform's own tools, not the open web. If you want to scrape or navigate a site, use a regular agent with `browser_*` tools.
- **It can't see all sessions in your org** — only the ones in your current project. Use the Sessions view for tenant-wide observability.
- **It can't change billing**, manage Stripe, change your password, or other deeply personal admin ops. Those still go through Settings.

## When the Copilot misbehaves

The most common issue: it tries to list resources via a tool that doesn't exist (a known bug — `read_resource` is in its allowlist but not implemented). Workaround: ask the question in a way that doesn't require enumeration. Example:

- ❌ *"Tell me about my knowledge bases."*
- ✅ *"What knowledge bases does my customer-support-bot have attached?"* (specifies the agent, scopes the lookup)

If the Copilot returns 401 ("Invalid base LLM token"), it's an admin-side config issue. Contact whoever runs your tenant.

## Keyboard shortcuts

- **⌘+/** (or **Ctrl+/**) — open the drawer
- **Esc** — close the drawer
- **Enter** — submit the current message
- **Shift+Enter** — newline in the composer

## What's next

Other tools: [Goals (`/goal`)](/work/tools/goals/), [Inbox](/work/tools/inbox/), [Programs](/work/tools/programs/).

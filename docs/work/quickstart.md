---
title: Quickstart
sidebar_position: 2
---

# Quickstart

A working agent on your team's Slack in **10 minutes**. No code, no setup.

## 1. Deploy from a template

Open the **Templates** page → pick a template that matches what you want the agent to do:

| Template | What it's good at |
|---|---|
| **Customer Support Bot** | Answers questions from your product docs |
| **Incident Responder** | Triages alerts, writes runbooks |
| **Content Writer** | Drafts, edits, headlines |
| **Data Analyst** | Reads CSVs, makes charts |
| **Code Reviewer** | Reviews code diffs |
| **Customer Support Bot** | Customer support |
| **Empty agent** | Start from scratch |

Click **DEPLOY** → fill in:

- **Name** — `acme-support-bot` (or whatever)
- **Description** — one sentence
- Leave **Model** as the platform default

Click **DEPLOY**. Wait 30 seconds while the agent comes online. Status flips from `deploying` to `running`.

## 2. Test it from the platform

On the agent's page, click **CHAT** (top right). Type a question. The agent streams back its response, calling tools (search, file reads) as needed. Tool calls render inline so you can see what it did.

If the agent doesn't know enough about your product, that's normal — templates ship without your team's content. Skip ahead to step 4 to fix that.

## 3. Give it a Slack channel

Open the agent → **CHANNELS** tab → toggle **Slack** ON. Paste:

- **App Token** — `xapp-…` from your Slack app's App-Level Tokens, scope `connections:write`
- **Bot Token** — `xoxb-…` from your Slack app's OAuth & Permissions

If you don't have a Slack app yet, create one at [api.slack.com/apps](https://api.slack.com/apps) → enable Socket Mode → add scopes (`chat:write`, `app_mentions:read`, `im:read`, `im:write`, `channels:history`, `groups:history`, `users:read`) → install to your workspace.

Click **SAVE CHANNELS**. Within 5 seconds, the bot is online in Slack. DM it or `@mention` it in a channel.

## 4. Make it smarter (optional but worth it)

Two quick wins:

### Add a knowledge base

Go to **Library → Knowledge Bases → NEW KNOWLEDGE BASE**:

- Name: `acme-product`
- Add a few `.md` or `.pdf` sources (product docs, FAQ, runbooks)
- Click **COMPILE**, wait

Attach it to your agent: open the agent → **KNOWLEDGE & TOOLS** → **+ ATTACH KNOWLEDGE BASE** → pick `acme-product`.

New sessions now have `kb_search` available. The agent uses it automatically when a question matches the KB.

### Tighten the persona

Open the agent → **CONFIG** tab → **SOUL.md**. Replace the default with:

```markdown
# Acme Support Agent

You are the Acme support assistant. Speak as "we" when referring to Acme.
Tone: warm, concise, technically literate. Avoid corporate boilerplate.

When you don't know something, say "I'll get a human on this" and call
the `escalate` skill rather than guessing.
```

Save. New sessions pick up the new persona; in-progress ones keep the old one (by design).

## 5. Watch what it does

Every conversation is a session. Go to **Sessions** → pick your agent → click any session.

For each session, hover assistant turns and click 👍 or 👎. This is the signal you use to improve the agent over time — see [Improve your agent](./workflow/improve-agent.md).

## What you've done

In 10 minutes:

- A live agent on a custom URL: `<your-slug>.cloud.surogate.ai`
- Available in Slack to your team
- Grounded in your product docs (via the KB)
- With your tone (via SOUL.md)
- Recording every conversation for review and improvement

That's enough to start using it for real work. Come back to [Run an agent](./workflow/run-agent.md) and [Improve your agent](./workflow/improve-agent.md) when you want to go deeper.

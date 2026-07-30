---
title: Quickstart
---

A working agent on your team's Slack in **10 minutes**. No code, no setup.

## 1. Create the agent

From the **Agents** page (left nav under WORK) or from the **Dashboard's "CREATE ANOTHER AGENT"** card, you land on the **Templates** page.

The template catalog is currently empty. Click **Start from scratch** at the top of the page — a **DEPLOY NEW AGENT** dialog opens.

Fill in:

| Field | What to put |
|---|---|
| **Display Name** | e.g. `Acme Support Bot` |
| **Slug** | auto-generated from the name. Becomes `acme-support-bot.cloud.surogate.ai`. Locked once you confirm. |
| **Description** | one sentence — what the agent does |
| **Model** | leave as `Surogate` (the platform default) |

Click **CREATE AGENT**. The agent provisions in ~30 seconds; status flips from `deploying` to `running`.

You land on the agent's **Overview** page with its public URL, stats, channels, and recent sessions.

## 2. Have your first conversation

On the agent's Overview page, click **New chat** in the left navigation (between **Configure** and **Inbox**).

The chat opens. Type a question, press Enter — the agent streams its response. Tool calls (KB searches, web fetches) appear inline so you can see what it did.

Templates ship without your team's content, so the agent doesn't know your product yet. Step 4 fixes that.

## 3. Publish to Slack

Click **Configure** in the left nav, then open the **Channels** tab. Find the **Slack** row and toggle the switch ON.

Paste your Slack credentials:

- **App Token** — `xapp-…` from your Slack app's **App-Level Tokens** (scope `connections:write`)
- **Bot Token** — `xoxb-…` from **OAuth & Permissions**

Don't have a Slack app yet? Create one at [api.slack.com/apps](https://api.slack.com/apps) → enable **Socket Mode** → add bot scopes (`chat:write`, `app_mentions:read`, `im:read`, `im:write`, `channels:history`, `groups:history`, `users:read`) → install to your workspace.

Click **SAVE CHANNELS**. Within a few seconds, the bot is online in Slack. DM it or `@mention` it in a channel.

## 4. Make it smarter (optional but worth it)

Two quick wins, both on the **Configure** page:

### Add a knowledge base

In the left nav under **LIBRARY**, click **Knowledge Bases** → **NEW KNOWLEDGE BASE**. Name it (e.g. `acme-product`) and pick a curator model. Add a few `.md` or `.pdf` sources, click **COMPILE**, wait for status `active`.

Back on the agent's **Configure** page → **Knowledge Bases** tab → **+ ATTACH KNOWLEDGE BASE** → pick the new KB.

The agent will now search the KB at runtime when a question matches its content.

### Tighten the persona

The agent's identity, tone, and rules live on **Configure → Identity tab** — the **DESCRIPTION** field for short summaries and a **SOUL.md** textarea (up to 20,000 characters) for the full persona block. Replace the default with something like:

```markdown
# Acme Support Agent

You are the Acme support assistant. Speak as "we" when referring to Acme.
Tone: warm, concise, technically literate. Avoid corporate boilerplate.

When you don't know something, say "I'll get a human on this" rather
than guessing.
```

Save. New chats pick up the new persona; in-progress sessions keep the old one (by design).

## 5. Watch what it does

Every chat is a **session**. Open **Sessions** in the left nav → pick a session.

For each session, hover assistant turns and click 👍 or 👎. This is the signal you use to improve the agent over time — see [Improve your agent](/work/workflow/improve-agent/).

## What you've done in 10 minutes

- A live agent on a public URL: `<your-slug>.cloud.surogate.ai`
- Available in Slack to your team
- Grounded in your product docs (via the KB)
- With your tone (via the persona)
- Recording every conversation for review and improvement

That's enough to start using it for real work. Come back to [Run an agent](/work/workflow/run-agent/) and [Improve your agent](/work/workflow/improve-agent/) when you want to go deeper.

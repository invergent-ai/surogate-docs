---
title: Slack
sidebar_position: 2
---

# Slack channel

Publishes the agent as a Slack bot. Users DM it or @mention it in channels. Same conversations as on Web — if Slack identities are linked to Surogate users, sessions are shared.

Surogate connects to Slack over **webhooks** (Event Subscriptions), not Socket Mode. You create a Slack app, paste a few Request URLs into it, and hand Surogate your app's Signing Secret and Bot Token.

## Configuration in Surogate

Open the agent → **Configure** in the left nav → the **Channels** tab → find the **Slack** card → **Connect**. That opens a step-by-step walkthrough:

1. **Create a Slack app** at [api.slack.com/apps](https://api.slack.com/apps) → *Create New App* → *From scratch*.
2. **Add Bot Token Scopes** (OAuth & Permissions → Bot Token Scopes):
   `chat:write`, `app_mentions:read`, `im:read`, `im:write`, `channels:history`, `groups:history`, `files:read`, `users:read`. The wizard has a **Copy** button for the full list.
3. **Enable Event Subscriptions and paste your Request URLs.** Enter your **App ID** in the wizard; it then shows the exact URLs to paste back into Slack:
   - Event Subscriptions Request URL — `https://channels.surogate.ai/slack/<APP_ID>`
   - Interactivity Request URL — `https://channels.surogate.ai/slack/<APP_ID>/interact`
   - Slash Command Request URL — `https://channels.surogate.ai/slack/<APP_ID>/commands`

   Also subscribe to these bot events: `message.im`, `app_mention`, `message.channels`.
4. **Install to your workspace** (OAuth & Permissions → *Install to Workspace*) and copy the **Bot User OAuth Token** (starts with `xoxb-`).
5. **Paste your credentials** — the **Signing Secret** (Basic Information) and the **Bot Token** (`xoxb-…`).

Click **Connect Slack**. There is no separate save button — the connect step and every later option change save automatically.

## Options (the Slack "Manage" screen)

Once connected, the Slack card shows **Manage**. The options there auto-save as you change them:

| Option | What it does |
|---|---|
| **Require @mention** (default ON) | Only replies when @mentioned. Off = replies to every message in any channel it's added to. |
| **Mode** | **Team member** — channel members talk to a shared agent identity. **Personal assistant** — each user links their own Surogate account; unlinked users are prompted to link. |
| **Allow Bots** | Whether other bots can talk to this agent: **None** (default), **Mentions only**, or **All**. |
| **Reply in thread** (default ON) | Keeps replies inside the message thread. |
| **Reply broadcast** (default OFF) | Also posts the threaded reply to the main channel. |
| **Free-response channels** | Comma-separated Slack **channel IDs** (not names, e.g. `C0123ABCD`) where it answers without being @mentioned. |

The Slack manage screen also has a **Surogate Mate** section (Follow / Ambient) — see [Proactive engagement](./proactive.md).

## What users see

### DMs

The user types a message; the bot responds. Each DM is one Surogate session. Subsequent messages in the same DM continue the session.

### Channel @mentions

```
@acme-support what's the refund policy?
```

The bot responds inside the thread (assuming Reply in thread is on). Subsequent messages in that thread continue the session — no need to @mention again.

### File attachments

Slack users can attach files to messages. The bot reads them (markdown, CSV, JSON, images, PDFs) like any other input. If the bot writes files in response (e.g. an analysis CSV), it uploads them to Slack.

## How Slack identities are linked

The first time a Slack user messages the bot:

1. The platform looks up `(platform=slack, platform_user_id=U03ABCDEF)` in the channel-identity table.
2. If found, the message routes to that user's existing Surogate sessions.
3. If not found, an internal user is created OR the bot DMs them a pairing link to connect to an existing web account (this is the **Personal assistant** mode).

Once linked, the same person on Web and Slack sees the same agent, same memory, same sessions.

## Multi-workspace

Each Slack workspace needs its own Slack app + its own credentials. To run the same agent across multiple workspaces, create multiple agents in Surogate (each pointing at its workspace's app), or use the API channel for cross-workspace routing.

## When the Slack bot isn't responding

Common causes:

- **Missing scopes** — you added a new scope but didn't re-install the app to the workspace. Re-install, then paste the new Bot Token via **Reconnect**.
- **Request URLs not verified** — Slack must accept the Event Subscriptions Request URL (it shows a green "Verified"). If it's not verified, events never reach Surogate.
- **Wrong credentials** — the Signing Secret and Bot Token must both be from the same Slack app.

Check the agent's **Sessions** view — if no Slack-channel sessions are appearing when you send Slack messages, the inbound path is broken.

## Reconnecting and disconnecting

- **Reconnect** reopens the walkthrough so you can paste a new Bot Token after re-installing the app (e.g. when you added scopes).
- **Disconnect** stops the bot from replying. Your Slack app and credentials stay in place — reconnect anytime.

## What's next

For Telegram setup: [Telegram channel](./telegram.md). For embedding chat on your website: [Website widget](./website-widget.md). For end-user accounts: [Users](./users.md).

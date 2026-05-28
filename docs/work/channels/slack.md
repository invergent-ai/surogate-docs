---
title: Slack
sidebar_position: 2
---

# Slack channel

Publishes the agent as a Slack bot. Users DM it or @mention it in channels. Same conversations as on Web — if Slack identities are linked to Surogate users, sessions are shared.

## What you need from Slack

1. **Create a Slack app** at [api.slack.com/apps](https://api.slack.com/apps).
2. Add **Bot Scopes**: at minimum `chat:write`, `app_mentions:read`, `im:read`, `im:write`, `channels:history`, `groups:history`, `files:read`, `users:read`.
3. Enable **Socket Mode** (no public webhook URL needed).
4. Add an **App-Level Token** with the `connections:write` scope.
5. Install the app to your workspace.

Copy two tokens:

- **App Token** — starts with `xapp-`. Authenticates the Socket Mode connection (inbound events).
- **Bot Token** — starts with `xoxb-`. Authenticates outbound messages.

## Configuration in Surogate

Open the agent → **Configure** in the left nav → the **Channels** tab → toggle **Slack** ON. The form expands:

| Field | What it does |
|---|---|
| **App Token** | Paste `xapp-…` |
| **Bot Token** | Paste `xoxb-…` |
| **Require @mention** (default ON) | If on, the bot only responds in channels when @mentioned. Without this it would respond to every message in any channel it's added to — usually not what you want. |
| **Allow Bots** | Whether other bots can talk to it. Default `None`. |
| **Reply in Thread** (default ON) | Responses go in the thread, not the channel. Recommended. |
| **Reply Broadcast** (default OFF) | When on, thread replies also post to the channel (everyone sees them). |
| **Free Response Channels** | Comma-separated channel IDs where @mention is NOT required (use for dedicated `#agent` channels). |

Click **SAVE CHANNELS**.

## What users see

### DMs

The user types a message; the bot responds. Each DM is one Surogate session. Subsequent messages in the same DM continue the session.

### Channel @mentions

```
@acme-support what's the refund policy?
```

The bot responds inside the thread (assuming Reply in Thread is on). Subsequent messages in that thread continue the session — no need to @mention again.

### File attachments

Slack users can attach files to messages. The bot reads them (markdown, CSV, JSON, images, PDFs) like any other input. If the bot writes files in response (e.g. an analysis CSV), it uploads them to Slack.

## How Slack identities are linked

The first time a Slack user messages the bot:

1. The platform looks up `(platform=slack, platform_user_id=U03ABCDEF)` in the channel-identity table.
2. If found, the message routes to that user's existing Surogate sessions.
3. If not found, an internal user is created OR the bot DMs them a pairing link to connect to an existing web account.

Once linked, the same person on Web and Slack sees the same agent, same memory, same sessions.

## Multi-workspace

Each Slack workspace needs its own Slack app + its own pair of tokens. To run the same agent across multiple workspaces, create multiple agents in Surogate (each pointing at its workspace's tokens), or use the API channel for cross-workspace routing.

## When the Slack bot isn't responding

Common causes:

- **Missing scopes** — you added a new scope but didn't re-install the app to the workspace. Re-install.
- **Socket Mode disabled** — toggle it back on in Slack app settings.
- **Wrong tokens** — App Token must have `connections:write`. Bot Token must have the bot scopes. Mix them up and nothing works.
- **Another instance is running** — Slack only delivers updates to one consumer at a time. Stop your dev environment.

Check the agent's **Sessions** view — if no Slack-channel sessions are appearing when you send Slack messages, the inbound path is broken.

## Toggling Slack off

Configure → Channels tab → toggle Slack OFF → **SAVE CHANNELS**. The bot stops responding within seconds. Sessions in flight finish; new ones don't start. Tokens are preserved — you can re-enable later without re-entering them.

## What's next

For Telegram setup: [Telegram channel](./telegram.md). For embedding chat on your website: [Website widget](./website-widget.md). For end-user accounts: [Users](./users.md).

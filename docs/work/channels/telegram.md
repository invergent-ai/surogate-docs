---
title: Telegram
sidebar_position: 3
---

# Telegram channel

Simpler than Slack — one bot token and you're up.

## What you need

1. Open Telegram, talk to `@BotFather`.
2. `/newbot` → give it a name + username.
3. BotFather returns a token like `123456:ABC-DEF...`. Save it.

## Configuration in Surogate

Open the agent → **Configure** in the left nav → the **Channels** tab → find the **Telegram** card → **Connect**. A short walkthrough (BotFather → `/newbot` → copy token) ends in a single **Bot Token** field. Paste the token and click **Connect Telegram**. Once connected, the bot's `@username` is shown.

There is no separate save button — connecting and every later option change save automatically.

## Options (the Telegram "Manage" screen)

Once connected, the Telegram card shows **Manage**. The options there auto-save as you change them:

| Option | What it does |
|---|---|
| **Require @mention** (default OFF) | Only replies in groups when @mentioned. Off = replies to every message in groups it's added to. |
| **Mode** | **Team member** — members talk to a shared agent identity. **Personal assistant** — each user links their own Surogate account; unlinked users are prompted to link. |
| **Reply Threading** | **First chunk only**, **All chunks**, or **Off** — controls whether replies are threaded to the user's message. |
| **Message Reactions** | Show processing status via emoji reactions. |
| **Per-User Group Chats** | Each user in a group gets their own chat. |

Photos, voice notes, and documents are handled automatically — voice notes get transcribed if the model supports it, and documents (PDFs, etc.) get parsed.

## What users see

If the agent's **AI disclosure** is on (Configure → Governance), the disclosure text arrives as the first message of every new conversation — see [Governance & AI disclosure](../workflow/governance.md).

Users find your bot in Telegram by its `@username`. They start a DM and just type. If the bot is in a group:

- It responds when @mentioned (if Require @mention is on)
- Or to every message, if you leave Require @mention off and add it to the group

## Identity linking

Same model as Slack — a `(platform=telegram, platform_user_id=12345)` row in the channel-identity table links Telegram users to Surogate users.

## When the Telegram bot stops responding

The most common cause: **another instance is consuming Telegram updates**. Telegram only delivers each update once. If you have a dev environment also running with the same bot token, only one of them gets the messages. Stop the other.

## Reconnecting and disconnecting

- **Reconnect** reopens the walkthrough so you can paste a new bot token.
- **Disconnect** stops the bot from replying on Telegram. Your bot token stays in place — reconnect anytime.

## What's next

For embedding chat on your website: [Website widget](./website-widget.md).

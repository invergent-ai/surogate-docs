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

Open the agent → **CHANNELS** tab → toggle **Telegram** ON. The form expands:

| Field | What it does |
|---|---|
| **Bot Token** | Paste the token from BotFather |
| **DM only** vs **Allow in groups** | Restrict where the bot responds |
| **Forum topics** | If on, each topic in a group with topics is its own session |
| **Media handling** | Accept photos, voice notes (transcribed), documents |

Click **SAVE CHANNELS**.

## What users see

Users find your bot in Telegram by its `@username`. They start a DM and just type. If the bot is in a group:

- It responds when @mentioned (like Slack)
- Or always, if you've turned off the @mention requirement and added it to the group

Voice notes get transcribed automatically if the model supports it. Documents (PDFs, etc.) get parsed.

## Identity linking

Same model as Slack — a `(platform=telegram, platform_user_id=12345)` row in the channel-identity table links Telegram users to Surogate users.

## When the Telegram bot stops responding

The most common cause: **another instance is consuming Telegram updates**. Telegram only delivers each update once. If you have a dev environment also running with the same bot token, only one of them gets the messages. Stop the other.

## Toggling off

CHANNELS → Telegram OFF → SAVE. Same semantics as Slack.

## What's next

For embedding chat on your website: [Website widget](./website-widget.md).

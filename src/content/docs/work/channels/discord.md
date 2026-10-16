---
title: Discord channel
sidebar:
  label: Discord
---

Your agent as a bot in your Discord server and in direct messages. You use a bot of your own, so it carries your agent's name and picture.

## What you need

1. Open the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**, and give it your agent's name.
2. Open **Bot** → **Reset Token**, and copy the token.
3. Optional: under **Bot**, switch on **Message Content Intent** if the agent should read every message in some channels (see [Free-response channels](#options-the-discord-manage-screen)). Without it the bot still reads direct messages and every message that mentions it.

## Configuration in Surogate

Open the agent → **Publish** → the **Channels** tab → **Discord** under **Add a channel**. A short walkthrough ends in a single **Bot Token** field. Paste the token and click **Connect Discord**. Surogate checks the token with Discord and shows the bot's name; a token Discord refuses is rejected with the reason.

Then add the bot to your server: the Discord screen shows an **Install link** and an **Add to a server** button. Open it, pick a server you manage and authorize. The bot asks only for what it uses: view channels, send messages and messages in threads, read message history, attach files, embed links and add reactions.

Nothing else to paste: there is no webhook URL for Discord. Surogate keeps a live connection to Discord for your bot.

## Options (the Discord "Manage" screen)

The options save automatically as you change them.

| Option | What it does |
|---|---|
| **Require @mention** (default ON) | In servers, the agent answers only when it is @mentioned or someone replies to it. Direct messages always get an answer. |
| **Free-response channels** | Channel IDs (right-click a channel → **Copy Channel ID**, with Developer Mode on) where it answers every message without a mention. |
| **Read every message** | Asks Discord for the Message Content intent. Needed only for free-response channels. Switch the intent on in the Developer Portal first, or Discord refuses the connection. |
| **Mode** | **Team member**: everyone talks to a shared agent identity. **Personal assistant**: each person links their own Surogate account. |

Images and files people send reach the agent as attachments. Long answers are split at Discord's 2,000-character limit, and in servers the agent replies to the message that asked.

## Try it

**Try it** on the Discord screen opens your bot's profile, where you can message it directly. In a server, mention it: `@YourBot what's on today?`

## Reaching people first

The agent can write first to someone who has already talked to the bot, in a direct message, for [Programs](/work/tools/programs/) steps and team alerts. A **Slack, Teams or Discord channel** can also be a team's shared alert place.

## Reconnecting and disconnecting

- **Reconnect** reopens the walkthrough so you can paste a new token (after **Reset Token** in the portal, the old one stops working).
- **Disconnect** takes the bot offline. Its token stays in place, so you can reconnect anytime.

## When the bot stays offline

- **The token was reset** in the Developer Portal. Paste the new one with **Reconnect**.
- **Read every message is on, but the intent is off** in the portal. Switch one of them so they match.
- A bot in **100 or more servers** needs Discord's verification before Discord grants it the Message Content intent; that is Discord's review of your app, not a Surogate setting.

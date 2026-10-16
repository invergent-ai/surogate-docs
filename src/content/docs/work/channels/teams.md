---
title: Microsoft Teams channel
sidebar:
  label: Microsoft Teams
---

Your agent inside your organisation's Teams: in one-to-one chats, in group chats and in channels. It runs as an Azure Bot in your own Microsoft tenant, so your Teams admins stay in control of who can use it.

## What you need

- An Azure subscription where you can create an **Azure Bot**.
- Permission to upload a custom app to Teams, or a Teams admin who can publish it for you.

## Configuration in Surogate

Open the agent → **Publish** → the **Channels** tab → **Microsoft Teams** under **Add a channel**, and follow the four steps:

1. **Create an Azure Bot** in the Azure portal, with **Type of App: Single Tenant** and **Create new Microsoft App ID**.
2. From the bot's **Configuration** page, copy the **Microsoft App ID** and the **App Tenant ID** into Surogate.
3. Under **Manage Password**, create a **New client secret** and paste its **Value** (not the Secret ID).
4. Surogate shows a **Messaging endpoint** once the App ID is complete. Copy it into the same Configuration page in Azure, save, then open the bot's **Channels** and add **Microsoft Teams**.

Click **Connect Microsoft Teams**. Surogate asks Microsoft for a token with these credentials, the same check it makes before every reply, so a wrong ID or an expired secret is rejected at once with Microsoft's reason.

## Add it to Teams

People find the bot through a Teams app. On the Teams screen, **Download app package** gives you a ready zip (the bot, your agent's name and the Surogate icons). In Teams, open **Apps → Manage your apps → Upload an app**. If custom uploads are off in your organisation, a Teams admin can publish the package to everyone from the **Teams admin center**.

## Try it

**Try it** opens a chat with the bot once the app is installed for you. In a channel or group chat, @mention it: Teams delivers channel and group messages to a bot only when it is mentioned; one-to-one chats always reach it.

## Options

| Option | What it does |
|---|---|
| **Mode** | **Team member**: colleagues talk to a shared agent identity. **Personal assistant** links each person's Surogate account; on Teams, use Team member for now. |

Answers support Markdown (lists, tables, code). Images the agent produces are shown inline; other files are not sent on Teams yet.

## Reaching people first

The agent can write first to someone who has installed the app or written to the bot, for [Programs](/work/tools/programs/) steps and team alerts. A Teams channel can also be a team's shared alert place.

## Reconnecting and disconnecting

- **Reconnect** reopens the walkthrough, for example when the client secret expires (Azure secrets expire after the period you chose).
- **Disconnect** stops the agent replying in Teams. The credentials stay in place, so you can reconnect anytime.

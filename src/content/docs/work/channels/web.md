---
title: Web channel
sidebar:
  label: Web
---

The Web channel is **always on** for every deployed agent. Once the agent is `running`, anyone with the URL `https://<slug>.cloud.surogate.ai` can sign in and chat.

## What users see

A clean, branded chat UI with:

- The agent's name and avatar
- A composer at the bottom
- A session history sidebar (their own sessions only)
- File upload + download
- A live browser pane (if the agent is using browser tools)
- An inbox icon for items needing the user's attention

This is the customer-facing Web UI — a separate React app from `ops.surogate.ai`. Each user only sees what they're allowed to see (their sessions, their files).

## Who can sign in

Two modes:

1. **Anonymous** (default): visitors use the agent without an account. Each browser session gets a UUID stored locally; subsequent visits resume the same Surogate session.
2. **Authorised users only**: open the agent → **Configure** in the left nav → the **Users** tab → **Add user** for each authorised email.

For authorised users, they sign in with the credentials you set (email + password, Google SSO, or GitHub SSO).

## The endpoint

`https://<agent-slug>.cloud.surogate.ai`

The slug is set when you deploy the agent (the URL is what your team and customers will see, so pick something readable).

You can't change the slug after deployment — only via the dedicated **Rename** button on the agent's Configure page.

## Customising the look

For now, branding is limited to:

- The agent's **name** (shown at the top of the chat)
- The agent's **avatar** (uploaded in Settings → Profile or via a preset picker)
- The **favicon** (tied to the agent slug)

Full white-label (custom domain, your logo, your colours) is on the roadmap. If you need it sooner, embed the **Website widget** on your own domain instead — see [Website widget](/work/channels/website-widget/).

## What's next

If you want to also publish to Slack: [Slack channel](/work/channels/slack/). For Telegram: [Telegram channel](/work/channels/telegram/). Or for a customer site: [Website widget](/work/channels/website-widget/).

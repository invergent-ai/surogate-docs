---
title: Per-agent users
sidebar:
  label: Users
---

The **Users** section on an agent's Configure page manages the people who chat with this agent through its public Web endpoint. These are **distinct from your operator account** (your `ops.surogate.ai` login).

## When you'd use this

Three patterns:

- **Internal-only agent** — your team only. Don't add users here; only operators in your tenant can chat with the agent via `ops.surogate.ai`. The Web endpoint at `<slug>.cloud.surogate.ai` is locked down.
- **Closed customer-facing bot** — invite specific customers / partners. Add them one at a time. The Web endpoint requires sign-in.
- **Open sign-up** — let visitors create their own accounts via Firebase. Configure once at the project level, then toggle **Let anyone sign up** per agent. See [Self-registration](/work/channels/self-registration/).
- **Public-facing bot** — use the **Website widget** instead (see [Website widget](/work/channels/website-widget/)). Visitors are anonymous; identity is managed in your existing system.

## Adding a user

Open the agent → **Configure** in the left nav → the **Users** tab → **Add user**:

| Field | Notes |
|---|---|
| **Email** | The user's login email (required) |
| **Display name** | Optional — what shows up in chat. Defaults to the email's local part. |
| **Password** | Optional — set one for password login, or leave empty for SSO / self-registration |

Click **Send invite** — the user gets an email with a link to chat with this agent. The auth provider (Email & password, Google, or GitHub) shows up per user in the list once they sign in; SSO providers are configured project-wide through [Self-registration](/work/channels/self-registration/), not on this form.

## Identity across channels

A user on the Web endpoint is one identity. If they also use Slack, Telegram, or WhatsApp, their channel identities link to this same user. They see the same sessions across all channels.

Linking is prompted only when the channel is in **Personal assistant** mode (in **Team member** mode everyone shares the agent's identity and is never prompted). An unknown sender gets a private message from the bot with an 8-character pairing code (like `A3F7-K9M2`) and a link to the agent app's `/link` page — they sign in there, enter the code, and the identities pair. Codes live **10 minutes**, are single-use, and are minted at most once per user per 10 minutes; if the private message can't be delivered, the still-live code is re-sent on their next message. Users can also start from the web side: **Settings → Connected Channels → Link a channel**.

## Per-user usage limits

Usage is tracked per **(agent, end user)** — and because channel identities link, the limit follows the user across web, Slack, Telegram, and WhatsApp; switching channels doesn't reset it.

The controls live on the **Monetize** tab, not here: a **Per-user usage limit** for free agents, and the **Free trial** for monetized ones (see [Monetize](/work/monetize/#free-trial-and-per-user-limits)). There is no per-row override on this page. A user who hits their limit sees a clear message in their chat — with a buy link when the agent sells access.

Each user's recorded **sign-in method** (email/password, Google, GitHub; blank for accounts you created here) also decides which password controls they see in their own Settings — see [Web](/work/channels/web/).

## Managing existing users

The Users section shows every user with email, display name, auth provider, and when they were added. A search box filters the list. Per-row actions let you **Edit**, **Disable**/**Enable**, or **Delete** each one.

## Bulk operations

The Users tab adds people one at a time. To add many users at once, operators with admin permissions can script it against the REST API.

## What's next

You've covered channels. Loop back to your daily workflow at [Improve your agent](/work/workflow/improve-agent/), or jump to [Use cases](/work/use-cases/) for end-to-end recipes.

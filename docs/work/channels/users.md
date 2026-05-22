---
title: Users
sidebar_position: 5
---

# Per-agent users

The **USERS** tab on an agent manages the people who chat with this agent through its public Web endpoint. These are **distinct from your operator account** (your `ops.surogate.ai` login).

## When you'd use this

Three patterns:

- **Internal-only agent** — your team only. Don't add users here; only operators in your tenant can chat with the agent via `ops.surogate.ai`. The Web endpoint at `<slug>.cloud.surogate.ai` is locked down.
- **Closed customer-facing bot** — invite specific customers / partners. Add them one at a time, or bulk-add from CSV. The Web endpoint requires sign-in.
- **Public-facing bot** — use the **Website widget** instead (see [Website widget](./website-widget.md)). Visitors are anonymous; identity is managed in your existing system.

## Adding a user

USERS tab → **+ ADD USER**:

| Field | Notes |
|---|---|
| **Email** | The user's login email |
| **Display name** | Optional — what shows up in chat |
| **Password** | Optional — leave blank if you'd rather they use SSO |
| **SSO link** | Optional Google / GitHub login |

The user gets an invite email with the agent's public URL and instructions.

## Identity across channels

A user on the Web endpoint is one identity. If they also use Slack or Telegram, their channel identities link to this same user (via the channel-identity table). They see the same sessions across all channels.

If a user signs up on Slack first and you then add them on the Web, **the platform pairs the identities** via a flow where the Slack bot DMs them a pairing link.

## Managing existing users

The USERS tab shows every user with:

- Email
- Display name
- Last active timestamp
- Sessions count

You can:

- **Edit** — change display name, reset password, toggle SSO
- **Disable** — temporarily revoke access without deleting the user (sessions stay)
- **Delete** — remove the user and (optionally) their sessions

## Bulk operations

For >20 users, the per-row workflow is slow. Operators with admin permissions can use the REST API to bulk-add — see [Develop mode → REST API](/develop/reference/runtime-architecture).

## What's next

You've covered channels. Loop back to your daily workflow at [Improve your agent](../workflow/improve-agent.md), or jump to [Use cases](../use-cases.md) for end-to-end recipes.

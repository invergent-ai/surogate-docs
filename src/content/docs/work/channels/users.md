---
title: Users
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

A user on the Web endpoint is one identity. If they also use Slack or Telegram, their channel identities link to this same user. They see the same sessions across all channels.

If a user signs up on Slack first and you then add them on the Web, the platform pairs the identities via a flow where the Slack bot DMs them a pairing link.

## Managing existing users

The Users section shows every user with email, display name, auth provider, and when they were added. A search box filters the list. Per-row actions let you **Edit**, **Disable**/**Enable**, or **Delete** each one.

## Bulk operations

The Users tab adds people one at a time. To add many users at once, operators with admin permissions can script it against the REST API.

## What's next

You've covered channels. Loop back to your daily workflow at [Improve your agent](/work/workflow/improve-agent/), or jump to [Use cases](/work/use-cases/) for end-to-end recipes.

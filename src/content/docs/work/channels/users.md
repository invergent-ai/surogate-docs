---
title: Per-agent users
sidebar:
  label: Users
---

The **Users** tab on an agent's [Publish](/work/workflow/publish-agent/) page manages the people who chat with this agent through its public Web endpoint. These are **distinct from your operator account** (your `ops.surogate.ai` login).

## When you'd use this

Three patterns:

- **Internal-only agent** — your team only. Don't add users here; only operators in your tenant can chat with the agent via `ops.surogate.ai`. The Web endpoint at `<slug>.cloud.surogate.ai` is locked down.
- **Closed customer-facing bot** — invite specific customers / partners. Add them one at a time. The Web endpoint requires sign-in.
- **Open sign-up** — let visitors create their own accounts via Firebase. Configure once at the project level, then toggle **Let anyone sign up** per agent. See [Self-registration](/work/channels/self-registration/).
- **Public-facing bot** — use the **Website widget** instead (see [Website widget](/work/channels/website-widget/)). Visitors are anonymous; identity is managed in your existing system.

## Adding a user

![The Users tab: self-registration, search, Add user, and the agent's existing end users](../../../../assets/screenshots/work-publish-users.png)

Open the agent → **Publish** in the left nav → the **Users** tab → **Add user**:

| Field | Notes |
|---|---|
| **Email** | Their sign-in for the agent's web address. Give an email, a phone number, or both |
| **Phone** | Their WhatsApp number with country code, e.g. `+40 746 148 303`. Lets the agent recognise them on their first WhatsApp message. See [Enrolling by phone](#enrolling-by-phone-whatsapp) |
| **Slack member** | Optional — pick the person from the agent's Slack workspace. See [Linking a Slack member](#linking-a-slack-member) |
| **Permission to message them first** | The agent may open a conversation with them on the channel you bound. Needed before [Programs](/work/tools/programs/) can write to them |
| **Display name** | Optional — what shows up in chat. Defaults to the email's local part |
| **Password** | Optional — set one for password login, or leave empty for SSO / self-registration |

Click **Create user**. Nothing is emailed: a user with an email can sign in at the agent's web address straight away, and a user added with only a phone number is recognised on their first WhatsApp message, or when a journey step writes to them. If the email or number already belongs to an account, that account is linked to this agent as it is (a typed password is not applied) and the confirmation says whose it was. The auth provider (Email & password, Google, or GitHub) shows up per user in the list once they sign in; SSO providers are configured project-wide through [Self-registration](/work/channels/self-registration/), not on this form.

Someone reached only on Slack or Telegram can also be added from [Programs](/work/tools/programs/) or the agent's team tools, by Slack member or by name alone, with Telegram linked afterwards through a start link.

### Enrolling by phone (WhatsApp)

A user added with a phone number is bound to that number on WhatsApp straight away, with no pairing code: their first message from that number reaches the agent as them, and a journey step can open a conversation with them.

- **Give the country code.** The number is normalised to WhatsApp's own form (digits only, no `+`, no trunk `0`), so `+40 (0)746 148 303` and `0040746148303` both become the same number. A number without a country code is refused.
- **One number, one person, per organisation.** If the number already belongs to another user, the form says so and does nothing; it never moves a number silently. Use that existing user, or change their number first. A team member's number can be changed from their **Edit** panel on the Programs **Team** tab.
- **Permission is recorded, not assumed.** The checkbox stores who granted permission and when. It is shown next to each user in the list. Leaving it unticked still creates the user; they can chat with the agent, but no journey step will write to them first, and **Review & activate** warns about them. WhatsApp's business messaging policy requires this opt-in, and any obligations that apply to what your steps ask about are yours to confirm before rolling out.
- **Withdrawing permission** is done from the person's **Edit** form; see [Permission to message first](#permission-to-message-first).

### Linking a Slack member

A journey step on Slack reaches a person through their workspace **member id**, the way WhatsApp reaches them through a phone number. Bind it from the person's row: **Link Slack member** opens the agent's workspace directory, searchable by name or email, and stores the member you pick. The email is shown so you can recognise the right person; it is never used to match automatically, because a person's Slack email often differs from the one they were enrolled with.

The app has to be installed in that workspace, which connecting the [Slack channel](/work/channels/slack/) already does, and the person has to be a member of it. Someone who has already paired their own Slack account with the agent is bound already; you only record permission.

### Permission to message first

Permission is recorded per bound channel, with who granted it and when, and shown on the row. **Edit** a person to grant or withdraw it for WhatsApp and Slack separately. The runtime re-checks permission every time it is about to send, so a withdrawal takes effect at once: queued steps to that person are cancelled and future ones skip them with a reason. Re-activating a journey never restores it. A person who writes **STOP** withdraws it themselves; see [Stop and opt-out](/work/tools/programs/#stop-and-opt-out).

The row shows **No permission to message first** with a **Grant** button for someone who can be reached but has not agreed yet; **Grant** records their agreement, as said to you.

### Linking Telegram

A Telegram bot never sees phone numbers, so a person links themselves: **Link Telegram** in the row's menu makes a one-use start link (valid 48 hours) to send them. When they open it and press **Start**, they are asked whether they are that person and linked only on yes; pressing Start also records their agreement to be messaged on Telegram. See [Linking a person safely](/work/tools/programs/#linking-a-person-safely).

## Identity across channels

A user on the Web endpoint is one identity. If they also use Slack, Telegram, or WhatsApp, their channel identities link to this same user. They see the same sessions across all channels. A user enrolled with a phone number already has their WhatsApp identity, so they are never asked to pair. On a voice line with **Remember callers** on, a call from exactly that WhatsApp number is the same person too, sharing their record, memory and journeys; never matched by name, and without that switch every call stays its own.

Linking is prompted only when the channel is in **Personal assistant** mode (in **Team member** mode everyone shares the agent's identity and is never prompted). An unknown sender gets a private message from the bot with an 8-character pairing code (like `A3F7-K9M2`) and a link to the agent app's `/link` page — they sign in there, enter the code, and the identities pair. Codes live **10 minutes**, are single-use, and are minted at most once per user per 10 minutes; if the private message can't be delivered, the still-live code is re-sent on their next message. Users can also start from the web side: **Settings → Connected Channels → Link a channel**.

## Per-user usage limits

Usage is tracked per **(agent, end user)** — and because channel identities link, the limit follows the user across web, Slack, Telegram, and WhatsApp; switching channels doesn't reset it.

The controls live on the **Monetize** tab, not here: a **Per-user usage limit** for free agents, and the **Free trial** for monetized ones (see [Monetize](/work/monetize/#free-trial-and-per-user-limits)). There is no per-row override on this page. A user who hits their limit sees a clear message in their chat — with a buy link when the agent sells access.

Each user's recorded **sign-in method** (email/password, Google, GitHub; blank for accounts you created here) also decides which password controls they see in their own Settings — see [Web](/work/channels/web/).

## Managing existing users

The list shows every user with their channels (an icon each), email, auth provider, Slack and Telegram accounts, and when they were added; a **Team** tag marks members of the Programs team. Search by name or phone, filter by channel (every channel the agent has, with counts; empty ones dimmed), by **No permission to message first**, or by **Team**.

Click a name to open their person panel — the same one Programs, Sessions and the Inbox open, with their channels, timeline, contacts, conversations and escalations. The row's menu offers **Open person**, **Their conversations** (Sessions, filtered to them), **Edit**, **Link Slack member** / **Change Slack member**, **Link Telegram**, **Disable** / **Enable**, and **Delete**. Deleting removes them from this agent's user list and reports; their account and conversations are kept, other agents are unaffected, and you can add them again anytime.

## Bulk operations

The Users tab adds people one at a time. To add many users at once, operators with admin permissions can script it against the REST API.

## What's next

You've covered channels. Loop back to your daily workflow at [Improve your agent](/work/workflow/improve-agent/), or jump to [Use cases](/work/use-cases/) for end-to-end recipes.

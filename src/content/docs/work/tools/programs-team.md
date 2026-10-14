---
title: Team and escalations
---

The **Team** and **Escalations** tabs on an agent's [Programs](/work/tools/programs/) page decide who hears about it when the agent needs a person, and keep track of who is dealing with what. The agent decides when something needs the team; your colleagues handle it.

## Team tab

The team is the list of colleagues told when the agent escalates or someone stops replying. Each row shows the member, their role, what they handle, whether they can be alerted on their first channel (e.g. *WhatsApp on*), and **Edit** and **Remove**. Someone the agent follows can never join the team: they would receive everyone else's alerts.

Below the list are the **Shared alert place** and **Add team member**, and under the team, **Recent alerts and messages** sent in your organisation's name.

### Adding a team member

**Add team member** asks how to **Reach them on**. Only the channels the agent has connected are offered:

| Choice | What you give | How alerts reach them |
|---|---|---|
| **WhatsApp** | Their name and WhatsApp number | The first alert opens with your approved alert template; the full alert follows when they tap. |
| **Slack** | A member chosen from the workspace (name optional) | A direct message from the agent's Slack app. |
| **Telegram** | Their name | **Add and make a Start link** shows a one-use link to send them. They are on the team at once, marked *Pending: waiting for them to press Start*, and alerts reach them from then on. |
| **Studio inbox only** | Nothing | **Send alerts to my Studio inbox**: alerts land in your Studio Inbox and nobody is messaged. |
| **Someone already here** | Search by name or number | Someone the agent already knows, on the channel they use. |

Pick a **Role** too (see below). Adding a member records their consent to alerts on that channel.

### Editing a member

**Edit** opens their panel:

- **Name**.
- **How they are reached** — change their WhatsApp number, choose or change their Slack member, or link Telegram with a start link. Adding a way to reach them records their consent to alerts there.
- **Alert them first on** — the channel tried first. If that fails, the agent tries their other channels.
- **Role** and permissions, **Handles**, then **Save permissions**.

### Roles and permissions

Each member has what they **Receive** and what they **Can do**, from a role you can then edit item by item (it shows as **Custom** once changed):

| | Full | Assistant | Alerts only |
|---|:-:|:-:|:-:|
| Receives **Urgent alerts**, **Attention alerts** | ✓ | ✓ | ✓ |
| Receives **Missed replies**, **New people enrolled**, **Daily report**, **Delivery failures** | ✓ | ✓ | – |
| Can **See people and reports**, **Message a person**, **Enroll**, **Pause, resume or end**, **Edit details** | ✓ | ✓ | – |
| Can **See full phone numbers** | ✓ | ✓ | ✓ |
| Can **Manage the team** | ✓ | – | – |

A member added before roles existed is **Full**. Replies to a member's own requests always reach them, whatever they receive. The same rules apply in Studio and when they talk to the agent in chat (see [Team commands in chat](#team-commands-in-chat)).

**Handles** is a short note in your words, e.g. *medication questions, weekday mornings*. The agent reads it to choose who to alert: it can address an escalation to the members whose handles fit, and alerts everyone who receives that kind when it does not. Empty means anything.

### Shared alert place

A Slack channel the whole team watches can receive alerts too, besides each member. Give the **Slack channel ID** (in Slack, under the channel's name → About) and an optional **Name**, then **Add**. Invite the agent's Slack app to the channel first. A shared place receives urgent alerts, attention alerts and missed replies.

It needs Slack connected on the agent.

## Alerts

The agent raises an escalation with a severity:

| Severity | When | How it reads |
|---|---|---|
| **Urgent** (red) | The agent gave the person urgent instructions to get help now. | 🔴 before the reason; *🔴 Urgent* in the Inbox. |
| **Attention** (yellow) | Anything else that needs a person. This is the default. | *🟡 Needs attention* in the Inbox. |

A third kind comes from the platform rather than the agent: **missed replies**, when a person has not answered the last N steps of a journey (set on each step as **Alert the team after**).

Each member gets the kinds they receive, on their first channel, falling back to their others. On WhatsApp outside the 24-hour window an alert opens with your approved alert template (chosen under **Settings → Channels → WhatsApp**).

**An unopened urgent alert is sent again, once.** If no team member has read an urgent alert on WhatsApp after 30 minutes, it goes out again to the whole team, starting *🔴 Reminder, not yet opened after 30 minutes*, so a colleague can act when the first one is away from their phone. Read means WhatsApp's own read receipt.

Quiet hours never hold alerts to the team.

## Escalations tab

The queue of everything escalated, **Open** or **Resolved**. Each item shows its severity (**Red**, **Yellow**, **Missed replies**, or **Nobody told** when no one could be reached), the person (click to open their panel), the channel, the step if it came from one, the agent's reason, when, and **Unclaimed** or **Owner: …**. **Open conversation** jumps to the conversation it came from.

- **Claim** makes you the owner, so colleagues see it is being handled.
- **Resolve** closes it and moves it to **Resolved**. Resolving also closes its Inbox item.

Escalations are recorded even when they come from a conversation outside any journey, or from someone the agent does not know yet.

## In the Inbox

Every escalation also lands in the Studio [Inbox](/work/tools/inbox/), titled **Needs your attention: <person>**, addressed to the operator responsible: whoever activated the step it came from, or, outside a step, whoever last changed the team. The item reads *🔴 Urgent* or *🟡 Needs attention* with the person's name, and opens to **What happened**, the last messages of **The conversation**, **What the agent knows about them**, **Open conversation**, **View person**, **Claim** and **Resolve**. Claim and Resolve act on the same record as the Escalations tab. You cannot answer in the person's own chat from an Inbox item.

## Team commands in chat

A team member can work with the agent from their own chat on any channel they are reached on, within their permissions. They just ask in their own words; the agent uses these tools:

| Tool | What the team member can ask |
|---|---|
| `team_overview` | A digest of everyone followed: their journey, day, status, last reply and last step's outcome, recent alerts, and the next send. Or one person in detail. Phone numbers are masked; a member allowed to see them can ask for a number, which comes in a separate message. |
| `team_message_person` | Send a person their message, word for word, on the person's preferred or last-used channel. The agent shows a preview first and sends only after a yes. Inside the person's quiet hours the message waits, and the preview says when it will arrive in the person's local time; they can ask to send it now. |
| `team_update_person` | Pause, resume or end someone's follow-up, correct their start date, name, who answers for them, timezone or preferred channel. Previewed first, changed only after a yes. |
| `team_enroll_person` | Enrol someone by WhatsApp number, Slack member, a Telegram start link, or as someone the agent already knows. Previewed first. |

Whoever enrols someone by number or Slack member vouches for their consent; the welcome message goes out at once.

<!-- TODO verify: claiming and resolving an escalation from chat (design round 2, item C: "owner/claim/resolve from Studio and from chat (team tool), and the rest of the team told who took it") is not in the runtime's team tools as of 4a3d69c64. Document once a tool ships. -->

## What's next

- [Programs](/work/tools/programs/) — journeys, steps and people.
- [Inbox](/work/tools/inbox/) — the rest of what the agent raises to you.

---
title: Programs
---

A **Program** is a scheduled check-in the agent starts. On a cadence you set, it sends each enrolled person an approved WhatsApp message, waits for their reply, runs a skill with them when they answer, and records how it went. A clinic checking on post-operative patients every morning and evening is the case it was built for.

A Program is five things: a **skill** (the questions), a **cadence** (which weekdays, at which local times, in which timezone), a **WhatsApp sender**, an **opener** (the Meta-approved template that starts the conversation), and a **roster** of patients. Ops holds that configuration; the agent runtime does the sending and keeps the per-patient record.

Open it from an agent's left navigation (**Programs**, under the agent) or go to `/work/agents/<agentId>/programs`. The entry appears only when the Programs capability is on for that agent.

Programs run on WhatsApp only. Telegram cannot be used because a bot may not write first there, and the website widget has no number to write to.

## Before you start

Five things have to be in place, and the activation gate checks every one of them:

1. **WhatsApp connected**, with the **WhatsApp Business Account ID** filled in — see [WhatsApp](/work/channels/whatsapp/). The account id is what the Templates screen and the activation gate talk to Meta with.
2. **An approved template** — the opener. Register it under **Publish → Channels → WhatsApp → Manage → Templates** and wait for Meta to approve it; see [Templates](/work/channels/whatsapp/#templates-the-check-in-opener). Keep it short and fixed: *Time for your check-in with Dr Ionescu. Reply to begin.* The questions do not go in it.
3. **Patients enrolled by phone, with permission** — add them on the agent's **Users** tab with a phone number and the **Permission to message them** box ticked; see [Enrolling by phone](/work/channels/users/#enrolling-by-phone-whatsapp).
4. **A skill with the questions** — an ordinary [skill](/work/library/skills/) available to the agent. The agent runs it when the patient replies, so write it as the conversation you want held: what to ask, in what order, what counts as done, and when to escalate.
5. **The capability on** — **Configure → Capabilities → Programs**. It is off by default because a Program messages real people on a schedule.

A skill edit reaches the agent when the agent's bundle is republished, not the moment it is saved. Check the bundle before assuming a corrected question is live.

## Creating a Program

Click **New Program** and fill in the form. Saving creates a **draft**; nothing is sent until you activate.

| Field | Notes |
|---|---|
| **Name** | For your own list, e.g. *Post-op daily check-in*. |
| **Skill** | The skill reference the agent runs on reply, e.g. `post-op-checkin`. |
| **WhatsApp phone number id** | Meta's id for the sending number, the same value as the channel's **Phone Number ID**. |
| **Template (the opener)** | The approved template's name, e.g. `daily_checkin`. |
| **Template language** | The template's language code, e.g. `en_US`. A template is approved per language; name and language have to match what Meta shows. |
| **Days** | The weekdays it fires. |
| **Times of day** | One or more local times, `HH:MM` on a 24-hour clock, e.g. `09:00, 21:00`. |
| **Timezone** | A named zone such as `Europe/Bucharest`. An offset like `+03:00` is refused: it cannot follow daylight-saving changes. |
| **Reply deadline (hours)** | How long after the opener a patient has to reply before the check-in is recorded as unanswered. Default 24. |

The cadence is a set of weekdays and local times, never an interval. Two times on the same day are two separate check-ins; the row shows the next one, in the Program's own zone, so twice-daily Programs show the next *time*, not the next day.

### The roster

Patients are agent users with a phone number and recorded permission. A Program's roster is the set of them it messages. In this release the roster is managed through the API rather than the page; the page shows the count.

```
POST   /api/programs/<program_id>/patients            {"user_id": "<user uuid>"}
DELETE /api/programs/<program_id>/patients/<user_id>
```

User ids come from `GET /api/agents/agents/<agent_id>/users`. A user id that does not belong to this agent's project is refused. The roster is the denominator every run counts against: a patient who cannot be reached on a given run stays on it, marked skipped, rather than disappearing from the count.

## Activating

**Activate** either turns the Program on or refuses and tells you everything that is wrong at once, so you can fix it in one pass rather than one save at a time. The blockers it can name:

- the Programs capability is off for this agent;
- no weekday, no time, an unparseable time, or an offset instead of a named timezone;
- no skill, or no sender number;
- no template, or a template name without its language;
- the template is not on this WhatsApp account, or Meta reports it as anything other than approved;
- the roster is empty;
- a patient on the roster has no phone number, or has not given permission.

Whoever activates a Program becomes its **responsible operator**: escalations from its check-ins land in that person's [Inbox](/work/tools/inbox/).

Once active, the row shows the **next run** in the Program's timezone. Edits that would break the gate on an active Program are refused; pause it first. Removing the last patient from an active Program is refused for the same reason.

## What happens on a run

At each slot the runtime opens an **occurrence** and writes one row per patient on the roster.

1. **Skipped patients are recorded first.** A patient whose permission has been withdrawn, whose number is gone, or whose previous check-in is still open (*Previous check-in still open*) gets a row with that reason and is not messaged.
2. **The opener goes out** to everyone else, as the approved template, through the same delivery path as the agent's replies. Permission is re-checked at the moment of sending, so a withdrawal between the slot and the send still holds.
3. **The reply deadline starts** when the opener is handed over. Meta's delivery reports move the row from *Queued* to *Sent* and *Delivered*, or to *Failed* with Meta's reason.
4. **When the patient replies**, the message lands in their own WhatsApp conversation with the agent, and the agent is told to run the Program's skill with them now. Only a first reply within the deadline counts; the conversation then continues as an ordinary WhatsApp chat inside Meta's 24-hour window.
5. **The agent closes the check-in** with `checkin_outcome` — *Completed* when it got the answers, *Declined* when the person refused or asked to be left alone. If something in the answers needs a human, it calls `checkin_escalate`, which raises **Check-in needs your attention** in the responsible operator's Inbox without ending the check-in.
6. **The deadline sweep** records what never finished. A delivered opener nobody answered becomes *No reply by deadline*. A reply the agent never closed becomes *Answered, not finished*. An opener that never reached the patient goes back to *Not started*, so one failed send never blocks that patient's next check-in.

A patient has at most one open check-in per agent. If a Program is paused, its unsent openers are withdrawn; openers already handed to Meta cannot be recalled. After an outage, a slot whose reply window has already passed is skipped rather than sent late: nobody receives yesterday's "good morning" this afternoon.

## Reading the results

Every row on the Programs page carries the outcome of its last run in one line, so a broken Program is visible without opening anything:

> Sent to 12 of 14. 2 skipped: no permission to message. 7 replied; 5 no reply by the deadline. 1 escalated.

A line that reads *Sent to 0 of 14. 14 not yet sent.* an hour after the slot means the openers are stuck, not that nobody answered.

Click a Program's name to open its **run history**: a chip per occurrence, newest first, and for the selected one a table with a row per patient.

Delivery, response and escalation are three separate columns because they are three separate facts. A failed send must never read as a patient who stayed silent.

| Column | Values |
|---|---|
| **Delivery** | *Queued*, *Sent*, *Delivered*, *Failed*, *Undelivered*, *Skipped*, *Cancelled* |
| **Response** | *Not started*, *Awaiting reply*, *Replied*, *Completed*, *Declined*, *Answered, not finished*, *No reply by deadline* |
| **Escalation** | — , *Escalated*, *Escalation failed* |
| **Reason** | Why a patient was skipped or cancelled, or Meta's error text for a failed send |

The filters above the table (**Everyone**, **Failures**, **Skipped patients**, **No reply**, **Escalated**) narrow the rows; the counts in their labels are over the whole roster.

## Pausing, resuming and deleting

- **Pause** stops new openers on the runtime's next scheduling pass and withdraws any not yet sent. History stays.
- **Resume** (**Activate** on a paused Program) re-runs the gate and starts at the next future slot. Missed slots are not sent.
- **Delete** asks for confirmation, then removes the Program and its roster. Past runs stay in the runtime's records but are no longer reachable from the page.
- Turning the **Programs capability off** is refused while any Program on the agent is active. Pause them first; otherwise the runtime would stop running them while the page still said *Active*.

## Limits in this release

- WhatsApp only; one fixed-text opener per Program, in one language; no variables in the template.
- No reminder after a missed check-in. The next slot simply comes round.
- While your Meta app is in development mode, Meta delivers only to the numbers on its recipient list, so a Program appears to work for you and fail for everyone else. That is Meta's restriction, not the gate's.
- The roster is managed through the API, as described above.

## What's next

- [WhatsApp](/work/channels/whatsapp/) for the connection and the Templates screen.
- [Users](/work/channels/users/) for enrolling patients by phone.
- [Skills](/work/library/skills/) for writing the questions.
- [Inbox](/work/tools/inbox/) for where escalations arrive.

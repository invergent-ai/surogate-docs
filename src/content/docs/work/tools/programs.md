---
title: Programs
---

**Programs** is where an agent reaches people first. You tell it who to follow and on which days to write; the agent writes each message itself, follows up on the reply, and alerts your team when something needs a person. People, the steps they get, the team, the escalations and the settings all live on one page.

Open it from an agent's left navigation (**Programs**, under the agent) or go to `/work/agents/<agentId>/programs`. The entry appears only when the Programs capability is on for that agent.

The words this page uses:

| Word | Meaning |
|---|---|
| **Person** | Someone the agent follows. They may be reached on WhatsApp, Slack, Telegram, a phone call, web chat or your own app. |
| **Journey** | A set of steps every person in it gets, counted from their own start date. One agent can have several journeys, e.g. *Onboarding* and *Renewal*. |
| **Step** | One message (or call) in a journey: when it goes out, on which channel, and what the agent does with the reply. |
| **Day 0** | The date a person's journey counts from: their start date. Day 3 is three days after it; day -1 is the day before it. |
| **Team** | The colleagues told when the agent escalates or someone stops replying. See [Team and escalations](/work/tools/programs-team/). |
| **Escalation** | Something the agent decided a person on the team should look at. |

## Before you start

1. **Turn the capability on**: **Configure → Capabilities → Programs**. It is off by default because Programs message real people. While any step is active, turning it off is refused; pause the journeys first.
2. **Connect a channel the agent can write first on**: WhatsApp, Slack, Telegram, or Voice with an outbound line. Web chat and your own app through the [Programs API](/work/tools/programs-api/) also count. See [How each channel reaches people](#how-each-channel-reaches-people).
3. **On WhatsApp, have an approved template.** Outside its 24-hour window WhatsApp opens a chat only with a text Meta approved. Register one under **Publish → Channels**: open the **WhatsApp** row under **Live**, then **Templates**; see [Templates](/work/channels/whatsapp/#templates-the-opener).
4. **Attach a skill with the instructions.** An ordinary [skill](/work/library/skills/) on the agent: what to ask, what counts as done, when to alert the team. A step names the skill it follows.
5. **Add yourself to the team** under the **Team** tab, so a test send has somewhere to go and escalations reach someone.

## The page

The header strip shows four numbers, each a shortcut to its tab: **People followed** (with paused and ended counts), **Messages, last 24 h** (with replies and no-replies), **Alerts, last 24 h**, and **Next send**.

Below it are five tabs:

| Tab | What it holds |
|---|---|
| **People** | Everyone enrolled in a journey: where they are, their next send, their last reply, their channels. |
| **Journeys** | Each journey's steps on a day timeline, their stats, and **Review & activate**. |
| **Team** | Who is told when something needs a person, on which channel, and what each may do. See [Team and escalations](/work/tools/programs-team/). |
| **Escalations** | The open and resolved escalations, with **Claim** and **Resolve**. |
| **Settings** | The journey's timezone, quiet hours and end; your wording; packages; each channel's sender. |

Every tab keeps itself current while it is open; you never need to refresh.

## Journeys tab

<!-- TODO verify: add a screenshot of the Journeys tab (work-programs-journeys.png) once the release is deployed. -->

The switcher at the top picks a journey (or **Fixed lists of people**, see [below](#fixed-lists-of-people)). Next to it: the journey's status (**Draft**, **Active** or **Paused**), **New journey**, and **Review & activate** (or **Pause** once it is live). Under the switcher: how many people are active in it, its key and its timezone.

Steps are shown on a vertical timeline grouped **Before**, **Day 0**, **Week 1**, **Weeks 2–4**, **Months 2–6** and **Later**. Each row says when it goes out (*Day 3 at 09:00*, *Days 1–7, daily at 09:00*), how long it waits for a reply, the channels it can use, its next send once active, and its numbers so far (*12 sent · 58% replied*). Each row also says what goes out: on WhatsApp the template as the person reads it (its header, its button and the form it opens), elsewhere *Agent writes it · default: «…»* with the step's default wording. **Preview** opens it under the row (a bottom sheet on a phone; Esc closes it): the message as a chat bubble, the form with its options, and the step's instructions under **What the agent does**. Template pickers in the wizard, the drawer and Settings show templates the same way, with a preview. Click a step to open it in the drawer; the **⋯** menu also offers **Pause this step**, **Activate this step** and **Delete**.

**Steps | Stats** switches the list to a table with one row per step and the columns **Sent**, **Delivered**, **Read**, **Replied**, **Completed**, **No reply**, **Failed** and **Skipped**, over the **Last 7**, **30** or **90 days**. Under each row: the outcomes the agent recorded, why people were skipped, and the channels used. Read is counted where the channel reports it (WhatsApp).

### Creating a journey

**New journey** opens a wizard of four short screens. Nothing is sent when you finish: the journey starts as a **draft**.

1. **Start.** Pick a starting point. Every step can be changed later.

   | Preset | Steps |
   |---|---|
   | **Health follow-up** | A welcome, daily in the first week, twice a week in weeks 2–4, then reviews at months 2, 3 and 6. |
   | **Customer onboarding** | Welcome, first steps, a tip, then feedback at two weeks and a month. |
   | **Sales follow-up** | An introduction, two follow-ups and a last nudge, then it stops. |
   | **Appointment reminders** | Confirm the booking, remind the day before, ask how it went. |
   | **Blank** | No steps yet. |

2. **People.**
   - **Name** — prefilled from the preset.
   - **Key** — people are enrolled under this key, by the agent, by a package or by you. It cannot change later.
   - **Timezone** — for people who have not set their own.
   - **How people join** — *The agent enrols them in conversation, with their consent*; *You enrol them under People*; or *They buy a package* (then pick the package; see [Monetize](/work/monetize/)).
   - **Finish after** (days, optional) — counted from each person's start date. Empty means they stay until someone ends it.
3. **Channels & team.** The accounts the agent sends from, and on WhatsApp the **Opening template** every step uses until you give one its own. Under **Team alerts**, pick which channel each team member is alerted on first.
4. **Review.** A sentence that sums the journey up, its steps, and **Instructions for these steps**: the skill every step follows until you give one its own. **Create journey** saves it as a draft and highlights **Review & activate**.

### Steps

**Add step**, or a click on an existing one, opens the step drawer. It has four sections.

**When**

| Field | Notes |
|---|---|
| **Name** | Only your team sees it, e.g. *Morning message, first week*. |
| **Sent** | **Once** (on one day) or **Repeating** (over a range of days). |
| **On day** / **From day** · **Until day** | Counted from the person's start date. **Negative days come before it**: day -1 is the day before. An empty **Until day** means no end. |
| **On these days** | The weekdays a repeating step fires on. |
| **Send once per person** | Fires on the first matching day in the step's window, then never again for that person, even if re-enrolled. Not offered on a **Once** step with a single time. |

Skipped, cancelled or failed sends don't count, so the next matching day tries again. A copy received as someone else's contact doesn't count as theirs. The timeline shows *once per person* on the step.

| **At** | One or more local times. **Add a time** for twice a day. |
| **Timezone** | People with their own zone get the step at this time in theirs. |
| **Only some people** | Optional: **Only people in these stages** (a label you or the agent put on a person, comma-separated) and **Only if they have not written for** N days, for an "are you still there?" message. |

**Channel & content**

| Field | Notes |
|---|---|
| **Send from** | The step's main channel and the account it writes from. |
| **WhatsApp template** · **Language** | The approved template that opens a WhatsApp chat once its 24-hour window has closed. **Preview what they receive** shows it, with its form if it has one. |
| **Data passed to the form** | When the template has a form button: values the form shows where it reads `${data.<key>}`, so one form can serve several steps. |
| **Default wording** | The wording the agent starts from on text channels, and sends as is when it has nothing to add. |

**Reply & follow-through**

| Field | Notes |
|---|---|
| **Wait for a reply** (hours) | When this passes with no reply, the agent looks at the conversation and decides: a nudge, an alert to the team, a pause, or nothing. 1 to 168 hours, default 24. |
| **Alert the team after** (missed in a row) | The platform's default: if the agent has not acted after this many missed in a row, the team is alerted. Empty means no alert. |
| **Stop sending after** (missed in a row) | The platform's default: stop sending this person steps until they write again. Empty means keep sending. |
| **Alert text** | Optional. `{name}`, `{phone}`, `{count}` and `{program}` are filled in. |

**Instructions**

| Field | Notes |
|---|---|
| **Skill** | What the agent asks and watches for once someone replies. **Read the instructions** previews it. Only skills attached to the agent are offered. |

A skill edit reaches the agent when its bundle is republished, not the moment it is saved.

### How a step goes out

When a step is due for a person, the agent is woken in that person's conversation with a short context block: the journey and step, which day it is for them and their local date, who is writing, how their last steps went, their last form answers, and why it is awake. It then writes the message in its own words, following the step's skill, or decides it is not needed and records why.

- **On WhatsApp, outside the 24-hour window**, the step's approved template goes first, and the agent carries on in its own words once the person answers.
- **When the person answers**, the agent is woken again with the same context, runs the step's skill with them, and records the result with `step_outcome` (for example *completed* or *declined*, with a label such as *red*).
- **When the wait passes with no reply**, the agent is woken once more and decides what to do. **Alert the team after** and **Stop sending after** apply only if it did nothing.
- **One open question per journey.** A person never has two steps of the same journey waiting for an answer; the next one is skipped with *An earlier step is still waiting for an answer*. A reply on any of their channels answers the step opened most recently.

### How the channel is chosen

For each person and each step, the agent writes on:

1. the person's **preferred channel**, when they have one and can be reached there;
2. else the channel **they last wrote on**;
3. else the **step's own channel**.

Reachable means they have an account linked there, have agreed to be contacted there, and the agent has a sender on that channel. On Telegram they must also have written to the bot at least once.

**If a message cannot be delivered** (for example WhatsApp reports it failed), the same step moves to the person's next reachable channel at once. The team hears that a message did not arrive only once every channel has failed. There is no timer: a message that was delivered but not answered does not move.

### Quiet hours, timezones and finishing

These live on the **Settings** tab, in the **Journey** card.

- **Timezone** — for people without their own. A person's own timezone (under People → **Edit details**) makes every step reach them at its local time in their zone.
- **Quiet hours, in each person's own time** — a step due inside them waits and goes out when they end, e.g. at 08:00 for 21:00–08:00. Team members' messages to a person wait too, and the team member is told when it will arrive; they can send it at once instead. Alerts to the team are never held. Review warns when every send time of a step falls in quiet hours.
- **Finish after** (days from the start date) — people past it are ended with the reason *Journey finished*. Empty means they stay until someone ends their follow-up.

### Review & activate

**Review & activate** opens a panel with three parts.

**Checklist.** Blocking problems disable **Activate**; warnings do not. Each item has a **Fix** link to where it is fixed. It blocks when there is no step, or a step fails its own check (no skill, no sender, a WhatsApp step without an approved template, a timezone given as an offset). It warns when a step has no content for another channel the agent sends on, steps use different timezones, every send time falls in quiet hours, nobody is on the team, nobody is enrolled yet, or some enrolled people cannot be messaged on any of the journey's channels. **Check again** re-runs it.

**Send a test.** Pick a step and a team member: the step's opener (its template on WhatsApp, else its default wording) goes to them now, on the first of the step's channels they can be reached on. *Queued. It arrives within a minute.*

**Dry run.** Pick a **Start date** and a number of **Days** (up to 90, default 14): the list shows, day by day in the journey's timezone, what one person starting that day would get. A step sent only after silence is marked as such (*only if silent 3 days*). Nothing is sent. It shows a future start date's days-before steps too.

**Activate** turns on every step that is not already active. If something changed since you opened the panel, the refusal lists every problem at once.

### Pausing, resuming and deleting

- **Pause** (confirmed first) stops every step: *No step sends until you activate it again. People stay in it, and the agent still answers anyone who writes.* Resume with **Review & activate**; missed sends are not made up.
- A single step can be paused or activated from its **⋯** menu.
- **Delete** is offered only while the journey is not active: its steps are removed for good, and the people in it and their conversations stay.
- **Delete step** stops it sending; past runs are kept but no longer shown.

### A step's recent runs

An open step shows its **Recent runs**: one line per send time with chips such as *12/14 sent*, *7 replied*, *5 no reply*, *1 escalated*, *2 not needed* (the agent decided no message was needed) and *1 handled by agent* (a missed reply the agent dealt with itself). Expand a run to see one row per person, filtered by **Escalated**, **No reply**, **Failures** or **Skipped**, each with:

| | Values |
|---|---|
| **Delivery** | *Queued*, *Sent*, *Delivered*, *Failed*, *Undelivered*, *Skipped*, *Cancelled* |
| **Response** | *Not started*, *Awaiting reply*, *Replied*, *In progress*, *Completed*, *Declined*, *Answered, not finished*, *No reply by deadline*, *Agent decided no message was needed* (with its note), *Answered by a contact* |
| **Escalation** | *Escalated*, *Escalation failed*, *Agent handled the missed reply* |

Delivery and response are separate because they are separate facts: a failed send never reads as a person who stayed silent. Click a person to open their panel, or open the conversation.

### Fixed lists of people

Under the journey switcher, **Fixed lists of people** holds schedules that are not part of a journey: a step sent to the people you tick, on the weekdays and times you set, with no day counting. **New schedule** opens the same drawer without the day fields, and an open schedule lists the agent's users with a checkbox each and whether they can be reached on its channel.

## People tab

<!-- TODO verify: add a screenshot of the People tab (work-programs-people.png) once the release is deployed. -->

One row per person and journey: **Person** (with their number and who answers for them, e.g. *with Ana (daughter)*), **Journey and step** (the journey, their day and current step), **Next send** (in their own time), **Last reply** (on any channel), **Channels** and **Status**. Each channel chip is green when they agreed to be contacted there.

Filter by **All / Active / Paused / Ended**, by journey, by stage, by channel, or search by name or number. **Export CSV** downloads every step sent (one row per step and recipient, with delivery, read time, response, label, form answers and escalation), for one journey or all.

People ever enrolled in a journey (even one that has ended), their confirmed contacts and your team never need a plan on a [monetized](/work/monetize/#people-you-bring-in-never-need-a-plan) agent: they can write on any channel, unmetered.

**Enrol someone** picks a person the agent already knows, a journey and **Day 0**. It is offered once at least one journey is active. The agent can also enrol people in conversation, with their consent; a package can enrol its buyer; and your own software can enrol people through the [Programs API](/work/tools/programs-api/).

### The person panel

Click a person to open their panel. The same panel opens from Users, Sessions, Inbox and Escalations.

- **Message** sends them your text word for word, in your name, on the channel the agent would use. Inside their quiet hours it waits, and Studio says when it will reach them in their own time; tick **Send now, even in their quiet hours** to send it at once. A message already waiting shows *Held for their quiet hours, until …* under **Messages and alerts**, with **Send now**. A newer message from the same team member to the same person replaces one still held, so the outdated one never goes out.
- **Pause**, **Resume** and **End** ask for a reason.
- **Channels** shows each account and its consent. **Link Telegram** makes a start link; see [Linking a person safely](#linking-a-person-safely).
- **What the agent knows** — the agent's memory of this person.
- **Messages and alerts** — what was sent to or about them, with its state.
- **Timeline** — newest first: enrolled, paused, ended, each step with its delivery and answer, the label the agent recorded, form answers field by field, escalations and team messages. Each links to its conversation.
- **Contacts** — see below.
- **Conversations** and **Escalations** for this person.
- **Edit details** — name, **Answered by**, **Start date (day 0)** (with **Approximate**), **Phase**, **Timezone** (*The journey's* or their own) and **Preferred channel** (*No preference* or one of their channels). A preferred channel is accepted only where the agent has a sender and the person has an account and has agreed to be contacted.

### Followed people and their contacts

The person in a journey is the one followed, a person of their own even without a phone. **Contacts** are people who answer for them, such as a relative or a carer, each with their own channels and a relation in your words (*daughter*, *carer*).

**Every step goes to the person and to every confirmed contact**, each on the channel chosen for them. An answer from any of them answers the step for all: the other copies read *Answered by a contact*, and the agent knows who answered. While any copy is still waiting for an answer, the next step waits too. Stats and missed-reply alerts count people, not copies. The person and their contacts share one record and memory, which the agent sees from any of their conversations. A contact's own panel says *Answers for …*.

A contact is linked:

- from the person panel: **Add contact**, name the **Relation**, then pick the person (they must already be one of the agent's users);
- by the agent in conversation, when the person or an already linked contact gives a number, matched **exactly**;
- or after a confirmation: when someone the agent does not know says they are a relative, the agent asks an already linked contact in their own chat whether that number is theirs, and falls back to the team (as an escalation) when nobody can be asked. A link is never made on a name alone, or on the newcomer's word alone.

A link waiting for that confirmation shows **Confirm link**; **Remove** stops them receiving this person's steps and keeps their own record.

Example: in a health follow-up, Ana enrols her father; he becomes the followed person with his own number, and Ana is his contact with the relation *daughter*. An alert about him names him and says Ana reported it.


### Linking a person safely

A person is never matched on a name. Accounts are linked by:

- **The exact number.** A WhatsApp number given with its country code is that person on WhatsApp. On a voice line with **Remember callers** on, a call from exactly that number is the same person too, with the same record, memory and journeys. Without that switch every call stays its own, because caller ID can be faked.
- **A Telegram start link.** A Telegram bot never sees phone numbers and may only write to someone who started it, so the person comes to the bot. **Link Telegram** (on the person panel, on the Users tab, or when adding a team member) makes a one-use link that works for **48 hours**. Whoever opens it and presses **Start** is asked *Are you {name}?* and is linked only on **Yes**. The person (on their other channel) and the team are told either way.
- **A confirmation by a known contact**, as above.

### Stop and opt-out

A person who writes **STOP** (or *unsubscribe*, *opt out*, and a few equivalents in other languages) on a channel is honoured before the agent even reads it: their permission on that channel is withdrawn and, for a followed person, their follow-up ends. The agent also stops when someone asks in their own words. A contact who stops just stops receiving the steps. The team is told once. A team member's "stop" is not an opt-out: it reaches the agent as an ordinary message, so they keep getting alerts.

## Settings tab

General settings first, then each channel:

- **Journey** — the selected journey's timezone, quiet hours and **Finish after**; see [above](#quiet-hours-timezones-and-finishing).
- **Messages** — your wording, on every channel, each named by purpose with a line on when it is used. First what people read (**Welcome**, and the Telegram linking question and answers, e.g. **Linking: are you them?**), then **To your team** (e.g. **Your message did not arrive**, **Urgent alert not opened**, **Someone took a case**, **A case was resolved**, **Telegram linked**), **Why a message didn't arrive** (each reason filled into those notices), **Plans and limits** (e.g. **Free trial ending**, **Free allowance used**, **Channel not in their plan**) and **Checkout fields**. Empty fields use the default shown; words in braces such as `{name}` are filled in.
- **Packages** — which journey a package's buyer joins. A package pointing at a journey that is not active warns that a buyer would join but hear nothing.
- **Channels** — each connected channel the agent writes first on, and the account it sends from. On WhatsApp: which approved template opens a closed chat for **An alert to the team**, **Your message to someone** and **A welcome after a purchase**, plus the wording used when a WhatsApp message cannot go out. **Manage templates** opens the Templates screen.

## How each channel reaches people

| Channel | Writing first | Notes |
|---|---|---|
| **WhatsApp** | Yes | Outside the 24-hour window only an approved template can open the chat; inside it the agent writes freely. Templates can carry quick-reply buttons and a **form button** that opens a native WhatsApp form. Reports delivered and read. See [WhatsApp](/work/channels/whatsapp/). |
| **Slack** | Yes | A direct message from the agent's Slack app, at any time; no templates. Needs **Personal assistant** mode. See [Slack](/work/channels/slack/#programs-on-slack). |
| **Telegram** | Yes, once they started the bot | The agent can write only to someone who pressed **Start**; a start link does that. No templates. See [Telegram](/work/channels/telegram/). |
| **Voice** | Yes, as a phone call | A step on Voice is a call from the agent's number: the agent talks it through and what they say is recorded like a reply. Busy, no answer or declined counts as failed, so the step moves to the next channel. Quiet hours apply to people; an urgent alert can ring a team member at any hour. Needs an outbound line on the number. |
| **Web chat** | Waits for their visit | A due step waits in the person's web chat and shows on their next visit. With **Browser notifications** on (Settings → Channels, when the platform has push set up), people who allowed notifications are told in their browser. |
| **Your app (API)** | Through your webhook | Steps for people you reach in your own app go to your webhook, and your app reports delivery and replies back. See [Programs API](/work/tools/programs-api/). |
| **Website widget** | No | Its visitors are anonymous, so there is no one to write to. |

Microsoft Teams and email cannot be used for Programs yet. Outbound calls are switched on for the platform by your administrator, with an outbound phone line (SIP trunk) for the agent's number.


## Limits in this release

- Branching between steps is not configured: the agent decides what happens next, with its tools and the person's history.
- While your Meta app is in development mode, Meta delivers only to the numbers on its recipient list, so steps seem to work for you and fail for everyone else.

## What's next

- [Team and escalations](/work/tools/programs-team/) — who hears about what, and the escalation queue.
- [Programs API and webhooks](/work/tools/programs-api/) — enrol people and hear about their steps from your own software.
- [WhatsApp](/work/channels/whatsapp/) for templates and forms.
- [Users](/work/channels/users/) for the people the agent knows.

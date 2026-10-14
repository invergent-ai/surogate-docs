---
title: What's new
---

<!-- TODO verify: put the release's version numbers (ops and runtime) and date in the heading below once the release is cut. -->

## October 2026

### Programs: journeys, a team and escalations, on any channel

[Programs](/work/tools/programs/) now reaches people on the channels they use, not only WhatsApp, and the agent does the writing.

- **Journeys.** The Programs page's former Check-ins tab is now the **Journeys** tab: each journey is a set of steps every person in it gets, counted from their own start date, shown on a day timeline. Steps can come before the start date (day -1 is the day before), for reminders ahead of an appointment.
- **A wizard and presets.** **New journey** sets one up in four short screens, from a preset (Health follow-up, Customer onboarding, Sales follow-up, Appointment reminders) or blank.
- **The agent writes each step.** When a step is due, the agent writes it in the person's conversation, following the step's skill, or decides it is not needed. When the reply deadline passes, it looks again and decides: a nudge, an alert, a pause, or nothing.
- **Review & activate**, with a checklist, a **test send** to a team member and a **dry run** of what one person would get. **Stats** shows each step's sent, delivered, read, replied, completed, no-reply, failed and skipped counts.
- **Each person on their own channel and clock.** A step goes to the person's preferred channel, else the one they last used, else the step's own, and moves to their other channels if it cannot be delivered. Per-person timezones, **quiet hours** and **Finish after N days** are set per journey.
- **Followed people and their contacts.** Relatives or carers can be linked to a person, never on a name alone. See [Followed people and their contacts](/work/tools/programs/#followed-people-and-their-contacts).
- **More channels.** Telegram (through a 48-hour start link that asks *Are you …?*), Slack, phone calls from the agent's voice number, steps that wait in web chat, and people reached in your own app.
- **People who say STOP** are no longer written to on that channel, at once.

### Team and escalations

- Add team members on WhatsApp, Slack, Telegram, or the Studio inbox only, and edit their name, channels and the channel they are alerted on first.
- **Roles**: Full, Assistant and Alerts only, editable item by item, plus what each member **handles**, which the agent reads to route an alert.
- A **shared alert place**, such as a Slack channel.
- **Urgent** and **attention** alerts; an urgent alert nobody opened is sent again once.
- The **Escalations** tab and the Inbox share one record, with **Claim** and **Resolve**.

See [Team and escalations](/work/tools/programs-team/).

### Programs API and webhooks

Enrol people, read their steps and escalations, and receive signed webhook events from your own software, with the agent's existing API keys. See [Programs API and webhooks](/work/tools/programs-api/).

### WhatsApp

Templates can have a header, a footer, quick-reply buttons and a form button. The new **Forms** screen publishes native WhatsApp forms the agent can send. See [WhatsApp](/work/channels/whatsapp/).

### One person, one channel list, across Studio

The same person panel opens from Users, Sessions, the Inbox and Programs, and every list filters by the same channels with counts. Lists keep themselves current. See [Review sessions](/work/workflow/review-sessions/#sessions-across-channels) and [Users](/work/channels/users/#managing-existing-users).

<!-- TODO verify: Monetize (a Free plan as a package with no card, trials without a card and what happens at their end, the upgrade path) and the landing page editor (blocks, images adjusted by URL, rich text, previews, templates) are in progress, uncommitted in surogate-ops as of 2026-10-14 14:55. Add their entries once committed. -->

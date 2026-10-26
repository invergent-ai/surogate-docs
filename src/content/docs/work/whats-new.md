---
title: What's new
---

## October 26, 2026: Surogate docs update

### Unanswered questions end the agent's turn

When you don't answer an agent's question within 30 minutes, its turn now ends: it says once that it will wait, and asks again when you next write if it still needs the answer. If you sent a message the agent hasn't read yet, such as a photo, the turn goes on with that message instead. See [Inbox](/work/tools/inbox/#when-nobody-answers) and [When nobody answers](/develop/reference/tool-catalog/#when-nobody-answers) in the tool catalog.

### The copilot builds datasets, starts training runs and serves models

- **Build guides.** The [copilot](/work/tools/copilot/#datasets-training-and-models) now follows build guides for datasets, training runs and model deployments, as it does for agents and skills.
- **What it can't do.** It now says that it can't change models beyond starting and stopping them, browse the Data Hub, create RL environments, start GRPO runs or run evaluations, and sends you to the right place instead. See [What the Copilot can't do](/work/tools/copilot/#what-the-copilot-cant-do).

### Docs corrected

- A new [Supported GPUs](/develop/features/training/#supported-gpus) section on the training page.
- Corrections to [Models](/develop/features/models/) and [Datasets](/develop/features/datasets/), including that a finished run doesn't land on Models by itself.

## October 25, 2026: Surogate Keel 0.2.1

### A user guide for Keel

[Surogate Keel](/keel/) runs business processes as cases: builders define case types of stages, steps, decisions and rules, and people and agents work cases of them. A new section documents its two apps.

- **Keel Builder**, for builders: [case types and drafts](/keel/builder/case-types/), the [designer's tabs](/keel/builder/workflow/), [dry runs and publishing](/keel/builder/publish/), [moving running cases](/keel/builder/versions/) to a new version, [rules and calendars](/keel/builder/rules/), [queues and supervisors](/keel/builder/queues/), and [service keys and effects](/keel/builder/settings/).
- **Keel**, the business app, for staff and supervisors: [the Work page](/keel/business/work/), [team queues](/keel/business/queues/), [cases](/keel/business/cases/), [an open case](/keel/business/open-case/), [working with agents](/keel/business/agents/), [Watch](/keel/business/watch/) and [the Team page](/keel/business/supervisors/).
- A [quickstart](/keel/quickstart/) from an empty project to a worked case, a [glossary](/keel/reference/glossary/), [roles and permissions](/keel/reference/roles/) and an [FAQ](/keel/reference/faq/).

## October 23, 2026: Surogate 1.19.0 (runtime 2.22.1)

### Office documents: a user guide

- **Work with documents.** A new guide walks through the common tasks: opening a document, asking the agent for a new report, spreadsheet or deck, editing alongside it, mentioning it in a comment, reviewing its changes in Word, filling in a PDF form, and what to do when a save is pending. See [Work with documents](/work/workflow/work-with-documents/).
- **Comment mentions in Studio.** Mentioning the agent in a comment works in Studio's Work chat, as in the agent's own web app. See [Comment mentions](/work/tools/office-documents/#comment-mentions).
- **Scripts where there is no editor.** On Slack, WhatsApp and other channels without a document pane, the agent builds and changes office files with its built-in `docx`, `xlsx`, `pptx` and `pdf-forms` skills and sends you the file. See [Files the agent builds with scripts](/work/tools/office-documents/#files-the-agent-builds-with-scripts).

## October 22, 2026: Surogate 1.16.0 (runtime 2.19.5)

### Discord and Microsoft Teams

Your agent can now talk to people on [Discord](/work/channels/discord/) and [Microsoft Teams](/work/channels/teams/); add them from **Publish → Channels**.

### Office documents: more formats, comment mentions and templates

- **Live editing for Word, spreadsheets, presentations and PDFs.** The agent now works alongside you in Word documents, spreadsheets, presentations and PDFs, not only Word. Its changes appear under its name as it makes them. See [what the agent can do live](/work/tools/office-documents/#what-the-agent-can-do-live).
- **Comment mentions.** @-mention the agent in a comment in an open document and it reaches the chat as your message. The agent answers in the comment thread and resolves it. See [Comment mentions](/work/tools/office-documents/#comment-mentions).
- **Templates for new files.** New Word, spreadsheet and slide files start from built-in templates. PDFs have none. See [Templates for new files](/work/tools/office-documents/#templates-for-new-files).

### Programs: send a step once per person

A journey step has a new **Send once per person** checkbox in its **When** section. The step fires on the first matching day inside its window, then stays quiet for that person, even if they are enrolled again. See [Steps](/work/tools/programs/#steps).

### The copilot answers from the docs

The [copilot](/work/tools/copilot/#asking-the-docs) now searches sections of the product documentation and answers from the matching text, and it opens its own build guides when it builds something.

### Project roles

Every project member now has a role, Viewer, Editor or Owner, that decides what they can see and change. See [what each role can do](/work/settings/members/#what-each-role-can-do).

### Now documented

Earlier features that now have their own pages:

- [Voice](/work/channels/voice/).
- [API access for web chat](/work/channels/web/#api-access).
- [Surogate Desktop (Linux)](/work/desktop/overview/): a desktop app that lets your agent work on your own computer. [Get started](/work/desktop/get-started/) walks through a first chat on a folder and a first project.
- [Projects in Surogate Desktop](/work/desktop/projects/): a coordinator chat that splits a goal into threads.
- [Skill canvas](/develop/features/skill-canvas/): draw a skill as a flow of steps. See also [Export a skill](/work/library/skills/#export-a-skill).
- [Vault](/work/settings/vault/): keep API keys and secrets the platform can use without showing them.

## October 14, 2026: Surogate 1.14.10 (runtime 2.18.1)

### Programs: journeys, a team and escalations, on any channel

[Programs](/work/tools/programs/) now reaches people on the channels they use, not only WhatsApp, and the agent does the writing.

- **Journeys.** The Programs page's former Check-ins tab is now the **Journeys** tab: each journey is a set of steps every person in it gets, counted from their own start date, shown on a day timeline. Steps can come before the start date (day -1 is the day before), for reminders ahead of an appointment.
- **A wizard and presets.** **New journey** sets one up in four short screens, from a preset (Health follow-up, Customer onboarding, Sales follow-up, Appointment reminders) or blank.
- **The agent writes each step.** When a step is due, the agent writes it in the person's conversation, following the step's skill, or decides it is not needed. When the reply deadline passes, it looks again and decides: a nudge, an alert, a pause, or nothing.
- **Review & activate**, with a checklist, a **test send** to a team member and a **dry run** of what one person would get. **Stats** shows each step's sent, delivered, read, replied, completed, no-reply, failed and skipped counts.
- **Each person on their own channel and clock.** A step goes to the person's preferred channel, else the one they last used, else the step's own, and moves to their other channels if it cannot be delivered. Per-person timezones, **quiet hours** and **Finish after N days** are set per journey.
- **Followed people and their contacts.** Relatives or carers can be linked to a person, never on a name alone. Every step reaches them too, and an answer from any of them answers it for all. See [Followed people and their contacts](/work/tools/programs/#followed-people-and-their-contacts).
- **More channels.** Telegram (through a 48-hour start link that asks *Are you …?*), Slack, phone calls from the agent's voice number, steps that wait in web chat with browser notifications, and people reached in your own app.
- **People who say STOP** are no longer written to on that channel, at once.

### Team and escalations

- Add team members on WhatsApp, Slack, Telegram, or the Studio inbox only, and edit their name, channels and the channel they are alerted on first.
- Choose directly what each member **gets told about** and **can do**, with **Everything** shortcuts and **Same as…** another member, plus what each member **handles**, which the agent reads to route an alert.
- A **shared alert place**, such as a Slack channel.
- **Urgent** and **attention** alerts; an urgent alert nobody opened is sent again once. An urgent alert can phone a team member, and one nobody confirms on the phone goes straight to their next channel.
- The **Escalations** tab and the Inbox share one record, with **Claim** and **Resolve**. Team members can also take or resolve an escalation from their own chat, and their colleagues are told.

See [Team and escalations](/work/tools/programs-team/).

### The copilot runs Programs

The Platform Copilot can now build and run Programs, People, the Team, Escalations, Monetize and the Inbox for you, and knows which Programs tab, journey and person you have open. `/build-program` walks you through setting up a whole program. See [Copilot](/work/tools/copilot/).

### Programs API and webhooks

Enrol people, read their steps and escalations, and receive signed webhook events from your own software, with the agent's existing API keys. See [Programs API and webhooks](/work/tools/programs-api/).

### WhatsApp

Templates can have a header, a footer, quick-reply buttons and a form button. The new **Forms** screen publishes native WhatsApp forms the agent can send. See [WhatsApp](/work/channels/whatsapp/).

### Office documents in the editor

Word documents, spreadsheets, presentations and PDFs in an agent's workspace now open in a full office editor beside the chat, in Studio and in the agent's web app. Edits save back into the workspace, and everyone with a document open sees each other's changes live. In a Word document the agent can work alongside you with `office_read` and `office_edit`: its changes appear under its name as it makes them, and your edits always win. See [Office documents](/work/tools/office-documents/).

### One person, one channel list, across Studio

The same person panel opens from Users, Sessions, the Inbox and Programs, and every list filters by the same channels with counts. Lists keep themselves current. See [Review sessions](/work/workflow/review-sessions/#sessions-across-channels) and [Users](/work/channels/users/#managing-existing-users).

### Monetize: a Free plan and trials without a card

- **A Free plan**: a plan at no price that people start on your buy page with no card, renewing monthly; it leads the buy page, and a buyer whose paid plan ends drops back to it.
- **Card-free trials on paid plans**: up to 90 days free, a reminder before the end, and if no card is added the trial is cancelled and the buyer moves to the Free plan.
- A **Subscribers** list with each buyer's plan and status.

See [Monetize](/work/monetize/#the-free-plan-and-trials-without-a-card).

### Landing page editor

- A live **Phone** / **Desktop** preview beside the forms; click a section to edit it.
- New blocks: **Testimonials**, **Gallery**, **FAQ**, **Video** and **Contact**, a second button on the hero and call to action, and **Hide from page** for any block.
- Images are still linked, never uploaded, and can now be framed: focal point, zoom, turn and mirror, with alt text.
- A formatting toolbar for prose, drag to reorder, undo and redo for the whole page, and drafts that save themselves until the page is live.
- Three more layouts: **The local service**, **The course** and **Link in bio**.

See [Landing page](/work/workflow/landing-page/).

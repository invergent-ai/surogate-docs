---
title: Keel
description: Connect the portal to Surogate Keel, and show each person their open work there.
---

Surogate Keel runs the institution's cases and processes. Connected, the portal shows each person signed in the work Keel holds for them, and links each item to it in Keel.

## What people see

A person signed in sees, on a page of the portal, the work Keel holds for them, and a supervisor of the Keel project sees its headline figures. Each item links to Keel's business app. Visitors see a prompt to sign in. The sections below say who sees what, and what happens when Keel does not answer.

## Connect Keel

The portal's configuration names your Keel. It gives:

- Keel's API address. Inside the same cluster, its service address works too.
- The Keel project whose work the portal shows, by its id.
- Keel's business app, where an item's link goes.
- How long the portal waits for Keel, from 1,000 to 10,000 ms; 3,000 when none is given.

The console has no screen for this yet. For now, this is set in the site's configuration: see [Developer: Keel](/portal/developer/keel/#connect-keel-in-keelyaml).

Keel must trust the portal. Its administrator adds the portal's **issuer**, shown on the console's **Apps** page under **For the apps' developers**, with the project, to Keel's trusted portals. Keel then finds each person among its staff by their email: the email they have in the portal must be the one they have in Keel.

## My work

The portal's My work widget is placed on a page. The console's page editor does not place it yet. For now, this is set in the site's configuration: see [Developer: Keel](/portal/developer/keel/#my-work-on-a-page).

A person signed in sees their open work: each step of a case or task of a process that waits on them, with its number, the step, its due time and whether it is on track, past its goal or late. The widget shows 1 to 50 items; 10 when it names no number. Each item opens in Keel's business app, which asks the person to sign in there if they have not.

- **Visitors** see a prompt to sign in.
- **Someone Keel does not know as staff** sees that they do not work in Keel.
- **When Keel does not answer**, the rest of the page shows as usual, and the widget says the work cannot be read now.
- **An administrator seeing the portal as someone else** does not see that person's work.

A page with the widget is made for each person: it is never kept in a cache and shown to someone else. The portal checks the widget when the site's configuration is published: placed on a portal that names no Keel, it is refused.

## The overview

The portal's Keel overview widget is placed on a page, such as a dashboard for the people who supervise the project. The console's page editor does not place it yet. For now, this is set in the site's configuration: see [Developer: Keel](/portal/developer/keel/#the-overview-on-a-page).

A supervisor of the Keel project sees its headline figures over the last days the widget names (1 to 92; 30 when it names none):

- the open cases, and in how many case types;
- the cases decided, against the same number of days before;
- the median time from a case's start to its decision, against before;
- the cases past their deadline;
- of the open cases, how many are on time, due within a day, and with no deadline.

A link opens Keel's own overview for the same days, with more: by case type, where cases wait, and what needs attention.

- **Only supervisors** see the figures. Others of the project's staff see that the overview is for its supervisors. Someone Keel does not know as staff sees that they do not work in Keel. Visitors see a prompt to sign in.
- **When Keel does not answer**, the rest of the page shows as usual, and the widget says the overview cannot be read now. My work is not held back by it.
- **The figures are a minute old at most.** The portal asks Keel again a minute after it last asked for that person; someone who stops being a supervisor may see the figures for that minute.
- **On a dashboard**, the widget is placed by the site. People may move it or take it off their own dashboard, but cannot add it from the dashboard's offers.

A page with the widget is never kept in a cache. Placed on a portal that names no Keel, the widget is refused.

## Start cases from the portal

A form, a job or an endpoint can start a Keel case or process, or tell Keel something, with four [actions](/portal/sites/actions/):

- **Start a case** of a Keel case type.
- **Start a process.**
- **Send a message:** it goes to the processes waiting for it with a key.
- **Send a signal:** it goes to every process waiting for it.

A case type or a process is named by the key Keel gives it, without spaces. A message or signal is named as the process waits for it, and a message also carries the key it waits with. For now, this is set in the site's configuration: see [Developer: Keel](/portal/developer/keel/#start-a-case-from-a-form).

The portal keeps what Keel answered: the case's or process's id and number, how many processes a message reached, or how many a signal is on its way to.

- **Keel's key:** the people who send a form are rarely Keel's staff, so these actions use Keel's key for the project. Add it as a secret [connector](/portal/sites/connectors/), set its value under **Connectors**, and name that connector in the site's configuration as Keel's key; no other action may use it. The key is kept for the Keel the configuration names: change its API address or project, and set the key again. See [Developer: Keel](/portal/developer/keel/#connect-keel-in-keelyaml).
- **Once each:** a job that runs again for the same event starts nothing twice in Keel: Keel answers with what it did the first time, even if values in the run changed meanwhile. The portal tells each call apart by where the action is in the list and how many times it has run there. In a loop over a list that may change between runs, the action names the item, such as the item's id, to tell calls apart. A person who sends a form again makes a new submission, and a new case.
- **When Keel refuses:** the action fails with Keel's reason, such as an unknown case type, and the list's error handling reads it. A form whose Keel call fails keeps its submission, with no case. A call that took too long may still have been done: check Keel before sending again. A message no process waits for reaches none, and the run goes on.
- **Forms anyone may send** start cases, but never signal Keel or send it messages, nor do the endpoints and flows they call: those move processes others started. Runs without a person signed in call Keel at most 200 times an hour.
- **Where:** in a form, job or endpoint that may change records, never in a GET endpoint or one anyone may call. A run takes at most 10 of them.

## When something happens in Keel

A [job](/portal/sites/jobs/) can run each time something happens in the Keel project: a case opened, entered a stage, closed or reopened, or a process started, ended or was cancelled. For example, a job can mail the person who asked when their case closes. The form that started the case keeps its id in a record of a [data model](/portal/sites/data-models/) whose case id field can be filtered on, so the job can find it. For now, this is set in the site's configuration: see [Developer: Keel](/portal/developer/keel/#a-job-that-mails-the-person-when-a-case-closes).

| Event | When | What the run also reads |
|---|---|---|
| A case opened | A case starts | its stage |
| A case entered a stage | A case enters a stage | its stage |
| A case closed | A case closes | its resolution |
| A case reopened | A closed case opens again | |
| A process started | A process starts | |
| A process ended | A process ends | its status: completed, terminated or failed |
| A process cancelled | A process is cancelled | |

The names the configuration gives these events are in [Developer: Keel](/portal/developer/keel/#keels-events-in-a-job).

- **What the run reads:** the event, which case or process it is about (its id, number, type and version), and when it happened. The stage, the resolution and the status are left out when Keel gives none. Keel's events never hold a case's data: keep what you need in a record, as above. One case's own events come in order.
- **Which:** a job names one or more events. It can narrow them to some case types and processes; without that, all of them.
- **Keel's key:** the portal reads Keel's events with Keel's key for the project, as for starting cases. Without Keel's key named in the site's configuration, the job is refused.
- **Once each:** each event runs each job that takes it once, a few seconds after it happens, in the order Keel recorded them. A job that starts cases of the kind it runs on would run itself again: the portal refuses one whose case opened (or process started) event takes a type its own actions start. A loop it cannot see, through an endpoint the job calls or between two jobs, ends on its own: the events of a case or process a job started start jobs one step further along a chain, and a chain ends after three, as chains of record changes do.
- **When the portal cannot read Keel:** it tries again, waiting longer each time, and loses nothing. **Jobs** in the console shows when Keel's events were last read, or what went wrong. If Keel has deleted old events the portal had not read yet, the portal reads on from then, and **Jobs** says when: those events are lost. Take Keel's key away and name it again later, and the portal reads on from then too. Keel keeps them a month unless set otherwise.
- **Also as events:** each one is also sent to [apps and webhooks](/portal/sites/apps/) as a portal event. A webhook that takes every event gets these too.

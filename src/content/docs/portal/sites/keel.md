---
title: Keel
description: Connect the portal to Surogate Keel, and show each person their open work there.
---

Surogate Keel runs the institution's cases and processes. Connected, the portal shows each person signed in the work Keel holds for them, and links each item to it in Keel.

## What people see

A person signed in sees, on a page of the portal, the work Keel holds for them, and a supervisor of the Keel project sees its headline figures. Each item links to Keel's business app. Visitors see a prompt to sign in. The sections below say who sees what, and what happens when Keel does not answer.

## Connect Keel

Name your Keel in `keel.yaml`, at the top of the portal's files (see the [config example](#connect-keel-in-keelyaml)):

- `api`: Keel's API. Inside the same cluster, its service address works too, such as `http://keel-api.keel.svc`.
- `project`: the Keel project whose work the portal shows, by its id.
- `app`: Keel's business app, where an item's link goes.
- `timeoutMs`: how long the portal waits for Keel, from 1,000 to 10,000 ms; 3,000 when left out.

Keel must trust the portal. Its administrator adds the portal's **issuer**, shown on the console's **Apps** page under **For the apps' developers**, with the project, to Keel's trusted portals. Keel then finds each person among its staff by their email: the email they have in the portal must be the one they have in Keel.

## My work

Place the portal's `my-work` widget on a page (see the [config example](#my-work-on-a-page)).

A person signed in sees their open work: each step of a case or task of a process that waits on them, with its number, the step, its due time and whether it is on track, past its goal or late. `limit` shows 1 to 50 items; 10 when left out. Each item opens in Keel's business app, which asks the person to sign in there if they have not.

- **Visitors** see a prompt to sign in.
- **Someone Keel does not know as staff** sees that they do not work in Keel.
- **When Keel does not answer**, the rest of the page shows as usual, and the widget says the work cannot be read now.
- **An administrator seeing the portal as someone else** does not see that person's work.

A page with the widget is made for each person: it is never kept in a cache and shown to someone else. The portal checks the widget when the files are published: placed without `keel.yaml`, it is refused.

## The overview

Place the portal's `keel-overview` widget on a page, such as a dashboard for the people who supervise the project (see the [config example](#the-overview-on-a-page)).

A supervisor of the Keel project sees its headline figures over the last `days` days (1 to 92; 30 when left out):

- the open cases, and in how many case types;
- the cases decided, against the same number of days before;
- the median time from a case's start to its decision, against before;
- the cases past their deadline;
- of the open cases, how many are on time, due within a day, and with no deadline.

A link opens Keel's own overview for the same days, with more: by case type, where cases wait, and what needs attention.

- **Only supervisors** see the figures. Others of the project's staff see that the overview is for its supervisors. Someone Keel does not know as staff sees that they do not work in Keel. Visitors see a prompt to sign in.
- **When Keel does not answer**, the rest of the page shows as usual, and the widget says the overview cannot be read now. My work is not held back by it.
- **The figures are a minute old at most.** The portal asks Keel again a minute after it last asked for that person; someone who stops being a supervisor may see the figures for that minute.
- **On a dashboard**, the page places the widget in its regions. People may move it or take it off their own dashboard, but cannot add it from the dashboard's offers.

A page with the widget is never kept in a cache. Placed without `keel.yaml`, the widget is refused.

## Start cases from the portal

A form, a job or an endpoint can start a Keel case or process, or tell Keel something, with four [actions](/portal/sites/actions/) (see the [config example](#start-a-case-from-a-form)):

| Action | What it does | Keys |
|---|---|---|
| `startCase` | Starts a case of a Keel case type | `caseType`, `data`, `once`, `into` |
| `startProcess` | Starts a Keel process | `process`, `data`, `once`, `into` |
| `sendMessage` | Gives a message to the processes waiting for it with a key | `name`, `key`, `payload`, `once`, `into` |
| `sendSignal` | Signals every process waiting for it | `name`, `once`, `into` |

`caseType` and `process` are the keys Keel gives them, without spaces. A message's or signal's `name` is the name the process waits for, and a message's `key` is an expression giving the key it waits with.

`into` keeps what Keel answered: the case's or process's id and number, how many processes a message reached, or how many a signal is on its way to.

- **Keel's key:** the people who send a form are rarely Keel's staff, so these actions use Keel's key for the project. Add it as a secret [connector](/portal/sites/connectors/), set its value under **Connectors**, and name the connector in `keel.yaml` as `serviceKey`; no other action may use it. The key is kept for the Keel `keel.yaml` names: change its `api` or `project`, and set the key again.
- **Once each:** a job that runs again for the same event starts nothing twice in Keel: Keel answers with what it did the first time, even if values in the run changed meanwhile. The portal tells each call apart by where the action is in the list and how many times it has run there. In a loop over a list that may change between runs, give the action `once`: an expression naming the item, such as `vars.item.id`. A person who sends a form again makes a new submission, and a new case.
- **When Keel refuses:** the action fails with Keel's reason, such as an unknown case type, and the run's `onError` reads it. A form whose Keel call fails keeps its submission, with no case. A call that took too long may still have been done: check Keel before sending again. A message no process waits for reaches none, and the run goes on.
- **Forms anyone may send** start cases, but never signal Keel or send it messages, nor do the endpoints and flows they call: those move processes others started. Runs without a person signed in call Keel at most 200 times an hour.
- **Where:** in a form, job or endpoint that may change records, never in a GET endpoint or one anyone may call. A run takes at most 10 of them.


## When something happens in Keel

A [job](/portal/sites/jobs/) can run each time something happens in the Keel project: a case opened, entered a stage, closed or reopened, or a process started, ended or was cancelled. For example, a job can mail the person who asked when their case closes. The form that started the case keeps its id in a record of a [data model](/portal/sites/data-models/) whose `case_id` field is `filterable: true`, so the job can find it (see the [config example](#a-job-that-mails-the-person-when-a-case-closes)).

| Event | When | What the run also reads |
|---|---|---|
| `case.opened` | A case starts | `stage` |
| `case.stage_entered` | A case enters a stage | `stage` |
| `case.closed` | A case closes | `resolution` |
| `case.reopened` | A closed case opens again | |
| `process.started` | A process starts | |
| `process.ended` | A process ends | `status`: `completed`, `terminated` or `failed` |
| `process.cancelled` | A process is cancelled | |

- **What the run reads:** `trigger.event` is the event, and `trigger.id`, `trigger.number`, `trigger.type` and `trigger.version` name the case or process. `trigger.at` is when it happened. `stage`, `resolution` and `status` are left out when Keel gives none: check with `has(trigger.resolution)`. Keel's events never hold a case's data: keep what you need in a record, as above. `trigger.seq` orders one case's own events.
- **Which:** `on` names one or more events. `types` narrows them to some case types and processes; without it, all of them.
- **Keel's key:** the portal reads Keel's events with Keel's key for the project, as for starting cases. Without `serviceKey` in `keel.yaml`, the job is refused.
- **Once each:** each event runs each job that takes it once, a few seconds after it happens, in the order Keel recorded them. A job that starts cases of the kind it runs on would run itself again: the portal refuses one whose `case.opened` (or `process.started`) takes a type its own actions start. A loop it cannot see, through an endpoint the job calls or between two jobs, ends on its own: the events of a case or process a job started start jobs one step further along a chain, and a chain ends after three, as chains of record changes do.
- **When the portal cannot read Keel:** it tries again, waiting longer each time, and loses nothing. **Jobs** in the console shows when Keel's events were last read, or what went wrong. If Keel has deleted old events the portal had not read yet, the portal reads on from then, and **Jobs** says when: those events are lost. Take Keel's key away and name it again later, and the portal reads on from then too. Keel keeps them a month unless set otherwise.
- **Also as events:** each one is also the portal event `portal/keel.<event>`, such as `portal/keel.case.closed`, for [apps and webhooks](/portal/sites/apps/). A webhook that takes every event gets these too.

## Config example

### Connect Keel in `keel.yaml`

At the top of the portal's files:

```yaml
api: https://keel-api.primaria.ro
project: 991bd3e2-3ff7-4352-8d46-bdf087eda408
app: https://keel-app.primaria.ro
```

- `api`: Keel's API.
- `project`: the Keel project whose work the portal shows, by its id.
- `app`: Keel's business app, where an item's link goes.
- `timeoutMs` and `serviceKey` are described under [Connect Keel](#connect-keel) and [Start cases from the portal](#start-cases-from-the-portal).

### My work on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: work
      app: portal
      widget: my-work
      preferences: { limit: 10 }
```

- `limit`: how many items it shows, 1 to 50; 10 when left out.

### The overview on a page

In a page's file:

```yaml
regions:
  main:
    - id: overview
      app: portal
      widget: keel-overview
      preferences: { days: 30 }
```

- `days`: the figures cover the last `days` days, 1 to 92; 30 when left out.

### Start a case from a form

In a form's actions (`forms/<id>.yaml`, under `actions`), a job's or an endpoint's:

```yaml
- type: startCase
  caseType: loan
  data:
    applicant: form.name
    amount: form.amount
  into: started
```

- `caseType`: the key Keel gives the case type, without spaces.
- `data`: what the case starts with, each value an expression.
- `into`: where Keel's answer is kept.

### A job that mails the person when a case closes

The form keeps the case's id in a record, in its actions (`forms/request.yaml`):

```yaml
- type: startCase
  caseType: permit
  data:
    address: form.address
  into: started
- type: createRecord
  model: requests
  values:
    case_id: vars.started.caseId
    email: user.email
```

The job finds the record when the case closes (`jobs/permit-decided.yaml`):

```yaml
trigger:
  keel:
    on: [case.closed]
    types: [permit]
site: main
runAs: user:registratura@primaria.ro
actions:
  - type: findRecords
    model: requests
    where:
      case_id: trigger.id
    limit: 1
    into: found
  - type: email
    condition: size(vars.found) > 0
    to: vars.found[0].email
    subject: '"Your request " + trigger.number + " has been decided"'
    text: '"The decision: " + (has(trigger.resolution) ? trigger.resolution : "see your account")'
```

- `keel.on`: the events that start the job, from the table under [When something happens in Keel](#when-something-happens-in-keel).
- `keel.types`: narrows them to some case types and processes.
- `where: { case_id: trigger.id }` finds the record the form made for this case.


---
title: Keel
description: The keel.yaml file, the portal's Keel widgets, the actions that start cases, and the jobs that take Keel's events.
---

The configuration behind [Keel](/portal/sites/keel/). That page covers what people see of their work in Keel, and what happens when Keel does not answer.

## Connect Keel in `keel.yaml`

At the top of the portal's files:

```yaml
api: https://keel-api.primaria.ro
project: 991bd3e2-3ff7-4352-8d46-bdf087eda408
app: https://keel-app.primaria.ro
```

- `api`: Keel's API. Inside the same cluster, its service address works too, such as `http://keel-api.keel.svc`.
- `project`: the Keel project whose work the portal shows, by its id.
- `app`: Keel's business app, where an item's link goes.
- `timeoutMs`: how long the portal waits for Keel, from 1,000 to 10,000 ms; 3,000 when left out.
- `serviceKey`: the secret [connector](/portal/developer/connectors/#a-connectors-file) holding Keel's key for the project. Add the key as a secret connector, set its value under **Connectors**, and name the connector here as `serviceKey`; no other action may use it. The key is kept for the Keel this file names: change its `api` or `project`, and set the key again. It is used to [start cases](#the-actions-that-talk-to-keel) and to [read Keel's events](#keels-events-in-a-job).

Keel must trust the portal: see [Connect Keel](/portal/sites/keel/#connect-keel).

## My work on a page

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

The portal checks the widget when the files are published: placed without `keel.yaml`, it is refused.

## The overview on a page

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

Placed without `keel.yaml`, the widget is refused.

On a dashboard, the page places the widget in its regions. People may move it or take it off their own dashboard, but cannot add it from the dashboard's offers.

## Start a case from a form

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

## The actions that talk to Keel

A form, a job or an endpoint can start a Keel case or process, or tell Keel something, with four [actions](/portal/sites/actions/):

| Action | What it does | Keys |
|---|---|---|
| `startCase` | Starts a case of a Keel case type | `caseType`, `data`, `once`, `into` |
| `startProcess` | Starts a Keel process | `process`, `data`, `once`, `into` |
| `sendMessage` | Gives a message to the processes waiting for it with a key | `name`, `key`, `payload`, `once`, `into` |
| `sendSignal` | Signals every process waiting for it | `name`, `once`, `into` |

`caseType` and `process` are the keys Keel gives them, without spaces. A message's or signal's `name` is the name the process waits for, and a message's `key` is an expression giving the key it waits with.

`into` keeps what Keel answered: the case's or process's id and number, how many processes a message reached, or how many a signal is on its way to.

- **Keel's key:** these actions use Keel's key for the project, named as `serviceKey` in `keel.yaml`; no other action may use it. See [Connect Keel in `keel.yaml`](#connect-keel-in-keelyaml).
- **Once each:** the portal tells each call apart by where the action is in the list and how many times it has run there. In a loop over a list that may change between runs, give the action `once`: an expression naming the item, such as `vars.item.id`.
- **When Keel refuses:** the action fails with Keel's reason, such as an unknown case type, and the run's `onError` reads it.

## A job that mails the person when a case closes

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

The record's data model, `requests`, has `case_id` as a `filterable: true` field, so the job can find the record.

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

- `keel.on`: the events that start the job, from the table under [Keel's events in a job](#keels-events-in-a-job).
- `keel.types`: narrows them to some case types and processes.
- `where: { case_id: trigger.id }` finds the record the form made for this case.

## Keel's events in a job

A [job](/portal/sites/jobs/) takes Keel's events in its `trigger`:

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
- **Once each:** a job whose `case.opened` (or `process.started`) takes a type its own actions start is refused.
- **Also as events:** each one is also the portal event `portal/keel.<event>`, such as `portal/keel.case.closed`, for [apps and webhooks](/portal/developer/apps/#events). A webhook that takes every event gets these too.

What happens when the portal cannot read Keel is on [When something happens in Keel](/portal/sites/keel/#when-something-happens-in-keel).

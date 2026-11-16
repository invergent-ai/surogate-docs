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

## The Workflows section

For what people do in the console, see [Workflows](/portal/console/workflows/). `keel.yaml` may also say:

```yaml
builder: https://keel-builder.example.ro
access:
  view: ["group:Analysts"]
  edit: ["group:Designers"]
  admin: ["role:administrator"]
staff: ["group:Case workers"]
supervisors: ["group:Supervisors"]
queues:
  registratura: ["group:Case workers", "user:anca@primaria.ro"]
flows:
  verificare-fisa-1:
    modify: ["group:Designers"]
    start: ["group:Case workers"]
    see: ["group:Case workers", "group:Supervisors"]
```

- `builder`: Keel's builder, an https origin with no path (http only to this machine).
- `access`: who opens the section at each level. Each list names at most 50 groups, organizations or people, never everyone or signed-in. A person has the highest level they are in; administrators have `admin`.
- `staff`, `supervisors`: who works in Keel. Every token the portal signs for Keel then carries `keel_role` (`supervisor`, `staff` or `none`), and Keel makes the person staff, or a supervisor, at each request, or refuses them. Left out, Keel keeps its own staff.
- `queues`: by Keel's queue key. Each list names at most 50 groups, organizations or people, never everyone or signed-in; the token's `keel_queues` carries the keys of the queues the person is in, and Keel puts them in those queues for as long as the portal says so, besides the people Keel names itself.
- `flows`: by Keel's key (at most 200). `modify` lists who may change the workflow in the builder; `start` lists who may start it from the portal; `see` lists who see its cases or instances. A workflow with no list for a verb is open to everyone who has it.

**Who the person is in Keel.** Keel keys a portal person by the token's `sub`, the portal's own id for them, under the issuer. The first sign-in finds the runtime user whose email the token gives and records the binding (`sub` to user id, one row per user); from then on `sub` alone says who the person is, and the email and name in the token are copies, followed when the portal changes them and used only to show. Changing a person's email in the portal changes nothing about who they are in Keel. An email no runtime user has binds no one (403 `not-staff`), and a user already bound to one `sub` of that issuer is not taken over by another person of it who comes with the same email; a second portal trusted for the same project binds the same user once more, for its own `sub`. A bound person is checked against the project's organisation at least once a minute: one who has left it is refused (403 `not-staff`). The memberships the portal gives through `keel_queues` are recorded apart from those Keel's administrators give, and by the issuer that gave them, so each portal takes away only its own when it stops naming the person.

**Staff the portal makes.** With `keel_role` `staff` or `supervisor` the portal adds the person as staff (`added_by` `portal`), promotes anyone it names a supervisor, and demotes only a supervisor it made itself. With `none` the person is refused and a staff row the portal made goes, with the queues it gave; one Keel's own people made stays. A migration (`0059`) makes the uniqueness of a binding per issuer and adds the issuer to the record of queue memberships.

**Unbinding.** `GET /api/build/projects/{project}/portal-people` (owners) lists who is bound: `issuer`, `sub`, `user_id`, `email`, `name`, `bound_at`. `DELETE /api/build/projects/{project}/portal-people/{sub}?issuer=…` (owners; `issuer` optional) deletes the binding, the record of the queues that issuer gave, and the staff row a portal made unless another portal's person is bound to the same user: 204 whether or not the person was bound. The portal calls it, as the administrator who did it, when a person is disabled or erased in the console; a person disabled by a directory sync or SCIM is not unbound by the portal.

**Who sees a workflow.** For a person below supervisor, the token carries `keel_hidden`: the keys of the workflows whose `see` list does not name them. Keel leaves those workflows' cases and instances out of every list and answers "not found" when one is opened by its id, in the work app and in the portal's views of Keel's work, which read Keel with the same token. Supervisors are never limited by it, and a person who holds an open step of a case or an instance still sees it. The queues' lists, their figures and counts, **Get next**, the project's live stream, the updates of followed cases, the startable case types and processes, and the cases and calls of a process instance are narrowed by it too.

**The frame.** The console frames `<builder>/?host=portal` and answers the builder's messages from its window alone, at the builder's origin: `keel-builder:ready` and `keel-builder:refresh` are answered with `keel-builder:session` (`token`, `expiresAt`, `project`, `role`, `person`), written to that origin only, or `keel-builder:ended` when the person is no longer signed in or no longer has the section. The first token is `POST /_portal/api/me/keel/workflows/open` (the audit log's "Opened the Workflows section"); later ones are `POST /_portal/api/me/keel/workflows/token`. They are for a person's own browser session, never a program's token, never an administrator seeing the portal as them, and live 2 minutes.

**What Keel checks.** The token is the usual `portal-keel+jwt` with `builder_role` (`viewer`, `editor` or `owner`) and, for those below `admin`, `builder_deny`: the keys of the workflows whose `modify` list does not name them. Keel signs the person in to its `/api/build/` routes with that role, in the one project its issuer is bound to, without Studio. It refuses, on the workflows in `builder_deny` (403 `forbidden`): saves, reverts, removals and restores of their files; retiring and reinstating a case type; starting a move of a process's instances; setting and deleting a connection's credentials; and updating, publishing or discarding a draft that changes one. A token with `builder_role` works none of the business routes (the project's cases, work, lists): it is in the person's browser, and carries none of `keel_role`, `keel_queues` and `keel_hidden`, so Keel answers 403 `forbidden`. Nothing of it is ever sent to ops: with a portal's sign-in, the designer's delegations, the helpers, a knowledge base's policy text and the creation of a service key are refused (403 `forbidden`), and a draft is checked against a directory that holds no agent or knowledge base, so one that names one is rejected as naming an unknown one. The builder's own server must name the portal's origin (the chart's `console.builder.config.portalOrigins`, or the builder server's list of portal origins), so that it sends `frame-ancestors` for it and reads the portal's messages; the portal's console allows only that origin as a frame. The server sends it only on the page the portal asks for (`?host=portal`): every other page of the builder is framed by no site, so a page on a portal's origin cannot frame a builder signed in with a person's own login. The app itself refuses to run in a frame no portal asked for. A Pages deployment cannot tell the query: it sets `frame-ancestors` for its portals on every page, and the app's own refusal is what remains.

**The keys the console offers.** The settings form reads Keel's case types, processes and queues as a viewer, with a token like the builder's, and offers them to pick from, so no key is typed by hand; a key Keel does not list yet can still be typed.

**A workflow cloned.** After a clone, the builder tells the console's frame with `keel-builder:cloned` (`kind`, `from`, `to`), at the console's origin only. The console asks the portal to copy `flows.<from>` to `flows.<to>` in `keel.yaml` (`POST /_portal/api/me/keel/workflows/cloned`, for those who change workflows, audited as `keel.workflow_cloned`), as a new version of the file, with its comments kept. Nothing is copied when there is nothing to copy or `<to>` has rules already. The portal also asks Keel (with the person's own token at the lowest role) which case types and processes it has published: `<to>` must not be one, and the person must be one who may change `<from>` (403 otherwise); when Keel cannot be read, the answer is 503 `keel_unavailable` and nothing is copied. A person cannot copy one workflow's lists onto another that is published, whatever the builder says it cloned.

**Who starts a workflow.** The actions **Start a case** and **Start a process**, run for a person, fail with `You may not start the workflow "<key>".` when the workflow's `start` list does not name the person. A run with no person behind it, a public form or an endpoint anyone may call, is refused too when the workflow has a `start` list: it is no one the list names. A job of the portal's own that runs as no one calls Keel with the project's service key as before; a job that runs as a person is held to the list as that person is. A workflow with no `start` list is open to every run.

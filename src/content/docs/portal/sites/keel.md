---
title: Keel
description: Connect the portal to Surogate Keel, and show each person their open work there.
---

Surogate Keel runs the institution's cases and processes. Connected, the portal shows each person signed in the work Keel holds for them, and links each item to it in Keel.

## Connect Keel

Name your Keel in `keel.yaml`, at the top of the portal's files:

```yaml
api: https://keel-api.primaria.ro
project: 991bd3e2-3ff7-4352-8d46-bdf087eda408
app: https://keel-app.primaria.ro
```

- `api`: Keel's API. Inside the same cluster, its service address works too, such as `http://keel-api.keel.svc`.
- `project`: the Keel project whose work the portal shows, by its id.
- `app`: Keel's business app, where an item's link goes.
- `timeoutMs`: how long the portal waits for Keel, from 1,000 to 10,000 ms; 3,000 when left out.

Keel must trust the portal. Its administrator adds the portal's **issuer**, shown on the console's **Apps** page under **For the apps' developers**, with the project, to Keel's trusted portals. Keel then finds each person among its staff by their email: the email they have in the portal must be the one they have in Keel.

## My work

Place the portal's `my-work` widget on a page:

```yaml
regions:
  main:
    - id: work
      app: portal
      widget: my-work
      preferences: { limit: 10 }
```

A person signed in sees their open work: each step of a case or task of a process that waits on them, with its number, the step, its due time and whether it is on track, past its goal or late. `limit` shows 1 to 50 items; 10 when left out. Each item opens in Keel's business app, which asks the person to sign in there if they have not.

- **Visitors** see a prompt to sign in.
- **Someone Keel does not know as staff** sees that they do not work in Keel.
- **When Keel does not answer**, the rest of the page shows as usual, and the widget says the work cannot be read now.
- **An administrator seeing the portal as someone else** does not see that person's work.

A page with the widget is made for each person: it is never kept in a cache and shown to someone else. The portal checks the widget when the files are published: placed without `keel.yaml`, it is refused.

## Start cases from the portal

A form, a job or an endpoint can start a Keel case or process, or tell Keel something, with four [actions](/portal/sites/actions/):

```yaml
- type: startCase
  caseType: loan
  data:
    applicant: form.name
    amount: form.amount
  into: started
```

| Action | What it does | Keys |
|---|---|---|
| `startCase` | Starts a case of a Keel case type | `caseType`, `data`, `into` |
| `startProcess` | Starts a Keel process | `process`, `data`, `into` |
| `sendMessage` | Gives a message to the processes waiting for it with a key | `name`, `key`, `payload`, `into` |
| `sendSignal` | Signals every process waiting for it | `name`, `into` |

`into` keeps what Keel answered: the case's or process's id and number, how many processes a message reached, or how many a signal is on its way to.

- **Keel's key:** the people who send a form are rarely Keel's staff, so these actions use Keel's key for the project. Add it as a secret [connector](/portal/sites/connectors/), set its value under **Connectors**, and name the connector in `keel.yaml` as `serviceKey`; no other action may use it. The key is kept for the Keel `keel.yaml` names: change its `api` or `project`, and set the key again.
- **Once each:** a job that runs again for the same event starts nothing twice in Keel: Keel answers with what it did the first time. A person who sends a form again makes a new submission, and a new case.
- **When Keel refuses:** the action fails with Keel's reason, such as an unknown case type, and the run's `onError` reads it. A form whose Keel call fails keeps its submission, with no case. A call that took too long may still have been done: check Keel before sending again. A message no process waits for reaches none, and the run goes on.
- **Forms anyone may send** start cases, but never signal Keel or send it messages: those move processes others started. Visitors' forms call Keel at most 200 times an hour.
- **Where:** in a form, job or endpoint that may change records, never in a GET endpoint or one anyone may call. A run takes at most 10 of them.


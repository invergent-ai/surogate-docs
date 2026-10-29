---
title: BPMN processes
sidebar:
  label: BPMN processes
---

Besides case types, Keel runs **processes** drawn in BPMN 2.0, the notation of process modellers such as Camunda Modeler and bpmn.io. A process is a BPMN file among the project's definitions. It is published through a draft, as a case type is, and each run of it is an **instance**.

In this release, processes have no screens of their own. A builder puts a process file in a draft through Keel Builder's API, and staff or another system start and work instances through Keel's API. The designer and the business app show processes in a later release. The Review and publish page already shows a process file's warnings.

## A process file

- One process is one file, `processes/<key>.bpmn`, in the project's definitions. Its key starts with a letter or a digit and holds letters, digits, `-` and `_`.
- Keel keeps the file exactly as it was saved, diagram layout included: the file you download is the file you uploaded.
- A file is at most 5,000,000 bytes and holds one process.
- What BPMN has no place for, such as a task's queue or the type of a variable, is written in Keel's own elements, in the namespace `https://surogate.ai/keel/bpmn/1`, inside the `extensionElements` of the BPMN element they describe. See [Keel's settings in the file](#keels-settings-in-the-file).

## What Keel runs

| Element | What Keel does |
|---|---|
| **Start event** | The instance starts here. Only a plain start event: a timer or message start event is refused. |
| **User task**, **manual task** | Waits for a person to complete it. |
| **Receive task**, **message catch event** | Waits for a message of its name. |
| **Timer catch event** | Waits for a duration, such as `PT2H` or `P3D`, or until a date. A repeating (cycle) timer is refused. |
| **Timer boundary event** | Fires on a task or a subprocess after a duration or at a date. An interrupting one withdraws the activity; a non-interrupting one starts its path beside it. |
| **Error boundary event** | Catches an error thrown inside the task or subprocess it sits on: the one with the error's code first, else one without a code. |
| **Exclusive gateway** | Takes the first outgoing flow, in the order written, whose condition holds, else its default flow. |
| **Parallel gateway** | Splits into every outgoing flow, or waits for every incoming one. |
| **Event-based gateway** | Waits for whichever of its timer and message catches comes first. |
| **End event** | Plain, **terminate** (ends everything still open in its process or subprocess), or **error** (throws its error's code). |
| **Embedded subprocess** | Runs its own flow, and may carry boundary events. |
| **Lanes** | A lane's name is the queue of the tasks in it. |

Not run yet, refused when published: service tasks, business rule tasks, call activities, multi-instance tasks, inclusive gateways, event subprocesses, data stores, message boundary events and pools that send each other messages.

Refused: script tasks, plain tasks, send tasks, throw events, signals, escalations, compensation, transactions, ad hoc subprocesses, conditional and link events, loops on a task (draw the loop with a gateway), data objects and correlation keys. Each refusal names the element.

Conditions are written in CEL over the process's variables, as a case type's are, for example `amount <= 250000.0`.

## Keel's settings in the file

Each setting sits in the `extensionElements` of its BPMN element. An element or attribute Keel does not know, or one where it has no meaning, is a problem when the file is published: nothing is ignored silently.

### The process

```xml
<bpmn:process id="loan-review" isExecutable="true">
  <bpmn:extensionElements>
    <keel:process queue="underwriting" calendar="ro"/>
    <keel:variables>
      <keel:variable name="amount" type="decimal" required="true"/>
      <keel:variable name="note" type="string"/>
    </keel:variables>
  </bpmn:extensionElements>
  …
</bpmn:process>
```

- `keel:process`: `queue`, the queue of every task that names none and lies in no lane, and `calendar`, the [calendar](/keel/builder/rules/#calendars) business timers count on.
- `keel:variables`: one `keel:variable` for each variable the instance keeps, with the same types as a case type's [fields](/keel/builder/data/). A variable can be `required`, which its start data must then hold, and `pii`. A process has only the variables it declares.

### A user or manual task

```xml
<bpmn:userTask id="approve" name="Approve the loan">
  <bpmn:extensionElements>
    <keel:task queue="committee" outcome-variable="decision">
      <keel:write variable="note" required="true"/>
      <keel:outcome name="approve" label="Approve"/>
      <keel:outcome name="decline" label="Decline" requires="note"/>
      <keel:check when="amount &lt;= 1000000.0" message="above the committee's limit"/>
      <keel:maker-checker task="prepare"/>
      <keel:authority amount="amount" scope="loan"/>
    </keel:task>
  </bpmn:extensionElements>
</bpmn:userTask>
```

| Setting | What it does |
|---|---|
| `queue` | The queue whose members complete the task. Without it, the task's lane names the queue, then the process's `queue`. |
| `user` | The one person who completes the task, by their user id. |
| `keel:write` | A variable the task's completion may write; `required` makes it one the completion must hold. A completion writes nothing else. |
| `keel:outcome` | An outcome the task ends with, with the variables it `requires`. A task with none has the one outcome `done`. |
| `outcome-variable` | A variable that takes the outcome's name, for a gateway after the task to read. |
| `keel:check` | A condition that must hold once the completion's values are in. When it does not, Keel refuses the completion with the message. |
| `keel:maker-checker` | Whoever completed the named task, in any round of a loop, may not complete this one. |
| `keel:authority` | The person completing the task needs an [authority limit](/keel/business/supervisors/#authority-limits) in the scope at least as large as the amount variable. |

### A message catch, a receive task, a timer

- `keel:message` on a message catch event or a receive task lists, with `keel:write`, the variables the message may write. A message that holds anything else is refused.
- `keel:timer business="true"` on a timer makes it count business time on the process's calendar.

## Publishing a process

A process file is saved in a draft and published with it, like any other file of the project:

1. Save the file in an open draft: `PUT /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}`, with the file as the body.
2. Run the [dry run](/keel/builder/publish/#dry-run), or open **Review and publish**. The checks read the file against what Keel runs, its settings, its variables, its conditions and the project's calendars.
3. Publish. The process has a new version, and new instances start on it.

A problem that Keel cannot run, such as a script task, refuses the publish and names the element. A vendor extension, such as Camunda's, Flowable's or SpiffWorkflow's own properties, is a **warning**: Keel ignores it and never runs it, and the publish goes on. The review page lists warnings under **Warnings**, and **Publish** stays on.

Running instances finish on the version they started on.

Builders read the published processes with:

| To | Call |
|---|---|
| List the processes, with each version's running instances | `GET /api/build/projects/{project}/processes` |
| Download a version's file | `GET /api/build/projects/{project}/processes/{key}/versions/{version}` |
| Read the file in a draft | `GET /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}` |
| Put the file back as the draft started with it | `POST /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}/revert` |

## Running instances

Staff sign in as they do for the business app; another system uses a [service key](/keel/systems/). Keel sets who acted and when on everything they send: a body that names `actor` or `at` is refused.

| To | Call | Who |
|---|---|---|
| Start an instance | `POST /api/projects/{project}/processes` with `{"process": "loan-review", "data": {"amount": "20000.00"}}` | Staff and service keys |
| List instances, newest first | `GET /api/projects/{project}/processes`, with `process`, `status`, `attention=true`, `cursor` and `limit` | Staff and service keys |
| Read an instance | `GET /api/processes/{instance_id}` | Staff and service keys |
| Its open tasks | `GET /api/processes/{instance_id}/tasks` | Staff and service keys |
| Its history | `GET /api/processes/{instance_id}/history` | Staff and service keys |
| Check its history replays | `POST /api/processes/{instance_id}/replay` | Staff and service keys |
| Send it an event | `POST /api/processes/{instance_id}/events` | See below |

Starting an instance answers its `instance_id`, its `number`, such as `P-000001`, and its status. The start data must fit the declared variables. Send an `Idempotency-Key` header with each start: a start sent again with the same key answers with the instance it started the first time.

The events an instance takes:

| Event | Body | Who sends it |
|---|---|---|
| Complete a task | `{"type": "task.completed", "task": "t3", "outcome": "approve", "output": {"note": "fine"}}` | The person the task names; while it names none, a member of its queue. Supervisors always. Never a service key. |
| Deliver a message | `{"type": "message.received", "name": "documents", "payload": {"docs": "received"}}` | Staff and service keys. Every task of the instance waiting for that message takes it. |
| Cancel the instance | `{"type": "process.cancelled", "reason": "withdrawn"}` | Supervisors |
| Retry a failed task | `{"type": "task.retried", "task": "t5"}` | Supervisors |

A task's id, such as `t3`, comes from the instance's open tasks. Completing a task that has already finished answers `409 task-closed`. An event sent again with the `Idempotency-Key` it was first sent with is answered with the instance as it stands, and the header `Idempotent-Replayed: true`; it is not applied twice.

Timers fire on their own. When a timer cannot fire because what follows it fails, such as a condition that cannot be evaluated on the instance's variables, the timer is kept as **stuck**: it is never fired again, the instance shows why, and the list's `attention=true` finds it. A supervisor then cancels the instance.

An instance is `running`, `completed`, `terminated` (by a terminate end event), `failed` (by an error no boundary event caught) or `cancelled`.

A refused call answers with a `code` and a `message`: `404 unknown-instance` for an instance that does not exist or belongs to another project, `422 invalid-event` for a body that is no event, `403 forbidden` for a sender who may not send it, and `409` with Keel's reason for anything the instance cannot take, such as `unknown-outcome` or `check-failed`.

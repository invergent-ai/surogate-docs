---
title: BPMN processes
sidebar:
  label: BPMN processes
---

Besides case types, Keel runs **processes** drawn in BPMN 2.0, the notation of process modellers such as Camunda Modeler and bpmn.io. A process is a BPMN file among the project's definitions. It is published through a draft, as a case type is, and each run of it is an **instance**.

A builder puts a process file in a draft through Keel Builder's API, and staff or another system start instances through Keel's API. Staff work a process's tasks in the business app, as they work a case's steps: in the same queues, on the Work page, and on the instance's own page. The designer, a list of processes and a diagram of each instance come in a later release. The Review and publish page already shows a process file's warnings.

## A process file

- One process is one file, `processes/<key>.bpmn`, in the project's definitions. Its key starts with a letter or a digit and holds letters, digits, `-` and `_`.
- Keel keeps the file exactly as it was saved, diagram layout included: the file you download is the file you uploaded.
- A file is at most 5,000,000 bytes and holds one process.
- What BPMN has no place for, such as a task's queue or the type of a variable, is written in Keel's own elements, in the namespace `https://surogate.ai/keel/bpmn/1`, inside the `extensionElements` of the BPMN element they describe. See [Keel's settings in the file](#keels-settings-in-the-file).

## What Keel runs

| Element | What Keel does |
|---|---|
| **Start event** | The instance starts here. Only a plain start event: a timer or message start event is refused. |
| **User task**, **manual task** | Waits for a person to complete it, from a queue. It can have a goal and a deadline. |
| **Business rule task** | Evaluates one of the project's [rules](/keel/builder/rules/), a decision table or a scorecard, and writes its results to variables. It never waits. |
| **Receive task**, **message catch event** | Waits for a message of its name. |
| **Timer catch event** | Waits for a duration, such as `PT2H` or `P3D`, or until a date. A repeating (cycle) timer is refused. |
| **Timer boundary event** | Fires on a task or a subprocess after a duration or at a date. An interrupting one withdraws the activity; a non-interrupting one starts its path beside it. |
| **Error boundary event** | Catches an error thrown inside the task or subprocess it sits on: the one with the error's code first, else one without a code. |
| **Exclusive gateway** | Takes the first outgoing flow, in the order written, whose condition holds, else its default flow. |
| **Parallel gateway** | Splits into every outgoing flow, or waits for every incoming one. |
| **Event-based gateway** | Waits for whichever of its timer and message catches comes first. |
| **End event** | Plain, **terminate** (ends everything still open in its process or subprocess), or **error** (throws its error's code). |
| **Embedded subprocess** | Runs its own flow, and may carry boundary events. |
| **Lanes** | A lane's name is the queue of the tasks in it, read as a queue key: lower case, with each run of other characters as `_`. A lane named "Back Office" is the queue `back_office`. |

Not run yet, refused when published: service tasks, call activities, multi-instance tasks, inclusive gateways, event subprocesses, data stores, message boundary events and pools that send each other messages.

Refused: script tasks, plain tasks, send tasks, business rule tasks that name a DMN decision instead of a Keel rule, throw events, signals, escalations, compensation, transactions, ad hoc subprocesses, conditional and link events, loops on a task (draw the loop with a gateway), data objects and correlation keys. Each refusal names the element.

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
      <keel:service-level goal="PT4H" deadline="P2D" business="true" escalate-to="committee-leads"/>
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
| `keel:service-level` | The task's `goal` and `deadline`, durations counted from the moment the task is ready, such as `PT4H` or `P2D`. The deadline is required. With `business="true"` they count working time on the process's calendar. With `escalate-to`, a missed deadline puts an escalation in that queue. See [Goals and deadlines](#goals-and-deadlines). |

### A business rule task

```xml
<bpmn:businessRuleTask id="score" name="Score the application">
  <bpmn:extensionElements>
    <keel:rule key="loan-score">
      <keel:assign result="score" variable="score"/>
      <keel:assign result="reasons" variable="reasons"/>
    </keel:rule>
  </bpmn:extensionElements>
</bpmn:businessRuleTask>
```

- `keel:rule` names one of the project's rules by its `key`. Each `keel:assign` writes a `result` of the rule to a `variable`, as a case type's rule node does. A task must assign at least one result.
- When the task is reached, Keel evaluates the version of the rule in force at that moment on the instance's variables, writes the results and goes on. A scorecard's results are `score` and `reasons`.
- If the rule gives no answer, such as a decision table where no row matches and there is no default, Keel refuses what reached the task: a completion answers `409 rule-error`, a start is refused, and a timer is kept as stuck.

### A message catch, a receive task, a timer

- `keel:message` on a message catch event or a receive task lists, with `keel:write`, the variables the message may write. A message that holds anything else is refused.
- `keel:timer business="true"` on a timer makes it count business time on the process's calendar.

## Publishing a process

A process file is saved in a draft and published with it, like any other file of the project:

1. Save the file in an open draft: `PUT /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}`, with the file as the body.
2. Run the [dry run](/keel/builder/publish/#dry-run), or open **Review and publish**. The checks read the file against what Keel runs, its settings, its variables, its conditions and the project's calendars.
3. Publish. The process has a new version, and new instances start on it.

The checks also refuse:

- a task whose queue the project does not have, whether the task names it, its lane gives it or the process does, and a deadline that escalates to a queue the project does not have;
- a business rule task that names a rule the project does not have, a rule with no version in force, a rule whose conditions read a variable the process does not declare, a rule whose own tests fail, a result the rule does not always return, and a value the rule can return that its variable cannot hold.

When a rule is published again, Keel checks the new version against the processes that use it, their current versions and any version with running instances, as it checks the case types that use it.

A problem that Keel cannot run, such as a script task, refuses the publish and names the element. A vendor extension, such as Camunda's, Flowable's or SpiffWorkflow's own properties, is a **warning**: Keel ignores it and never runs it, and the publish goes on. The review page lists warnings under **Warnings**, and **Publish** stays on.

Running instances finish on the version they started on.

Builders read the published processes with:

| To | Call |
|---|---|
| List the processes, with each version's running instances | `GET /api/build/projects/{project}/processes` |
| Download a version's file | `GET /api/build/projects/{project}/processes/{key}/versions/{version}` |
| Read the file in a draft | `GET /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}` |
| Put the file back as the draft started with it | `POST /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}/revert` |

## Working a process's tasks

A process's user and manual tasks are worked in the business app, like a case's steps.

- **Work.** A task waits in its queue, or with the person the file names, and shows in **Mine**, in the queue's views and in **Get next**, as a step does. Its row reads the instance's number and the process's name, such as **P-000001 · Loan review**. On its item, **Open process** opens the instance's page. **Get next case** on the Cases page opens it too. A process's task is handed to people only: **Delegate** and **Reassign** offer no agents for it.
- **The instance's page** shows the process's name, the instance's number, version and start day, and its status: **Running**, **Completed**, **Ended**, **Failed** or **Cancelled**. A failed instance says which error ended it and where.
  - A task you hold shows its form under **Your task**, with **Submit** and **Return to queue**. A task waiting in one of your queues asks you to **Claim** it first.
  - A task someone else holds shows under **Now**, with who holds it.
  - **Waiting for** lists the timers and messages the instance waits on, and **Process data** lists its variables by their labels.
  - The page stays current on its own.
- **Refusals.** When a task closes before your submission arrives, because someone else completed it or a timer withdrew it, the page says "This step is no longer open." and shows the instance as it now is. An instance that ended says "This process has ended."
- **Away.** While you are away, a process's task assigned to you moves as your absence says, as a step does, and supervisors are told of what stays with you.
- **Notices.** A task that reaches you or your queue is a notice, and its mail names the process and the task.
- **Authority limits.** The **Team** page's authority limits dialog lists the process tasks that check each scope beside the case types' steps.

### Goals and deadlines

A task with a `keel:service-level` has a goal and a deadline from the moment it is ready.

- Its work item carries them, so the queue serves it by its deadline, counts it among the items past their deadline, and sends its holder or its queue the goal-near and deadline-near notices, as it does for a step.
- On the instance's page the task shows its service level, such as **Past deadline**, and its goal and deadline.
- A missed goal is only recorded in the history.
- A missed deadline with `escalate-to` puts an escalation in that queue. The page shows **Escalated to** that queue. Members of that queue may complete the task, and the escalation closes when the task does. Without `escalate-to`, a missed deadline is only recorded.
- When the task leaves, completed or withdrawn, its goal and deadline go with it. A task reached again in a loop counts from its new start.

A process's tasks never count in the cases' figures.

## Running instances

Staff sign in as they do for the business app; another system uses a [service key](/keel/systems/). Keel sets who acted and when on everything they send: a body that names `actor` or `at` is refused.

| To | Call | Who |
|---|---|---|
| Start an instance | `POST /api/projects/{project}/processes` with `{"process": "loan-review", "data": {"amount": "20000.00"}}` | Staff and service keys |
| List instances, newest first | `GET /api/projects/{project}/processes`, with `process`, `status`, `attention=true`, `cursor` and `limit` | Staff and service keys |
| Read an instance | `GET /api/processes/{instance_id}` | Staff and service keys |
| Read it as its page shows it: its tasks with their forms and who holds each, its goals and deadlines, what it waits for, its data | `GET /api/processes/{instance_id}/outline` | Staff and service keys |
| Follow its changes as server-sent events | `GET /api/processes/{instance_id}/live` | Staff |
| Its open tasks | `GET /api/processes/{instance_id}/tasks` | Staff and service keys |
| Its history | `GET /api/processes/{instance_id}/history` | Staff and service keys |
| Check its history replays | `POST /api/processes/{instance_id}/replay` | Staff and service keys |
| Send it an event | `POST /api/processes/{instance_id}/events` | See below |

Starting an instance answers its `instance_id`, its `number`, such as `P-000001`, and its status. The start data must fit the declared variables. Send an `Idempotency-Key` header with each start: a start sent again with the same key answers with the instance it started the first time.

The events an instance takes:

| Event | Body | Who sends it |
|---|---|---|
| Complete a task | `{"type": "task.completed", "task": "t3", "outcome": "approve", "output": {"note": "fine"}}` | Whoever holds its work item; while no one holds it, a member of its queue. A member of the queue its missed deadline escalated to. Supervisors always. Never a service key. |
| Deliver a message | `{"type": "message.received", "name": "documents", "payload": {"docs": "received"}}` | Staff and service keys. Every task of the instance waiting for that message takes it. |
| Cancel the instance | `{"type": "process.cancelled", "reason": "withdrawn"}` | Supervisors |
| Retry a failed task | `{"type": "task.retried", "task": "t5"}` | Supervisors |

A task's id, such as `t3`, comes from the instance's open tasks. Completing a task that has already finished answers `409 task-closed`. An event sent again with the `Idempotency-Key` it was first sent with is answered with the instance as it stands, and the header `Idempotent-Replayed: true`; it is not applied twice.

Timers fire on their own. When a timer cannot fire because what follows it fails, such as a condition that cannot be evaluated on the instance's variables, the timer is kept as **stuck**: it is never fired again, the instance shows why, and the list's `attention=true` finds it. A supervisor then cancels the instance.

An instance is `running`, `completed`, `terminated` (by a terminate end event), `failed` (by an error no boundary event caught) or `cancelled`.

A refused call answers with a `code` and a `message`: `404 unknown-instance` for an instance that does not exist or belongs to another project, `422 invalid-event` for a body that is no event, `403 forbidden` for a sender who may not send it, and `409` with Keel's reason for anything the instance cannot take, such as `unknown-outcome`, `check-failed` or `rule-error`.

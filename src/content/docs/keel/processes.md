---
title: BPMN processes
sidebar:
  label: BPMN processes
---

Besides case types, Keel runs **processes** drawn in BPMN 2.0, the notation of process modellers such as Camunda Modeler and bpmn.io. A process is a BPMN file among the project's definitions. It is published through a draft, as a case type is, and each run of it is an **instance**.

A builder draws a process in a draft on Keel Builder's [Processes](/keel/builder/processes/) page, which lists the project's processes and draws each one's file, uploads a file made in another modeller, or saves it through Keel Builder's API. Staff or another system start instances through Keel's API. Staff work a process's tasks in the business app, as they work a case's steps: in the same queues, on the Work page, and on the instance's own page. A process's tasks can also call other systems, and agents can work them or draft them for the person who completes them.

## A process file

- One process is one file, `processes/<key>.bpmn`, in the project's definitions. Its key starts with a letter or a digit and holds letters, digits, `-` and `_`.
- Keel keeps the file exactly as it was saved, diagram layout included: the file you download is the file you uploaded, or, once the diagram is changed in Keel Builder, the file Keel Builder wrote after that change. Keel Builder writes the whole file in its own layout: XML comments are dropped, and the elements, their settings and the diagram's layout are kept.
- A file is at most 5,000,000 bytes and holds one process.
- What BPMN has no place for, such as a task's queue or the type of a variable, is written in Keel's own elements, in the namespace `https://surogate.ai/keel/bpmn/1`, inside the `extensionElements` of the BPMN element they describe. See [Keel's settings in the file](#keels-settings-in-the-file).

## What Keel runs

| Element | What Keel does |
|---|---|
| **Start event** | The instance starts here. Only a plain start event: a timer or message start event is refused. |
| **User task**, **manual task** | Waits for a person to complete it, from a queue. It can have a goal and a deadline. A user task can have an agent that drafts for the person: see [An agent that drafts for a person](#an-agent-that-drafts-for-a-person). |
| **Business rule task** | Evaluates one of the project's [rules](/keel/builder/rules/), a decision table or a scorecard, and writes its results to variables. It never waits. |
| **Service task** that calls a system | Calls another system's API through one of the process's connections, waits for the answer, writes its values to variables and goes on. See [A service task that calls a system](#a-service-task-that-calls-a-system). |
| **Service task** that calls an agent | Starts an agent on the task. The agent completes it under the task's contract, or asks a person. See [A service task that calls an agent](#a-service-task-that-calls-an-agent). |
| **Service task** that starts a case | Starts a case of one of the project's case types, and waits for it to close or goes on at once. See [A service task that starts a case](#a-service-task-that-starts-a-case). |
| **Receive task**, **message catch event** | Waits for a message of its name. |
| **Timer catch event** | Waits for a duration, such as `PT2H` or `P3D`, or until a date. A repeating (cycle) timer is refused. |
| **Timer boundary event** | Fires on a task or a subprocess after a duration or at a date. An interrupting one withdraws the activity; a non-interrupting one starts its path beside it. |
| **Error boundary event** | Catches an error thrown inside the task or subprocess it sits on: the one with the error's code first, else one without a code. |
| **Exclusive gateway** | Takes the first outgoing flow, in the order written, whose condition holds, else its default flow. |
| **Parallel gateway** | Splits into every outgoing flow, or waits for every incoming one. |
| **Event-based gateway** | Waits for whichever of its timer and message catches comes first. |
| **End event** | Plain, **terminate** (ends everything still open in its process or subprocess), or **error** (throws its error's code). |
| **Embedded subprocess** | Runs its own flow, and may carry boundary events. |
| **Lanes** | A lane's name is the queue of the tasks in it, read as a queue key: lower case, with each run of other characters as `_`. A lane named "Back Office" is the queue `back_office`. Keel Builder names a lane for the queue you pick in its panel. |

Not run yet, refused when published: call activities, multi-instance tasks, inclusive gateways, event subprocesses, data stores, message boundary events and pools that send each other messages.

Refused: script tasks, plain tasks, send tasks, business rule tasks that name a DMN decision instead of a Keel rule, throw events, signals, escalations, compensation, transactions, ad hoc subprocesses, conditional and link events, loops on a task (draw the loop with a gateway), data objects and correlation keys. Each refusal names the element.

Conditions are written in CEL over the process's variables, as a case type's are, for example `amount <= 250000.0`.

## Keel's settings in the file

Each setting sits in the `extensionElements` of its BPMN element. An element or attribute Keel does not know, or one where it has no meaning, is a problem when the file is published: nothing is ignored silently.

Keel Builder's panel sets the process's settings and variables, a user or manual task's settings, a user task's drafting agent, a service task's call (a call to a system, a call to an agent or the start of a case), a business rule task's rule, a lane's queue (its name), a sequence flow's condition, an exclusive gateway's default flow, a timer, a message and an error: see [Changing the diagram](/keel/builder/processes/#changing-the-diagram). A change made in the panel keeps whatever else the file holds.

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

- `keel:process`: `queue`, the queue of every task that names none and lies in no lane, `calendar`, the [calendar](/keel/builder/rules/#calendars) business timers count on, and `knowledge`, the knowledge bases the process grants to its agents, separated by spaces.
- `keel:variables`: one `keel:variable` for each variable the instance keeps, with the same types as a case type's [fields](/keel/builder/data/), except `file`. A variable can be `required`, which its start data must then hold, and `pii`. A process has only the variables it declares.

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

### A service task that starts a case

```xml
<bpmn:serviceTask id="open_claim" name="Open the claim">
  <bpmn:extensionElements>
    <keel:case type="claim" wait="true" cancel-event="withdrawn" resolution-variable="claim_outcome">
      <keel:field name="amount" variable="amount"/>
      <keel:field name="reason" variable="reason"/>
      <keel:result variable="payout" field="payout"/>
    </keel:case>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

| Setting | What it does |
|---|---|
| `type` | The case type the task starts, by its key. Required. |
| `wait` | `true` waits for the case to close; `false` starts it and goes on at once. Required. |
| `keel:field` | A field of the case (`name`) and the variable that fills it (`variable`). A field the case type requires must be filled. Each field once. |
| `keel:result` | A variable (`variable`) that takes a field of the case (`field`) when the case closes. Each variable once. |
| `resolution-variable` | A string or choice variable that takes the case's resolution, such as `approved`, when the case closes. It cannot also be a `keel:result` variable. |
| `cancel-event` | The case event Keel sends the case when the instance leaves the task first: by a boundary event, a cancel or its end. The case type must declare it as interrupting, and none of its wait nodes may wait for it. |
| `keep-running` | `true` leaves the case running when the instance leaves the task first. |

A task that waits names exactly one of `cancel-event` and `keep-running`. A task that does not wait names neither, and no `keel:result` or `resolution-variable`: it receives nothing.

When the case closes, a waiting task completes: its `keel:result` variables and its `resolution-variable` take the case's values. Otherwise the task throws a BPMN error, which an error boundary event on the task, or on a subprocess around it, catches by its code; uncaught, it fails the instance:

| Error | When |
|---|---|
| `case-not-started` | Keel could not start the case. |
| `case-failed` | A step's failure closed the case. |
| `case-values` | The case closed with a value its variables cannot hold. Nothing is written. |

### A service task that calls a system

```xml
<bpmn:serviceTask id="check" name="Check the bureau">
  <bpmn:extensionElements>
    <keel:system connection="bureau" method="POST" path="/checks/{customer}" timeout-seconds="30" accept="404">
      <keel:header name="X-Reference">{"$case": "number"}</keel:header>
      <keel:body>{"amount": {"$field": "amount", "as": "number"}}</keel:body>
      <keel:output variable="clear" path="$.body.clear"/>
    </keel:system>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

| Setting | What it does |
|---|---|
| `connection` | The [connection](#a-processs-connections) the call goes through, by name. Required. |
| `method`, `path` | `GET`, `POST`, `PUT`, `PATCH` or `DELETE`, and the path after the connection's base URL. Required. `{variable}` in the path puts a variable's value in it; `{case.id}`, `{case.number}` and `{case.type}` put the instance's own: its id, its number and `process:<key>`. |
| `keel:query`, `keel:header` | A `name` and a JSON value: a JSON string such as `"keel"`, or `{"$field": "amount"}` for a variable's value. Add `"optional": true` to leave it out when the variable has no value. `{"$case": "id"}`, `{"$case": "number"}` and `{"$case": "type"}` are the instance's own. Each name once. |
| `keel:body` | A JSON template for `POST`, `PUT` and `PATCH`, with the same markers. `"as": "number"` writes a decimal variable as a JSON number. |
| `keel:output` | A `variable` that takes the value at a `path` of the response, such as `$.body.clear`. `$.status` and `$.headers.name` read the status and a header. Each variable once. |
| `accept` | Statuses outside 2xx, separated by spaces, that count as answers to map, such as `404 409`. |
| `timeout-seconds` | How long one call may take. Without it, the connection's default. |

The task waits while the call is out. The answer completes it with its one outcome, `done`, and the values its outputs name. The history keeps where each value came from: the connection and the path in the response. Every call but a `GET` carries an idempotency key, the same on each attempt of one call, in the header the connection names.

Credentials never go in a call's headers; they belong to the connection. A call that sets a header its connection sends itself is refused when the process is published.

A call that fails for good is not a BPMN error, and no error boundary event catches it. After Keel's attempts, a refused status, a call that did not answer in time, or an answer a variable cannot hold leaves the task with an **incident**. See [Incidents](#incidents).

### A process's connections

A call goes through a **connection** of the process, as a case type's system steps go through its own: its base URL, how calls authenticate, and the credential they send. A process's connections and credentials are its own. A case type of the same key has its own, apart.

- A connection is the file `process-connections/<process>/<name>.json`, with the settings of a [case type's connection](/keel/builder/connections/#a-connection): its base URL, its authentication, its idempotency-key header and its default timeout. A connection that sends a credential must use `https`.
- It is made and changed in a draft in Keel Builder, on the **Connections** tab of the process's page, [as its page says](/keel/builder/processes/#the-connections-tab), and published with it. Through the API, `PUT /api/build/projects/{project}/drafts/{draft_id}/files/process-connections/{process}/{name}` saves the file, `GET` on the same path reads it, and `POST` on `…/revert` puts it back as the draft started with it. A connection file is never deleted.
- Its credentials are not part of a draft. They are set on the published connection and apply at once, in the **Connections** tab of the process's page in Keel Builder, [as its page says](/keel/builder/processes/#the-connections-tab), or through the API: `PUT /api/build/projects/{project}/processes/{process}/connections/{name}/credentials/{kind}` sets one, in place of any it had, and `DELETE` on the same path deletes it. They take a case type's bodies, are for editors and owners, and are refused as a case type's are. A connection the process never published is `404 unknown-connection`, and a credential that does not exist is `404 unknown-credential`.

### A service task that calls an agent

```xml
<bpmn:serviceTask id="assess" name="Assess the claim">
  <bpmn:extensionElements>
    <keel:agent agent="assessor" raise-hand-to="underwriting" tools="search read" knowledge="product-terms"
                mcp-servers="crm" outcome-variable="decision">
      <keel:read variable="amount"/>
      <keel:write variable="score" required="true"/>
      <keel:write variable="band"/>
      <keel:outcome name="approve" requires="band"/>
      <keel:check when="amount &gt; 0.0" message="The amount must be positive."/>
      <keel:maker-checker task="review"/>
      <keel:authority amount="amount" scope="claims"/>
      <keel:service-level deadline="P1D" goal="PT4H" escalate-to="leads"/>
    </keel:agent>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

| Setting | What it does |
|---|---|
| `agent` | The agent, by its id in Studio. Required. |
| `raise-hand-to` | The queue the agent's questions go to, and the queue the task goes to when the agent is switched off. Required. |
| `tools`, `mcp-servers`, `knowledge` | What the agent may use here, separated by spaces. Without one, the agent keeps its own tools and MCP servers, and the process's knowledge. An empty value allows none. A task can narrow what the agent has, never widen it: each knowledge base must be one the process grants with `keel:process knowledge`. |
| `keel:read` | A variable the agent is sent when it starts. |
| `keel:write`, `keel:outcome`, `outcome-variable`, `keel:check`, `keel:maker-checker`, `keel:authority`, `keel:service-level` | The task's contract, as on a [user task](#a-user-or-manual-task). A task holds one of `keel:system`, `keel:agent` and `keel:case`. |

- **The contract.** When the task starts, Keel starts the agent in a session of its own and sends it the variables it reads, what it may write and its outcomes. It sees the process's key, as `process:<key>`, where a case's agent sees the case type. The agent completes the task with one of its outcomes and the values it writes, with a source for each value. The task's checks, maker-checker and authority limit apply to it as to a person; its limits are set on the Team page.
- **A refused output.** An output the contract refuses is answered with the reason, and the agent tries again. The refusal that reaches the limit raises the agent's hand.
- **A raised hand.** The agent asks a question, sometimes with answer choices and evidence. The task pauses, and the question goes to the `raise-hand-to` queue as an item that members answer on the Work page, or a supervisor. The agent resumes with the answer. A question never expires.
- **A task the agent is off for.** A task that starts, or is retried, while the project has the agent switched off opens for people as a step in the `raise-hand-to` queue, with the form of its contract, and a person completes it with no sources. An agent already at work keeps working, and its completion is taken.
- **A task that fails.** If the runtime refuses the agent, its start gives up, its session fails, or a quiet run's session is gone, the task is left with an **incident**: see [Incidents](#incidents).
- **People can message the agent while it works.** See [Working a process's tasks](#working-a-processs-tasks).

### An agent that drafts for a person

```xml
<bpmn:userTask id="assess" name="Assess the claim">
  <bpmn:extensionElements>
    <keel:task queue="underwriting" outcome-variable="decision">…</keel:task>
    <keel:agent agent="assessor" raise-hand-to="underwriting" tools="search" knowledge="product-terms">
      <keel:read variable="amount"/>
    </keel:agent>
  </bpmn:extensionElements>
</bpmn:userTask>
```

A `keel:agent` beside the `keel:task` of a user task drafts for the person who completes it. The agent works first; its draft fills the person's form; the person checks it and completes the task.

- `keel:agent` is a sibling of `keel:task`, never inside it. It names `agent` and `raise-hand-to`, may narrow `tools`, `mcp-servers` and `knowledge` as a service task's does, and holds only `keel:read`. The contract is the task's own `keel:task`. A manual task cannot hold one, and a user task holds one at most.
- **When it starts.** The person's item opens at once, and the agent starts as the task becomes ready. The person may complete the task before any draft, which stops the agent.
- **The draft.** The agent proposes an outcome and values, with a source for each value. A draft meets what a completion's report meets: a known outcome, only what the task writes, valid values, the outputs the task and the outcome require. It does not meet the task's checks, maker-checker or authority limit: the person's completion does. A draft writes no variable. A new draft replaces the last. The history keeps the sources of each value; the form shows none.
- **Only the person decides.** The person completes the task under its whole contract, and the completion is theirs. The history records, for each value, whether the agent or the person gave it: a value the person left as drafted is the agent's, and one they changed is theirs.
- **A raised hand.** The agent asks the `raise-hand-to` queue, as above. While its hand is up, no one completes the task: the question comes first.
- **A revision, and a message.** The person who holds the task can ask the agent to revise its draft with a note, and anyone on the staff can message it while it drafts. See [Working a process's tasks](#working-a-processs-tasks).
- **When the agent cannot help.** An agent that fails for good, or one switched off when the task starts, leaves the person to work alone. This is not an incident: the person's item stays open, nothing needs a supervisor, and the task has no retry. The history records `agent.failed` or `agent.disabled`.
- A task an agent drafts is never given to an agent from a queue: only a person finishes it.

### A message catch, a receive task, a timer

- `keel:message` on a message catch event or a receive task lists, with `keel:write`, the variables the message may write. A message that holds anything else is refused.
- `keel:timer business="true"` on a timer makes it count business time on the process's calendar.

## Cases and processes that start each other

A case's [process node](/keel/builder/flow-nodes/#processes) starts a process, and a process's [start-a-case task](#a-service-task-that-starts-a-case) starts a case. Keel starts the other side itself, a moment after the case or the instance reached the node or the task, and keeps a link between the two.

- A side that waits takes the other's end: a case leaves its process node by Ended or Failed, and a process's task completes or throws its error.
- When the waiting side moves on first, Keel withdraws the other: it cancels a process whose case no longer waits at its node, and sends a case its task's `cancel-event`, unless the task says `keep-running`.
- When Keel cannot start the other side, such as a retired case type or values that no longer fit, the waiting side takes its error path.
- A chain of starts stops at eight. The ninth start in a chain is refused, and its waiting side takes its error path, so a case type and a process that start each other never loop without end.

The business app shows the links on both sides:

- On a case's page, the **Now** card of a process node shows the instance by its number, its process and how it stands, such as **P-000003 · KYC check · Running**, linked to its page; until Keel starts it, **Waiting for the process** and the process's key made readable, such as **Waiting for the process Kyc check**. Under it, "It could not start: …" says why Keel could not start the process, and "Keel could not take its end: …" why the case, which still waits, could not take how the process or its start ended.
- A case a process started shows **Started by** and the instance, such as **P-000001 · Claim settlement**, over its stage bar. A case that started processes lists them under **Processes**: each instance and how it stands, the node that started it and when.
- On an instance's page, **Started by** names the case that started it. **Waiting for** shows each task that waits on its case, such as **Open the claim · CL-000001 · Claim · Open**, or "waits for its case to start", with the same notes. **Cases it started** lists the cases its tasks started.
- The Cases page's **Now** column names the process a case waits on, such as `Know your customer · KYC check`.
- A case's **Full history** shows "Requested the process" and the process's key made readable, such as "Requested the process Kyc check", at the node, and the process's end, such as "Process P-000003 ended", at the way the case left by.

## Publishing a process

A process file is saved in a draft and published with it, like any other file of the project:

1. Save the file in an open draft: in Keel Builder, with **New process** on the [Processes](/keel/builder/processes/) page or **Upload a file** on a process's page, or through the API with `PUT /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}`, with the file as the body.
2. Run the [dry run](/keel/builder/publish/#dry-run), or open **Review and publish**. For editors and owners, a process's Diagram tab checks its draft by itself and lists the [problems](/keel/builder/processes/#problems) beside the drawing. The checks read the file against what Keel runs, its settings, its variables, its conditions and the project's calendars.
3. Publish. The process has a new version, and new instances start on it.

The checks also refuse:

- a task whose queue the project does not have, whether the task names it, its lane gives it or the process does, and a deadline that escalates to a queue the project does not have;
- a service task whose connection the process has no file for, a call that sets a header its connection sends itself, and an agent task or a drafting agent whose agent, tool, MCP server or knowledge base the project or the agent does not have, whose raise-hand queue the project does not have, or whose knowledge the process does not grant (the codes below);
- a business rule task that names a rule the project does not have, a rule with no version in force, a rule whose conditions read a variable the process does not declare, a rule whose own tests fail, a result the rule does not always return, and a value the rule can return that its variable cannot hold.

When a rule is published again, Keel checks the new version against the processes that use it, their current versions and any version with running instances, as it checks the case types that use it.

### Checking what starts what

A start is checked when the case type or the process that holds it is published, against what it starts as the publish leaves it. It is checked again when what it starts is published again, at each stored version that starts it: the current version of each case type or process the publish leaves alone, and each version that cases or instances still run on. Such a problem is at `<case type> v<n>: <node>` or `<process> v<n>: <task>`, in the file published again. A retired case type is checked against the processes that start it like any other, and its republish is never refused `retired-case-type`. A problem at a version cases or instances still run on stays until nothing runs on it, or the file fits it again; a problem at a current version does not end by itself.

| Problem | Where | What it says |
|---|---|---|
| `unknown-process` | The case type's file, at the node | "*node* starts *process*, a process the project does not have" |
| `unknown-case-type` | The process's file, at the task | "*task* starts *case type*, a case type the project does not have" |
| `retired-case-type` | The process's file, at the task | "*task* starts *case type*, which is retired: no new case can start on it" |
| `process-input` | The case type's file, or the process's file at `<case type> v<n>: <node>` | "*process* requires *variable*, which no input fills", "inputs names *variable*, which *process* does not declare", "*variable*, a *type*, is filled from *field*, a *type* of another shape", "*field* may hold *choices*, which *variable* does not take" |
| `process-output` | The same | "*field* receives *variable*, which *process* does not declare", "*field*, a *type*, receives *variable*, a *type* of another shape", "*variable* may hold *choices*, which *field* does not take" |
| `case-input` | The process's file, or the case type's file at `<process> v<n>: <task>` | "*case type* requires *field*, which no keel:field fills", "keel:field names *field*, which *case type* does not declare", "*field*, a *type*, is filled from *variable*, a *type* of another shape", "*variable* may hold *choices*, which *field* does not take" |
| `case-output` | The same | "*variable* receives *field*, which *case type* does not declare", "*variable*, a *type*, receives *field*, a *type* of another shape", "*field* may hold *choices*, which *variable* does not take"; and in the process's own file, "the resolution variable *variable* must be a string or a choice variable" |
| `case-cancel` | The same | "*case type* has no event *event*", "*event* of *case type* does not interrupt: it would not withdraw the case", "*node* of *case type* waits for *event*: it would take the event as the one it waits for"; and in the process's own file, "*task* waits on its case: name cancel-event, the case event that withdraws it when the process leaves the task, or keep-running="true"" and "*task* names both cancel-event and keep-running: it does one or the other" |
| `broken-definition` | `<key> v<n>` | "*key* v*n* is stored but no longer loads: …" |
| `checks-stale` | `<case type> v<n>` or `<process> v<n>` | "cases started on it while the publish was checked; publish again", or "instances started on it while the publish was checked; publish again" |

### Checking what a process calls and which agents work it

A process's calls and agents are checked when the process is published, and a connection published again is checked against the current version of each process the publish leaves alone and every process version instances still run on.

| Problem | Where | What it says |
|---|---|---|
| `unknown-connection` | The process's file, at the task | "*task* calls *connection*, which *process* has no connection file for: process-connections/*process*/*connection*.json" |
| `system-request` | The process's file, at the task; the connection's file, at `<process> v<n>: <task>` | "*task* sets *header*, which connection *connection* sends itself", or, for the API key's header, "*task* sets *header*, the header of connection *connection*'s API key: credentials belong in the connection's credential, never in a step" |
| `unknown-agent` | The process's file, at the task | "*agent* is not an agent of this project" |
| `agent-tool` | The process's file, at the task | "*agent* has no tool *tool*" |
| `agent-mcp-server` | The process's file, at the task | "*agent* has no MCP server *server*" |
| `unknown-knowledge` | The process's file, at the process | "*knowledge base* is not a knowledge base of this project" |
| `knowledge` | The process's file, at the task | "*knowledge base* is not knowledge of the process" |
| `unknown-queue` | The process's file, at the task | "*task* raises its hand to the queue *queue*, which the project does not have" |

Publishing records the names of the agents and knowledge bases a process names, as it does for case types. A `system-request` problem at a version instances still run on stays until none does, or the connection's file fits it again. One at a current version stays until you publish a new version of the process, or the connection's file fits it again.

A problem at an old version is fixed in one of these ways:

- Change the file you publish so that it fits that version again.
- At a version cases or instances still run on: move its open cases to a newer version of the case type, or wait for them to close, or for the instances to end or be cancelled.
- At a current version: publish a new version of that case type or process in the same draft. The new version is then checked instead.

A problem that Keel cannot run, such as a script task, refuses the publish and names the element. A vendor extension, such as Camunda's, Flowable's or SpiffWorkflow's own properties, is a **warning**: Keel ignores it and never runs it, and the publish goes on. The review page lists warnings under **Warnings**, and **Publish** stays on.

Running instances finish on the version they started on.

Builders read the published processes with:

| To | Call |
|---|---|
| List the processes, with each version's running instances | `GET /api/build/projects/{project}/processes` |
| Download a version's file | `GET /api/build/projects/{project}/processes/{key}/versions/{version}` |
| Read the file in a draft | `GET /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}` |
| Read the variables a version declares | `GET /api/build/projects/{project}/processes/{key}/versions/{version}/variables` |
| Read the variables the file in a draft declares, before its checks pass | `GET /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}/variables` |
| Put the file back as the draft started with it | `POST /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}/revert` |

## Working a process's tasks

A process's user and manual tasks are worked in the business app, like a case's steps.

- **Work.** A task waits in its queue, or with the person the file names, and shows in **Mine**, in the queue's views and in **Get next**, as a step does. Its row reads the instance's number and the process's name, such as **P-000001 · Loan review**. On its item, **Open process** opens the instance's page. **Get next case** on the Cases page opens it too. **Delegate** and **Reassign** offer people and agents, as for a case's items: see [Agents in a process's queues](#agents-in-a-processs-queues).
- **The instance's page** shows the process's name, the instance's number, version and start day, and its status, with the tasks, what it waits for, its diagram, its data and its history. A task you hold shows its form under **Your task**, with **Submit** and **Return to queue**. A task waiting in one of your queues asks you to **Claim** it first. A task someone else holds shows under **Now**, with who holds it. The page stays current on its own. See [An open process](/keel/business/open-process/). The [Processes](/keel/business/processes/) page lists the project's instances and starts one.
- **Refusals.** When a task closes before your submission arrives, because someone else completed it or a timer withdrew it, the page says "This step is no longer open." and shows the instance as it now is. An instance that ended says "This process has ended."
- **Away.** While you are away, a process's task assigned to you moves as your absence says, as a step does, and supervisors are told of what stays with you.
- **Notices.** A task that reaches you or your queue is a notice, and its mail names the process and the task.
- **Authority limits.** The **Team** page's authority limits dialog lists the process tasks that check each scope beside the case types' steps.

### Tasks agents work

A task with an agent shows what the agent does and what you may do about it. **Open its session** shows the agent's session, read-only, while its run has one: see [Watch](/keel/business/watch/). **Message the agent** is on every task whose agent takes a message now: any member of the staff may use it.

| The task | If it is yours to work, or yours to take | If it is not |
|---|---|---|
| An agent at work on a task | — | **Now**: "*Agent* is working · *Starting*, *Running* or *Waiting*", its goal and deadline, its plan and when it was last active, and where its question would go, such as "If the agent needs a person, its question goes to Underwriting, which includes you." **Message the agent**, **Open its session**. |
| An agent's question | **Your task**: "*Agent* asked a question · *queue*", its progress, **Answer in Work**, **Open its session**. | **Now**: "*Agent* asked a question" and who holds the question, such as "Held by Mihai Ionescu", or the queue it waits in. |
| An agent task whose agent failed for good | — | **Now**: "*Agent* could not finish this task: a supervisor retries it or cancels the process." No button. |
| An agent task people work, because its agent is switched off | **Your task**: "*Agent* is off: people work this task." and the task's form, or **Claim** first. | **Now**: who holds it, and the same line. |
| A user task its agent drafts, while it drafts | **Your task**: "*Agent* is drafting · *run*" with its progress, **Message the agent** and **Open its session**, over the form, or over **Claim** while the task waits in your queue. | **Now**: "*Agent* is drafting · *run*", its progress, who holds the task, **Message the agent** and **Open its session**. No form. |
| The same, once the draft is in | **Your task**: the form filled from the draft, and **Ask to revise**. | **Now**: who holds the task. |
| A drafted task whose agent failed or is off | **Your task**: "*Agent* could not finish its draft: you work this task alone." or "*Agent* is off: you work this task alone." and the form. | **Now**: who holds the task. |

- **Answer in Work** opens the question's item on the Work page, in **Needs me** when you hold it, else among its queue's agent questions. See [Answer an agent's question](/keel/business/work/#answer-an-agents-question).
- **A drafted form.** The draft fills the form over the values the process holds, and the outcome it chose is picked. Each field the agent drafted is marked "Drafted by *agent*. Nothing is sent until you submit." until you change it. A draft that sets no field picks its outcome and marks no field. A new draft fills the form afresh. **Submit** sends what you keep, as your completion.
- **Ask to revise** opens **Ask *agent* to revise**: "*Agent* drafts the task again with your note. Nothing is sent until you submit." Type **What should change** and press **Send**. It is for whoever holds the task. When Keel refuses it, such as while the agent is still working, the dialog says why and the page reads the instance again.
- **Message the agent** opens **Message *agent***: "*Agent* reads it while it works on *task*. It is kept in the process history as your note." Type the **Message**, at most 20,000 characters, and press **Send**: Keel says **Sent to *agent*.** An empty message is not sent: "Write a message first." When the agent takes none now, the dialog says "*Agent* takes no message now."

### Goals and deadlines

A task with a `keel:service-level` has a goal and a deadline from the moment it is ready.

- Its work item carries them, so the queue serves it by its deadline, counts it among the items past their deadline, and sends its holder or its queue the goal-near and deadline-near notices, as it does for a step.
- On the instance's page the task shows its service level, such as **Past deadline**, and its goal and deadline.
- A missed goal is only recorded in the history.
- A missed deadline with `escalate-to` puts an escalation in that queue. The page shows **Escalated to** that queue. Members of that queue may complete the task, and the escalation closes when the task does. Without `escalate-to`, a missed deadline is only recorded.
- When the task leaves, completed or withdrawn, its goal and deadline go with it. A task reached again in a loop counts from its new start.

A process's tasks never count in the cases' figures.

## Agents in a process's queues

An agent can take a process's work items as it takes a case's: as a member of a queue, as a delegate, or by **Reassign**. See [Agents in queues and as delegates](/keel/business/agents/#agents-in-queues-and-as-delegates).

- **What an agent takes.** The step of a user task that no agent drafts for, and a question an agent task's agent raised, from any agent but that task's own.
- **What it never takes.** A manual task, whose work is done without any application. A user task its own agent drafts for, whether its step or its question: only a person finishes it. The step an agent task opens for people when its agent is switched off. An escalation.
- **Who is offered.** An agent that a case type or a process of the project names, that is not switched off, and that is no helper.
- **How it works the item.** In a session of its own, started when it takes the item. It completes a step as a person does, with one of the task's outcomes and the values it writes, or answers a question, and the task's checks, maker-checker and authority limits apply to it. A refusal is kept on its run, and the item goes back. An agent that cannot work an item returns it, to the person who delegated it or else to its queue, and says why: the item's pane on the Work page shows it under **Returned**.
- **When the item leaves.** The agent's session stops when its item closes, because someone else completed the task, a timer or a cancel withdrew it, or a supervisor gave the item to another.
- **History.** The agent is the actor of what it completes or answers.

## Running instances

Staff sign in as they do for the business app; another system uses a [service key](/keel/systems/). Keel sets who acted and when on everything they send: a body that names `actor`, `at`, `run` or `sender` is refused.

| To | Call | Who |
|---|---|---|
| Start an instance | `POST /api/projects/{project}/processes` with `{"process": "loan-review", "data": {"amount": "20000.00"}}` | Staff and service keys |
| List the processes an instance may start on, each with the form it starts with | `GET /api/projects/{project}/process-types` | Staff and service keys |
| List instances, newest first | `GET /api/projects/{project}/processes`, with `process`, `status`, `attention=true`, `q` (a part of the number, two to a hundred characters), `cursor` and `limit`. Each row names its process. | Staff and service keys |
| Read an instance | `GET /api/processes/{instance_id}` | Staff and service keys |
| Read it as its page shows it: its tasks with their forms and who holds each, its goals and deadlines, what it waits for, its data | `GET /api/processes/{instance_id}/outline` | Staff and service keys |
| Follow its changes as server-sent events | `GET /api/processes/{instance_id}/live` | Staff |
| Its diagram: the shapes and lines its file lays out, each shape marked `done`, `active`, `incident` or `withdrawn`, or not marked | `GET /api/processes/{instance_id}/diagram` | Staff and service keys |
| The attempts of its calls to systems | `GET /api/processes/{instance_id}/system-calls` | Staff and service keys |
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
| Answer an agent's question | `{"type": "hand.answered", "task": "t5", "answer": "2026", "note": "the new policy"}` | Whoever holds the question's item; while no one holds it, a member of the queue it went to; supervisors always. Never a service key. The `note` is optional, and an answer must be one of the question's choices when it has some. |
| Ask a drafting agent to revise | `{"type": "revision.requested", "task": "t3", "note": "Cite the bureau"}` | Whoever holds the task, or its queue while no one does; supervisors always. Never a service key. |
| Message an agent | `{"type": "agent.messaged", "task": "t5", "text": "Use the May statement."}` | Any member of the staff. Keel adds the sender's name. Never a service key. |
| Retry a task with an incident | `{"type": "task.retried", "task": "t5"}` | Supervisors |

Keel sends the rest itself: a timer firing (`timer.fired`), a call or an agent failing (`task.failed`), an agent raising its hand (`hand.raised`), an agent's draft (`task.drafted`) and a case's close (`case.closed`). A body that names one is `422 invalid-event`, with the reason.

A task's id, such as `t3`, comes from the instance's open tasks. Completing a task that has already finished answers `409 task-closed`. An event sent again with the `Idempotency-Key` it was first sent with is answered with the instance as it stands, and the header `Idempotent-Replayed: true`; it is not applied twice.

### Incidents

A call or an agent task that fails for good leaves its task with an **incident**. The task stays where it is, the instance keeps running, and a supervisor decides. The instance's list finds it with `attention=true`.

- The history records `incident.raised`, with the reason.
- The instance's page says so, and shows it to supervisors first, under **Needs a supervisor**, with **Retry** and, for a call, its attempts. **Waiting for** reads "*task* · its call to *system* failed: a supervisor retries it or cancels the process", and an agent task's **Now** card reads "*Agent* could not finish this task: a supervisor retries it or cancels the process."
- A supervisor sends `task.retried` for the task, or cancels the instance with `process.cancelled`: the instance's page has **Retry** and **Cancel the process…** for both. A call that may have reached its system before it failed asks first. A retried call is made again as a new call. A retried agent task starts the agent in a fresh run, with a new session, or goes to people in its raise-hand queue when its agent is switched off by then.
- A task without an incident answers `task.retried` with `409 not-allowed`.
- The agent that drafts for a person is the exception: its failure is no incident. The person works alone, and the task has no retry.

Timers fire on their own. When a timer cannot fire because what follows it fails, such as a condition that cannot be evaluated on the instance's variables, the timer is kept as **stuck**: it is never fired again, the instance shows why, and the list's `attention=true` finds it. A supervisor then cancels the instance.

The history, `GET /api/processes/{instance_id}/history`, records what happened to the instance's tasks. For agents it holds `task.drafted`, `revision.requested`, `agent.messaged`, `hand.raised`, `hand.answered`, `agent.failed`, `agent.disabled`, `incident.raised` and `task.retried`. A person's `task.completed` on a task an agent drafts also holds `contributions`: who gave each value, the agent or the person.

An instance is `running`, `completed`, `terminated` (by a terminate end event), `failed` (by an error no boundary event caught) or `cancelled`.

A refused call answers with a `code` and a `message`: `404 unknown-instance` for an instance that does not exist or belongs to another project, `422 invalid-event` for a body that is no event, `403 forbidden` for a sender who may not send it, and `409` with Keel's reason for anything the instance cannot take, such as `unknown-outcome`, `check-failed` or `rule-error`. An agent's task adds `hand-raised` (a task with a question waiting takes no completion, draft, revision or message), `no-hand-raised` and `invalid-answer` for an answer, `wrong-actor` for an event only a person or only an agent may send, and `not-allowed` for a message when no agent is working on the task now, and for a revision while its agent still drafts or once its agent failed or is off.

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
| **Start event** | The instance starts here. Only a plain start event: a timer, message or signal start event is refused. Only the start event of an event subprocess takes a timer, a message, a signal or an error. |
| **User task**, **manual task** | Waits for a person to complete it, from a queue. It can have a goal and a deadline. A user task can have an agent that drafts for the person: see [An agent that drafts for a person](#an-agent-that-drafts-for-a-person). |
| **Business rule task** | Evaluates one of the project's [rules](/keel/builder/rules/), a decision table or a scorecard, and writes its results to variables. It never waits. |
| **Service task** that calls a system | Calls another system's API through one of the process's connections, waits for the answer, writes its values to variables and goes on. See [A service task that calls a system](#a-service-task-that-calls-a-system). |
| **Service task** that calls an agent | Starts an agent on the task. The agent completes it under the task's contract, or asks a person. See [A service task that calls an agent](#a-service-task-that-calls-an-agent). |
| **Service task** that starts a case | Starts a case of one of the project's case types, and waits for it to close or goes on at once. See [A service task that starts a case](#a-service-task-that-starts-a-case). |
| **Call activity** | Starts another published process of the project, named by its key, and waits for it to end. See [A call activity](#a-call-activity). |
| **A task that runs several times** | A user, manual, service or business rule task, or a call activity, can run once for each item of a list, or a number of times, all at once or one after another. See [A task that runs for each item](#a-task-that-runs-for-each-item). |
| **Receive task**, **message catch event** | Waits for a message of its name, sent to the instance or, when the wait names a key, sent to the project with that key. See [A message catch, a receive task, a timer](#a-message-catch-a-receive-task-a-timer). |
| **Timer catch event** | Waits for a duration, such as `PT2H` or `P3D`, or until a date. A repeating (cycle) timer is refused. |
| **Signal catch event** | Waits for a signal of its name. A signal reaches every instance of the project that waits for it when it is sent. See [A signal](#a-signal). |
| **Message boundary event** | Fires on a task, a call activity or a subprocess when a message of its name arrives, and withdraws the activity. Only one that interrupts: a message boundary event that does not interrupt is refused, with the way round it. |
| **Signal boundary event** | Fires on a task, a call activity or a subprocess when a signal of its name arrives, and withdraws the activity. Only one that interrupts: a signal boundary event that does not interrupt is refused, with the way round it. |
| **Timer boundary event** | Fires on a task, a call activity or a subprocess after a duration or at a date. An interrupting one withdraws the activity; a non-interrupting one starts its path beside it. |
| **Error boundary event** | Catches an error thrown inside the task or subprocess it sits on, or by the call activity it sits on: the one with the error's code first, else one without a code. |
| **Exclusive gateway** | Takes the first outgoing flow, in the order written, whose condition holds, else its default flow. |
| **Parallel gateway** | Splits into every outgoing flow, or waits for every incoming one. |
| **Inclusive gateway** | Takes every outgoing flow whose condition holds, else its default flow. Where flows meet, it waits for each path still running that can reach it along a flow that has not arrived yet, then goes on. A path that can reach it along a flow that has already arrived does not hold it: when it comes, the gateway goes on again. |
| **Event-based gateway** | Waits for whichever of its timer, message and signal catches comes first. |
| **End event** | Plain, **terminate** (ends everything still open in its process or subprocess), or **error** (throws its error's code). |
| **Signal throw event** | Sends its signal when it completes, and goes on. The instance's own waits for that signal take it at once, and every other running instance of the project that waits for it takes it after the change is saved. See [A signal](#a-signal). |
| **Signal end event** | An end event that sends its signal when it completes, as a signal throw event does, before its process or subprocess ends: an event subprocess of it that does not interrupt still starts. See [A signal](#a-signal). |
| **Embedded subprocess** | Runs its own flow, and may carry boundary events. |
| **Event subprocess** | A subprocess with no flow in or out, that starts while the process or subprocess around it runs, when its start event's timer fires, its message or its signal arrives or an error is thrown inside it. It stops the rest of the process or subprocess, or runs beside it. See [An event subprocess](#an-event-subprocess). |
| **Lanes** | A lane's name is the queue of the tasks in it, read as a queue key: lower case, with each run of other characters as `_`. A lane named "Back Office" is the queue `back_office`. Keel Builder names a lane for the queue you pick in its panel. |

Not run yet, refused when published: data stores and pools that send each other messages. An event subprocess that starts on an escalation, a condition, compensation or a link is refused too.

Refused: script tasks, plain tasks, send tasks, business rule tasks that name a DMN decision instead of a Keel rule, message throw events and message end events (a process sends a signal, or calls a process), throw events that send no signal, the process's own signal start event (a signal reaches the instances that wait for it, and starts none), signal boundary events that do not interrupt, escalations, compensation, transactions, ad hoc subprocesses, complex gateways, conditional and link events, loops on a task (draw the loop with a gateway), data objects and the standard's correlation keys, properties and subscriptions (a message wait names its key with `keel:message key`). Each refusal names the element.

A receive task and a subprocess cannot run for each item, and are refused when they try. "a multi-instance receive task is not supported: every instance would wait for the same message" A multi-instance subprocess is refused with the way round it: "draw its steps as a process of their own and call it from a multi-instance call activity", each called process being an instance of its own with its own page, number and history.

Conditions are written in CEL over the process's variables, as a case type's are, for example `amount <= 250000.0`. An exclusive gateway stops at the first condition that holds; an inclusive gateway evaluates every one. A condition that reads a variable with no value, such as one only a branch not taken writes, refuses what reached the gateway: a completion answers `409 evaluation-error`, a start is refused, and a timer is kept as stuck. So give such a variable a value on every path.

An exclusive or an inclusive gateway with more than one flow leaving it needs a condition on every flow but its default, and one with a condition on any flow needs a default flow. A condition on the default flow is never evaluated, and Keel warns of it.

A parallel or an inclusive gateway where flows meet takes one flow from each element that leads to it, so two flows from one element into it are refused.

## Keel's settings in the file

Each setting sits in the `extensionElements` of its BPMN element. An element or attribute Keel does not know, or one where it has no meaning, is a problem when the file is published: nothing is ignored silently.

Keel Builder's panel sets the process's settings and variables, a user or manual task's settings, a user task's drafting agent, a service task's call (a call to a system, a call to an agent or the start of a case), a call activity's process, what it passes and what it receives, a business rule task's rule, how a task runs for each item, a lane's queue (its name), a sequence flow's condition, an exclusive or an inclusive gateway's default flow, a timer, a message, a signal and an error, and an event subprocess with what starts it and whether it interrupts: see [Changing the diagram](/keel/builder/processes/#changing-the-diagram). A change made in the panel keeps whatever else the file holds.

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

When the case closes, a waiting task completes: its `keel:result` variables and its `resolution-variable` take the case's values. Otherwise the task throws a BPMN error, which an error boundary event on the task, an error event subprocess around it, or an error boundary event on a subprocess around it, catches by its code; uncaught, it fails the instance:

| Error | When |
|---|---|
| `case-not-started` | Keel could not start the case. |
| `case-failed` | A step's failure closed the case. |
| `case-values` | The case closed with a value its variables cannot hold. Nothing is written. |

### A call activity

```xml
<bpmn:callActivity id="check" name="Check credit" calledElement="credit-check">
  <bpmn:extensionElements>
    <keel:called>
      <keel:pass variable="amount" to="loan_amount"/>
      <keel:receive variable="band" from="rating"/>
    </keel:called>
  </bpmn:extensionElements>
</bpmn:callActivity>
```

| Setting | What it does |
|---|---|
| `calledElement` | The process the call activity starts, by its key: the name of its file under `processes/`, not the process id inside the file. Required. A vendor's `calledElementBinding` is a warning and never read. |
| `keel:pass` | A variable of this process (`variable`) that fills a variable of the called process (`to`). A variable with no value is not passed. Each called variable once. |
| `keel:receive` | A variable of this process (`variable`) that takes a variable of the called process (`from`) when it ends. Each variable once. |

Nothing is passed or received that is not named: the two processes do not share variables by name.

Each call starts the newest published version of the called process, and that instance runs on it until it is moved to a newer one, whatever is published after. It is an instance of its own, with its own number, page, tasks and history: see [Running instances](#running-instances). The calling instance waits at the call activity until it ends; no one holds a lock on either meanwhile. A called process that requires a variable no `keel:pass` fills cannot start, and a `keel:pass` of a variable with no value leaves it unfilled.

When the called process ends, the call activity completes: each `keel:receive` variable takes the called process's variable, when it holds one, and a terminate end event in the called process ends only that process. Otherwise the call activity throws a BPMN error, which an error boundary event on it, an error event subprocess around it, or an error boundary event on a subprocess around it, catches by its code; uncaught, it fails the instance:

| Error | When |
|---|---|
| `process-not-started` | Keel could not start the process: it is not published, the values passed do not fit it, the chain of starts is too deep, its first steps refused, or Keel gave up starting it. |
| `process-cancelled` | The called process was cancelled. |
| The called process's own error code | The called process failed on an error nothing in it caught, such as an error end event. |
| `process-values` | The called process ended with a value the receiving variables cannot hold. Nothing is written. |

When the calling instance leaves the call activity first, by an interrupting boundary event, a supervisor's cancel or an error caught elsewhere, Keel cancels the called process, as the system `keel`. A boundary event that does not interrupt leaves it running. A called process that waits on an incident keeps the caller waiting until a supervisor retries it or cancels it.

A process cannot call itself, or call a process that calls it back: the publish refuses a cycle of calls, naming each call activity of the published processes that lies on it.

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

- `keel:message` on a message catch event, a receive task or a message boundary event lists, with `keel:write`, the variables the message may write. A message that holds anything else is refused.
- `keel:message key="<variable>"` makes the wait addressable by a business key: see [A message addressed by a key](#a-message-addressed-by-a-key).
- `keel:timer business="true"` on a timer makes it count business time on the process's calendar.
- A signal has no Keel setting: see [A signal](#a-signal).

### A message addressed by a key

A system outside Keel knows a business key, such as a claim number, not Keel's instance id. A message wait can name the process variable that holds it with `key`, and a message sent to the project with that key reaches the running instances whose wait holds it.

```xml
<bpmn:intermediateCatchEvent id="docs" name="Documents in">
  <bpmn:extensionElements>
    <keel:message key="claim_number">
      <keel:write variable="docs_note"/>
    </keel:message>
  </bpmn:extensionElements>
  <bpmn:messageEventDefinition messageRef="documents_arrived"/>
</bpmn:intermediateCatchEvent>
```

- **Which wait.** A message catch event, a receive task, a message boundary event, the start event of a message event subprocess, and a branch of an event-based gateway take a `key`.
- **Which variable.** A declared string, whole-number (`int`) or choice variable. Its key is its value as text: a string or a choice as it is, a whole number in decimal digits. The sender sends the key as a string, `"2041"` for the whole number 2041, and the comparison is exact, case and all.
- **When it is read.** After every transition, not only when the wait opens: a task that writes the variable while the wait is open moves the wait to the new value. A wait whose variable holds no value, only spaces, or more than 1,000 characters (the most a send carries) has no key, and only a message sent to its instance reaches it.
- **Without a `key`**, a wait is reached only by a message sent to its instance, as before. A message sent to an instance with a `key` reaches only the waits whose key holds it; without one, every wait of its name, keyed or not.
- **Personal data.** A variable marked as personal data may be a key. Its value is kept with the wait while the wait is open, in the event that took the message, and in the `subscription.set` command of each transition that opened or moved the wait, which the instance's history returns; **Waiting for** shows it as the sender sends it (2041, not 2,041; a choice's value, not its label), and the audit and the history's sentences never state it.

A message boundary event interrupts the task, call activity or subprocess it sits on, and writes what its message carries, as a message catch event does. A receive task cannot carry a message boundary event for its own message: the task takes the message and goes on, and the boundary event is withdrawn. A task that runs for each item, or a subprocess, carries one on the whole activity, and the message withdraws every instance of it, or everything in the subprocess.

### A signal

A message is for one instance, or for the instances a business key names. A **signal** is for every instance that waits for it: a broadcast, such as "the rates changed", to every open loan. A signal has a name and nothing else: it carries no values, has no key and has no Keel setting in the file.

```xml
<bpmn:signal id="rates_changed" name="rates changed"/>
…
<bpmn:intermediateCatchEvent id="repriced" name="Rates">
  <bpmn:signalEventDefinition signalRef="rates_changed"/>
</bpmn:intermediateCatchEvent>
<bpmn:intermediateThrowEvent id="tell" name="Rates published">
  <bpmn:signalEventDefinition signalRef="rates_changed"/>
</bpmn:intermediateThrowEvent>
```

- **Which wait.** A signal catch event, a signal boundary event, a branch of an event-based gateway and the start event of an event subprocess, interrupting or not, wait for a signal. A signal boundary event interrupts the task, call activity or subprocess it sits on, as a message boundary event does: on a task that runs for each item it withdraws every instance, and on a subprocess everything in it.
- **Which send.** A signal throw event and a signal end event send their signal when they complete. A throw event goes on at once. A signal end event sends its signal before its process or subprocess ends, so an event subprocess of that scope that does not interrupt still starts.
- **Who takes it.** The instance's own waits for the signal take it at once, in the same change, so an event subprocess of the instance that waits for it starts at once. Every other running instance of the project that waits for it takes it after the sender's change is saved, each in a change of its own. An instance with several waits for the signal takes it at each of them, and an event subprocess among them that interrupts starts and stops the rest, as it does for a message.
- **Which waits.** A signal reaches the waits open when it is sent. An instance that starts waiting afterwards is not reached. An instance that moved on, because it ended or its wait is done, skips it. An instance that cannot take it for any other reason is logged for the operators, and the other instances are not affected.
- **From outside.** A supervisor or a service key sends a signal to the project: see [Running instances](#running-instances). The history shows who sent it, or the instance it came from.
- **In order.** An instance takes the signals sent to it in the order they were sent. If one cannot be applied just now, the instance's later signals wait for it.
- **Round in a circle.** A signal an instance throws as it takes a signal is sent on with the signals that led to it, and one that is already among them is not sent again: two processes that answer each other's signal stop at the signal that comes round, and the operators' log says so. A task whose own signal boundary event catches a signal that its flow throws is interrupted at once, before the flow goes on.
- **No cap.** A signal reaches every instance that waits for it, however many. A signal and a message of the same name are two waits, and a signal has no payload.

### A task that runs for each item

A user task, a manual task, a service task (a call to a system, a call to an agent or the start of a case), a business rule task and a call activity can run more than once where the flow reaches them: once for each item of a list, or a number of times. BPMN calls this a multi-instance activity. Each run is an **instance** of the task, numbered from 1. Do not confuse it with an instance of the process.

```xml
<bpmn:userTask id="vote" name="Approve">
  <bpmn:extensionElements>
    <keel:task outcome-variable="vote">…</keel:task>
  </bpmn:extensionElements>
  <bpmn:multiInstanceLoopCharacteristics>
    <bpmn:extensionElements>
      <keel:instances collection="members" item="member" results="votes" result="vote" distinct="true"/>
    </bpmn:extensionElements>
    <bpmn:completionCondition xsi:type="bpmn:tFormalExpression">votes.filter(v, v == "approve").size() &gt;= 2</bpmn:completionCondition>
  </bpmn:multiInstanceLoopCharacteristics>
</bpmn:userTask>
```

| Setting | What it does |
|---|---|
| `isSequential` | On the loop. `true` runs the instances one after another, each opening when the one before completes. Absent or `false` runs them all at once. |
| `loopCardinality` | How many instances, as a number of times: a whole number from 1 to 100, or a CEL expression of the process's variables that gives an `int`. Give this or a `collection`, never both. |
| `completionCondition` | A CEL condition, over the process's variables but the item and the result, that ends the task before every instance has: see [How it ends](#how-it-ends). Left empty, there is none. |
| `collection` | On `keel:instances`, in the loop's own `extensionElements`. A `list` variable: one instance for each of its items, in the list's order. |
| `item` | The variable that holds the instance's item while it runs. With a `loopCardinality` it is an `int` variable that holds the instance's number, from 1. |
| `results`, `result` | `results` is a `list` variable that takes what the instances give, when the task ends. `result` is the variable each instance writes. They come together. |
| `distinct` | `true` makes each instance take a different person: see [People](#people-and-agents-at-an-instance). |

Every attribute of `keel:instances` is optional. A variable named in it is declared by the process, and the collection, the item, the results and the result are four different variables. The item and the result cannot be `required`: each instance gives them its own value. Publishing refuses a variable of a shape the list does not take: the item must have the shape of the list's items and take every choice they may hold, and the result must have the shape of the `results` list's items, with every choice it may hold taken by them and every part they require required of it too, at any depth. Otherwise the last instance's completion would be refused for another's result.

- **What an instance sees and gives.** Inside an instance, its checks, its authority amount, its form's values, its agent's reads, its call's templates, a case's fields, a call activity's passes and a rule's inputs read the `item` variable as the instance's item, and the `result` variable holds nothing until the instance writes it. What an instance writes to its `result` variable goes into the `results` list, never into the process's variables. Neither the item nor the result variable is ever written to the process's variables: after the task, the process holds of them only what it held before. What else an instance writes is the process's, and the last writer wins, as for parallel branches. The task itself must write its `result` variable, or publishing refuses it: through `keel:write`, its outcome variable, a call's outputs, a case's results or resolution variable, a call activity's receives or a rule's assignments. It must not write the `item` variable, nor the `results` list.
- **The results.** When the task ends, `results` holds the result of each instance that completed and wrote one, in the order of the items, whichever instance completed first. It is shorter than the list when an instance was withdrawn or gave nothing, since a list holds no empty place. When each result must be read beside its item, make the result an object that names the item. The list is written once, at the end.
- **The count.** The list is read once, when the task is reached. A later change to the variable changes no instance. An empty list, or a `loopCardinality` that gives 0, completes the task at once with an empty `results` list, and the condition is never read. A list variable with no value refuses what reached the task, as a gateway whose condition reads an unset variable does: a completion answers `409 evaluation-error` with "*task*: *list* has no value", a start is refused, and a timer is kept as stuck.
- **At most 100.** Publishing refuses a `loopCardinality` written as a number under 1 or over 100. A list of more than 100 items, or a `loopCardinality` that gives more, refuses what reached the task, `409 too-many-instances`: "*task*: *list* holds 101 items, over 100", or "*task*: loopCardinality gave 101, over 100". The business app says "This would run a step more than 100 times. Ask your supervisor." A `loopCardinality` that gives a negative number or no whole number is `409 evaluation-error`.
- **In a loop.** A task reached again starts afresh: it reads its list again, numbers its instances from 1 and never reads the first round's results. An instance of the first round completed late is refused `task-closed`.
- **Where flows meet.** A parallel or an inclusive gateway after a task that runs for each item waits for the whole task, and goes on once, after its last instance.
- **A call activity.** Each instance starts a process of its own, with its own number, page, tasks and history: see [A call activity](#a-call-activity). A task that ends early cancels the processes of its open instances, as a call activity does when the instance leaves it first.
- **A rule.** A business rule task never waits: all its instances evaluate their rule in the step that reaches the task, one after another in the order of the items.

#### How it ends

- **Every instance completed.** The results are written, the history says "All 3 instances of *task* completed", and the task completes.
- **The completion condition.** `completionCondition` is read each time an instance completes. It reads the process's variables, the `results` list holding the results so far, in the order of the items, and three counts: `numberOfInstances`, the number of instances; `numberOfCompletedInstances`; and `numberOfActiveInstances`, the instances started and not yet completed. When it holds, the instances still open are withdrawn: a person's items close, an agent's session is cancelled, a called process an instance started is cancelled, a case it started is sent its cancel event (or left running when the task says `keep-running`), and a task that runs one after another opens no more. The task then completes, and the history says "*Task* ended early: 2 of 3 instances completed". A condition that cannot be evaluated, such as one that reads a place the list does not have, refuses the completion that reads it: `409 evaluation-error`.
- **An error.** A BPMN error one instance throws, such as a call that fails with an error code, a called process that ends in an error or a case that fails, leaves the whole task. An error boundary event on the task catches it, and every instance is withdrawn, the one that threw it too. With none, an error event subprocess around the task catches it; uncaught, the process fails at the task.
- **An incident.** A call or an agent that fails for good leaves an incident on that instance only. The others go on, the task waits, and a supervisor retries that instance or cancels the process: see [Incidents](#incidents).
- **A timer boundary event on the task** is on all its instances. An interrupting one withdraws every instance; one that does not interrupt leaves them running.
- **A cancel of the process**, a terminate end event elsewhere and an interrupted subprocess around the task withdraw every instance with the task.

#### People and agents at an instance

- **One work item for each instance.** A user or manual task instance is a work item of its own, in the task's queue or for its one user. All at once, they open together; one after another, each opens when the one before completes. Who may complete one, its goal and deadline, its checks, maker-checker, authority limit, outcomes and drafting agent are each the instance's, so a goal and a deadline count from the moment *that* instance opens.
- **Its words.** Where Keel names an instance's work, it reads "*task* · *n* of *count*", such as "Approve · 2 of 3": on the Work page, on the instance's page, in the mail and notices that tell you of the work, and in the history. With an `item` variable, the instance's page shows the item under the name.
- **"Each person completes one instance at most".** With `distinct="true"`, someone who completed one instance of the task cannot complete another of it: the completion is refused `409 maker-checker`, "*person* already completed another instance of *task*", which the business app words "Someone else must finish this step." Absence routing never hands an instance to a substitute who completed another of the task. A task reached again in a loop starts with nobody. Without `distinct`, one person completes as many instances as they hold. Only a user or a manual task takes it: an agent, a call or a rule completes every instance as one actor, and publishing refuses it there.
- **An agent task for each item** starts one agent run for each item, each in a session of its own, so a task of 100 items is up to 100 runs at once, and costs as many. Pick one after another when the cost or the agent's load matters. A task that runs one after another starts one run at a time. A user task's drafting agent drafts each instance.

The panel in Keel Builder sets all of this: see [Instances](/keel/builder/processes/#instances). A file from another modeller can carry the loop with Camunda's `camunda:collection` and `camunda:elementVariable`. Keel reads neither: they are a warning, "camunda:collection, camunda:elementVariable are ignored: Keel runs only BPMN and its keel: extension", and the task then has no count until `loopCardinality` or `collection` gives one. An expression such as `${members}` is not CEL.

### An event subprocess

An event subprocess is a subprocess that no flow enters or leaves. It sits in a process or a subprocess, and its start event says what starts it. While the process or subprocess around it runs, it waits; when a timer fires, a message or a signal arrives or an error is thrown, it runs.

```xml
<bpmn:subProcess id="late" name="Escalate" triggeredByEvent="true">
  <bpmn:startEvent id="late_start" name="Five days" isInterrupting="false">
    <bpmn:extensionElements>
      <keel:timer business="true"/>
    </bpmn:extensionElements>
    <bpmn:timerEventDefinition>
      <bpmn:timeDuration xsi:type="bpmn:tFormalExpression">P5D</bpmn:timeDuration>
    </bpmn:timerEventDefinition>
  </bpmn:startEvent>
  …
</bpmn:subProcess>
```

| Setting | What it does |
|---|---|
| `triggeredByEvent="true"` | On the `bpmn:subProcess`: it is an event subprocess. |
| The start event's definition | One of `timerEventDefinition`, `messageEventDefinition`, `signalEventDefinition` and `errorEventDefinition`. A start event with none, or with another, is refused. |
| `isInterrupting` | On the start event. `false` runs the event subprocess beside the rest; absent or `true` stops the rest first. An error event subprocess always interrupts, and `false` on it is refused. Any other value is refused. |
| `keel:timer`, `keel:message` | On the start event, as on a timer or a message catch event: `business="true"` counts business time on the process's calendar, and `keel:write` lists the variables the message may write. A signal start event has no Keel setting. |

**What starts it.**

- **A timer**: a duration, which counts from the start of the process or subprocess around it, or a date. A repeating (cycle) timer is refused. A date already past when the process or subprocess starts starts the event subprocess at once.
- **A message**: a message of its name, as a message catch event takes it, sent to the instance through Keel's API, or to the project with the start event's `key`. Messages are not matched by their content.
- **A signal**: a signal of its name, as a signal catch event takes it, sent to the project or thrown by an instance of it: see [A signal](#a-signal).
- **An error**: an error thrown inside the process or subprocess around it, caught by its code, or any error when the start event names no error. An error end event, a call activity whose process could not start, was cancelled or ended in an error, and a start-a-case task whose case could not start or failed each throw one. A call to a system or an agent that fails for good throws none: it leaves an incident.

**Where it may sit.** In the process, in an embedded subprocess, in another event subprocess, and in a process that another calls. It has no boundary event, and two of one process or subprocess cannot start on the same error code, nor on the same message, nor on the same signal. Two that start on a timer are fine, and so is one that starts on a message that a task beside it also waits for: both take it. One that does not interrupt runs beside the task, and an interrupting one withdraws the task first. The message may then write only the variables both list.

**When it waits.** An event subprocess waits from the start of the process or subprocess around it. A subprocess that is reached again starts afresh, so its event subprocess waits again, and its duration counts again from then. It stops waiting when the process or subprocess around it has ended its own flow, when an interrupting event subprocess of it starts, and when the process or subprocess is withdrawn. An event subprocess that never starts leaves nothing in the history.

**An interrupting event subprocess** stops everything else the process or subprocess around it is doing, as an interrupting boundary event stops its task: people's items close, an agent's session is cancelled, a task's instances are withdrawn, a called process is cancelled, a case is sent its cancel event (or left running when the task says `keep-running`), and so are the runs of its other event subprocesses. No other event subprocess of it can start after that. When the event subprocess ends, the process or subprocess ends with it: the process completes, and a subprocess goes on by its outgoing flow. A terminate end event inside it ends only the event subprocess, and the process or subprocess ends the same way. An error end event inside it throws outward.

**An event subprocess that does not interrupt** runs beside the rest:

- A message or a signal starts a run each time it arrives, so several runs of one event subprocess can be open at once. A timer starts it once.
- At most 100 runs of one event subprocess are open at once. The message that would start the 101st is refused `409 too-many-instances`: "*element*: 100 runs of it are open, the most an event subprocess runs at once". A signal that would start the 101st run is taken at none of the instance's waits: one sent to the project, or by another instance, is logged for the operators, as one that cannot take a signal is, and one the instance sends itself refuses what reached the throw event, `409 too-many-instances`, with the same words.
- The process or subprocess around it waits for its runs. Once its own flow has ended, no new run starts, and a message for the event subprocess is refused `409 unknown-message`: "the instance is not waiting for the message *name*", unless another task waits for it. A signal for it is passed over, as for any instance that moved on. It ends when its last run does, and only once.
- A run reads and writes the process's variables, and the last writer wins, as for parallel branches. A message writes its values once, when it arrives, so two runs open at once both read the values of the second message.

**Errors.** An error goes to the nearest handler: the error boundary event on the task that threw it, then an error event subprocess of the process or subprocess the task is in, then the error boundary event on the subprocess, then the event subprocess of the one around it, and so on outward. An error thrown inside an event subprocess goes to the process or subprocess around it, never to the event subprocess that threw it. An error thrown after the flow around it has ended passes its error event subprocess. Uncaught, it fails the process at the task that threw it. An incident, a call or an agent that fails for good, is no error and starts nothing.

An event subprocess that can never start, such as one on an error that nothing in its scope throws, or on a message or a signal nobody sends, is not checked.

Keel Builder sets all of it: see [Event subprocesses](/keel/builder/processes/#event-subprocesses). The business app draws an event subprocess dotted, and says **Waiting to start** while it waits: see [The diagram](/keel/business/open-process/#the-diagram).

## Cases and processes that start each other

A case's [process node](/keel/builder/flow-nodes/#processes) starts a process, and a process's [start-a-case task](#a-service-task-that-starts-a-case) starts a case. Keel starts the other side itself, a moment after the case or the instance reached the node or the task, and keeps a link between the two.

- A side that waits takes the other's end: a case leaves its process node by Ended or Failed, and a process's task completes or throws its error.
- When the waiting side moves on first, Keel withdraws the other: it cancels a process whose case no longer waits at its node, and sends a case its task's `cancel-event`, unless the task says `keep-running`.
- When Keel cannot start the other side, such as a retired case type or values that no longer fit, the waiting side takes its error path.
- A call activity starts a process the same way, and waits for it to end; see [A call activity](#a-call-activity). A call counts in the chain.
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

A start or a call is checked when the case type or the process that holds it is published, against what it starts or calls as the publish leaves it. It is checked again when what it starts is published again, at each stored version that starts or calls it: the current version of each case type or process the publish leaves alone, and each version that cases or instances still run on. Such a problem is at `<case type> v<n>: <node>` or `<process> v<n>: <task>`, in the file published again. A retired case type is checked against the processes that start it like any other, and its republish is never refused `retired-case-type`. A problem at a version cases or instances still run on stays until nothing runs on it, or the file fits it again; a problem at a current version does not end by itself.

| Problem | Where | What it says |
|---|---|---|
| `unknown-case-type` | The process's file, at the task | "*task* starts *case type*, a case type the project does not have" |
| `retired-case-type` | The process's file, at the task | "*task* starts *case type*, which is retired: no new case can start on it" |
| `called-element` | The process's file, at the call activity | "*element* needs calledElement: the key of the process it calls" |
| `unknown-process` | The case type's file, at the node; or the process's file, at the call activity | "*node* starts *process*, a process the project does not have"; "*element* calls *process*, a process the project does not have" |
| `call-input` | The process's file, at the call activity, or at `<process> v<n>: <call activity>` in the called process's file | "*process* requires *name*, which no keel:pass fills", "keel:pass names *to*, which *process* does not declare", "*to*, a *type*, is filled from *variable*, a *type* of another shape", "*variable* may hold *choices*, which *to* does not take" |
| `call-output` | The same | "*variable* receives *from*, which *process* does not declare", "*variable*, a *type*, receives *from*, a *type* of another shape", "*from* may hold *choices*, which *variable* does not take" |
| `call-cycle` | The process's file, at each call activity of it that lies on a cycle of calls | "*element* calls *process*, the process it is in: a process cannot wait on itself", "*element* calls *called*, and the calls of *a, b, c* lead back round: a process cannot wait on itself" |
| `process-input` | The case type's file, or the process's file at `<case type> v<n>: <node>` | "*process* requires *variable*, which no input fills", "inputs names *variable*, which *process* does not declare", "*variable*, a *type*, is filled from *field*, a *type* of another shape", "*field* may hold *choices*, which *variable* does not take" |
| `process-output` | The same | "*field* receives *variable*, which *process* does not declare", "*field*, a *type*, receives *variable*, a *type* of another shape", "*variable* may hold *choices*, which *field* does not take" |
| `case-input` | The process's file, or the case type's file at `<process> v<n>: <task>` | "*case type* requires *field*, which no keel:field fills", "keel:field names *field*, which *case type* does not declare", "*field*, a *type*, is filled from *variable*, a *type* of another shape", "*variable* may hold *choices*, which *field* does not take" |
| `case-output` | The same | "*variable* receives *field*, which *case type* does not declare", "*variable*, a *type*, receives *field*, a *type* of another shape", "*field* may hold *choices*, which *variable* does not take"; and in the process's own file, "the resolution variable *variable* must be a string or a choice variable" |
| `case-cancel` | The same | "*case type* has no event *event*", "*event* of *case type* does not interrupt: it would not withdraw the case", "*node* of *case type* waits for *event*: it would take the event as the one it waits for"; and in the process's own file, "*task* waits on its case: name cancel-event, the case event that withdraws it when the process leaves the task, or keep-running="true"" and "*task* names both cancel-event and keep-running: it does one or the other" |
| `broken-definition` | `<key> v<n>` | "*key* v*n* is stored but no longer loads: …" |
| `checks-stale` | `<case type> v<n>` or `<process> v<n>` | "cases started on it while the publish was checked; publish again", or "instances started on it while the publish was checked; publish again" |

### Checking a task that runs for each item

A task's loop is checked when the process is published, against the process's own variables. Each problem is in the process's file, at the task. A call activity that runs for each item is also checked against the process it calls, and a start-a-case task against its case type, as one that runs once is.

| Problem | What it says |
|---|---|
| `unsupported` | "a multi-instance receive task is not supported: every instance would wait for the same message"; "a multi-instance subprocess is not supported: draw its steps as a process of their own and call it from a multi-instance call activity"; "loopDataInputRef is not supported: name the collection, its item and the results in keel:instances", and the same for `loopDataOutputRef`, `inputDataItem` and `outputDataItem`; "a multi-instance behavior other than All is not supported: it throws events, which a process does not" |
| `extension` | "keel:instances has no attribute *name*", "keel:instances cannot hold *name*", "keel:*name* has no meaning on a multiInstanceLoopCharacteristics", "keel:instances appears twice on one multiInstanceLoopCharacteristics", "keel:instances *attribute* is blank: name a variable or leave it out", "keel:instances distinct must be true or false, not '*value*'" |
| `instances` | "isSequential must be true or false, not '*value*'"; "*task* needs a loopCardinality or a keel:instances collection: how many instances it runs"; "*task* has both a loopCardinality and a keel:instances collection: give one" |
| `instances` | "the collection *list* is a *type*, not a list", "the result list *list* is a *type*, not a list"; "*item*, a *type*, takes each item of *list*, a *type* of another shape"; "the items of *list* may hold *choices*, which *item* does not take"; "*item* is a *type*: with a loopCardinality each instance's item is its number, an int"; "each item of *results*, a *type*, takes *result*, a *type* of another shape"; "*result* may hold *choices*, which *results* does not take", "*result* may leave *part* empty, which *results* requires" |
| `instances` | "keel:instances names the result list *list* but no result", "keel:instances names the result *variable* but no result list"; "*variable* is named twice in keel:instances: the collection, the item, the result list and the result are four variables"; "*variable* cannot be required: each instance gives it its own value" |
| `instances` | "*task* writes *item*, the item each instance is given", "*task* writes *results*, which its instances' results fill when it ends", "*task* does not write *result*, the result each instance gives"; "distinct needs a user or a manual task: an agent, a call or a rule completes every instance", "distinct needs a queue: a task given to one user could be completed once at most" |
| `instances` | "loopCardinality *n* runs no instance: give a whole number from 1 to 100, or an expression", "loopCardinality *n* is over 100, the most instances an activity runs", "loopCardinality *expression* is *TYPE*, not INT" |
| `undeclared-variable` | "the collection names *variable*, which is not a declared variable", and the same for "the item", "the result list" and "the result" |
| `expression`, `not-boolean` | The `loopCardinality` or the `completionCondition` does not compile, "*condition*: *why*", or a condition is not a yes or no, "*condition* is *TYPE*, not BOOL". The condition is checked with `numberOfInstances`, `numberOfCompletedInstances` and `numberOfActiveInstances` declared. Neither the `loopCardinality` nor the `completionCondition` can read the `item` or the `result` variable: outside an instance they hold no value, so the check reports them as undeclared. |

A boundary event on a task that runs for each item is checked as on one that runs once: an error boundary event on a user task still never fires.

### Checking an event subprocess

An event subprocess is checked when the process is published. Each problem is in the process's file.

| Problem | Where | What it says |
|---|---|---|
| `unsupported` | The start event's event definition, else the start event | "escalation event subprocesses are not supported: an event subprocess starts on a timer, a message, a signal or an error", and the same for conditional, compensation, link, cancel and terminate |
| `event-subprocess` | The start event | "isInterrupting must be true or false, not '*value*'"; "*start* starts the event subprocess *element*: it needs a timer, a message, a signal or an error"; "an error event subprocess always interrupts" |
| `event-subprocess` | The event subprocess | "*element* is an event subprocess: no flow enters or leaves it, its start event starts it"; "another event subprocess of this scope catches the same errors"; "another event subprocess of this scope waits for the message *name*"; "another event subprocess of this scope waits for the signal *name*" |
| `boundary` | The boundary event | "a boundary event cannot be attached to an event subprocess" |
| `start-events`, `end-events` | The event subprocess | "*element* needs exactly one start event, and has *n*", "*element* needs an end event" |
| `extension` | The start event | "keel:timer has no meaning on a startEvent", and the same for any Keel element a start event's definition has no use for; "keel:message key is blank: name a variable or leave it out" |
| `timer`, `business-timer`, `message-name`, `signal-name`, `undeclared-variable`, `message-key`, `unknown-reference` | The start event | The problems of a timer, a message, a signal and an error, as on a catch event or a boundary event |

The process's own start event with a timer, a message or a signal stays refused: "timer start events are not supported", "message start events are not supported", "signal start events are not supported: a signal reaches the instances that wait for it, and starts none". An event subprocess has no `no-outgoing` and no `unreachable` problem: its start event reaches it.

### Checking a message key and a message boundary event

A message wait's key and a message boundary event are checked when the process is published. Each problem is in the process's file, at the wait or the boundary event.

| Problem | What it says |
|---|---|
| `extension` | "keel:message key is blank: name a variable or leave it out" |
| `undeclared-variable` | "a message key names *variable*, which is not a declared variable" |
| `message-key` | "the key *variable* is a *type* variable: a key is a string, a whole number or a choice" |
| `boundary` | "a message boundary event that does not interrupt is not supported yet: put the task in a subprocess with a message event subprocess that does not interrupt"; "cancelActivity must be true or false, not '*value*'"; "another message boundary event of this activity waits for the message *name*"; "the receive task *task* waits for the message *name* too: the task takes it and goes on, and this boundary event is withdrawn" |
| `message-name`, `unknown-reference` | As for a message catch event: "*element* needs a bpmn:message", "the message *id* is not a bpmn:message of the file", "the message *id* has no name" |
| `unsupported` | "correlation is not supported: a message wait names its key with keel:message key", at a `correlationKey`, `correlationProperty` or `correlationSubscription` |

A key that no sender can know, and a message nobody sends, are not checked.

### Checking a signal

A signal wait or send is checked when the process is published. Each problem is in the process's file, at the element.

| Problem | What it says |
|---|---|
| `signal-name` | "*element* needs a bpmn:signal", when a signal event names none; "the signal *ref* has no name", for a name that is blank; "the signal *ref* has a name of more than 200 characters" |
| `unknown-reference` | "the signal *ref* is not a bpmn:signal of the file" |
| `boundary` | "a signal boundary event that does not interrupt is not supported yet: put the task in a subprocess with a signal event subprocess that does not interrupt"; "cancelActivity must be true or false, not '*value*'"; "another signal boundary event of this activity waits for the signal *name*" |
| `event-subprocess` | "another event subprocess of this scope waits for the signal *name*" |
| `event-gateway` | "two branches of *gateway* wait for the signal *name*"; "*gateway* leads to *target*, which is not a timer, a message, a signal or a receive task" |
| `extension` | "keel:*name* has no meaning on *the element*", at a signal catch event, a throw event, a signal end event, a signal boundary event or a signal start event: a signal has no Keel settings |
| `unsupported` | "an intermediate catch event needs a timer, a message or a signal"; "a throw event needs a signal: a process sends nothing else"; "signal start events are not supported: a signal reaches the instances that wait for it, and starts none", at the process's own start event; "message throw events are not supported: a process sends a signal, or calls a process"; "message end events are not supported: a process sends a signal, or calls a process" |

A signal nobody sends, and a wait that opens only after its signal was sent, are not checked.

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
- At a version cases or instances still run on: move its open cases to a newer version of the case type, or move its instances to the process's current version ([Moving instances to a newer version](#moving-instances-to-a-newer-version)), or wait for them to close, or for the instances to end or be cancelled.
- At a current version: publish a new version of that case type or process in the same draft. The new version is then checked instead.

A problem that Keel cannot run, such as a script task, refuses the publish and names the element. A vendor extension, such as Camunda's, Flowable's or SpiffWorkflow's own properties, is a **warning**: Keel ignores it and never runs it, and the publish goes on. So is a cycle of tasks that no path leaves for an end event: an instance that reaches it never ends. The review page lists warnings under **Warnings**, and **Publish** stays on.

A running instance runs on the version it started on until it is moved to the process's current version: see [Moving instances to a newer version](#moving-instances-to-a-newer-version).

Builders read the published processes with:

| To | Call |
|---|---|
| List the processes, with each version's running instances | `GET /api/build/projects/{project}/processes` |
| Download a version's file | `GET /api/build/projects/{project}/processes/{key}/versions/{version}` |
| Read the file in a draft | `GET /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}` |
| Read the variables a version declares | `GET /api/build/projects/{project}/processes/{key}/versions/{version}/variables` |
| Read the variables the file in a draft declares, before its checks pass | `GET /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}/variables` |
| Put the file back as the draft started with it | `POST /api/build/projects/{project}/drafts/{draft_id}/files/processes/{key}/revert` |
| Check what moving the running instances of a version to the current one would do | `GET /api/build/projects/{project}/processes/{key}/moves/forecast?from_version=2` |
| Start that move | `POST /api/build/projects/{project}/processes/{key}/moves` with `{"from_version": 2}` |
| List the process's moves, newest first | `GET /api/build/projects/{project}/processes/{key}/moves` |
| Read a move | `GET /api/build/projects/{project}/processes/{key}/moves/{move_id}` |
| List the instances a move left on their version | `GET /api/build/projects/{project}/processes/{key}/moves/{move_id}/stayed`, with `limit` (1 to 100, 50 unless given) and `offset` |
| Read the process's figures: see [Figures](#the-figures-through-the-api) | `GET /api/build/projects/{project}/processes/{key}/figures`, with `days` and `version` |

Any member of the project reads the moves; an editor or an owner starts one. The forecast checks the oldest 1,000 running instances of `from_version` as they stand, and answers how many run, how many it checked, how many of those could move, and the reasons the others could not, the one most instances meet first:

```json
{"process": "loan-review", "from_version": 2, "to_version": 3, "running": 12, "checked": 12, "moving": 10, "staying": 2,
 "reasons": [{"code": "missing-element", "element": "pay", "message": "Pay is open, and version 3 has no element pay", "instances": 2}]}
```

Starting the move answers `201` with its progress, and the sweeper moves the instances after the answer, one in each transaction:

```json
{"id": 5, "process": "loan-review", "from_version": 2, "to_version": 3, "status": "running", "total": 12,
 "moved": 0, "stayed": 0, "remaining": 12, "started_by": "…", "started_at": "…", "finished_at": null}
```

`total` counts the instances running on `from_version` when the move started. `moved` and `stayed` count the instances handled so far, `remaining` is what is left of `total` while the move runs and `0` once it is `done`, and `status` is `running` or `done`. An instance another transaction holds waits for a later pass; one that ended, or that a supervisor moved meanwhile, gets no outcome of the move, so `moved` and `stayed` can add up to less than `total`. The instances that stayed come by their number, as people count, P-000009 before P-000010, each with its `instance_id`, `number` and `problems`, and the `total` that stayed. They carry no data. An instance whose move fails on five passes in a row stays on its version with the reason `failed`, "Keel could not move it; it stays on v2.", so that the move can finish.

A refused start has Keel's words: `404 unknown-process`, "The project has no process *key*." or "The project has no process *key* v9."; `409 not-older`, "v3 is the current version of *key*: its instances run on it already."; `409 nothing-to-move`, "No instance of *key* runs on v1."; `409 move-running`, "A move of the running instances of *key* is running: wait until it is done."; `409 broken-definition` when the current version no longer loads; `403` for a viewer; `422 invalid-request` for a body that is not exactly `from_version`, a whole number from 1 to 2,147,483,647. A move of another process or project, or an id that is no move, is `404 unknown-move`: "The project has no such move." The list of processes shows `running_move` for each process: the id of its running move, else `null`; an older Keel does not send it.

## Moving instances to a newer version

An instance runs on the version of its process that it started on, whatever is published after, until it is moved. A move puts it on the process's current version, the newest published, from where it stands: it keeps its number, its data and its history, and from then on it runs the new version. Keel records the move in the instance's history, and replays that history with each side of the move on its own version.

### When an instance can move

An instance moves when what it holds carries over to the new version as it is:

- **The same elements.** Each task it holds, an open one or one a join still counts, is the element with the same id in the new version, of the same kind, in the same place: in the process, or in the same subprocess.
- **Worked the same way.** Each open task is worked as it was: a user task for the same queue or person and the same drafting agent, an agent task by the same agent with the same reads, writes, required values and outcomes, a call to a system with the same call (its request, its outputs, its timeout and what it does when it fails), a task that starts a case for the same case type with the same results, a call activity for the same process with the same variables taken back, an event-based gateway with the same branches, a boundary event on the same activity.
- **Nothing new around it.** The new version adds no boundary event to an open task, takes none away, and adds or takes away no event subprocess of the process or of a subprocess that is running: such an event would not have been armed when the task was reached.
- **Data that fits.** The instance's data fits the new version's variables, required ones included.

Anything else changes nothing for an instance that is at a task: tasks added, removed or rewired ahead of where it stands, a gateway's conditions, a subprocess that gains a task ahead, an open user task's name, form, outcomes, checks, writes and service level, the name or the key of a message it waits for, the name of a signal, a timer's duration, whether an event subprocess interrupts, whether a boundary event interrupts (one that already fired without interrupting cannot be made interrupting while its task is open), a completion condition. An element behind where the instance stands, which it passed, does not matter either, unless a join still counts it. Keel does not map a renamed element to its old one: element ids are the mapping, so an instance whose task's element id changed stays where it is.

An instance that cannot move stays on its version, untouched, and Keel says why, in one line for each reason:

| Reason | Keel says | What to do |
|---|---|---|
| An element it holds is gone | "*Task* is open, and version 3 has no element *id*", or "*Task* has finished, but the instance still needs it, and version 3 has no element *id*" | Publish a version that keeps the element, or move the instance once it is past it. |
| It became another kind | "*Task* is a user task in version 2 and a manual task in version 3", with the kinds of element a process has: a service task that calls a system, an agent task, a service task that starts a case, a call activity, a receive task, a catch event, a throw event, a boundary event, an event-based gateway, an exclusive, an inclusive or a parallel gateway, a subprocess, an event subprocess, a business rule task, a start event, an end event | Keep the element's kind, or wait. |
| It moved | "*Task* is in the process in version 2 and in *Checks* in version 3". When two subprocesses share a name, their ids tell them apart: "*Checks* (s1)". | Keep the task where it was. A subprocess that is only renamed is no reason. |
| It waits for another event | "*Task* waits for a timer in version 2 and for a message in version 3" (a timer, a message, a signal or an error). For an event subprocess started by a timer, a new start event: "…and for another timer in version 3". For a catch event or a receive task put behind an event-based gateway: "*Task* waits for a message in version 2 and is a branch of an event-based gateway in version 3". | Keep the kind of event. |
| It is worked another way | "*Task* is open for the queue *q*, and version 3 gives it to the queue *r*"; "*Task* has the agent *a* drafting for its person, and version 3 has no agent"; "The agent *a* is at work on *Task*, and version 3 gives it to the agent *b*", or "…changes what it reads, writes or ends with"; "*Task* has called *connection*, and version 3 makes another call"; "*Task* waits on a case of *type*, and version 3 starts a case of *type*", or "…takes other values back from it or ends it another way"; "*Task* waits on *process*, and version 3 calls *process*", or "…takes other variables back from it"; "*Boundary* sits on *A* in version 2 and on *B* in version 3"; "*Gateway* waits on its branches, and version 3 gives it other branches" | Finish the task, then move. |
| A boundary event differs | "*Task* is open, and version 3 adds the boundary event *B*", or "…takes away the boundary event *B*". Also "*B* has fired on *Task*, which is still open, and version 3 makes it interrupt": a boundary event that fired without interrupting, made interrupting while its task is open. | Move once the task is done. |
| An event subprocess differs | "The process is running, and version 3 adds the event subprocess *E*", or "…takes away the event subprocess *E*"; "*Phase* is running, …" for a subprocess | Move once the scope has ended. |
| A join would join other flows | "*Join* holds a branch that arrived, and version 3 joins other flows there" | Move once the join has fired. |
| A task that runs for each item differs | "*Task* runs once in version 2 and for each item in version 3", "…runs for each item in version 2 and once in version 3", or "*Task* runs for each item, and version 3 runs its items another way" (only the completion condition may change) | Move once the task is done. |
| The data does not fit | "Version 3 refuses its data: *note*: must be an integer", or "…*note*: not a declared field", "…*amount*: required". For an object the new version gives fields, "…*answers*: holds a field that version 3 does not declare". A reason names the variable, never its value or a key in it. | Declare the variable the way the instance holds it. |
| The process has another id | "The process is open, and version 3 names its process *x*, not *y*" | Keep the `id` of the `bpmn:process`. |

Moving through the API adds a few more: the version asked for is not the process's current one, the instance runs on it already, the instance ended, or a version it needs no longer loads. Each says so in its own words below.

### What a move keeps

A move keeps what was set when the task was reached:

- Every task, and its work item, who holds it, its queue, its goal and its deadline.
- The timers it armed, at their due times. A timer of the new version with another duration does not re-arm, and a goal or a deadline of the new version does not change the ones set.
- A call already made, with its retries, and an agent's session, its draft and its raised hand.
- The case or the process a task waits on, and its link.
- Its number, data and history.

The new version decides the rest, as the instance reaches it: a task's form, outcomes, checks and writes, labels, the queues and service levels of the tasks it reaches next, and everything ahead. A message or a signal wait the new version names another way is set again under the new name, so the instance takes the new name from then on; a signal already on its way under the old name finds no wait and is dropped. A move opens and closes no work item, and tells no one: no notice, no mail.

The instance's history shows "*Who* moved the process to version 3", or "The process moved to version 3" when Keel's own move did it. Its diagram becomes the new version's, with what the instance did before marked wherever the new version has the same elements.

### Who moves

- A **supervisor** moves one instance, from its page, to the current version ("Move to version 3…" in [An open process](/keel/business/open-process/#move-to-the-current-version)), or by the API.
- **Editors and owners** move every running instance of an older version at once, from the process's [Versions tab](/keel/builder/processes/#the-versions-tab). The builder first sees how many could move and why the others could not, from the oldest thousand instances. The move starts after they confirm, and Keel moves the instances one at a time, in the background. One that cannot move stays on its version, and the move lists it, with why. A process has one running move: a move starts only when the one before it is done.

An instance moves only to its process's current version, and only from an older one, never back. A version published while a move runs leaves the instances not yet moved on their version, with the reason "Version 4 was published while the move ran: move the instance to version 4"; start another move.

## Figures

Keel counts a process's instances and its tasks over a period. Supervisors read the figures on the business app's [Processes](/keel/business/processes/#figures-supervisors) page, above the list. Builders read them on the **Figures** tab of a process's page in Keel Builder, by version: see [the Figures tab](/keel/builder/processes/#the-figures-tab). They are apart from the cases' figures: the [Overview](/keel/business/overview/) never counts an instance, and a process's tasks and instances never count in a case's figures. The figures name no instance and show no value of its data.

A period is the last 7, 30 or 90 days in the apps, and ends now. Through the API it is `days`, 1 to 92, 30 unless given. A count of none reads **None**, and a time or a share that nothing is behind reads `—`.

### What the instances' figures count

| Figure | What it counts |
|---|---|
| **Running** | Instances running now. |
| **Needs a supervisor** | Instances with an incident or a timer that could not fire, now: the count of the Processes page's **Needs a supervisor** tab. |
| **Started** | Instances that started in the period. |
| **Finished** | Instances that completed, or that a terminate end event ended, in the period, with `28 completed · 2 ended` under it when any ended. |
| **Failed or cancelled** | Instances an error ended, or a supervisor cancelled, in the period, with `1 failed · 3 cancelled` under it. |
| **Median to finish** | The median time from start to finish of the instances that finished in the period, with `90% within 4.2 d` under it. |

An instance counts in the period it ended in, and an instance still running counts in no time. An instance counts under the version it runs on, or ended on: one moved to a newer version counts under the newer one, with its whole time and its start.

### What the tasks' figures count

A process has a row for each task its file shows a figure for. **Waits on** says what the task waits for, and so which tasks have a row:

| Waits on | The task |
|---|---|
| **A person** | A user task or a manual task. |
| **An agent** | A service task that calls an agent. |
| **A system** | A service task that calls a system. |
| **A case** | A service task that starts a case, while it waits for it. |
| **A called process** | A call activity. |
| **A message** | A receive task, or a message catch event. |
| **A signal** | A signal catch event. |
| **A timer** | A timer catch event. |
| **The first of its events** | An event-based gateway. |
| **Its own tasks** | An embedded subprocess, or an event subprocess. |

Start and end events, the other gateways, business rule tasks and boundary events have no row: they take no time of their own.

| Figure | What it counts |
|---|---|
| **Open** | Tasks waiting now, in instances running now. `4 · 1 past deadline` counts, of them, those whose deadline passed while they waited. |
| **Done** | Tasks that left in the period by completing, or by ending in a BPMN error. A task withdrawn, because an instance was cancelled or an event subprocess interrupted it, is not done. |
| **Median time** | The median time from the start of the done tasks to their end. |
| **Met deadline** | Of the done tasks, the share that were not past their deadline, for a task with a service level. `—` for another, and when none is done. |
| **Waited to be taken** | For a person's task only: the median time from the opening of its work item to its taking, or to its closing when nobody took it. A task given back and taken again counts to its last taking. |
| **Incidents** | Incidents raised on the tasks that left in the period, done or withdrawn. |

A task counts under the version of the change that ended it, so what an instance finished before a move stays with the older version. A task still open counts under the version of its instance now.

- **A task that runs for each item** counts each of its instances as a task of its own: each vote, each call.
- **A subprocess** counts once, as **Its own tasks**, and its tasks count as theirs. An event subprocess counts its run the same way, and the task it interrupted is withdrawn.
- **A call activity** counts the time it waits for the called instance. The called process's tasks count under that process.
- **A service task that starts a case** counts the time its case takes. The case counts only in the cases' figures.
- **A timer** counts the time the timer ran.
- **A version that no longer loads** keeps its instances' figures, but its tasks cannot be shown: "Version 2 no longer loads, so its tasks cannot be shown." Read for every version, a task shows by the name the current version gives it, else the newest version that names it. A task no version that loads names has no row.

After an upgrade to a Keel that counts them, Keel counts the tasks of the instances that ran before in the background. Until it is done, the task figures cover the instances counted so far.

### The figures through the API

The routes are listed with the others: the business door's two in [Running instances](#running-instances), for supervisors, and Keel Builder's, for any member of the project, in the builders' list above. Other staff and service keys get `403 forbidden` on the business door's: "Only the project's supervisors read the process figures."

The first answers a row for each published process, by name, with zeros for one that has no instance. `name` is the current version's name, else the key made readable:

```json
{"period": {"since": "2026-10-14T09:00:00Z", "until": "2026-11-13T09:00:00Z", "previous_since": "2026-09-14T09:00:00Z"},
 "processes": [{"process": "loan-review", "name": "Loan review", "version": 3, "running": 12, "attention": 1, "started": 40,
                "completed": 30, "terminated": 2, "failed": 1, "cancelled": 3, "median_seconds": 183600.0, "p90_seconds": 432000.0}]}
```

The other two answer the same for one process. `version` left out reads every version, and `instances` is the process's row; a version reads that version's row and tasks. `versions` has each version with an instance figure and the current one, newest first. `tasks` is `null` for a version that no longer loads:

```json
{"period": {"since": "2026-10-14T09:00:00Z", "until": "2026-11-13T09:00:00Z", "previous_since": "2026-09-14T09:00:00Z"},
 "process": "loan-review", "name": "Loan review", "current_version": 3, "version": null,
 "instances": {"running": 12, "attention": 1, "started": 40, "completed": 30, "terminated": 2, "failed": 1, "cancelled": 3,
               "median_seconds": 183600.0, "p90_seconds": 432000.0},
 "versions": [{"version": 3, "running": 12, "attention": 1, "started": 40, "completed": 30, "terminated": 2, "failed": 1,
               "cancelled": 3, "median_seconds": 183600.0, "p90_seconds": 432000.0}],
 "tasks": [{"element": "review", "name": "Review the loan", "kind": "person", "open": 4, "past_deadline": 1, "done": 28,
            "median_seconds": 7200.0, "within_deadline": 0.9285714285714286, "waited_seconds": 1800.0, "incidents": 0}]}
```

A process the project never published, and a version above its current one, are `404 unknown-process`: "The project has no process *key*." or "The project has no process *key* v9." A `days` outside 1 to 92, or a `version` that is not a whole number from 1 to 2,147,483,647, is `422 invalid-request`. A read that takes more than 15 seconds is `503 figures-unavailable`: "The figures took too long to read. Try a shorter period."

## Working a process's tasks

A process's user and manual tasks are worked in the business app, like a case's steps.

- **Work.** A task waits in its queue, or with the person the file names, and shows in **Mine**, in the queue's views and in **Get next**, as a step does. Its row reads the instance's number and the process's name, such as **P-000001 · Loan review**. On its item, **Open process** opens the instance's page. **Get next case** on the Cases page opens it too. **Delegate** and **Reassign** offer people and agents, as for a case's items: see [Agents in a process's queues](#agents-in-a-processs-queues).
- **A task that runs for each item.** Each instance is a work item of its own in the task's queue, or with the person the file names, and its step reads "*task* · *n* of *count*", such as "Approve · 2 of 3". Anyone in the queue may claim any instance. With "Each person completes one instance at most", someone who completed one instance cannot complete another of the task, and the page says "Someone else must finish this step." See [A task that runs for each item](#a-task-that-runs-for-each-item).
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
- Each instance of a task that runs for each item has a goal and a deadline of its own, from the moment that instance is ready: when the task runs one after another, an instance counts from when the one before it completed.

A process's tasks never count in the cases' figures. Their own are in [Figures](#figures).

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
| Send a message to the instances that wait for it with a key | `POST /api/projects/{project}/messages` with `{"name": "documents arrived", "key": "CL-2041", "payload": {"docs_note": "scan"}}`; see below | Staff and service keys |
| Send a signal to every instance that waits for it | `POST /api/projects/{project}/signals` with `{"name": "rates changed"}`; see below | Supervisors and service keys |
| Start an instance | `POST /api/projects/{project}/processes` with `{"process": "loan-review", "data": {"amount": "20000.00"}}` | Staff and service keys |
| List the processes an instance may start on, each with the form it starts with | `GET /api/projects/{project}/process-types` | Staff and service keys |
| List instances, newest first | `GET /api/projects/{project}/processes`, with `process`, `status`, `attention=true`, `q` (a part of the number, two to a hundred characters), `cursor` and `limit`. Each row names its process. | Staff and service keys |
| Read the figures of every process the project published: see [Figures](#the-figures-through-the-api) | `GET /api/projects/{project}/process-figures`, with `days` | Supervisors |
| Read the figures of one process | `GET /api/projects/{project}/process-figures/{key}`, with `days` and `version` | Supervisors |
| Read an instance | `GET /api/processes/{instance_id}` | Staff and service keys |
| Ask whether it can move to the process's current version, and why not | `GET /api/processes/{instance_id}/move` | Staff and service keys |
| Move it to the current version | `POST /api/processes/{instance_id}/move` with `{"to_version": 3}` | Supervisors |
| The processes its call activities called, oldest first, each with its state | `GET /api/processes/{instance_id}/calls` | Staff and service keys |
| Read it as its page shows it: its tasks with their forms and who holds each, its goals and deadlines, what it waits for, its data. An instance of a task that runs for each item carries `instance`: its `number`, how many there are (`of`) and its `item`; so do the rows of `…/tasks` | `GET /api/processes/{instance_id}/outline` | Staff and service keys |
| Follow its changes as server-sent events | `GET /api/processes/{instance_id}/live` | Staff |
| Its diagram: the shapes and lines its file lays out, each shape marked `done`, `active`, `incident`, `withdrawn` or `armed` (an event subprocess that waits to start), or not marked, `triggered` on an event subprocess, and, on a task that runs for each item, `loop`: `parallel` or `sequential` | `GET /api/processes/{instance_id}/diagram` | Staff and service keys |
| The attempts of its calls to systems | `GET /api/processes/{instance_id}/system-calls` | Staff and service keys |
| Its open tasks | `GET /api/processes/{instance_id}/tasks` | Staff and service keys |
| Its history | `GET /api/processes/{instance_id}/history` | Staff and service keys |
| Check its history replays | `POST /api/processes/{instance_id}/replay` | Staff and service keys |
| Send it an event | `POST /api/processes/{instance_id}/events` | See below |

A message sent to the project (`POST /api/projects/{project}/messages`) gives the message `name` to every running instance of the project that waits for it with the `key` (1 to 1,000 characters, not blank), each in a transaction of its own, oldest first, with the `payload` the waits list. It answers `200`:

```json
{"reached": [{"instance_id": "…", "number": "P-000001", "process": "claim-documents", "seq": 2, "status": "running"}],
 "refused": []}
```

An instance that refuses the message (its key changed since, it ended, the payload does not fit, its version no longer loads) is in `refused` with its `code` and `message`, and never undoes another's delivery. No instance waiting is `409 unknown-message`: "No running instance of the project waits for the message *name* with that key." More than 100 is `409 too-many-instances`: "More than 100 instances wait for the message *name* with that key: a message reaches at most 100." When every instance refuses, the answer is the first refusal, with the instance's number before it: "P-000001: the message documents arrived may not write other". Sent again with the `Idempotency-Key` it was first sent with, by the same caller and with the same body, it answers as the first time with the header `Idempotent-Replayed: true`, and no instance takes it twice. A send cut short, such as by a restart between two instances, is finished by sending it again with the same key. A send every instance refuses keeps nothing, so its key can be used again. The key another caller or another body used is `422 key-reused`: "*key* was used for another send in this project".

A signal sent to the project (`POST /api/projects/{project}/signals`) gives the signal `name` (1 to 200 characters, with a character other than a space) to every running instance of the project that waits for it. It carries no values: a body with any other field is refused `422`. It answers `202`, with the signal and the number of instances it is on its way to:

```json
{"signal": "rates changed", "instances": 3}
```

Each instance takes the signal after the answer, in a change of its own, so the answer says how many instances it is for, not what each did. No instance waiting is `202` with `"instances": 0`, not a failure, and there is no cap on how many it reaches. Supervisors and service keys send a signal, since it can interrupt every open instance at once: another member of the staff gets `403 forbidden`, "Only a supervisor may send a signal." Sent again with the `Idempotency-Key` it was first sent with, by the same caller and with the same body, it answers as the first time with the header `Idempotent-Replayed: true`, and nothing is sent twice. The key another caller or another body used is `422 key-reused`: "*key* was used for another send in this project".

Whether an instance can move to the process's current version (`GET /api/processes/{instance_id}/move`) answers with the version it runs on, the version it would move to, and the reasons it cannot, which are empty when it can:

```json
{"from_version": 2, "to_version": 3,
 "problems": [{"code": "missing-element", "element": "pay", "message": "Pay is open, and version 3 has no element pay"}]}
```

It reads the instance as it stands, so an event since may change the answer; the move checks again. Each reason has a `code` (`missing-element`, `other-kind`, `other-place`, `other-event`, `not-alike`, `boundary-events`, `event-subprocesses`, `join-inputs`, `invalid-values`), the `element` it is about (none for the data, and for an event subprocess of the process itself), and the words above. An instance that already runs on the current version answers one reason, `same-version`: "P-000001 already runs on version 2."; an ended one `process-ended`: "P-000001 is cancelled: only a running instance moves to another version."; a version that no longer loads `broken-definition`. The read is logged as a view of the instance, like the others.

A move (`POST /api/processes/{instance_id}/move`, with `{"to_version": 3}`, a whole number from 1 to 2,147,483,647) is for supervisors: another member of the staff or a service key gets `403 forbidden`, "Only a supervisor may move an instance to another version." It checks again with the instance locked, so an event between the read and the move is seen. It answers `200` with the instance as the move left it, as an event does:

```json
{"instance_id": "…", "number": "P-000004", "seq": 5, "status": "running"}
```

An instance that cannot move answers `409 cannot-move` and is left as it was, with the reasons:

```json
{"code": "cannot-move", "message": "P-000004 cannot move to version 3.",
 "problems": [{"code": "missing-element", "element": "pay", "message": "Pay is open, and version 3 has no element pay"}]}
```

A version that is not the current one is `409 not-current-version`: "Version 3 is the current version of *key*: an instance moves only to it." (older versions included); one the instance runs on already `409 same-version`; an instance that ended `409 process-ended`. A body that is not exactly `to_version`, as a whole number, is `422 invalid-request`. Sent again with the `Idempotency-Key` it was first sent with, by the same caller and with the same body, it answers with the instance as it stands and the header `Idempotent-Replayed: true`, and moves nothing twice; the key another caller or another body used is `422 key-reused`. Two supervisors at once: the second finds the instance moved and gets `409 same-version`.

Starting an instance answers its `instance_id`, its `number`, such as `P-000001`, and its status. The start data must fit the declared variables. Send an `Idempotency-Key` header with each start: a start sent again with the same key answers with the instance it started the first time.

A process a call activity called is an instance like any other, with its own number: it is listed, read, followed and cancelled as the others are, and a cancel of it makes the call activity that waits for it throw `process-cancelled`. Its page says it was called by the instance that started it.

The events an instance takes:

| Event | Body | Who sends it |
|---|---|---|
| Complete a task | `{"type": "task.completed", "task": "t3", "outcome": "approve", "output": {"note": "fine"}}` | Whoever holds its work item; while no one holds it, a member of its queue. A member of the queue its missed deadline escalated to. Supervisors always. Never a service key. |
| Deliver a message | `{"type": "message.received", "name": "documents", "payload": {"docs": "received"}}`, with `"key": "CL-2041"` to reach only the waits whose key holds it | Staff and service keys. Every task of the instance waiting for that message takes it (with a `key`, those whose key holds it). |
| Cancel the instance | `{"type": "process.cancelled", "reason": "withdrawn"}` | Supervisors |
| Answer an agent's question | `{"type": "hand.answered", "task": "t5", "answer": "2026", "note": "the new policy"}` | Whoever holds the question's item; while no one holds it, a member of the queue it went to; supervisors always. Never a service key. The `note` is optional, and an answer must be one of the question's choices when it has some. |
| Ask a drafting agent to revise | `{"type": "revision.requested", "task": "t3", "note": "Cite the bureau"}` | Whoever holds the task, or its queue while no one does; supervisors always. Never a service key. |
| Message an agent | `{"type": "agent.messaged", "task": "t5", "text": "Use the May statement."}` | Any member of the staff. Keel adds the sender's name. Never a service key. |
| Retry a task with an incident | `{"type": "task.retried", "task": "t5"}` | Supervisors |

Keel sends the rest itself: a timer firing (`timer.fired`), a signal arriving (`signal.received`), a call or an agent failing (`task.failed`), an agent raising its hand (`hand.raised`), an agent's draft (`task.drafted`), a case's close (`case.closed`) and a called process's end (`called.ended`). A body that names one is `422 invalid-event`, with the reason: for `signal.received`, "Only Keel delivers a signal: send it to the project."

A task's id, such as `t3`, comes from the instance's open tasks. Completing a task that has already finished answers `409 task-closed`. An event sent again with the `Idempotency-Key` it was first sent with is answered with the instance as it stands, and the header `Idempotent-Replayed: true`; it is not applied twice.

### Incidents

A call or an agent task that fails for good leaves its task with an **incident**. The task stays where it is, the instance keeps running, and a supervisor decides. The instance's list finds it with `attention=true`.

- The history records `incident.raised`, with the reason.
- The instance's page says so, and shows it to supervisors first, under **Needs a supervisor**, with **Retry** and, for a call, its attempts. **Waiting for** reads "*task* · its call to *system* failed: a supervisor retries it or cancels the process", and an agent task's **Now** card reads "*Agent* could not finish this task: a supervisor retries it or cancels the process."
- A supervisor sends `task.retried` for the task, or cancels the instance with `process.cancelled`: the instance's page has **Retry** and **Cancel the process…** for both. A call that may have reached its system before it failed asks first. A retried call is made again as a new call. A retried agent task starts the agent in a fresh run, with a new session, or goes to people in its raise-hand queue when its agent is switched off by then.
- A task without an incident answers `task.retried` with `409 not-allowed`.
- The agent that drafts for a person is the exception: its failure is no incident. The person works alone, and the task has no retry.

Timers fire on their own. When a timer cannot fire because what follows it fails, such as a condition that cannot be evaluated on the instance's variables, the timer is kept as **stuck**: it is never fired again, the instance shows why, and the list's `attention=true` finds it. A supervisor then cancels the instance.

The history, `GET /api/processes/{instance_id}/history`, records what happened to the instance's tasks. For a task that runs for each item it holds `instances.started` and `instances.completed`, and every entry of an instance of it carries `instance` and `of`. For an event subprocess it holds `subprocess.triggered` each time a run starts: the event subprocess (`element`), the run's task, the start event (`trigger`), whether it interrupts and the subprocess it sits in (`scope`, none for the process). For a signal it holds `signal.thrown` when a throw event or a signal end event sends one (the `signal` and the sending `element`) and `signal.received` when an instance takes one (the `signal`, and who sent it: the `actor` of a send to the project, else the `origin` of one an instance sent, its `instance_id`, `number` and `element`). For agents it holds `task.drafted`, `revision.requested`, `agent.messaged`, `hand.raised`, `hand.answered`, `agent.failed`, `agent.disabled`, `incident.raised` and `task.retried`. A person's `task.completed` on a task an agent drafts also holds `contributions`: who gave each value, the agent or the person.

An instance is `running`, `completed`, `terminated` (by a terminate end event), `failed` (by an error no error boundary event or error event subprocess caught) or `cancelled`.

A refused call answers with a `code` and a `message`: `404 unknown-instance` for an instance that does not exist or belongs to another project, `422 invalid-event` for a body that is no event, `403 forbidden` for a sender who may not send it, and `409` with Keel's reason for anything the instance cannot take, such as `unknown-outcome`, `check-failed` or `rule-error`. An agent's task adds `hand-raised` (a task with a question waiting takes no completion, draft, revision or message), `no-hand-raised` and `invalid-answer` for an answer, `wrong-actor` for an event only a person or only an agent may send, and `not-allowed` for a message when no agent is working on the task now, and for a revision while its agent still drafts or once its agent failed or is off.

---
title: Steps and their contract
sidebar:
  label: Steps
---

A step is work: something an agent, a person, a queue or another system does before the case goes on. Pick a step on the [board](/keel/builder/workflow/) or in a stage's flow, and its panel opens. The panel is the step's **contract**: who does it, what it reads, what it must return, what must hold, and where each outcome leads.

The panel's header names the kind: **Agent step**, **Person step**, **Agent with a person**, **System step**, or **Vote** for a step decided by votes. Its sections follow in this order.

## Done by

Pick the performer. Changing it keeps what the new performer uses and drops the rest.

### An agent

- **Agent**: one of the project's agents, by name. Agents are made and changed in Studio; an agent made there shows here when you come back to the window. The project's helpers, the case agent and the designer agent, are never offered (see [The project's helpers](/keel/builder/designer-agent/#the-projects-helpers)).
- **Raised hands go to**: the queue that gets the agent's questions when it needs a person.

The step needs both. Until both are picked, the panel says **Pick its agent to save it.** or **Pick where its raised hands go to save it.**, and nothing is saved.

The agent works the step in its own session. It gets the values of the fields the step reads, may use only what [May use](#may-use) allows, and must finish with one of the step's outcomes and the fields that outcome requires. Keel also refuses an agent's result that does not say where each value came from.

If the agent fails for good, people take the step: it opens as work in the **Raised hands go to** queue. The same happens to each of its steps that opens while a supervisor has the agent turned off.

### A person or a queue

- **A queue**: one of the project's queues. Its members see the step in the queue and claim it.
- **A person**: one person, found by name. Picking one clears the queue.

With no person picked, you can turn on **Decided by a vote**. Set **Votes needed** and **Out of**; the panel reads, for example, `2 of 3 votes decide`. Every member of the queue may vote, once, choosing one of the step's outcomes. As soon as one outcome has the votes needed, the step ends with it. A vote returns no fields.

A step with neither a queue nor a person opens with no one to work it: nobody can take it in the business app, and a supervisor has to [move the case by hand](/keel/business/supervisors/#move-a-case-by-hand). Give every person step a queue or a person.

### An agent with a person

The agent drafts the step, and one person finishes it: they see the agent's draft in the step's form, change what they need, and submit it. The person, not the agent, is checked against [maker-checker](#maker-checker) and [authority](#authority).

- **Agent** and **Raised hands go to**, as for an agent step.
- **Finished by**: the queue whose member finishes it, or **A person**. It is never a vote.

If the agent fails, or is turned off when the step opens, the person works the step alone.

### A system

The step calls another system's REST API through one of the case type's [connections](/keel/builder/connections/), and maps the answer into fields. Pick the **Connection** first; the rest shows once one is picked, starting as a `GET` of `/`.

| Setting | What it is |
|---|---|
| **Method** | `GET`, `POST`, `PUT`, `PATCH` or `DELETE`. |
| **Path** | The path after the connection's base URL. `{field}` puts a field's value in the path; `{case.id}`, `{case.number}` and `{case.type}` put the case's own. |
| **Query**, **Headers** | JSON objects of names and values. A value is text, or `{"$field": "amount"}` for a field's value. Add `"optional": true` to leave it out when the field has no value. `{"$case": "number"}` is the case's own. |
| **Body** | A JSON template for `POST`, `PUT` and `PATCH`, with the same markers. `"as": "number"` writes a decimal field as a JSON number. |
| **Outputs** | **Add output** picks a field; then write the response path its value is read from, such as `$.body.decision`. `$.status` and `$.headers.name` read the status and a header. A field you map is added to what the step writes. |
| **Accept statuses** | Statuses outside 2xx that count as answers to map, such as `404, 409`. |
| **Timeout (seconds)** | How long one call may take; blank uses the connection's. |
| **When it fails for good** | **Fail the case**, **Send to a queue** (people in the queue then complete the step by hand), or **Go to** a place in the flow. |

Credentials never go in a step's headers; they belong to the connection. Every call but a `GET` has an idempotency key, the same on each attempt of one call, so the other system can tell a retry from a new request. The connection's **Idempotency-key header** names the header it is sent in.

If the connection list is empty, the panel says **The case type has no connections yet.**

## Receives

The fields the step reads, as chips; a file field is marked `· file`. The **Add** menu picks another. An agent gets these values when it starts.

## May use

Only for steps an agent works. Each list starts with everything the agent has:

- **Tools**: the agent's tools, as Studio lists them;
- **MCP servers**: the agent's MCP servers;
- **Knowledge**: the knowledge bases the case type grants on its [Settings tab](/keel/builder/case-type-settings/#knowledge).

Press **Narrow** to keep only some, then add them one by one from the **Add** menu; the list names what it leaves out as **Not allowed**. **Use everything** drops the narrowing. "A step can narrow these lists, never widen them."

For tools the agent reaches by a prefix, type the tool's name; a name the agent has no tool by is refused.

## Must return

The fields the step writes, one row each, with the field's type and whether it is required: **Required**, **Required for** some outcomes, or **Optional**. The row's switch makes it required whatever the outcome. The **Add** menu adds another. **Edit form** opens the step's form on the [Forms tab](/keel/builder/forms/).

A vote reads **A vote returns no fields.**

## Checks

Conditions that must hold when the step completes. Each has a **Condition** and a **Message**. The condition is written in CEL over the case's fields, as they will be with the step's values, for example `amount <= 250000.0`. When a condition does not hold, Keel refuses the completion and the person sees the message.

Press **Add check** to add one. The dry run reports a condition it cannot read.

## Allowed outcomes

Each outcome has a **Label**, the words people and agents see, and **Leads to**, where the case goes next:

| Choice | Where the case goes |
|---|---|
| A node's name | That node of the same stage. |
| **Next stage:** *name* | The next primary stage. |
| **Done** | Shown instead of Next stage after the last primary stage, and after an alternate stage: the case closes as `completed`. |
| **Stage:** or **Alternate stage:** *name* | The start of that stage. |
| **End of this path** | This path stops. The case goes on along its other paths. |
| **Action:** *name* | Starts that optional action. |
| **Closed:** *resolution* | The case closes with that resolution. |
| **Close as…** | Asks for a new **Resolution**, such as `Approved`, then **Close as**. |

When the step writes fields, each outcome also lists the fields it **Requires** beyond those always required. Its **Add** menu adds one.

Type a label in **Name an outcome** and press **Add outcome** to add one. A step keeps at least one outcome.

For an agent step, a box **If the agent needs a person** says where its questions go, such as **Raised hand goes to the Underwriting queue**. Change it under **Done by**.

## Maker-checker

The earlier steps whose doers may not do this one: "Someone other than whoever did" each of them. Pick them from the case type's other steps. With none, **Anyone may do it.** Voters count as doers of a vote.

## Authority

An authority check needs both:

- **Amount field**: a whole number or decimal field of the case type;
- **Scope**: a name for the kind of authority, such as `lending`.

Whoever completes the step, or votes on it, needs a limit in that scope at least as large as the amount, with the step's own values included. Someone with no limit in the scope is refused. Supervisors set limits on the business app's [Team page](/keel/business/supervisors/#authority-limits). **Clear** removes the check.

## Service level

A **Goal** and a **Deadline**, each a number and **Minutes**, **Hours** or **Days**. A goal without a deadline is not saved: "A service level needs a deadline."

Once there is a deadline:

- **Count business time**, when the case type has a calendar, counts only working time. It is on by default.
- **Past the deadline, escalate to** picks a queue. When the deadline passes, an escalation opens there; the step stays with whoever works it.

**Clear** removes the service level.

## The panel's footer

- **Open agent**, for a step an agent works, opens Studio's agents page in a new tab, where agents are changed.
- **Test this step**, for a step no agent works, dry-runs the draft and lists the [scenarios](/keel/builder/scenarios/) whose expected path passes through the step, each **Passed**, **Failed** or **Not run**. With none, it says **No scenario passes through this step. Add one in Scenarios.**
- **Remove step** removes the step after asking.

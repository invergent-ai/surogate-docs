---
title: Keel concepts
sidebar:
  label: Concepts
---

This page explains the words Keel uses. Each term also has a one-line entry in the [Glossary](/keel/reference/glossary/).

## Case types and versions

A **case type** is the definition of one kind of case, such as a loan request or an insurance claim. It holds:

- **fields**: the data a case carries;
- **stages**: the primary path a case follows, and alternate stages it can be sent to;
- a **flow** in each stage: the steps and the automatic nodes between them;
- **optional actions**: steps people can start at any time in a case;
- **forms**: how each step's form, and the form a case starts with, are laid out;
- **service levels**, **case events**, the **knowledge** its agent steps may use, and its **connections** to other systems.

Builders change case types in a **draft**. Publishing the draft gives each changed case type a new **version**: version 1, version 2 and so on. New cases start on the current version. A running case stays on the version it started on unless a builder moves it.

## Cases

A **case** is one running instance of a case type version. It has a number made of the case type's number prefix and a count, such as `LD-000042`, a title, its data, its files and its full history. A case is **open** until it closes with a **resolution**, such as `approved`, `declined` or `completed`.

## Processes

A **process** is a second way to define work, drawn as a diagram in BPMN, the standard notation for business processes. A process has tasks done by people and agents, decisions, waits, timers and calls to other systems. Builders upload a diagram made in another modeller, draw one in Keel Builder, or describe it to the designer agent. Publishing gives the process a version, as for a case type. Staff start **instances** of it in the business app. See [BPMN processes](/keel/processes/).

A case type and a process can work together: a case's process node starts an instance of a process, and a process can start and follow cases.

## Stages

A case is always in one **stage**. The **primary stages** are the normal path, shown left to right on the builder's board. **Alternate stages**, such as Withdrawn or Fraud hold, are stages a case only reaches when an outcome, a case event or a supervisor sends it there. A case type can have a single stage.

When the last step of a stage leads to **Next stage**, the case enters the next primary stage. After the last primary stage, the case closes as `completed`.

## Flows, steps and nodes

Inside a stage, the **flow** is a graph of nodes. The case enters the stage at its start node and moves along the outcomes of each node.

| Node | What it does |
|---|---|
| **Step** | Work done by an agent, a person or queue, an agent with a person, or another system. The case waits until the step finishes with an outcome. |
| **Decision** | Picks one branch from conditions over the case's data. Automatic. |
| **Rule** | Runs a decision table or a scorecard and writes its results into fields. Automatic. |
| **Wait** | Waits for an event, a time, or a condition, with an optional limit. |
| **Parallel split** | Starts several paths at once. |
| **Join** | Waits until every path that leads to it has arrived, then goes on. |

[Node kinds](/keel/reference/node-kinds/) lists every setting of each node.

## Performers

Every step has a **performer**: who does the work.

- **An agent**: a Surogate agent of the project works the step in its own session. It must return one of the step's outcomes and the fields the step asks for, and say where each value came from. When it needs a person, it **raises a hand**.
- **A person or a queue**: the step becomes a work item for one person, or for a queue whose members claim it. It can also be decided by a **vote** of the queue's members.
- **An agent with a person**: the agent drafts the step, and one person checks the draft, changes it if needed, and submits it.
- **A system**: Keel calls another system through one of the case type's connections and maps the answer into fields.

People and agents are treated alike. Maker-checker and authority limits apply to both. An agent can also take a work item as a person does: as a member of a queue, as a delegate, or when a supervisor reassigns the item to it.

## Outcomes

A step ends with an **outcome**, such as Approve or Decline. Each outcome leads somewhere: another node in the stage, the next stage, another stage, an optional action, the end of this path, or a close with a resolution. An outcome can require fields: the step cannot finish with that outcome until they are filled.

## Fields, forms and documents

A **field** is one piece of a case's data: text, a number, a date, a choice, a file, a list or an object. Each step lists the fields it **reads** and the fields it **writes**.

A step's **form** is made from the fields it writes. The form a case starts with shows the case type's required fields. Builders order, group and label form fields on the Forms tab.

**Documents** are files the case holds in a file field, or files its agents wrote. Office documents open in the web editor inside the case. The person who holds a step of the case can edit them; other staff can comment.

## Queues

A **queue** is a shared list of work for a team. Builders define a queue's name, its **serving order** (which work comes first) and its **priority** among queues. Supervisors decide who works each queue: people, agents, or both. **Get next** hands a person the next item from their queues.

## Service levels and calendars

A **service level** has a **goal** and a **deadline**, both as durations. It can be set on a step, a stage or the whole case. Past the goal, the work shows **Past goal**. Past the deadline it shows **Past deadline**, and when the service level names a queue to escalate to, an **escalation** item opens there. The step stays with whoever works it.

A **calendar** sets working days, working hours and holidays. When a case type has a calendar, its service levels and waits can count **business time** only. While a case waits on the client, the case's own service-level clock pauses.

## Authority limits and maker-checker

An **authority check** on a step compares an amount field with the limit of the person or agent who completes it, in a named **scope** such as `lending`. Supervisors set each person's and agent's limits. Someone with no limit in the scope, or a limit below the amount, cannot complete the step.

**Maker-checker** names earlier steps whose doers may not do this step, so a different person checks the work.

## Raised hands

When an agent needs a person, it **raises a hand**: it asks a question, sometimes with answer choices and evidence. The question goes to the queue the step names. The agent waits, without a time limit, until someone answers. The answer, with an optional note, goes back to the agent and into the case's history.

## The project's helpers

Each project has two **helpers**, agents Keel sets up for it:

- the **case agent**, which a person asks about one case, or one process instance, in the business app. It answers from the case's data, files and history, or the instance's data, tasks, waits and history, and fills in that person's form when they ask. It never submits. See [The case agent](/keel/business/case-agent/).
- the **designer agent**, which a builder chats with in Keel Builder. It drafts case types and processes in the open draft, as the builder, and never publishes. See [The designer agent](/keel/builder/designer-agent/).

A helper never works a step or a work item, and is never offered as a step's agent or an intake agent.

## Optional actions and case events

An **optional action** is a step people can start from the case's header, in the stages and conditions the builder allows, such as "Ask the client for a document".

A **case event** is a named signal another system sends to a case. A wait for that event moves on when it arrives. Otherwise the case type's event of that name fires: it either interrupts the case and moves it, or starts an optional action alongside the current work.

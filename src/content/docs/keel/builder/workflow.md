---
title: The Workflow tab
sidebar:
  label: Workflow
---

The **Workflow** tab is where you draw a case type: its stages, the steps in each stage, and the flow between them. It has three parts:

- the **stage board**: the stages as columns of cards, with alternate stages and optional actions under them;
- the **flow** of the stage you pick, drawn below the board;
- the **panel** of the node or action you pick, on the right.

Viewers see all of it and change nothing. If no draft is open, your first change asks for one (see [Drafts](/keel/builder/drafts/#starting-a-draft)). While the [designer agent](/keel/builder/designer-agent/) takes its turn in the draft, the tab is read-only until the turn ends.

## The stage board

### Primary stages

The **Primary stages** are the columns, left to right, in the order a case goes through them. Each column shows:

- its number (`01`, `02`, …) and its name;
- its service level, such as `SLA 5 days`, when it has one;
- a card for each step, rule and wait of the stage, in the order of its flow. Decisions, splits and joins show only in the flow.

Each card shows who does the node and how:

| Card | Its line |
|---|---|
| A step done by an agent | The agent's name |
| A step done by a person or a queue | The queue, such as `Underwriting queue`, or `Assigned to` and the person |
| A vote | `2 of 3 votes decide` |
| A step an agent drafts for a person | `Intake agent drafts, Review queue finishes` |
| A system step | `Calls` and the connection's name |
| A rule | The rule's name |
| A wait | `Waits up to 5 days`, `Waits for` an event, or `Waits until` a condition |

A node that a parallel split starts reads `Parallel with` and the split's other paths instead.

Press a stage's name to open its flow below the board. Press a card to open its panel.

Editors and owners also see:

- **Add step** under each column, to add a node to that stage;
- **Add stage** after the last column, which asks for the new stage's **Name**;
- a pencil beside each stage's name, which opens **Edit stage**: its **Name**, its service level's **Goal** and **Deadline**, and **Remove stage**. The last primary stage has no **Remove stage**.

Removing a stage asks **Remove *stage*?**: "Its steps go with it. Outcomes that lead to it will need a new target."

### Alternate stages

**Alternate stages** are listed under the board as chips. A case reaches one only when an outcome, a case event or a supervisor sends it there; it is not on the primary path. Press **Add alternate stage** to add one, its name to pick it, and its × to remove it.

After an alternate stage, **Next stage** leads to the end of the case: it closes as `completed`.

### Optional actions

**Optional actions · any stage** are steps people can start from a case's header while the case is open, such as "Ask the client for a document". Press **Add action**, give it a **Name**, and pick who does it under **Done by**. Its panel has one more section, **When it is offered**:

- **Condition**: a condition over the case's fields; "Blank offers it always."
- **Stages**: the stages it is offered in; with none, "In every stage."

Removing an action asks first: "Outcomes and case events that lead to it will need a new target."

## Adding nodes

**Add step** under a column opens **Add to *stage***:

1. Pick the **Kind**: **Step**, **Decision**, **Rule**, **Wait**, **Parallel split** or **Join**.
2. Type a **Name**. It must have a letter or a digit; the node's key is made from it.
3. For a step, pick **Done by**: **An agent**, **A person or a queue**, **An agent with a person** or **A system**.
4. Press **Add**.

A new node leads on to the next stage until you say where it goes. A new rule names no rule yet, and a new wait waits one day. The first node you add to an empty stage becomes the stage's start.

## A stage's flow

Pick a stage and its flow opens below the board, with its number and name, and a count such as `Flow · 3 steps · 1 decision`. The canvas draws the stage's entry, every node, and where each outcome leads, including the ways out of the stage. Its branches carry their labels.

- Press a node on the canvas to open its panel.
- **Add step** and **Add decision** add a node to this stage.
- **Back to board** closes the flow.

Keel draws the flow from the case type as you edit it. While it redraws, the canvas keeps the last drawing.

## The node panel

Picking a card, a node on the canvas, or an action opens its panel on the right. Its header shows the node's kind and its **Name**, which you can change, and a close button.

- A step's panel is its contract: see [Steps](/keel/builder/steps/).
- Decisions, rules, waits, splits and joins: see [Decisions, rules, waits and parallel paths](/keel/builder/flow-nodes/).

The panel's footer holds **Remove step** (or **Remove decision**, **Remove rule**, and so on), which asks first: "Outcomes that lead to it will need a new target." Keel never rewrites outcomes that pointed at a removed node; the next dry run lists them.

## Problems on the board

After a [dry run](/keel/builder/publish/), its problems are pinned where they are: a red count on the stage, the card, the outcome or the action, and on the canvas's nodes. A problem with the case as a whole shows beside **Primary stages**, as `2 problems on the case`; press it to open the dry run's list.

A dry run of an older state of the draft pins nothing, since its problems may be gone.

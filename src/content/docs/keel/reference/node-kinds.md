---
title: Node kinds and their settings
sidebar:
  label: Node kinds
---

Every node of a stage's flow, with each setting its panel holds in Keel Builder. The pages [Steps](/keel/builder/steps/) and [Decisions, rules, waits and parallel paths](/keel/builder/flow-nodes/) explain them in full.

## Step

A step is work that waits for its performer. On the board it is a card; it ends with one of its outcomes.

| Section | Settings |
|---|---|
| **When it is offered** | Optional actions only: **Condition**, **Stages**. |
| **Done by** | **An agent**: **Agent**, **Raised hands go to**. **A person or a queue**: **A queue** or **A person**, **Decided by a vote** with **Votes needed** and **Out of**. **An agent with a person**: **Agent**, **Raised hands go to**, **Finished by** or **A person**. **A system**: **Connection**, **Method**, **Path**, **Query**, **Headers**, **Body**, **Outputs**, **Accept statuses**, **Timeout (seconds)**, **When it fails for good**. |
| **Receives** | The fields it reads. |
| **May use** | Agent steps only: **Tools**, **MCP servers**, **Knowledge**, each everything or narrowed. |
| **Must return** | The fields it writes, each required or not. **Edit form**. |
| **Checks** | Each a **Condition** and a **Message**. |
| **Allowed outcomes** | Each a **Label**, where it **Leads to**, and the fields it **Requires**. |
| **Maker-checker** | The steps whose doers may not do this one. |
| **Authority** | **Amount field** and **Scope**. |
| **Service level** | **Goal**, **Deadline**, **Count business time**, **Past the deadline, escalate to**. |

| Performer | Its work opens as | Who completes it |
|---|---|---|
| An agent | An agent session | The agent; people in its raised-hands queue if it fails or is off |
| A person or a queue | A work item for the person or the queue | The person, a member who claims it, or every member for a vote |
| An agent with a person | An agent session and the person's work item | The person, with the agent's draft |
| A system | A call to the connection | Keel's own call; people in the failure queue, if one is set |

## Decision

Automatic. Takes the first branch whose condition holds.

| Section | Settings |
|---|---|
| **Branches** | Each a **Condition**, a **Label** and **Goes to**. |
| **Otherwise** | **Goes to** and **Label**, for when no branch holds. |

## Rule

Automatic. Runs a decision table or scorecard and writes its results.

| Section | Settings |
|---|---|
| **Rule** | One of the project's rules. |
| **Assignments** | Each a **Result** of the rule and the **Field** it goes to. |
| **Then** | Where the case goes next. |

## Wait

Holds the case until something happens.

| Section | Settings |
|---|---|
| **Waits for** | **A time** (**How long**), **An event** (**Event**) or **A condition** (**Condition**); and **At most**, a limit. |
| **Waiting on** | **The client**, **A third party** or **Inside the bank**. |
| **Outcomes** | One per trigger: Elapsed, Arrived, Met and Deadline, each with a **Label** and where it **Leads to**. |

## Parallel split

Automatic. **Starts in parallel**: the places each path starts.

## Join

Automatic. Waits for every path leading to it, then goes to **Then**.

## Where an outcome can lead

| Choice | Meaning |
|---|---|
| A node's name | That node, in the same stage. |
| **Next stage:** *name* / **Done** | The next primary stage; after the last one, or after an alternate stage, the case closes as `completed`. |
| **Stage:** / **Alternate stage:** *name* | The start of that stage. |
| **End of this path** | This path stops; other paths go on. |
| **Action:** *name* | Starts an optional action. |
| **Closed:** *resolution* / **Close as…** | Closes the case with that resolution. |

An optional action's outcomes can also lead to a node of any stage. A case event that interrupts can lead to a node, the next stage, a stage or a close; one that does not interrupt starts an optional action.

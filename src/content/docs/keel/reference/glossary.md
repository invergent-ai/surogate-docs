---
title: Keel glossary
sidebar:
  label: Glossary
---

Every Keel term in one place. [Concepts](/keel/concepts/) explains how they fit together.

| Term | Definition |
|---|---|
| **Agent** | A Surogate agent of the project, made in Studio. It can work a step, draft a step for a person, take work items as a queue member or a delegate, or start cases as an intake agent. |
| **Agent question** | An agent's raised hand as it shows in work lists. |
| **Alternate stage** | A stage off the primary path, such as Withdrawn, that a case reaches only when an outcome, a case event or a supervisor sends it there. |
| **Authority limit** | The most a person or an agent may approve in a scope. Supervisors set it on the Team page. |
| **Authority check** | A step's rule that whoever completes it needs a limit in a scope at least as large as an amount field. |
| **Builder** | A member of the project in Surogate Studio, who signs in to Keel Builder as an owner, editor or viewer. |
| **Business app** | The Keel app where staff and supervisors work cases. |
| **Business time** | Time that counts only working hours on working days, by the case type's calendar. |
| **Calendar** | A project's working days, working hours, holidays and time zone. A case type can use one. |
| **Case** | One running instance of a case type version, with its data, files and history. |
| **Case agent** | The project's helper that answers a person's questions about one case, and fills in their form when they ask. It never submits. |
| **Case event** | A named signal another system sends to a case. A wait for it moves on; otherwise the case type's event of that name fires. |
| **Case number** | The case type's number prefix and a count, such as `LR-000001`. |
| **Case type** | The definition of one kind of case: its fields, stages, flows, forms and settings. Versioned. |
| **Check** | A condition a step's result must meet, with the message people see when it does not. |
| **Claim** | Taking an unclaimed item from one of your queues, so it is yours. |
| **Condition** | An expression in CEL over the case's fields, used by checks, decisions, rules, waits and optional actions. |
| **Connection** | Another system a case type's system steps call: its base URL, authentication and credential. |
| **Credential** | The secret a connection sends. Set on the published connection, never shown again. |
| **Decision** | A node that picks a branch from conditions over the case's data. |
| **Delegate** | Handing an item you hold to someone else on the staff, or to an agent. |
| **Designer agent** | The project's helper that drafts case types with a builder in Keel Builder, in the open draft. It never publishes. |
| **Draft** | A set of changes to the project's definitions, not live until published. |
| **Dry run** | Every publish check and scenario, run on a draft without publishing it. |
| **Effect** | Work Keel does outside a case after a transition: starting an agent, or calling a system. |
| **Escalation** | An item that opens in a queue when a service level's deadline passes. The step stays with whoever works it. |
| **Field** | One piece of a case's data, with a name, a label and a type. |
| **Flow** | The nodes of a stage and how its outcomes connect them. |
| **Form** | What a person fills to start a case or complete a step, made from fields and laid out on the Forms tab. |
| **Get next** | The button that gives you the first item of Needs me, or else the next unclaimed item of your queues. |
| **Helper** | One of the two agents Keel sets up for each project: the case agent and the designer agent. A helper never works a step or a work item. |
| **Intake agent** | An agent allowed to start cases of a case type. |
| **Join** | A node that waits until every path leading to it has arrived. |
| **Maker-checker** | A step's rule that it must be done by someone other than whoever did named earlier steps. |
| **Mapping** | The part of a draft that says where the open cases of an older version go in the new version. |
| **Needs me** | The list of work you hold, on the Work page. |
| **Number prefix** | The start of a case type's case numbers. |
| **Optional action** | A step people can start from a case's header, where the case type allows it. |
| **Outcome** | How a step, vote or wait ends, and where the case goes from there. |
| **Parallel split** | A node that starts several paths at once. |
| **Performer** | Who does a step: an agent, a person or a queue, an agent with a person, or a system. |
| **Pinned rule** | A rule each case keeps at the version in effect when it started. |
| **Primary stage** | A stage of the normal path, shown as a column on the board. |
| **Priority** | A queue's place among queues for Get next: lower numbers first. |
| **Publish** | Making a draft live. Each changed case type gets a new version. |
| **Queue** | A team's shared list of work, with a serving order and a priority. |
| **Raised hand** | An agent's question to a person, which pauses its step until someone answers. |
| **Reassign** | A supervisor giving an open work item, other than a vote, to someone on the staff or to an agent. |
| **Resolution** | How a case closed, such as `approved` or `completed`. |
| **Rule** | A decision table or scorecard, versioned by when each version takes effect. |
| **Rule node** | A node that runs a rule and writes its results into fields. |
| **Scenario** | A stored test of a case type: how a case starts, what happens, and what must hold. |
| **Scope** | The name of a kind of authority, such as `lending`. |
| **Serving order** | The order in which a queue hands out work: kinds first, then oldest or nearest deadline. |
| **Service key** | A key another system uses to start cases and send case events in the project. |
| **Service level** | A goal and a deadline on a step, a stage or a case, with an optional queue to escalate to. |
| **Staff** | The people of a project who sign in to the business app. |
| **Stage** | A phase of a case. A case is always in one stage. |
| **Step** | Work in a stage, done by its performer, which ends with an outcome. |
| **Supervisor** | Staff who also run the Team page and move cases by hand. |
| **Version** | One published state of a case type. A case stays on the version it started on unless it is moved. |
| **Vote** | A step decided when enough members of a queue choose the same outcome. |
| **Wait** | A node that holds a case until an event, a time or a condition, with an optional limit. |
| **Watch** | The read-only view of an agent's session on a step. |
| **Work item** | An item in someone's work or a queue: a step, a vote, an agent question or an escalation. |

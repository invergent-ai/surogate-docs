---
title: Decisions, rules, waits and parallel paths
sidebar:
  label: Decisions, rules and waits
---

Besides steps, a stage's flow holds nodes that Keel works through by itself. Add them with **Add step** on the board (pick the **Kind**) or **Add decision** in a stage's flow, and edit them in their panel. See [The Workflow tab](/keel/builder/workflow/) for the board and the flow.

Conditions in these nodes are written in CEL, the Common Expression Language, over the case type's field names. `now` is the current time. For example:

```
amount > 50000.0
over_limit && term_years <= 30
```

Keel keeps a condition exactly as you type it; the [dry run](/keel/builder/publish/) reports one it cannot read.

## Decisions

A decision sends the case down one branch. It never calls a model: it checks its branches' conditions against the case's data, in order, and takes the first that holds.

The panel has two sections:

- **Branches**: each with a **Condition**, a **Label** that people read (such as `Over the limit`), and **Goes to**. **Add branch** adds one; the × removes it. With none, "It has no branches: every case goes the other way."
- **Otherwise**: where a case goes when no branch holds (**Goes to**), and its **Label**, such as `Within the limit`.

**Goes to** offers the same places as a step's outcome. See [Allowed outcomes](/keel/builder/steps/#allowed-outcomes).

Decisions show in the stage's flow, not as cards on the board.

## Rules

A rule node runs one of the project's [decision tables or scorecards](/keel/builder/rules/) on the case's data, writes its results into fields, and goes on.

- **Rule**: pick the rule.
- **Assignments**: which of the rule's results goes to which field. Each row has a **Result**, the result's key as the rule writes it, and a **Field**. **Add assignment** adds a row. A scorecard's results are `score` and `reasons`.
- **Then**: where the case goes next.

The case uses the version of the rule in effect at that moment, unless the case type [pins](/keel/builder/case-type-settings/#pinned-rules) the rule: then each case uses the version in effect when it started.

If the rule cannot give an answer, such as a table with no matching row and no default, Keel refuses whatever led the case to it, such as the completion of the step before. The person sees **Keel could not apply a rule on this step. Ask your supervisor.**

## Waits

A wait holds the case until something happens. Its panel has three sections.

**Waits for** picks what ends the wait:

| Choice | Setting | The outcome it leaves by |
|---|---|---|
| **A time** | **How long**, a duration | Elapsed |
| **An event** | **Event**, the name of a [case event](/keel/builder/case-type-settings/#case-events) another system sends | Arrived |
| **A condition** | **Condition**: "It is checked each time the case changes." | Met |

**At most** sets a limit. When the limit passes first, the wait leaves by its **Deadline** outcome. When the case type has a calendar, these durations count business time: "Counted in business time, by the case type's calendar."

**Waiting on** says whom the case waits on: **The client**, **A third party** or **Inside the bank**. It shows in the business app, on the case list's tabs and on the case page. While a case waits on the client, its own service-level clock is paused.

**Outcomes** lists one outcome for each thing the wait waits for, each with a **Label** and where it **Leads to**. They come and go as you change **Waits for** and **At most**.

## Parallel splits and joins

A **parallel split** starts several paths at once. Its panel, **Starts in parallel**, lists where each path starts; the **Add** menu adds one. Steps on parallel paths are open at the same time, and their cards read `Parallel with` and the other paths.

A **join** waits until every path that leads to it has arrived, then goes on to its **Then**. A join needs at least two paths leading to it; the dry run reports one that could never fire.

A path can also stop on its own, with **End of this path**: the case goes on along its other paths. A case left open with nothing to do is refused, so every path must end somewhere a case can rest or close.

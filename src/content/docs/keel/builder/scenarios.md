---
title: The Scenarios tab
sidebar:
  label: Scenarios
---

A **scenario** is a stored test of a case type: given how a case starts and what happens to it, the path it should take and how it should end. Every dry run plays the scenarios of the case types a draft changes, and publishing needs every scenario to pass.

## The list

The left of the tab lists the case type's scenarios by name, each with how it did in the last dry run: **Passed**, **Failed** or **Not run**. Pick one to see it.

In a draft, editors and owners see:

- **New scenario**: asks for its name. "It is made in the draft. How the case starts, the steps played and what must hold come next."
- **Run**: dry-runs the draft, which plays every scenario, and updates their results.

With no draft open, the tab shows the published scenarios, read-only and not run.

## A scenario

A scenario has three sections. A failed one shows Keel's message under its name.

### Start

- **At**: when the case starts, in your time zone.
- **Data**: the case's data, as a JSON object, such as `{"applicant": "Ioana Popescu", "amount": "20000.00"}`.
- **Started by**: who starts it, a **Person**, an **Agent** or a **System**, with an **Id**.

### Steps

The things that happen to the case, in order. Steps count from 0. The **Add** menu under **Steps** picks the kind:

| Kind | What you fill in |
|---|---|
| **Complete a step** | The **Step**, its **Outcome**, its **Output** and **Sources** as JSON, and who did it (**Done by**; by default, the step's performer). |
| **Cast a vote** | The **Step**, the **Choice**, and who voted. |
| **Raise a hand** | The **Step**, the **Question**, the **Evidence**, and who raised it. |
| **Answer a hand** | The **Step**, the **Reply**, a **Note**, and who answered. |
| **Send an event** | The **Event**, its **Payload**, and who sent it (by default, no one). |
| **Start an action** | The **Action**, and who started it. |
| **Move the case** | Where it goes (**To**), the **Reason**, and who moved it. |
| **Let time pass** | A **Duration**, so timers and service levels can fire. |

Each step has an **At**: a time with its offset, or `+` and a duration after the step before, such as `+PT1M`. Blank means a minute after the step before.

### Expect

What must hold once the steps are played:

- **Path**: the nodes the case must pass through, in order. The **Add** menu adds one. Empty, it reads **Any path.**
- **Status**: **Any**, **Open** or **Closed**.
- **Resolution**: how the case closed, such as `approved`.
- **Data**: field values the case must hold, as a JSON object.
- **Rejections**: steps that Keel must refuse, each by its **Step** number and the refusal's **Code**, such as `authority`.

## Remove a scenario

**Remove scenario** asks first: "Its file is deleted from the draft."

## Test one step

In a step's panel, **Test this step** runs the dry run and lists only the scenarios whose path passes through that step. See [Steps](/keel/builder/steps/#the-panels-footer).

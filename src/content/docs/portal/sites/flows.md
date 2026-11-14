---
title: Logic flows
description: Short server logic with typed inputs and outputs, decisions and tests; called from action lists, by name or by contract.
---

A logic flow is a short piece of server logic. It takes typed inputs, works through its steps, and gives typed outputs. An [action list](/portal/sites/actions/) calls it, and gets the outputs back at once. Anything that waits for a person, a timer or an outside event is not a flow.

## What people see

Flows have no page of their own: a person sees only what the form, job or endpoint that calls them does with the outputs. Administrators see the portal's flows under [Flows](/portal/console/flows/) in the console, with each flow's inputs and outputs. **Run tests** runs the flow's tests and shows each one passing or failing:

![The Flows page with New value, New contract and New flow: the flow "Building permit fee" with its inputs and outputs, Edit, four tests marked Passed, and under Named values the permit fee rate, values.cotaTaxa, an expression kept for the whole portal for 3,600 seconds, with Edit.](../../../../assets/screenshots/portal-flows-tests.png)

## A flow

A flow has an id of lower-case letters, digits and hyphens, and a name. Flows are made and changed in the console, under [Flows](/portal/console/flows/#make-or-change-a-flow). Developers can also write them in the site's configuration: see [Developer: Logic flows](/portal/developer/flows/#a-flow).

**Inputs and outputs** are names with a type: `text`, `number`, `integer`, `boolean`, `list`, `object` or `any`. An input may be optional, which means it may be left out. A flow has at most 32 of each.

**Steps** have names, and the flow begins at its start step. A step is one of:
- a step that runs an action list, then goes to the next step;
- a decision: it goes to the first condition that holds, else to the step it names for when none does;
- an end: it gives the outputs, each worked out with an expression.

A flow has at most 100 steps. Every step must be reachable from the start, and an end must be reachable. Each end sets every output that is not optional.

Expressions in a flow read the flow's inputs, the person, the site, the language, the time, what the steps before kept, and [named values](/portal/sites/values/). A flow cannot tell the person something, send them elsewhere, or stop its caller's run; only the list that calls it can.

## Call a flow

An action list calls a flow by its id, and keeps its outputs for the actions after it. The inputs are checked against the flow's types when the call runs. If the flow fails, the calling action fails with the message `Flow <id>: …`, and the list's error handling can catch it. Flows can call other flows, at most 8 deep. A flow's steps count toward the run's 10 seconds and 10,000 steps.

In the console, **Run a logic flow** calls one from any action list: a form's [steps](/portal/console/forms/#steps), an endpoint's or a job's actions, or another flow's. Developers can also write it in the site's configuration: see [Developer: Logic flows](/portal/developer/flows/#call-a-flow).

## Contracts

A contract is a shared set of inputs and outputs. A flow can implement a contract: it then takes the contract's inputs and outputs, and does not write its own. A caller can then pick one of the contract's flows with an expression that gives a flow's id. If no such flow implements the contract, the action fails, and no other flow runs.

Contracts are made and changed in the console, under [Flows](/portal/console/flows/#make-or-change-a-contract), and a flow follows one under **Follows a contract**. Developers can also write them in the site's configuration: see [Developer: Logic flows](/portal/developer/flows/#contracts).

## Tests

A flow carries its own tests, at most 50. Each test has a name, the inputs to run with, and what it expects:
- the outputs: each one listed must be exactly what is given;
- or a failure: the flow must fail.

A test can also give a person, with an id, a name, an email and roles, for a flow that reads the person. A test never reaches out: it gives the answers to the flow's web calls, and its emails are listed, never sent ([In tests](/portal/sites/connectors/#in-tests)). It never touches the portal's files or content either:
- it gives the test folders of its own, with files of text;
- it gives named values their value for the test;
- a collection value the test does not give is left out. Every value the flow reads is worked out afresh for the test. A test that runs out of time fails, whatever it expects.

Tests run from the console, under [Flows](/portal/console/flows/), and when a site is [checked](/portal/developer/check-a-site/): each failing test is reported against its flow. The tests themselves are written with the flow. For now, this is set in the site's configuration: see [Developer: Logic flows](/portal/developer/flows/#tests).

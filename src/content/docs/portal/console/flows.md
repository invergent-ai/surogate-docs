---
title: Flows
description: The logic flows, contracts and named values the portal runs, and running each flow's tests.
---

**Flows** shows administrators the [logic flows](/portal/sites/flows/), contracts and [named values](/portal/sites/values/) the portal runs now. This page shows them, runs their tests, and makes and changes flows: see [Make or change a flow](#make-or-change-a-flow). Contracts and named values are still written in the site's configuration: see [Developer: Logic flows](/portal/developer/flows/).

## Logic flows

Each flow shows its name and id, the contract it implements, and its inputs and outputs as `name: type` (a `?` marks an optional one).

## Run tests

**Run tests** runs the flow's tests one after another, and lists each as **Passed** or **Failed**, with why it failed. **Open** shows the outputs it gave and its log. The tests of one flow stop after 30 seconds; those left are listed as not run. A flow without tests cannot be run from here.

## Make or change a flow

**New flow** makes one and **Edit** opens one. A flow whose file has problems, or that was written by hand in a shape the console cannot draw, is listed under **Flows not running**, with **Edit**. The editor has three tabs:

- **Settings:** the id (lower-case letters, digits and hyphens, fixed once saved), the name and description in each language, and **Follows a contract**: a contract's inputs and outputs, or the flow's own. Its own **Inputs** and **Outputs** are rows: a name like a variable's, a type, whether it **May be left out**, and a note.
- **Steps:** **Starts at** names the first step. The map shows how the steps lead to each other, in columns from the start; a step nothing leads to stands apart, under **Nothing leads here**. Click a step, on the map or in the list, to open it:
  - its name: change it, and every step that leads to it follows;
  - its type: **Actions**, **Decision** or **End**;
  - **Actions** runs an action list, built as a form's [steps](/portal/console/forms/#steps) are, and **Then** names the step after it;
  - **Decision** has ways, each an **If** condition and the step to **go to**, and **Otherwise**, the step when no way holds; with none, the flow fails;
  - **End** gives each output with an expression; a `*` marks one it must give.

  **Add a step** adds one of the type chosen. Removing a step leaves what led to it naming a step that is gone, said at each, to be chosen again.
- **Tests:** the flow's tests, each with what it expects. Renaming an input or an output carries the new name into the tests and the ends. A test can be removed here; tests are still written in the site's configuration.

![The flow Building permit fee's Steps tab: Starts at verifica, and the map: the decision verifica leads to four action steps, invalid, standard, anexa and comercial, which all lead to calcul, then to the end final. Under the map, the steps listed one by one.](../../../../assets/screenshots/portal-flow-edit.png)

Each problem is said at its field as you type, and **Save** waits until there are none; above the tabs, the editor says what it still needs and which tabs have problems. A problem in another file, such as an endpoint calling the flow without an input it now needs, is listed above the tabs with that file's name. **Remove** takes the flow away, after asking.

## Contracts and values

**Contracts** lists each contract's inputs and outputs. **Named values** lists each value with what it is (an expression or a flow's outputs), for whom it is kept, and for how long.

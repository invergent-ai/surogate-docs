---
title: Flows
description: The logic flows, contracts and named values the portal runs, and running each flow's tests.
---

**Flows** shows administrators the [logic flows](/portal/sites/flows/), contracts and [named values](/portal/sites/values/) the portal runs now. They are written in the portal's files; this page shows them and runs their tests.

## Logic flows

Each flow shows its name and id, the contract it implements, and its inputs and outputs as `name: type` (a `?` marks an optional one).

## Run tests

**Run tests** runs the flow's tests one after another, and lists each as **Passed** or **Failed**, with why it failed. **Open** shows the outputs it gave and its log. The tests of one flow stop after 30 seconds; those left are listed as not run. A flow without tests cannot be run from here.

## Contracts and values

**Contracts** lists each contract's inputs and outputs. **Named values** lists each value with what it is (an expression or a flow's outputs), for whom it is kept, and for how long.

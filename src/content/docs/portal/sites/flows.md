---
title: Logic flows
description: Short server logic with typed inputs and outputs, decisions and tests; called from action lists, by name or by contract.
---

A logic flow is a short piece of server logic, written in the portal's files. It takes typed inputs, works through its steps, and gives typed outputs. An [action list](/portal/sites/actions/) calls it, and gets the outputs back at once. Anything that waits for a person, a timer or an outside event is not a flow.

## A flow

A flow lives in `flows/<id>.yaml`. The id is lower-case letters, digits and hyphens.

```yaml
name:
  ro: Preț cu TVA
  en: Price with VAT
inputs:
  amount: { type: number }
  vip: { type: boolean, optional: true }
outputs:
  total: { type: number }
start: check
steps:
  check:
    type: decide
    when:
      - if: has(inputs.vip) && inputs.vip
        go: free
    otherwise: compute
  compute:
    type: actions
    actions:
      - type: set
        values:
          total: inputs.amount * values.vatRate
    next: done
  done:
    type: end
    outputs:
      total: vars.total
  free:
    type: end
    outputs:
      total: "0.0"
tests:
  - name: plain
    inputs: { amount: 100 }
    expect: { outputs: { total: 119 } }
  - name: vip
    inputs: { amount: 100, vip: true }
    expect: { outputs: { total: 0 } }
```

**Inputs and outputs** are names with a type: `text`, `number`, `integer`, `boolean`, `list`, `object` or `any`. Add `optional: true` when one may be left out. A flow has at most 32 of each.

**Steps** have names, and the flow begins at `start`. A step is one of:
- `actions`: runs an action list, then goes to `next`;
- `decide`: goes to the first `when` whose `if` holds, else to `otherwise`;
- `end`: gives the outputs, each worked out with an expression.

A flow has at most 100 steps. Every step must be reachable from the start, and an end must be reachable. Each end sets every output that is not optional.

Expressions in a flow read `inputs`, `user`, `site`, `locale`, `now`, `vars` and [named values](/portal/sites/values/) as `values.<name>`. A flow cannot tell the person something, send them elsewhere, or stop its caller's run; only the list that calls it can.

## Call a flow

An action list calls a flow with `callFlow`:

```yaml
- type: callFlow
  flow: price-with-vat
  inputs:
    amount: form.amount
  into: price
- type: message
  text:
    ro: "De plată: {{ vars.price.total }} lei"
    en: "To pay: {{ vars.price.total }} lei"
```

The outputs land in `vars.<into>`. The inputs are checked against the flow's types when the call runs. If the flow fails, the calling action fails with the message `Flow <id>: …`, and its `onError` can catch it. Flows can call other flows, at most 8 deep. A flow's steps count toward the run's 10 seconds and 10,000 steps.

## Contracts

A contract is a shared set of inputs and outputs, in `contracts/<id>.yaml`:

```yaml
name:
  ro: Preț
  en: Pricing
inputs:
  amount: { type: number }
outputs:
  total: { type: number }
```

A flow that says `implements: pricing` takes the contract's inputs and outputs, and does not write its own. A caller can then pick one of the contract's flows with an expression:

```yaml
- type: callFlow
  contract: pricing
  pick: '"price-" + form.plan'
  inputs:
    amount: form.amount
  into: price
```

`pick` gives a flow's id. If no such flow implements the contract, the action fails, and no other flow runs.

## Tests

A flow carries its own tests, at most 50. Each test has a `name`, the `inputs` to run with, and what it expects:
- `expect: { outputs: { … } }`: each listed output must be exactly this;
- `expect: { fails: true }`: the flow must fail.

A test can also give a `user`, with `id`, `name`, `email` and `roles`, for a flow that reads the person. Every value the flow reads is worked out afresh for the test. A test that runs out of time fails, whatever it expects.

Tests run from the console, under [Flows](/portal/console/flows/), and when you [check a site](/portal/sites/check-a-site/): each failing test is reported against its flow. Add `--no-flow-tests` to leave them out.

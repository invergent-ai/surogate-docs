---
title: Actions
description: Lists of actions that run when something happens, such as a form being sent; values worked out with CEL expressions.
---

An action list is a short program written in the portal's files. It runs when something happens. For now that is a form being sent ([After it is sent](/portal/sites/forms/#after-it-is-sent)); later, endpoints, flows and scheduled jobs run them too. Each action does one thing: works out a value, logs a line, tells the person something, sends them elsewhere.

## An action list

```yaml
actions:
  submitted:
    - type: set
      values:
        reference: '"REQ-" + string(now.getFullYear()) + "-" + form.county'
    - type: log
      level: info
      message: '"Request " + vars.reference'
    - type: message
      text:
        ro: "Cererea {{ vars.reference }} a fost primită."
        en: "Request {{ vars.reference }} was received."
```

Every action has a `type`, and may also have:
- `description`: a note for whoever reads the file;
- `condition`: an expression that must be true for the action to run;
- `onSuccess`: actions run after it succeeds;
- `onError`: actions run when it fails; the list then goes on;
- `then: stop`: the run ends after this action; `then: continue` lets a `message` or `redirect` go on;
- `errorMessage`: what the person is told if the run fails at this action, in each language.

## Expressions

Values are worked out with [CEL](https://cel.dev), the expression language Keel uses too. An expression can read:

| Name | What it holds |
|---|---|
| `form` | What was sent, by field key |
| `submission` | `id`: the submission's id |
| `user` | The person who sent it (`id`, `name`, `email`, `roles`), or `null` for a visitor |
| `site`, `locale` | The site and the language |
| `now` | When the run started |
| `vars` | The values earlier actions set |

Whole numbers are integers, the others decimals. Reading a field that was not sent is an error; check it first with `has(form.phone)`. Beside CEL's own functions there are `replace(text, a, b)`, `urlEncode(text)`, `slice(list or text, from, to)`, `sort(list)`, `round`, `floor` and `ceil`.

## The actions

| Type | What it does | Takes |
|---|---|---|
| `set` | Works out values into `vars` | `values: { name: expression }` |
| `group` | Runs actions together; its `onError` catches theirs | `actions` |
| `each` | Runs actions for each item of a list | `list`, `as`, `actions` |
| `repeat` | Runs actions a number of times | `times`, `as` (the count), `actions` |
| `throw` | Fails with a message | `message` |
| `stop` | Ends the run | |
| `log` | Writes a line in the run's log | `level` (`info` or `warn`), `message` |
| `wait` | Waits up to 5 seconds | `ms` |
| `parseJson` | Reads JSON text into a value | `from`, `into` |
| `toJson` | Writes a value as JSON text | `from`, `into` |
| `message` | Tells the person something, and ends the run | `text`, in each language |
| `redirect` | Sends the person to another page, and ends the run | `to` |

A `redirect` goes to a page of the same site, or to another https site the form names under `redirects`.

## When something fails

An action that fails runs its `onError` actions, and the list goes on. Without them, the failure goes up to the enclosing group's `onError`, and otherwise ends the run. Inside `onError`, `vars.error.message` says what went wrong.

A run stops after 10 seconds or 10,000 steps, and a loop goes over at most 1,000 items. Each run is kept for 30 days, with its log; reviewers see them under **Runs** on [Forms](/portal/console/forms/#runs).

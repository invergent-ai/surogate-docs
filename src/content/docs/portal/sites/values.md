---
title: Named values
description: Values worked out once and kept for a while, per portal, site or person, that action lists and flows read by name.
---

A named value is a value worked out by the portal and read by name, as `values.<name>`, in any [action list](/portal/sites/actions/) or [logic flow](/portal/sites/flows/). A VAT rate, a greeting, a price list from a flow: each is written once and kept for a while.

## A value

A value lives in `values/<name>.yaml`. The file's name is the value's name: letters, digits and `_`, starting with a lower-case letter.

```yaml
name:
  ro: Cota TVA
  en: VAT rate
cache: install
ttl: 3600
value: "1.19"
```

A value is either:
- `value`: an expression;
- `flow`: a flow's outputs, with `flow: { id, inputs }`. Read one output as `values.<name>.<output>`.

## How long it is kept

`cache` says for whom a value is kept, and `ttl` how many seconds (1 to 86,400; 300 when left out):

| `cache` | Kept for | Its expression may read |
|---|---|---|
| `install` | The whole portal | `locale`, `now`, other `install` values |
| `site` | Each site | as above, and `site` and `site` values |
| `user` | Each signed-in person | as above, and `user` and `user` values |
| `none` | Nobody: worked out every time | everything above |

A value is kept per language too. A value kept for a site or the whole portal never sees the person, even inside a flow it calls: what it keeps is the same for everyone. A value cannot read a value kept for fewer people than it is, and values cannot read each other in a circle. The portal refuses either when the file is saved. A `user` value is never kept for visitors.

Kept values start afresh whenever the portal's files change.

## When a value fails

Every value a list can reach is worked out before the list runs, each after the values it reads. A value that fails is left out, and the run's log says why. Reading it is then the action's error, which its `onError` can catch.

Values are read as `values.<name>`. Any other way, such as `values["name"]`, is refused when the file is saved.

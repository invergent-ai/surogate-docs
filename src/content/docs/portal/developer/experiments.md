---
title: Experiments
description: Experiments in experiments/<id>.yaml, and the placements that are their versions, as the site's configuration writes them.
---

What these do is on [Experiments](/portal/sites/experiments/).

## An experiment's file

```yaml
# experiments/taxes-banner.yaml
name: { ro: Banner taxe, en: Taxes banner }
status: running            # draft (when left out), running or ended
started: 2026-11-16T10:00:00Z
variants:
  - { id: blue, name: { ro: Albastru, en: Blue } }
  - { id: green, name: { ro: Verde, en: Green }, weight: 1 }
goal: { page: { site: main, path: /plata } }   # or goal: { form: contact }
# winner: green            # only when ended
```

- `variants`: 2 to 5; `id` lower-case letters, digits and hyphens (up to 31), unique; `weight` 1 to 100, 1 when left out. The first is the control.
- `started` is written by the console's **Start**: results count only who saw it since.
- `winner` only with `status: ended`, one of the variants.
- At most 20 experiments.

## A placement that is a version

```yaml
regions:
  main:
    - id: banner-blue
      app: portal
      widget: group
      experiment: { id: taxes-banner, variant: blue }
      blocks: [...]
    - id: banner-green
      app: portal
      widget: group
      experiment: { id: taxes-banner, variant: green }
      blocks: [...]
```

## Load checks

- An experiment's problems are `experiment` with a reason: `name`, `status`, `variants`, `variant`, `weight`, `winner`, `started`, `goal`, `goal_site`, `goal_page`, `goal_form`, `goal_on_page` (the goal page carries the experiment).
- A placement naming an experiment or a variant there is not: `unknown_experiment`. More than 20 experiments: `too_many_experiments`.

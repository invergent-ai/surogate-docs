---
title: KPIs
description: A model's kpis, the kpis widget on a page, and the page of figures a model makes.
---

The configuration behind [KPIs](/portal/sites/kpis/). That page covers what the figures show and who sees which.

## KPIs in a model's file

KPIs go in the model's file. A KPI counts the records or works out a sum, an average, a least or a most; it can keep only some records, split them by a field, or follow them over time. A model has at most 12 KPIs, each with its own `id`.

In `models/<id>.yaml`, next to the model's fields:

```yaml
kpis:
  - id: total
    label: { ro: Cereri, en: Requests }
    measure: count
  - id: fees
    label: { ro: Taxe încasate, en: Fees collected }
    measure: sum
    field: fee
    where: { status: approved }
  - id: byStatus
    label: { ro: Pe stări, en: By status }
    measure: count
    by: status
  - id: monthly
    label: { ro: Pe luni, en: By month }
    measure: count
    period: month
```

- **`measure`:** `count`, `sum`, `avg`, `min` or `max`. Everything but a count names its `field`, a number or an amount.
- **`where`:** keeps only the records whose filterable fields have these values, at most 5 of them.
- **`by`:** makes bars, one for each value of a filterable text or yes-or-no field. The 10 largest are shown; records with no value make a bar of their own, "—".
- **`period`:** makes bars over the last 12 days, weeks, months or years, up to the current one. Weeks start on Monday, and periods follow UTC. `on` names the date they count by: a date field, a date and time field, or `created_at` (the default).
- A model has at most 12 KPIs, each with its own `id`.

## The kpis widget on a page

The portal's `kpis` widget shows a model's KPIs, all of them or the ones named. In a region of a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
- id: figures
  app: portal
  widget: kpis
  preferences: { model: requests, kpis: [total, monthly] }
```

- `model`: the model whose KPIs it shows.
- `kpis`: the ones to show, by their `id`; all of them when left out.

## A page of figures from the model

A model can also make its own page of KPIs on a site, as it makes [its own pages](/portal/developer/listings/#a-models-own-page). In the model's file:

```yaml
dashboards:
  - site: main
    path: /requests/figures
    title: { ro: Indicatori, en: Figures }
```

- `site` and `path`: where the page is.
- `title`: the page's title, in both languages.

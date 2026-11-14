---
title: Listings
description: The listing widget in a page's file, and the pages a model makes for itself.
---

The configuration behind [Listings](/portal/sites/listings/). That page covers what people see in a listing, and what each person may do in it.

## A listing on a page

A listing is the portal's `listing` widget. In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: requests
      app: portal
      widget: listing
      preferences:
        model: requests
        columns: [subject, status, amount]
        filters: [status]
        add: true
        edit: true
        delete: false
```

- `model`: the model whose records it shows.
- `columns`: the fields shown, at most 8; links are not shown in columns. Left out, the title and up to 3 more fields.
- `filters`: filterable fields to filter on, by exact value: text, numbers, dates, yes or no.
- `add`, `edit`, `delete`: whether the listing offers them. The model's [permissions](/portal/sites/data-models/#who-may-do-what) still decide who may.

## A model's own page

A model can make its own page on a site, with a listing that offers everything. In the model's file (`models/<id>.yaml`):

```yaml
pages:
  - site: main
    path: /requests/register
    title: { ro: Registrul cererilor, en: Request register }
```

- `site` and `path`: where the page is.
- `title`: the page's title; the model's name when left out.
- A `path` that a written page already has is refused.

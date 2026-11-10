---
title: Listings
description: A data model's records on a page, searchable, filterable and sortable, with add, edit and delete in place.
---

A listing shows the records of a [data model](/portal/sites/data-models/) on a page, as a table. People see the records they may see, search and filter them, open one, and, where they may, add, edit and delete them in place.

## Place a listing

A listing is the portal's `listing` widget:

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
- `add`, `edit`, `delete`: whether the listing offers them. The model's [permissions](/portal/sites/data-models/#who-may-do-what) still decide who may: someone who may only edit their own records sees **Edit** only on theirs.

A search box shows when the model has searchable fields. Sortable columns sort when their heading is clicked. A listing shows 20 records, and **Load more** brings the next ones.

## What each person sees

- Everyone sees only the records they may see: their own, where that is all they may see.
- Someone who may neither see the records nor add any sees nothing of the listing.
- Adding, editing and deleting are offered only to people signed in, never to visitors.
- Values show as text; dates and times in the person's own time; web addresses as links only when they are http, https or mailto.

**Open** shows a record's details below the list, with the title of the records it links to when the person may see them. Its address can be shared: `?p_<placement id>_record=<record id>`. Search engines are told not to keep such addresses.

**Add** and **Edit** open a small form with the model's fields. A link is chosen with **Choose**, from a list of the linked model's records, as a form's [record field](/portal/sites/forms/#pick-a-record) does. A change sends only what was changed. A value the model refuses is shown with its field.

## A model's own pages and form

A model can make its own page on a site, with a listing that offers everything:

```yaml
pages:
  - site: main
    path: /requests/register
    title: { ro: Registrul cererilor, en: Request register }
```

The title is the model's name when left out. A path that a written page already has is refused.

Each model also has its own form, `model-<id>` (an `_` in the id becomes `-`), to place like any [form](/portal/sites/forms/): one field for each of the model's fields, links as [record fields](/portal/sites/forms/#pick-a-record), sent to a new record. Who may send it is who may add records: with `add: [everyone]`, visitors too, even where the form is placed on no page. The record holds what was sent; the form keeps its own copy for a day only.

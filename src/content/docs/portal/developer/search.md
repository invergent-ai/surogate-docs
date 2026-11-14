---
title: Search
description: The search widget in a page's file, the DMS section, search.yaml, and the call from an app.
---

The configuration behind [Search](/portal/sites/search/). That page covers what a site's search finds, how words match, and who finds what.

## A search box on a page

In a page's file, the search box is the portal's `search` widget (`sites/<site>/pages/<page>.yaml`):

```yaml
- id: search
  app: portal
  widget: search
  preferences: { limit: 10 }
```

- `limit`: how many results a page of results shows, from 1 to 50 (10 when left out).

## Documents of the DMS in the search box

A search box shows the documents of the [DMS](/portal/sites/documents/) that match, beside the site's own results, when it has `documents`. In a region of a page's file:

```yaml
regions:
  main:
    - id: search
      app: portal
      widget: search
      preferences:
        limit: 10
        documents: { limit: 5 }
```

- `documents.limit`: how many of the DMS's documents the section shows, 1 to 10; 5 when left out.

## Tune search in `search.yaml`

Administrators set the same on the console's [Search](/portal/console/search/) page. In the site's files it is `sites/<site>/search.yaml`:

```yaml
weights: { title: 3, body: 1 }
synonyms:
  ro: ["primărie, consiliu local"]
pinned:
  - { query: taxe, paths: [/taxe, /plata-online] }
exclude: { paths: [/intern/*], types: [memo] }
fuzzy: true
wildcard: false
```

- `weights`: how much a word found in a title counts against one found in the text, each from 1 to 10; the portal's own are 3 and 1.
- `synonyms`: for each language, groups of words or phrases that mean the same, separated by commas.
- `pinned`: for a search (`query`), up to five addresses (`paths`) shown first, in that order.
- `exclude`: `paths` to leave out, where `/intern/*` leaves out `/intern` and everything under it, and content `types` search never finds.
- `fuzzy`: a word with a typo counts; on by default.
- `wildcard`: a word ending in `*` finds every word it starts, with three letters at least; off by default.

## From an app

An app's backend searches a site through the SDK, as a visitor finds it:

```ts
const found = await portal.search({ q: "taxe locale", site: "main", locale: "ro" });
```

Each result has a `title`, a `url` on the portal's address, the `kind` and, for content, its `type`; the `snippet` is escaped HTML with the words found in `<mark>`. An app's searches are not counted in [what people search for](/portal/console/search/#what-people-search-for).

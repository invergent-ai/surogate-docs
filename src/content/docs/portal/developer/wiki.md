---
title: Wikis and knowledge bases
description: The wiki widget on a page, with its kind, who writes and the article it opens on.
---

The configuration behind [Wikis and knowledge bases](/portal/sites/wiki/). That page covers what people see, reading, writing, looking after a wiki and knowledge bases.

## A wiki on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: wiki
      app: portal
      widget: wiki
      preferences: { kind: wiki, edit: members, home: home }
```

- `kind`: `wiki` (when left out), or `knowledge` for a knowledge base.
- `edit`: who writes a wiki: `members` (when left out), everyone signed in who may [see the widget](/portal/sites/permissions/), or `editors`, the site's editors only. A knowledge base is always written by the site's editors.
- `home`: the address of the article the wiki opens on (`home` when left out).

The articles belong to the widget: moving it to another page, or giving it another `id`, leaves them behind, and they come back if it returns.

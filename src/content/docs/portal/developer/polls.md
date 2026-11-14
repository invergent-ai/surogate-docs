---
title: Polls
description: The poll widget in a page's file, and its time zone.
---

The configuration behind [Polls](/portal/sites/polls/). What people see, and how polls are opened, voted on and closed, is on that page.

## A poll on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  aside:
    - id: question
      app: portal
      widget: poll
      preferences: { zone: Europe/Bucharest }
```

- `zone`: the time zone a poll's closing time is read in, such as `Europe/Bucharest` (when left out).

---
title: Forums and Q&A
description: The forum widget on a page, with its kind, moderation and list length.
---

The configuration behind [Forums and Q&A](/portal/sites/forums/). That page covers what people see, topics and answers, questions and answers, moderation and limits.

## A forum on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: forum
      app: portal
      widget: forum
      preferences: { kind: questions, moderation: after, limit: 20 }
```

- `kind`: `discussion` (when left out) for topics people talk about, or `questions` for questions and their answers. Changing it later changes the topics started afterwards; each topic keeps the kind it was started with.
- `moderation`: `after` (when left out) publishes a topic or an answer as soon as it is written; `before` keeps it waiting until a moderator approves it.
- `limit`: how many topics a page of the list shows (1 to 50; 20 when left out).

The topics belong to the widget where they were started. Moving the widget to another page, or giving it another `id`, leaves its topics behind: they come back if it returns.

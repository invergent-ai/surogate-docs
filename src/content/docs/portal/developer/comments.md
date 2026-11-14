---
title: Comments and ratings
description: The comments and rating widgets on a page, and their moderation and limit.
---

The configuration behind [Comments and ratings](/portal/sites/comments/). That page covers what people see, writing and answering, naming someone, flags, limits and what happens to comments later.

## Comments and a rating on a page

In a page's file (`sites/<site>/pages/<page>.yaml`), such as the display page of a content type:

```yaml
regions:
  main:
    - id: rating
      app: portal
      widget: rating
    - id: comments
      app: portal
      widget: comments
      preferences: { moderation: before, limit: 20 }
```

- `moderation`: `after` (when left out) publishes a comment as soon as it is written; moderators hide or delete it later. `before` keeps it waiting until a moderator approves it.
- `limit`: how many comments the widget shows, newest first, each with its answers (1 to 100; 50 when left out). Older comments are not shown.
- The `rating` widget takes no preferences.

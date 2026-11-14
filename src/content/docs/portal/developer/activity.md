---
title: Activity
description: The activity widget on a page, with its moderation, limit and what it shows.
---

The configuration behind [Activity](/portal/sites/activity/). That page covers what people see, posts, the comments and entries it lists, and who is told what.

## The widget on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: activity
      app: portal
      widget: activity
      preferences: { moderation: after, limit: 20, show: [posts, comments, entries] }
```

- `moderation`: `after` (when left out) publishes a post as soon as it is written; moderators hide or delete it later. `before` keeps it waiting until a moderator approves it.
- `limit`: how many things the widget shows, newest first (1 to 50; 20 when left out). Older ones are not shown.
- `show`: what it shows, each named once (all three when left out):
  - `posts`: what people write on this widget, with a form to write;
  - `comments`: comments written on the site;
  - `entries`: entries published on the site.

A widget whose `show` leaves out `posts` takes none.

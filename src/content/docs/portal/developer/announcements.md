---
title: Announcements
description: The announcements widget on a page, with how many it shows and the time zone of its days and times.
---

The configuration behind [Announcements](/portal/sites/announcements/). That page covers what people see, reading and dismissing, how editors write announcements and tell people by a notification.

## The widget on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: notices
      app: portal
      widget: announcements
      preferences: { limit: 3, zone: Europe/Bucharest }
```

- `limit`: how many announcements the widget shows at once, 1 to 10 (3 when left out).
- `zone`: the time zone the editors' days and times are read in, such as `Europe/Bucharest` (when left out).

Announcements belong to the site, not to the widget: every `announcements` widget on the site shows the same ones, so a site can place it on its home page and on any other.

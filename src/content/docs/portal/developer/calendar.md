---
title: Calendars
description: The calendar widget on a page, with who adds events, its time zone and what it opens on.
---

The configuration behind [Calendars](/portal/sites/calendar/). That page covers what people see, how events are read and added, and the calendar feed.

## A calendar on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: events
      app: portal
      widget: calendar
      preferences: { edit: editors, zone: Europe/Bucharest, view: month }
```

- `edit`: who adds events: `editors` (when left out), the site's editors and those who [edit the page](/portal/sites/permissions/), or `members`, everyone signed in who may see the widget.
- `zone`: the time zone the calendar shows its times in, such as `Europe/Bucharest` (when left out) or `UTC`.
- `view`: what the calendar opens on: `month` (when left out), or `agenda`, the list of what is coming.

The events belong to the widget: moving it to another page, or giving it another `id`, leaves them behind, and they come back if it returns.

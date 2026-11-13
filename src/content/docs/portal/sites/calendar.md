---
title: Calendars
description: Give a page a calendar of events its editors or members keep, which people add to their own calendar apps.
---

The portal's `calendar` widget is a calendar of events: a month at a time or a list of what is coming, each event with its own page, and a feed people add to their own calendar apps.

## Place a calendar

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

Each `calendar` widget is a calendar of its own. Its events belong to the widget: moving it to another page, or giving it another `id`, leaves them behind, and they come back if it returns. A page with a calendar is made for each person and never kept in a cache.

## Read it

**Month** shows a month as a grid of weeks, Monday first, with **Previous month** and **Next month**; an event that lasts several days shows on each of them. **Coming up** lists the next 50 events within a year. Every time is in the calendar's time zone, which the calendar names.

An event's page shows when it starts and ends, where it is, its description, how it repeats and, for an event that repeats, when it happens next. **Add to my calendar** downloads the event as a file calendar apps open.

## Add events

Those who may add events see **New event**. An event has a title of up to 200 characters, a place of up to 200 and a description of up to 5,000; it starts and ends on a day and at a time, or lasts whole days with **All day**, and lasts at most a year.

An event can repeat daily, weekly, monthly or yearly, every 1 to 99 days, weeks, months or years: for ever, until a day, or a number of times, at most 1,000. It keeps its time of day when the clocks change. A monthly event on the 31st skips the months without one; a yearly one on 29 February happens in leap years. **Skip a day** leaves out one of its days and keeps the rest.

On a calendar its members write, each person changes and deletes only the events they added; the editors change any. Deleting an event deletes all its repeats, once its writer ticks that they know it. When two people change the same event and the second saves after the first, the second save is refused, and what they wrote is kept as their draft. Any save the calendar refuses keeps the form the same way, for a week.

Each person adds at most 60 events an hour, and a calendar holds at most 5,000.

## Add it to a calendar app

**Subscribe (iCal)** gives the calendar's address for calendar apps: Google Calendar, Outlook or Apple Calendar add it as a subscription, and show its events from a year back to two years ahead, checking again every hour. The address opens for everyone who may see the page: anyone at all on a public page.

On a page only some people may see, a calendar app cannot sign in. Its editors then use **Share by a private address**: the portal shows an address once, which opens the calendar for anyone who has it. Keep it as you would a password. **Make another private address** ends the old one; **Stop sharing** ends it without a new one.

## What happens to them later

When a person is erased from the portal, the events they added stay on the calendar, without their name, and their drafts go. The events they added are part of what they get when they ask for their data.

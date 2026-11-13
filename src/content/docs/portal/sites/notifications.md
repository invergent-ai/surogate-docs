---
title: Notifications
description: Tell people of the portal something from a form or a job; they find it on the site, in the console, by email and in their browsers when they choose.
---

A notification tells one person something: a title, a few words, and a page of the portal it leads to. A form or a job sends it, for example to tell the clerks that someone wrote to the city hall. A notification is kept for 90 days; each person keeps their newest 500.

## Where people find them

**On the site.** A page can show a person's notifications. The heading counts the ones they have not read; opening one marks it read and goes to its page.

![The notifications widget on a site page: "Notifications 2", with two messages, each with its title, its words and when it came.](../../../../assets/screenshots/portal-notifications-widget.png)

Only people signed in see theirs. Visitors see nothing, and neither does an administrator seeing the portal as someone else.

**In the console.** The bell at the bottom of the menu shows how many are unread. Press it to read them, open one, or **Mark all read**.

![The console with the notifications panel open: two new messages and the Mark all read button. The bell at the bottom of the menu shows 2.](../../../../assets/screenshots/portal-notifications-bell.png)

**By email and in the browser.** On [My account](/portal/console/account/#notifications), everyone chooses whether their notifications also come by email, and turns on notifications in the browser they use.

![The Notifications section of My account: the switch for email and the notifications in this browser.](../../../../assets/screenshots/portal-account-notifications.png)

- **By email.** It is off until the person turns it on. The email has the notification's title as its subject, and its words and link. It goes only when the install sends email, and within the portal's hourly allowance of email; when it sends none, the switch is off and says so, as above.
- **[In the browser](/portal/console/account/#notifications-in-this-browser).** Each notification also appears on that device as the browser's own notification, with its title and words; clicking it opens the notification's page and marks it read. It goes only when the install sends notifications to browsers, through the browsers' own push services.

## Send one

The `sendNotification` action sends one, from a [form](/portal/sites/forms/)'s actions or a [job](/portal/sites/jobs/). It says whom it goes to, a title, some words and a page to open: see the [config example](#config-example). Like `email`, it is sent once the run ends well: a run that fails tells no one, and neither does its `onError` list.

Whom it goes to: people of the portal, by their id or their email, and groups. Names that are no one of the portal's (another portal's people, service accounts, people disabled, unknown emails) are passed by, saying nothing. A notification reaches at most 100 people; past that, the rest are left out.

A run sends at most 5 notifications; a run for a visitor, such as a public form sent by someone not signed in, at most 2. Visitors' runs share an allowance of 200 notifications an hour, one form or job sends at most 1,000 an hour, and a portal at most 5,000. An endpoint sends no notifications.

A job can also ask an [agent](/portal/sites/actions/#ask-an-agent) and send its answer to the people concerned.

## Config example

### A form's message, to the clerks

In a form's actions (`forms/<id>.yaml`, under `actions`), or a job's:

```yaml
- type: sendNotification
  to: "['group:7c1e9a52-3b4d-4e5f-8a6b-1c2d3e4f5a6b', 'clerk@primaria.ro']"
  title: "'New request from ' + form.name"
  body: "'Request ' + form.subject + ' waits for a review.'"
  link: "'/cereri'"
```

Each value is an [expression](/portal/sites/actions/): the outer quotes are the file's, the inner `'…'` are text, and `form.name` is what the person typed in the form's `name` field.

- `to`: whom it goes to, as one name or a list: a person's id, their email, or `group:` and a group's id.
- `title`: the title, up to 200 characters.
- `body`: the words, up to 2,000 characters. Optional.
- `link`: a page of the portal, a path such as `/cereri/42` or `/_portal/admin/proposals`. A link to another site is refused when the portal checks the files, and passed by when it is made as the run goes. Optional.

### An agent's answer, as a notification

In a job (`jobs/<id>.yaml`):

```yaml
actions:
  - type: askAgent
    agent: helper
    task: summary
    prompt: '"Request: " + string(trigger.after.description)'
    into: summary
  - type: sendNotification
    to: "trigger.after.owner"
    title: "'Summary of your request'"
    body: "vars.summary.text"
    link: "'/cereri/' + string(trigger.id)"
```

### The widget on a page

In a page's file (`sites/<site>/pages/<page>.yaml`), or in a layout region every page has:

```yaml
regions:
  aside:
    - id: notifications
      app: portal
      widget: notifications
      preferences: { limit: 5 }
```

- `limit`: how many of the newest it shows, 1 to 20; 5 when left out.

A page with the widget is made for each person and never kept in a cache.

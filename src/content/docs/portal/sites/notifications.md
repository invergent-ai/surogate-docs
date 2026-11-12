---
title: Notifications
description: Tell people of the portal something from a form or a job; they find it on the site, in the console, and by email when they choose.
---

A notification tells one person something: a title, a few words, and a page of the portal it leads to. People find theirs in three places: the notifications widget on a site's pages, the bell in the console, and their mailbox, when they chose email on **My account**. A notification is kept for 90 days; each person keeps their newest 500.

## Send one

The `sendNotification` action sends one, from a [form](/portal/sites/forms/)'s actions or a [job](/portal/sites/jobs/). Like `email`, it is sent once the run ends well: a run that fails tells no one, and neither does its `onError` list.

```yaml
- type: sendNotification
  to: "['group:7c1e9a52-3b4d-4e5f-8a6b-1c2d3e4f5a6b', 'clerk@primaria.ro']"
  title: "'New request from ' + form.name"
  body: "'Request ' + form.subject + ' waits for a review.'"
  link: "'/cereri'"
```

- `to`: whom it goes to, as an expression giving one name or a list: a person's id, their email, or `group:` and a group's id. Names that are no one of the portal's (another portal's people, service accounts, people disabled, unknown emails) are passed by, saying nothing. A notification reaches at most 100 people; past that, the rest are left out.
- `title`: an expression giving the title, up to 200 characters.
- `body`: an expression giving the words, up to 2,000 characters. Optional.
- `link`: an expression giving a page of the portal, a path such as `/cereri/42` or `/_portal/admin/proposals`. A link to another site is refused when the portal checks the files, and passed by when it is made as the run goes. Optional.

A run sends at most 5 notifications; a run for a visitor, such as a public form sent by someone not signed in, at most 2. Visitors' runs share an allowance of 200 notifications an hour, one form or job sends at most 1,000 an hour, and a portal at most 5,000. An endpoint sends no notifications.

### An agent's answer, as a notification

A job can ask an [agent](/portal/sites/actions/#ask-an-agent) and send its answer to the people concerned:

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

## The widget

Place the portal's `notifications` widget on a page, or in a layout region every page has:

```yaml
regions:
  aside:
    - id: notifications
      app: portal
      widget: notifications
      preferences: { limit: 5 }
```

A person signed in sees how many notifications they have not read, and the newest `limit` (1 to 20; 5 when left out). Opening one marks it read and goes to its page. Visitors see nothing, and neither does an administrator seeing the portal as someone else. A page with the widget is made for each person and never kept in a cache.

## By email

Everyone chooses on [My account](/portal/console/account/#notifications) whether their notifications come by email too; it is off until they turn it on. The email has the notification's title as its subject, and its words and link. It goes only when the install sends email, and within the portal's hourly allowance of email; when it sends none, the switch is off and says so.

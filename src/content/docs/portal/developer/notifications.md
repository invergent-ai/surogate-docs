---
title: Notifications
description: The sendNotification action of a form or a job, and the notifications widget on a page, key by key.
---

The configuration behind [Notifications](/portal/sites/notifications/). That page covers where people find their notifications, whom one goes to and the limits.

## The action

The `sendNotification` action sends one, from a [form](/portal/sites/forms/)'s actions or a [job](/portal/sites/jobs/). It says whom it goes to, a title, some words and a page to open: see [A form's message, to the clerks](/portal/developer/notifications/#a-forms-message-to-the-clerks). Like `email`, it is sent once the run ends well: a run that fails tells no one, and neither does its `onError` list.

## A form's message, to the clerks

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

## An agent's answer, as a notification

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

## The widget on a page

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

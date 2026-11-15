---
title: Newsletters with Mailchimp and Constant Contact
description: The mailchimp and constantcontact connectors and the mailchimpMember and constantContactContact actions, as the site's configuration writes them.
---

What these do, and their limits, are on [Newsletters with Mailchimp and Constant Contact](/portal/sites/marketing/).

## A Mailchimp connector

In `connectors/news.yaml`:

```yaml
name: { ro: Știri, en: News }
kind: mailchimp
```

Its credential is `apiKey`, set in the console.

## A Constant Contact connector

```yaml
name: { ro: Știri, en: News }
kind: constantcontact
clientId: 0f3c2a1b-5d6e-4f70-8a9b-0c1d2e3f4a5b
```

- `clientId`: the app's API key. The account is connected from the console, through `/_portal/connect/<connector>`. Its credentials, `clientSecret` and `refreshToken`, are never typed. Changing `clientId` disconnects the account.

## A Mailchimp member

```yaml
- type: mailchimpMember
  connector: news
  op: save
  list: '"a1b2c3d4e5"'
  email: form.email
  status: pending
  fields:
    FNAME: form.firstName
  tags: '["site"]'
  permissions:
    Email: form.agreeEmail
  into: member
```

- `op`: `save`, `get`, `archive` or `erase`. `list` and `email`: expressions.
- For `save`: `status` (`subscribed`, `pending`, `unsubscribed` or `transactional`; someone new is `pending` when it is left out, and an existing member's status changes only when it is given), `fields`, `tags`, `removeTags`, `permissions` (a map of the permission's words or id to a true or false expression), `language`.
- `into` keeps `{id, email, status, fields, tags, permissions}` for `save` and `get` (`null` when none), `{done}` for the others. A visitor's `save` keeps `{done: true}` only.

## A Constant Contact contact

```yaml
- type: constantContactContact
  connector: news
  op: save
  email: form.email
  lists: '["3f1b2c4d-0000-4000-8000-000000000001"]'
  firstName: form.firstName
  into: contact
```

- `op`: `save`, `get`, `unsubscribe` or `delete`. For `save`: `lists` (1 to 50 list ids), `firstName`, `lastName`, `resubscribe: true` to sign up again someone who unsubscribed. For `unsubscribe`: `by: contact` when the person asked (`account` by default).
- `into` keeps `{id, email, lists, created}` for `save` (`skipped: true` when it was left unsubscribed), `{id, email, permission, firstName, lastName, lists}` or `null` for `get`, `{done}` for the others.

A form with `public: true` may use only `op: save`, with Mailchimp's `status` `pending` or left out and no `resubscribe`; anything else is refused with `marketing_public`.

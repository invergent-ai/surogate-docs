---
title: Managing people from steps
description: The findPerson, invitePerson, updatePerson, setPersonGroups and unlockPerson actions, as the site's configuration writes them.
---

What these do, and who may run them, are on [Managing people from steps](/portal/sites/people-actions/).

## The actions

```yaml
- type: findPerson
  email: form.email
  into: person
- type: invitePerson
  email: form.email
  site: main
  groups: '["volunteers"]'
  message: '"Bine ați venit!"'
  into: invitation
- type: updatePerson
  email: form.email
  name: form.name
  fields:
    department: form.department
  status: active
- type: setPersonGroups
  email: form.email
  add: '["volunteers"]'
  remove: '["applicants"]'
- type: unlockPerson
  email: form.email
```

- `findPerson` keeps `{id, email, name, status, fields, groups: [{name, source}]}` or `null`; `updatePerson` keeps the same; `setPersonGroups` keeps `{groups}`; `invitePerson` keeps `{id}`; `unlockPerson` keeps `{done}`.
- `site` is a site's id; `fields` names user fields, each an expression; `status` is `active` or `disabled`; `groups`, `add` and `remove` are lists of group names.

## Load checks

- A form with `public: true`, or an endpoint with `access: public` or a `cache`, may not use them: `people_public`.
- A job using them names `runAs`: `people_needs_run_as`.
- A job not started by time (`every`, `at`, `daily`, `cron`) may only `findPerson`, in its actions, its `onError` and the endpoints and flows they reach: `people_untrusted`.

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

## Delete a person, check a login, register a person

```yaml
- type: deletePerson
  email: "'fost.angajat@spital.ro'"

- type: checkCredentials
  user: form.email
  password: form.parola
  into: verificare        # {valid, userId?, reason?}

- type: registerPerson
  email: form.email
  name: form.nume
  password: form.parola   # optional: left out, the person chooses it
  fields:
    unitate: form.unitate # user field: expression
  site: primaria
  into: cont              # {status: pending | exists}
```

- `deletePerson` is for a job with `runAs` an administrator, never a form; a job started by anything but time may not delete.
- `checkCredentials` and `registerPerson` may be in a form anyone may send. `registerPerson` needs `signUp` on in the sign-in policy and mail; the sign-up is kept in `self_service_tokens` with its fields and a password hash until the link is used.


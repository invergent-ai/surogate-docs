---
title: Forms
description: The keys of a form's file, and the actions that run once it is sent.
---

The configuration behind [Forms](/portal/sites/forms/). That page covers what people see, how administrators build a form in the console, who sends it and who reads what was sent.

## Write a form

Forms are written in [form.io](https://form.io)'s format: the components form.io's builder makes, as JSON or YAML.

Each form is a file of the portal's, `forms/<id>.yaml`. Its id is lower-case letters, digits and hyphens, starting with a letter. See the [config example](#a-forms-file).

- `name`: the form's name, in both languages.
- `language`: the language its components are written in, `ro` unless you say otherwise.
- `display`: `form`, or `wizard` for a form in steps, where each step is a `panel` at the top of the form.
- `sites`: the sites that offer it. Leave it out to offer it on every site.
- `confirmation`: what a person reads once the form is sent. Without it, the portal thanks them.

## A form's file

In `forms/<id>.yaml`, here `forms/cerere-audienta.yaml`:

```yaml
name: { ro: Cerere de audiență, en: Meeting request }
public: true
permissions:
  review: [group:Registratura]
components:
  - { type: textfield, key: name, label: Nume, input: true, validate: { required: true } }
  - { type: email, key: email, label: Email, input: true, validate: { required: true } }
  - type: select
    key: topic
    label: Subiect
    input: true
    dataSrc: values
    data: { values: [{ label: Taxe, value: taxes }, { label: Urbanism, value: planning }] }
  - { type: textarea, key: details, label: Detalii, input: true }
  - { type: button, key: submit, label: Trimite, action: submit }
i18n:
  en: { Nume: Name, Subiect: Subject, Taxe: Taxes, Urbanism: Planning, Detalii: Details, Trimite: Send }
confirmation:
  ro: Mulțumim. Vă vom contacta în cel mult trei zile lucrătoare.
  en: Thank you. We will contact you within three working days.
```

- `public: true` lets anyone send it; `permissions.review` names who reads what was sent.
- `components` are form.io's components, each with a `type`, a `key` and a `label`; `validate` sets what is required.
- `i18n` gives each text in the other language, the text as the key.
- `confirmation` is what a person reads once the form is sent.
- `name`, `language`, `display`, `sites` and `confirmation` are described under [Write a form](#write-a-form).

## What a form may hold

A text block is a component of type `content`, in the markup a site's pages allow.

## A field shown on a condition

On a component:

```yaml
conditional:
  show: true
  conjunction: all
  conditions: [{ component: topic, operator: isEqual, value: planning }]
```

- The field shows only when the `topic` field equals `planning`.

## Translations

The text of a form is written in its `language`. Under `i18n`, give each text in each of its sites' other languages, the text as the key.

## Who sends it and who reads what was sent

- **Who sends it:** `public: true` lets anyone send it, signed in or not. Otherwise `permissions.submit` names who may: `signed-in`, groups, organizations or people.
- **Who reads what was sent:** `permissions.review` names the people, groups or organizations who read, export and delete its submissions.

Name them one per entry, as `signed-in`, `group:<name>`, `organization:<path>` or `user:<email>`.

## A form on a page

A form is placed with the portal's `form` widget.

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
- { id: audienta, app: portal, widget: form, preferences: { form: cerere-audienta } }
```

- `form`: the id of a form the site offers.

## What the portal checks

Lengths and number limits are set under a component's `validate`: `minLength`, `maxLength`, `min` and `max`. `required: true` makes a field required.

## Come back to a form

Turn drafts off for a form with `drafts: false`.

## Consent

In the form's file:

```yaml
consent:
  text:
    ro: Sunt de acord cu prelucrarea datelor mele pentru această cerere.
    en: I agree to my data being used for this request.
```

- `consent.text`: what the person agrees to, in each language.

## Tell the reviewers by email

In the form's file:

```yaml
notify:
  to: [registratura@primarie.ro]
  answers: false
```

- `to`: the addresses, at most 20.
- `answers`: whether the email also holds the answers.
- `subject`: the email's subject, in each language; optional.

## Delete submissions after a time

In the form's file:

```yaml
retention:
  days: 365
```

- `days`: how long a submission is kept.
- Without `retention`, submissions are kept until someone deletes them.

## Fill in offline

In the form's file:

```yaml
public: true
offline: true
```

- `offline: true` lets the browser fill the form in without a connection; the form must be public.

## A record field

Among a form's `components`:

```yaml
- type: record
  key: applicant
  label: Solicitant
  model: people
- type: record
  key: related
  label: Cereri legate
  model: requests
  multiple: true
```

- `model`: the data model whose records are picked.
- `multiple: true`: the person picks up to 50.

## Fields from an app

An approved app can add field types and option lists ([Build an app](/portal/developer/build-an-app/#form-fields-and-options)). Use them in the form's file.

Among a form's `components`:

```yaml
components:
  - { type: appfield, key: sig, label: Semnătură, input: true, app: crm, field: signature, validate: { required: true } }
  - { type: select, key: county, label: Județ, input: true, dataSrc: app, data: { app: crm, options: counties } }
```

- `appfield`: a field type an approved app gives; `app` and `field` name them.
- `dataSrc: app`: a select whose options come from the app, named by `data.app` and `data.options`.

## Actions after it is sent

A form can run [actions](/portal/sites/actions/) once it is sent and kept: work out a reference number, tell the person something, or send them to a payment page. If the actions fail, the person is told so, with the failing action's `errorMessage` when it has one.

In the form's file:

```yaml
redirects: [https://plati.example.ro]
actions:
  submitted:
    - type: redirect
      to: '"https://plati.example.ro/plata?ref=" + urlEncode(submission.id)'
```

- `redirects`: the https sites the form may send people to.
- `actions.submitted`: the [actions](/portal/sites/actions/) that run once the form is sent and kept.

The keys of an action list are in [Developer: Actions](/portal/developer/actions/).

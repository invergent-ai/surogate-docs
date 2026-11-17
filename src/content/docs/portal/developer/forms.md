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

Lengths and number limits are set under a component's `validate`: `minLength`, `maxLength`, `minWords`, `maxWords`, `min` and `max`. `required: true` makes a field required.

`pattern` is a regular expression the whole value must match. The portal checks it in time linear in the value, so it takes no back references (`\1`) and no lookarounds (`(?=…)`, `(?!…)`, `(?<=…)`, `(?<!…)`): a field whose pattern has them refuses every value it is sent. The console says so before it saves.

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

## Confirm who sends it

```yaml
public: false
reauth: true
```

- `reauth: true` asks a person signed in to prove who they are again before the form is sent, if they have not within the sign-in policy's minutes; the server answers `403` with `reauth_required` and the page asks and sends again. A public form, and a form bound to a model (`model:`), cannot take it: a bound form's moves ask with `reauth: true` on the transition in the model's `states`.

```yaml
states:
  field: stare
  initial: draft
  list: {…}
  transitions:
    - id: send
      label: { ro: Transmite, en: Send }
      from: [draft]
      to: sent
      by: [group:staff]
      reauth: true
```

## Keep robots out

```yaml
public: true
captcha: true
```

- `captcha: true` makes a visitor send, with the form, a solution of a challenge asked of `/_portal/api/auth/captcha?form=form` and solved with the worker the portal serves at `/_portal/captcha/worker.js`: `{ "data": {…}, "captcha": { "challenge": "…", "nonce": "…" } }`. A missing or wrong solution is answered `400`, `captcha_required` or `captcha_failed`, and nothing is kept. The form must be public and cannot be offline.
- The actions `checkCredentials` and `registerPerson` take an optional `captcha` expression (a map of `challenge` and `nonce`), solved for the form `check` or `register`. A visitor's run of `registerPerson` needs it unless the form it runs for has `captcha: true`.

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

## A form bound to a model

A form with `model` creates that model's records and opens existing ones to edit: [Forms for records](/portal/sites/model-forms/) in the site guide describes what people see.

```yaml
name: { ro: Fișa lunară, en: Monthly sheet }
language: en
model: monthly_reports
sites: [reports]
permissions: { submit: [signed-in] }
components:
  - type: panel
    key: period
    title: Reporting period
    components:
      - { type: textfield, key: year, label: Year, input: true }
      - { type: textfield, key: month, label: Month, input: true }
  - type: lines
    key: lines
    label: Waste by code
    lineColumns:
      - { field: code, label: Code, width: 12 }
      - { field: generated, label: Generated, width: 12 }
      - { field: closing }
```

- `model`: the id of a model of the portal. The form's own address takes `?record=<id>` to open a record.
- A field is a component whose `key` is a field of the model: the loader refuses any other key on an input component. Its type may be any the form takes; the model, not the component, says what is required, active and read-only, and a `required` set on the component is ignored. A form bound to a model needs no submit button.
- `lines` is a component for the grid of the model's lines (its `lines` setting): at most one a form, and only in a form bound to a model whose model has lines. `lineColumns` lists 1 to 40 columns, in order: `field` is a field of the line model, never the link back to the record; `label` is the text of the heading, in the form's language and translated like any label (the field's own label when left out); `width` is 4 to 80 characters.
- The page runs `evaluateAggregate`, the code the server runs, on every change, and asks `POST /_portal/api/data/<model>/evaluate` for what depends on other records. It saves with `POST` or `PATCH` on `/_portal/api/data/<model>` (the header's fields and `lines: [...]` in one body) and moves with `POST /_portal/api/data/<model>/<id>/transition`.
- A panel, a fieldset or a well may carry `activeWhen: <CEL>`, and so may a tab of a `tabs` component (`{ label, key, activeWhen, components }`): a condition over the model's fields, at most 2,000 characters. The loader gives it to the fields the section holds: each such field's `activeWhen` becomes `(its own) && (the section's)`, and a grid's columns get it with the header's names written `parent.<name>`. So the portal enforces it on every path (a value sent for an inactive field is refused, a stored one is cleared, none is required), and the models the portal runs differ from the model files. It is refused on a form with no model (`section_unbound`), on a step of a `wizard` (`section_wizard`), when it does not hold over the model's fields (`section_condition`), and when another form puts the same field under a different condition, or shows it outside any section (`section_conflict`: a model's own form claims nothing, and one form uses a key once, so a field is never in two sections of one form).
- A form bound to a model with `public: true` sends its answer as any form does, and the record is made only by a `createRecord` action for the model among `actions.submitted` (reason `public_no_record` when there is none). With a `lines` grid, the action's `values` must carry the rows, with a `lines` key such as `lines: 'form["lines"]'` (reason `public_no_lines`): the page puts the rows written in the grid in the submission under the grid's `key`, as a list of objects with the line model's fields, and the data layer checks them as it checks any write. `model-<id>` forms do this for you.
- **Everything the model says is in the page.** The page runs the model's own logic, so the model's rules, lock, states, prefill, results and linked models, with their expressions and messages, are sent to the browser of anyone who can open a bound form, signed in or not (a public bound form too). Keep nothing in a model's expressions or messages that a person who may open a form bound to it should not read.
- `offline: true` is refused on a form bound to a model, and the form keeps no drafts. `display: wizard` works: each top-level panel is a step.
- Each model's own form `model-<id>` is bound to the model, with a `lines` component for the model's lines.

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

## Options from a model, a data source or a web service

A choice field's `optionsFrom` is in [Developer: Data sources](/portal/developer/data-sources/#a-fields-options).

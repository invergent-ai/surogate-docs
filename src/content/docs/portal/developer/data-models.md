---
title: Data models
description: A model's file, its fields and permissions, and the REST and GraphQL calls that read and write its records.
---

The configuration behind [Data models](/portal/sites/data-models/). That page covers what a model holds, who sees its records, and what happens when it changes.

## A model's file

A model lives in `models/<id>.yaml`. The portal makes its table and keeps it in step with the file.

In `models/<id>.yaml`, here `models/requests.yaml`:

```yaml
name:
  ro: Cereri
  en: Requests
title: subject
fields:
  subject:
    type: text
    label: { ro: Subiect, en: Subject }
    required: true
    searchable: true
    sortable: true
  status:
    type: text
    label: { ro: Stare, en: Status }
    filterable: true
  amount:
    type: money
    label: { ro: Sumă, en: Amount }
  citizen:
    type: link
    model: citizens
    label: { ro: Cetățean, en: Citizen }
permissions:
  view: { all: [group:clerks], own: [signed-in] }
  add: [everyone]
  edit: { all: [group:clerks] }
  delete: { all: [role:administrator] }
```

- `name`: what the model is called, in Romanian and English.
- `title`: the field that names a record in lists.
- `fields`: each by its id, with a `type` from the [field types](#fields) and a `label` in both languages. Add `required`, `searchable`, `filterable` or `sortable` as the field needs. A `link` names the `model` it points at.
- `permissions`: who may `view`, `edit` and `delete` all records or only their own, and who may `add`. See [Who may do what](#who-may-do-what).
- The id, here `requests`, and each field's id are lower-case letters, digits and `_`, starting with a letter, at most 30 characters. A portal has at most 50 models, each with at most 100 fields.

A model can also declare [KPIs](/portal/sites/kpis/), and make its own pages: see [Developer: KPIs](/portal/developer/kpis/) and [Developer: Listings](/portal/developer/listings/).

## Fields

| Type | Holds |
|---|---|
| `text` | Text, up to 10,000 characters (500 when filterable or sortable) |
| `largeText` | Text, up to 1,000,000 characters |
| `number` | A number |
| `money` | An amount with up to 4 decimals, answered as text such as `12.5000` |
| `date`, `datetime`, `time` | `2026-11-10`, `2026-11-10T09:30:00Z`, `09:30` |
| `boolean` | `true` or `false` |
| `email`, `phone`, `url` | Checked as what they are; a `url` is http, https or mailto |
| `link` | One record of the model named by `model` |
| `links` | Several records of the model named by `model` |

A field can be `required`, `searchable` (text, searched by `q`), `filterable` and `sortable`. Every record also has its `id`, its owner, and when and by whom it was made and last changed.

A link to a record that is deleted is cleared; a record's own links to others go with it.

## Who may do what

`permissions` says, for each role, whether it may view, edit and delete **all** records or only its **own**, and who may **add** records. Principals are those used everywhere in the portal: `everyone`, `signed-in`, `role:administrator`, `user:<email>`, `group:<name>`, `organization:<path>`. Administrators may always do everything; with no `permissions`, only they may.

A record is someone's own when they added it. A visitor owns nothing: with `add: [everyone]`, a public form can add records that its visitors then cannot see.

### Access by condition

`permissions` can also hold `rules`, a `holder` and who may work on its behalf. A rule gives a verb (`view`, `add`, `edit` or `delete`) to some principals only for the records a [CEL](/portal/developer/actions/) condition picks, over `record` and `user`:

```yaml
permissions:
  view: { all: [role:user_vizualizare] }
  rules:
    view:
      - to: [role:user_dsp]
        when: record.entitate.judet == user.fields.judet || record.entitate.retea == user.fields.retea
      - to: [role:user_furnizor]
        when: record.entitate in user.fields.entitati
    edit:
      - to: [role:user_furnizor]
        when: record.entitate in user.fields.entitati
  holder: entitate
  onBehalf:
    - to: [role:user_dsp]
      when: user.fields.judet != null
  reasons:
    - Spitalul nu are acces la internet
```

The condition reads `record.<field>` (and `record.<link>.<field>`, up to four links deep, and `record.owner` and `record.id`), `user.id`, `user.roles` and `user.fields.<key>`. It may use `==`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`, `!` and `in`. A value the person has no value for makes the condition false. The file is refused when a condition does not read, names a field or a user field that does not exist, or compares unlike values.

`holder` names a link field of the model; `onBehalf` says who may work on a record whose holder is not one of the person's own entities, with an optional condition; `reasons` are the reasons the console offers. The reason is asked of every such change, through `reason` on the REST API (a query parameter, or the percent-encoded `X-Portal-Reason` header), `reason` on a GraphQL change, and `reason` on the record actions. See [Access to records by condition](/portal/sites/row-access/).

### User fields

The fields the portal keeps of each person are `users/fields.yaml`, a list. Besides `text`, `number`, `boolean`, `date`, `email` and `phone`, a field can be a `link` or `links` with the `model` it points at; `institution: true` marks the link that names the person's institution, and `ownEntities: true` the links that name the entities they work for:

```yaml
- key: judet
  label: { ro: Județ, en: County }
  type: link
  model: judete
- key: entitati
  label: { ro: Entitățile proprii, en: Own entities }
  type: links
  model: entitati
  ownEntities: true
```

Rules and expressions read a field as `user.fields.<key>`: the id of the record, or the list of ids.

## When the file changes

The portal adds what the file adds: a new model gets its table, a new field its column. It never takes anything away: a field or model taken out of the file keeps its data, and comes back with it if it is put back.

A field's type can never change. A file that changes one is refused when it is saved, and the portal keeps what was live; add a new field with the new type instead.

## The API

Records are served at the portal's address:

- `GET /_portal/api/data/<model>` lists records. It takes:
  - `filter.<field>=<value>` on a filterable field;
  - `q=` to search the searchable fields;
  - `sort=<field>` or `sort=-<field>`;
  - `limit` (at most 100);
  - `after`, to page on.
  The answer has `items` and, when there are more, `next`.
- `GET /_portal/api/data/<model>/<id>` reads one record.
- `POST /_portal/api/data/<model>` adds one.
- `PATCH /_portal/api/data/<model>/<id>` changes the fields given.
- `DELETE /_portal/api/data/<model>/<id>` deletes one.

Adding, changing and deleting need someone signed in; an app's token needs the `data` access. A record someone may not see answers as if it did not exist. A value that does not fit its field is refused, naming the field.

## GraphQL

The same records answer GraphQL at `POST /_portal/api/graphql`, with the same rules as the API above. Each person sees only the models they may reach:

- `get_<model>(id: "…")` reads one record, or gives null when there is none for them.
- `list_<model>(first, after, q, sort, filter)` lists records, with `items` and `next` as above. `filter` takes the filterable fields.
- `create_<model>(values: {…})`, `update_<model>(id: "…", values: {…})` and `delete_<model>(id: "…")` change records. They are offered only to someone signed in, never to visitors, and never while an administrator sees the portal as someone else.

A record has `id`, `ownerId`, `createdAt`, `updatedAt` and its fields. A link gives the linked record, when the person may see it.

```graphql
{
  list_requests(first: 20, filter: { status: "new" }) {
    items { id subject applicant { name } }
    next
  }
}
```

```graphql
mutation {
  create_requests(values: { subject: "Fence repair" }) { id }
}
```

A request may nest 6 levels, ask for 10 things at its top and name 500 fields in all. One that would read more than 2000 records stops with a single `too_costly` error and no data. A refused value names its field in `extensions.field`. Every change is in the [audit log](/portal/console/audit/), one entry each.

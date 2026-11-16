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

## History

`history` makes the model keep a version of every write and archive what is deleted: see [History and archiving](/portal/sites/data-models/#history-and-archiving).

```yaml
history:
  enabled: true
  archive: true
  archiveReason: true
  referenceState: accepted
permissions:
  history: [group:auditors]
  archive: { all: [group:clerks], own: [signed-in] }
  viewArchived: [group:clerks]
  restore: [role:administrator]
```

- `enabled`: keep every version. The default when `history` is there; `false` turns it off and keeps what was written.
- `archive`: deleting archives. The default while the history is on; `false` keeps versions but deletes for good.
- `archiveReason`: archiving needs a reason. Not with `archive: false`.
- `referenceState`: the state whose sealed version stands for a closed period, read with `version=accepted`.
- `permissions.history`: who sees the versions of the records they may read; none, administrators only. `archive`, `viewArchived` and `restore` say who archives (all or own, as deleting), who sees what is archived and who restores. These four need `history`.
- A model with a history has the columns `archived_at`, `archived_by` and `archive_reason`, which no field may use as its id, and a table of versions, `portal__versions`, and a view of each record's reference version, `portal__reference`, which the [data console](/portal/console/data-console/) reads.

## Who may do what

`permissions` says, for each role, whether it may view, edit and delete **all** records or only its **own**, and who may **add** records. Principals are those used everywhere in the portal: `everyone`, `signed-in`, `role:administrator`, `user:<email>`, `group:<name>`, `organization:<path>`. Administrators may always do everything; with no `permissions`, only they may.

A record is someone's own when they added it. A visitor owns nothing: with `add: [everyone]`, a public form can add records that its visitors then cannot see.

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

### History and archiving through the API

On a model that keeps its history:

- `DELETE /_portal/api/data/<model>/<id>` archives. `?reason=` gives the reason; a model that asks for one refuses without it, naming `reason`. An archived record answers as if it did not exist, except to those who see archived records.
- `GET /_portal/api/data/<model>?archived=only` lists only the archived records; `includeArchived=true` adds them to the others, and the same on one record. Archived records have `archivedAt`, `archivedBy` and `archiveReason`. For anyone who may not see them, `archived=only` is an empty list and `includeArchived` changes nothing.
- `POST /_portal/api/data/<model>/<id>/restore` brings an archived record back.
- `GET /_portal/api/data/<model>/<id>/versions` lists its versions, oldest first: `version`, `at`, `operation` (`create`, `update`, `transition`, `archive`, `restore`, `revert`, `auto` or `initial`), `detail`, `channel` (`form`, `listing`, `rest`, `graphql`, `job` or `endpoint`), `author` (kind, name and email as they were, and `status`: `active`, `disabled` or `deleted`), `onBehalf`, `changed`, `sealed`, `sealState` and `sealLabel`. `?sealed=true` lists only the sealed ones.
- `GET .../versions/<n>` gives one version with its `values` and `refs`, the title each link had.
- `GET .../versions/compare?from=<n>&to=<m>` gives the fields that differ, each with its value in both.
- `GET .../versions/verify` recalculates the sealed versions' fingerprints: `{ ok: true, checked: N }`, or `{ ok: false, version: N }` for the first that was changed.
- `POST .../versions/<n>/revert` writes version *n*'s values as a new version, as a save by the caller: the model's checks apply.
- `GET .../<id>/title` gives `{ id, title, archived }` for a record that a link points at, an archived one too.
- Versions are never changed: `PATCH`, `PUT` and `DELETE` on `.../versions` and `.../versions/<n>` answer 403 `version_immutable` and are in the audit log.

A person sees a record's versions only when `permissions.history` names them and they may read the record. For anyone else every one of these answers as for a record that does not exist.

#### Reports and closed periods

`GET /_portal/api/data/<model>` and `GET .../<id>` read the past:

- `asOf=<date or date and time>` gives each record as it was by then: its last version made at or before that moment. A time written without a zone is Romania's, compared in UTC; `2026-11-15T00:00Z` or `+02:00` are taken as written. A record not yet made is not there; one archived by then is not there either.
- `version=accepted` gives each record's last version sealed in the model's `referenceState`, whatever it is now. A record that was never sealed in that state is not there, and neither is one that is archived now. With `asOf`, the last such version made by then.
- Both keep the caller's reach: a person who reads their own records gets only those. Each item has `_version`, the version it is.

A reporting tool that loads the versions itself reads `portal__versions` in the [data console](/portal/console/data-console/): `seq` only grows, so `where seq > <the last taken>` gives what is new and nothing twice; `portal__reference` gives each record's reference version.

## GraphQL

The same records answer GraphQL at `POST /_portal/api/graphql`, with the same rules as the API above. Each person sees only the models they may reach:

- `get_<model>(id: "…")` reads one record, or gives null when there is none for them.
- `list_<model>(first, after, q, sort, filter)` lists records, with `items` and `next` as above. `filter` takes the filterable fields.
- `create_<model>(values: {…})`, `update_<model>(id: "…", values: {…})` and `delete_<model>(id: "…")` change records. They are offered only to someone signed in, never to visitors, and never while an administrator sees the portal as someone else.

On a model that keeps its history, `get_<model>` and `list_<model>` also take `asOf` and `version: "accepted"`, and `includeArchived` (`onlyArchived` for a list); a record has `archivedAt`. `versions_<model>(id: "…")` lists the versions and `version_<model>(id: "…", number: 1)` opens one, each with `values`, for those the model names. `restore_<model>(id: "…")` and `revert_<model>(id: "…", version: 1)` bring a record back and write a version back; `delete_<model>` takes `reason`. What a person may not do is not in their schema.

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

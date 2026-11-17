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
| `decimal` | An exact decimal with `decimals` places (0 to 6, 2 by default), answered as text such as `125.750`; sent as a number or as text with a point; more places than the field has are refused, never rounded |
| `date`, `datetime`, `time` | `2026-11-10`, `2026-11-10T09:30:00Z`, `09:30` |
| `boolean` | `true` or `false` |
| `email`, `phone`, `url` | Checked as what they are; a `url` is http, https or mailto |
| `link` | One record of the model named by `model` |
| `links` | Several records of the model named by `model` |
| `location` | A GeoJSON point or polygon; `shape` and `snapshot` are its own keys: see [Maps](/portal/developer/maps/#a-location-field) |

A field can be `required`, `searchable` (text, searched by `q`), `filterable` and `sortable`. Every record also has its `id`, its owner, and when and by whom it was made and last changed.

A link to a record that is deleted is cleared; a record's own links to others go with it.

## Logic in a model's file

The model editor writes these keys; they can also be written by hand. They are described for people in [Calculated fields and checks](/portal/sites/model-logic/) and [Lines, values from other records and states](/portal/sites/model-lines-states/). Expressions are CEL, with exact decimals, in the language that page lists.

A field takes, besides `type`, `label`, `required`, `searchable`, `filterable`, `sortable` and `model`:

```yaml
fields:
  grad_ocupare:
    type: decimal
    decimals: 2              # 0 to 6
    separator: point         # point, comma; left out: the page's language
    thousands: true
    min: 0
    max: 100
    calculated:
      expression: paturi_ocupate / (paturi_total * zile_luna) * 100
      when: se_aplica && paturi_total > 0      # empty when false
  media_an:
    type: decimal
    decimals: 4
    calculated:
      expression: avg(set.map(r, r.kg_pat_luna))
      when: luna == 12 && size(set) == 12
      over:                  # over other records; they are `set`
        model: fisa
        match: { unitate: unitate, an: an }     # their field: an expression of this record
        where: row.stare in ['transmisa']       # optional, over `row` and `record`
  paturi_ocupate:
    type: decimal
    decimals: 0
    required: true
    requiredAt: submit       # save (default) or submit
    requiredMessage: { ro: …, en: … }
    requiredWhen: { when: paturi_total > 0, at: save }
    activeWhen: se_aplica
    inactive: hidden         # or disabled
    editableBy: [group:dsp, role:administrator]
    validators:
      - kind: integer        # integer, positive_integer, email, date
        message: { en: Whole beds only }
      - expression: paturi_ocupate >= 0        # true when valid
        when: se_aplica
        message: { ro: …, en: … }
        severity: warning    # error (default) or warning
        at: submit
  cant_sp:
    type: decimal
    prefill:
      model: fisa_linie
      match:
        fisa.unitate: parent.unitate           # a field, or a link's field
        fisa.luna: "parent.luna == 1 ? 12 : parent.luna - 1"
        cod_deseu: cod_deseu
      field: cant_rs                           # or: expression over `source`
      missing: { value: "0", message: { ro: …, en: … } }
      states: [ciorna, corectat]               # default: every state that is not checked
      manualFlag: sp_manual
  fisa:
    type: link
    model: fisa
    lineOf: true             # this model's records are lines of fisa
  stare:
    type: text
    system: true             # only the portal writes it
```

A model takes:

```yaml
results: { problemCount: nr_probleme, complete: complet }
rules:
  - id: paturi
    label: { ro: …, en: … }
    check: paturi_ocupate <= paturi_total * zile_luna   # true when valid
    when: se_aplica                                      # optional
    field: paturi_ocupate                                # where the words are said
    message: { ro: "Maximum {{paturi_total * zile_luna}}", en: "At most {{paturi_total * zile_luna}}" }
    severity: error          # or warning
    at: save                 # or submit
    disabled: false
  - id: unica
    label: { ro: …, en: … }
    unique: [unitate, an, luna]
    field: luna
    message: { ro: …, en: … }
lines:
  model: fisa_linie
  rows:
    mode: fixed              # one line for each record of `from`
    from: nom_cod
    where: { activ: true }
    order: ord
    field: cod_deseu         # the line's link field that takes the record
    # or: { mode: free, min: 0, max: 20 }
states:
  field: stare
  initial: ciorna
  submittedAt: transmis_la   # optional
  submittedBy: transmis_de   # optional, the person's id
  list:
    ciorna: { label: { ro: …, en: … }, editableBy: [group:furnizori] }
    transmisa: { label: { ro: …, en: … }, checked: true }
  transitions:
    - id: transmite
      label: { ro: Transmite, en: Submit }
      from: [ciorna]
      to: transmisa
      by: [group:furnizori]
      when: complet           # optional
      comment: false          # true asks for one
lock:
  editable: now < startOfDay(an + 1, 4, 1) || user.roles.exists(r, r == 'administrator')
  message: { ro: …, en: … }
  covers: [update, delete, transition]   # default: all three
```

### What a write answers

Every way of writing a record gives a refusal the same shape. A write that breaks a check answers `400` with `error: "record_invalid"` and the whole list of `problems`:

```json
{
  "error": "record_invalid",
  "message": "Maximum 3000 (beds × days in the month)",
  "field": "paturi_ocupate",
  "problems": [
    {
      "field": "paturi_ocupate",
      "line": null,
      "message": "Maximum 3000 (beds × days in the month)",
      "severity": "error",
      "at": "save",
      "rule": "paturi"
    }
  ]
}
```

`line` is `{ "index", "id", "key" }` for a problem of a line: its place in the record's lines, its id once saved and, for a fixed row, the id of the record it was made from. `at` is `save` or `submit`. A record held by its lock answers `403` with `error: "record_locked"` and the words of the lock; one in a state nobody may change it in answers `403` with `state_locked`. In GraphQL the error's `extensions` carry `code`, `field` and `problems`. In an action, the message lists the problems of severity error.

A write that goes through answers the record as before, and also `_problems` (what did not stop it: warnings, and checks that wait for submitting) and, for a header, `_lines`. A value taken from another record that was not found adds `_notes`. `GET /_portal/api/data/<model>/<id>` of a header carries `_lines` too, and GraphQL records have `_problems` and `_lines`.

### Lines

A header's `POST` and `PATCH` take `lines`: a list of `{ "id"?, …fields }`, written with the header in one transaction. Fixed rows are matched by `id` or by the row's link field and are neither added nor removed; with free rows the list sent is the whole list. A single line can also be written, changed or deleted on its own at `/_portal/api/data/<line model>`, and the header is worked out again in the same transaction. In GraphQL, `create_<model>` and `update_<model>` take `lines` among their `values`.

### What a form needs

`POST /_portal/api/data/<model>/evaluate` takes `{ "id"?, "values"?, "lines"? }` and writes nothing. It answers what the write would do: `values` (calculated and taken values included), `active`, `required` (`save`, `submit` or `null`), `editable` (rights, lock, state, and fields only the portal writes taken into account), `lines`, `problems`, `notes`, `locked`, `state` and the `transitions` the person may make from where the record is. It is what opens a form with last month's value in it, and checks it as it is filled.

### States

- `POST /_portal/api/data/<model>/<id>/transition` takes `{ "to"` (or `"transition"` for a move's id)`, "comment"?, "values"?, "lines"? }`. The values and the move are one write. It answers the record as `PATCH` does.
- `GET /_portal/api/data/<model>/<id>/transitions` answers the log: `items` with `from`, `to`, `transition`, `by` (`id`, `name`), `at` and `comment`.
- GraphQL has `transition_<model>(id, to, transition, comment, values)`.
- The action `changeState` takes `model`, `id`, `to` and, optionally, `comment` and `values`, all expressions.
- `POST /_portal/api/data/<model>/recalculate` takes `{ "filter"?, "after"? }`, `filter` of filterable fields, and works out again the fields calculated over other records, for people who may change every record, a page of 1,000 records at a time. It answers `{ "recalculated", "failed", "next" }`: ask again with `"after": <next>` until `next` is `null`. The action `recalculateRecords` takes `model` and `where` and goes through all the pages.
- `GET /_portal/api/tenant/data/model-log?model=<id>&limit=<n>&before=<id>` is the model's log, newest first, for administrators: `{ "items": [{ "id", "at", "model", "recordId", "field", "rule", "line", "kind", "message" }], "next" }`.

Calculated fields, fields written by the portal (the state, the figures kept of the checks, the flag of a value written by hand) and, for people not named in `editableBy`, a field with that key are refused when a write changes them.

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

Where the model has `states`, `holder` changes only while the record is in `states.initial`; the attempt in any other state is refused with `holder_locked`, and kept in the audit log.

A field can name the roles it is hidden from, `hiddenFor: [user_viz]` (role codes, each once). The field is absent for a person whose roles that count are all listed; see [Fields hidden from a role](/portal/sites/row-access/#fields-hidden-from-a-role).

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

### History and archiving through the API

On a model that keeps its history:

- `DELETE /_portal/api/data/<model>/<id>` archives. `?reason=` gives the reason; a model that asks for one refuses without it, naming `reason`. An archived record answers as if it did not exist, except to those who see archived records.
- `GET /_portal/api/data/<model>?archived=only` lists only the archived records; `includeArchived=true` adds them to the others, and the same on one record. Archived records have `archivedAt`, `archivedBy` and `archiveReason`. For anyone who may not see them, `archived=only` is an empty list and `includeArchived` changes nothing.
- `POST /_portal/api/data/<model>/<id>/restore` brings an archived record back.
- `GET /_portal/api/data/<model>/<id>/versions` lists its versions, oldest first, at most `limit` (200 by default, 500 at most) after the version `after`, with `truncated: true` when there are more: `version`, `at`, `operation` (`create`, `update`, `transition`, `archive`, `restore`, `revert`, `auto`, `initial` or `delete`, the last version of a record deleted for good), `detail`, `channel` (`form`, `listing`, `rest`, `graphql`, `job` or `endpoint`; `listing` is taken from a person's session only), `author` (kind, name and email as they were, and `status`: `active`, `disabled` or `deleted`), `onBehalf`, `changed`, `sealed`, `sealState` and `sealLabel`. `?sealed=true` lists only the sealed ones.
- `GET .../versions/<n>` gives one version with its `values` and `refs`, the title each link had.
- `GET .../versions/compare?from=<n>&to=<m>` gives the fields that differ, each with its value in both.
- `GET .../versions/verify` recalculates the sealed versions' fingerprints: `{ ok: true, checked: N }`, or `{ ok: false, version: N }` for the first that was changed.
- `POST .../versions/<n>/revert` writes version *n*'s values as a new version, as a save by the caller: the model's checks apply.
- `GET .../<id>/title` gives `{ id, title, archived }` for a record that a link points at, an archived one too.
- Versions are never changed: `PATCH`, `PUT` and `DELETE` on `.../versions` and `.../versions/<n>` answer 403 `version_immutable` and are in the audit log.

A person sees a record's versions only when `permissions.history` names them and they may read the record. For anyone else every one of these answers as for a record that does not exist.

#### Reports and closed periods

`GET /_portal/api/data/<model>` and `GET .../<id>` read the past:

- Both need the right to see the history (a visitor or anyone else is answered as for a model that has none); a record that is archived now is in the past only for those who see archived records.
- `asOf=<date or date and time>` gives each record as it was by then: its last version made at or before that moment. A time written without a zone is Romania's, compared in UTC; `2026-11-15T00:00Z` or `+02:00` are taken as written. A record not yet made is not there; one archived by then is not there either.
- `version=accepted` gives each record's last version sealed in the model's `referenceState`, whatever it is now. A record that was never sealed in that state is not there, and neither is one that is archived now. With `asOf`, the last such version made by then.
- Both keep the caller's reach: a person who reads their own records gets only those. Each item has `_version`, the version it is.

A reporting tool that loads the versions itself reads them in the [data console](/portal/console/data-console/). `portal__versions` has every version with `seq` and `tx`, the transaction that wrote it. `seq` is given when a version is written and not when it stands, so a lower one can stand after a higher one was read: `seq` alone is no safe watermark. Read `portal__settled`, the versions no open transaction of the server can still add to, by `where (tx, seq) > (<last tx>, <last seq>) order by tx, seq`. `portal__reference` gives each record's reference version.

## GraphQL

The same records answer GraphQL at `POST /_portal/api/graphql`, with the same rules as the API above. Each person sees only the models they may reach:

- `get_<model>(id: "…")` reads one record, or gives null when there is none for them.
- `list_<model>(first, after, q, sort, filter)` lists records, with `items` and `next` as above. `filter` takes the filterable fields.
- `create_<model>(values: {…})`, `update_<model>(id: "…", values: {…})` and `delete_<model>(id: "…")` change records. They are offered only to someone signed in, never to visitors, and never while an administrator sees the portal as someone else.

On a model that keeps its history, `get_<model>` and `list_<model>` also take `asOf` and `version: "accepted"`, and `includeArchived` (`onlyArchived` for a list); a record has `archivedAt`. `versions_<model>(id: "…")` lists the versions and `version_<model>(id: "…", number: 1)` opens one, each with `values`, for those the model names. `restore_<model>(id: "…")` and `revert_<model>(id: "…", version: 1)` bring a record back and write a version back; `delete_<model>` takes `reason`. What a person may not do is not in their schema: `asOf` and `version` are offered to those who see the history, `includeArchived` and `onlyArchived` to those who see the archived. A link to an archived record is named by its title and `archivedAt`.

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

## Links in depth

`unique`, `lookup` and a model read from a data source (`source`) are in [Developer: Data sources](/portal/developer/data-sources/#entities).

## Reading records as a person may

For a read the portal's own pages and APIs do not make (an export, say), ask the person's rights once and use what comes back: `RowAccess.readable(model)` answers whether they may see any record, which (`scope`: their own, or a condition as SQL), the model without the fields hidden from them, and the field ids; `RowAccess.list(model, query)` and `RowAccess.get(model, id)` are the data API's own list and get with the rules and the hidden fields applied. Do not read the table or `listRecords` directly: nothing else is held to the rules.

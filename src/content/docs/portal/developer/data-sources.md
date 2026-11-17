---
title: Data sources
description: The files behind data sources, the preferences of a listing over a model or a source, a field's options, entities, and the database actions.
---

The configuration behind [Data sources](/portal/sites/data-sources/) and [Database actions](/portal/sites/database-actions/). Those pages say what people see and what each setting does. The console writes all of it: this page is for those who write the files.

## A data source's file

A data source is a file `data-sources/<id>.yaml`. The id is lower-case letters, digits and hyphens, starting with a letter. A portal has at most 100.

### A SQL source

```yaml
name: { ro: Unități pe județ, en: Units by county }
description: { ro: Unitățile unui județ, en: The units of a county }
type: sql
connector: siui                       # a SQL database connector
query: select cod, denumire, paturi from unitati where judet = :judet order by denumire
params: { judet: filters.judet }      # name: expression
maxRows: 1000                         # 1 to 10,000; 1,000 when left out
key: cod                              # the column that identifies a row
columns:
  - { key: cod, label: { ro: Cod, en: Code }, type: text }
  - { key: paturi, label: { ro: Paturi, en: Beds }, type: int }
use: [signed-in]
```

- `query`: one SELECT (or WITH ... SELECT), at most 20,000 characters. Write each parameter as `:name`. A statement with a second statement, a lock (`FOR UPDATE`) or anything that changes data or reaches outside the database is refused.
- `params`: an expression for each `:name`, over `user`, `form`, `filters`, `now` and `locale`. At most 20, and every `:name` has one.
- `columns`: optional. Each is a `key`, a `label` in each language and a `type`: `text`, `int`, `number`, `boolean`, `date`, `datetime` or `time`. At most 50. Left out, the columns are those the query answers.
- `use`: who may use the source, as [permissions](/portal/developer/permissions/) name people. Left out, only administrators.
- The connector must be of kind `sql`, and must not sign in as each person.

A source can add, remove and open a row:

```yaml
add:
  query: insert into unitati (cod, denumire, judet) values (:cod, :den, :judet)
  params: { cod: form.cod, den: form.den, judet: form.judet }
  fields:                                 # the boxes of the Add dialog
    - { key: cod, label: { ro: Cod, en: Code }, type: text, required: true }
    - { key: den, label: { ro: Denumire, en: Name }, type: text, required: true }
    - { key: judet, label: { ro: Județ, en: County }, type: text }
delete:
  query: delete from unitati where cod = :id
view:
  query: select cod, denumire, judet from unitati where cod = :id
```

- `add` and `delete` need a connector with `allowWrites: true`; `view` is a read. A change is one INSERT, UPDATE, DELETE, MERGE or CALL.
- `fields`: at most 30; a `type` of `text`, `number`, `boolean` or `date`. Their values are `form.<key>` in `params`.
- In `delete` and `view`, `:id` is the row's key and takes no entry in `params`.

### A source over the portal's data

```yaml
name: { ro: Raportări pe județ, en: Reports by county }
type: models
query: select judet, count(*)::int as raportari, sum(cantitate) as cantitate from raportari group by judet order by judet
use: [signed-in]
```

The query is PostgreSQL over the tables of the portal's [data models](/portal/developer/data-models/), named without a schema. Whoever reads it sees only the records the models let them see. `params`, `maxRows`, `key` and `columns` are as for a SQL source; there are no `add`, `delete` or `view`.

### A JSON web service source

```yaml
name: { ro: Operatori, en: Operators }
type: api
connector: registry                   # an http connector that does not sign in as each person
path: /operators
query: { county: filters.judet }      # query string: name: expression
listPath: data.items                  # where the list is in the answer
key: cui
cacheSeconds: 300                     # 0 to 3,600
columns:
  - { key: cui, label: { ro: CUI, en: Tax id }, type: text }
  - { key: city, label: { ro: Oraș, en: City }, type: text, path: address.city }
use: [signed-in]
add: { path: /operators }             # POST
delete: { path: /operators/:id }      # DELETE
view: { path: /operators/:id }        # GET
```

- It is a GET call. `columns` is required, and each column's `path` says where its value is in an item (the `key` when left out).
- The answer may hold at most 5,000 rows.
- `add`, `delete` and `view` are each a path under the connector's address, which can never climb above it.

### A form's submissions

```yaml
name: { ro: Cereri trimise, en: Submitted requests }
type: form
form: cerere
own: true                             # each person reads only what they sent
use: [signed-in]
```

The form's reviewers always read everything.

## A listing over a model or a source

A listing's preferences, in the page's file (`sites/<site>/pages/<page>.yaml`), add to those of [Listings](/portal/developer/listings/#a-listing-on-a-page):

```yaml
regions:
  main:
    - id: reports
      app: portal
      widget: listing
      preferences:
        model: reports                  # or: source: units
        columns:
          - county
          - period
          - { field: code, label: { ro: Cod, en: Code }, sortable: true, filterable: true, searchable: false, width: 120 }
          - total
        sort:
          - { field: county, dir: asc }
          - { field: period, dir: desc }
        pageSize: 20                    # 20, 50 or 100
        group:
          allow: [county, period]       # columns people may group by
          default: [county]             # at most 2
          totals:
            - { field: total, fn: sum } # sum, avg, min or max
          dateBy: month                 # day, month or year
        export:
          xlsx: [role:administrator]
          csv: [signed-in]
          pdf: [role:administrator]
        add: true
        edit: true
        delete: true
        archive: true
```

- Exactly one of `model` and `source`.
- `columns`: at most 20. Each is a field or column name, or an object with `field`, `label`, `sortable`, `filterable`, `searchable` and `width`. Left out, every column of a source, or a model's title and first fields. A column that is a link shows the linked record's title; a time of day is not filtered.
- `sort`: at most 3. `group.default`: at most 2. Grouping applies to text, links, yes or no, and dates.
- `export`: who may export, by format. A format that is not named is not offered. Administrators always may export the formats named. Excel and CSV take at most 50,000 rows, and PDF 5,000; more is refused with a message asking to narrow the filters.
- `add`, `edit`, `delete`: as for a model. A source's rows can only be added and removed, and only when the source has `add` and `delete`.
- `archive: true`: the model must keep its history and archive what is deleted; **Archive** is then the button that removes the row from the list, and the model's [history](/portal/developer/data-models/) keeps it.
- The address of a listing keeps what people chose, under `p_<placement id>_`: `sort`, `f.<column>` for a filter, `q.<column>` for a column's search, `q`, `page`, `size`, `group`, `open` and `archived`. An address can be shared.

## A field's options

A choice field takes its options from a model, a data source or a web service, in the form's file:

```yaml
components:
  - type: select
    key: cod
    label: Cod deșeu
    input: true
    optionsFrom:
      kind: model
      model: coduri
      value: cod                      # the option's value; the record's id when left out
      label: denumire                 # the option's label; the model's title when left out
      sort: cod                       # a leading - sorts from the last
      filter: record.activ == true    # over record, form and user
```

```yaml
    optionsFrom:
      kind: source
      source: unitati-judet           # the source's columns value and label are the options
```

```yaml
    optionsFrom:
      kind: api
      connector: registry
      path: /operators
      query: { county: form.county }  # name: expression over form, user and search
      listPath: data.items
      value: cui
      label: name
      cacheSeconds: 300               # 0 to 3,600
```

- `select`, `radio` and `selectboxes` fields take `optionsFrom`, and then need no options written in the field. The portal asks the source, never the browser. When it cannot answer, the field says "The options cannot be had right now."
- A form that anyone may send does not take options that depend on the person, or from a source only some may use.
- A field offers at most 1,000 options. A person's choice is checked again when the form is sent, against what the source offers that person, and the chosen label is kept with the value, as `<key>__label`.
- A field that follows another (`record.county == form.county`) offers the options again when the other changes.

## Entities

In a model's file, `models/<id>.yaml`:

```yaml
name: { ro: Coduri de deșeuri, en: Waste codes }
title: denumire
lookup: true                          # adds the field activ (Active)
fields:
  cod: { type: text, label: { ro: Cod, en: Code }, filterable: true }
  denumire: { type: text, label: { ro: Denumire, en: Name } }
  parent: { type: link, model: coduri, unique: true, label: { ro: Părinte, en: Parent } }
```

- `unique: true` on a `link` field makes it one to one: each record is linked from at most one record. It is refused while two records already link to the same one.
- `lookup: true`: the model gets a yes or no field `activ`. A value turned off is not offered for a new choice, stays where it was chosen, and cannot be removed while it is in use: turn it off. The check counts what links to it, in every model.
- The portal indexes each link column, and the pairs of a many-to-many link.
- A model with no table, read from a data source:

```yaml
name: { ro: Operatori (din registru), en: Operators (from the register) }
title: denumire
source:
  dataSource: operatori
  key: cui                            # the column that identifies a record
  map: { name: denumire }             # optional: a field's column, when it is not the field's own id
fields:
  cui: { type: text, label: { ro: CUI, en: Tax id } }
  denumire: { type: text, label: { ro: Denumire, en: Name }, searchable: true }
permissions:
  view: { all: [signed-in] }
```

A model read from a source is only read: it has no add, edit or delete, no links, no lookup and no history, and nothing links to it. It answers the API, GraphQL, listings and the data console like any other model, filtered, sorted and searched by the portal.

## Database actions

In any action list (a job's `actions`, a form's `steps`, an endpoint's or a flow's):

```yaml
actions:
  - type: runSql
    connector: siui
    mode: read                        # or write; read when left out
    query: select cod, denumire, paturi from unitati where judet = :judet
    params: { judet: "'Cluj'" }       # expressions: this one is a text
    maxRows: 500                      # optional
    timeout: 20                       # optional, in seconds
    into: unitati                     # vars.unitati.rows, .columns, .rowCount, .truncated, .affected
  - type: importRecords
    model: unitati_locale
    list: vars.unitati.rows
    fields: { cod: item.cod, denumire: item.denumire, paturi: item.paturi }
    match: cod                        # update the record with this value
    atomic: true                      # default: one refused row, nothing written
    into: loaded                      # vars.loaded.created, .updated, .failed, .errors
```

- `connector: portal` reads the portal's own data, in a job that runs as an administrator with the data console on. It reads only.
- A `write` needs a connector with `allowWrites: true`, a signed-in run, and a place that is not a GET endpoint or an endpoint anyone may call.
- `importRecords` is for jobs, and the job runs as a person (`runAs`). `fields` gives each field's expression over `item`, `user` and `now`; `match` is a field that can be filtered on.

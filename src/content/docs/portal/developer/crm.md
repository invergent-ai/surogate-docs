---
title: CRM records in Dynamics 365 and Salesforce
description: The dynamics and salesforce connectors and the dynamicsRecord, dynamicsQuery, salesforceRecord and salesforceQuery actions, as the site's configuration writes them.
---

What these do, and their limits, are on [CRM records in Dynamics 365 and Salesforce](/portal/sites/crm/).

## A Dynamics 365 connector

In `connectors/crm.yaml`:

```yaml
name: { ro: CRM, en: CRM }
kind: dynamics
url: https://contoso.crm4.dynamics.com
directory: 0f3c2a1b-5d6e-4f70-8a9b-0c1d2e3f4a5b
clientId: 6a7b8c9d-0e1f-4a2b-8c3d-4e5f6a7b8c9d
```

Its credential is `clientSecret`, set in the console.

## A Salesforce connector

```yaml
name: { ro: Vânzări, en: Sales }
kind: salesforce
url: https://acme.my.salesforce.com
clientId: 3MVG9…
```

Its credential is `clientSecret`, the app's consumer secret.

## A record

```yaml
- type: salesforceRecord
  connector: sales
  op: create
  object: Lead
  values:
    Email: form.email
    LastName: form.name
    Company: "'—'"
  assign: true
  into: lead
- type: dynamicsRecord
  connector: crm
  op: upsert
  table: contacts
  key:
    emailaddress1: form.email
  values:
    firstname: form.firstName
    "parentcustomerid_account@odata.bind": "'/accounts(' + vars.account + ')'"
  into: contact
```

- `op`: `create`, `get`, `update`, `upsert` or `delete`.
- Dynamics 365: `table`, then `id` (an expression giving a GUID) or `key` (a map of columns to expressions) for every op but `create`; `values` for `update` and `upsert`; `select` (columns, separated by commas) for `get`.
- Salesforce: `object`; `id` for `get`, `update` and `delete`; `externalField` and `externalId` for `upsert`; `values` for `update` and `upsert`; `fields` (the record's own) for `get`; `assign` (true or false; Salesforce's rules when left out) for `create` and `upsert`.
- `into` keeps `{id}` for `create` (and `upsert` in Dynamics 365), `{id, created}` for Salesforce's `upsert`, the record or `null` for `get`, and `{done}` for `update` and `delete`.

## A query

```yaml
- type: dynamicsQuery
  connector: crm
  table: incidents
  select: title,ticketnumber,statecode
  where:
    "_customerid_value:guid": vars.contact
  filter: statecode eq 0
  orderBy: createdon desc
  top: "20"
  into: cases
- type: salesforceQuery
  connector: sales
  object: Contact
  fields: Id, Name, Account.Name
  where:
    Email: form.email
  maxRecords: "5"
  into: found
```

- `where`: each column or field equals its expression's value, compared as text unless the name ends `:guid`, `:date` or `:datetime`. `filter` and `orderBy` are written as they are sent.
- `into` keeps `{records, more}`.

A form with `public: true`, or an endpoint with `access: public` or a `cache`, may use only record actions with `op: create`; anything else is refused with `crm_public`.

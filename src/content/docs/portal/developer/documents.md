---
title: Documents
description: The dms.yaml file, the portal's documents and document widgets, and the jobs that take the DMS's events.
---

The configuration behind [Documents](/portal/sites/documents/). That page covers what people see of the DMS's documents in a page, how filing and downloads work, and what happens when the DMS does not answer.

## Connect the DMS in `dms.yaml`

At the top of the portal's files:

```yaml
api: https://dms.primaria.ro
app: https://dms.primaria.ro
```

- `api`: the DMS's API. Inside the same cluster, its service address works too, such as `http://sdms.surogate-docs.svc`.
- `app`: the DMS's web app, where a document's link and its downloads go.
- `timeoutMs`: how long the portal waits for the DMS, from 1,000 to 10,000 ms; 3,000 when left out.
- `uploadMb`: the largest file a person can file from a page, from 1 to 5,120 megabytes; 100 when left out. See [File documents from a page](/portal/sites/documents/#file-documents-from-a-page).
- `audience`: what the portal names the DMS as in its sign-ins; leave it out unless the DMS's administrator set another.
- `serviceKey`: the connector holding the DMS's key for its events; see [The service key and a job](#the-service-key-and-a-job).

The DMS must trust the portal: see [Connect the DMS](/portal/sites/documents/#connect-the-dms).

## A folder on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: rules
      app: portal
      widget: documents
      preferences:
        folder: 5d8e2c1a-1b2c-4d3e-8f90-112233445566
        limit: 10
        sort: newest
```

- `folder`: the DMS folder, by its id. Open the folder in the DMS and copy the id from its address.
- `limit`: how many documents, 1 to 50; 10 when left out.
- `sort`: `title` (when left out) or `newest`, the ones changed last first.

Placed without `dms.yaml`, the widget is refused when the files are published.

## A folder with filing from the page

In a region of a page's file:

```yaml
- id: requests
  app: portal
  widget: documents
  preferences:
    folder: 5d8e2c1a-1b2c-4d3e-8f90-112233445566
    upload: true
    type: 3c8f7f6e-2a3c-4d5e-9f10-111213141516
```

- `upload: true` shows a form under the list, with a title and a file. When left out, the widget only shows the folder.
- `type`: the DMS document type new documents are filed under, by its id. When left out, they are filed with no type, if the folder allows that. A type with a folder of its own in the DMS files there, not in the widget's folder, so its new documents do not show in this list.
- `uploadMb` in `dms.yaml` is the largest file the form takes: see [Connect the DMS in `dms.yaml`](#connect-the-dms-in-dmsyaml).

## One document on a page

In a region of a page's file:

```yaml
- id: regulation
  app: portal
  widget: document
  preferences:
    document: 0b8f7f6e-2a3c-4d5e-9f10-111213141516
    versions: 5
    upload: true
```

- `document`: the DMS document, by its id. Open it in the DMS and copy the id from its address.
- `versions`: how many of the newest versions to list, 1 to 50; 10 when left out. A link below the list says how many older ones the DMS holds.
- `upload: true` lets people add a version from the page. When left out, the widget only shows the document.

## The service key and a job

In `dms.yaml`, with the connector that holds the DMS's key:

```yaml
api: https://dms.primaria.ro
app: https://dms.primaria.ro
serviceKey: dms-key
```

A job that runs when a document changes state, in `jobs/document-approved.yaml`:

```yaml
trigger:
  dms:
    on: [document.state]
site: main
runAs: user:registratura@primaria.ro
actions:
  - type: log
    level: info
    message: '"Document " + trigger.document + " is now " + trigger.to'
```

- `serviceKey`: the secret connector holding the DMS's key. Ask the DMS's administrator for a service key, add it as a secret [connector](/portal/developer/connectors/#a-connectors-file), set its value under **Connectors**, and name the connector in `dms.yaml` as `serviceKey`.
- `trigger.dms.on`: the events that start the job, from the table under [The DMS's events in a job](#the-dmss-events-in-a-job).
- `runAs`: the person the job acts as.

## The DMS's events in a job

A [job](/portal/sites/jobs/) takes the DMS's events in its `trigger`:

| Event | When | What the run also reads |
|---|---|---|
| `document.created` | A document is made | `folder`, `type`, `source` |
| `document.version` | A new version becomes the current one | `version`, `versionId` |
| `document.state` | Its state changes | `from`, `to` |
| `document.moved` | It moves to another folder | `from`, `to` (the folders) |
| `document.updated` | Its title, type or a field changes | `fields`, the names changed |
| `document.deleted` | It is deleted after a selection | `selection` |

- **What the run reads:** `trigger.event` is the event, `trigger.document` the document's id, and `trigger.at` when it happened. Events never hold a title, a file name or what a document says.
- **Also as events:** each one is also the portal event `portal/dms.<event>`, such as `portal/dms.document.state`, for [apps and webhooks](/portal/developer/apps/#events).

What the key sees, and what happens when the portal cannot read the DMS, are on [When something happens in the DMS](/portal/sites/documents/#when-something-happens-in-the-dms).

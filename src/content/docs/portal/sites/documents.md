---
title: Documents
description: Connect the portal to Surogate DMS, and show a DMS folder's documents in a page.
---

Surogate DMS keeps the institution's documents. Connected, a page of the portal shows the documents of a DMS folder to the person signed in, as the DMS lets them see it, with a link to each in the DMS and a download.

## Connect the DMS

Name your DMS in `dms.yaml`, at the top of the portal's files:

```yaml
api: https://dms.primaria.ro
app: https://dms.primaria.ro
```

- `api`: the DMS's API. Inside the same cluster, its service address works too, such as `http://sdms.surogate-docs.svc`.
- `app`: the DMS's web app, where a document's link and its downloads go.
- `timeoutMs`: how long the portal waits for the DMS, from 1,000 to 10,000 ms; 3,000 when left out.
- `audience`: what the portal names the DMS as in its sign-ins; leave it out unless the DMS's administrator set another.
- `serviceKey`: the connector holding the DMS's key for its events; see [When something happens in the DMS](#when-something-happens-in-the-dms).

The DMS must trust the portal. Its administrator adds the portal's **issuer**, shown on the console's **Apps** page under **For the apps' developers**, to the DMS's trusted portals, with the address of the portal's keys. The DMS then finds each person among its people by their email: the email they have in the portal must be the one they have in the DMS.

## Show a folder

Place the portal's `documents` widget on a page:

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

A person signed in sees the folder's documents they may see in the DMS, each with its state, version, file name, size and date. Each title opens the document in the DMS. Below the list, a link opens the folder in the DMS, saying how many more it holds.

- **Visitors** see a prompt to sign in.
- **Someone the DMS does not know**, or has deactivated, sees that they have no access to the DMS.
- **A folder they cannot read** shows no documents. A folder that is not there says so.
- **When the DMS does not answer**, the rest of the page shows as usual, and the widget says the documents cannot be read now.
- **An administrator seeing the portal as someone else** does not see that person's documents.

What a document holds, its fields and their values, is never shown in the portal. A page with the widget is never kept in a cache and shown to someone else. Placed without `dms.yaml`, the widget is refused when the files are published.

## Search the DMS from the portal

A search box can show the DMS's documents too: see [Search](/portal/sites/search/#documents-in-the-dms).

## Downloads

**Download** asks the DMS, as the person, for a link to the file that works for a minute, and opens it: the file comes from the DMS, never through the portal.

- When the DMS asks why the person opens a document, as it does for documents with personal data, or holds the file aside after a failed check, Download opens the document in the DMS instead, where the person can say why or see what happened.
- A visitor is asked to sign in first.

## When something happens in the DMS

A [job](/portal/sites/jobs/) can run each time a document is made, given a new version, moved to another state or folder, changed, or deleted in the DMS. The portal reads the DMS's events with a key of its own: ask the DMS's administrator for a service key, add it as a secret [connector](/portal/sites/connectors/), set its value under **Connectors**, and name the connector in `dms.yaml`:

```yaml
api: https://dms.primaria.ro
app: https://dms.primaria.ro
serviceKey: dms-key
```

Then a job can wait for documents to be approved:

```yaml
# jobs/document-approved.yaml
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

| Event | When | What the run also reads |
|---|---|---|
| `document.created` | A document is made | `folder`, `type`, `source` |
| `document.version` | A new version becomes the current one | `version`, `versionId` |
| `document.state` | Its state changes | `from`, `to` |
| `document.moved` | It moves to another folder | `from`, `to` (the folders) |
| `document.updated` | Its title, type or a field changes | `fields`, the names changed |
| `document.deleted` | It is deleted after a selection | `selection` |

- **What the run reads:** `trigger.event` is the event, `trigger.document` the document's id, and `trigger.at` when it happened. Events never hold a title, a file name or what a document says.
- **What the key sees:** the DMS shows its key's account only the events of documents it may read. Ask the DMS's administrator to give the account the right to read the documents your jobs should hear of, the right to read the archive for deletions, and, for documents holding personal data, the clearance for their level. Without them the portal hears of nothing, and no error says so.
- **Once each:** each event runs each job that takes it once, a few seconds after it happens, in the order the DMS recorded them. When the portal cannot read the DMS, it tries again and loses nothing. **Jobs** in the console shows when the DMS's events were last read. If the DMS has deleted old events the portal had not read yet, the portal reads on from then, and **Jobs** says when: those events are lost.
- **Also as events:** each one is also the portal event `portal/dms.<event>`, such as `portal/dms.document.state`, for [apps and webhooks](/portal/sites/apps/).

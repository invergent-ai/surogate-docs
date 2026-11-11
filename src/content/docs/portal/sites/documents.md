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

## Downloads

**Download** asks the DMS, as the person, for a link to the file that works for a minute, and opens it: the file comes from the DMS, never through the portal.

- When the DMS asks why the person opens a document, as it does for documents with personal data, or holds the file aside after a failed check, Download opens the document in the DMS instead, where the person can say why or see what happened.
- A visitor is asked to sign in first.

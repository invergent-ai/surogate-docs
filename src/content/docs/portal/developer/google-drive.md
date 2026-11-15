---
title: Files in Google Drive
description: The googledrive connector and the googleDriveList, googleDriveUpload, googleDriveDownload, googleDocFromTemplate, googleDriveShare and googleDriveDelete actions, as the site's configuration writes them.
---

What these do, and who may run them, are on [Files in Google Drive](/portal/sites/google-drive/).

## The connector

```yaml
# connectors/drive.yaml: a service account acting as a Workspace user
name: { ro: Drive, en: Drive }
kind: googledrive
signIn: serviceAccount
subject: registratura@primaria.ro
```

```yaml
# connectors/drive-account.yaml: a Google account connected from the console
name: { ro: Drive, en: Drive }
kind: googledrive
signIn: account
clientId: 123456789012-abc123def456ghi789.apps.googleusercontent.com
```

- `signIn` is `serviceAccount` (credential `serviceAccountKey`) or `account` (credentials `clientSecret` and `refreshToken`, set only by **Connect**).
- `subject` (a service account only, optional) is the Workspace user it acts as. `clientId` (an account only) is the OAuth client's id.
- `timeoutMs` is at most 60,000 (30,000 when left out). `baseUrl`, `auth`, `test` and `perUser` are not taken.

## The actions

```yaml
- type: googleDriveList
  connector: drive
  folderId: 0AbCdEfGhIjKlMnOpQ
  nameContains: form.search
  max: "50"
  into: found
- type: googleDriveUpload
  connector: drive
  folder: cvs
  name: vars.application.cv
  toFolderId: 0AbCdEfGhIjKlMnOpQ
  replace: true
  into: sent
- type: googleDriveShare
  connector: drive
  fileId: vars.sent.id
  role: reader
  email: vars.application.email
  notify: false
- type: googleDocFromTemplate
  connector: drive
  templateId: 1aBcDeFgHiJkLmNoPqRsT
  toFolderId: 0AbCdEfGhIjKlMnOpQ
  name: "'Contract ' + vars.number"
  values:
    client: vars.name
    date: vars.date
  into: doc
- type: googleDriveDownload
  connector: drive
  fileId: vars.doc.id
  toFolder: contracts
  toName: "'contract-' + vars.number + '.pdf'"
  as: pdf
  into: kept
- type: googleDriveDelete
  connector: drive
  fileId: vars.doc.id
```

- `folderId`, `toFolderId` and `templateId` are written as they are: a Drive id (10 to 200 letters, digits, `-` and `_`), or `root` for a folder. `fileId`, `name`, `toName`, `nameContains`, `max` and `email` are expressions.
- `googleDriveList` keeps `{files: [{id, name, mimeType, size, modifiedTime, webViewLink, folder}], more}`; `googleDriveUpload` keeps `{id, name, webViewLink}`; `googleDriveDownload` keeps `{id, name, mimeType, size}`; `googleDocFromTemplate` keeps `{id, name, webViewLink, missing}`; `googleDriveShare` keeps `{id}`; `googleDriveDelete` keeps nothing.
- `convert` and `replace` are `true` or `false`. `as` is `pdf`, `docx`, `odt`, `txt` (a Doc), `pdf`, `xlsx`, `ods`, `csv` (a Sheet) or `pdf`, `pptx`, `odp`, `txt` (Slides); the portal file's name ends with it.
- `googleDriveShare` takes `email` or `anyone: true`, one of the two; `role` is `reader`, `commenter` or `writer` (not with `anyone`); `notify` (with `email`) is `true` unless written `false`.
- `values` names at most 50 placeholders: letters, digits, `.`, `-` and `_`, as the template writes them between `{{` and `}}`.

## Load checks

- A form with `public: true`, or an endpoint with `access: public` or a `cache`, may not use them: `google_drive_public`.
- A job not started by time (`every`, `at`, `daily`, `cron`) may not `googleDriveShare` or `googleDriveDelete`, in its actions, its `onError` and the endpoints and flows they reach: `google_drive_untrusted`.
- A `googleDriveShare` with both `email` and `anyone`, or neither: `share`.

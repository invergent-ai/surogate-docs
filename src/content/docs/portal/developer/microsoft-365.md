---
title: Files in OneDrive and SharePoint
description: The microsoft365 connector and the microsoftDriveList, microsoftDriveUpload, microsoftDriveDownload, microsoftDriveShare and microsoftDriveDelete actions, as the site's configuration writes them.
---

What these do, and who may run them, are on [Files in OneDrive and SharePoint](/portal/sites/microsoft-365/).

## The connector

```yaml
# connectors/hr-files.yaml: a SharePoint site's document library
name: { ro: Dosare HR, en: HR files }
kind: microsoft365
directory: 0f3c2a1b-5d6e-4f70-8a9b-0c1d2e3f4a5b
clientId: 6a1d4c2e-7b3f-4e8a-9c0d-1e2f3a4b5c6d
driveOf: site
site: contoso.sharepoint.com/sites/hr
```

- `directory` and `clientId` are GUIDs. `driveOf` is `site` (with `site`: a `*.sharepoint.com` host, and `/sites/<name>` or `/teams/<name>` unless it is the root site) or `user` (with `user`: the user's sign-in name).
- The credential is `clientSecret`. `timeoutMs` is at most 60,000 (30,000 when left out). `baseUrl`, `auth`, `test` and `perUser` are not taken.

## The actions

```yaml
- type: microsoftDriveList
  connector: hr-files
  path: /Candidați/2026
  max: "50"
  into: found
- type: microsoftDriveUpload
  connector: hr-files
  folder: cvs
  name: vars.application.cv
  toPath: /Candidați/2026
  into: sent
- type: microsoftDriveShare
  connector: hr-files
  itemId: vars.sent.id
  role: read
  email: vars.application.recruiter
  notify: true
- type: microsoftDriveDownload
  connector: hr-files
  itemId: vars.contract.id
  toFolder: contracts
  toName: "'contract-' + vars.number + '.pdf'"
  as: pdf
  into: kept
- type: microsoftDriveDelete
  connector: hr-files
  itemId: vars.old.id
```

- `path` and `toPath` are written as they are: `/`, or `/` and folder names separated by `/`, at most 400 characters. A name holds none of `" * : < > ? / \ |`, is not `.` or `..`, neither starts with a space nor ends with a space or a dot, and is not one SharePoint keeps for itself (`CON`, `_vti_`…). `itemId`, `name`, `toName`, `email` and `max` are expressions.
- `microsoftDriveList` keeps `{items: [{id, name, size, folder, modifiedTime, webUrl}], more}`; `microsoftDriveUpload` keeps `{id, name, webUrl}`; `microsoftDriveDownload` keeps `{id, name, size}`; `microsoftDriveShare` keeps `{id, link}` (`link` null for a person); `microsoftDriveDelete` keeps nothing.
- `replace` is `true` or `false`. `as` is `pdf`; the portal file's name ends with `.pdf`.
- `microsoftDriveShare` takes `email` or `link` (`organization` or `anyone`), one of the two; `role` is `read` or `write` (only `read` with `anyone`); `notify` goes only with `email`.

## Load checks

- A form with `public: true`, or an endpoint with `access: public` or a `cache`, may not use them: `microsoft_drive_public`.
- A job not started by time (`every`, `at`, `daily`, `cron`) may not `microsoftDriveShare`, `microsoftDriveDelete` or `microsoftDriveUpload` with `replace: true`, in its actions, its `onError` and the endpoints and flows they reach: `microsoft_drive_untrusted`.
- A `microsoftDriveShare` with both `email` and `link`, or neither: `share`.

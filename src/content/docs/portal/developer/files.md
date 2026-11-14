---
title: Files
description: A folder's file, public or secure, and a folder kept in a bucket.
---

The configuration behind [Files](/portal/console/files/). That page covers what people see, uploading, linking, moving and removing files, and where files are kept.

## A folder's file

Folders are made in the portal's files, `content/folders/<id>.yaml`. Administrators can also make them in the console's [Folders](/portal/console/folders/) page. The console does not keep comments written in the file by hand when it saves it.

In `content/folders/<id>.yaml`, here `content/folders/forms.yaml`:

```yaml
name: { ro: Formulare, en: Forms }
public: true
permissions: { view: [signed-in], edit: [group:Registratura] }
```

- `name`: the folder's name, in Romanian and English.
- `public: true` makes it a public folder; left out, it is secure.
- `permissions.view`: who may open the files of a secure folder.
- `permissions.edit`: who edits the folder, besides the administrators.

## A folder kept in a bucket

In `content/folders/<id>.yaml`, here `content/folders/archive.yaml`, with a [bucket connector](/portal/developer/connectors/#a-buckets-file) `archive-bucket`:

```yaml
name: { ro: Arhivă, en: Archive }
public: false
permissions: { view: [group:Staff], edit: [group:Registratura] }
storage:
  connector: archive-bucket
  prefix: city/archive/
```

- `storage.connector`: a connector of kind `bucket`.
- `storage.prefix`: where the folder's files are in the bucket: lower-case letters, digits, hyphens, underscores and slashes, ending in a slash, at most 200 characters. When left out, the folder's id and a slash (`archive/`). Two folders never share one place of one bucket.

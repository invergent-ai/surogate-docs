---
title: Files
description: Keep documents and images in the portal's folders, public or secure, and link to them from pages and content.
---

**Files** keeps the portal's documents and images, such as forms to download, reports, or photos for news, in folders. Pages, HTML blocks and content entries link to them.

**Files** is in the menu for the people who edit a folder: the editors it names, those given it on [Access](/portal/console/access/), and the administrators.

## What people see

Visitors and people signed in meet the files as links on the site's pages and entries. Here a page lists the documents of a public folder, and each title is a link to a file anyone can download:

![A page of public documents: a note that the files are in the public folder documente, and a table of four documents, each with its title as a link, a description and its format, CSV or TXT.](../../../../assets/screenshots/portal-files-page.png)

Editors and administrators keep the files under **Files** in the console, as the sections below say.

## Folders

Each folder is either:
- **Public**: anyone downloads its files, signed in or not;
- **Secure**: only the people the folder names may open its files, and its editors. A secure folder that names no one is for its editors only.

Folders are made in the portal's files, `content/folders/<id>.yaml` (see the [config example](#config-example)).

## Upload a file

Choose the **Folder**, then **Upload** a file. The portal keeps:
- images (PNG, JPEG, GIF, WebP, AVIF) and text, which browsers show;
- PDFs, Word, Excel and PowerPoint documents, OpenDocument files, CSV, JSON and ZIP archives, which browsers download.

A file is at most 10 MB. Its name becomes lower case, with other characters as hyphens: `Cerere Înscriere.PDF` becomes `cerere-inscriere.pdf`. Uploading a file of the same name replaces it, after the console asks you; links then open the new file.

## Link to a file

**Copy link** copies the file's address, such as `/_portal/files/forms/cerere-inscriere.pdf`. Use it in a page's text, an [HTML block](/portal/sites/layouts/#an-html-block), or a content entry's link or image field.

A visitor opening a secure folder's file is asked to sign in; someone the folder does not let view it is told there is no such file.

## Remove a file

**Remove** takes a file away, after asking. Links to it stop working. Earlier versions of a file, replaced or removed, are kept a month, then gone.

A folder taken out of the portal's files keeps its files; a folder made again under the same id finds them.

## Config example

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


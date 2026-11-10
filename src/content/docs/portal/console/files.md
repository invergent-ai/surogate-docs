---
title: Files
description: Keep documents and images in the portal's folders, public or secure, and link to them from pages and content.
---

**Files** keeps the portal's documents and images, such as forms to download, reports, or photos for news, in folders. Pages, HTML blocks and content entries link to them.

**Files** is in the menu for the people who edit a folder: the editors it names, those given it on [Access](/portal/console/access/), and the administrators.

## Folders

Each folder is either:
- **Public**: anyone downloads its files, signed in or not;
- **Secure**: only the people the folder names may open its files, and its editors. A secure folder that names no one is for its editors only.

Folders are made in the portal's files, `content/folders/<id>.yaml`:

```yaml
name: { ro: Formulare, en: Forms }
public: true
permissions: { view: [signed-in], edit: [group:Registratura] }
```

## Upload a file

Choose the **Folder**, then **Upload** a file. The portal keeps:
- images (PNG, JPEG, GIF, WebP, AVIF) and text, which browsers show;
- PDFs, Word, Excel and PowerPoint documents, OpenDocument files, CSV, JSON and ZIP archives, which browsers download.

A file is at most 10 MB. Its name becomes lower case, with other characters as hyphens: `Cerere Înscriere.PDF` becomes `cerere-inscriere.pdf`. Uploading a file of the same name replaces it.

## Link to a file

**Copy link** copies the file's address, such as `/_portal/files/forms/cerere-inscriere.pdf`. Use it in a page's text, an [HTML block](/portal/sites/layouts/#an-html-block), or a content entry's link or image field.

A visitor opening a secure folder's file is asked to sign in; someone the folder does not let view it is told there is no such file.

## Remove a file

**Remove** takes a file away, after asking. Links to it stop working. Earlier versions of a file, replaced or removed, are kept a month, then gone.

A folder taken out of the portal's files keeps its files; a folder made again under the same id finds them.

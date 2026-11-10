---
title: Content
description: Write a site's news, announcements and other entries, save drafts, and publish them when they are ready.
---

**Content** is where a site's news, announcements and other entries are written. Each entry follows a content type, such as News or Announcement, which says what fields it has. Administrators build content types on [Content types](/portal/console/content-types/). Visitors see an entry only once it is published.

**Content** is in the menu for the people who edit a site: its administrators, and the editors named for the site or given the site on [Access](/portal/console/access/). An administrator seeing the portal as someone else does not see it.

## Find an entry

Choose the **Site** and the **Content type**. The list shows each entry with its title, its address and when it last changed. **Search** finds entries by their title, their text or their address.

Each entry shows where it is:
- **Draft**: visitors do not see it yet.
- **Published**: visitors see it as it is.
- **Published, with changes**: visitors see the published entry; the draft has changes they do not see yet.

## Write an entry

**New entry** opens an empty entry. **Edit** opens one from the list.

- **Address**: lower-case letters, digits and hyphens, such as `program-de-iarna`. It is unique among the site's entries of the type. An entry keeps its address once it is published.
- **The fields** come from the content type. A field written per language has one box for each of the site's languages, such as **Headline (ro)** and **Headline (en)**. A field marked `*` must be filled in, in every language, before the entry can be published.
- **Rich text** is written in HTML. It holds what a page's [HTML block](/portal/sites/layouts/#an-html-block) may hold.
- **A link** has an address and its text. **An image** has an address and a description of what it shows.

**Save draft** keeps your changes without showing them to visitors. Save as often as you like.

## Publish

**Publish** saves your changes, then shows the entry to visitors. When something is missing, nothing is published and the editor lists what to fix, such as **Headline (en): fill it in to publish**.

**Unpublish** takes the entry off the site. Its draft stays, to publish again later.

**Delete** removes the entry, its draft and every published version, after asking.

Each publication is kept, the newest hundred.

## History

A published entry lists its publications under **History**: each version's number, when it was published and by whom. **Bring back version** puts that version back as the draft; publish it to show it to visitors. Save or undo your changes first.

## When someone else is editing

If someone saved the same entry after you opened it, your save is refused rather than overwriting theirs. Open the entry again to see their changes, then make yours.

## Show content on a page

In the [page editor](/portal/console/pages/), **Add content…** places a content type in a part of the page. It shows either:
- **The newest entries**: how many, and in what order (newest first, oldest first, or by title);
- **One entry**: by its address.

A page always shows the published entries. A visitor reading in a language an entry does not have sees the site's main language.

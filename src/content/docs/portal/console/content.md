---
title: Content
description: Write a site's news, announcements and other entries, save drafts, and publish them when they are ready.
---

**Content** is where a site's news, announcements and other entries are written. Each entry follows a content type, such as News or Announcement, which says what fields it has. Administrators build content types on [Content types](/portal/console/content-types/). Visitors see an entry only once it is published.

**Content** is in the menu for the people who edit a site: its administrators, and the editors named for the site or given the site on [Access](/portal/console/access/). An administrator seeing the portal as someone else does not see it.

Next to the sites, **Site** lists the [libraries](/portal/sites/content-types/#libraries) you edit, as **Library:** and their name. A library's entries are written once and shown by every site it serves.

## Overview

The Content page opens with where your content stands, for each site and library you edit:
- per content type, how many entries are **Drafts**, **Published**, and published **With changes** not published yet;
- **Recently changed**: the ten entries changed last, each opening in the editor;
- **Tags in use**: the tags of published entries, with how many entries have each.

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

## Categories and tags

When the portal has vocabularies that sort the content type, the editor lists their categories under the fields, indented under the category above them. Tick the ones the entry belongs to; for a vocabulary that takes only one, choose it, or **None**.

**Tags** are words of your own, separated by commas, such as `iarna, drumuri`. They are kept in lower case, each once, at most 20.

If the portal later drops a category an entry has, the entry simply loses it the next time it is saved or published.

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
- **The newest entries**: how many, and in what order (newest first, oldest first, or by title). **Category** and **Tag** show only the entries in that category (or one under it) and with that tag;
- **One entry**: by its address.

**From** chooses where the entries come from: **This site**, or a library that serves the site.

**Add a collection…** places a [collection](/portal/sites/content-types/#collections): entries chosen once for several pages. **Collection** changes which one.

A page always shows the published entries. A visitor reading in a language an entry does not have sees the site's main language.

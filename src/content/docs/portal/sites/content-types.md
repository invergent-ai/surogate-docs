---
title: Content types
description: Define the kinds of content a portal's sites hold, their fields, and how each entry looks on a page.
---

A content type says what a kind of entry holds, such as a news item's headline, date and text. The people who edit a site write entries in the console's [Content](/portal/console/content/) page; pages show them with the content widget.

## What people see

**People who edit a site** find its entries under **Content** in the console, filtered by site and content type:

![The Content page filtered to the News type: six published entries, each with its address and Edit, and the tags in use.](../../../../assets/screenshots/portal-content-types-entries.png)

An entry's form is built from the type's fields: the headline and the summary once for each language, a day for the date, a choice for the kind, and so on. Fields marked with a star must be filled in to publish.

![A news entry open in the console: the address, the headline in Romanian and in English, the date, the kind and the summary, with its history on the right.](../../../../assets/screenshots/portal-content-types-editor.png)

**Visitors** see the published entries on the site's pages. A list shows each entry as the type's template says, and each entry has a page of its own:

![The news page of a site: a list of entries, each with its date, its kind, its headline as a link and its summary.](../../../../assets/screenshots/portal-news-list.png)

![One news entry on its own page: its date, its summary and its text, with a link to all news.](../../../../assets/screenshots/portal-news-entry.png)

Administrators can also build the types in the console, on [Content types](/portal/console/content-types/).

## A content type

Each content type is a file in the portal's files, `content/types/<id>.yaml`, shared by all the sites. Administrators can also build them in the console's [Content types](/portal/console/content-types/) page. See the [config example](#a-content-types-file).

- **`name`** and each field's **`label`** are in Romanian and English.
- **`title`** names the text field that names an entry in lists.
- A field's **`id`** is lower-case letters, digits and hyphens. **`required: true`** must be filled in, in every language, to publish.
- A portal has at most 100 content types, each with at most 50 fields.
- **`blog: true`** makes the type a [blog](/portal/sites/blogs/): its entries are posts, each by the person who wrote it.

## Field types

| Type | Holds | Per language |
|---|---|---|
| `text` | one line, 200 characters unless `maxLength` says otherwise | yes |
| `textarea` | lines of plain text, 10,000 characters unless `maxLength` says otherwise | yes |
| `richtext` | HTML, as an [HTML block](/portal/sites/layouts/#an-html-block) holds | yes |
| `number` | a number | no |
| `boolean` | yes or no | no |
| `date` | a day, shown in the visitor's language | no |
| `link` | an address and its text | yes |
| `image` | an image's address and what it shows | yes |
| `select` | one of the field's `options` | no |

`localized: false` makes a text, link or image field the same in every language.

## How an entry looks

Without a template, an entry shows its title as a heading, then each other field.

A **`template`** places the fields in markup of your own. It takes what a site's [layouts](/portal/sites/layouts/) take, and `<portal-field name="…"></portal-field>` where a field's value goes (see the [config example](#a-template)).

A rich text field holds paragraphs and other blocks. It stands directly in a block such as a `div` or a `section`, never inside a paragraph or a heading.

When the site has a [display page](#display-pages) for the type, `<portal-entry-link>` links what it holds to the entry's address; it takes a `class` and holds no other link. Without a display page it shows what it holds, unlinked. Without a template, the entry's title is the link.

Each entry is an `article` with the class `portal-content`; a list of entries is a `div` with the class `portal-content-list`. Style them in the site's layout stylesheet.

## Vocabularies

A vocabulary sorts entries into categories, such as Topics or Area. Each is a file, `content/vocabularies/<id>.yaml` (see the [config example](#a-vocabularys-file)).

- A category's id is lower-case letters, digits and hyphens, unique in its vocabulary. Categories nest at most five levels deep, 500 per vocabulary; a portal has at most 20 vocabularies.
- A category is named by its vocabulary and its id: `topics/winter`.
- People choose an entry's categories, and type its tags, in the [content editor](/portal/console/content/#categories-and-tags).
- Categories and tags sort and filter entries; pages do not show them yet.

## Libraries

A library holds content shared by several sites, such as announcements every site of a city hall shows. Its own editors write its entries; pages of the sites it serves show them. Each library is a file, `content/libraries/<id>.yaml` (see the [config example](#a-librarys-file)).

- Who edits a library: the people and groups its `edit` names, those given it on [Access](/portal/console/access/), and the administrators. A site's editors do not, unless named.
- A library's entries are written in the portal's languages, Romanian and English. A site shows them in its own languages, falling back to its main one.
- A site the portal no longer has is forgotten. A library left with no site serves none.
- Removing a library keeps its entries out of reach; saving a library again under the same id brings them back, published ones included.
- At most 20 libraries.

## Collections

A collection names a set of entries once, for pages and for apps: a hand-picked list, or a saved query. Each is a file, `content/collections/<id>.yaml` (see the [config example](#a-collections-file)).

- A hand-picked collection names up to 50 entries by their address, each once. An entry not published yet is left out until it is.
- A query works as a content list's: `category`, `tag`, `order` and `limit`.
- A page shows it with `preferences: { collection: front }`, and nothing else, on its site or a site its library serves.
- At most 100 collections.

### Reading a collection

Apps and other consumers read a collection's published entries at `/_portal/api/collections/<id>`, with `?locale=ro` or `en`:

```json
{ "id": "front", "name": { "ro": "…", "en": "…" }, "type": "news",
  "items": [{ "id": "…", "slug": "deszapezire", "publishedAt": "2026-11-10T…", "values": { "headline": "…" } }] }
```

- Each field is in the asked language, or the site's main one; categories and tags come as they are.
- A **public** collection answers anyone, unless visitors may not view its site. Answers may be kept for a minute.
- The people who edit its site or library can always read it: signed in, or with a token given the content scope. A collection that is not public answers only them.
- Anyone else is told there is no such collection.
- The address has no cross-origin access: call it from a server, or from a page of the same portal.
- `public` decides only who reads this address; pages show a collection as they show any content.

## Show it on a page

A placement of the portal's content widget shows a site's published entries of one type: a list of the newest, one entry, a collection, or a library's entries. See the [config example](#a-content-widget-on-a-page).

A value that no longer fits its field, after the type changed, is left out rather than breaking the page.

## Display pages

A page gives each published entry of a type its own address with `display` (see the [config example](#a-display-page)).

- An entry is at the page's address followed by its own: `/stire/program-de-iarna`, `/en/stire/program-de-iarna`. The page's own address shows nothing.
- **`current: true`** shows the entry the address names; with **`field`**, only that field. These placements go only on a display page, or in a page template.
- The page takes the entry's title. In the portal's own look the entry then leaves its title out, since the page's heading says it.
- The home page and a dashboard cannot be display pages. A site has one per type and library. The sitemap lists every published entry's address of a display page visitors may see.

See [Display pages](/portal/console/pages/#display-pages) in the console.

## Config example

### A content type's file

In `content/types/<id>.yaml`:

```yaml
name: { ro: Știri, en: News }
title: headline
fields:
  - { id: headline, type: text, label: { ro: Titlu, en: Headline }, required: true, maxLength: 200 }
  - { id: date, type: date, label: { ro: Data, en: Date } }
  - { id: body, type: richtext, label: { ro: Text, en: Text } }
  - { id: photo, type: image, label: { ro: Fotografie, en: Photo } }
  - id: kind
    type: select
    label: { ro: Fel, en: Kind }
    options:
      - { value: event, label: { ro: Eveniment, en: Event } }
      - { value: notice, label: { ro: Anunț, en: Notice } }
```

- `name`: the type's name, in Romanian and English.
- `title`: the text field that names an entry in lists.
- `fields`: each with an `id`, a `type` from the [field types](#field-types) and a `label` in both languages. `required: true` must be filled in to publish; `maxLength` limits a text.
- `options` of a `select`: each with a `value` and a `label`.
- `blog: true` would make the type a [blog](/portal/sites/blogs/).

### A template

In the same file, a `template` places the fields:

```yaml
template: >-
  <div class="news">
    <h2><portal-field name="headline"></portal-field></h2>
    <p class="date"><portal-field name="date"></portal-field></p>
    <portal-field name="body"></portal-field>
  </div>
```

With a display page, `<portal-entry-link>` links what it holds to the entry's address:

```yaml
template: >-
  <portal-entry-link class="more"><h2><portal-field name="headline"></portal-field></h2></portal-entry-link>
```

- `<portal-field name="…">` is where the field of that name goes.
- `<portal-entry-link>` links what it holds to the entry; it takes a `class` and holds no other link.

### A vocabulary's file

In `content/vocabularies/<id>.yaml`:

```yaml
name: { ro: Teme, en: Topics }
types: [news, events]   # the content types it sorts; left out, all of them
multiple: true          # an entry may take several of its categories; false allows one
categories:
  - id: roads
    name: { ro: Drumuri, en: Roads }
    children:
      - { id: winter, name: { ro: Iarna, en: Winter } }
  - { id: "2024", name: { ro: "2024", en: "2024" } }
```

- `types`: the content types it sorts; left out, all of them.
- `multiple`: `true` lets an entry take several of its categories; `false` allows one.
- `categories`: each with an `id` and a `name` in both languages, and `children` to nest.

### A library's file

In `content/libraries/<id>.yaml`:

```yaml
name: { ro: Comune, en: Shared }
sites: [main, turism]                    # left out, every site; [] none
permissions: { edit: [group:Comunicare] }
```

- `sites`: the sites the library serves; left out, every site; `[]`, none.
- `permissions.edit`: who edits the library, besides the administrators.

### A collection's file

In `content/collections/<id>.yaml`:

```yaml
name: { ro: Pe prima pagină, en: Front page }
type: news
site: main               # or library: shared
entries: [deszapezire, parc-nou]                      # hand-picked, in this order
# or: query: { category: topics/roads, tag: iarna, order: newest, limit: 10 }
public: true             # its address answers anyone; left out, only the shelf's editors
```

- `type`: the content type of its entries.
- `site` or `library`: where the entries are.
- `entries`: the hand-picked entries, in this order; or `query` to pick by `category`, `tag`, `order` and `limit`.
- `public`: whether its address answers anyone; left out, only the shelf's editors.

### A content widget on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
- id: latest-news
  app: portal
  widget: content
  preferences: { type: news, list: { limit: 5, order: newest } }
```

- **`list`**: the newest entries, `limit` from 1 to 50 (10 when left out), `order` `newest`, `oldest` or `title`. `category: topics/roads` shows only the entries in that category or one under it, and `tag: iarna` only those with the tag; both together show the entries that have both.
- **`entry`**: one entry, by its address: `preferences: { type: news, entry: program-de-iarna }`.
- **`collection`**: a [collection](#collections), alone: `preferences: { collection: front }`.
- **`library`**: the entries of a library instead of the site's own, on a site the library serves: `preferences: { type: news, library: shared, list: { limit: 5 } }`.

### A display page

In a page's file:

```yaml
path: /stire
title: { ro: Știre, en: News item }
layout: one-column
display: { type: news }          # add library: shared for a library's entries
regions:
  main:
    - { id: entry, app: portal, widget: content, preferences: { current: true } }
  aside:
    - { id: photo, app: portal, widget: content, preferences: { current: true, field: image } }
```

- `display`: the content type whose entries the page shows; add `library` for a library's entries.
- `current: true`: shows the entry the address names; with `field`, only that field.

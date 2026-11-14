---
title: Content types
description: The files that define content types, vocabularies, libraries and collections, and the page settings that show them.
---

The configuration behind [Content types](/portal/sites/content-types/). That page covers what a type holds, how an entry looks, and how entries are sorted, shared and shown.

## A content type's file

Each content type is a file in the portal's files, `content/types/<id>.yaml`, shared by all the sites. Administrators can also build them in the console's [Content types](/portal/console/content-types/) page.

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
- `blog: true` makes the type a [blog](/portal/sites/blogs/): its entries are posts, each by the person who wrote it.
- A field's `id` is lower-case letters, digits and hyphens. A field with `required: true` must be filled in, in every language, to publish.
- A portal has at most 100 content types, each with at most 50 fields.

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

## A template

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
- A `template` takes what a site's [layouts](/portal/sites/layouts/) take.

## A vocabulary's file

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
- A category's `id` is lower-case letters, digits and hyphens, unique in its vocabulary. Categories nest at most five levels deep, 500 per vocabulary; a portal has at most 20 vocabularies.
- A category is named by its vocabulary and its id: `topics/winter`.

## A library's file

In `content/libraries/<id>.yaml`:

```yaml
name: { ro: Comune, en: Shared }
sites: [main, turism]                    # left out, every site; [] none
permissions: { edit: [group:Comunicare] }
```

- `sites`: the sites the library serves; left out, every site; `[]`, none.
- `permissions.edit`: who edits the library, besides the administrators.
- Who edits a library: the people and groups its `edit` names, those given it on [Access](/portal/console/access/), and the administrators. A site's editors do not, unless named.
- A site the portal no longer has is forgotten. A library left with no site serves none.
- Removing a library keeps its entries out of reach; saving a library again under the same id brings them back, published ones included.
- At most 20 libraries.

## A collection's file

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
- A hand-picked collection names up to 50 entries by their address, each once. An entry not published yet is left out until it is.
- A query works as a content list's: `category`, `tag`, `order` and `limit`.
- A page shows it with `preferences: { collection: front }`, and nothing else, on its site or a site its library serves.
- At most 100 collections.

## Reading a collection

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

## A content widget on a page

A placement of the portal's `content` widget shows a site's published entries of one type: a list of the newest, one entry, a collection, or a library's entries.

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
- id: latest-news
  app: portal
  widget: content
  preferences: { type: news, list: { limit: 5, order: newest } }
```

- **`list`**: the newest entries, `limit` from 1 to 50 (10 when left out), `order` `newest`, `oldest` or `title`. `category: topics/roads` shows only the entries in that category or one under it, and `tag: iarna` only those with the tag; both together show the entries that have both.
- **`entry`**: one entry, by its address: `preferences: { type: news, entry: program-de-iarna }`.
- **`collection`**: a [collection](/portal/sites/content-types/#collections), alone: `preferences: { collection: front }`.
- **`library`**: the entries of a library instead of the site's own, on a site the library serves: `preferences: { type: news, library: shared, list: { limit: 5 } }`.

## A display page

A page gives each published entry of a type its own address with `display`. In a page's file:

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
- `current: true`: shows the entry the address names; with `field`, only that field. These placements go only on a display page, or in a page template.

See [Display pages](/portal/console/pages/#display-pages) in the console.

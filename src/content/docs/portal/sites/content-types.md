---
title: Content types
description: Define the kinds of content a portal's sites hold, their fields, and how each entry looks on a page.
---

A content type says what a kind of entry holds, such as a news item's headline, date and text. The people who edit a site write entries in the console's [Content](/portal/console/content/) page; pages show them with the content widget.

## A content type

Each content type is a file in the portal's files, `content/types/<id>.yaml`, shared by all the sites. Administrators can also build them in the console's [Content types](/portal/console/content-types/) page:

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

- **`name`** and each field's **`label`** are in Romanian and English.
- **`title`** names the text field that names an entry in lists.
- A field's **`id`** is lower-case letters, digits and hyphens. **`required: true`** must be filled in, in every language, to publish.
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

## How an entry looks

Without a template, an entry shows its title as a heading, then each other field.

A **`template`** places the fields in markup of your own. It takes what a site's [layouts](/portal/sites/layouts/) take, and `<portal-field name="…"></portal-field>` where a field's value goes:

```yaml
template: >-
  <div class="news">
    <h2><portal-field name="headline"></portal-field></h2>
    <p class="date"><portal-field name="date"></portal-field></p>
    <portal-field name="body"></portal-field>
  </div>
```

A rich text field holds paragraphs and other blocks. It stands directly in a block such as a `div` or a `section`, never inside a paragraph or a heading.

Each entry is an `article` with the class `portal-content`; a list of entries is a `div` with the class `portal-content-list`. Style them in the site's layout stylesheet.

## Show it on a page

A placement of the portal's content widget shows a site's published entries of one type:

```yaml
- id: latest-news
  app: portal
  widget: content
  preferences: { type: news, list: { limit: 5, order: newest } }
```

- **`list`**: the newest entries, `limit` from 1 to 50 (10 when left out), `order` `newest`, `oldest` or `title`.
- **`entry`**: one entry, by its address: `preferences: { type: news, entry: program-de-iarna }`.

A value that no longer fits its field, after the type changed, is left out rather than breaking the page.

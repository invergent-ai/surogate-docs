---
title: Content types
description: Build the kinds of content the portal's sites hold, their fields and how an entry looks, in the console.
---

**Content types** builds what each kind of entry holds, such as a news item's headline, date and text. The people who edit a site then write entries on the [Content](/portal/console/content/) page.

**Content types** is for administrators, on a portal whose site files the portal keeps. Every save is a [version](/portal/console/versions/) you can undo.

## The list

Each content type shows its name, its id and how many fields it has. **Edit** opens it; **New content type** starts one. A content type whose file cannot be read is marked **Cannot be read**: **Remove** is all it offers.

## Build a content type

- **Id**: lower-case letters, digits and hyphens, such as `stiri`. It is fixed once saved.
- **Name**: one in Romanian and one in English.
- **Fields**: each has an id, a type and a label in each language.
  - **Must be filled in to publish**: an entry cannot be published without it, in every language.
  - **Written in each language**: for text, longer text, rich text, links and images. Untick it for a field that is the same in every language, such as a code.
  - **Most characters**, for text and longer text.
  - **Options**, for a choice from a list: each has a value (lower-case letters, digits and hyphens) and a label in each language.
  - **Move up**, **Move down** and **Remove** arrange them; **Add field** adds one.
- **Title**: the text field that names an entry in lists.
- **Template**: optional HTML that places each field with `<portal-field name="field id"></portal-field>`. Left empty, an entry shows its title, then each field. See [Content types](/portal/sites/content-types/#how-an-entry-looks) for what it may hold.

**Save** stays off until something changed and everything needed is filled in; the editor says what is missing.

## Change a content type

A saved field keeps its id, its type and whether it is written in each language, so entries keep their values. You can change its labels, whether it must be filled in, its most characters and its options. To change a field's type, remove it and add a new one: a field you remove loses its values the next time each entry is saved.

While you build a new field, changing its type clears what the new type does not take, such as a list's options.

## Remove a content type

**Remove** asks first. While a page shows the content type, the confirmation names the pages: take it off them in the [page editor](/portal/console/pages/) first.

The content type's entries stay. They show nowhere, and the Content page lists them, under the type's id, for deletion. A new content type saved with the same id brings them back.

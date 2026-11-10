---
title: Pages
description: Build a site's pages in the console, with its page tree and an editor for each page's title, address, layout and content.
---

**Pages** builds the portal's sites in the console. It shows each site's pages as a tree. For each page you set its title, its address and its layout, and arrange what each part of the layout holds. Every save is a [version](/portal/console/versions/) you can undo.

**Pages** is for administrators, on a portal whose site files the portal keeps. It is not in the menu otherwise.

## The page tree

Each site lists its pages by address. A page sits under the page above it: `/servicii/taxe` under `/servicii`. The home page is marked **Home page**. A page file the portal cannot read is marked **Cannot be read**; fix or remove it where the site's files are edited.

- **Edit** opens a page in the editor.
- **New page** opens the editor for a new page of that site.

## Edit a page

- **Address**: where the page is, such as `/despre`. The site's home page keeps its address. Changing another page's address asks first: links to the old address stop working, and settings made on the page itself start again.
- **Title**: one per language of the site.
- **Layout**: the portal's `one-column` or `two-column`, or one of the site's own [layouts](/portal/sites/layouts/).

**Search and sharing** sets how [search engines and link previews](/portal/sites/seo/) show the page: a description in each language, a share image, and **Hide from search engines**.

Under them, each part of the layout lists what it holds, in order:

- **Add text** adds a text block, written in HTML for each of the site's languages. It holds what an [HTML block](/portal/sites/layouts/#an-html-block) may hold.
- **Add content…** shows the site's [content](/portal/console/content/#show-content-on-a-page) of one type: its newest entries, or one entry.
- **Add a widget…** adds one of the apps' widgets. When a widget needs a setting to work, the editor asks for it; its other settings are made on the page itself, from its menu.
- **Remove** takes a block or widget off the page.

**Save** stays off until something changed and every title and text is filled in.

## Move what a page holds

Drag a block or widget by its handle onto another one to put it before it, or onto **Drop here** to put it at the end of a part. With the keyboard, use **Move up**, **Move down**, or **Move to** to send it to the end of another part.

When you choose a layout without one of the page's parts, what that part held moves to `main`, and the editor says so.

## Fragments

A fragment is text kept once and shown on many pages, such as opening hours or a contact box. Change it once, and every page that holds it changes.

Each site lists its fragments under its pages. **New fragment** asks for:
- an id, such as `program`: lower-case letters, digits and hyphens, fixed once saved;
- a name and the text, written in HTML, in each of the site's languages.

**Edit** changes a fragment. In the page editor, **Add a fragment…** places one in a part of the page. It shows as **Fragment:** and its name, with nothing to fill in.

**Remove** takes a fragment off the site. When pages or templates still hold it, the confirmation names them, and the removal is refused until the fragment is taken off them.

## Page templates

A page template is a page's starting point: a layout and what its parts hold.

- **Save as template**, in the page editor, keeps the page's layout and blocks as a template. It asks for an id and a name in each language. The page's address and titles stay with the page.
- When you make a **New page**, **Start from** offers the site's templates.
- **Remove** takes a template off the site; pages made from it keep what they hold.

## Display pages

A display page shows one entry at a time: each published entry of a content type gets its own address, the page's address followed by the entry's. A display page at `/stire` shows the entry `program-de-iarna` at `/stire/program-de-iarna`.

1. Make a page, such as `/stire`, and choose a type under **One entry at a time**, **Shows one entry of**. Choose a type *from* a library to show that library's entries.
2. Under **Add content…** in a part of the page, choose **The entry shown here**. It shows the whole entry. To show one field alone, such as its image in a wide part, choose it under **Part of the entry**.
3. Add anything else the page needs, such as a list of the newest entries beside it.

What visitors see:
- The page takes the entry's title, in their language or else in the site's main one. Search engines and link previews see the entry's address, title and first image.
- The page's own address shows nothing: only the entries' addresses do. In the page tree it shows as `/stire/…`.
- A draft, or an address no entry has, shows the site's "page not found".
- Lists of the type on the site link each entry's title to its address.
- If a page of the site has the same address as an entry, visitors see the page.

The home page and personal dashboards cannot be display pages, and a site has one display page per type and library. Choosing **No entries** removes the parts that showed the entry. **Preview** shows a display page with the newest published entry.

Apps on a display page are told the page's address, not which entry it shows.

## Personal dashboards

A page can be a personal dashboard: each person signed in arranges it for themselves. Under **Personal dashboard** in the editor, tick **People arrange this page for themselves**, then tick what they may add: the apps' widgets that need no settings, and the site's fragments.

A dashboard is only for people signed in. If the page was open to everyone, ticking the box lets only people signed in see it.

On the page, people see **Customize this page**. There they can:
- move a section up or down, or to another part of the page;
- remove a section;
- add one of the sections the page offers;
- go back to the page as it is made.

Each person's changes are theirs alone. A section you add to the page later shows for everyone, where you put it. A section you take off the page goes from everyone's dashboard. A person holds at most 30 sections.

Sections on a dashboard have no menu on the page itself: set their settings here, in the editor. An administrator seeing the portal as someone sees that person's dashboard but cannot change it.

## Preview before saving

**Preview** shows the page as it is being edited, before anything is saved, as visitors would see it. Choose **Phone**, **Tablet** or **Desktop** to see it at that width, and the language to see it in. Press **Preview** again after more changes.

Only the portal's administrators can open a preview, and only for a quarter of an hour. A preview shows only what anyone may see, and is never shown to search engines. An app that is not live yet shows as waiting.

When the page cannot be shown as it is, the editor lists what is wrong, as it does when a save is refused.

## When a save is refused

- **Problems**: the save would break the site, so nothing is saved. The editor lists what is wrong.
- **Someone saved this site meanwhile**: another administrator saved first. **Load the newest** shows the page as it is now. Your changes to it are lost, so the editor asks first.

**Remove page** takes the page off the site, after asking. The home page cannot be removed. Undo the version on [Versions](/portal/console/versions/) to bring a page back.

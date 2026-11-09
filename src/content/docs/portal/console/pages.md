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

Under them, each part of the layout lists what it holds, in order:

- **Add text** adds a text block, written in HTML for each of the site's languages. It holds what an [HTML block](/portal/sites/layouts/#an-html-block) may hold.
- **Add a widget…** adds one of the apps' widgets. When a widget needs a setting to work, the editor asks for it; its other settings are made on the page itself, from its menu.
- **Remove** takes a block or widget off the page.

**Save** stays off until something changed and every title and text is filled in.

## Move what a page holds

Drag a block or widget by its handle onto another one to put it before it, or onto **Drop here** to put it at the end of a part. With the keyboard, use **Move up**, **Move down**, or **Move to** to send it to the end of another part.

When you choose a layout without one of the page's parts, what that part held moves to `main`, and the editor says so.

## When a save is refused

- **Problems**: the save would break the site, so nothing is saved. The editor lists what is wrong.
- **Someone saved this site meanwhile**: another administrator saved first. **Load the newest** shows the page as it is now. Your changes to it are lost, so the editor asks first.

**Remove page** takes the page off the site, after asking. The home page cannot be removed. Undo the version on [Versions](/portal/console/versions/) to bring a page back.

---
title: User guides
description: In-app walkthroughs that show people around a page, step by step.
---

A user guide walks people through a page, one step at a time. Each step has a title and a text, and can point at a part of the page, which is outlined and scrolled into view. People move with **Next** and **Previous**, and end with **Finish** or **Close**.

## What people see

Here a guide starts on someone's first visit to the home page. Its first step points at the main menu:

![The home page of a site with a guide's first step open under the main menu, which is outlined: "Main menu", its text, "1 / 5", and the Next and Close buttons.](../../../../assets/screenshots/portal-guide-step.png)

- The step's box sits next to the part of the page it is about; a step that points at nothing shows on its own.
- **Escape** closes a guide when it has the focus.
- A guide's text is part of its pages: everyone who may see a page can read the guides on it.

## Write a guide

A guide has a name, in every language. It applies to the sites and pages it names; left out, it applies on every site or every page. Each page it names must be a page of one of the guide's sites. It starts when asked for, which is the default, or by itself the first time someone opens one of its pages.

A guide has at most 30 steps. Each step has a title and a text in every language, as plain text, and can point at a part of the page. A step that points at nothing, or at a part that is not found, shows on its own.

The console does not write guides yet. For now, this is set in the site's configuration: see [Developer: User guides](/portal/developer/guides/#a-guides-file).

## Start a guide

A guide starts:

- at its page's address with `?guide=<id>`, for example in a link from a help page;
- from a form, with the action that starts a guide ([UI actions](/portal/sites/actions/#ui-actions)), on a page that shows the form and that the guide applies to. A form opened at its own address starts no guide;
- by itself on a first visit, when the guide says so.

Each browser remembers the guides it has shown by themselves and those it finished: a first-visit guide does not start again there, even when the person left the page without closing it. When a page has several first-visit guides, the first by id starts. A browser that keeps nothing never starts a guide by itself.

The console does not add this action to a form yet. For now, this is set in the site's configuration: see [Developer: User guides](/portal/developer/guides/#start-a-guide).

## In the console

[Guides](/portal/console/guides/) lists the portal's guides for administrators: each guide's name and id, how it starts, its number of steps, and the sites and pages it applies to.

![The console's Guides page: the guide "Welcome to the site", marked "On the first visit", with 5 steps, on the site primaria at /.](../../../../assets/screenshots/portal-guides-console.png)

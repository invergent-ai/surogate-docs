---
title: User guides
description: In-app walkthroughs that show people around a page, step by step, written in the portal's files.
---

A user guide walks people through a page, one step at a time. Each step has a title and a text, and can point at a part of the page, which is outlined and scrolled into view. People move with **Next** and **Previous**, and end with **Finish** or **Close**.

## A guide

A guide lives in `guides/<id>.yaml`:

```yaml
name:
  ro: Bun venit
  en: Welcome
sites: [main]
pages: [/, /servicii]
start: first-visit
steps:
  - title:
      ro: Căutați aici
      en: Search here
    text:
      ro: Scrieți ce căutați și apăsați Enter.
      en: Type what you look for and press Enter.
    target: "[data-placement=search]"
  - title:
      ro: Gata
      en: That's all
    text:
      ro: Puteți reporni ghidul oricând.
      en: You can start the guide again any time.
```

- `sites` and `pages` say where the guide applies. Left out, it applies on every site or every page.
- `start` is `manual`, the default, or `first-visit`: the guide starts by itself the first time someone opens one of its pages.
- `steps`: at most 30, each with a `title` and a `text` in every language, as plain text.
- `target` is a CSS selector for the part of the page the step is about, such as `#main` or `[data-placement=intro]`; each part placed on a page carries its id as `data-placement`. A step whose target finds nothing shows on its own.

A guide can be written in JSON instead: the file is read the same way. To bring in a guide made elsewhere, save its JSON as `guides/<id>.yaml`.

## Start a guide

A guide starts:
- at its page's address with `?guide=<id>`, for example in a link from a help page;
- from a form, with the `startGuide` action ([UI actions](/portal/sites/actions/#ui-actions));
- by itself on a first visit, when it says `start: first-visit`.

Each browser remembers the guides it finished, and a first-visit guide does not start again there. When a page has several first-visit guides, the first by id starts. A browser that keeps nothing never starts a guide by itself.

A guide's text is part of its pages: everyone who may see a page can read the guides on it.

---
title: User guides
description: A guide's file, its steps and targets, and the form action that starts a guide.
---

The configuration behind [User guides](/portal/sites/guides/). That page covers what people see, how a guide starts and where the console lists them.

## A guide's file

A guide lives in its own file, `guides/<id>.yaml`. This one is `guides/welcome.yaml`, so its id is `welcome`:

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

- `name`: the guide's name, in every language.
- `sites` and `pages` say where the guide applies. Left out, it applies on every site or every page. Each page must be a page of one of the guide's sites.
- `start` is `manual`, the default, or `first-visit`: the guide starts by itself the first time someone opens one of its pages.
- `steps`: at most 30, each with a `title` and a `text` in every language, as plain text.
- `target` is a CSS selector for the part of the page the step is about, such as `#main` or `[data-placement=intro]`; each part placed on a page carries its id as `data-placement`. A step whose target finds nothing shows on its own.

A guide can be written in JSON instead: the file is read the same way. To bring in a guide made elsewhere, save its JSON as `guides/<id>.yaml`.

## Start a guide

A guide starts at its page's address with `?guide=<id>`, for example in a link from a help page.

A form starts a guide with the `startGuide` action ([UI actions](/portal/sites/actions/#ui-actions)), which takes the guide's id as `guide`. The page must show the form, and the guide must apply to the page. A form opened at its own address starts no guide.

A guide with `start: first-visit` starts by itself on a first visit.

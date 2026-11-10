---
title: Search settings
description: Tune how a site's search weighs titles and text, which words mean the same, which results come first, and what it leaves out.
---

**Search** in the console tunes a site's [search](/portal/sites/search/). It is for the tenant's administrators. Choose the **Site** when the tenant has several.

## Weights

**Weight of the title** and **Weight of the text**, from 1 to 10, say how much a word found in a page's or an entry's title counts against one found in its text. The portal's own are 3 and 1: titles first.

## Synonyms

One box per language. Each line is a group of words or phrases that mean the same, separated by commas:

```
primărie, consiliu local, municipalitate
taxe, impozite
```

A search for any of them finds pages with the others too. Diacritics and a word's other forms count: `primăriei` finds what `consiliu local` finds. Use letters, digits, spaces, hyphens and apostrophes only. A change works at once.

## Pinned results

One per line: a search, then `=` and up to five addresses shown first, in that order:

```
taxe = /taxe, /plata-online
```

They come first on the first page of results for that search, when no filter narrows it. A pinned address someone may not see, or one that is gone, is simply not shown.

## What search leaves out

- **Pages left out**: one address per line. `/intern/*` leaves out `/intern` and everything under it.
- **Content left out**: tick the content types search never finds.

## Typos and word starts

- **A word with a typo counts**: on by default, so `noembrie` finds `noiembrie`.
- **A word ending in * finds every word it starts**: off by default. On, `noiem*` finds `noiembrie`; the start needs three letters at least.

**Save** keeps the settings as a new version of the site's files. **Use the portal's own** goes back to the defaults. Settings the portal cannot take are refused, and the page says what to change.

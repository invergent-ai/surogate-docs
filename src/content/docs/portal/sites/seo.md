---
title: Search engines and link previews
description: How a site's pages are described to search engines and when they are shared, and what crawlers are told.
---

Every page of a site tells search engines and link previews what it is. The portal writes all of this from the site's files, so a page needs nothing more than its title to be found. A site can say more.

## What each page says

- **Its description**: the page's own, else the site's.
- **Its address**: one address per language. The home page's address is the site's root, such as `https://example.ro/` and `https://example.ro/en`.
- **The same page in the site's other languages**, so search engines show each visitor theirs.
- **How it looks when shared**: its title, the site's name, its description and its image.
- **Structured data** about the site and the page, and about the organization behind the site when it names one.

## Describe a page

In the site's files, a page's `seo` holds:

```yaml
seo:
  description: { ro: Programul și serviciile primăriei., en: The city hall's hours and services. }
  image: https://img.example.ro/share.png
  noindex: false
```

- **`description`**: at most 300 characters. Once it is given in one language, give it in all of the site's languages.
- **`image`**: an `https:` address. It shows when the page is shared.
- **`noindex: true`**: asks search engines not to list the page.

Administrators can set these in the console too, under **Search and sharing** in the [page editor](/portal/console/pages/).

## Describe a site

A site's `site.yaml` can say the same for all its pages, and who is behind it:

```yaml
seo:
  description: { ro: Site-ul Primăriei Exemplu., en: Example City Hall's site. }
  image: https://img.example.ro/share.png
  organization:
    name: Primăria Exemplu
    url: https://example.ro
    logo: https://img.example.ro/logo.png
  index: true
```

A page's own description and image win over the site's. **`index: false`** asks search engines to leave the whole site out.

## What crawlers are told

Each address the portal serves answers two files:

- **`/robots.txt`** keeps crawlers away from the portal's own paths, but not from what pages need to show, and names the sitemap.
- **`/sitemap.xml`** lists every page anyone may see, in each language, with its other-language addresses. It leaves out:
  - pages only signed-in people may see;
  - pages with `noindex`;
  - the pages of a site with `index: false`.

Previews are never listed: their robots.txt keeps every crawler out.

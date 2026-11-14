---
title: Search engines and link previews
description: A page's and a site's seo in their files, which search engines and link previews read.
---

The configuration behind [Search engines and link previews](/portal/sites/seo/). That page covers what each page says to search engines and link previews, and what crawlers are told.

## A page's `seo`

In the site's files, a page's `seo` holds the following. Administrators can set these in the console too, under **Search and sharing** in the [page editor](/portal/console/pages/). In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
seo:
  description: { ro: Programul și serviciile primăriei., en: The city hall's hours and services. }
  image: https://img.example.ro/share.png
  noindex: false
```

- `description`: at most 300 characters. Once it is given in one language, give it in all of the site's languages.
- `image`: an `https:` address. It shows when the page is shared.
- `noindex: true` asks search engines not to list the page.

## A site's `seo`

A site's `site.yaml` can say the same for all its pages, and who is behind it. A page's own description and image win over the site's. In `site.yaml`:

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

- `description` and `image`: the same for all the site's pages; a page's own win.
- `organization`: who is behind the site, with its `name`, `url` and `logo`.
- `index: false` asks search engines to leave the whole site out.

---
title: Reading web pages
description: The fetchPage, cleanHtml, crawlSite, crawlBatch and removeCrawl actions, as the site's configuration writes them.
---

What these do, and who may run them, are on [Reading web pages](/portal/sites/web-pages/).

## The actions

```yaml
- type: fetchPage
  url: vars.address
  into: page
- type: cleanHtml
  html: vars.reply.body
  into: content
- type: crawlSite
  crawl: city-news
  url: '"https://www.example.ro/news"'
  paths: '["/news"]'
  maxPages: "500"
  recrawlHours: "24"
- type: crawlBatch
  crawl: city-news
  size: "5"
  into: batch
- type: each
  list: vars.batch.pages
  as: page
  actions:
    - type: createRecord
      model: news
      values:
        title: vars.page.title
        body: vars.page.html
        source: vars.page.url
- type: removeCrawl
  crawl: city-news
```

- `fetchPage` keeps `{ok: true, url, status, title, description, image, published, text, html, links, truncated}`, or `{ok: false, url, status, error}`, with `blocked: true` when robots.txt keeps the portal out and `retry: true` when trying later may work. `html` holds the main content's first blocks up to 64 KB, with `truncated: true` when more was left out; `links` are the page's absolute addresses.
- `cleanHtml` keeps `{title, text, html, truncated}`.
- `crawlSite` keeps `{crawl, pages}` (the pages queued); `crawlBatch` keeps `{pages: [{url, title, description, image, published, text, html, truncated}], left}` and needs `into`; `removeCrawl` keeps `{done}`.
- `crawl` is lower-case letters, digits and hyphens, written as it is. `paths` is a list of 1 to 20 paths starting with `/` (`["/"]` unless given); `maxPages` 1 to 1,000 (200 unless given); `recrawlHours` 1 to 720; `size` 1 to 5 (5 unless given).

A job reading a site every 15 minutes, as a person who may read it (without `runAs`, a job acts as a visitor and reads nothing):

```yaml
# jobs/city-news.yaml
trigger:
  every: 15m
site: main
runAs: user:editor@example.ro
actions:
  - type: crawlSite
    crawl: city-news
    url: '"https://www.example.ro/news"'
    paths: '["/news"]'
  - type: crawlBatch
    crawl: city-news
    into: batch
  - type: each
    list: vars.batch.pages
    as: page
    actions:
      - type: createRecord
        model: news
        values:
          title: vars.page.title
          body: vars.page.html
```

## Load checks

- A form with `public: true`, or an endpoint with `access: public` or a `cache`, may not use them: `crawler_public`.
- A job not started by time (`every`, `at`, `daily`, `cron`) may not `fetchPage`, `crawlSite` or `crawlBatch`, in its actions, its `onError` and the endpoints and flows they reach: `crawler_untrusted`.

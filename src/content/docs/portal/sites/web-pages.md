---
title: Reading web pages
description: Read another site's pages from jobs, one page or a whole site batch by batch, and keep their title, text and main content.
---

The portal's **Web pages** extension lets steps read pages of other sites. A job fills a collection with another site's news every night; an administrators' form reads the page someone names and keeps its text. As with every extension, it is open to every tenant of the portal.

## The actions

- **Read a web page** reads one page and keeps its address (after any redirects), its title, description, image and date, its text, its main content and its links. What cannot be read comes back with the reason, so the next steps can decide what to do: the site's robots.txt asks the portal not to, the address is not an HTML page, the site is busy or does not answer.
- **Keep a page's main content** takes HTML a step already has (from a connector, say) and keeps its title, text and main content. It reads nothing from the web.
- **Start reading a site** names a site to read page by page: a name for it in the portal, its first page, and, if you like, the paths to stay under (`/news` keeps `/news/...`, never `/newsletter`), the most pages to read (200 unless you say, up to 1,000), and after how many hours to read pages again. Naming it again with other settings changes it; another site or other paths start it over.
- **Read a site's next pages** reads the next pages of a site being read, at most five at a time, and keeps them as a list, with how many are left. Add a **For each** step after it to keep every page, in a collection for instance.
- **Stop reading a site** forgets it and the pages it found.

The main content is the page's `<main>`, else its largest article, else its body, without menus, headers, footers, forms, scripts, styles and hidden parts. It is kept as the portal's own markup, as a rich text field holds it: headings, paragraphs, lists, tables, images and links, every link marked `nofollow`. Text and main content are each kept up to 64 KB.

## How a site is read

A site is read the way a polite reader reads it:

- **Its own pages only:** links are followed on the same site (scheme, host and port), under the paths given, at most ten links deep. Links to other sites, links marked `nofollow`, pages that ask not to be followed, and files such as PDFs and images are left alone. Sitemaps are not read.
- **Its robots.txt** is honoured for the portal (`SurogatePortal`), else for every reader (`*`); a `Crawl-delay` of up to 10 seconds is kept.
- **One page a second** from each site, across every server of the portal.
- **A busy site** (it answers 429 or 5xx, or does not answer) is tried again after 1, 5 and 30 minutes, then given up.
- Each page is read once, even when two jobs read the same site at once. Tracking parameters (`utm_...`, `fbclid`, `gclid`) and session parameters are dropped from addresses, so one page is not read twice under two names.

A run has a time limit and takes at most 20 extension actions, so a large site is read over many runs: a job every 15 minutes reading the next pages until none are left, then again when pages are read again.

The portal tells sites who it is: `SurogatePortal/1 (+https://docs.surogate.ai/portal/sites/web-pages/)`.

## Who may do what

- **Administrators** and **jobs** read pages and sites. A job runs as a person (**Runs as**); one that runs as no one acts as a visitor and reads nothing.
- **A job started by anything but time** (a record, a person's change, mail, a payment, an app's event, a page request) does not read pages or sites: what started it was written by others, and could point the portal anywhere. Read the web from jobs on a schedule.
- **Signed-in people** only keep the main content of HTML a step already has.
- **Forms anyone may send and endpoints anyone may call** use none of these actions: anyone could make the portal fetch for them.

The portal never reads addresses on private networks, before or after a redirect.

## Treat what you read as untrusted

A page says whatever its author wrote. Keep what you read as data: show it, store it, search it. Do not hand it to an assistant, a mail or a redirect as if it were yours to trust: a page can say "ignore your instructions" or carry a link anywhere. The main content is cleaned of scripts and styles, but its words are the other site's.

## Limits

- At most 1,000 pages an hour on a tenant, between every action and job. A page robots.txt keeps the portal from does not count.
- A page is read only when it is HTML, at most 1 MB, in at most three redirects.
- A site read is at most 1,000 pages; a tenant keeps at most 50,000 pages of all its sites.
- One batch's pages are kept up to 900 KB in all; pages past it wait for the next batch.
- HTML to clean is at most 512 KB.

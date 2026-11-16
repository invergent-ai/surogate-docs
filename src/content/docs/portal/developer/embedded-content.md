---
title: "Developer: Embedded content"
description: The site's list of embeddable addresses and the embed block in the site's files.
---

For what people do in the console, see [Embedded content](/portal/sites/embedded-content/).

## The site's list

In `sites/<site>/site.yaml`:

```yaml
embeds:
  - name: Reporting dashboards
    prefix: https://answers.example.ro/dashboard/
  - name: Public reports
    prefix: https://answers.example.ro/public/
    public: true
```

- `name`: what the console calls it, 1 to 100 characters.
- `prefix`: an https address with no login, query or fragment, whose path is `/` or ends with `/`. At most 50 entries, none twice.
- `public`: true lets pages anyone may see use it; false when left out.

## The block

In a page's file:

```yaml
regions:
  main:
    - id: report
      app: portal
      widget: embed
      permissions:
        view: ["group:Case workers"]
      preferences:
        url: https://answers.example.ro/dashboard/12
        title: { ro: Tablou de bord, en: Dashboard }
        height: 900
        newWindow: true
```

- `url`: required. An https address that falls under a listed prefix. It may carry a query and a fragment of your own; the portal adds nothing. A login in it, a backslash or an encoded slash (`%2f`, `%5c`) is refused.
- `title`: required, `{ ro, en }` with at least one language, each at most 200 characters.
- `height`: 200 to 4,000, 800 when left out.
- `newWindow`: whether the link that opens the address in a window of its own shows, true when left out.

A page is public when its site, the page and the block all let everyone view. On a public page the address must fall under a prefix with `public: true`; a check of the files refuses the block otherwise, with the problem `embed_preference` (reason `public`). An address under no prefix is the reason `not_allowed`.

## Taking an address away

Saving a site's settings without an address that a page's block still shows is refused, naming the pages. The settings request takes `removeEmbeds: true` to take, in the same version, the `embed` blocks of the site's pages that no longer fall under a listed prefix, wherever they are in a page's regions; nothing else of the pages changes. The console offers it as "Also take the Embedded content blocks off those pages when I save".

## The portal's own hosts

The frame has scripts and its own origin (`allow-scripts allow-same-origin`), which is no sandbox for a page of the portal's own: it would share the portal's cookies and scripts. So an address on one of the portal's hosts (a host a site is served on, or the one the page is asked at) is never framed. Saving a site's settings with such a prefix is refused (`400`, `embedOwnHost`), and a block whose address is one is not rendered for visitors (editors see "The address is no longer allowed on this site.").

## What the page sends

The frame is `<iframe loading="lazy" referrerpolicy="strict-origin-when-cross-origin" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox allow-downloads" allow="fullscreen">`, with `src` the address as the browser reads it. The response's content security policy carries `frame-src 'self' <origin> …`: one origin for each frame the page shows to that person, then the origin of each module of the approved apps the page loads, so a frame an app opens of its own origin keeps working. The page keeps no other `frame-src` than that; a page with no embedded content has none, and no `frame-src` at all, as before.

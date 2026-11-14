---
title: Give a site its own layout
description: A site's layout files, their markup and stylesheet, and the HTML blocks, fragments and page templates in a page's files.
---

The configuration behind [Give a site its own layout](/portal/sites/layouts/). That page covers what a layout is, what people see, and the HTML blocks, fragments and page templates a page holds.

## A layout of the site's own

A site's layouts sit in the `layouts` folder beside its pages:

```
sites/main/layouts/
  civic.html       the frame, for every language
  civic.en.html    the frame in English, when English needs its own words
  civic.css        its stylesheet (optional)
```

The name of the file is the name of the layout: lower-case letters, digits and hyphens, starting with a letter. A frame for one language adds the language's two-letter code. A page uses the layout by its name (see [A page that uses the layout](#a-page-that-uses-the-layout)). A site has at most 32 layouts. `one-column` and `two-column` are taken.

## The marked places

The frame is HTML, with three elements of the portal's own, each written empty with its end tag:

| Element | What goes there |
| --- | --- |
| `<portal-region name="main"></portal-region>` | the page's main content; required. Add other regions, such as `name="aside"`, as the layout needs, each name once; a page's `regions` name them. |
| `<portal-title></portal-title>` | the page's title, as its heading; at most once. Without one, the title opens the main region. |
| `<portal-locales></portal-locales>` | links to the same page in each of the site's languages; at most once. |

They stand at the top of the frame, or directly inside `div`, `section`, `article`, `aside`, `header`, `footer`, `nav`, `li`, `td`, `th`, `figure`, `details` or `blockquote`.

```html
<header class="civic-top">
  <nav aria-label="Meniu principal">
    <a href="/">Acasă</a> <a href="/servicii">Servicii</a>
  </nav>
  <portal-locales></portal-locales>
</header>
<div class="civic-hero"><portal-title></portal-title></div>
<div class="civic-body">
  <portal-region name="main"></portal-region>
  <aside aria-label="Noutăți"><portal-region name="aside"></portal-region></aside>
</div>
<footer class="civic-foot"><p>Primăria Exemplu</p></footer>
```

A frame for one language, such as `civic.en.html`, has the same regions as `civic.html`.

## What a frame may hold

The portal checks the markup and refuses what it does not take, naming the element or attribute; nothing is quietly dropped.

- **Elements:** text and structure, such as `header`, `nav`, `footer`, `section`, `article`, `aside`, `div`, `p`, `h2` to `h6`, lists, links, images, figures, tables and `details`. No `main` or `h1`: the page gives one of each. No scripts, styles, frames, forms, buttons or `svg`, and no comments.
- **Attributes:** `class`, `id`, `role`, `lang`, `dir`, `title`, `hidden`, `tabindex`, `aria-*` and `data-*`, plus each element's own, such as `href`, `src` and `alt`. No `style` and no event handlers. Images need `alt`, empty for decoration.
- **The portal's own names:** the frame cannot use `id="main"`, ids starting with `portal-`, the roles `main`, `heading` and `application`, or the `data-` attributes the portal puts on placements. `tabindex` is `0` or `-1`, and `target` only `_blank`.
- **Addresses:** links to pages of the site (`/…`, but not the portal's own `/_portal/…`), `?…`, `#…`, `https:`, `http:`, `mailto:` and `tel:`; images from `https:` or embedded as PNG, JPEG, GIF, WebP or AVIF. An address relative to the page, such as `logo.png`, is refused: it would change from page to page.

A frame takes at most 256 KB.

### Images in each screen's size

Give an image its width in pixels, such as `<img src="https://img.example.ro/hero.jpg" width="640" alt="…">`. The portal then serves it at that width, and twice that for sharp screens, in a lighter format, so phones load less. An image without a width, or with sizes of its own (`srcset`), is shown as it is. If the portal cannot resize an image, visitors get the original.

## Its stylesheet

The stylesheet styles the frame with the site's [design tokens](/portal/developer/design/), by their own names:

```css
.civic-top {
  display: flex;
  justify-content: space-between;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}
.civic-foot { color: var(--muted); }
```

- It fetches nothing from elsewhere: no `@import`, and `url()` only for addresses on the site (`/…`) or embedded images and fonts.
- It styles the frame's own elements and classes, not `html` or `body`, and not the content: on `html`, `body` and inside a region, the token names belong to the apps' widgets.
- It leaves the portal's own controls alone: the placement menus and the skip link.
- It takes at most 256 KB.

## A page that uses the layout

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
path: /despre
title: { ro: Despre, en: About }
layout: civic
regions:
  main:
    - id: story
      app: portal
      preferences:
        html:
          ro: |
            <h2>Cine suntem</h2>
            <p>…</p>
          en: |
            <h2>Who we are</h2>
            <p>…</p>
  aside:
    - { id: news, app: content-block }
```

- `layout`: the layout's name, the file name without its extension: `civic` for `civic.html`.
- `regions`: each region the layout marks, such as `main` and `aside`, with the placements in it.

## An HTML block on a page

An HTML block is text a page holds itself: `app: portal`, with the text for each of the site's languages under `preferences.html`. It needs no app and no approval. In a region of a page's file:

```yaml
- id: story
  app: portal
  preferences:
    html:
      ro: |
        <h2>Cine suntem</h2>
        <p>Program: luni–vineri.</p>
      en: |
        <h2>Who we are</h2>
        <p>Open: Monday to Friday.</p>
```

- `app: portal`: the portal's own block, which needs no app.
- `preferences.html`: the text of each of the site's languages, each written as a `|` block.

Write each text as a `|` block, as above: a plain value breaks at the first colon followed by a space. Give the text of every language of the site, and no other. The text is checked like a frame, without the portal's own elements, and takes at most 64 KB per language. An HTML block can go in any layout's regions.

## A fragment

A fragment is text kept once and placed on many pages, in `sites/<site>/fragments/<id>.yaml`. A page places it by its id; change the file, and every page that holds it changes. Its text holds what an HTML block holds. A site has at most 200 fragments.

In `sites/<site>/fragments/<id>.yaml`, here `sites/main/fragments/program.yaml`:

```yaml
name: { ro: Program, en: Opening hours }
html:
  ro: |
    <p>Luni–vineri, 8–16.</p>
  en: |
    <p>Monday to Friday, 8 to 4.</p>
```

A page places it by its id, in a region of the page's file:

```yaml
- id: hours
  app: portal
  widget: fragment
  preferences: { fragment: program }
```

- `name`: the fragment's name, in each language.
- `html`: its text, for each of the site's languages.
- `fragment`: the id of the fragment, the file name without its extension.

## A page template

A page template, in `sites/<site>/templates/<id>.yaml`, is a page's starting point. It holds a `name` in each language, a `layout` and `regions`, written as a page's. It is never shown to visitors; administrators start new pages from it in the console. A site has at most 50.

## Check it

[`portal check`](/portal/developer/check-a-site/) reads the layouts and blocks with the rest of the site, and names each problem with its file:
- a page naming a layout the site does not have, or a region its layout does not have;
- markup or a stylesheet the portal does not take, with the reason;
- a frame without a main region, or with a region named twice;
- a frame for a language the site does not have.

A problem keeps the whole change from going live. To see the layout, render the pages:

```sh
portal check ./portal-config --start --render
```

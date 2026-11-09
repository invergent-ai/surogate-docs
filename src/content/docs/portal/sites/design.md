---
title: Give a site its look
description: A site's colours, fonts and spacing come from its design package, in Open Design's format, kept with the site's files.
---

A site looks the way its design package says: its colours, fonts, text sizes, spacing and corners. The package sits beside the site's pages in the config repository, so a change to the look is reviewed and merged like any other change. Apps' widgets on the site take the same look.

A site without a package has the portal's own look.

## The design package

The package is a folder named `design` in the site's folder:

```
sites/main/design/
  manifest.json    what the package is
  DESIGN.md        the brand in words
  tokens.css       the brand in values
```

It is an [Open Design](https://github.com/nexu-io/open-design) design-system package, in Open Design's own format, so a package made in Open Design works here as it is.

**`manifest.json`** names the package:

```json
{
  "schemaVersion": "od-design-system-project/v1",
  "id": "civic",
  "name": "Civic",
  "category": "Public sector",
  "source": { "type": "local", "path": "design" },
  "files": { "design": "DESIGN.md", "tokens": "tokens.css" }
}
```

**`DESIGN.md`** describes the brand for people and coding agents: its theme, colour, typography, components, layout, depth, what to do and not do, and how it adapts to small screens.

**`tokens.css`** holds the values, as design tokens:

```css
:root {
  --bg: #ffffff;
  --surface: #f7f8fa;
  --fg: #111827;
  --muted: #4b5563;
  --border: #d1d5db;
  --accent: #1d4ed8;
  --font-display: system-ui, sans-serif;
  --font-body: system-ui, sans-serif;
  /* … the text sizes, line heights, section spacing and page width */
}
```

## The tokens

| Tokens | What they set | Required |
| --- | --- | --- |
| `--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent` | the page, cards, text, secondary text, lines, and the brand colour | yes |
| `--font-display`, `--font-body` | the fonts of headings and text | yes |
| `--text-xs` … `--text-4xl`, `--leading-body`, `--leading-tight`, `--tracking-display` | text sizes, line heights and letter spacing | yes |
| `--section-y-*`, `--container-max`, `--container-gutter-*` | space between sections, the page's width and its margins on each kind of screen | yes |
| `--accent-on`, `--space-*`, `--radius-*`, `--focus-ring`, `--success`, `--warn`, `--danger` and others | text on the brand colour, spacing, corners, the focus ring, and status colours | no: they have defaults |

You can add tokens of your own; they are kept.

Values are colours, sizes, `var()`, `calc()` and colour functions. Names in quotes are allowed only in fonts. Anything else is refused: images, `url()`, imports, markup.

Fonts are named, not loaded: name fonts the visitor's device has, or that a later version of the portal will serve.

## Check it

[`portal check`](/portal/sites/check-a-site/) reads the package with the rest of the site:
- A missing required token is named.
- A value the portal refuses is named, with its reason.
- A manifest Open Design would not accept is refused.

A package with a problem keeps the whole change from going live, as any problem in the site's files does.

To see the look, render the pages:

```sh
portal check ./portal-config --start --render
```

The check fails when text is hard to read against its background, so a palette with too little contrast is caught before anyone sees it. To show the change to others, make a [preview](/portal/sites/previews/).

## For apps

A widget looks like the site it is on when it uses the tokens: `var(--fg)` and `var(--muted)` for text, `var(--accent)` and `var(--accent-on)` for actions, `var(--font-body)` for its font, `var(--space-4)` and `var(--radius-md)` for spacing and corners. A widget built on the Surogate UI kit takes the site's look by itself. See [Build an app](/portal/sites/build-an-app/).

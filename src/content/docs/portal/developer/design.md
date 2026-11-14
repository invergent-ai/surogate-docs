---
title: Give a site its look
description: A site's colours, fonts and spacing come from its design package, kept with the site's files.
---

A site looks the way its design package says: its colours, fonts, text sizes, spacing and corners. The package sits beside the site's pages in its files, so a change to the look is saved, and can be undone, like any other change. Apps' widgets on the site take the same look.

A site without a package has the portal's own look. A site's own frame, its header, navigation and footer, is a [layout](/portal/sites/layouts/) that styles itself with the same tokens.

## The design package

The package is a folder named `design` in the site's folder:

```
sites/main/design/
  manifest.json    what the package is
  DESIGN.md        the brand in words
  tokens.css       the brand in values
```

The package is plain files, so it is written and reviewed like the rest of the site.

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

[`portal check`](/portal/developer/check-a-site/) reads the package with the rest of the site:
- A missing required token is named.
- A value the portal refuses is named, with its reason.
- A manifest that is not a design package's is refused.

A package with a problem keeps the whole change from going live, as any problem in the site's files does.

To see the look, render the pages:

```sh
portal check ./portal-config --start --render
```

The check fails when text is hard to read against its background, so a palette with too little contrast is caught before anyone sees it. To show the change to others, make a [preview](/portal/developer/previews/).

## Design it in the studio

Administrators can explore a look in the portal's [design studio](/portal/console/studio/) before writing the package: describe the brand, see pages in it, and change it until it is right. The package in the site's files is still what the site uses.

## For apps

A widget looks like the site it is on when it takes its colours from the page:
- **Colours:** `var(--foreground)` and `var(--muted-foreground)` for text, `var(--primary)` and `var(--primary-foreground)` for actions, `var(--background)`, `var(--card)` and `var(--border)` for surfaces and lines.
- **Fonts and sizes:** `var(--font-body)` for the font, `var(--space-4)` and `var(--radius-md)` for spacing and corners.

On a page, `--muted`, `--accent` and `--surface` hold the UI kit's light tints, not the site's colours: don't use them for text or actions. A widget built on the Surogate UI kit takes the site's look by itself. See [Build an app](/portal/developer/build-an-app/).

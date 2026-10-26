# Docs site redesign

Date: 2026-10-26. Owner: Flavius Burca.

## Intent

docs.surogate.ai is for the people who use Surogate Agents and Keel. Today it has three problems:

1. It still looks like default Starlight with a green accent, nothing like the new surogate.ai.
2. Every page of all three tracks (Work, Develop and Keel) shares one long sidebar.
3. The home page is a splash page with the old "Multiply yourself." tagline and long prose sections.

The redesign gives the docs the website's look, a home page that lets the reader choose a product, and a separate sidebar for each track. It does not rewrite the guides.

## Reference designs

The mockups are artboards on the design canvas https://claude.ai/artifact/7nq6FogASMZVLX4ELKo5pi, in the "Documentation site" group to the right of the website pages:

| Artboard | What it fixes |
|---|---|
| Docs home | The home page, light theme |
| Docs home, dark | The home page, dark theme |
| Docs page A: sidebar with toggle | Every guide page, light theme |
| Docs page A, dark | Every guide page, dark theme |

The "Docs page B: product tabs" and "Docs page C: reading mode" artboards were rejected options and only show what not to build. The website artboards on the same canvas (Homepage, Surogate Agents, Keel, Partners) are the style reference for anything the docs artboards don't show.

The mockups are built from scripts that hold every colour, size and string used: `/home/flavius/.claude/projects/-work-surogate-ops/canvas-backup/docs_themed.py` (home and page A, both themes) and `build_docs_pages.py` (the three page variants). Read colours and spacing from there, not from screenshots.

## Goals

- The docs look like part of surogate.ai: the same aubergine nav, Inter type, square corners, palette and drawing style.
- The home page offers the two products, Surogate Agents and Keel, with logos, a short intro and use cases.
- Each track has its own sidebar. A Keel reader never sees Work or Develop pages, and the reverse.
- Light and dark themes both work, and the reader can switch between them. Dark mode is mandatory.
- Every current URL keeps working.

## Non-goals

- No rewriting of guide content. The only page whose text changes is the home page (`src/content/docs/index.mdx` or its replacement).
- No new guide pages and no change to page addresses.
- No dark-mode screenshots. The existing light screenshots stay as they are in both themes.
- No API reference page. The docs home mockup has an "API reference" link in its help band; drop it, because no such page exists.

## Anti-goals

These would count as failure even if everything technically works:

- Default Starlight with new colours. The header, sidebar, home and footer must look like the mockups, not like Starlight's layout recoloured.
- Rounded corners anywhere, including search, buttons, code blocks, note boxes and cards.
- A legend under any drawing, decorative icon tiles, ALL-CAPS micro-labels or italic accent headings.
- Headlining the Copilot or "vibecoding" on the home page.
- Breaking any URL listed in `migration/baseline-urls.txt`.

## Constraints

- Stack: Astro + Starlight, as today (`astro` 7.1.6, `@astrojs/starlight` 0.41.5 at the time of writing). Keep `starlight-links-validator` and `starlight-llms-txt`.
- CI (`.github/workflows/deploy-docs.yml`) runs `migration/assert_content.py`, the migration unit tests, `npm run build`, `npm run check` and `migration/check_routes.py`. All must stay green. If the home page change trips `assert_content.py`, update its expectation to match.
- Fonts: Inter (400, 500, 600, 700, 800) and JetBrains Mono, self-hosted through `@fontsource` like today's Inter.
- The site deploys to GitHub Pages as today; the deploy workflow does not change beyond what the build needs.

## Structure and navigation

### Tracks and sidebars

There are three tracks, each with its own sidebar. Their contents and order are today's three sidebar groups in `astro.config.mjs`, unchanged:

- **Work**: the "Work — for operators" group (pages under `/work/`).
- **Develop**: the "Develop — for builders" group (pages under `/develop/`).
- **Keel**: the "Keel — for case work" group (pages under `/keel/`).

Work and Develop together are the Surogate Agents product. Keel is its own product.

Inner groups stay collapsed by default, as today. The group that holds the current page is open.

### The nav bar

The nav bar is on every page, aubergine (`#2a102d`) in both themes. Left to right:

1. "Surogate" in 800 weight with "Docs" beside it in 600 weight at 70% white. It links to the docs home.
2. Product links: "Surogate Agents", linking to `/work/`, and "Keel", linking to `/keel/`. The current product is white and bold; on Work and Develop pages that's Surogate Agents, on Keel pages it's Keel. On the home page neither is current.
3. Search: a compact field (search icon, "Search", a "Ctrl K" key hint) on guide pages. The home page has a link to surogate.ai in its place, because the home hero carries the large search field.
4. The theme switch: a square 40 px button with a 1 px border, showing a moon in light mode and a sun in dark mode.
5. "Sign in", an orange (`#ffaf10`) button linking to https://ops.surogate.ai.

The GitHub and X icons leave the header. GitHub moves to the footer.

### The docs home (`/`)

Follow the "Docs home" artboards. Top to bottom:

1. Nav, as above.
2. Hero on aubergine: the heading "Surogate documentation", the line "Guides, tutorials and reference for Surogate Agents and Keel.", and a large search field (56 px tall, square, "Search the docs", "Ctrl K"). The field opens Starlight's search.
3. Products section: the heading "Two products, built to work together." and the intro "Surogate Agents is where you build and run agents: each one has its own computer, browser and files, and works with your skills and knowledge. Keel runs your business processes, with agents, people and systems each doing their step." Then two equal product cards side by side, stacking on narrow screens:
   - **Surogate Agents**: the rabbit logo, the line "Run agents for your team, or build and train them.", the drawing of one agent deployed to three places, the button "Open the Agents docs" to `/work/`, and the link "Quickstart" to `/work/quickstart/`.
   - **Keel**: the Keel logo, the line "Design processes in Keel Builder, and work the cases in the business app.", the drawing of a board stage opening into its flow, the button "Open the Keel docs" to `/keel/`, and the link "Quickstart" to `/keel/quickstart/`.
4. Use cases on the paper background: the heading "Start from a real task.", the line "Each guide takes you from an empty project to something that works.", and two columns of five task links, each with a small label for its track on the right:

   | Task | Label | Links to |
   |---|---|---|
   | Deploy a customer-support agent in 10 minutes | Work | `/work/use-cases/`, section 1 |
   | Add Slack so your team can chat with the same agent | Work | `/work/use-cases/`, section 2 |
   | Build a knowledge base from your wiki and tickets | Work | `/work/use-cases/`, section 4 |
   | Fine-tune an expert from your agent's sessions | Develop | `/develop/use-cases/`, section 1 |
   | Run batch jobs through the API | Develop | `/develop/use-cases/`, section 6 |
   | Build a loan request and work your first case | Quickstart | `/keel/quickstart/` |
   | Route cases by amount with a decision table | Keel Builder | `/keel/builder/rules/` |
   | Give a team a queue with a serving order | Keel Builder | `/keel/builder/queues/` |
   | Let an agent work a step and ask when unsure | Business app | `/keel/business/agents/` |
   | Test a case type with scenarios before you publish | Keel Builder | `/keel/builder/scenarios/` |

   Use the real heading anchors of those use-case sections.
5. Help band: "Can't find what you need? Ask on our Discord, or email surogate@invergent.ai." with links to What's new (`/work/whats-new/`) and Discord (https://discord.gg/eVTq93BrQ4).
6. Footer, as below.

The old home sections ("Vibecode your agents", "The improvement loop", "Skills and expert models" and the rest) are removed from the home page. Their topics already have their own pages under Develop.

### Guide pages

Follow the "Docs page A" artboards. Every guide page has:

- **Sidebar** on the left, 290 px wide, on the soft background with a 1 px right border:
  - At the top, the product logo (26 px) and name: "Surogate Agents" on Work and Develop pages, "Keel" on Keel pages.
  - On Work and Develop pages only, a two-part switch under it: "Work" and "Develop", full width, square. The selected half is filled with the mark colour; the other is outlined. Choosing a half goes to that track's welcome page (`/work/` or `/develop/`) and its sidebar. Keel pages have no switch.
  - Then the track's page tree. The current page has a 3 px left bar in the mark colour, the surface background and bold ink text. Groups show a chevron.
- **Article** in the middle, at most 780 px wide: a breadcrumb (product, track, page; Keel pages have product and page), the title, the page's lead paragraph, then the content.
- **"On this page"** on the right, 220 px: the page's headings, the current one marked with a 2 px bar, and an "Edit this page" link (today's edit link).
- **Previous and next** links at the bottom of the article, as two bordered boxes.
- **Footer**.

### Footer

A slim bar on `#1a0a1c` in both themes: "Surogate © 2026" on the left, and links to surogate.ai, Discord and GitHub (https://github.com/invergent-ai/surogate) on the right.

### Phones

Below Starlight's existing breakpoints, the sidebar folds into a menu button in the nav (Starlight's mobile menu, restyled), the Work / Develop switch stays at the top of that menu, and "On this page" moves above the article as Starlight already does. The product cards and the use-case columns stack. The nav wraps; no horizontal scrolling.

## Visual system

### Colour tokens

Both themes come from one token set, so implement them as CSS variables that Starlight's own variables map onto. Values from the mockups:

| Token | Light | Dark | Used for |
|---|---|---|---|
| bg | `#ffffff` | `#1a0a1c` | Page background |
| soft | `#faf9f7` | `#211024` | Sidebar, table header row, note boxes, use-case band |
| surface | `#ffffff` | `#24102a` | Cards, current sidebar item, search field |
| ink | `#2a102d` | `#ffffff` | Headings, bold text, current items |
| text | `#403e4a` | `rgba(255,255,255,0.74)` | Body text, sidebar items |
| line | `#e6e3eb` | `rgba(255,255,255,0.12)` | Borders and rules |
| card | `#ebe4ee` | `#33183a` | Boxes inside drawings |
| cardline | `#dcd2e1` | `rgba(255,255,255,0.16)` | Their borders, the switch's outline |
| link | `#9b1f61` | `#ffaf10` | Links |
| mark | `#2a102d` | `#ffe845` | Selected switch half, primary buttons |
| markink | `#ffffff` | `#2a102d` | Text on the mark colour |
| bar | `#2a102d` | `#ffe845` | Current-page bars in the sidebar and "On this page" |
| rule | `#2a102d` | `rgba(255,255,255,0.85)` | Top edge of product cards |
| codeinline | `#ebe4ee` | `rgba(255,255,255,0.10)` | Inline code background |
| codebg | `#1a0a1c` | `#0f0511` | Code block background |

Fixed in both themes: nav and hero `#2a102d`, footer `#1a0a1c`, Sign in `#ffaf10`, decision diamonds `#ffe845`, note-box edges as below.

The old green accent is removed.

### Type

Inter throughout, JetBrains Mono for code. Page title 46 px / 800; h2 28 px / 800; body 17 px with 1.7 line height; lead paragraph 21 px. Keep today's root size (17 px base) unless the mockup sizes need otherwise.

### Components

- **Corners:** square everywhere.
- **Tables:** 1 px border, a header row on the soft background, 1 px row rules.
- **Screenshots:** a 1 px frame in the line colour, the caption under them at 14 px in the text colour. Light screenshots stay light in dark mode.
- **Code blocks:** the codebg background, a 1 px border, a header strip with the file name and a "Copy" action, JetBrains Mono at 14 px. Starlight's Expressive Code can be themed to match.
- **Inline code:** the codeinline background, a 1 px 5 px padding, the ink colour.
- **Note boxes (asides):** the soft background, a 3 px left edge and a bold title. Note: yellow `#ffe845`. Tip: powder `#bdccd4`. Caution: orange `#ffaf10`. Danger: wine `#9b1f61`.
- **Tabs, steps, cards in pages and badges** take the same tokens and square corners. The existing "Coming soon" badge stays.

### Logos

- **Surogate Agents:** the Surogate rabbit in aubergine on an orange (`#ffaf10`) square, as drawn in the mockups. The rabbit's paths come from `/work/surogate-website/public/brand/rabbit.svg`.
- **Keel:** a placeholder mark drawn for these mockups: an aubergine hull and keel on a yellow (`#ffe845`) square. Its geometry is in `keel_sq()` in `docs_themed.py`. It ships as is until a real Keel logo exists.

### Drawings

The two product-card drawings are flat inline SVG in the house style: the colour tokens, square corners and grey bars standing for text. Their code is `mini_agents()` and `mini_keel()` in `docs_themed.py`. They are static.

## How it gets built

The look comes from the tokens above plus replaced Starlight components: the header, the sidebar, the home page, the footer, and the theme switch. Search stays Starlight's built-in search, restyled; the home hero's field opens the same search.

For the separate sidebars, the `starlight-sidebar-topics` plugin matches the Work / Develop / Keel model. Version 0.9.0 needs `@astrojs/starlight` 0.42 or later and `astro` ^7.2.10, so using it means upgrading both from today's versions. Writing a sidebar component instead is acceptable.

The site's title and description in `astro.config.mjs` change to match the new home: description "Guides, tutorials and reference for Surogate Agents and Keel."

## Left to the builder

- Plugin or own sidebar component, and the Starlight upgrade that comes with the plugin.
- How the home page is implemented: a splash page with custom components, or an Astro page.
- Exact CSS architecture and which Starlight variables each token maps onto.
- Hover and focus states, in the token colours, with visible focus rings.
- Small spacing adjustments where Starlight's markup differs from the mockup's.

## Decisions and who made them

Flavius decided:

- A home page in the website's style, with two product cards, logos, an intro and use cases.
- The Surogate Agents card leads into the existing Work / Develop tracks; the Keel card leads to the Keel welcome page.
- Guide page layout A: a sidebar with a Work / Develop switch, the article, and "On this page" on the right.
- Dark mode is mandatory; the dark mockups are accepted.
- Light screenshots stay as they are in dark mode.
- The build plan, the content changes and the Keel placeholder logo, as described above.

Claude's calls, accepted without objection:

- Agents lands straight on the Work welcome page; there is no separate Agents landing page.
- Keel's sidebar has no switch.
- Sidebar groups stay collapsed by default.
- The phone layout.
- The note-box edge colours.
- Use cases taken from the existing use-case pages.

Claude's calls made while writing this document:

- Dropping the mockup's "API reference" link.
- Moving GitHub from the header to the footer and dropping X.
- The new site description.

Claude's calls settled after the builder check:

- **Code-block header strip.** The strip appears on every code block, labelled with the fence's language when it has one, and always offers "Copy". The mockup's "SOUL.md" label was only an example; no fence in the content has a title. Expressive Code's terminal frame (rounded corners, window dots) is turned off.
- **Captions.** The content uses `![alt](…)`, and its alt texts are already full-sentence captions. Each becomes a visible `<figcaption>`, and the image's `alt` is emptied so screen readers don't read the sentence twice.
- **Lead paragraph.** No page has a `description`. A page's first paragraph is styled as the 21 px lead only when it is the page's first block and at most 250 characters long. Longer openings stay at body size, so no lead runs to seven lines.
- **Site title.** "Surogate Docs". The stale `twitter:*` and keywords meta are updated to match the new description.
- **Previous and next** stay inside the current track: the end of Work doesn't run on into Develop.
- **Theme.** The site follows the reader's system theme until they use the switch, then remembers their choice, as Starlight does today.

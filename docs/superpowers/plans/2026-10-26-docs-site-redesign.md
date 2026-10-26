# Docs Site Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give docs.surogate.ai the surogate.ai look, a product-choice home page, a separate sidebar per track (Work, Develop, Keel) and light and dark themes from one token set.

**Architecture:** Stay on Astro + Starlight. Upgrade to Starlight 0.42 and split the one sidebar into three topics with `starlight-sidebar-topics`. Override a small set of Starlight components (Header, Sidebar, PageTitle, PageSidebar, Footer, MobileMenuFooter, ThemeSelect, Hero). Colours live in one token file mapped onto Starlight's variables. Two rehype plugins add the lead paragraph and the screenshot captions. The home page is the existing `index.mdx` splash page, rebuilt from MDX components.

**Tech Stack:** Astro 7.4, @astrojs/starlight 0.42, starlight-sidebar-topics 0.9.0, Expressive Code (bundled with Starlight), `node --test` for unit tests, Python `unittest` for checks on the built `dist/`.

**Spec:** `docs/superpowers/specs/2026-10-26-docs-site-redesign-design.md`. The mockup source with every colour, size and string is `/home/flavius/.claude/projects/-work-surogate-ops/canvas-backup/docs_themed.py`. Copy markup values (padding, font sizes, SVG geometry) from it; it is the reference wherever this plan says "as in the mockup".

## Global Constraints

- Square corners everywhere: buttons, search, inputs, code blocks, note boxes, cards, tables, images, pagination. No `border-radius` other than `0` in our CSS, and override Starlight's and Expressive Code's radii to `0`.
- Fonts: Inter 400, 500, 600, 700, 800 and JetBrains Mono 400, 600, self-hosted through `@fontsource/inter` and `@fontsource/jetbrains-mono`.
- Fixed colours in both themes: nav and home hero `#2a102d`, site footer `#1a0a1c`, Sign in `#ffaf10` with `#2a102d` text, decision diamonds `#ffe845`.
- Token values are the spec's "Colour tokens" table, verbatim. The old green accent (`#07a000`, `#87ed82`) is removed.
- Product names are exactly "Surogate Agents" and "Keel". Track names are exactly "Work" and "Develop".
- Links: Sign in `https://ops.surogate.ai`, Discord `https://discord.gg/eVTq93BrQ4`, GitHub `https://github.com/invergent-ai/surogate`, email `surogate@invergent.ai`.
- Every URL in `migration/baseline-urls.txt` keeps working: `python3 migration/check_routes.py` passes.
- CI stays green: `migration/assert_content.py`, the migration unit tests, `npm run build`, `npm run check`, `migration/check_routes.py`, plus the two test commands this plan adds.
- No guide page text changes. Only `src/content/docs/index.mdx` is rewritten.
- No headline about the Copilot or "vibecoding" anywhere on the home page.

## Review Focus

- **A page missing from every topic.** `starlight-sidebar-topics` fails the build for a page with a sidebar that no topic lists. Today every page is listed (verified), and a future unlisted page should fail the build with the plugin's message, not render a wrong sidebar. Task 1 asserts the build succeeds and every built guide page shows exactly one track's pages.
- **Phone widths.** At 375 px the nav must wrap without horizontal scroll, the mobile menu must hold the product header and the Work / Develop switch, and the home cards and use-case columns must stack. Task 8 checks this with screenshots at 375 px in both themes.
- **Theme choice persistence.** A reader who picks dark must get dark on the next page and after a reload, and a reader who never touches the switch follows the OS. Task 3 unit-tests the toggle logic and Task 8 checks it in a browser.
- **Dark mode on Starlight's own widgets.** The search dialog, the mobile menu, the mobile "On this page" dropdown, badges and tabs use Starlight variables. They must take the dark tokens, not white backgrounds. Task 8 opens each in dark mode.
- **Long titles and leads.** Breadcrumbs with long page titles wrap, and openings over 250 characters stay at body size. Task 6 tests the 250-character boundary, and Task 8 checks a long breadcrumb in the browser.

---

## File map

| File | Responsibility |
|---|---|
| `package.json`, `package-lock.json` | Upgrades, new dependencies, `test:unit` and `test:site` scripts |
| `astro.config.mjs` | Topics, component overrides, rehype plugins, Expressive Code options, title and meta |
| `.github/workflows/deploy-docs.yml` | Runs the two new test commands |
| `src/lib/product.mjs` + `product.test.mjs` | Route id to product and track, and their labels and home links |
| `src/scripts/theme.mjs` + `theme.test.mjs` | Theme toggle logic |
| `src/plugins/rehype-lead.mjs` + `.test.mjs` | Marks the first short paragraph as the lead |
| `src/plugins/rehype-figure.mjs` + `.test.mjs` | Turns lone images into figures with captions |
| `src/styles/tokens.css` | The `--d-*` tokens per theme and their mapping onto Starlight variables |
| `src/styles/custom.css` | Component styling (replaces today's file content) |
| `src/components/brand/AgentsMark.astro`, `KeelMark.astro` | The two product logos as inline SVG |
| `src/components/Header.astro` | Nav bar |
| `src/components/ThemeToggle.astro` | The sun / moon button, also used as the ThemeSelect override |
| `src/components/MobileMenuFooter.astro` | Product links, theme button and Sign in inside the mobile menu |
| `src/components/Sidebar.astro` | Product header, Work / Develop switch, then Starlight's sidebar |
| `src/components/PageTitle.astro` | Breadcrumb and title |
| `src/components/PageSidebar.astro` | "On this page" plus "Edit this page" |
| `src/components/Footer.astro` | Previous / next and the slim site footer |
| `src/components/home/HomeHero.astro` | Hero band (Hero override) |
| `src/components/home/ProductCards.astro`, `UseCases.astro`, `HelpBand.astro`, `MiniAgents.astro`, `MiniKeel.astro` | Home sections and card drawings |
| `src/content/docs/index.mdx` | The new home page |
| `tests/docsite.py`, `tests/test_*.py` | Checks on the built `dist/` |
| `src/components/HeaderLinks.astro` | Deleted (replaced by Header) |

Every component that tests target carries a `data-docs="<name>"` attribute: `header`, `product-link`, `theme-toggle`, `product-head`, `track-switch`, `breadcrumb`, `edit-link`, `site-footer`, `product-card`, `task`, `help-band`.

---

### Task 1: Upgrade Starlight and split the sidebar into three topics

**Files:**
- Modify: `package.json`, `package-lock.json`, `astro.config.mjs`, `.github/workflows/deploy-docs.yml`
- Create: `tests/docsite.py`, `tests/test_topics.py`

**Interfaces:**
- Produces: `tests/docsite.py` (not `site.py`: Python preloads the stdlib `site` module) with `DIST: Path`, `page(route: str) -> str` (reads `dist/<route>/index.html`, `route` like `/work/quickstart/` or `/`), and `section(doc: str, name: str) -> str` (the inner HTML of the first element whose `data-docs` attribute equals `name`, or whose `id` equals `name` when `name` starts with `#`; raises `AssertionError` when missing). Use `html.parser`, tracking nesting by tag. Every test module starts with `import re, unittest` and `from docsite import DIST, page, section`. Where a test's regex assumes an attribute order, an equivalent check on the parsed element is fine.
- Produces: topic configuration with ids `work`, `develop`, `keel`, linking to `/work/`, `/develop/`, `/keel/`. Their `items` are today's three sidebar groups' `items`, unchanged and in order. Labels are "Work", "Develop" and "Keel".

- [ ] **Step 1: Write the failing tests in `tests/test_topics.py`**

```python
class Topics(unittest.TestCase):
    def sidebar_links(self, route):
        return re.findall(r'href="(/[^"#]*)"', section(page(route), '#starlight__sidebar'))

    def test_keel_sidebar_has_only_keel_pages(self):
        links = self.sidebar_links('/keel/')
        self.assertIn('/keel/builder/designer-agent/', links)
        self.assertFalse([l for l in links if l.startswith(('/work/', '/develop/'))])

    def test_work_sidebar_has_only_work_pages(self):
        links = self.sidebar_links('/work/quickstart/')
        self.assertIn('/work/channels/slack/', links)
        self.assertFalse([l for l in links if l.startswith(('/keel/', '/develop/'))])

    def test_develop_sidebar_has_only_develop_pages(self):
        links = self.sidebar_links('/develop/')
        self.assertIn('/develop/features/training/', links)
        self.assertFalse([l for l in links if l.startswith(('/keel/', '/work/'))])

    def test_pagination_stays_in_track(self):
        self.assertNotIn('rel="next"', page('/work/reference/faq/'))
        self.assertNotIn('rel="prev"', page('/develop/'))
```

The Starlight sidebar container id is `starlight__sidebar`; if 0.42 renames it, use the new id in all tests.

- [ ] **Step 2: Build and run the tests to verify they fail**

Run: `npm run build && python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: the three sidebar tests FAIL, because the shared sidebar lists all tracks.

- [ ] **Step 3: Upgrade and configure**

Upgrade to `@astrojs/starlight@^0.42.7`, `astro@^7.4.2`, `starlight-links-validator@^0.27.0` and `starlight-llms-txt@^0.12.0`, and add `starlight-sidebar-topics@0.9.0`. Move the three `sidebar` groups into `starlightSidebarTopics([...])` in `plugins` (the plugin throws if `sidebar` is still set) and delete `sidebar`. Add to `package.json` scripts: `"test:unit": "node --test \"src/**/*.test.mjs\""` and `"test:site": "python3 -m unittest discover -s tests -p 'test_*.py' -v"`. In the deploy workflow, run `npm run test:unit` before the build and `npm run test:site` after it. Fix anything the 0.42 upgrade breaks before going on.

- [ ] **Step 4: Run everything**

Run: `npm run build && npm run check && npm run test:site && python3 migration/assert_content.py && python3 migration/check_routes.py`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add package.json package-lock.json astro.config.mjs .github/workflows/deploy-docs.yml tests/
git commit -m "build(docs): starlight 0.42 and one sidebar per track"
```

---

### Task 2: Tokens, fonts and article styling

**Files:**
- Create: `src/styles/tokens.css`, `tests/test_theme_css.py`
- Modify: `src/styles/custom.css` (replace its content), `astro.config.mjs` (`customCss`, `expressiveCode`), `package.json` (`@fontsource/jetbrains-mono`)

**Interfaces:**
- Produces: CSS variables `--d-bg`, `--d-soft`, `--d-surface`, `--d-ink`, `--d-text`, `--d-line`, `--d-card`, `--d-cardline`, `--d-link`, `--d-mark`, `--d-markink`, `--d-bar`, `--d-rule`, `--d-codeinline`, `--d-codebg` on `:root[data-theme='light']` and `:root[data-theme='dark']`, with the spec's values. Every later component uses these, never raw hex, except the Global Constraints' fixed colours.

- [ ] **Step 1: Write the failing test in `tests/test_theme_css.py`**

```python
def built_css():
    return '\n'.join(p.read_text() for p in (DIST / '_astro').glob('*.css'))

class ThemeCss(unittest.TestCase):
    def test_both_token_sets_ship(self):
        css = built_css()
        for value in ('--d-bg:#fff', '--d-bg:#1a0a1c', '--d-link:#9b1f61', '--d-link:#ffaf10', '--d-mark:#ffe845'):
            self.assertIn(value, css.replace(' ', '').lower())

    def test_old_green_is_gone(self):
        css = built_css().lower()
        self.assertNotIn('#07a000', css)
        self.assertNotIn('#87ed82', css)
```

Adjust the expected strings if the minifier shortens differently (`#ffffff` to `#fff`); keep one light and one dark value per assertion.

- [ ] **Step 2: Build and run to verify it fails**

Run: `npm run build && npm run test:site`
Expected: FAIL on both tests.

- [ ] **Step 3: Implement**

In `tokens.css`, define the tokens and map Starlight's variables onto them: `--sl-color-bg`, `--sl-color-bg-sidebar` (soft), `--sl-color-bg-nav` (`#2a102d` in both themes), the hairline variables (line), `--sl-color-text` (text), `--sl-color-white` (ink: Starlight's strongest text in both themes), `--sl-color-accent`, `--sl-color-text-accent` (link), `--sl-font` (Inter), `--sl-font-mono` (JetBrains Mono), and `--sl-nav-height: 4rem`. Keep today's `html { font-size: 106.25% }`.

In `custom.css`, style article content as in the mockup's `page()`:
- h1 46 px / 800, h2 28 px / 800 in ink; body 17 px with 1.7 line height in text.
- `p.lead` 21 px / 1.5 (the class comes from Task 6).
- Tables: a 1 px line border, header row on soft.
- Inline code on codeinline.
- `figure` img with a 1 px line frame and no radius; `figcaption` 14 px in text.
- Asides: soft background, a 3 px left edge, a bold title in ink and no icon. Edges by type: note `#ffe845`, tip `#bdccd4`, caution `#ffaf10`, danger `#9b1f61`.
- Tabs, steps, link cards and badges take the tokens with square corners.

Expressive Code in `astro.config.mjs`:
- `themes: ['github-dark-default']` with `useStarlightDarkModeSwitch: false`, so code stays dark in both themes;
- `defaultProps: { frame: 'code' }`, so no terminal window frames;
- `styleOverrides` with `borderRadius: '0'`, `codeBackground: 'var(--d-codebg)'` and the JetBrains Mono font.

Every block shows a header strip with the fence's language (from `data-language`) on the left and the copy button on the right; add the label with CSS on frames without a title. Delete the old header-link and screenshot rules.

- [ ] **Step 4: Run to verify it passes**

Run: `npm run build && npm run test:site`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/styles astro.config.mjs package.json package-lock.json tests/test_theme_css.py
git commit -m "feat(docs): surogate tokens for light and dark, article styling"
```

---

### Task 3: Nav bar and theme switch

**Files:**
- Create: `src/lib/product.mjs`, `src/lib/product.test.mjs`, `src/scripts/theme.mjs`, `src/scripts/theme.test.mjs`, `src/components/Header.astro`, `src/components/ThemeToggle.astro`, `src/components/MobileMenuFooter.astro`, `tests/test_header.py`
- Modify: `astro.config.mjs` (`components`, remove `social`)
- Delete: `src/components/HeaderLinks.astro`

**Interfaces:**
- Produces in `src/lib/product.mjs`:
  - `trackFor(id: string): 'work' | 'develop' | 'keel' | null`. `id` is `Astro.locals.starlightRoute.id`; `'work'` and `'work/...'` give `'work'`, and the same for `develop` and `keel`. Anything else, including `''` for the home page, gives `null`.
  - `productFor(id: string): 'agents' | 'keel' | null`.
  - Constants `PRODUCT_LABEL = { agents: 'Surogate Agents', keel: 'Keel' }`, `PRODUCT_HOME = { agents: '/work/', keel: '/keel/' }`, `TRACK_LABEL = { work: 'Work', develop: 'Develop', keel: 'Keel' }`, `TRACK_HOME = { work: '/work/', develop: '/develop/', keel: '/keel/' }`.
- Produces in `src/scripts/theme.mjs`: `nextTheme(current: 'light' | 'dark'): 'light' | 'dark'`, and `applyTheme(theme, doc = document, storage = localStorage): void`. `applyTheme` sets `doc.documentElement.dataset.theme` and stores `theme` under Starlight's key `starlight-theme`.
- Produces: `ThemeToggle.astro`, used by Header, MobileMenuFooter and as the `ThemeSelect` override.

- [ ] **Step 1: Write the failing unit tests**

```js
// src/lib/product.test.mjs
test('tracks', () => {
  assert.equal(trackFor('work'), 'work');
  assert.equal(trackFor('work/channels/slack'), 'work');
  assert.equal(trackFor('develop/features/training'), 'develop');
  assert.equal(trackFor('keel/builder/rules'), 'keel');
  assert.equal(trackFor(''), null);
  assert.equal(trackFor('workshop'), null);
});
test('products', () => {
  assert.equal(productFor('develop'), 'agents');
  assert.equal(productFor('keel'), 'keel');
  assert.equal(productFor(''), null);
});
// src/scripts/theme.test.mjs
test('nextTheme flips', () => {
  assert.equal(nextTheme('light'), 'dark');
  assert.equal(nextTheme('dark'), 'light');
});
test('applyTheme sets the attribute and remembers the choice', () => {
  const doc = { documentElement: { dataset: {} } }; const store = new Map();
  applyTheme('dark', doc, { setItem: (k, v) => store.set(k, v) });
  assert.equal(doc.documentElement.dataset.theme, 'dark');
  assert.equal(store.get('starlight-theme'), 'dark');
});
```

- [ ] **Step 2: Write the failing site tests in `tests/test_header.py`**

```python
class Header(unittest.TestCase):
    def test_sign_in_and_products_on_every_kind_of_page(self):
        for route in ('/', '/work/quickstart/', '/keel/'):
            head = section(page(route), 'header')
            self.assertIn('href="https://ops.surogate.ai"', head)
            self.assertIn('Surogate Agents', head)
            self.assertIn('Keel', head)
            self.assertIn('data-docs="theme-toggle"', head)

    def test_current_product(self):
        work = section(page('/develop/'), 'header')
        self.assertRegex(work, r'aria-current="page"[^>]*>\s*Surogate Agents')
        keel = section(page('/keel/quickstart/'), 'header')
        self.assertRegex(keel, r'aria-current="page"[^>]*>\s*Keel')
        self.assertNotIn('aria-current', section(page('/'), 'header'))

    def test_no_social_icons(self):
        self.assertNotIn('x.com', page('/work/'))
```

- [ ] **Step 3: Run to verify they fail**

Run: `npm run test:unit; npm run build && npm run test:site`
Expected: FAIL (modules missing, no `data-docs="header"`).

- [ ] **Step 4: Implement**

`Header.astro` lays out, left to right:
- "Surogate" (800) with "Docs" (600, 70% white), linking to `/`;
- the two product links from `PRODUCT_LABEL` and `PRODUCT_HOME`, with `aria-current="page"` on the current product;
- Starlight's `Search` (from `virtual:starlight/components/Search`), restyled as the mockup's compact field. On the home page (`productFor(id) === null`), render a plain `surogate.ai` link in its place;
- `ThemeToggle`;
- Sign in.

Below the `md` breakpoint, hide the product links and Sign in (they move to `MobileMenuFooter`).

`ThemeToggle` is a 40 px square button with a 1 px `rgba(255,255,255,0.3)` border, using the moon and sun SVGs from the mockup. Show the moon in light and the sun in dark with CSS on `[data-theme]`, and set the `aria-label` to "Switch to dark mode" / "Switch to light mode" from a small inline script using `nextTheme` and `applyTheme`. Starlight's ThemeProvider still follows the OS when nothing is stored.

Register `Header`, `ThemeSelect` (as `ThemeToggle`) and `MobileMenuFooter` in `components`, and remove `social` and `HeaderLinks.astro`.

- [ ] **Step 5: Run to verify they pass**

Run: `npm run test:unit && npm run build && npm run test:site`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/lib src/scripts src/components astro.config.mjs tests/test_header.py
git commit -m "feat(docs): surogate nav bar with products and a theme switch"
```

---

### Task 4: Sidebar with product header and Work / Develop switch

**Files:**
- Create: `src/components/brand/AgentsMark.astro`, `src/components/brand/KeelMark.astro`, `src/components/Sidebar.astro`, `tests/test_sidebar.py`
- Modify: `astro.config.mjs` (`components.Sidebar`; the plugin keeps a user override)

**Interfaces:**
- Consumes: `trackFor`, `productFor`, `PRODUCT_LABEL`, `TRACK_LABEL`, `TRACK_HOME` from Task 3.
- Produces: `<AgentsMark size={number} />` and `<KeelMark size={number} />`, square inline SVGs with `aria-hidden="true"`. The paths are `rabbit_sq()` and `keel_sq()` in the mockup script; the rabbit paths match `/work/surogate-website/public/brand/rabbit.svg`.

- [ ] **Step 1: Write the failing tests in `tests/test_sidebar.py`**

```python
class Sidebar(unittest.TestCase):
    def test_agents_pages_have_head_and_switch(self):
        doc = page('/work/quickstart/')
        self.assertIn('Surogate Agents', section(doc, 'product-head'))
        switch = section(doc, 'track-switch')
        self.assertRegex(switch, r'href="/work/"[^>]*aria-current="page"')
        self.assertIn('href="/develop/"', switch)

    def test_develop_is_current_on_develop_pages(self):
        switch = section(page('/develop/features/training/'), 'track-switch')
        self.assertRegex(switch, r'href="/develop/"[^>]*aria-current="page"')

    def test_keel_has_head_and_no_switch(self):
        doc = page('/keel/builder/rules/')
        self.assertIn('Keel', section(doc, 'product-head'))
        self.assertNotIn('data-docs="track-switch"', doc)
```

If the attribute order differs, assert on the parsed `<a>` instead of a regex.

- [ ] **Step 2: Run to verify they fail**

Run: `npm run build && npm run test:site`
Expected: FAIL (no `product-head`).

- [ ] **Step 3: Implement `src/components/Sidebar.astro`**

Render, in order:
1. The product head: the mark at 26 px and the product name, 16 px / 800 in ink.
2. On Work and Develop pages only, the switch: two equal links to `TRACK_HOME.work` and `TRACK_HOME.develop`. The current one is filled with `--d-mark` and `--d-markink`; the other has a 1 px `--d-cardline` border on `--d-surface`.
3. `<Default><slot /></Default>`, Starlight's sidebar from `@astrojs/starlight/components/Sidebar.astro`.

Do not render the plugin's topic list. Style the tree as in the mockup's `tree()`: the current page gets a 3 px `--d-bar` left edge, the surface background and bold ink text. The sidebar is 290 px wide (`--sl-sidebar-width`) on `--d-soft` with a 1 px `--d-line` right border. Starlight's mobile menu shows this component, so the head and the switch appear there too.

- [ ] **Step 4: Run to verify they pass**

Run: `npm run build && npm run test:site`
Expected: PASS, and Task 1's topic tests still pass.

- [ ] **Step 5: Commit**

```bash
git add src/components astro.config.mjs tests/test_sidebar.py
git commit -m "feat(docs): product head and work / develop switch in the sidebar"
```

---

### Task 5: Breadcrumb, edit link and footer

**Files:**
- Create: `src/components/PageTitle.astro`, `src/components/PageSidebar.astro`, `src/components/Footer.astro`, `tests/test_page_frame.py`
- Modify: `astro.config.mjs` (`components`)

**Interfaces:**
- Consumes: `trackFor`, `productFor`, `PRODUCT_LABEL`, `PRODUCT_HOME`, `TRACK_LABEL`, `TRACK_HOME` from Task 3.

- [ ] **Step 1: Write the failing tests in `tests/test_page_frame.py`**

```python
class PageFrame(unittest.TestCase):
    def test_breadcrumb_agents(self):
        crumb = re.sub(r'<[^>]+>', ' ', section(page('/work/quickstart/'), 'breadcrumb'))
        self.assertEqual(crumb.split(), ['Surogate', 'Agents', '/', 'Work', '/', 'Quickstart'])

    def test_breadcrumb_keel_has_no_track(self):
        crumb = re.sub(r'<[^>]+>', ' ', section(page('/keel/quickstart/'), 'breadcrumb'))
        self.assertEqual(crumb.split(), ['Keel', '/', 'Keel', 'quickstart'])

    def test_breadcrumb_on_a_track_home_stops_at_the_track(self):
        crumb = re.sub(r'<[^>]+>', ' ', section(page('/develop/'), 'breadcrumb'))
        self.assertEqual(crumb.split(), ['Surogate', 'Agents', '/', 'Develop'])

    def test_edit_link_moves_beside_the_toc(self):
        doc = page('/work/quickstart/')
        self.assertIn('github.com/invergent-ai/surogate-docs/edit/main/', section(doc, 'edit-link'))
        self.assertNotIn('surogate-docs/edit/main/', section(doc, 'site-footer'))

    def test_site_footer(self):
        foot = section(page('/keel/'), 'site-footer')
        for href in ('https://surogate.ai', 'https://discord.gg/eVTq93BrQ4', 'https://github.com/invergent-ai/surogate'):
            self.assertIn(href, foot)
```

Separators may be rendered by CSS instead of text; if so, drop the `'/'` items from the expected lists. The `/keel/quickstart/` page's title is "Keel quickstart".

- [ ] **Step 2: Run to verify they fail**

Run: `npm run build && npm run test:site`
Expected: FAIL.

- [ ] **Step 3: Implement**

- `PageTitle.astro`: the breadcrumb, then the `h1` with `id="_top"` as Starlight's does. The breadcrumb is the product (linking to `PRODUCT_HOME`), then for Agents the track (linking to `TRACK_HOME`), then the page title, unless the page is the track's home, in which case it ends at the track. It is 14 px in `--d-text` with half-opacity `/` separators and wraps.
- `PageSidebar.astro`: Starlight's default output, then an "Edit this page" link (`--d-link`, 14 px, 600) under the desktop table of contents, built from `Astro.locals.starlightRoute.editUrl`. Label the heading "On this page", and mark the current item with a 2 px `--d-bar` left edge.
- `Footer.astro`: Starlight's `Pagination` styled as two bordered boxes ("Previous" / "Next" at 13 px in `--d-text`, the title at 18 px / 800 in ink), with no EditLink and no credits. Then the site footer bar, full width of the content column, on `#1a0a1c`: "Surogate © 2026" on the left, and surogate.ai, Discord and GitHub on the right. Starlight's sidebar is fixed, so the bar sits under the content column rather than across the sidebar.

- [ ] **Step 4: Run to verify they pass**

Run: `npm run build && npm run test:site`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components astro.config.mjs tests/test_page_frame.py
git commit -m "feat(docs): breadcrumb, edit link beside the toc, slim footer"
```

---

### Task 6: Lead paragraphs and screenshot captions

**Files:**
- Create: `src/plugins/rehype-lead.mjs`, `src/plugins/rehype-lead.test.mjs`, `src/plugins/rehype-figure.mjs`, `src/plugins/rehype-figure.test.mjs`, `tests/test_content.py`
- Modify: `astro.config.mjs` (`markdown.rehypePlugins`), `package.json` (dev dependencies for the unit tests if needed: `unified`, `rehype-parse`, `rehype-stringify`)

**Interfaces:**
- Produces: `rehypeLead(options?: { maxLength?: number }): Transformer`, default `maxLength` 250. If the root's first element child is a `p` whose text content is at most `maxLength` characters, it adds the class `lead`.
- Produces: `rehypeFigure(): Transformer`. Every `p` whose only non-whitespace child is an `img` becomes `<figure><img …><figcaption>{alt}</figcaption></figure>`, with the `img` keeping all its properties except `alt`, which becomes `""`. Images with an empty alt are left alone.

- [ ] **Step 1: Write the failing unit tests**

```js
// rehype-lead.test.mjs  (run() = unified().use(rehypeParse, { fragment: true }).use(plugin).use(rehypeStringify))
test('short first paragraph is the lead', async () => {
  assert.equal(await run('<p>Short opening.</p><p>Next.</p>'), '<p class="lead">Short opening.</p><p>Next.</p>');
});
test('250 characters is still a lead, 251 is not', async () => {
  assert.match(await run(`<p>${'a'.repeat(250)}</p>`), /class="lead"/);
  assert.doesNotMatch(await run(`<p>${'a'.repeat(251)}</p>`), /class="lead"/);
});
test('a heading first means no lead', async () => {
  assert.doesNotMatch(await run('<h2>Title</h2><p>Text.</p>'), /lead/);
});
// rehype-figure.test.mjs
test('a lone image becomes a captioned figure', async () => {
  assert.equal(await run('<p><img src="a.png" alt="The Channels tab"></p>'),
    '<figure><img src="a.png" alt=""><figcaption>The Channels tab</figcaption></figure>');
});
test('an image inside text is left alone', async () => {
  assert.equal(await run('<p>See <img src="a.png" alt="x"> here.</p>'), '<p>See <img src="a.png" alt="x"> here.</p>');
});
```

- [ ] **Step 2: Write the failing site test in `tests/test_content.py`**

```python
class Content(unittest.TestCase):
    def test_quickstart_screenshots_have_captions(self):
        doc = page('/work/quickstart/')
        self.assertIn('<figcaption>The template catalog, filtered by category, with the Empty Agent card first</figcaption>', doc)
        self.assertRegex(doc, r'<figure>\s*<img[^>]+src="/_astro/')

    def test_short_opening_is_a_lead(self):
        self.assertIn('class="lead"', page('/work/quickstart/'))
```

- [ ] **Step 3: Run to verify they fail**

Run: `npm run test:unit; npm run build && npm run test:site`
Expected: FAIL.

- [ ] **Step 4: Implement both plugins and register them in `markdown.rehypePlugins`**

Put `rehypeFigure` first. Confirm in the built output that Astro still optimises the images (the `src` points into `/_astro/`).

- [ ] **Step 5: Run to verify they pass**

Run: `npm run test:unit && npm run build && npm run test:site && npm run check`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/plugins astro.config.mjs package.json package-lock.json tests/test_content.py
git commit -m "feat(docs): lead paragraphs and captions under screenshots"
```

---

### Task 7: The docs home page

**Files:**
- Create: `src/components/home/HomeHero.astro`, `ProductCards.astro`, `MiniAgents.astro`, `MiniKeel.astro`, `UseCases.astro`, `HelpBand.astro`, `tests/test_home.py`
- Modify: `src/content/docs/index.mdx` (rewrite), `astro.config.mjs` (`components.Hero`, `title: 'Surogate Docs'`, `description`, the `twitter:*` and keywords meta), `migration/assert_content.py` only if its expectations break

**Interfaces:**
- Consumes: `AgentsMark`, `KeelMark` from Task 4.
- Produces: `index.mdx` with frontmatter `title: Surogate documentation`, `template: splash` and a `hero` (so Starlight sets `data-has-hero` and renders the Hero override), and a body that imports and renders `<ProductCards />`, `<UseCases />` and `<HelpBand />`.

- [ ] **Step 1: Write the failing tests in `tests/test_home.py`**

```python
TASKS = [
    ('Deploy a customer-support agent in 10 minutes', '/work/use-cases/#1-deploy-a-customer-support-bot-in-10-minutes'),
    ('Add Slack so your team can chat with the same agent', '/work/use-cases/#2-add-slack-so-your-team-can-chat-with-the-same-agent'),
    ('Build a knowledge base from your wiki and tickets', '/work/use-cases/#4-build-a-product-knowledge-base-from-internal-wiki--tickets'),
    ('Fine-tune an expert from your agent', '/develop/use-cases/#1-fine-tune-an-expert-from-your-traffic'),
    ('Run batch jobs through the API', '/develop/use-cases/#6-integrate-via-the-api-channel-for-batch-jobs'),
    ('Build a loan request and work your first case', '/keel/quickstart/'),
    ('Route cases by amount with a decision table', '/keel/builder/rules/'),
    ('Give a team a queue with a serving order', '/keel/builder/queues/'),
    ('Let an agent work a step and ask when unsure', '/keel/business/agents/'),
    ('Test a case type with scenarios before you publish', '/keel/builder/scenarios/'),
]

class Home(unittest.TestCase):
    def setUp(self):
        self.doc = page('/')

    def test_hero(self):
        self.assertIn('Surogate documentation', self.doc)
        self.assertIn('Guides, tutorials and reference for Surogate Agents and Keel.', self.doc)

    def test_product_cards(self):
        self.assertEqual(self.doc.count('data-docs="product-card"'), 2)
        self.assertIn('Two products, built to work together.', self.doc)
        for href in ('href="/work/"', 'href="/work/quickstart/"', 'href="/keel/"', 'href="/keel/quickstart/"'):
            self.assertIn(href, self.doc)

    def test_tasks_link_to_real_sections(self):
        for title, href in TASKS:
            self.assertRegex(self.doc, rf'href="{re.escape(href)}"[^>]*>[\s\S]*?{re.escape(title)}')
            path, _, anchor = href.partition('#')
            if anchor:
                self.assertIn(f'id="{anchor}"', page(path))

    def test_help_band(self):
        band = section(self.doc, 'help-band')
        self.assertIn('surogate@invergent.ai', band)
        self.assertIn('href="/work/whats-new/"', band)
        self.assertNotIn('API reference', band)

    def test_old_home_is_gone(self):
        for old in ('Multiply yourself', 'Vibecode', 'The improvement loop'):
            self.assertNotIn(old, self.doc)
```

The anchors above are the slugs Starlight generates from the use-case headings. If one differs, take the real `id` from the built page; the second assertion in `test_tasks_link_to_real_sections` catches a wrong one.

- [ ] **Step 2: Run to verify they fail**

Run: `npm run build && npm run test:site`
Expected: FAIL.

- [ ] **Step 3: Implement**

Build each section from the mockup's `home()`, with the copy exactly as in the spec's "The docs home" section:
- `HomeHero` is the aubergine band, with the large search field opening Starlight's search dialog.
- `ProductCards` holds two `article data-docs="product-card"` elements. Each has its mark at 48 px, its name, its line, its drawing (`MiniAgents` / `MiniKeel`, the mockup's `mini_agents()` and `mini_keel()` with `style="fill: var(--d-…)"` instead of attributes), the button and the Quickstart link. A 4 px `--d-rule` top border, square.
- `UseCases` has two columns of `a data-docs="task"` rows, each with its label on the right, on `--d-soft`.
- `HelpBand` holds the help line and the What's new and Discord links.

Make the home bands full width with CSS scoped to `html[data-has-hero]`: remove the content panel padding and the `sl-container` max width, and give each band its own 1200 px inner container. Set `title: 'Surogate Docs'`, the description "Guides, tutorials and reference for Surogate Agents and Keel.", and matching `twitter:*` and keywords meta. If `assert_content.py` fails on the home page, update only the expectation the home rewrite changed.

- [ ] **Step 4: Run to verify they pass**

Run: `npm run build && npm run test:site && npm run check && python3 migration/assert_content.py && python3 migration/check_routes.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/home src/content/docs/index.mdx astro.config.mjs migration/assert_content.py tests/test_home.py
git commit -m "feat(docs): product-choice home page"
```

---

### Task 8: Visual check against the mockups

**Files:**
- Modify: whatever CSS or component the check shows is off. No new tests beyond the Review Focus items.

- [ ] **Step 1: Capture screenshots**

Run `npm run build && npm run preview` and capture, in both themes (set `localStorage['starlight-theme']` before load):
- `/` and `/work/quickstart/` at 1440 px;
- `/` and `/work/quickstart/` at 375 px;
- `/keel/builder/rules/` at 1440 px.

Compare each with the matching artboard: Docs home, Docs home dark, Docs page A, Docs page A dark.

- [ ] **Step 2: Check the Review Focus items in a browser**

- At 375 px there's no horizontal scroll, and the mobile menu shows the product head, the switch, the product links, the theme button and Sign in.
- After picking dark, a reload and a link click stay dark. With `starlight-theme` cleared, the OS setting wins.
- In dark mode, the search dialog, the mobile menu, the mobile "On this page" dropdown, a badge (the "Coming soon" badge on `/develop/features/experts-arenas/` in the sidebar) and a tab group are on dark tokens.
- A long breadcrumb wraps.
- Focus rings are visible on the switch, the theme button and the product links.

- [ ] **Step 3: Fix what differs and re-run the full suite**

Run: `npm run test:unit && npm run build && npm run check && npm run test:site && python3 migration/assert_content.py && python3 -m unittest discover -s migration -p 'test_*.py' && python3 migration/check_routes.py`
Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add -A src astro.config.mjs
git commit -m "fix(docs): match the mockups in both themes and on phones"
```

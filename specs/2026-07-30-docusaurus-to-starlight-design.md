# Migrating surogate-docs from Docusaurus to Astro Starlight

**Date:** 2026-07-30
**Status:** design, awaiting approval
**Branch:** `feat/starlight-migration`
**Target versions:** Astro 7.1.6, `@astrojs/starlight` 0.41.5

> Spec lives in `specs/` rather than `docs/superpowers/specs/` because `docs/` is the
> Docusaurus content root — any `.md` placed there becomes a live page.

---

## 1. Goal

Replace Docusaurus 3.9 with Astro Starlight, preserving all operator and builder
documentation content and keeping every live URL reachable. Replace custom code with
native Starlight features wherever one exists ("port + simplify"), and archive the
legacy training-framework documentation.

Non-goals: content rewrites, IA restructuring, a screenshot pass, Tailwind, i18n.

---

## 2. Evidence base

Every claim below is backed by direct measurement of this repo, an observed Starlight
build, or a live HTTP check. Three evidence sources:

- **[probe]** — a throwaway Starlight 0.41.5 site built to test behaviours the official
  docs do not document. At
  `/tmp/claude-1000/-work-surogate-ops/<session>/scratchpad/sl-probe`.
- **[audit]** — a parallel multi-agent inventory of the repo plus an adversarial
  completeness review. It caught four things direct greps missed (§9).
- **[live]** — `curl` against the deployed site.

§9 records every assumption these overturned. Two would have shipped silently broken.

---

## 3. Scope

### In scope — 72 files

| Tree | Files | Serves |
|---|---|---|
| `docs/work/` | 36 | Operator track, `/work/*` |
| `docs/develop/` | 36 | Builder track, `/develop/*` |

### Out of scope — deleted, no redirects

| Item | Count | Rationale |
|---|---|---|
| Legacy trainer tree: `docs/index.mdx`, `about/`, `getting-started/`, `guides/`, `examples/`, `reference/`, `appendix/` | ~46 files | Documents the `surogate` training framework, a different product. Recoverable from git history. **Correction (found at execution):** an earlier claim of "zero links from work/ or develop/ into this tree" was wrong — that grep only matched root-absolute forms. `develop/features/memory.md` carried a *relative* link, `[memory guide](../../guides/memory.md)`. The link validator caught it; the sentence now disambiguates agent memory from GPU memory without the dead cross-reference. |
| `static/img/screenshots/*.png` | 42 | **Referenced by no page anywhere in the repo.** Committed in `2b00238` "v2.3: audit-driven expansion + visual pipeline"; the `<Figure>` calls that would have consumed them were never written. |
| `static/img/transformer-block.{png,svg}` | 2 | Used only by the legacy tree. |

Their URLs will 404. Accepted decision, not an oversight.

---

## 4. What the surviving 72 files actually contain

Measured fence-aware, not assumed. This is why the migration is small:

| Feature | Uses in the 72 files |
|---|---|
| Images (`![]()`, `<Figure>`, `<img>`) | **0** |
| Mermaid diagrams | **0** (theme configured, nothing uses it — repo-wide) |
| Math (`$$`, remark-math) | **0** |
| `<Tabs>` / `<TabItem>` | **0** |
| MDX `import` / `export` | **0** |
| `<details>` / raw JSX | **0** |
| Explicit heading IDs `{#id}` | **0** |
| Admonitions | **13** (9 plain + 4 blockquote-wrapped) |
| Real `<h1>` headings | 71 files × 1, plus 1 file × 2 |
| `# ` lines that are **code-fence comments** | **22** |
| Stray tool-call XML artifacts in prose | **4** |
| Duplicate heading slugs | 2 files |
| Frontmatter keys | `title` (72), `sidebar_position` (72), `slug` (2), `sidebar_label` (2), `draft` (1) |

---

## 5. Target repository layout

```
astro.config.mjs                    replaces docusaurus.config.js (194 lines) + sidebars.js (258 lines)
tsconfig.json                       NEW — none exists today; required by `astro check`
package.json                        5 packages, down from 27
.gitignore                          add dist/ and .astro/
src/content.config.ts               docsLoader() + docsSchema()
src/content/docs/
  index.mdx                         splash homepage (replaces src/pages/index.jsx)
  work/…       36 files             moved from docs/work/
  develop/…    36 files             moved from docs/develop/
src/styles/custom.css               ~20 lines, replaces 98-line src/css/custom.css
src/assets/logo-black.svg
src/assets/logo-white.svg
src/components/HeaderLogin.astro    SocialIcons override — the one custom component
public/CNAME                        docs.surogate.ai   (new)
public/favicon.svg                  new — see §8
public/og-card.png                  new — see §8
public/robots.txt                   new — see §8
specs/                              this document
migration/baseline-urls.txt         frozen pre-cutover fixture — see §10 gate 0
.github/workflows/deploy-docs.yml   rewritten build step
```

### Deleted

`docusaurus.config.js`, `sidebars.js`, `src/pages/`, `src/css/`, `static/`,
`src/theme/` (4 overrides: `Root.js`, `MDXComponents.js`, `ColorModeToggle/`,
`NavbarItem/ComponentTypes.js`), `src/components/` (`Figure`, `LogoGrid`,
`ModeToggle`, `MuiTheme`).

### Dependency reduction — 27 → 5

Today: 26 `dependencies` + 1 `devDependency` (`@docusaurus/module-type-aliases`),
verified from `package.json`.

Dropped: all 8 `@docusaurus/*` packages, `@mui/material`, `@mui/icons-material`,
`@emotion/react`, `@emotion/styled`, `primeflex`, `rehype-katex`, `remark-math`,
`remark-cli`, `remark-lint`, `remark-lint-no-dead-urls`, `remark-validate-links`,
`remark-validate-links-heading-id`, `prism-react-renderer`, `clsx`, `react`,
`react-dom`, `@mdx-js/react`, `yarn`.

Added — 4 `dependencies` (`astro`, `@astrojs/starlight`, `starlight-links-validator`,
`@fontsource/inter` per §7.5) + 1 `devDependency` (`typescript`, for `astro check`).

`react`/`react-dom`/MUI exist solely to serve `src/pages/index.jsx` and
`src/theme/Root.js`; both are deleted, so the whole tree goes.

---

## 6. Content transform

Ordered. Steps 6.1 and 6.5 are scripted; the rest are hand edits with scripted
verification.

### 6.0 Scaffold first, move content second

Commit 1 is a stock Starlight site building green with three placeholder pages:
`astro.config.mjs`, `src/content.config.ts`, `tsconfig.json`, `package.json`,
`public/`, and the `.gitignore` update. Content moves only once `astro build` and
`astro check` are clean. This keeps a red build attributable to one cause at a time.

### 6.1 Strip the leading `# H1` — 72 files, scripted, **fence-aware**

Starlight's `PageTitle` component *is* the page `<h1>`; the reference calls it
"Component containing the `<h1>` element for the current page."

**[probe]** `title: Hello` + body `# Hello World` emits two `<h1>`s:

```html
<h1 id="_top" class="astro-2sm4b3ln">Hello</h1>   <!-- frontmatter title -->
<h1 id="hello-world">Hello World</h1>             <!-- body heading -->
```

Pagefind indexes both as separate anchors.

Measured: in all 72 files the first non-blank body line is the H1 — zero exceptions —
so the leading strip is unambiguous.

⚠ **The transform must be fence-aware.** 22 `# ` lines in these files are shell and
Python comments inside code fences (`# List sessions matching filters`,
`# The same Stripe secret key…`). A naive `sed '/^# /d'` or `grep -v '^# '` would
delete them, silently corrupting ~20 code examples across
`develop/use-cases.md`, `work/monetize.md`, `develop/loop/observe.md`,
`develop/quickstart.md`, `develop/reference/event-types.md` and others. The script
tracks fence state and removes only the first heading outside a fence.

### 6.2 Reconcile the 14 title/H1 mismatches

Rule agreed: richer H1 text becomes `title:`, short text becomes `sidebar.label`. No
editorial wording lost, sidebar entries stay short.

| File | New `title:` | New `sidebar.label` |
|---|---|---|
| `work/intro.md` | Work mode | Welcome |
| `work/channels/web.md` | Web channel | Web |
| `work/channels/slack.md` | Slack channel | Slack |
| `work/channels/telegram.md` | Telegram channel | Telegram |
| `work/channels/users.md` | Per-agent users | Users |
| `work/channels/self-registration.md` | Let end users sign up for your agent | Self-registration |
| `develop/intro.md` | Develop mode | Welcome |
| `develop/loop/overview.md` | The builder loop | Overview |
| `develop/loop/build.md` | Build phase — designing the agent | Build |
| `develop/loop/observe.md` | Observe phase — what the agent actually does | Observe |
| `develop/loop/train.md` | Train phase — using observed signal | Train |
| `develop/loop/redeploy.md` | Redeploy phase — rolling out the changes | Redeploy |
| `develop/features/byo-llm.md` | BYO LLM (Bring Your Own LLM) | BYO LLM |
| `develop/features/skills-and-experts.md` | Skills & Experts (unchanged) | Skills & Experts |

`work/intro.md` and `develop/intro.md` already carry `sidebar_label: Welcome`, which
becomes `sidebar.label: Welcome`.

### 6.3 `develop/features/skills-and-experts.md` — the one structural edit

This is the only file with **two real H1s**, and its title conflict is substantive
rather than cosmetic:

```
line   2   # Skills & Tools                    ← first H1
line 180   # Experts — model-backed skills     ← second H1
```

The page is two documents concatenated. `# Skills & Tools` also collides with the
label of a *different* Work-track sidebar group.

Resolution: keep `title: Skills & Experts` (the accurate umbrella), delete the
`# Skills & Tools` H1 per §6.1, and **demote `# Experts — model-backed skills` to
`##`** so it becomes a peer of the page's other `##` sections. Its `###` children are
untouched. Result: correct heading order, correct ToC, no rogue H1.

⚠ Mild semantic flattening — "Experts" becomes a sibling of `## SKILL.md format`
rather than of the whole Skills half. The clean fix is splitting the page in two,
which is content restructuring and out of scope. **Flagged in §15.**

### 6.4 Rewrite all 13 admonitions

**[probe]** All failure modes are silent — clean build, no warning:

| Input | Starlight output |
|---|---|
| `:::note` / `:::tip` / `:::caution` / `:::danger` | correct `<aside class="starlight-aside--*">` |
| `:::info` | **bare `<div>`** — no aside, no icon, no title, no error |
| `:::warning` | **bare `<div>`** — same |
| `:::note[Free plan]` | correct aside, title "Free plan" |
| `:::note Free plan` | aside renders, **the words "Free plan" are deleted entirely** |

Starlight supports exactly four types: `note`, `tip`, `caution`, `danger`.

**Plain — 9:**

| File:line | Current | Becomes |
|---|---|---|
| `develop/features/datasets.md:89` | `:::note` | unchanged |
| `work/channels/self-registration.md:48` | `:::info` | `:::note` |
| `work/channels/self-registration.md:81` | `:::warning` | `:::caution` |
| `work/channels/self-registration.md:115` | `:::tip` | unchanged |
| `develop/features/compute.md:42` | `:::note Free plan` | `:::note[Free plan]` |
| `develop/features/compute.md:46` | `:::warning Billing` | `:::caution[Billing]` |
| `develop/features/experts-arenas.md:13` | `:::note Preview` | `:::note[Preview]` |
| `develop/features/connect-compute.md:62` | `:::note Preview` | `:::note[Preview]` |
| `develop/features/connect-compute.md:99` | `:::note Free plan` | `:::note[Free plan]` |

**Blockquote-wrapped — 4.** These were missed by a `^:::` grep and found by
**[audit]**. Every line carries a `> ` prefix:

```markdown
> :::info Credentials never reach the sandbox
> The agent's sandbox is the most untrusted component in the platform. …
> :::
```

| File:line | Current | Becomes |
|---|---|---|
| `work/library/knowledge-bases.md:64-66` | `> :::warning Curator model is locked` | de-quote → `:::caution[Curator model is locked]` |
| `work/library/knowledge-bases.md:76-78` | `> :::tip Smaller is more reliable` | de-quote → `:::tip[Smaller is more reliable]` |
| `work/library/mcp-servers.md:59-61` | `> :::info Credentials never reach the sandbox` | de-quote → `:::note[Credentials never reach the sandbox]` |
| `work/library/skills.md:64-66` | `> :::info Templates are real, not empty` | de-quote → `:::note[Templates are real, not empty]` |

The `> ` prefix must be stripped from every line of these four blocks. A
type-and-title-only rewrite would leave a blockquote wrapping an aside — or an
unclosed directive. Hand-edited, not scripted.

Type breakdown checks out: note ×5, info ×3, warning ×3, tip ×2 = 13.

### 6.5 Rewrite the 240 internal links — scripted, then build-gated

**[probe] Astro rewrites nothing.** All four forms pass through byte-for-byte with
**zero build warnings**, and no config option exists (`grep -rl
'markdownLinks\|resolveRelativeLinks\|rewriteMarkdownLinks'` over
`node_modules/astro/dist` returns nothing):

```html
<a href="../b/two.md">   <a href="../b/two">   <a href="/b/two">   <a href="./one.md">
```

Served and curled under the chosen config (§7.2), only `/b/two` returns 200. Every
`.md` link is a 404.

Current state: **240 relative links carrying `.md`**, 26 root-absolute, 8 anchor-only,
15 external.

Transform: all 240 → root-absolute, extensionless, **with trailing slash** —
`](../tools/chat.md)` → `](/work/tools/chat/)`. Root-absolute is the only form that
resolves in every config, and `starlight-links-validator` rejects relative links
outright. Anchor-only and external links untouched.

### 6.6 `slug` frontmatter — 2 files

`slug: /work` → `slug: work`; `slug: /develop` → `slug: develop`.

**[probe]** `slug: work` emits `dist/work/index.html`, no `dist/work/intro/`,
coexists with `/work/*` children, and resolves from `{ slug: 'work' }`. Caveat: a
duplicate slug produces only `[WARN] Duplicate id … Later items with the same id will
overwrite earlier ones` — silent content loss, so §10 gate 4 lints for it.

### 6.7 Delete 4 stray tool-call XML artifacts — **[audit]**

Three in-scope files end with orphaned closing tags that were never meant to ship:

| File:line | Content |
|---|---|
| `develop/features/compute.md:112` | `</content>` |
| `work/library/mcp-servers.md:110` | `</content>` |
| `work/library/skills.md:153` | `</content>` |
| `work/library/skills.md:154` | `</invoke>` |

All four sit outside any code fence, as the literal last lines of the file. Under
Docusaurus's CommonMark parsing they pass through as dropped raw HTML and go
unnoticed — they ship today, invisibly. Delete them. (They would be a hard parse
error if these files were ever `.mdx`.)

### 6.8 The two orphan pages

Neither appears in any sidebar today.

- **`develop/features/agents.md`** — builds today, reachable only by direct URL. It is
  **load-bearing**: linked four times from prose (`develop/tools/copilot.md:60`,
  `develop/loop/redeploy.md:102`, `develop/loop/build.md:106` and `:114`) and is the
  target of the `/ops/features/agents` redirect. Someone forgot to add it. Added to
  the Develop sidebar.
- **`develop/features/experts-arenas.md`** — carries **`draft: true`**, which is *why*
  it is orphaned: Docusaurus excludes drafts from production builds and Starlight
  honours the same flag. Zero inbound links from anywhere. **Adding it to the sidebar
  requires removing `draft: true`, publishing a page that has never been publicly
  visible.** It gains `badge: { text: 'Preview', variant: 'caution' }`.

⚠ **A content-visibility change, not a mechanical one. Needs explicit sign-off (§15).**
If withheld, it stays `draft: true` and out of the sidebar, exactly as today.

### 6.9 Duplicate heading slugs — verify, don't assume

Two in-scope files reuse headings, fence-aware measured:

| File | Duplicate slug | Count |
|---|---|---|
| `develop/use-cases.md` | `steps` | 7 |
| `work/use-cases.md` | `steps` | 4 |
| `work/use-cases.md` | `follow-up` | 4 |

Docusaurus dedupes via `github-slugger` (`steps`, `steps-1`, `steps-2`, …). Astro 7
generates heading IDs with its own markdown processor, and dedupe suffixing is exactly
where implementations diverge. All 15 of these anchors are live deep-link targets.

Action: build both files under Astro 7 and diff emitted heading IDs against today's
`build/**/index.html`. If they diverge, rename the duplicate headings — they are
genuinely ambiguous ToC entries ("Steps" seven times) and renaming is the better fix
regardless. Do this **before** the link rewriter runs, since §6.5 must emit correct
anchors.

---

## 7. Configuration

### 7.1 Navigation — one sidebar, two groups

The trainer sidebar is gone; the remaining two become sibling top-level groups in a
single sidebar, preserving current order and category labels. Ten per-page label
overrides move from `sidebars.js` into frontmatter (`sidebar: { label: … }`), the
documented mechanism, so a page owns its own label: `work/workflow/review-sessions` →
Sessions, `work/library/knowledge-bases` → Knowledge Bases, `develop/tools/dashboard`
→ Dashboard, `develop/features/sessions` → Sessions, `develop/features/models` →
Models, `develop/features/playground` → Playground, `develop/features/hub` → Data Hub,
`develop/features/datasets` → Datasets, `develop/features/training` → Training,
`develop/features/evaluations` → Evaluations.

```js
sidebar: [
  { label: 'Work — for operators', items: [
    'work',                                   // slug: work → /work/
    'work/quickstart',
    { label: 'Agents', collapsed: true, items: [
      'work/workflow/run-agent', 'work/workflow/configure-agent',
      'work/tools/chat', 'work/tools/commands', 'work/tools/goals',
      'work/tools/missions', 'work/tools/scheduled-work',
      'work/tools/deep-research', 'work/tools/code',
      'work/tools/sub-agents', 'work/tools/inbox',
      'work/workflow/improve-agent',
    ]},
    'work/workflow/review-sessions',
    { label: 'Skills & Tools', collapsed: true, items: [
      'work/library/skills', 'work/library/mcp-servers',
      'work/library/integrations', 'work/workflow/templates',
    ]},
    'work/library/knowledge-bases',
    { label: 'Channels', collapsed: true, items: [
      'work/channels/web', 'work/channels/slack', 'work/channels/telegram',
      'work/channels/website-widget', 'work/channels/users',
      'work/channels/self-registration', 'work/channels/proactive',
    ]},
    { label: 'Settings', collapsed: true, items: [
      'work/settings/profile', 'work/settings/settings',
      'work/settings/usage', 'work/settings/billing',
    ]},
    'work/tools/copilot', 'work/monetize', 'work/use-cases',
    { label: 'Reference', collapsed: true, items: [
      'work/reference/glossary', 'work/reference/faq',
    ]},
  ]},
  { label: 'Develop — for builders', items: [
    'develop',                                // slug: develop → /develop/
    'develop/quickstart',
    { label: 'The builder loop', collapsed: true, items: [
      'develop/loop/overview', 'develop/loop/build', 'develop/loop/observe',
      'develop/loop/train', 'develop/loop/redeploy',
    ]},
    'develop/tools/dashboard',
    'develop/features/agents',                // newly surfaced (§6.8)
    'develop/features/sessions', 'develop/features/models',
    'develop/features/playground', 'develop/features/hub',
    'develop/features/datasets', 'develop/features/training',
    'develop/features/evaluations',
    { label: 'Compute', collapsed: true, items: [
      'develop/features/compute', 'develop/features/connect-compute',
    ]},
    { label: 'Skills & knowledge', collapsed: true, items: [
      'develop/features/skills-and-experts', 'develop/features/skill-optimization',
      'develop/features/knowledge-bases', 'develop/features/mcp-and-vault',
      'develop/features/byo-llm',
      { slug: 'develop/features/experts-arenas',
        badge: { text: 'Preview', variant: 'caution' } },   // newly surfaced (§6.8)
    ]},
    { label: 'Agent capabilities', collapsed: true, items: [
      'develop/features/memory', 'develop/features/browser',
      'develop/features/browser-profiles',
    ]},
    { label: 'Tools', collapsed: true, items: [
      'develop/tools/copilot', 'develop/tools/templates',
    ]},
    'develop/use-cases',
    { label: 'Reference', collapsed: true, items: [
      'develop/reference/runtime-architecture', 'develop/reference/tool-catalog',
      'develop/reference/event-types', 'develop/reference/background-jobs',
      'develop/reference/coordination', 'develop/reference/glossary',
    ]},
  ]},
]
```

**Deliberate change:** all inner subgroups `collapsed: true`. Today each track owns a
whole sidebar so several groups sit expanded; sharing one sidebar puts ~72 entries in
one column. Only the two top-level groups stay open. Reversible in one edit.

Prev/next pagination now flows continuously, ending the Work track at the start of the
Develop track. That is desirable here; if not, `pagination: false` globally or
`next: false` on the boundary page.

### 7.2 URLs — Astro defaults, trailing slash accepted

**[live]** measured:

| URL | Response |
|---|---|
| `https://docs.surogate.ai/work/tools/chat` | **200** |
| `https://docs.surogate.ai/work/tools/chat/` | **404** |
| `https://docs.surogate.ai/ops/features/agents` | **301** → `/ops/features/agents/` |

Today's canonical form is extensionless with no trailing slash, and the host 301s
extensionless → trailing-slash whenever a directory index exists.

**[probe]** three configurations:

| Config | hrefs | canonical | sitemap | Pagefind | verdict |
|---|---|---|---|---|---|
| `format:'file'` | `/work/tools.html` | `.html` | extensionless | `.html` | **rejected** — `.html` in every href, incl. `href="/index.html"` on the site title; canonical/sitemap disagree |
| `trailingSlash:'never'` + `format:'directory'` | `/work/tools` | matches | matches | `/work/tools/` | **rejected on this host** — every href would 301 |
| **defaults** (`format:'directory'`) | `/work/tools/` | matches | matches | matches | **chosen** |

Decision: **Astro defaults.** Canonical URLs become `/work/tools/chat/`; today's
`/work/tools/chat` 301s to it, so inbound links, bookmarks and search results keep
resolving and Google re-canonicalises across a crawl cycle. Every emitted URL,
canonical tag, sitemap entry and search result agrees. Internal links are written
*with* the trailing slash (§6.5) to avoid a 301 per click.

### 7.3 `astro.config.mjs`

```js
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';

export default defineConfig({
  site: 'https://docs.surogate.ai',
  // No `base` — custom domain. No trailingSlash / build.format overrides (§7.2).
  redirects: {
    '/ops':                           '/work/',
    '/ops/getting-started/quickstart':'/work/',
    '/ops/features/agents':           '/develop/features/agents/',
    '/ops/features/skills':           '/develop/features/skills-and-experts/',
    '/ops/features/knowledge-bases':  '/develop/features/knowledge-bases/',
    '/ops/features/models':           '/develop/features/models/',
    '/ops/features/datasets':         '/develop/features/datasets/',
    '/ops/features/training':         '/develop/features/training/',
    '/ops/features/evaluations':      '/develop/features/evaluations/',
    '/ops/features/sessions':         '/develop/features/sessions/',
    '/ops/features/compute':          '/develop/features/compute/',
    '/ops/features/hub':              '/develop/features/hub/',
    '/ops/features/templates':        '/develop/tools/templates/',
    '/search':                        '/',        // §7.7 — was a real page
  },
  integrations: [starlight({
    title: 'Surogate',
    description: 'Documentation for Surogate Ops — operator and builder tracks.',
    logo: { light: './src/assets/logo-black.svg',
            dark:  './src/assets/logo-white.svg',
            alt: 'Surogate', replacesTitle: false },   // §7.4
    favicon: '/favicon.svg',
    customCss: ['@fontsource/inter/400.css', '@fontsource/inter/600.css',
                './src/styles/custom.css'],
    social: [
      { icon: 'github', label: 'GitHub', href: 'https://github.com/invergent-ai/surogate' },
      { icon: 'x.com',  label: 'X',      href: 'https://x.com/surogate_ai' },
    ],
    editLink: { baseUrl: 'https://github.com/invergent-ai/surogate-docs/edit/main/' },
    components: { SocialIcons: './src/components/HeaderLogin.astro' },
    head: [ /* gtag G-7YRDGYZN0R; og:*, twitter:* tags; keywords — §7.6 */ ],
    plugins: [starlightLinksValidator()],
    sidebar: [ /* §7.1 */ ],
  })],
});
```

All 14 entries above (13 `/ops/*` ported verbatim from `docusaurus.config.js`, plus the
new `/search`) are static literals — no wildcards.
**[probe]** each emits a meta-refresh stub —
correct for a static build, excluded from the sitemap:

```html
<!doctype html><title>Redirecting to: /work/</title>
<meta http-equiv="refresh" content="0;url=/work/">
<meta name="robots" content="noindex">
<link rel="canonical" href="https://docs.surogate.ai/work/">
```

Recorded constraint: prefix-rewriting wildcards are **impossible** in `astro.config`.
`'/ops/features/[...slug]': '/develop/features/[...slug]'` is a hard build failure
(`InvalidRedirectDestination`); only `'/prefix/[...slug]': '/[...slug]'` works, and the
param must literally be named `slug`. Not needed here, but any future bulk redirect
belongs at the host layer.

### 7.4 Header

Starlight's header holds only site title, search, social icons and the theme toggle —
there is no arbitrary top-nav-links config.

| Today | Becomes |
|---|---|
| GitHub | native `social` icon |
| Follow us on X | native `social` icon |
| Login → ops.surogate.ai | `HeaderLogin.astro`, ~20-line `SocialIcons` override |
| About → surogate.ai | **dropped from chrome**; splash-page action button instead |
| Search | Pagefind modal |
| Work/Develop pill toggle | **deleted** — superseded by the two sidebar groups |

Login keeps header prominence as the only one of the four with commercial value.
"About" is reachable via the logo, the splash CTA and the GitHub icon.

**[audit] — two config values have no Starlight home.** Docusaurus sets
`navbar.title: 'Documentation'` (rendered *next to* the logo) and
`tagline: 'AgentOps Factory'`. Starlight has no `tagline` option at all, and its
`description` is the meta-description, not visible chrome. With
`replacesTitle: false` the header reads logo + "Surogate" — so the visible word
changes from "Documentation" to "Surogate". Deliberate: "Surogate" is the site title
and the docs context is already implied by the domain. **Flagged in §15.**

### 7.5 Styling

98 lines → ~20. Only the brand green survives, mapped to Starlight accent tokens:
`#07a000` light, `#87ed82` dark.

Inter moves from a runtime `@import url('https://fonts.googleapis.com/…')` at
`custom.css:10` to self-hosted `@fontsource/inter` — removes a render-blocking
third-party request and a privacy dependency.

Dead on arrival: all `--ifm-*` variables, Docusaurus-internal selectors
(`.tabs-container`, `.footer--dark`, `.header-github-link`), the KaTeX override, the
asciinema terminal theme, and the `primeflex` import.

⚠ **[audit] — the consequence nobody signed off on.** Because `custom.css` contains no
`.navbar` / `.menu__*` / `.theme-doc-*` / `.markdown` selectors, there is nothing to
port — which means **the shipped site will look like default Starlight**: different
sidebar, different table of contents, different type scale, Starlight's token model
instead of Infima's, and clickable heading anchors. This is the single most visible
change to every reader. §10 gate 6 makes it an explicit sign-off, not a surprise.

### 7.6 Head, SEO, and analytics

`head:` carries the gtag `G-7YRDGYZN0R` snippet and the og/twitter/keywords tags.

**[audit]** Starlight's head builder emits `og:title`/`og:description` but **not**
`twitter:title` or `twitter:description` — so those are kept explicitly rather than
dropped as "redundant". `og:image`, `og:image:alt`, `twitter:card` and `twitter:image`
are kept and repointed at the new `og-card.png` (§8).

`public/robots.txt` is added pointing at the sitemap — there is none today, a
regression-free win.

Optional, out of the critical path: `starlight-llms-txt` to emit an `llms.txt`. For
documentation *about building agents*, an AI-crawler surface is close to table stakes.
**Flagged in §15.**

### 7.7 Search

Pagefind, Starlight's default, replacing Algolia DocSearch (app `K46M9C3QXR`, index
"Surogate Docs"). No crawler, no keys, indexes at build time, correct on first deploy.
Accepted trade-offs: weaker ranking and no search analytics. The Algolia account stays
untouched and is reinstatable later via `@astrojs/starlight-docsearch`.

⚠ **[audit] — two artifacts disappear that the plan nearly missed.**
`@docusaurus/theme-search-algolia` generates a real `/search` **page** and an
`/opensearch.xml`. Both verified **[live]** as HTTP 200, and `/search` is in today's
sitemap. Pagefind is a modal only — no search page, no OpenSearch document.
Consequences: the indexed `/search` URL 404s, and browser address-bar site-search
breaks.

Mitigation: `/search` → `/` redirect (§7.3). OpenSearch is a deliberate loss —
hand-writing `public/opensearch.xml` would point at a `/search?q=` route that no
longer exists. **Flagged in §15.**

### 7.8 Homepage

`src/pages/index.jsx` (141 lines of React + inline style objects) →
`src/content/docs/index.mdx` with `template: splash`, a `hero` (title, tagline,
`surogate.ai` and Work/Develop action buttons), and a `CardGrid` of `LinkCard`s. The
"What is Surogate?" prose, three-repo list, and which-mode table carry over as
Markdown. Its `<Link to="/old-docs">` footnote goes with the legacy tree.

No filename collision: the legacy `docs/index.mdx` (which held `slug: /old-docs`) is
deleted, freeing `index.mdx`.

---

## 8. Assets that are already broken

`docusaurus.config.js` references two files that **do not exist**:

- `favicon: 'img/favicon.ico'` → absent. The site has had no favicon.
- `og:image`/`twitter:image` → `https://docs.surogate.ai/img/social-card.jpg` →
  absent. Every social share preview is broken.

Both are created during the migration (`public/favicon.svg`, `public/og-card.png`)
from the existing `logo-black.svg` / `logo-white.svg`, rather than porting dangling
references.

There is also **no `CNAME` file**, so the custom domain relies on an implicit GitHub
Pages repository setting that lives outside the artifact. Adding `public/CNAME` makes
it explicit and survivable — an improvement, not a prerequisite.

---

## 9. Assumptions this design corrected

Recorded so the reasoning is auditable. Two would have shipped silently broken.

1. **`build.format: 'file'` was proposed to preserve exact URLs, and is wrong.**
   **[probe]** It bakes `.html` into every href, canonical, `og:url` and Pagefind
   result, and builds with **zero warnings**. Superseded by §7.2.
2. **Relative `.md` link handling was listed as an open question.** **[probe]** It is
   not ambiguous: Astro rewrites nothing and warns about nothing. All 240 links are a
   mandatory rewrite; the link validator is load-bearing.
3. **The admonition rewrites were scoped as cosmetic.** **[probe]** They are silent
   content loss: `:::note Free plan` deletes the title text; `:::info`/`:::warning`
   degrade to unstyled `<div>`s.
4. **The admonition count was 9. It is 13.** **[audit]** A `^:::` grep misses the four
   blockquote-wrapped ones (`> :::info …`), which also need de-quoting (§6.4).
5. **"Strip the body H1" would have destroyed 22 code comments.** 71 files have exactly
   one real H1, but 22 `# ` lines are shell/Python comments inside fences. The
   transform must be fence-aware (§6.1).
6. **Four stray `</content>` / `</invoke>` artifacts ship in prose today.** **[audit]**
   Invisible under CommonMark. Deleted (§6.7).
7. **`/search` and `/opensearch.xml` are real, live artifacts** that vanish with
   Pagefind. **[audit]** + **[live]**. Mitigated (§7.7).
8. **`tsconfig.json` does not exist**, so `astro check` could not have run. Added
   (§5).
9. **Duplicate heading anchors were assumed to survive** because both systems "use
   github-slugger". Dedupe suffixing is where implementations diverge; 15 live anchors
   are at stake. Now a verification step (§6.9).

---

## 10. Verification gates

No completion claim without these passing.

**Gate 0 — freeze the baseline first.** Before any Docusaurus dependency is removed,
build the current site and commit `migration/baseline-urls.txt` (its sitemap URL list)
plus the `<head>` of three representative pages. **[audit]** measured today's build:
113 sitemap URLs, exactly one trailing slash (the root), 13 meta-refresh pages under
`build/ops/**`, zero `/ops/` sitemap entries, no robots.txt, no CNAME. **After the
toolchain is deleted this is unregenerable**, and gate 3 depends on it.

1. **Build clean.** `npm run build` with zero warnings; `astro check` clean.
2. **Link validation.** `starlight-links-validator` fails the build on any broken
   internal link or anchor. **[probe]** confirmed it flags relative links, `.md` links
   and trailing-slash mismatches as hard errors. Strictly stronger than today:
   `onBrokenLinks: 'warn'` hides breakage and the `remarkConfig` was never wired into
   the build at all.
3. **Route parity.** Diff the new `dist/` routes against gate 0's baseline. Required:
   all 72 work/develop routes present (modulo §7.2's trailing slash), all 14 redirect
   stubs present (13 `/ops/*` + `/search`), and the only deletions being the legacy
   tree, the screenshots, and `/opensearch.xml` (§7.7).
4. **Content assertions**, scripted over `src/content/docs/`, all fence-aware:
   - zero body-level `# ` headings outside code fences
   - **22 in-fence `# ` comments still present** (guards against a naive strip)
   - zero `^\s*>?\s*:::(info|warning)\b`
   - zero `^\s*>?\s*:::[a-z]+[ ]+\S` (space-separated aside titles)
   - zero `>\s*:::` (blockquote-wrapped asides)
   - zero `</content>` / `</invoke>` / `<invoke`
   - zero `](….md)` link targets
   - zero `sidebar_position:` keys
   - every file has a frontmatter `title:`
   - no duplicate `slug` values (**[probe]**: duplicates only warn, then overwrite)
5. **Anchor parity.** Diff emitted heading IDs for `develop/use-cases.md` and
   `work/use-cases.md` against the baseline (§6.9).
6. **Rendered spot-check with brand sign-off.** The splash page; one page per sidebar
   group; `compute.md` + `connect-compute.md` (most admonitions);
   `self-registration.md` (the info/warning/tip cluster); the four de-quoted
   blockquote asides; and the six files containing box-drawing ASCII art
   (`develop/intro.md`, `develop/features/mcp-and-vault.md`,
   `develop/features/knowledge-bases.md`, `work/library/knowledge-bases.md`,
   `develop/loop/overview.md`, `develop/loop/build.md`) — Astro 7 changes default
   HTML whitespace handling, and `<pre>` blocks are the risk class. Confirm exactly
   one `<h1>` per page, all asides styled, and get explicit sign-off on the
   default-Starlight look (§7.5).
7. **Live post-deploy checks.** `/work/tools/chat` → 301 → `/work/tools/chat/` → 200;
   `/ops/features/agents` → the new develop page; `/search` → `/`.

---

## 11. Toolchain and CI

`package.json`: `dev` / `build` / `preview`, with `start` aliased to `dev` so muscle
memory survives.

**[probe]** `astro@7.1.6` declares `"engines": { "node": ">=22.12.0", "npm": ">=9.6.5" }`;
`@astrojs/starlight@0.41.5` declares no `engines` and peers `astro ^7.0.2`. The current
workflow pins **Node 20**, which cannot build Astro 7.

`.github/workflows/deploy-docs.yml` keeps its `push: main` trigger, `pages`
permissions, `concurrency: { group: pages, cancel-in-progress: false }` and
`github-pages` environment. Only the build job changes:

```yaml
- uses: actions/checkout@v4
- uses: withastro/action@v6      # replaces setup-node + npm ci + npm run build
                                 # + actions/upload-pages-artifact
```

Deploy job → `actions/deploy-pages@v5`. `starlight-links-validator` runs inside the
build, so broken links block deployment.

Note: git history contains a commit disabling the auto-trigger for runner
availability. Confirm the workflow is currently enabled before relying on it.

---

## 12. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| A naive H1 strip deletes 22 code-fence comments | **High** | Fence-aware script (§6.1); gate 4 asserts all 22 survive |
| A missed `.md` link ships as a 404 | **High** | Gate 2 makes it a build failure; gate 4 asserts zero remain |
| A blockquote-wrapped aside is rewritten without de-quoting | Medium | Hand-edited (§6.4); gate 4 asserts zero `>\s*:::`; gate 6 renders all four |
| Duplicate heading anchors change, breaking 15 deep links | Medium | Gate 5 diffs against baseline; rename headings if divergent (§6.9) |
| Site looks like default Starlight; readers notice | Medium | Explicit sign-off, gate 6 (§7.5) |
| Publishing `experts-arenas.md` exposes never-public content | Medium | Explicit sign-off (§15); default is to leave it draft |
| Canonical URLs gain a trailing slash | Medium | Host 301s the old form — **[live]** verified. Resubmit sitemap post-deploy |
| Baseline lost before gate 3 can run | Medium | Gate 0 freezes it as commit 1 |
| `/search` 404s for indexed visitors | Low | Redirect (§7.3) |
| Astro 7 whitespace handling mangles ASCII art | Low | Gate 6 covers all six affected files |
| Pagefind ranks worse than Algolia | Low | Accepted; reinstatable without content changes |
| 42 screenshot + ~46 legacy URLs 404 | Low | Accepted decision (§3) |
| `HeaderLogin.astro` breaks on upgrade | Low | ~20 lines against a documented, stable API |

---

## 13. Housekeeping

The branch carries two pre-existing uncommitted changes from `main`. **The working
tree must be clean before any codemod runs** — a migration starting with
`git checkout .` silently resurrects them; one starting with `git add -A` silently
commits them.

- `D OPEN_QUESTIONS.md` — a 40-line editorial backlog (17 verification items, "App
  snapshot: surogate-ops-main (downloaded 2026-05-10)"), deleted but never committed.
  It lives at repo root, not in `docs/`, so it is not part of the published site.
  **Decision needed:** commit the deletion or `git restore` it.
- `M src/pages/index.jsx` — a two-line copy tweak to the trainer-docs footnote. Moot:
  the file is deleted and the footnote removed with the legacy tree.

---

## 14. Decisions of record

| # | Decision | Choice |
|---|---|---|
| 1 | Fidelity | Port + simplify structure |
| 2 | Legacy trainer tree | Archived — deleted from the new site |
| 3 | Archived-page URLs | Deleted, no redirects |
| 4 | Navigation model | One sidebar, two top-level groups; pill toggle deleted |
| 5 | Homepage | Starlight splash template |
| 6 | Search | Pagefind |
| 7 | Title/H1 conflicts | Richer H1 → `title`, short text → `sidebar.label` |
| 8 | Screenshots | Dropped; recoverable from git |
| 9 | Repo mechanics | One branch, full replacement |
| 10 | Orphan pages | Both added to the Develop sidebar (§6.8 needs sign-off) |
| 11 | Header links | Login in header; About dropped |
| 12 | URL form | Trailing slash accepted; old form 301s |

---

## 15. Open items for spec review

1. **§6.8** — publishing `develop/features/experts-arenas.md` removes its
   `draft: true` flag, making it public for the first time. Confirm or withhold.
2. **§6.3** — `skills-and-experts.md` is two documents in one file. Demoting the
   second H1 to `##` is the in-scope fix; splitting it into `skills.md` +
   `experts.md` is the clean one. Confirm the demotion, or approve the split.
3. **§7.5** — the site will look like default Starlight. Confirm that is acceptable,
   or budget a brand pass.
4. **§7.4** — the header word changes from "Documentation" to "Surogate", and the
   "AgentOps Factory" tagline has no home in Starlight. Confirm.
5. **§7.7** — `/opensearch.xml` is dropped (address-bar site-search stops working).
   Confirm.
6. **§7.6** — add `starlight-llms-txt` for an AI-crawler surface? Optional, ~1 hour.
7. **§8** — a new favicon and OG card will be generated from the existing logos.
   Confirm nothing should come from design instead.
8. **§13** — commit the `OPEN_QUESTIONS.md` deletion, or restore the file?

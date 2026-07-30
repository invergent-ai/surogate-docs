# Docusaurus → Astro Starlight Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Docusaurus 3.9 with Astro Starlight in `/work/surogate-docs`, migrating the 72 operator/builder pages, archiving the legacy trainer tree, and keeping every live URL reachable.

**Architecture:** One branch, full replacement. The Docusaurus toolchain is deleted and Starlight scaffolded in its place, then content moves from `docs/` to `src/content/docs/` through a tested, fence-aware Python codemod. Hand edits follow for the cases that cannot be safely scripted (asides, structural headings). Verification is by build gates — a link validator that fails the build, scripted content assertions, and a route-parity diff against a baseline frozen before the old toolchain is removed.

**Tech Stack:** Astro 7.1.6, `@astrojs/starlight` 0.41.5, `starlight-links-validator`, Pagefind (bundled), `@fontsource/inter`, Python 3 stdlib (codemod + tests), GitHub Actions + `withastro/action@v6`.

**Spec:** [`specs/2026-07-30-docusaurus-to-starlight-design.md`](./2026-07-30-docusaurus-to-starlight-design.md). Section references below (§N) point into it.

## Global Constraints

Every task's requirements implicitly include this section.

- **Branch:** `feat/starlight-migration`. Already created. Never commit to `main`.
- **Commits:** Conventional Commits (`type(scope): subject`). **No `Co-Authored-By` trailer.**
- **Node:** `>=22.12.0`, npm `>=9.6.5` — required by `astro@7.1.6`. CI currently pins Node 20 and must change.
- **Pinned versions:** `astro@7.1.6`, `@astrojs/starlight@0.41.5`.
- **Never set `trailingSlash` or `build.format`.** Astro's defaults are load-bearing (§7.2). Setting `format: 'file'` bakes `.html` into every href, canonical, `og:url` and Pagefind result.
- **Starlight supports exactly four aside types:** `note`, `tip`, `caution`, `danger`. `:::info` and `:::warning` render as bare unstyled `<div>`s with no error.
- **Aside titles use bracket syntax only:** `:::note[Title]`. The space form `:::note Title` silently deletes the title text.
- **All internal doc links:** root-absolute, extensionless, **with** trailing slash — `/work/tools/chat/`. Relative links and `.md` extensions are build failures once the link validator is installed.
- **Never modify lines inside fenced code blocks.** 22 `# ` lines in the corpus are shell/Python comments. Every transform is fence-aware.
- **Scope:** only `docs/work/` (40 files) and `docs/develop/` (32 files). The legacy trainer tree and all 42 screenshots are deleted.
- **Working tree must be clean before Task 3's codemod runs** (Task 1 handles this).

---

## File Structure

| Path | Responsibility |
|---|---|
| `migration/baseline-urls.txt` | Frozen pre-cutover sitemap URL list. Route-parity fixture. |
| `migration/baseline-anchors.txt` | Frozen heading IDs for the two duplicate-slug pages. |
| `migration/codemod.py` | One-shot fence-aware content transform. Python 3 stdlib only. |
| `migration/test_codemod.py` | `unittest` suite for the codemod. Guards the fence-awareness invariant. |
| `migration/assert_content.py` | Post-transform content assertions (§10 gate 4). Runs in CI. |
| `astro.config.mjs` | Site config, sidebar, redirects, head, integrations. |
| `src/content.config.ts` | Starlight content collection (`docsLoader` + `docsSchema`). |
| `tsconfig.json` | Required by `astro check`. None exists today. |
| `src/content/docs/index.mdx` | Splash homepage. |
| `src/content/docs/work/**`, `src/content/docs/develop/**` | The 72 migrated pages. |
| `src/styles/custom.css` | Brand accent tokens only. |
| `src/components/HeaderLogin.astro` | `SocialIcons` override adding the Login CTA. |
| `src/assets/logo-{black,white}.svg` | Header logo, light/dark. |
| `public/{CNAME,favicon.svg,og-card.png,robots.txt}` | Host + SEO static assets. |
| `.github/workflows/deploy-docs.yml` | Build/deploy pipeline. |

---

## Task 1: Freeze the baseline and clean the working tree

The Docusaurus toolchain still exists only during this task. Once Task 2 removes it, the baseline is unregenerable — and Task 14's route-parity gate depends on it.

**Files:**
- Create: `migration/baseline-urls.txt`
- Create: `migration/baseline-anchors.txt`
- Delete: `OPEN_QUESTIONS.md` (commit the existing uncommitted deletion, §13)
- Restore: `src/pages/index.jsx` (discard the uncommitted 2-line edit — the file is deleted in Task 2 anyway)

**Interfaces:**
- Produces: `migration/baseline-urls.txt` — one URL per line, sorted. `migration/baseline-anchors.txt` — lines of `path<TAB>heading-id`.

- [ ] **Step 1: Confirm the starting state**

```bash
cd /work/surogate-docs
git branch --show-current   # must print: feat/starlight-migration
git status --short           # expect exactly: " D OPEN_QUESTIONS.md" and " M src/pages/index.jsx"
```

- [ ] **Step 2: Build the current Docusaurus site**

```bash
npm ci
npm run build
```

Expected: `build/` directory created. Warnings about broken links are expected and fine (`onBrokenLinks: 'warn'`).

- [ ] **Step 3: Freeze the sitemap URL list**

```bash
mkdir -p migration
grep -oE '<loc>[^<]+</loc>' build/sitemap.xml \
  | sed 's|<loc>||; s|</loc>||' \
  | sort > migration/baseline-urls.txt
wc -l < migration/baseline-urls.txt
```

Expected: **113** lines. If the count differs, stop and investigate before proceeding — the spec's measurements were taken against 113.

- [ ] **Step 4: Freeze the heading anchors for the two duplicate-slug pages**

These are the pages whose anchors may not survive Astro's heading-ID generation (§6.9). `develop/use-cases.md` has `steps` ×7; `work/use-cases.md` has `steps` ×4 and `follow-up` ×4.

```bash
python3 - <<'PY' > migration/baseline-anchors.txt
import re, pathlib
for rel in ['develop/use-cases', 'work/use-cases']:
    html = pathlib.Path(f'build/{rel}/index.html').read_text()
    for hid in re.findall(r'<h[23][^>]*\bid="([^"]+)"', html):
        print(f'{rel}\t{hid}')
PY
grep -c 'steps' migration/baseline-anchors.txt
```

Expected: at least 11 lines containing `steps` (7 from develop + 4 from work). Inspect the file and confirm you can see the dedupe suffix pattern (`steps`, `steps-1`, `steps-2`, …).

- [ ] **Step 5: Verify the redirect stub count matches the spec**

```bash
find build/ops -name index.html | wc -l
```

Expected: **13**. This is the number of `/ops/*` redirects Task 11 must reproduce.

- [ ] **Step 6: Clean the working tree**

```bash
git restore src/pages/index.jsx     # discard the copy tweak; file dies in Task 2
git add -A migration OPEN_QUESTIONS.md
git status --short                   # expect only staged additions + the OPEN_QUESTIONS deletion
```

- [ ] **Step 7: Commit**

```bash
git commit -m "chore(migration): freeze pre-cutover URL and anchor baseline

Captures build/sitemap.xml (113 URLs) and the heading IDs of the two pages
with duplicate heading slugs, before the Docusaurus toolchain is removed and
they become unregenerable. Route parity and anchor parity gate on these.

Also commits the pending OPEN_QUESTIONS.md deletion: a stale editorial
backlog (app snapshot 2026-05-10) that lives at repo root and was never part
of the published site."
```

---

## Task 2: Scaffold Starlight and delete the Docusaurus toolchain

One coherent cutover. Ends with a green Starlight build serving three placeholder pages. Content still sits untouched in `docs/work/` and `docs/develop/` — Task 4 moves it.

**Files:**
- Create: `astro.config.mjs`, `src/content.config.ts`, `tsconfig.json`
- Modify: `package.json` (full replacement), `.gitignore`
- Create: `src/content/docs/{index,work-placeholder,develop-placeholder}.md`
- Delete: `docusaurus.config.js`, `sidebars.js`, `src/pages/`, `src/css/`, `src/theme/`, `src/components/`, `static/`, and the legacy doc tree

**Interfaces:**
- Produces: a working `npm run build` / `npm run dev` / `npm run preview`; `src/content/docs/` as the content root.

- [ ] **Step 1: Delete every Docusaurus artifact and the out-of-scope content**

```bash
cd /work/surogate-docs
git rm -r -q docusaurus.config.js sidebars.js src/pages src/css src/theme src/components static
git rm -r -q docs/index.mdx docs/about docs/getting-started docs/guides \
             docs/examples docs/reference docs/appendix
rm -rf node_modules package-lock.json build .docusaurus
ls docs/                     # expect exactly: develop  work
find docs -type f | wc -l    # expect 72
```

- [ ] **Step 2: Write the new `package.json`**

```json
{
  "name": "surogate-docs",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "engines": { "node": ">=22.12.0" },
  "scripts": {
    "dev": "astro dev --host 0.0.0.0",
    "start": "astro dev --host 0.0.0.0",
    "build": "astro build",
    "preview": "astro preview",
    "check": "astro check",
    "assert": "python3 migration/assert_content.py"
  },
  "dependencies": {
    "@astrojs/starlight": "0.41.5",
    "@fontsource/inter": "^5.2.5",
    "astro": "7.1.6",
    "starlight-links-validator": "^0.25.2"
  },
  "devDependencies": {
    "typescript": "^5.7.0"
  }
}
```

- [ ] **Step 3: Write `tsconfig.json`**

None exists today, so `astro check` could never have run.

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist", "migration"]
}
```

- [ ] **Step 4: Write `src/content.config.ts`**

```ts
import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
};
```

- [ ] **Step 5: Write a minimal `astro.config.mjs`**

Deliberately minimal — sidebar, redirects, head and styling arrive in Tasks 7–11. Note the absence of `trailingSlash` and `build.format`; that is intentional and permanent.

```js
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://docs.surogate.ai',
  integrations: [
    starlight({
      title: 'Surogate',
      description: 'Documentation for Surogate Ops — operator and builder tracks.',
      sidebar: [
        { label: 'Work — for operators', items: ['work-placeholder'] },
        { label: 'Develop — for builders', items: ['develop-placeholder'] },
      ],
    }),
  ],
});
```

- [ ] **Step 6: Create three placeholder pages**

`src/content/docs/index.md`:

```markdown
---
title: Surogate documentation
description: Placeholder — replaced by the splash homepage in a later task.
---

Scaffold placeholder.
```

`src/content/docs/work-placeholder.md`:

```markdown
---
title: Work placeholder
---

Scaffold placeholder.
```

`src/content/docs/develop-placeholder.md`:

```markdown
---
title: Develop placeholder
---

Scaffold placeholder.
```

- [ ] **Step 7: Update `.gitignore`**

It currently lists only `.docusaurus/**`, `build/**`, `node_modules/**`. Replace with:

```
node_modules/
dist/
.astro/
.DS_Store
```

- [ ] **Step 8: Install and verify the build is green**

```bash
npm install
npm run build
```

Expected: build succeeds. `dist/index.html`, `dist/work-placeholder/index.html`, `dist/develop-placeholder/index.html` exist. Zero warnings other than the informational `Entry docs → 404 was not found.` line, which Starlight prints on every build when no user-supplied `404` page exists.

- [ ] **Step 9: Verify `astro check` passes**

```bash
npm run check
```

Expected: `0 errors, 0 warnings`.

- [ ] **Step 10: Confirm the URL shape is directory-format with trailing slash**

```bash
test -f dist/work-placeholder/index.html && echo "directory format OK"
grep -o 'href="/work-placeholder[^"]*"' dist/index.html | head -1
```

Expected: `directory format OK`, and the href ends with a trailing slash. If you see `.html` anywhere, `build.format` has been set — remove it.

- [ ] **Step 11: Commit**

```bash
git add -A
git commit -m "feat(build): replace Docusaurus with Astro Starlight scaffold

Deletes the Docusaurus config, sidebars, swizzled theme overrides, custom
React components, static assets, and the legacy trainer doc tree. Adds an
Astro 7 + Starlight 0.41.5 scaffold building green on three placeholders.

Dependencies drop 27 -> 5. Adds the tsconfig.json that never existed, so
astro check can run. trailingSlash and build.format are deliberately unset:
Astro's defaults are the only combination whose hrefs, canonical tags,
sitemap and Pagefind results agree on this host."
```

---

## Task 3: Build and test the content codemod

This is the only real code in the migration, and its riskiest invariant is fence-awareness: 22 `# ` lines in the corpus are shell/Python comments that a naive strip would destroy. Test first.

**Files:**
- Create: `migration/codemod.py`
- Test: `migration/test_codemod.py`

**Interfaces:**
- Produces:
  - `fence_states(lines: list[str]) -> list[bool]` — True where a line is inside or is a fence delimiter.
  - `strip_leading_h1(body: str) -> tuple[str, str | None]` — returns `(new_body, removed_h1_text)`.
  - `drop_frontmatter_key(fm: str, key: str) -> str`
  - `rewrite_links(body: str, src_slug: str) -> tuple[str, int]` — returns `(new_body, rewrite_count)`.
  - `SLUG_OVERRIDES: dict[str, str]` — `{'work/intro': 'work', 'develop/intro': 'develop'}`.

- [ ] **Step 1: Write the failing test suite**

`migration/test_codemod.py`:

```python
import unittest
from codemod import (
    fence_states, strip_leading_h1, drop_frontmatter_key,
    rewrite_links, SLUG_OVERRIDES,
)


class TestFenceStates(unittest.TestCase):
    def test_marks_lines_inside_backtick_fence(self):
        lines = ['text', '```bash', '# a comment', '```', 'more']
        self.assertEqual(fence_states(lines), [False, True, True, True, False])

    def test_handles_tilde_fence(self):
        lines = ['~~~', '# inside', '~~~', '# outside']
        self.assertEqual(fence_states(lines), [True, True, True, False])

    def test_longer_closer_required_for_longer_opener(self):
        # A 3-backtick line does not close a 4-backtick fence.
        lines = ['````', '```', '# still inside', '````', 'out']
        self.assertEqual(fence_states(lines), [True, True, True, True, False])

    def test_language_tag_does_not_close_fence(self):
        lines = ['```python', '# comment', '```']
        self.assertEqual(fence_states(lines), [True, True, True])


class TestStripLeadingH1(unittest.TestCase):
    def test_removes_first_h1_and_reports_text(self):
        body = '\n# Slack channel\n\nSome prose.\n'
        new, removed = strip_leading_h1(body)
        self.assertEqual(removed, 'Slack channel')
        self.assertNotIn('# Slack channel', new)
        self.assertIn('Some prose.', new)

    def test_preserves_hash_comments_inside_code_fences(self):
        body = (
            '\n# Observe phase\n\n'
            '```bash\n'
            '# List sessions matching filters\n'
            'curl /api/sessions\n'
            '```\n'
        )
        new, removed = strip_leading_h1(body)
        self.assertEqual(removed, 'Observe phase')
        self.assertIn('# List sessions matching filters', new)

    def test_does_not_touch_a_second_h1(self):
        # skills-and-experts.md has two real H1s; only the first is the
        # title duplicate. The second is demoted by hand, not here.
        body = '\n# Skills & Tools\n\nprose\n\n# Experts\n\nmore\n'
        new, removed = strip_leading_h1(body)
        self.assertEqual(removed, 'Skills & Tools')
        self.assertIn('# Experts', new)

    def test_returns_none_when_no_h1(self):
        body = '\n## Only a subheading\n'
        new, removed = strip_leading_h1(body)
        self.assertIsNone(removed)
        self.assertEqual(new, body)


class TestDropFrontmatterKey(unittest.TestCase):
    def test_removes_the_key_line(self):
        fm = 'title: Slack\nsidebar_position: 2\n'
        self.assertEqual(drop_frontmatter_key(fm, 'sidebar_position'), 'title: Slack')

    def test_leaves_other_keys_untouched(self):
        fm = 'title: Slack\ndraft: true\n'
        self.assertEqual(drop_frontmatter_key(fm, 'sidebar_position'), fm.rstrip('\n'))


class TestRewriteLinks(unittest.TestCase):
    def test_sibling_link(self):
        out, n = rewrite_links('See [chat](./chat.md).', 'work/tools/commands')
        self.assertEqual(out, 'See [chat](/work/tools/chat/).')
        self.assertEqual(n, 1)

    def test_parent_relative_link(self):
        out, n = rewrite_links('[skills](../library/skills.md)', 'work/tools/chat')
        self.assertEqual(out, '[skills](/work/library/skills/)')

    def test_cross_tree_link(self):
        out, n = rewrite_links('[agents](../../develop/features/agents.md)',
                               'work/tools/chat')
        self.assertEqual(out, '[agents](/develop/features/agents/)')

    def test_preserves_anchor(self):
        out, n = rewrite_links('[x](./chat.md#history)', 'work/tools/commands')
        self.assertEqual(out, '[x](/work/tools/chat/#history)')

    def test_applies_slug_override(self):
        out, n = rewrite_links('[home](../intro.md)', 'work/tools/chat')
        self.assertEqual(out, '[home](/work/)')

    def test_leaves_external_links_alone(self):
        src = '[x](https://example.com/a.md)'
        out, n = rewrite_links(src, 'work/intro')
        self.assertEqual(out, src)
        self.assertEqual(n, 0)

    def test_leaves_anchor_only_links_alone(self):
        src = '[x](#section)'
        out, n = rewrite_links(src, 'work/intro')
        self.assertEqual(out, src)
        self.assertEqual(n, 0)

    def test_leaves_root_absolute_links_alone(self):
        src = '[x](/develop/features/mcp-and-vault)'
        out, n = rewrite_links(src, 'work/library/mcp-servers')
        self.assertEqual(out, src)
        self.assertEqual(n, 0)

    def test_does_not_rewrite_inside_code_fence(self):
        body = '```markdown\n[x](./chat.md)\n```\n'
        out, n = rewrite_links(body, 'work/tools/commands')
        self.assertEqual(out, body)
        self.assertEqual(n, 0)


class TestSlugOverrides(unittest.TestCase):
    def test_exactly_two_overrides(self):
        self.assertEqual(SLUG_OVERRIDES,
                         {'work/intro': 'work', 'develop/intro': 'develop'})


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd /work/surogate-docs/migration && python3 -m unittest test_codemod -v
```

Expected: `ModuleNotFoundError: No module named 'codemod'`.

- [ ] **Step 3: Write the codemod**

`migration/codemod.py`:

```python
#!/usr/bin/env python3
"""One-shot codemod: Docusaurus docs/ -> Starlight src/content/docs/.

Python 3 stdlib only. Every transform is fence-aware: 22 '# ' lines in this
corpus are shell/Python comments inside code fences, and destroying them
would silently corrupt ~20 code examples.
"""
from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path

# The only two pages whose URL is not their file path.
SLUG_OVERRIDES = {'work/intro': 'work', 'develop/intro': 'develop'}

_FENCE = re.compile(r'(`{3,}|~{3,})')
_H1 = re.compile(r'^#\s+(.+?)\s*$')
_LINK = re.compile(r'\]\(([^)\s]+)\)')
_FRONTMATTER = re.compile(r'\A---\n(.*?)\n---\n', re.S)


def fence_states(lines: list[str]) -> list[bool]:
    """True for every line inside a fenced code block, including delimiters.

    A closing fence must use the same character as the opener, be at least as
    long, and carry nothing after it. This is what stops ```python from
    closing a ``` fence.
    """
    states: list[bool] = []
    opener: tuple[str, int] | None = None
    for line in lines:
        stripped = line.lstrip()
        m = _FENCE.match(stripped)
        if opener is None:
            if m:
                opener = (m.group(1)[0], len(m.group(1)))
                states.append(True)
            else:
                states.append(False)
            continue
        states.append(True)
        if (m and m.group(1)[0] == opener[0]
                and len(m.group(1)) >= opener[1]
                and not stripped[len(m.group(1)):].strip()):
            opener = None
    return states


def strip_leading_h1(body: str) -> tuple[str, str | None]:
    """Remove the first out-of-fence '# ' heading. Starlight renders the
    frontmatter title as the page <h1>, so a body H1 is a duplicate.

    Only the FIRST is removed. skills-and-experts.md has a legitimate second
    H1 that is demoted by hand.
    """
    lines = body.split('\n')
    for i, (line, in_fence) in enumerate(zip(lines, fence_states(lines))):
        if in_fence:
            continue
        m = _H1.match(line)
        if m:
            del lines[i]
            # Collapse the blank line the heading left behind.
            if i < len(lines) and not lines[i].strip():
                del lines[i]
            return '\n'.join(lines), m.group(1)
    return body, None


def drop_frontmatter_key(fm: str, key: str) -> str:
    kept = [l for l in fm.split('\n') if not re.match(rf'^{re.escape(key)}\s*:', l)]
    return '\n'.join(kept).rstrip('\n')


def _resolve(target: str, src_slug: str) -> str | None:
    """Map a relative .md link to a root-absolute trailing-slash URL."""
    path, _, anchor = target.partition('#')
    if not path.endswith('.md'):
        return None
    if path.startswith('/') or '://' in path:
        return None
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src_slug), path))
    resolved = resolved[:-3]  # strip .md
    slug = SLUG_OVERRIDES.get(resolved, resolved)
    suffix = f'#{anchor}' if anchor else ''
    return f'/{slug}/{suffix}'


def rewrite_links(body: str, src_slug: str) -> tuple[str, int]:
    """Rewrite relative .md links to root-absolute trailing-slash URLs.

    Astro rewrites nothing and warns about nothing, so an unrewritten .md
    link ships as a 404.
    """
    count = 0
    out: list[str] = []
    lines = body.split('\n')
    for line, in_fence in zip(lines, fence_states(lines)):
        if in_fence:
            out.append(line)
            continue

        def sub(m: re.Match[str]) -> str:
            nonlocal count
            new = _resolve(m.group(1), src_slug)
            if new is None:
                return m.group(0)
            count += 1
            return f']({new})'

        out.append(_LINK.sub(sub, line))
    return '\n'.join(out), count


def transform_file(path: Path, src_slug: str) -> dict[str, object]:
    text = path.read_text(encoding='utf-8')
    m = _FRONTMATTER.match(text)
    if not m:
        raise SystemExit(f'{path}: no frontmatter')
    fm, body = m.group(1), text[m.end():]

    fm = drop_frontmatter_key(fm, 'sidebar_position')
    body, removed_h1 = strip_leading_h1(body)
    body, n_links = rewrite_links(body, src_slug)

    path.write_text(f'---\n{fm}\n---\n{body}', encoding='utf-8')
    return {'slug': src_slug, 'h1': removed_h1, 'links': n_links}


def main(root: str) -> None:
    base = Path(root)
    total_links = 0
    rows = []
    for path in sorted(base.rglob('*.md')):
        slug = path.relative_to(base).with_suffix('').as_posix()
        info = transform_file(path, slug)
        total_links += int(info['links'])
        rows.append(info)
    print(f'files: {len(rows)}')
    print(f'h1 removed: {sum(1 for r in rows if r["h1"])}')
    print(f'links rewritten: {total_links}')
    for r in rows:
        print(f'  {r["slug"]}\th1={r["h1"]!r}\tlinks={r["links"]}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'src/content/docs')
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd /work/surogate-docs/migration && python3 -m unittest test_codemod -v
```

Expected: all tests pass, `OK`.

- [ ] **Step 5: Commit**

```bash
cd /work/surogate-docs
git add migration/codemod.py migration/test_codemod.py
git commit -m "feat(migration): add fence-aware content codemod with tests

Strips the duplicate body H1, drops sidebar_position, and rewrites relative
.md links to root-absolute trailing-slash URLs.

Fence-awareness is the load-bearing invariant and is tested directly: 22 '# '
lines in the corpus are shell comments inside code fences, and a naive strip
would corrupt ~20 code examples. The closing-fence rule (same char, >= length,
nothing trailing) is what stops a language-tagged opener from self-closing."
```

---

## Task 4: Move the content and run the codemod

**Files:**
- Move: `docs/work/` → `src/content/docs/work/`, `docs/develop/` → `src/content/docs/develop/`
- Delete: `src/content/docs/{work-placeholder,develop-placeholder}.md`
- Modify: all 72 content files (via codemod)
- Modify: `astro.config.mjs` (placeholder sidebar → autogenerate, temporarily)

- [ ] **Step 1: Move the two trees with git**

```bash
cd /work/surogate-docs
git mv docs/work src/content/docs/work
git mv docs/develop src/content/docs/develop
git rm -q src/content/docs/work-placeholder.md src/content/docs/develop-placeholder.md
rmdir docs
find src/content/docs -name '*.md' | wc -l   # expect 72
```

- [ ] **Step 2: Record the pre-transform invariant counts**

These are the numbers the codemod must move. Capture them before it runs.

```bash
cd /work/surogate-docs/src/content/docs
python3 - <<'PY'
import re, glob, sys
sys.path.insert(0, '../../../migration')
from codemod import fence_states
files = sorted(glob.glob('**/*.md', recursive=True))
in_fence_hashes = 0
for p in files:
    lines = open(p).read().split('\n')
    in_fence_hashes += sum(1 for l, f in zip(lines, fence_states(lines))
                           if f and l.startswith('# '))
print('files:', len(files))
print('in-fence "# " comments (MUST survive):', in_fence_hashes)
print('.md links:', sum(len(re.findall(r'\]\([^)]*\.md[^)]*\)', open(p).read())) for p in files))
PY
```

Expected: `files: 72`, `in-fence "# " comments (MUST survive): 22`, `.md links: 240`.

- [ ] **Step 3: Run the codemod**

```bash
cd /work/surogate-docs
python3 migration/codemod.py src/content/docs | tee /tmp/codemod-report.txt
tail -3 /tmp/codemod-report.txt
grep -E '^(files|h1 removed|links rewritten):' /tmp/codemod-report.txt
```

Expected: `files: 72`, `h1 removed: 72`, `links rewritten: 240`.

- [ ] **Step 4: Verify the fence invariant held**

This is the check that catches the failure mode the whole codemod was designed around.

```bash
cd /work/surogate-docs/src/content/docs
python3 - <<'PY'
import glob, sys
sys.path.insert(0, '../../../migration')
from codemod import fence_states
n = 0
for p in sorted(glob.glob('**/*.md', recursive=True)):
    lines = open(p).read().split('\n')
    n += sum(1 for l, f in zip(lines, fence_states(lines)) if f and l.startswith('# '))
print('in-fence "# " comments surviving:', n)
assert n == 22, f'FENCE INVARIANT BROKEN: expected 22, got {n}'
print('OK')
PY
```

Expected: `in-fence "# " comments surviving: 22` then `OK`. **If this fails, revert and fix the codemod — do not proceed.**

- [ ] **Step 5: Verify no out-of-fence H1s and no `.md` links remain**

```bash
cd /work/surogate-docs/src/content/docs
python3 - <<'PY'
import glob, re, sys
sys.path.insert(0, '../../../migration')
from codemod import fence_states
h1 = []; mdlinks = []
for p in sorted(glob.glob('**/*.md', recursive=True)):
    body = open(p).read()
    lines = body.split('\n')
    for i, (l, f) in enumerate(zip(lines, fence_states(lines)), 1):
        if not f and re.match(r'^#\s+\S', l):
            h1.append(f'{p}:{i}')
        if not f and re.search(r'\]\([^)]*\.md[^)]*\)', l):
            mdlinks.append(f'{p}:{i}')
print('out-of-fence H1s:', h1)
print('remaining .md links:', mdlinks)
PY
```

Expected: `out-of-fence H1s: ['develop/features/skills-and-experts.md:...']` — exactly one, the legitimate second H1 handled in Task 5. `remaining .md links: []`.

- [ ] **Step 6: Point the sidebar at autogenerated groups so the build can run**

Temporary — Task 7 replaces this with the curated sidebar. In `astro.config.mjs`, replace the `sidebar` array:

```js
      sidebar: [
        { label: 'Work — for operators',
          items: [{ autogenerate: { directory: 'work' } }] },
        { label: 'Develop — for builders',
          items: [{ autogenerate: { directory: 'develop' } }] },
      ],
```

- [ ] **Step 7: Build and confirm the routes exist**

```bash
cd /work/surogate-docs && npm run build
find dist -name index.html | wc -l
test -f dist/work/tools/chat/index.html && echo "work route OK"
test -f dist/develop/features/agents/index.html && echo "develop route OK"
```

Expected: both `OK` lines. The `slug: /work` frontmatter is still in its Docusaurus form, so `/work/` will not resolve yet — that is Task 6.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "refactor(content): move the 72 work/develop pages into src/content/docs

Runs the codemod: 72 duplicate body H1s stripped, 72 sidebar_position keys
dropped, 240 relative .md links rewritten to root-absolute trailing-slash
URLs.

Verified all 22 in-fence '# ' shell comments survived, and that the only
remaining out-of-fence H1 is the legitimate second heading in
skills-and-experts.md."
```

---

## Task 5: Hand-edit the 13 asides, 4 stray XML artifacts, and the one structural heading

Everything here is a silent-failure class: it builds clean whether or not you get it right. Scripted assertions follow in Task 12.

**Files:**
- Modify: `src/content/docs/work/channels/self-registration.md`
- Modify: `src/content/docs/develop/features/{compute,connect-compute,experts-arenas}.md`
- Modify: `src/content/docs/work/library/{knowledge-bases,mcp-servers,skills}.md`
- Modify: `src/content/docs/develop/features/skills-and-experts.md`

- [ ] **Step 1: Rewrite the 5 unsupported / space-titled plain asides**

Starlight has only `note`/`tip`/`caution`/`danger`, and titles need brackets.

| File | Find | Replace |
|---|---|---|
| `work/channels/self-registration.md` | `:::info` | `:::note` |
| `work/channels/self-registration.md` | `:::warning` | `:::caution` |
| `develop/features/compute.md` | `:::note Free plan` | `:::note[Free plan]` |
| `develop/features/compute.md` | `:::warning Billing` | `:::caution[Billing]` |
| `develop/features/experts-arenas.md` | `:::note Preview` | `:::note[Preview]` |
| `develop/features/connect-compute.md` | `:::note Preview` | `:::note[Preview]` |
| `develop/features/connect-compute.md` | `:::note Free plan` | `:::note[Free plan]` |

`develop/features/datasets.md`'s bare `:::note` and `self-registration.md`'s `:::tip` need no change.

- [ ] **Step 2: De-quote the 4 blockquote-wrapped asides**

Each has a `> ` prefix on every line. Strip the prefix *and* fix the type/title. For example, `work/library/mcp-servers.md` around line 59:

```markdown
> :::info Credentials never reach the sandbox
> The agent's sandbox is the most untrusted component in the platform. Credentials live in the Vault and are injected by the MCP proxy as it forwards each call — even a fully prompt-injected agent can't exfiltrate them.
> :::
```

becomes:

```markdown
:::note[Credentials never reach the sandbox]
The agent's sandbox is the most untrusted component in the platform. Credentials live in the Vault and are injected by the MCP proxy as it forwards each call — even a fully prompt-injected agent can't exfiltrate them.
:::
```

All four:

| File | Current opener | New opener |
|---|---|---|
| `work/library/knowledge-bases.md` | `> :::warning Curator model is locked` | `:::caution[Curator model is locked]` |
| `work/library/knowledge-bases.md` | `> :::tip Smaller is more reliable` | `:::tip[Smaller is more reliable]` |
| `work/library/mcp-servers.md` | `> :::info Credentials never reach the sandbox` | `:::note[Credentials never reach the sandbox]` |
| `work/library/skills.md` | `> :::info Templates are real, not empty` | `:::note[Templates are real, not empty]` |

- [ ] **Step 3: Delete the 4 stray tool-call XML artifacts**

These are the literal last lines of three files and ship in production today, invisible under CommonMark.

```bash
cd /work/surogate-docs/src/content/docs
for f in develop/features/compute.md work/library/mcp-servers.md work/library/skills.md; do
  python3 - "$f" <<'PY'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
t = re.sub(r'\n*(</content>|</invoke>)\s*(?=\n|\Z)', '', t).rstrip() + '\n'
p.write_text(t)
PY
done
grep -rn '</content>\|</invoke>' . ; echo "exit=$? (1 means clean)"
```

Expected: no output, `exit=1`.

- [ ] **Step 4: Demote the second H1 in `skills-and-experts.md`**

The file is two documents concatenated. Its first H1 was already stripped by the codemod. The remaining `# Experts — model-backed skills` must become `##` so it is a peer of the page's other sections and the heading order is valid.

```bash
cd /work/surogate-docs/src/content/docs
sed -i 's/^# Experts — model-backed skills$/## Experts — model-backed skills/' \
  develop/features/skills-and-experts.md
grep -n '^#\{1,2\} ' develop/features/skills-and-experts.md | head -5
```

Expected: no `^# ` lines remain; `## Experts — model-backed skills` is present.

- [ ] **Step 5: Verify every aside is now valid**

```bash
cd /work/surogate-docs/src/content/docs
echo "unsupported types (want 0):"; grep -rcE '^\s*>?\s*:::(info|warning)\b' . | grep -v ':0' | wc -l
echo "space-titled (want 0):";      grep -rnE '^\s*>?\s*:::[a-z]+[ ]+\S' . | wc -l
echo "blockquoted (want 0):";       grep -rnE '^\s*>\s*:::' . | wc -l
echo "valid asides (want 13):";     grep -rhoE '^:::(note|tip|caution|danger)' . | wc -l
```

Expected: `0`, `0`, `0`, `13`.

- [ ] **Step 6: Build and eyeball the two densest aside pages**

```bash
cd /work/surogate-docs && npm run build
grep -c 'starlight-aside' dist/develop/features/connect-compute/index.html
grep -o 'starlight-aside--[a-z]*' dist/work/channels/self-registration/index.html | sort -u
```

Expected: a nonzero aside count on `connect-compute`; `self-registration` shows `starlight-aside--note`, `--caution`, `--tip` and **no bare `<div>`** where an aside should be.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "fix(content): normalise asides, drop stray XML, fix heading order

Rewrites all 13 admonitions for Starlight, which supports only
note/tip/caution/danger and requires bracket titles. Every failure mode here
is silent: :::info and :::warning render as unstyled divs, and the
space-separated title form deletes the title text outright.

Four asides were wrapped in blockquotes and invisible to a ^::: grep; their
'> ' prefixes are stripped.

Deletes four orphaned </content> and </invoke> tool-call artifacts that have
been shipping in prose, and demotes the second H1 in skills-and-experts.md so
the page has a valid heading order."
```

---

## Task 6: Frontmatter — titles, sidebar labels, and slugs

**Files:**
- Modify: 14 files for `title`/`sidebar.label`, 2 for `slug`, 1 to drop `draft`

- [ ] **Step 1: Convert the two Docusaurus slugs**

```bash
cd /work/surogate-docs/src/content/docs
sed -i 's|^slug: /work$|slug: work|' work/intro.md
sed -i 's|^slug: /develop$|slug: develop|' develop/intro.md
grep -n '^slug:' work/intro.md develop/intro.md
```

Expected: `slug: work` and `slug: develop`.

- [ ] **Step 2: Convert the two existing `sidebar_label` keys**

`work/intro.md` and `develop/intro.md` carry `sidebar_label: Welcome`. Starlight nests this. Both files' frontmatter becomes:

```yaml
---
title: Work mode
slug: work
sidebar:
  label: Welcome
---
```

```yaml
---
title: Develop mode
slug: develop
sidebar:
  label: Welcome
---
```

- [ ] **Step 3: Apply the 12 remaining title/label pairs**

Rule: the richer H1 text (removed by the codemod) becomes `title`; the short text becomes `sidebar.label`.

| File | `title:` | `sidebar.label` |
|---|---|---|
| `work/channels/web.md` | Web channel | Web |
| `work/channels/slack.md` | Slack channel | Slack |
| `work/channels/telegram.md` | Telegram channel | Telegram |
| `work/channels/users.md` | Per-agent users | Users |
| `work/channels/self-registration.md` | Let end users sign up for your agent | Self-registration |
| `develop/loop/overview.md` | The builder loop | Overview |
| `develop/loop/build.md` | Build phase — designing the agent | Build |
| `develop/loop/observe.md` | Observe phase — what the agent actually does | Observe |
| `develop/loop/train.md` | Train phase — using observed signal | Train |
| `develop/loop/redeploy.md` | Redeploy phase — rolling out the changes | Redeploy |
| `develop/features/byo-llm.md` | BYO LLM (Bring Your Own LLM) | BYO LLM |
| `develop/features/skills-and-experts.md` | Skills & Experts *(unchanged)* | Skills & Experts |

Each gets the nested form, e.g. `work/channels/slack.md`:

```yaml
---
title: Slack channel
sidebar:
  label: Slack
---
```

- [ ] **Step 4: Add the 10 sidebar labels that used to live in `sidebars.js`**

These were `{ id, label }` overrides in the old config; a page now owns its own label.

| File | `sidebar.label` |
|---|---|
| `work/workflow/review-sessions.md` | Sessions |
| `work/library/knowledge-bases.md` | Knowledge Bases |
| `develop/tools/dashboard.md` | Dashboard |
| `develop/features/sessions.md` | Sessions |
| `develop/features/models.md` | Models |
| `develop/features/playground.md` | Playground |
| `develop/features/hub.md` | Data Hub |
| `develop/features/datasets.md` | Datasets |
| `develop/features/training.md` | Training |
| `develop/features/evaluations.md` | Evaluations |

- [ ] **Step 5: Un-draft `experts-arenas.md`**

Removing `draft: true` publishes a page that has never been publicly visible (spec §6.8, sign-off recorded). Its sidebar Preview badge is added in Task 7.

```bash
cd /work/surogate-docs/src/content/docs
sed -i '/^draft: true$/d' develop/features/experts-arenas.md
grep -c '^draft:' develop/features/experts-arenas.md   # expect 0
```

- [ ] **Step 6: Verify every file still has a title and the slugs resolve**

```bash
cd /work/surogate-docs/src/content/docs
python3 - <<'PY'
import glob, re
missing = []
for p in sorted(glob.glob('**/*.md', recursive=True)):
    m = re.match(r'\A---\n(.*?)\n---\n', open(p).read(), re.S)
    if not m or not re.search(r'^title:\s*\S', m.group(1), re.M):
        missing.append(p)
print('files missing a title:', missing)
PY
cd /work/surogate-docs && npm run build
test -f dist/work/index.html && echo "/work/ OK"
test -f dist/develop/index.html && echo "/develop/ OK"
test ! -d dist/work/intro && echo "no stray /work/intro/ OK"
```

Expected: `files missing a title: []`, then all three `OK` lines.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(content): reconcile frontmatter titles, sidebar labels, and slugs

Starlight renders the frontmatter title as the page h1, so the 14 pages whose
title and h1 disagreed now carry the richer h1 wording as the title with the
short form as sidebar.label -- no editorial wording is lost and sidebar
entries stay short.

Moves the 10 label overrides out of the deleted sidebars.js into the pages
that own them, converts the two /work and /develop slugs to Starlight's
collection-relative form, and un-drafts experts-arenas so it can be surfaced
in the sidebar."
```

---

## Task 7: The curated sidebar

**Files:**
- Modify: `astro.config.mjs`

- [ ] **Step 1: Replace the autogenerated sidebar with the curated one**

Preserves the old `sidebars.js` order and category labels. Both orphan pages are now surfaced. All inner subgroups are collapsed because the two tracks share one column.

```js
      sidebar: [
        { label: 'Work — for operators', items: [
          'work',
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
          'develop',
          'develop/quickstart',
          { label: 'The builder loop', collapsed: true, items: [
            'develop/loop/overview', 'develop/loop/build', 'develop/loop/observe',
            'develop/loop/train', 'develop/loop/redeploy',
          ]},
          'develop/tools/dashboard',
          'develop/features/agents',
          'develop/features/sessions', 'develop/features/models',
          'develop/features/playground', 'develop/features/hub',
          'develop/features/datasets', 'develop/features/training',
          'develop/features/evaluations',
          { label: 'Compute', collapsed: true, items: [
            'develop/features/compute', 'develop/features/connect-compute',
          ]},
          { label: 'Skills & knowledge', collapsed: true, items: [
            'develop/features/skills-and-experts',
            'develop/features/skill-optimization',
            'develop/features/knowledge-bases', 'develop/features/mcp-and-vault',
            'develop/features/byo-llm',
            { slug: 'develop/features/experts-arenas',
              badge: { text: 'Preview', variant: 'caution' } },
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
      ],
```

- [ ] **Step 2: Build and verify every page is reachable from the sidebar**

A `slug` that does not resolve is a build error, so a green build proves all 72 entries exist. Confirm the count and the badge:

```bash
cd /work/surogate-docs && npm run build
grep -o 'href="/work/[^"]*"' dist/work/index.html | sort -u | wc -l
grep -c 'Preview' dist/develop/features/experts-arenas/index.html
```

Expected: a nonzero Work link count, and the Preview badge present.

- [ ] **Step 3: Confirm no page is missing from the sidebar**

```bash
cd /work/surogate-docs
python3 - <<'PY'
import glob, re, pathlib
cfg = pathlib.Path('astro.config.mjs').read_text()
listed = set(re.findall(r"'((?:work|develop)(?:/[a-z0-9-]+)*)'", cfg))
listed |= set(re.findall(r"slug:\s*'([^']+)'", cfg))
on_disk = set()
for p in glob.glob('src/content/docs/**/*.md', recursive=True):
    rel = pathlib.Path(p).relative_to('src/content/docs').with_suffix('').as_posix()
    on_disk.add({'work/intro': 'work', 'develop/intro': 'develop'}.get(rel, rel))
print('on disk but not in sidebar:', sorted(on_disk - listed))
print('in sidebar but not on disk:', sorted(listed - on_disk))
PY
```

Expected: both lists empty.

- [ ] **Step 4: Commit**

```bash
git add astro.config.mjs
git commit -m "feat(nav): add the curated two-group sidebar

Replaces the three Docusaurus sidebars with one sidebar holding the Work and
Develop tracks as sibling top-level groups, preserving the previous order and
category labels. The Work/Develop pill toggle and its 60-entry path
equivalence map are gone -- the grouping replaces them.

Surfaces the two pages that were reachable only by direct URL: agents.md,
which is linked four times from prose and was simply forgotten, and
experts-arenas.md with a Preview badge.

Inner subgroups collapse by default: the two tracks now share one column."
```

---

## Task 8: Splash homepage

**Files:**
- Delete: `src/content/docs/index.md` (the scaffold placeholder)
- Create: `src/content/docs/index.mdx`

- [ ] **Step 1: Replace the placeholder with the splash page**

```bash
cd /work/surogate-docs && git rm -q src/content/docs/index.md
```

`src/content/docs/index.mdx`:

```mdx
---
title: Surogate documentation
description: Two documentation tracks for Surogate Ops — Work mode for operators, Develop mode for builders.
template: splash
hero:
  tagline: Two tracks — one for operators who run agents day-to-day, one for builders who design and train them.
  actions:
    - text: Work mode — for operators
      link: /work/
      icon: right-arrow
      variant: primary
    - text: Develop mode — for builders
      link: /develop/
      icon: right-arrow
    - text: surogate.ai
      link: https://surogate.ai
      icon: external
      variant: minimal
---

import { Card, CardGrid, LinkCard } from '@astrojs/starlight/components';

<CardGrid>
  <LinkCard
    title="Work mode"
    href="/work/"
    description="You sign in, use existing agents, watch sessions, and improve from real traffic. Plain-language workflow guides, no code, no infrastructure."
  />
  <LinkCard
    title="Develop mode"
    href="/develop/"
    description="You design agents, write skills, attach knowledge bases, train experts, run evaluations, ship to channels. Deep configuration, code snippets, runtime internals."
  />
</CardGrid>

## What is Surogate?

Surogate is a hosted platform for building, deploying, and improving autonomous AI
agents. You don't manage Kubernetes, model serving, policy enforcement, or the LLM
loop yourself — the platform handles the runtime so you focus on what the agent does.

The platform is built on three open-source components:

- **[surogates](https://github.com/invergent-ai/surogates)** — the agent runtime
  (harness, sessions, sandbox, governance, MCP integration)
- **[surogate](https://github.com/invergent-ai/surogate)** — the training framework
  (SFT/RL engine for the expert models you own)
- **[surogate-hub](https://github.com/invergent-ai/surogate-hub)** — the artifact
  versioning store

## Which mode is right for you?

| If you... | Use |
| --- | --- |
| Chat with deployed agents, configure them in a UI, review sessions | [Work mode](/work/) |
| Manage skills, knowledge bases, channels, billing for your team | [Work mode](/work/) |
| Design new agents, write skills, configure tools / governance | [Develop mode](/develop/) |
| Train experts, run evaluations, integrate via the REST API | [Develop mode](/develop/) |
| Deploy on your own cluster, customize the runtime | [Develop mode](/develop/) |
```

- [ ] **Step 2: Build and verify the splash template renders**

```bash
cd /work/surogate-docs && npm run build
grep -c 'sl-hero\|hero' dist/index.html
grep -o 'href="/work/"' dist/index.html | head -1
grep -c 'old-docs' dist/index.html ; echo "exit=$? (1 = no legacy link, good)"
```

Expected: hero markup present, the `/work/` link present, and no `old-docs` reference (the legacy footnote is gone with the tree).

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat(home): replace the React landing page with a Starlight splash

Ports the 141-line src/pages/index.jsx into a splash-template content page:
hero with Work/Develop/surogate.ai actions, a LinkCard grid for the two
tracks, and the What-is-Surogate prose, repo list and which-mode table as
plain Markdown.

This is what lets the MUI, Emotion and React dependency tree go entirely.
The About navbar link is folded into the hero actions."
```

---

## Task 9: Styling and the header Login CTA

**Files:**
- Create: `src/styles/custom.css`, `src/components/HeaderLogin.astro`
- Create: `src/assets/logo-black.svg`, `src/assets/logo-white.svg`
- Modify: `astro.config.mjs`

- [ ] **Step 1: Restore the two logos from git**

`static/` was deleted in Task 2; these are the only two assets that were ever referenced.

```bash
cd /work/surogate-docs
mkdir -p src/assets
git show HEAD~7:static/img/logo-black.svg > src/assets/logo-black.svg 2>/dev/null \
  || git show $(git log --format=%H -1 --diff-filter=D -- static/img/logo-black.svg)^:static/img/logo-black.svg > src/assets/logo-black.svg
git show $(git log --format=%H -1 --diff-filter=D -- static/img/logo-white.svg)^:static/img/logo-white.svg > src/assets/logo-white.svg
head -c 60 src/assets/logo-black.svg; echo
ls -la src/assets/
```

Expected: both files present and non-empty, starting with SVG markup.

- [ ] **Step 2: Write `src/styles/custom.css`**

98 lines become this. Everything else was Infima variables, Docusaurus-internal selectors, KaTeX, asciinema, or primeflex — none of which exist in Starlight.

```css
/* Brand accent — the only thing carried over from the Docusaurus theme.
   Light #07a000 / dark #87ed82 were the --ifm-color-primary ramps. */
:root {
  --sl-color-accent-low: #d4f5d2;
  --sl-color-accent: #07a000;
  --sl-color-accent-high: #045c00;
  --sl-font: 'Inter Variable', 'Inter', ui-sans-serif, system-ui, sans-serif;
}

:root[data-theme='dark'] {
  --sl-color-accent-low: #12401a;
  --sl-color-accent: #87ed82;
  --sl-color-accent-high: #e3fbe2;
}

/* Login CTA in the header (see HeaderLogin.astro). */
.header-login {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--sl-color-gray-5);
  border-radius: 0.375rem;
  font-size: var(--sl-text-sm);
  font-weight: 600;
  color: var(--sl-color-white);
  text-decoration: none;
  white-space: nowrap;
}

.header-login:hover {
  border-color: var(--sl-color-accent);
  color: var(--sl-color-accent);
}

@media (max-width: 50rem) {
  .header-login { display: none; }
}
```

- [ ] **Step 3: Write `src/components/HeaderLogin.astro`**

Overrides `SocialIcons` to render the Login CTA before the default icons. Starlight's override contract is to re-export the default and add around it.

```astro
---
import Default from '@astrojs/starlight/components/SocialIcons.astro';
---

<a class="header-login" href="https://ops.surogate.ai">Login</a>
<Default><slot /></Default>
```

- [ ] **Step 4: Wire logo, fonts, CSS, social and the override into `astro.config.mjs`**

Add inside the `starlight({...})` call:

```js
      logo: {
        light: './src/assets/logo-black.svg',
        dark: './src/assets/logo-white.svg',
        alt: 'Surogate',
        replacesTitle: false,
      },
      customCss: [
        '@fontsource/inter/400.css',
        '@fontsource/inter/600.css',
        './src/styles/custom.css',
      ],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/invergent-ai/surogate' },
        { icon: 'x.com', label: 'X', href: 'https://x.com/surogate_ai' },
      ],
      editLink: { baseUrl: 'https://github.com/invergent-ai/surogate-docs/edit/main/' },
      components: { SocialIcons: './src/components/HeaderLogin.astro' },
```

- [ ] **Step 5: Build and verify the header**

```bash
cd /work/surogate-docs && npm run build
grep -c 'header-login' dist/work/index.html
grep -o 'ops.surogate.ai' dist/work/index.html | head -1
grep -o 'aria-label="GitHub"\|aria-label="X"' dist/work/index.html | sort -u
grep -o 'Edit page' dist/work/index.html | head -1
grep -c 'fonts.googleapis.com' dist/work/index.html ; echo "exit=$? (1 = self-hosted fonts, good)"
```

Expected: the Login CTA present with its `ops.surogate.ai` href, both social icons, the edit link, and **no** `fonts.googleapis.com` request.

- [ ] **Step 6: Verify the accent colour applies in both themes**

```bash
grep -o '\-\-sl-color-accent: #07a000' dist/_astro/*.css | head -1
grep -o '\-\-sl-color-accent: #87ed82' dist/_astro/*.css | head -1
```

Expected: both present.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(theme): brand accent, self-hosted Inter, and a header Login CTA

Reduces 98 lines of custom.css to the brand green mapped onto Starlight
accent tokens; the rest was Infima variables, Docusaurus-internal selectors,
KaTeX and asciinema rules with no equivalent here.

Inter moves from a render-blocking Google Fonts @import to @fontsource,
removing a third-party request on every page load.

Starlight's header has no arbitrary nav-links config, so Login -- the only
one of the four old navbar items with commercial value -- gets a ~20-line
SocialIcons override. GitHub and X map onto native social icons. About is
folded into the splash hero."
```

---

## Task 10: Head, SEO, analytics, and static assets

**Files:**
- Create: `public/CNAME`, `public/robots.txt`, `public/favicon.svg`, `public/og-card.png`
- Modify: `astro.config.mjs`

- [ ] **Step 1: Create the host and crawler files**

`public/CNAME` — no such file exists today; the custom domain relies on an implicit GitHub Pages setting outside the artifact.

```bash
cd /work/surogate-docs && mkdir -p public
printf 'docs.surogate.ai\n' > public/CNAME
cat > public/robots.txt <<'EOF'
User-agent: *
Allow: /

Sitemap: https://docs.surogate.ai/sitemap-index.xml
EOF
```

- [ ] **Step 2: Create the favicon**

`img/favicon.ico` has been referenced but absent — the site has had no favicon. Derive one from the mark. `public/favicon.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#07a000"/>
  <path d="M9 22.5c1.9 1.4 4.2 2.1 6.9 2.1 4.6 0 7.4-2.2 7.4-5.5 0-3-2-4.5-6.2-5.4l-2-.4c-2-.4-2.8-1-2.8-2 0-1.2 1.2-2 3.2-2 1.9 0 3.7.5 5.3 1.6l1.9-3.2C21 6.5 18.7 5.8 16.1 5.8c-4.4 0-7.2 2.2-7.2 5.4 0 3 2 4.6 6 5.4l2 .4c2.1.4 3 1 3 2.1 0 1.3-1.3 2.1-3.5 2.1-2.2 0-4.2-.7-5.8-2z" fill="#fff"/>
</svg>
```

- [ ] **Step 3: Create the social card**

`https://docs.surogate.ai/img/social-card.jpg` is referenced by 5 meta tags and does not exist — every share preview is broken today. Generate a 1200×630 PNG:

```bash
cd /work/surogate-docs
python3 - <<'PY'
import struct, zlib
W, H = 1200, 630
bg = (13, 13, 12)
accent = (7, 160, 0)
rows = []
for y in range(H):
    px = bytearray([0])
    for x in range(W):
        # accent bar down the left edge
        px += bytes(accent if x < 16 else bg)
    rows.append(bytes(px))
raw = b''.join(rows)

def chunk(tag, data):
    return (struct.pack('>I', len(data)) + tag + data
            + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))

png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(raw, 9))
       + chunk(b'IEND', b''))
open('public/og-card.png', 'wb').write(png)
print('wrote', len(png), 'bytes')
PY
ls -la public/og-card.png
```

Expected: a 1200×630 PNG written. This is a plain branded backdrop — it replaces a 404 with something valid. Note for a follow-up: a designed card with the logo and wordmark would be better, and swapping the file needs no code change.

- [ ] **Step 4: Add favicon, head tags and gtag to `astro.config.mjs`**

Starlight emits `og:title` and `og:description` but **not** `twitter:title`/`twitter:description`, so those stay explicit.

```js
      favicon: '/favicon.svg',
      head: [
        { tag: 'script', attrs: {
            async: true,
            src: 'https://www.googletagmanager.com/gtag/js?id=G-7YRDGYZN0R',
        }},
        { tag: 'script', content:
            "window.dataLayer=window.dataLayer||[];" +
            "function gtag(){dataLayer.push(arguments);}" +
            "gtag('js',new Date());gtag('config','G-7YRDGYZN0R');" },
        { tag: 'meta', attrs: { name: 'keywords', content:
            'Surogate, AgentOps, agents, LLM, MCP, training, fine-tuning, RL, evaluations' }},
        { tag: 'meta', attrs: { property: 'og:image',
            content: 'https://docs.surogate.ai/og-card.png' }},
        { tag: 'meta', attrs: { property: 'og:image:alt', content: 'Surogate' }},
        { tag: 'meta', attrs: { property: 'og:locale', content: 'en_US' }},
        { tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' }},
        { tag: 'meta', attrs: { name: 'twitter:site', content: '@surogate_ai' }},
        { tag: 'meta', attrs: { name: 'twitter:creator', content: '@surogate_ai' }},
        { tag: 'meta', attrs: { name: 'twitter:title', content: 'Surogate Documentation' }},
        { tag: 'meta', attrs: { name: 'twitter:description', content:
            'Operator and builder documentation for Surogate Ops.' }},
        { tag: 'meta', attrs: { name: 'twitter:image',
            content: 'https://docs.surogate.ai/og-card.png' }},
      ],
```

- [ ] **Step 5: Build and verify head output and static passthrough**

```bash
cd /work/surogate-docs && npm run build
for f in CNAME robots.txt favicon.svg og-card.png; do
  test -f "dist/$f" && echo "dist/$f OK"
done
grep -o 'G-7YRDGYZN0R' dist/work/index.html | head -1
grep -o 'og-card.png' dist/work/index.html | head -1
grep -o 'twitter:title' dist/work/index.html | head -1
grep -o '<link rel="canonical" href="[^"]*"' dist/work/tools/chat/index.html
```

Expected: all four static files present; the gtag ID, OG card and twitter:title in the head; and the canonical reading `https://docs.surogate.ai/work/tools/chat/` — **with** the trailing slash.

- [ ] **Step 6: Verify the sitemap exists and agrees with the canonicals**

```bash
ls dist/sitemap*.xml
grep -o '<loc>https://docs.surogate.ai/work/tools/chat/</loc>' dist/sitemap-0.xml
```

Expected: sitemap files present and the URL trailing-slashed, matching the canonical.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(seo): add favicon, social card, robots.txt, CNAME and head tags

The Docusaurus config pointed favicon at img/favicon.ico and the og/twitter
cards at /img/social-card.jpg; neither file has ever existed, so the site has
had no favicon and broken share previews. Both are now real.

Adds the CNAME the repo never had -- the custom domain was relying on an
implicit Pages setting outside the artifact -- plus a robots.txt pointing at
the sitemap. Keeps twitter:title and twitter:description explicitly, since
Starlight's head builder emits only the og: equivalents. Carries over gtag
G-7YRDGYZN0R."
```

---

## Task 11: Redirects

**Files:**
- Modify: `astro.config.mjs`

- [ ] **Step 1: Add the 14 redirects**

13 `/ops/*` entries ported verbatim from the deleted `docusaurus.config.js`, plus `/search` — which was a real page under Algolia and is in today's sitemap, but does not exist under Pagefind's modal-only search. All destinations carry trailing slashes to avoid a redirect chain.

At the top level of `defineConfig`, beside `site`:

```js
  redirects: {
    '/ops': '/work/',
    '/ops/getting-started/quickstart': '/work/',
    '/ops/features/agents': '/develop/features/agents/',
    '/ops/features/skills': '/develop/features/skills-and-experts/',
    '/ops/features/knowledge-bases': '/develop/features/knowledge-bases/',
    '/ops/features/models': '/develop/features/models/',
    '/ops/features/datasets': '/develop/features/datasets/',
    '/ops/features/training': '/develop/features/training/',
    '/ops/features/evaluations': '/develop/features/evaluations/',
    '/ops/features/sessions': '/develop/features/sessions/',
    '/ops/features/compute': '/develop/features/compute/',
    '/ops/features/hub': '/develop/features/hub/',
    '/ops/features/templates': '/develop/tools/templates/',
    '/search': '/',
  },
```

Do **not** attempt a wildcard such as `'/ops/features/[...slug]': '/develop/features/[...slug]'`. Astro rejects prefix-rewriting wildcards with `InvalidRedirectDestination`; only `'/prefix/[...slug]': '/[...slug]'` is legal, and the parameter must literally be named `slug`.

- [ ] **Step 2: Build and verify every stub exists**

```bash
cd /work/surogate-docs && npm run build
find dist/ops -name index.html | wc -l
test -f dist/search/index.html && echo "/search stub OK"
cat dist/ops/features/agents/index.html
```

Expected: **13** stubs under `dist/ops`, the `/search` stub present, and the agents stub containing a `meta http-equiv="refresh"` pointing at `/develop/features/agents/` plus `<meta name="robots" content="noindex">`.

- [ ] **Step 3: Confirm redirect stubs stay out of the sitemap**

```bash
grep -c '/ops/' dist/sitemap-0.xml ; echo "exit=$? (1 = no /ops in sitemap, correct)"
```

Expected: no matches — redirects must not be indexed.

- [ ] **Step 4: Commit**

```bash
git add astro.config.mjs
git commit -m "feat(routing): port the 13 /ops redirects and add /search

Reproduces the @docusaurus/plugin-client-redirects behaviour as static
meta-refresh stubs, excluded from the sitemap. Destinations carry trailing
slashes so no visitor takes two hops.

/search is new: Algolia generated a real search page that sits in today's
sitemap, while Pagefind is modal-only, so the indexed URL would 404."
```

---

## Task 12: Content assertions and the link validator

The gate that makes every silent failure mode in this migration loud, permanently.

**Files:**
- Create: `migration/assert_content.py`
- Modify: `astro.config.mjs`

- [ ] **Step 1: Write the assertion script**

`migration/assert_content.py`:

```python
#!/usr/bin/env python3
"""Post-migration content assertions. Exit 1 on any violation.

Each check corresponds to a failure mode that builds clean but is wrong.
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from codemod import fence_states  # noqa: E402

ROOT = 'src/content/docs'
EXPECTED_FILES = 73          # 72 pages + index.mdx
EXPECTED_FENCE_HASHES = 22   # shell comments a naive H1 strip would destroy
EXPECTED_ASIDES = 13

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def main() -> int:
    files = sorted(glob.glob(f'{ROOT}/**/*.md', recursive=True)
                   + glob.glob(f'{ROOT}/**/*.mdx', recursive=True))
    if len(files) != EXPECTED_FILES:
        fail(f'expected {EXPECTED_FILES} content files, found {len(files)}')

    fence_hashes = 0
    asides = 0
    slugs: dict[str, str] = {}

    for p in files:
        text = Path(p).read_text(encoding='utf-8')
        m = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not m:
            fail(f'{p}: no frontmatter')
            continue
        fm, body = m.group(1), text[m.end():]

        if not re.search(r'^title:\s*\S', fm, re.M):
            fail(f'{p}: missing frontmatter title')
        if re.search(r'^sidebar_position:', fm, re.M):
            fail(f'{p}: leftover Docusaurus sidebar_position')

        sm = re.search(r'^slug:\s*(\S+)', fm, re.M)
        if sm:
            slug = sm.group(1)
            if slug.startswith('/'):
                fail(f'{p}: slug must be collection-relative, got {slug!r}')
            if slug in slugs:
                fail(f'{p}: duplicate slug {slug!r} (also {slugs[slug]}) '
                     '- Starlight only warns and silently overwrites')
            slugs[slug] = p

        lines = body.split('\n')
        for i, (line, in_fence) in enumerate(zip(lines, fence_states(lines)), 1):
            if in_fence:
                if line.startswith('# '):
                    fence_hashes += 1
                continue
            if re.match(r'^#\s+\S', line):
                fail(f'{p}:{i}: body H1 duplicates the frontmatter title')
            if re.search(r'\]\([^)]*\.md[^)]*\)', line):
                fail(f'{p}:{i}: unrewritten .md link - Astro ships this as a 404')
            if re.match(r'^\s*>\s*:::', line):
                fail(f'{p}:{i}: blockquote-wrapped aside')
            if re.match(r'^\s*:::(info|warning)\b', line):
                fail(f'{p}:{i}: unsupported aside type - renders as a bare div')
            if re.match(r'^\s*:::[a-z]+[ ]+\S', line):
                fail(f'{p}:{i}: space-separated aside title - text is discarded')
            if re.match(r'^\s*:::(note|tip|caution|danger)\b', line):
                asides += 1
            if re.search(r'</content>|</invoke>|<invoke\b', line):
                fail(f'{p}:{i}: stray tool-call XML artifact')

    if fence_hashes != EXPECTED_FENCE_HASHES:
        fail(f'in-fence "# " comments: expected {EXPECTED_FENCE_HASHES}, '
             f'found {fence_hashes} - the H1 strip was not fence-aware')
    if asides != EXPECTED_ASIDES:
        fail(f'valid asides: expected {EXPECTED_ASIDES}, found {asides}')

    if failures:
        print(f'FAIL ({len(failures)} violations)')
        for f in failures:
            print(f'  {f}')
        return 1
    print(f'OK - {len(files)} files, {fence_hashes} fence comments preserved, '
          f'{asides} asides')
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 2: Run it and confirm it passes**

```bash
cd /work/surogate-docs && python3 migration/assert_content.py
```

Expected: `OK - 73 files, 22 fence comments preserved, 13 asides`.

- [ ] **Step 3: Prove the assertions actually catch violations**

An assertion script that cannot fail is worthless. Break something, confirm the failure, restore.

```bash
cd /work/surogate-docs
cp src/content/docs/work/channels/slack.md /tmp/slack.bak
printf '\n# A duplicate title\n' >> src/content/docs/work/channels/slack.md
python3 migration/assert_content.py; echo "exit=$? (want 1)"
cp /tmp/slack.bak src/content/docs/work/channels/slack.md
python3 migration/assert_content.py; echo "exit=$? (want 0)"
```

Expected: first run exits 1 reporting the body H1; second exits 0.

- [ ] **Step 4: Install the link validator**

In `astro.config.mjs`, add the import and the plugin:

```js
import starlightLinksValidator from 'starlight-links-validator';
```

and inside `starlight({...})`:

```js
      plugins: [starlightLinksValidator()],
```

- [ ] **Step 5: Build and confirm the validator passes**

```bash
cd /work/surogate-docs && npm run build 2>&1 | tail -20
```

Expected: build succeeds with no `[starlight-links-validator]` errors. If it reports broken links or anchors, fix each one — the validator is the gate that replaces `onBrokenLinks: 'warn'`, under which breakage was invisible.

- [ ] **Step 6: Prove the validator fails on a bad link**

```bash
cd /work/surogate-docs
cp src/content/docs/work/quickstart.md /tmp/qs.bak
printf '\n[broken](/work/does-not-exist/)\n' >> src/content/docs/work/quickstart.md
npm run build 2>&1 | grep -c 'starlight-links-validator'; echo "(want >0)"
cp /tmp/qs.bak src/content/docs/work/quickstart.md
npm run build >/dev/null 2>&1 && echo "restored build OK"
```

Expected: the validator reports the broken link, then the restored build succeeds.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "test(migration): add content assertions and the link validator

Every failure mode in this migration builds clean: unrewritten .md links 404
silently, :::info degrades to a bare div, a space-separated aside title is
deleted, and a naive H1 strip eats shell comments from code fences. None of
them warn.

assert_content.py checks all of them plus duplicate slugs, which Starlight
only warns about before silently overwriting. starlight-links-validator turns
any broken internal link or anchor into a build failure, replacing
onBrokenLinks: 'warn' under which breakage was invisible.

Both are verified to actually fail when the invariant is broken."
```

---

## Task 13: Anchor parity for the duplicate-heading pages

`develop/use-cases.md` has `steps` ×7; `work/use-cases.md` has `steps` ×4 and `follow-up` ×4. Docusaurus deduped via `github-slugger`; Astro 7 generates heading IDs itself, and dedupe suffixing is exactly where implementations diverge. 15 live deep-link targets are at stake.

**Files:**
- Read: `migration/baseline-anchors.txt`
- Possibly modify: `src/content/docs/{develop,work}/use-cases.md`

- [ ] **Step 1: Diff the emitted anchors against the frozen baseline**

```bash
cd /work/surogate-docs && npm run build
python3 - <<'PY'
import re, pathlib, collections
base = collections.defaultdict(list)
for line in pathlib.Path('migration/baseline-anchors.txt').read_text().splitlines():
    rel, hid = line.split('\t')
    base[rel].append(hid)
for rel in ['develop/use-cases', 'work/use-cases']:
    html = pathlib.Path(f'dist/{rel}/index.html').read_text()
    now = re.findall(r'<h[23][^>]*\bid="([^"]+)"', html)
    old, new = base[rel], now
    print(f'\n{rel}')
    print(f'  baseline: {len(old)} anchors')
    print(f'  now     : {len(new)} anchors')
    missing = [a for a in old if a not in new]
    added = [a for a in new if a not in old]
    print(f'  MISSING from new build: {missing}')
    print(f'  new-only              : {added}')
PY
```

- [ ] **Step 2: Decide based on the diff**

- **If `MISSING` is empty** for both pages: anchors are preserved. Record that in the commit message and skip to Step 4.
- **If `MISSING` is non-empty**: the dedupe scheme differs. Proceed to Step 3 and rename the headings — do not try to force Astro's slugger to match, and do not leave the anchors broken.

- [ ] **Step 3: Only if anchors diverged — rename the ambiguous headings**

Seven identical `### Steps` headings are a genuine documentation problem, not just a slug problem: the table of contents reads "Steps" seven times with no way to tell them apart. Rename each to name its use case, which fixes the ToC and the anchors together. In `src/content/docs/develop/use-cases.md`, each `### Steps` becomes a scoped variant matching its parent `## N. <name>` section, e.g.:

```markdown
## 1. Fine-tune an expert from your traffic
### Steps — fine-tune an expert
```

Apply the same treatment to `work/use-cases.md` for its 4 `### Steps` and 4 `### Follow-up` headings. Then re-run Step 1's diff to confirm the new anchors are intentional, and check the two files for internal anchor links that pointed at the old IDs:

```bash
cd /work/surogate-docs
grep -rn '#steps\|#follow-up' src/content/docs/ || echo "no internal refs to renamed anchors"
npm run build 2>&1 | grep -c 'starlight-links-validator'; echo "(want 0)"
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "test(content): verify heading anchor parity for the use-cases pages

Both pages reuse headings (steps x7 in develop, steps x4 + follow-up x4 in
work), so their anchors depend on the dedupe suffixing scheme. Docusaurus
used github-slugger; Astro 7 generates IDs itself. Diffed the emitted IDs
against the pre-cutover baseline to confirm the 15 live deep links survive."
```

---

## Task 14: Route parity against the frozen baseline

The gate that proves no inbound link silently died.

**Files:**
- Create: `migration/check_routes.py`

- [ ] **Step 1: Write the route-parity checker**

`migration/check_routes.py`:

```python
#!/usr/bin/env python3
"""Diff dist/ routes against the pre-cutover baseline.

Deletions are expected and enumerated. Anything else is a regression.
"""
from __future__ import annotations

import pathlib
import re
import sys

BASE = pathlib.Path('migration/baseline-urls.txt')
SITE = 'https://docs.surogate.ai'

# Trees the migration deliberately drops (spec section 3 and 7.7).
EXPECTED_GONE = re.compile(
    r'^/(old-docs|about|getting-started|guides|examples|appendix|reference)(/|$)'
    r'|^/opensearch\.xml$'
)


def norm(url: str) -> str:
    path = url.replace(SITE, '') or '/'
    return path if path.endswith('/') else path + '/'


def main() -> int:
    baseline = {norm(u) for u in BASE.read_text().split() if u.strip()}
    built = set()
    for p in pathlib.Path('dist').rglob('index.html'):
        rel = p.parent.relative_to('dist').as_posix()
        built.add('/' if rel == '.' else f'/{rel}/')

    missing = sorted(u for u in baseline - built if not EXPECTED_GONE.match(u))
    dropped = sorted(u for u in baseline - built if EXPECTED_GONE.match(u))
    added = sorted(built - baseline)

    print(f'baseline routes : {len(baseline)}')
    print(f'built routes    : {len(built)}')
    print(f'intentionally dropped : {len(dropped)}')
    print(f'newly added           : {len(added)}')
    for u in added:
        print(f'  + {u}')
    if missing:
        print(f'\nREGRESSION - {len(missing)} baseline routes vanished '
              'without being in the expected-drop list:')
        for u in missing:
            print(f'  - {u}')
        return 1
    print('\nOK - every retained baseline route is present')
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 2: Run the parity check**

```bash
cd /work/surogate-docs && npm run build && python3 migration/check_routes.py
```

Expected: `OK - every retained baseline route is present`. The `newly added` list should contain `/search/` and nothing surprising.

- [ ] **Step 3: Investigate any regression before proceeding**

If routes are reported missing, each is an inbound link that will 404. For each: either it belongs in `EXPECTED_GONE` (a legacy path the spec drops — verify against spec §3), or a page/redirect is genuinely missing and must be added. Do not widen `EXPECTED_GONE` to silence a real gap.

- [ ] **Step 4: Confirm the 72 in-scope routes and 14 redirects are all present**

```bash
cd /work/surogate-docs
echo "work+develop pages: $(find dist/work dist/develop -name index.html | wc -l)"
echo "redirect stubs: $(( $(find dist/ops -name index.html | wc -l) + 1 ))"
```

Expected: `74` pages (72 content pages plus the `/work/` and `/develop/` slug-override roots resolve within that tree count — confirm the number matches `find src/content/docs/work src/content/docs/develop -name '*.md' | wc -l`), and `14` redirect stubs.

- [ ] **Step 5: Commit**

```bash
git add migration/check_routes.py
git commit -m "test(migration): add route parity check against the frozen baseline

Diffs dist/ against the pre-cutover sitemap captured before the Docusaurus
toolchain was removed. Intentional deletions -- the legacy trainer tree and
opensearch.xml -- are enumerated explicitly, so any other vanished route is
reported as a regression rather than absorbed silently."
```

---

## Task 15: CI pipeline

**Files:**
- Modify: `.github/workflows/deploy-docs.yml`

- [ ] **Step 1: Rewrite the workflow**

Trigger, permissions, concurrency and the `github-pages` environment are unchanged. The build step and Node version change, and the two verification gates run before deploy.

```yaml
name: Deploy Starlight docs to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Assert content invariants
        run: python3 migration/assert_content.py

      - name: Codemod unit tests
        run: python3 -m unittest discover -s migration -p 'test_*.py' -v

      - name: Build site
        run: npm run build

      - name: Type check
        run: npm run check

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Note: `withastro/action@v6` would replace the setup/install/build steps, but it does not run the content assertions or the codemod tests. Explicit steps are used so both gates block deployment. `starlight-links-validator` runs inside `npm run build`, so broken links fail the build without a separate step.

- [ ] **Step 2: Verify the workflow parses and the artifact path is right**

```bash
cd /work/surogate-docs
python3 -c "import sys;
try:
    import yaml
except ImportError:
    sys.exit('pyyaml unavailable - inspect the YAML by eye instead')
d = yaml.safe_load(open('.github/workflows/deploy-docs.yml'))
print('jobs:', list(d['jobs']))
print('node:', d['jobs']['build']['steps'][1]['with']['node-version'])
print('artifact path:', d['jobs']['build']['steps'][-1]['with']['path'])"
```

Expected: `jobs: ['build', 'deploy']`, `node: 22`, `artifact path: dist`. The path must be `dist` (Astro), not `build` (Docusaurus).

- [ ] **Step 3: Run the whole CI sequence locally**

```bash
cd /work/surogate-docs
rm -rf node_modules dist
npm ci
python3 migration/assert_content.py
python3 -m unittest discover -s migration -p 'test_*.py'
npm run build
npm run check
python3 migration/check_routes.py
```

Expected: every command exits 0.

- [ ] **Step 4: Confirm the workflow's auto-trigger is enabled**

Git history contains a commit disabling the auto-trigger when no runner was available. Verify `on.push.branches` includes `main` in the file you just wrote, and check the Actions tab is not disabled for the repo:

```bash
gh workflow list 2>/dev/null || echo "check the Actions tab manually"
```

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/deploy-docs.yml
git commit -m "ci: build the Starlight site and gate deploys on the invariants

Node moves 20 -> 22: astro@7.1.6 declares engines.node >=22.12.0, so the old
pin cannot build. Artifact path moves build/ -> dist/.

Runs the content assertions and codemod unit tests before the build, so the
silent-failure classes block deployment. Uses explicit steps rather than
withastro/action because the action would skip both gates.
starlight-links-validator already runs inside the build."
```

---

## Task 16: Final rendered verification and brand sign-off

Nothing here is scripted — it is the human pass that catches what assertions cannot.

**Files:** none modified (unless a defect is found)

- [ ] **Step 1: Serve the built site**

```bash
cd /work/surogate-docs && npm run build && npm run preview
```

- [ ] **Step 2: Confirm exactly one `<h1>` on every page**

```bash
cd /work/surogate-docs
python3 - <<'PY'
import pathlib, re
bad = []
for p in pathlib.Path('dist').rglob('index.html'):
    n = len(re.findall(r'<h1\b', p.read_text()))
    if n != 1:
        bad.append((p.parent.relative_to('dist').as_posix() or '/', n))
print('pages without exactly one h1:', bad)
PY
```

Expected: `[]`, or only redirect stubs (which have no `<h1>` at all — verify any entry is under `ops/` or `search/`).

- [ ] **Step 3: Check the ASCII-art pages for whitespace damage**

Astro 7 changes default HTML whitespace handling, and `<pre>` blocks are the risk class. Open each in the preview server and confirm the box-drawing diagrams still align:

- `/develop/` (`develop/intro.md`)
- `/develop/features/mcp-and-vault/`
- `/develop/features/knowledge-bases/`
- `/work/library/knowledge-bases/`
- `/develop/loop/overview/`
- `/develop/loop/build/`

- [ ] **Step 4: Check the aside-dense pages render styled**

- `/work/channels/self-registration/` — note, caution and tip, all three in one page
- `/develop/features/compute/` — `note[Free plan]` and `caution[Billing]`
- `/develop/features/connect-compute/` — two `note[Preview]` plus `note[Free plan]`
- `/work/library/mcp-servers/`, `/work/library/skills/`, `/work/library/knowledge-bases/` — the four de-quoted asides. Confirm each renders as a standalone aside and **is not wrapped in a blockquote**.

- [ ] **Step 5: Check navigation and search**

- Both sidebar groups present, inner subgroups collapsed
- `/develop/features/experts-arenas/` reachable and carrying its Preview badge
- Login CTA in the header linking to `ops.surogate.ai`; GitHub and X icons present
- Open the search modal, search "skills", confirm Pagefind returns results with trailing-slash URLs
- Toggle dark/light and confirm the accent green changes

- [ ] **Step 6: Brand sign-off**

There was nothing in the old `custom.css` to port beyond the accent colour, so the chrome now looks like default Starlight: different sidebar, different table of contents, different type scale, clickable heading anchors. **This is the most visible change to every reader.** Capture a before/after of `/work/` and confirm it is acceptable, or open a follow-up for a brand pass. Do not treat this as a defect to fix inside this migration.

- [ ] **Step 7: Record the results and commit any fixes**

If Steps 2–5 surfaced defects, fix them and commit with a `fix(content):` or `fix(theme):` subject. If everything passed, there is nothing to commit — say so explicitly rather than inventing a commit.

---

## Task 17 (optional): AI-crawler surface

Off the critical path. For documentation *about building agents*, an `llms.txt` is close to table stakes.

**Files:**
- Modify: `package.json`, `astro.config.mjs`

- [ ] **Step 1: Install the plugin**

```bash
cd /work/surogate-docs && npm install starlight-llms-txt
```

- [ ] **Step 2: Wire it in**

In `astro.config.mjs`, add the import and append to `plugins`:

```js
import starlightLlmsTxt from 'starlight-llms-txt';
```

```js
      plugins: [starlightLinksValidator(), starlightLlmsTxt()],
```

- [ ] **Step 3: Build and verify the output**

```bash
cd /work/surogate-docs && npm run build
ls -la dist/llms.txt dist/llms-full.txt
head -20 dist/llms.txt
```

Expected: both files present; `llms.txt` lists the site structure with real page titles.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat(seo): emit llms.txt for AI crawlers

Adds starlight-llms-txt so the docs expose a machine-readable index. For
documentation about building agents, an AI-crawler surface is close to table
stakes, and there was none before."
```

---

## Self-Review

**Spec coverage.** Walked every spec section against the plan:

| Spec § | Task |
|---|---|
| §3 scope / deletions | 2 (step 1) |
| §5 repo layout | 2, 9, 10 |
| §6.0 scaffold first | 2 |
| §6.1 fence-aware H1 strip | 3, 4 |
| §6.2 14 title/label pairs | 6 |
| §6.3 skills-and-experts structural edit | 5 (step 4) |
| §6.4 all 13 asides | 5 (steps 1–2) |
| §6.5 240 link rewrites | 3, 4 |
| §6.6 slug conversion | 6 (step 1) |
| §6.7 stray XML artifacts | 5 (step 3) |
| §6.8 orphan pages | 6 (step 5), 7 |
| §6.9 duplicate heading slugs | 1 (step 4), 13 |
| §7.1 sidebar | 7 |
| §7.2 URL form | 2 (step 10), 10 (step 5) |
| §7.3 config + redirects | 2, 9, 10, 11 |
| §7.4 header | 9 |
| §7.5 styling | 9 |
| §7.6 head/SEO/robots | 10 |
| §7.7 search + `/search` redirect | 11 |
| §7.8 homepage | 8 |
| §8 broken assets | 10 |
| §10 gate 0 baseline | 1 |
| §10 gates 1–7 | 12, 13, 14, 16 |
| §11 toolchain + CI | 2, 15 |
| §13 housekeeping | 1 (step 6) |
| §15 open items (defaults) | 5, 6, 9, 10, 17 |

No spec section is unimplemented.

**Placeholder scan.** No "TBD", "TODO", "implement later", "add error handling", or "similar to Task N". Every code step carries the actual content. Task 13 step 3 and Task 16 step 7 are conditional on a measurement rather than vague — each states the decision rule and both branches.

**Type consistency.** The codemod's public names are used identically everywhere they appear: `fence_states(lines) -> list[bool]` is imported by `migration/assert_content.py` (Task 12) and by the inline verification scripts in Task 4 steps 2/4/5; `strip_leading_h1`, `drop_frontmatter_key`, `rewrite_links` and `SLUG_OVERRIDES` are defined in Task 3 and referenced under the same names in Task 3's tests. `EXPECTED_FILES = 73` counts the 72 pages plus `index.mdx`, which Task 8 creates before Task 12 runs. `migration/baseline-anchors.txt`'s `path<TAB>heading-id` format is written in Task 1 step 4 and parsed with the same `split('\t')` in Task 13 step 1.

**One tension worth flagging to the executor.** Task 14 step 4's expected page count depends on how the two `slug`-override pages land in the `dist/work` / `dist/develop` trees. The step tells you to reconcile the number against the on-disk file count rather than asserting a hardcoded value, because `slug: work` emits `dist/work/index.html` — inside the same tree the check counts. Confirm the arithmetic rather than trusting a literal.

#!/usr/bin/env python3
"""Content assertions for the Starlight docs. Exit 1 on any violation.

Each check corresponds to a failure mode that builds clean but is wrong.
Nothing here produces a warning from Astro or Starlight.

Two tiers:

  structural  Rules that hold forever. Run on every build and in CI.
  counts      One-time corpus invariants from the Docusaurus migration.
              Run with --strict-counts. NOT suitable for CI, because they
              fail the moment someone legitimately adds a page or an aside.

Usage:
    python3 migration/assert_content.py                  # structural only
    python3 migration/assert_content.py --strict-counts  # + migration counts
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from codemod import fence_states  # noqa: E402

ROOT = 'src/content/docs'

# One-time corpus invariants, asserted only under --strict-counts.
EXPECTED_FILES = 76  # 75 migrated pages + the splash index
EXPECTED_FENCE_HASHES = 27  # shell comments a naive H1 strip would destroy
# 13 came across from Docusaurus; the 14th is the homepage's Open source note,
# written after the migration. This tracks the corpus, so it moves whenever
# content legitimately does -- which is why it is not a CI gate.
EXPECTED_ASIDES = 14

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def main(strict_counts: bool) -> int:
    files = sorted(
        glob.glob(f'{ROOT}/**/*.md', recursive=True)
        + glob.glob(f'{ROOT}/**/*.mdx', recursive=True)
    )
    if not files:
        fail(f'no content files found under {ROOT}')

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
        if re.search(r'^sidebar_label:', fm, re.M):
            fail(f'{p}: leftover Docusaurus sidebar_label (use sidebar.label)')

        sm = re.search(r'^slug:\s*(\S+)', fm, re.M)
        if sm:
            slug = sm.group(1)
            if slug.startswith('/'):
                fail(f'{p}: slug must be collection-relative, got {slug!r}')
            if slug in slugs:
                fail(
                    f'{p}: duplicate slug {slug!r} (also {slugs[slug]}) - '
                    'Starlight only warns and silently overwrites'
                )
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

    if strict_counts:
        if len(files) != EXPECTED_FILES:
            fail(f'expected {EXPECTED_FILES} content files, found {len(files)}')
        if fence_hashes != EXPECTED_FENCE_HASHES:
            fail(
                f'in-fence "# " comments: expected {EXPECTED_FENCE_HASHES}, '
                f'found {fence_hashes} - the H1 strip was not fence-aware'
            )
        if asides != EXPECTED_ASIDES:
            fail(f'valid asides: expected {EXPECTED_ASIDES}, found {asides}')

    if failures:
        print(f'FAIL ({len(failures)} violations)')
        for f in failures:
            print(f'  {f}')
        return 1

    tier = 'structural + migration counts' if strict_counts else 'structural'
    print(
        f'OK [{tier}] - {len(files)} files, {fence_hashes} fence comments '
        f'preserved, {asides} asides'
    )
    return 0


if __name__ == '__main__':
    sys.exit(main('--strict-counts' in sys.argv))

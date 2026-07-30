#!/usr/bin/env python3
"""One-shot codemod: Docusaurus docs/ -> Starlight src/content/docs/.

Python 3 stdlib only. Every transform is fence-aware: 22 '# ' lines in this
corpus are shell/Python comments inside code fences, and destroying them would
silently corrupt ~20 code examples.
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
    long, and carry nothing after it. That last rule is what stops ```python
    from closing the fence it just opened.
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
        if (
            m
            and m.group(1)[0] == opener[0]
            and len(m.group(1)) >= opener[1]
            and not stripped[len(m.group(1)):].strip()
        ):
            opener = None
    return states


def strip_leading_h1(body: str) -> tuple[str, str | None]:
    """Remove the first out-of-fence '# ' heading.

    Starlight renders the frontmatter title as the page <h1>, so a body H1 is a
    duplicate. Only the FIRST is removed: skills-and-experts.md has a
    legitimate second H1 that is demoted by hand.
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

    Astro rewrites nothing and warns about nothing, so an unrewritten .md link
    ships as a 404.
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

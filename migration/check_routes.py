#!/usr/bin/env python3
"""Diff dist/ routes against the pre-cutover baseline.

Deletions are expected and enumerated. Anything else is a regression: a URL
that was live before the migration and 404s after it.
"""

from __future__ import annotations

import pathlib
import re
import sys

BASE = pathlib.Path('migration/baseline-urls.txt')
SITE = 'https://docs.surogate.ai'

# Trees the migration deliberately drops (spec sections 3 and 7.7).
EXPECTED_GONE = re.compile(
    r'^/(old-docs|about|getting-started|guides|examples|appendix|reference)(/|$)'
    r'|^/opensearch\.xml/?$'
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

    print(f'baseline routes       : {len(baseline)}')
    print(f'built routes          : {len(built)}')
    print(f'intentionally dropped : {len(dropped)}')
    print(f'newly added           : {len(added)}')
    for u in added:
        print(f'  + {u}')

    if missing:
        print(
            f'\nREGRESSION - {len(missing)} baseline routes vanished without '
            'being in the expected-drop list:'
        )
        for u in missing:
            print(f'  - {u}')
        return 1

    print('\nOK - every retained baseline route is present')
    return 0


if __name__ == '__main__':
    sys.exit(main())

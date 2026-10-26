"""Helpers for checks on the built site in dist/. Run `npm run build` first."""

from html.parser import HTMLParser
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / 'dist'

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


def page(route: str) -> str:
    """The built HTML for a route such as '/work/quickstart/' or '/'."""
    path = DIST / route.strip('/') / 'index.html' if route.strip('/') else DIST / 'index.html'
    return path.read_text(encoding='utf-8')


class _Finder(HTMLParser):
    def __init__(self, key: str, value: str):
        super().__init__(convert_charrefs=False)
        self.key, self.value = key, value
        self.start = self.end = None
        self.depth = 0
        self.tag = None

    def handle_starttag(self, tag, attrs):
        if self.end is not None:
            return
        if self.start is None:
            if dict(attrs).get(self.key) == self.value:
                self.tag = tag
                self.start = self._offset() + len(self.get_starttag_text())
                self.depth = 0 if tag in VOID else 1
                if tag in VOID:
                    self.end = self.start
        elif tag == self.tag and tag not in VOID:
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        if self.start is None and dict(attrs).get(self.key) == self.value:
            self.start = self.end = self._offset() + len(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.start is not None and self.end is None and tag == self.tag:
            self.depth -= 1
            if self.depth == 0:
                self.end = self._offset()

    def _offset(self) -> int:
        line, col = self.getpos()
        return self.line_starts[line - 1] + col


def section(doc: str, name: str) -> str:
    """Inner HTML of the first element with data-docs=name, or id=name[1:] when name starts with '#'."""
    key, value = ('id', name[1:]) if name.startswith('#') else ('data-docs', name)
    finder = _Finder(key, value)
    finder.line_starts = [0]
    for line in doc.splitlines(keepends=True):
        finder.line_starts.append(finder.line_starts[-1] + len(line))
    finder.feed(doc)
    finder.close()
    if finder.start is None or finder.end is None:
        raise AssertionError(f'no element with {key}="{value}"')
    return doc[finder.start:finder.end]

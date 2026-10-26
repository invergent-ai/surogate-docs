import re
import unittest

from docsite import DIST, page, section


def built_css():
    return '\n'.join(p.read_text(encoding='utf-8') for p in (DIST / '_astro').glob('*.css'))


class ThemeCss(unittest.TestCase):
    def test_both_token_sets_ship(self):
        css = built_css().replace(' ', '').lower()
        for value in ('--d-bg:#fff', '--d-bg:#1a0a1c', '--d-link:#9b1f61', '--d-link:#ffaf10', '--d-mark:#ffe845'):
            self.assertIn(value, css)

    def test_old_green_is_gone(self):
        css = built_css().lower()
        self.assertNotIn('#07a000', css)
        self.assertNotIn('#87ed82', css)


if __name__ == '__main__':
    unittest.main()

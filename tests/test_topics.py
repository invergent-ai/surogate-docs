import re
import unittest

from docsite import DIST, page, section


class Topics(unittest.TestCase):
    def sidebar_links(self, route):
        # The page tree only: the track switch and the topic list above it link to other tracks on purpose.
        pane = section(page(route), '#starlight__sidebar')
        tree = pane[pane.index('<ul class="top-level'):]
        if 'data-docs="mobile-foot"' in tree:  # the mobile menu's product links follow the tree
            tree = tree[:tree.index('data-docs="mobile-foot"')]
        return re.findall(r'href="(/[^"#]*)"', tree)

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


if __name__ == '__main__':
    unittest.main()

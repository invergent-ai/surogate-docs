import re
import unittest

from docsite import DIST, page, section


CAPTURE = ['/dms/quickstart-capture/', '/dms/examples/incoming-mail/', '/dms/work/capture/', '/dms/work/capture-inbox/',
           '/dms/work/capture-validate/', '/dms/admin/capture-channels/', '/dms/admin/separator-sheets/',
           '/dms/admin/capture-templates/', '/dms/admin/capture-flows/']


PORTAL = ['/portal/', '/portal/quickstart/', '/portal/console/sign-in/', '/portal/console/users/',
          '/portal/console/groups/', '/portal/console/organizations/', '/portal/console/sign-in-providers/',
          '/portal/console/tokens/', '/portal/console/tenants/', '/portal/reference/roles/']


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

    def test_dms_sidebar_has_only_dms_pages(self):
        links = self.sidebar_links('/dms/')
        self.assertIn('/dms/', links)
        self.assertFalse([l for l in links if l.startswith(('/work/', '/develop/', '/keel/'))])

    def test_dms_sidebar_lists_the_capture_pages(self):
        links = self.sidebar_links('/dms/')
        for route in CAPTURE:
            self.assertIn(route, links)

    def test_other_sidebars_have_no_dms_pages(self):
        for route in ('/keel/', '/work/quickstart/', '/develop/'):
            self.assertFalse([l for l in self.sidebar_links(route) if l.startswith('/dms/')], route)

    def test_portal_sidebar_has_only_portal_pages(self):
        links = self.sidebar_links('/portal/')
        for route in PORTAL:
            self.assertIn(route, links)
        self.assertFalse([l for l in links if not l.startswith('/portal/')])

    def test_other_sidebars_have_no_portal_pages(self):
        for route in ('/keel/', '/dms/', '/work/quickstart/', '/develop/'):
            self.assertFalse([l for l in self.sidebar_links(route) if l.startswith('/portal/')], route)

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
        self.assertNotIn('rel="prev"', page('/dms/'))
        self.assertNotIn('rel="next"', page('/dms/reference/faq/'))
        self.assertNotIn('rel="prev"', page('/portal/'))
        self.assertNotIn('rel="next"', page('/portal/reference/roles/'))


if __name__ == '__main__':
    unittest.main()

import re
import unittest

from docsite import DIST, page, section


def words(html):
    return re.sub(r'<[^>]+>', ' ', html).split()


class PageFrame(unittest.TestCase):
    def test_breadcrumb_agents(self):
        crumb = words(section(page('/work/quickstart/'), 'breadcrumb'))
        self.assertEqual(crumb, ['Surogate', 'Agents', '/', 'Work', '/', 'Quickstart'])

    def test_breadcrumb_keel_has_no_track(self):
        crumb = words(section(page('/keel/quickstart/'), 'breadcrumb'))
        self.assertEqual(crumb, ['Keel', '/', 'Keel', 'quickstart'])

    def test_breadcrumb_dms_quickstart(self):
        crumb = words(section(page('/dms/quickstart/'), 'breadcrumb'))
        self.assertEqual(crumb, ['Surogate', 'DMS', '/', 'Surogate', 'DMS', 'quickstart'])

    def test_breadcrumb_dms_home_stops_at_the_product(self):
        crumb = words(section(page('/dms/'), 'breadcrumb'))
        self.assertEqual(crumb, ['Surogate', 'DMS'])

    def test_breadcrumb_on_a_track_home_stops_at_the_track(self):
        crumb = words(section(page('/develop/'), 'breadcrumb'))
        self.assertEqual(crumb, ['Surogate', 'Agents', '/', 'Develop'])

    def test_edit_link_moves_beside_the_toc(self):
        doc = page('/work/quickstart/')
        self.assertIn('github.com/invergent-ai/surogate-docs/edit/main/', section(doc, 'edit-link'))
        self.assertNotIn('surogate-docs/edit/main/', section(doc, 'site-footer'))

    def test_site_footer(self):
        foot = section(page('/keel/'), 'site-footer')
        for href in ('https://surogate.ai', 'https://discord.gg/eVTq93BrQ4', 'https://github.com/invergent-ai/surogate'):
            self.assertIn(href, foot)


if __name__ == '__main__':
    unittest.main()

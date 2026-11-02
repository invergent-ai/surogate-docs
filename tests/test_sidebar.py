import re
import unittest

from docsite import DIST, page, section


class Sidebar(unittest.TestCase):
    def test_agents_pages_have_head_and_switch(self):
        doc = page('/work/quickstart/')
        self.assertIn('Surogate Agents', section(doc, 'product-head'))
        switch = section(doc, 'track-switch')
        self.assertRegex(switch, r'href="/work/"[^>]*aria-current="page"')
        self.assertIn('href="/develop/"', switch)

    def test_develop_is_current_on_develop_pages(self):
        switch = section(page('/develop/features/training/'), 'track-switch')
        self.assertRegex(switch, r'href="/develop/"[^>]*aria-current="page"')

    def test_keel_has_head_and_no_switch(self):
        doc = page('/keel/builder/rules/')
        self.assertIn('Surogate Keel', section(doc, 'product-head'))
        self.assertNotIn('data-docs="track-switch"', doc)

    def test_dms_admin_page_has_head_and_no_switch(self):
        doc = page('/dms/admin/people/')
        self.assertIn('Surogate DMS', section(doc, 'product-head'))
        self.assertNotIn('data-docs="track-switch"', doc)

    def test_dms_has_head_and_no_switch(self):
        doc = page('/dms/')
        self.assertIn('Surogate DMS', section(doc, 'product-head'))
        self.assertNotIn('data-docs="track-switch"', doc)


if __name__ == '__main__':
    unittest.main()

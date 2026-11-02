import re
import unittest

from docsite import DIST, page, section


class Header(unittest.TestCase):
    def test_sign_in_and_products_on_every_kind_of_page(self):
        for route in ('/', '/work/quickstart/', '/keel/', '/dms/'):
            head = section(page(route), 'header')
            self.assertIn('href="https://ops.surogate.ai"', head)
            self.assertIn('Surogate Agents', head)
            self.assertIn('Surogate Keel', head)
            self.assertIn('Surogate DMS', head)
            self.assertIn('data-docs="theme-toggle"', head)

    def test_current_product(self):
        work = section(page('/develop/'), 'header')
        self.assertRegex(work, r'aria-current="page"[^>]*>\s*Surogate Agents')
        keel = section(page('/keel/quickstart/'), 'header')
        self.assertRegex(keel, r'aria-current="page"[^>]*>\s*Surogate Keel')
        dms_quick = section(page('/dms/quickstart/'), 'header')
        self.assertRegex(dms_quick, r'aria-current="page"[^>]*>\s*Surogate DMS')
        self.assertEqual(dms_quick.count('aria-current="page"'), 1)
        dms = section(page('/dms/'), 'header')
        self.assertRegex(dms, r'aria-current="page"[^>]*>\s*Surogate DMS')
        self.assertEqual(dms.count('aria-current="page"'), 1)
        self.assertNotIn('aria-current', section(page('/'), 'header'))

    def test_no_social_icons(self):
        self.assertNotIn('x.com', page('/work/'))


if __name__ == '__main__':
    unittest.main()

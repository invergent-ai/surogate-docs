import re
import unittest

from docsite import DIST, page, section


class Header(unittest.TestCase):
    def test_sign_in_and_products_on_every_kind_of_page(self):
        for route in ('/', '/work/quickstart/', '/keel/'):
            head = section(page(route), 'header')
            self.assertIn('href="https://ops.surogate.ai"', head)
            self.assertIn('Surogate Agents', head)
            self.assertIn('Keel', head)
            self.assertIn('data-docs="theme-toggle"', head)

    def test_current_product(self):
        work = section(page('/develop/'), 'header')
        self.assertRegex(work, r'aria-current="page"[^>]*>\s*Surogate Agents')
        keel = section(page('/keel/quickstart/'), 'header')
        self.assertRegex(keel, r'aria-current="page"[^>]*>\s*Keel')
        self.assertNotIn('aria-current', section(page('/'), 'header'))

    def test_no_social_icons(self):
        self.assertNotIn('x.com', page('/work/'))


if __name__ == '__main__':
    unittest.main()

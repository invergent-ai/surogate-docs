import re
import unittest

from docsite import DIST, page, section


class Content(unittest.TestCase):
    def test_quickstart_screenshots_have_captions(self):
        doc = page('/work/quickstart/')
        self.assertIn('<figcaption>The template catalog, filtered by category, with the Empty Agent card first</figcaption>', doc)
        self.assertRegex(doc, r'<figure>\s*<img[^>]+src="/_astro/')

    def test_short_opening_is_a_lead(self):
        self.assertIn('class="lead"', page('/work/quickstart/'))

    def test_dms_quickstart_caption_and_lead(self):
        doc = page('/dms/quickstart/')
        self.assertIn('<figcaption>The Upload a document dialog: the file, the title, the Building permit type and its required fields</figcaption>', doc)
        self.assertIn('class="lead"', doc)

    def test_dms_capture_quickstart_caption_and_lead(self):
        doc = page('/dms/quickstart-capture/')
        self.assertIn('<figcaption>The dialog New separator sheet profile filled in for Applications: the document type Application and the folder of the channel, with no template</figcaption>', doc)
        self.assertIn('class="lead"', doc)

    def test_portal_pages_show_the_console(self):
        doc = page('/portal/quickstart/')
        self.assertIn('<figcaption>The New user dialog: Email, Name and Password (optional).</figcaption>', doc)
        self.assertRegex(doc, r'<figure>\s*<img[^>]+src="/_astro/')
        tenants = page('/portal/console/tenants/')
        self.assertIn('Add administrator', tenants)
        self.assertNotIn('kubectl', tenants)


if __name__ == '__main__':
    unittest.main()

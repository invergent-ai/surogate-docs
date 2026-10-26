import re
import unittest

from docsite import DIST, page, section


def built_css():
    return '\n'.join(p.read_text(encoding='utf-8') for p in (DIST / '_astro').glob('*.css'))


class ReviewFixes(unittest.TestCase):
    def test_edit_link_also_in_footer_below_lg_on_toc_pages(self):
        doc = page('/work/channels/slack/')
        foot = section(doc, 'edit-link-footer')
        self.assertIn('github.com/invergent-ai/surogate-docs/edit/main/', foot)
        self.assertRegex(doc, r'data-docs="edit-link-footer"[^>]*class="[^"]*lg:sl-hidden|class="[^"]*lg:sl-hidden[^"]*"[^>]*data-docs="edit-link-footer"')

    def test_404_header_has_search(self):
        doc = (DIST / '404.html').read_text(encoding='utf-8')
        head = section(doc, 'header')
        self.assertIn('data-open-modal', head)
        self.assertNotIn('class="site-link"', head)

    def test_screenshots_keep_space_above_them(self):
        css = built_css().replace(' ', '')
        rule = re.search(r'figure:not\(\.frame\)\{([^}]*)\}', css)
        self.assertIsNotNone(rule)
        self.assertNotRegex(rule.group(1), r'(^|;)margin:0(;|$)')

    def test_sign_in_stays_on_phones_when_there_is_no_menu(self):
        self.assertIn('data-has-menu="false"', section(page('/'), 'header') + page('/'))
        self.assertIn('data-has-menu="true"', page('/work/quickstart/'))


if __name__ == '__main__':
    unittest.main()

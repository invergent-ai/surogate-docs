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

    def test_portal_directory_pages(self):
        doc = page('/portal/console/directories/')
        self.assertIn('<figcaption>A directory open in the console: Test connection says it finds 3 users, and its group mappings are below.</figcaption>', doc)
        for route in ('/portal/console/group-mappings/', '/portal/console/scim/'):
            self.assertIn('Directories', page(route))
        for route in ('/portal/console/directories/', '/portal/console/scim/', '/portal/console/group-mappings/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

    def test_portal_permission_pages(self):
        doc = page('/portal/console/access/')
        self.assertIn('<figcaption>Check access for ana@example.ro on the page main/intranet: Allowed, with the steps down to the group Funcționari.</figcaption>', doc)
        guide = page('/portal/sites/permissions/')
        self.assertIn('group:Funcționari', guide)
        self.assertIn('href="/portal/console/access/"', guide)
        for route in ('/portal/console/access/', '/portal/sites/permissions/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

    def test_portal_audit_and_personal_data(self):
        doc = page('/portal/console/audit/')
        self.assertIn('<figcaption>The Audit log: the latest events, each with who did it and to what, and the note that the log is intact.</figcaption>', doc)
        self.assertIn('Personal data', page('/portal/console/users/'))
        for route in ('/portal/console/audit/', '/portal/console/users/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))


    def test_portal_machine_access(self):
        doc = page('/portal/console/service-accounts/')
        self.assertIn('<figcaption>A service account', doc)
        self.assertIn('Act for a person', doc)
        self.assertIn('id="scopes"', page('/portal/console/tokens/'))
        self.assertIn('id="impersonate"', page('/portal/console/users/'))
        self.assertIn('Private repository', page('/portal/console/tenants/'))
        for route in ('/portal/console/service-accounts/', '/portal/console/tokens/',
                      '/portal/console/users/', '/portal/console/tenants/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

    def test_portal_sign_in_policies(self):
        self.assertIn('id="the-second-step"', page('/portal/console/sign-in/'))
        self.assertIn('id="with-a-certificate"', page('/portal/console/sign-in/'))
        self.assertIn('id="two-step-sign-in"', page('/portal/console/account/'))
        self.assertIn('id="sessions"', page('/portal/console/account/'))
        self.assertIn('Who needs it', page('/portal/console/sign-in-policy/'))
        self.assertIn('id="two-step-sign-in"', page('/portal/console/users/'))
        for route in ('/portal/console/sign-in/', '/portal/console/account/',
                      '/portal/console/sign-in-policy/', '/portal/console/users/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

if __name__ == '__main__':
    unittest.main()

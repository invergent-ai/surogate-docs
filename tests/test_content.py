import re
import unittest
from pathlib import Path

from docsite import DIST, page, section

ROOT = Path(__file__).resolve().parent.parent


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

    def test_portal_hooks(self):
        guide = page('/portal/sites/apps/')
        self.assertIn('id="hooks"', guide)
        self.assertIn('env.memory', guide)
        self.assertIn('href="/portal/sites/apps/#hooks"', page('/portal/console/apps/'))
        self.assertIn('Revoke', page('/portal/console/apps/'))
        for route in ('/portal/sites/apps/', '/portal/console/apps/', '/portal/console/users/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

    def test_portal_app_kit(self):
        guide = page('/portal/sites/build-an-app/')
        for anchor in ('start-from-a-working-app', 'check-what-the-portal-sends', 'send-events-from-the-apps-server', 'write-a-web-component', 'types-from-the-manifest'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('portalVerifier', guide)
        self.assertIn('href="/portal/console/apps/#for-the-apps-developers"', guide)
        self.assertIn('href="/portal/sites/build-an-app/"', page('/portal/sites/apps/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_develop_locally(self):
        guide = page('/portal/sites/develop-locally/')
        for anchor in ('start-the-portal', 'keep-it-in-step-with-your-files', 'test-against-a-throwaway-portal'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('startPortal', guide)
        self.assertIn('href="/portal/sites/develop-locally/"', page('/portal/sites/build-an-app/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_check(self):
        guide = page('/portal/sites/check-a-site/')
        for anchor in ('check-the-files-and-the-apps', 'permission-sanity', 'render-every-page', 'compare-with-the-previous-run', 'the-report'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('href="/portal/sites/develop-locally/"', guide)
        self.assertIn('href="/portal/sites/check-a-site/"', page('/portal/sites/develop-locally/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_agents(self):
        guide = page('/portal/sites/agents/')
        for anchor in ('install-the-skills', 'give-the-agent-an-identity', 'connect-the-mcp-server', 'the-loop'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('href="/portal/sites/check-a-site/"', guide)
        self.assertIn('href="/portal/sites/agents/"', page('/portal/console/tokens/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_design(self):
        guide = page('/portal/sites/design/')
        for anchor in ('the-design-package', 'the-tokens', 'check-it', 'for-apps'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('od-design-system-project/v1', guide)
        self.assertIn('href="/portal/sites/design/"', page('/portal/sites/build-an-app/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_studio(self):
        doc = page('/portal/console/studio/')
        for anchor in ('turn-it-on', 'design-in-the-studio', 'use-a-design-in-a-site', 'turn-it-off', 'new-tokens', 'erase'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/studio/"', page('/portal/sites/design/'))
        for route in ('/portal/console/studio/', '/portal/sites/design/'):
            text = page(route)
            for word in ('kubectl', 'helm', 'PORTAL_', 'Open Design', 'open-design', 'OpenDesign', 'nexu'):
                self.assertNotIn(word, text)
        source = (ROOT / 'src/content/docs/portal/console/studio.md').read_text()
        for word in ('git', 'Git', 'commit', 'repositor', 'Hub', 'merge'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_layouts(self):
        doc = page('/portal/sites/layouts/')
        for anchor in ('a-layout-of-the-sites-own', 'the-marked-places', 'what-a-frame-may-hold', 'images-in-each-screens-size', 'its-stylesheet', 'an-html-block', 'fragments-and-page-templates'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/layouts/"', page('/portal/sites/design/'))
        source = (ROOT / 'src/content/docs/portal/sites/layouts.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'parse5', 'Open Design'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_pages(self):
        doc = page('/portal/console/pages/')
        for anchor in ('the-page-tree', 'edit-a-page', 'move-what-a-page-holds', 'fragments', 'page-templates', 'personal-dashboards', 'preview-before-saving', 'when-a-save-is-refused'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/pages/"', page('/portal/console/versions/'))
        self.assertIn('href="/portal/console/pages/"', page('/portal/sites/layouts/'))
        source = (ROOT / 'src/content/docs/portal/console/pages.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'YAML', 'yaml'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_content(self):
        doc = page('/portal/console/content/')
        for anchor in ('find-an-entry', 'write-an-entry', 'publish', 'when-someone-else-is-editing', 'show-content-on-a-page'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/content/#show-content-on-a-page"', page('/portal/console/pages/'))
        source = (ROOT / 'src/content/docs/portal/console/content.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'YAML', 'yaml'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)
        types = page('/portal/sites/content-types/')
        for anchor in ('a-content-type', 'field-types', 'how-an-entry-looks', 'show-it-on-a-page'):
            self.assertIn(f'id="{anchor}"', types)
        self.assertIn('href="/portal/console/content/"', types)
        source = (ROOT / 'src/content/docs/portal/sites/content-types.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'repositor', 'Hub'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_seo(self):
        doc = page('/portal/sites/seo/')
        for anchor in ('what-each-page-says', 'describe-a-page', 'describe-a-site', 'what-crawlers-are-told'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/seo/"', page('/portal/console/pages/'))
        source = (ROOT / 'src/content/docs/portal/sites/seo.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_versions(self):
        doc = page('/portal/console/versions/')
        for anchor in ('what-the-list-shows', 'undo-a-change'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/versions/"', page('/portal/console/tenants/'))
        self.assertIn('id="kept-by-the-portal"', page('/portal/console/tenants/'))
        # The page's own words: what a tenant administrator reads never names the store behind it.
        source = (ROOT / 'src/content/docs/portal/console/versions.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub'):
            self.assertNotIn(word, source)

    def test_portal_previews(self):
        guide = page('/portal/sites/previews/')
        for anchor in ('make-a-preview', 'its-people', 'see-it-as-one-of-its-people', 'sync-it-again', 'its-apps', 'when-it-ends', 'who-may-make-previews'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('manager@preview.example', guide)
        self.assertIn('href="/portal/sites/previews/"', page('/portal/sites/agents/'))
        self.assertIn('href="/portal/sites/previews/"', page('/portal/console/tokens/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_events(self):
        doc = page('/portal/console/events/')
        self.assertIn('<figcaption>The Events page', doc)
        self.assertIn('id="webhooks"', doc)
        guide = page('/portal/sites/apps/')
        self.assertIn('id="events"', guide)
        self.assertIn('portal-event+jwt', guide)
        self.assertIn('href="/portal/console/events/"', guide)
        for route in ('/portal/console/events/', '/portal/sites/apps/'):
            for word in ('kubectl', 'helm', 'PORTAL_', 'whsec_x'):
                self.assertNotIn(word, page(route))

    def test_portal_apps(self):
        doc = page('/portal/console/apps/')
        self.assertIn('<figcaption>The Apps page', doc)
        self.assertIn('id="approve-an-app"', doc)
        self.assertIn('id="for-the-apps-developers"', doc)
        self.assertIn('href="/portal/sites/apps/"', page('/portal/sites/permissions/') + doc)
        guide = page('/portal/sites/apps/')
        self.assertIn('portal-request+jwt', guide)
        self.assertIn('href="/portal/console/apps/#for-the-apps-developers"', guide)
        for route in ('/portal/console/apps/', '/portal/sites/apps/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))
        for route in ('/portal/console/sign-in/', '/portal/console/account/',
                      '/portal/console/sign-in-policy/', '/portal/console/users/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

if __name__ == '__main__':
    unittest.main()

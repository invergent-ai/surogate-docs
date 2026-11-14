import re
import unittest
from pathlib import Path

from docsite import DIST, page, section

ROOT = Path(__file__).resolve().parent.parent

# The portal's site pages written UI first, with screenshots of what people see.
UI_FIRST_PAGES = ('actions.md', 'activity.md', 'announcements.md', 'apps.md', 'assistants.md', 'blogs.md', 'calendar.md',
                  'comments.md', 'connectors.md', 'content-types.md', 'data-models.md', 'endpoints.md', 'environments.md',
                  'flows.md', 'form-fields.md', 'forms.md', 'forums.md', 'guides.md', 'jobs.md', 'kpis.md', 'layouts.md', 'listings.md',
                  'notifications.md', 'permissions.md', 'polls.md', 'search.md', 'seo.md', 'values.md', 'wiki.md')

# The console pages written the same way.
CONSOLE_PAGES = ('data-console.md', 'files.md', 'invitations.md', 'sites.md')

# Developer pages that are not the config of one user page.
DEVELOPER_ONLY = ('index.md', 'command-line.md', 'develop-locally.md', 'check-a-site.md', 'previews.md', 'agents.md',
                  'build-an-app.md', 'design.md')

# Code a person types into a console screen, not config: search synonyms and pinned results, a data console query.
TYPED_IN_THE_CONSOLE = {'console/search.md': '', 'console/data-console.md': 'sql'}

PORTAL = ROOT / 'src/content/docs/portal'


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
        for anchor in ('what-people-see', 'restrict-a-page', 'editors', 'bloggers'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('group:Funcționari', page('/portal/developer/permissions/'))
        self.assertIn('href="/portal/console/access/"', guide)
        for route in ('/portal/console/access/', '/portal/sites/permissions/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

    def test_portal_principal_picker(self):
        # Who sees and who edits are chosen in the console, with the picker, not written in files.
        perms = (PORTAL / 'sites/permissions.md').read_text()
        self.assertIn('portal-principal-picker', perms)
        self.assertIn('portal-principal-picker', page('/portal/sites/permissions/'))
        self.assertIn('id="choose-who"', page('/portal/sites/permissions/'))
        self.assertIn('Who edits it', (PORTAL / 'console/sites.md').read_text())
        self.assertIn('Who writes blog posts', (PORTAL / 'console/sites.md').read_text())
        self.assertIn('Who sees this block', (PORTAL / 'console/pages.md').read_text())
        self.assertIn('id="who-sees-and-who-edits"', page('/portal/console/pages/'))
        forms = (PORTAL / 'console/forms.md').read_text()
        self.assertNotIn('one per line', forms)
        self.assertIn('Who may send it', forms)
        self.assertIn('Who reads what was sent', forms)
        self.assertIn('Who writes blog posts', (PORTAL / 'sites/blogs.md').read_text())
        # Only libraries' bloggers are still set in the site's configuration.
        self.assertEqual(perms.count('For now'), 1)

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
        self.assertNotIn('Private repository', page('/portal/console/tenants/'))
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
        self.assertIn('env.memory', page('/portal/developer/apps/'))
        self.assertIn('href="/portal/sites/apps/#hooks"', page('/portal/console/apps/'))
        self.assertIn('Revoke', page('/portal/console/apps/'))
        for route in ('/portal/sites/apps/', '/portal/developer/apps/', '/portal/console/apps/', '/portal/console/users/'):
            for word in ('kubectl', 'helm', 'PORTAL_'):
                self.assertNotIn(word, page(route))

    def test_portal_app_kit(self):
        guide = page('/portal/developer/build-an-app/')
        for anchor in ('start-from-a-working-app', 'check-what-the-portal-sends', 'send-events-from-the-apps-server', 'write-a-web-component', 'let-the-person-pick-a-dms-document', 'types-from-the-manifest'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('portalVerifier', guide)
        self.assertIn('href="/portal/console/apps/#for-the-apps-developers"', guide)
        self.assertIn('href="/portal/developer/build-an-app/"', page('/portal/sites/apps/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_develop_locally(self):
        guide = page('/portal/developer/develop-locally/')
        for anchor in ('start-the-portal', 'keep-it-in-step-with-your-files', 'test-against-a-throwaway-portal'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('startPortal', guide)
        self.assertIn('href="/portal/developer/develop-locally/"', page('/portal/developer/build-an-app/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_check(self):
        guide = page('/portal/developer/check-a-site/')
        for anchor in ('check-the-files-and-the-apps', 'permission-sanity', 'render-every-page', 'compare-with-the-previous-run', 'the-report'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('href="/portal/developer/develop-locally/"', guide)
        self.assertIn('href="/portal/developer/check-a-site/"', page('/portal/developer/develop-locally/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_agents(self):
        guide = page('/portal/developer/agents/')
        for anchor in ('install-the-skills', 'give-the-agent-an-identity', 'connect-the-mcp-server', 'the-loop'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('href="/portal/developer/check-a-site/"', guide)
        self.assertIn('href="/portal/developer/agents/"', page('/portal/console/tokens/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_design(self):
        guide = page('/portal/developer/design/')
        for anchor in ('the-design-package', 'the-tokens', 'check-it', 'for-apps'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('od-design-system-project/v1', guide)
        self.assertIn('href="/portal/developer/design/"', page('/portal/developer/build-an-app/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_studio(self):
        doc = page('/portal/console/studio/')
        for anchor in ('turn-it-on', 'design-in-the-studio', 'use-a-design-in-a-site', 'turn-it-off', 'new-tokens', 'erase'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/studio/"', page('/portal/developer/design/'))
        for route in ('/portal/console/studio/', '/portal/developer/design/'):
            text = page(route)
            for word in ('kubectl', 'helm', 'PORTAL_', 'Open Design', 'open-design', 'OpenDesign', 'nexu'):
                self.assertNotIn(word, text)
        source = (ROOT / 'src/content/docs/portal/console/studio.md').read_text()
        for word in ('git', 'Git', 'commit', 'repositor', 'Hub', 'merge'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_layouts(self):
        doc = page('/portal/sites/layouts/')
        for anchor in ('what-people-see', 'a-layout-of-the-sites-own', 'the-marked-places', 'what-a-frame-may-hold', 'images-in-each-screens-size', 'its-stylesheet', 'an-html-block', 'fragments-and-page-templates'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/layouts/"', page('/portal/developer/design/'))
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

    def test_portal_vocabularies(self):
        doc = page('/portal/console/vocabularies/')
        for anchor in ('the-list', 'make-a-vocabulary', 'categories', 'removing', 'when-a-save-is-refused'):
            self.assertIn(f'id="{anchor}"', doc)
        source = (PORTAL / 'console/vocabularies.md').read_text()
        for shot in ('portal-vocabularies-list', 'portal-vocabulary-edit'):
            self.assertIn(shot, source)
        self.assertIn('href="/portal/console/vocabularies/"', page('/portal/sites/content-types/'))
        self.assertIn('href="/portal/console/vocabularies/"', page('/portal/console/content/'))
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'YAML', 'yaml'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_rich_text(self):
        doc = page('/portal/console/pages/')
        self.assertIn('id="write-text"', doc)
        self.assertIn('portal-rich-text', (PORTAL / 'console/pages.md').read_text())
        self.assertIn('href="/portal/console/pages/#write-text"', page('/portal/console/content/'))
        self.assertNotIn('written in HTML', (PORTAL / 'console/pages.md').read_text())

    def test_portal_widgets_in_the_page_editor(self):
        for shot in ('portal-widget-poll-set', 'portal-widget-calendar-set'):
            self.assertIn(shot, (PORTAL / 'console/pages.md').read_text())
        doc = page('/portal/console/pages/')
        self.assertIn('id="the-portals-widgets"', doc)
        for route in ('/portal/sites/polls/', '/portal/sites/listings/'):
            self.assertRegex(doc, rf'href="{route}(#[a-z-]+)?"')
        # The feature pages tell how to place a widget in the editor, not that the editor cannot.
        for name in ('activity', 'announcements', 'assistants', 'blogs', 'calendar', 'comments', 'documents', 'forums',
                     'keel', 'kpis', 'listings', 'notifications', 'polls', 'wiki'):
            source = (PORTAL / 'sites' / f'{name}.md').read_text()
            self.assertNotIn('does not place', source, name)
            self.assertIn('/portal/console/pages/#the-portals-widgets', source, name)
            self.assertIn('/portal/console/pages/#the-portals-widgets', page(f'/portal/sites/{name}/'), name)
        self.assertIn('**Add a widget…**', (PORTAL / 'sites/polls.md').read_text())

    def test_portal_sites(self):
        doc = page('/portal/console/sites/')
        for anchor in ('the-list', 'make-a-site', 'change-a-sites-settings', 'when-a-save-is-refused'):
            self.assertIn(f'id="{anchor}"', doc)
        for shot in ('portal-sites-list', 'portal-site-new', 'portal-site-settings', 'portal-site-settings-seo'):
            self.assertIn(shot, (PORTAL / 'console/sites.md').read_text())
        self.assertIn('href="/portal/console/sites/"', page('/portal/quickstart/'))
        self.assertIn('href="/portal/console/sites/"', page('/portal/console/pages/'))
        self.assertIn('href="/portal/console/sites/#change-a-sites-settings"', page('/portal/sites/seo/'))
        self.assertIn('href="/portal/console/sites/#change-a-sites-settings"', page('/portal/console/invitations/'))
        source = (PORTAL / 'console/sites.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'YAML', 'yaml', 'site.yaml'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_content(self):
        doc = page('/portal/console/content/')
        for anchor in ('overview', 'find-an-entry', 'write-an-entry', 'categories-and-tags', 'publish', 'history', 'when-someone-else-is-editing', 'show-content-on-a-page'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/content/#show-content-on-a-page"', page('/portal/console/pages/'))
        self.assertIn('href="/portal/sites/content-types/#libraries"', doc)
        self.assertIn('href="/portal/sites/assistants/#suggest-tags-for-content"', doc)
        source = (ROOT / 'src/content/docs/portal/console/content.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'YAML', 'yaml'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)
        types = page('/portal/sites/content-types/')
        for anchor in ('what-people-see', 'a-content-type', 'field-types', 'how-an-entry-looks', 'vocabularies', 'libraries', 'collections', 'reading-a-collection', 'show-it-on-a-page'):
            self.assertIn(f'id="{anchor}"', types)
        self.assertIn('href="/portal/console/content/"', types)
        source = (ROOT / 'src/content/docs/portal/sites/content-types.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'repositor', 'Hub'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_content_type_builder(self):
        doc = page('/portal/console/content-types/')
        for anchor in ('the-list', 'build-a-content-type', 'change-a-content-type', 'remove-a-content-type'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/content-types/"', page('/portal/console/content/'))
        self.assertIn('href="/portal/console/content-types/"', page('/portal/sites/content-types/'))
        source = (ROOT / 'src/content/docs/portal/console/content-types.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'YAML', 'yaml'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_files(self):
        doc = page('/portal/console/files/')
        for anchor in ('what-people-see', 'folders', 'upload-a-file', 'link-to-a-file', 'remove-a-file'):
            self.assertIn(f'id="{anchor}"', doc)
        source = (ROOT / 'src/content/docs/portal/console/files.md').read_text()
        # Where the portal keeps its own files is never said; S3-compatible buckets are a feature people use.
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)
        self.assertNotIn('kept by the portal itself, on', source)

    def test_portal_display_pages(self):
        doc = page('/portal/console/pages/')
        self.assertIn('id="display-pages"', doc)
        types = page('/portal/sites/content-types/')
        self.assertIn('id="display-pages"', types)
        self.assertIn('href="/portal/console/pages/#display-pages"', types)
        for path in ('src/content/docs/portal/console/pages.md', 'src/content/docs/portal/sites/content-types.md'):
            source = (ROOT / path).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_search(self):
        doc = page('/portal/sites/search/')
        for anchor in ('what-people-see', 'what-search-finds', 'how-words-match', 'who-finds-what', 'put-a-search-box-on-a-page', 'suggestions-while-typing', 'documents-in-the-dms', 'from-an-app'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="search"', page('/portal/console/pages/'))
        self.assertIn('href="/portal/sites/search/"', page('/portal/console/pages/'))
        source = (ROOT / 'src/content/docs/portal/sites/search.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'OpenSearch', 'index'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_forms(self):
        guide = page('/portal/sites/forms/')
        for anchor in ('what-people-see', 'write-a-form', 'what-a-form-may-hold', 'translations', 'who-sends-it-and-who-reads-what-was-sent',
                       'put-a-form-on-a-page', 'its-own-address', 'what-the-portal-checks', 'from-an-app',
                       'come-back-to-a-form', 'ask-for-consent', 'tell-the-reviewers', 'keep-submissions-for-a-time',
                       'fill-in-a-form-offline', 'fields-from-apps'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('id="a-forms-file"', page('/portal/developer/forms/'))
        console = page('/portal/console/forms/')
        for anchor in ('what-the-list-shows', 'read-a-submission', 'report', 'export', 'delete', 'build-a-form'):
            self.assertIn(f'id="{anchor}"', console)
        self.assertIn('href="/portal/sites/forms/"', console)
        self.assertIn('id="forms"', page('/portal/console/pages/'))
        self.assertIn('href="/portal/console/forms/#build-a-form"', guide)
        self.assertIn('id="form-fields-and-options"', page('/portal/developer/build-an-app/'))
        for anchor in ('actions', 'connector-types', 'start-jobs'):
            self.assertIn(f'id="{anchor}"', page('/portal/developer/build-an-app/'))
        self.assertIn('id="app-actions"', page('/portal/sites/actions/'))
        for path in ('src/content/docs/portal/sites/forms.md', 'src/content/docs/portal/console/forms.md'):
            source = (ROOT / path).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'MongoDB', 'Postgres', 'SMTP', 'outbox', 'IndexedDB', 'service worker'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_actions(self):
        doc = page('/portal/sites/actions/')
        for anchor in ('what-people-see', 'an-action-list', 'expressions', 'the-actions', 'ask-an-agent', 'when-something-fails'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="after-it-is-sent"', page('/portal/sites/forms/'))
        self.assertIn('id="runs"', page('/portal/console/forms/'))
        source = (ROOT / 'src/content/docs/portal/sites/actions.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_flows_and_values(self):
        doc = page('/portal/sites/flows/')
        for anchor in ('what-people-see', 'a-flow', 'call-a-flow', 'contracts', 'tests'):
            self.assertIn(f'id="{anchor}"', doc)
        values = page('/portal/sites/values/')
        for anchor in ('what-people-see', 'a-value', 'how-long-it-is-kept', 'when-a-value-fails'):
            self.assertIn(f'id="{anchor}"', values)
        self.assertIn('id="run-tests"', page('/portal/console/flows/'))
        self.assertIn('href="/portal/sites/flows/#call-a-flow"', page('/portal/sites/actions/'))
        for path in ('sites/flows.md', 'sites/values.md', 'console/flows.md'):
            source = (ROOT / 'src/content/docs/portal' / path).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'index', 'repositor', 'store'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_connectors(self):
        doc = page('/portal/sites/connectors/')
        for anchor in ('what-people-see', 'a-connector', 'credentials', 'call-a-service', 'email',
                       'hashes-signatures-and-random-values', 'mailboxes', 'each-persons-own-account', 'in-tests'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="a-connectors-file"', page('/portal/developer/connectors/'))
        for anchor in ('set-credentials', 'test'):
            self.assertIn(f'id="{anchor}"', page('/portal/console/connectors/'))
        self.assertIn('id="your-connections"', page('/portal/console/account/'))
        self.assertIn('href="/portal/sites/connectors/#call-a-service"', page('/portal/sites/actions/'))
        for path in ('sites/connectors.md', 'console/connectors.md'):
            source = (ROOT / 'src/content/docs/portal' / path).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'index', 'repositor', 'store', 'Vault'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_file_actions(self):
        doc = page('/portal/sites/actions/')
        self.assertIn('id="files"', doc)
        values = (ROOT / 'src/content/docs/portal/developer/values.md').read_text()
        for kind in ('`http`', '`collection`'):
            self.assertIn(kind, values)
        self.assertIn('files: {', (ROOT / 'src/content/docs/portal/developer/flows.md').read_text())
        source = (ROOT / 'src/content/docs/portal/sites/actions.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_pages_show_the_ui(self):
        # A site page shows how it works in the portal, with screenshots.
        pages = [('sites', name) for name in UI_FIRST_PAGES] + [('console', name) for name in CONSOLE_PAGES]
        for folder, name in pages:
            path = PORTAL / folder / name
            images = re.findall(r'!\[([^\]]+)\]\(([^)]+\.png)\)', path.read_text())
            self.assertTrue(images, name)
            for alt, src in images:
                self.assertTrue((path.parent / src).resolve().is_file(), (name, src))
                self.assertGreater(len(alt), 20, (name, src))

    def test_portal_user_pages_hold_no_config(self):
        # Config files are the developers' path: their examples live under Developer, never in the user guide.
        for folder in ('sites', 'console'):
            for path in sorted((PORTAL / folder).glob('*.md')):
                name = f'{folder}/{path.name}'
                source = path.read_text()
                fences = re.findall(r'^\s*```(\S*)', source, re.M)[::2]
                allowed = TYPED_IN_THE_CONSOLE.get(name)
                self.assertEqual([f for f in fences if f != allowed], [], name)
                self.assertNotIn('## Config example', source, name)
                self.assertNotIn('config example', source.lower(), name)

    def test_portal_developer_pages(self):
        # Each developer page is the config of a user page, links back to it, and is linked from it.
        index = page('/portal/developer/')
        for anchor in ('the-files', 'pull-and-push', 'other-ways-in'):
            self.assertIn(f'id="{anchor}"', index)
        for word in ('portal config pull', 'portal config push', '--onto-latest'):
            self.assertIn(word, index)
        for path in sorted((PORTAL / 'developer').glob('*.md')):
            source = path.read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'Open Design'):
                self.assertNotIn(word, source, path.name)
            if path.name in DEVELOPER_ONLY:
                continue
            folder = 'console' if (PORTAL / 'console' / path.name).is_file() and not (PORTAL / 'sites' / path.name).is_file() else 'sites'
            user = f'/portal/{folder}/{path.stem}/'
            self.assertIn(f'href="{user}"', page(f'/portal/developer/{path.stem}/'), path.name)
            self.assertIn(f'href="/portal/developer/{path.stem}/', page(user), path.name)
            self.assertIn('```', source, path.name)

    def test_portal_moved_developer_pages_redirect(self):
        for name in ('build-an-app', 'develop-locally', 'check-a-site', 'previews', 'design', 'agents'):
            self.assertFalse((PORTAL / 'sites' / f'{name}.md').exists(), name)
            self.assertIn(f'/portal/developer/{name}/', page(f'/portal/sites/{name}/'), name)

    def test_portal_guides(self):
        doc = page('/portal/sites/guides/')
        for anchor in ('what-people-see', 'start-a-guide', 'in-the-console'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="ui-actions"', page('/portal/sites/actions/'))
        self.assertIn('href="/portal/sites/guides/"', page('/portal/console/guides/'))
        for path in ('sites/guides.md', 'console/guides.md'):
            source = (ROOT / 'src/content/docs/portal' / path).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'index', 'repositor', 'localStorage'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_data_models(self):
        doc = page('/portal/sites/data-models/')
        for anchor in ('what-people-see', 'a-model', 'fields', 'who-may-do-what', 'when-the-file-changes', 'the-api', 'graphql', 'relations'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="records"', page('/portal/sites/actions/'))
        self.assertIn('href="/portal/sites/data-models/"', page('/portal/console/data/'))
        for path in ('sites/data-models.md', 'console/data.md'):
            source = (ROOT / 'src/content/docs/portal' / path).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'schema'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_data_console(self):
        doc = page('/portal/console/data-console/')
        for anchor in ('what-you-see', 'turn-it-on', 'what-a-query-may-read', 'download-and-keep', 'who-may-use-it'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/data-console/"', page('/portal/console/data/'))
        source = (ROOT / 'src/content/docs/portal/console/data-console.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'schema', 'role'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_pick_a_record(self):
        self.assertIn('id="pick-a-record"', page('/portal/sites/forms/'))
        self.assertIn('href="/portal/sites/forms/#pick-a-record"', page('/portal/sites/listings/'))
        source = (ROOT / 'src/content/docs/portal/sites/listings.md').read_text()
        self.assertNotIn('links are not edited there', source)

    def test_portal_jobs(self):
        doc = page('/portal/sites/jobs/')
        for anchor in ('write-a-job', 'when-it-runs', 'when-records-change', 'when-people-come-and-go', 'when-the-portal-starts-fails-or-is-asked-for', 'when-mail-arrives', 'when-an-app-sends-an-event', 'send-mail', 'what-it-may-do', 'in-the-console'):
            self.assertIn(f'id="{anchor}"', doc)
        source = (ROOT / 'src/content/docs/portal/sites/jobs.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'lease', 'CEL'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_endpoints(self):
        doc = page('/portal/sites/endpoints/')
        for anchor in ('what-people-see', 'write-an-endpoint', 'parameters', 'its-actions-and-its-answer', 'who-may-call-it', 'keep-answers-and-other-sites', 'private-endpoints', 'its-calls'):
            self.assertIn(f'id="{anchor}"', doc)
        source = (ROOT / 'src/content/docs/portal/sites/endpoints.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'CEL'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_keel(self):
        doc = page('/portal/sites/keel/')
        for anchor in ('what-people-see', 'connect-keel', 'my-work', 'the-overview', 'start-cases-from-the-portal', 'when-something-happens-in-keel'):
            self.assertIn(f'id="{anchor}"', doc)
        source = (ROOT / 'src/content/docs/portal/sites/keel.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'JWT', 'token'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_assistants(self):
        doc = page('/portal/sites/assistants/')
        for anchor in ('connect-your-agents', 'what-people-see', 'who-the-agent-talks-with', 'a-chat-for-visitors', 'help-in-the-console', 'describe-a-change', 'suggest-tags-for-content', 'give-an-agent-the-portal-as-a-tool'):
            self.assertIn(f'id="{anchor}"', doc)
        for anchor in ('the-agent-and-its-key', 'the-assistant-on-a-page', 'the-chat-for-visitors', 'the-consoles-agents'):
            self.assertIn(f'id="{anchor}"', page('/portal/developer/assistants/'))
        self.assertIn('href="/portal/sites/assistants/"', page('/portal/sites/documents/'))
        source = (ROOT / 'src/content/docs/portal/sites/assistants.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'JWT', 'iframe', 'SSE', 'end_user', 'inject'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_documents(self):
        doc = page('/portal/sites/documents/')
        for anchor in ('what-people-see', 'connect-the-dms', 'show-a-folder', 'file-documents-from-a-page', 'show-one-document', 'add-a-version', 'search-the-dms-from-the-portal', 'downloads', 'when-something-happens-in-the-dms'):
            self.assertIn(f'id="{anchor}"', doc)
        source = (ROOT / 'src/content/docs/portal/sites/documents.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'JWT', 'token'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_kpis(self):
        doc = page('/portal/sites/kpis/')
        for anchor in ('what-people-see', 'declare-them', 'show-them', 'what-each-person-sees'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/kpis/"', page('/portal/sites/data-models/'))
        source = (ROOT / 'src/content/docs/portal/sites/kpis.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'SQL', 'cache'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_listings(self):
        doc = page('/portal/sites/listings/')
        for anchor in ('what-people-see', 'place-a-listing', 'what-each-person-sees', 'a-models-own-pages-and-form'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/listings/"', page('/portal/sites/data-models/'))
        source = (ROOT / 'src/content/docs/portal/sites/listings.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'worker', 'Postgres', 'repositor', 'csrf', 'CDN'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_files_kept_by_the_portal(self):
        for path in ('src/content/docs/portal/console/tenants.md', 'src/content/docs/portal/developer/previews.md',
                     'src/content/docs/portal/developer/design.md'):
            source = (ROOT / path).read_text()
            for word in ('git', 'Git', 'repositor', 'branch'):
                self.assertIsNone(re.search(rf'\b{word}', source), (path, word))

    def test_portal_search_settings(self):
        doc = page('/portal/console/search/')
        for anchor in ('weights', 'synonyms', 'pinned-results', 'what-search-leaves-out', 'typos-and-word-starts', 'what-people-search-for'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="tune-search"', page('/portal/sites/search/'))
        source = (ROOT / 'src/content/docs/portal/console/search.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub', 'OpenSearch', 'index', 'repositor'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_seo(self):
        doc = page('/portal/sites/seo/')
        for anchor in ('what-people-see', 'what-each-page-says', 'describe-a-page', 'describe-a-site', 'what-crawlers-are-told'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/seo/"', page('/portal/console/pages/'))
        source = (ROOT / 'src/content/docs/portal/sites/seo.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'Hub'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_proposals(self):
        doc = page('/portal/console/proposals/')
        for anchor in ('what-may-be-proposed', 'the-list', 'read-a-proposal', 'preview-a-proposal', 'approve-or-reject', 'for-agents-and-developers'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/proposals/"', page('/portal/console/tokens/'))
        self.assertIn('href="/portal/sites/assistants/#describe-a-change"', doc)
        source = (ROOT / 'src/content/docs/portal/console/proposals.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub'):
            self.assertNotIn(word, source)

    def test_portal_versions(self):
        doc = page('/portal/console/versions/')
        for anchor in ('what-the-list-shows', 'see-what-a-version-changed', 'compare-with-the-live-version', 'undo-a-change', 'go-back-to-a-version', 'send-a-version-to-another-environment'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/versions/"', page('/portal/console/tenants/'))
        self.assertIn('id="kept-by-the-portal"', page('/portal/console/tenants/'))
        # The page's own words: what a tenant administrator reads never names the store behind it.
        source = (ROOT / 'src/content/docs/portal/console/versions.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub'):
            self.assertNotIn(word, source)

    def test_portal_environments(self):
        doc = page('/portal/sites/environments/')
        for anchor in ('what-people-see', 'what-travels', 'name-the-environments', 'make-the-key', 'send-a-version'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/environments/"', page('/portal/console/versions/'))
        source = (ROOT / 'src/content/docs/portal/sites/environments.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'git', 'Git', 'commit', 'branch', 'repositor', 'Hub', 'pat_'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_notifications(self):
        doc = page('/portal/sites/notifications/')
        for anchor in ('where-people-find-them', 'send-one'):
            self.assertIn(f'id="{anchor}"', doc)
        for anchor in ('a-forms-message-to-the-clerks', 'an-agents-answer-as-a-notification', 'the-widget-on-a-page'):
            self.assertIn(f'id="{anchor}"', page('/portal/developer/notifications/'))
        self.assertIn('href="/portal/sites/notifications/"', page('/portal/sites/actions/'))
        self.assertIn('id="notifications"', page('/portal/console/account/'))
        source = (ROOT / 'src/content/docs/portal/sites/notifications.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'outbox', 'vaul'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_comments(self):
        doc = page('/portal/sites/comments/')
        for anchor in ('what-people-see', 'place-the-widgets', 'write-and-answer', 'delete-and-flag', 'rate', 'limits', 'what-happens-to-them-later'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/moderation/"', doc)
        console = page('/portal/console/moderation/')
        for anchor in ('who-moderates', 'decide-on-a-comment'):
            self.assertIn(f'id="{anchor}"', console)
        self.assertIn('href="/portal/sites/comments/#delete-and-flag"', console)
        for name in ('sites/comments.md', 'console/moderation.md'):
            source = (ROOT / 'src/content/docs/portal' / name).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'subject'):
                self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_activity(self):
        doc = page('/portal/sites/activity/')
        for anchor in ('what-people-see', 'posts', 'comments-and-entries', 'who-is-told-what'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="the-widget-on-a-page"', page('/portal/developer/activity/'))
        self.assertIn('href="/portal/sites/comments/#name-someone"', doc)
        comments = page('/portal/sites/comments/')
        self.assertIn('id="name-someone"', comments)
        self.assertIn('href="/portal/console/users/#handle"', comments)
        self.assertIn('id="handle"', page('/portal/console/users/'))
        for name in ('sites/activity.md', 'sites/comments.md'):
            source = (ROOT / 'src/content/docs/portal' / name).read_text()
            for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'subject', 'stream:'):
                self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_blogs(self):
        doc = page('/portal/sites/blogs/')
        for anchor in ('what-people-see', 'make-a-blog-type', 'name-the-bloggers', 'show-a-blog', 'show-several-blogs', 'recent-bloggers', 'who-sees-what'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/permissions/#bloggers"', doc)
        self.assertIn('id="bloggers"', page('/portal/sites/permissions/'))
        self.assertIn('href="/portal/sites/blogs/#name-the-bloggers"', page('/portal/console/content/'))
        self.assertIn('href="/portal/sites/blogs/"', page('/portal/sites/content-types/'))
        source = (ROOT / 'src/content/docs/portal/sites/blogs.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'created_by', 'content_entries'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_forums(self):
        doc = page('/portal/sites/forums/')
        for anchor in ('what-people-see', 'place-a-forum', 'topics-and-answers', 'questions-and-answers', 'moderate-a-forum', 'limits'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/console/moderation/#who-moderates"', doc)
        self.assertIn('href="/portal/sites/comments/#name-someone"', doc)
        source = (ROOT / 'src/content/docs/portal/sites/forums.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'subject', 'p_'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_wiki(self):
        doc = page('/portal/sites/wiki/')
        for anchor in ('what-people-see', 'place-a-wiki', 'read-and-find', 'write', 'look-after-a-wiki', 'knowledge-bases', 'what-happens-to-them-later'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('href="/portal/sites/permissions/"', doc)
        source = (ROOT / 'src/content/docs/portal/sites/wiki.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'p_w_'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_calendar(self):
        doc = page('/portal/sites/calendar/')
        for anchor in ('what-people-see', 'read-it', 'add-events', 'add-it-to-a-calendar-app', 'what-happens-to-them-later'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="a-calendar-on-a-page"', page('/portal/developer/calendar/'))
        self.assertIn('href="/portal/sites/permissions/"', doc)
        self.assertIn('href="/portal/sites/calendar/"', page('/portal/sites/wiki/'))
        for label in ('Bring back', 'Discard the draft', 'Subscribe (iCal)', 'Share by a private address'):
            self.assertIn(label, doc)
        source = (ROOT / 'src/content/docs/portal/sites/calendar.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'p_events_', 'token'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_announcements(self):
        doc = page('/portal/sites/announcements/')
        for anchor in ('what-people-see', 'write-an-announcement', 'tell-them', 'read-and-dismiss', 'what-happens-to-them-later'):
            self.assertIn(f'id="{anchor}"', doc)
        self.assertIn('id="the-widget-on-a-page"', page('/portal/developer/announcements/'))
        for label in ('New announcement', 'Manage announcements', 'Tell them by a notification', 'Dismiss'):
            self.assertIn(label, doc)
        source = (ROOT / 'src/content/docs/portal/sites/announcements.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'p_notices_'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_polls(self):
        doc = page('/portal/sites/polls/')
        for anchor in ('what-people-see', 'place-a-poll', 'open-a-poll', 'vote', 'results', 'what-happens-to-them-later'):
            self.assertIn(f'id="{anchor}"', doc)
        for label in ('New poll', 'Change my vote', 'Past polls', 'Close the poll'):
            self.assertIn(label, doc)
        source = (ROOT / 'src/content/docs/portal/sites/polls.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'p_question_'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_invitations(self):
        doc = page('/portal/console/invitations/')
        for anchor in ('invite-people', 'what-the-person-sees', 'follow-your-invitations', 'let-a-sites-editors-invite', 'what-happens-to-them-later'):
            self.assertIn(f'id="{anchor}"', doc)
        for label in ('Send invitations', 'Accept the invitation', 'Sign in to accept', 'Make my account and accept', 'Send again', 'Withdraw'):
            self.assertIn(label, doc)
        self.assertIn('href="/portal/console/invitations/"', page('/portal/console/users/'))
        source = (ROOT / 'src/content/docs/portal/console/invitations.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Postgres', 'token'):
            self.assertIsNone(re.search(rf'\b{word}', source), word)

    def test_portal_push_notifications(self):
        doc = page('/portal/console/account/')
        self.assertIn('id="notifications-in-this-browser"', doc)
        for label in ('Turn on', 'Turn off', 'Remove'):
            self.assertIn(label, doc)
        self.assertIn('href="/portal/console/account/#notifications-in-this-browser"', page('/portal/sites/notifications/'))

    def test_portal_document_actions(self):
        guide = page('/portal/sites/document-actions/')
        for anchor in ('what-people-get', 'make-a-pdf-from-html', 'work-with-pdfs', 'fill-a-word-template', 'excel-and-csv', 'barcodes-and-qr-codes', 'who-may-do-what', 'limits'):
            self.assertIn(f'id="{anchor}"', guide)
        developer = page('/portal/developer/document-actions/')
        for action in ('htmlToPdf', 'htmlToWord', 'convertToPdf', 'mergePdfs', 'overlayPdf', 'splitPdf', 'readPdf', 'fillWordTemplate', 'readWord', 'writeExcel', 'readExcel', 'excelSheets', 'writeCsv', 'readCsv', 'barcode'):
            self.assertIn(action, developer)
        self.assertIn('href="/portal/sites/document-actions/"', page('/portal/sites/actions/'))
        source = (ROOT / 'src/content/docs/portal/sites/document-actions.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Euro-Office', 'Open Design'):
            self.assertNotIn(word, source)

    def test_portal_file_management(self):
        guide = page('/portal/sites/file-management/')
        for anchor in ('what-people-get', 'copy-move-and-rename-a-file', 'read-a-files-details', 'zip-archives', 'images', 'files-on-a-server', 'who-may-do-what', 'limits'):
            self.assertIn(f'id="{anchor}"', guide)
        developer = page('/portal/developer/file-management/')
        for action in ('copyFile', 'moveFile', 'renameFile', 'fileInfo', 'zipFiles', 'zipNames', 'unzipFile', 'replace: true', 'resizeImage', 'imageInfo', 'ftpUpload', 'ftpDownload', 'ftpList', 'ftpDelete'):
            self.assertIn(action, developer)
        self.assertIn('href="/portal/sites/file-management/"', page('/portal/sites/actions/'))
        self.assertIn('id="file-servers"', page('/portal/sites/connectors/'))
        self.assertIn('id="a-file-servers-file"', page('/portal/developer/connectors/'))
        self.assertIn('href="/portal/sites/connectors/#file-servers"', guide)
        files = page('/portal/console/files/')
        self.assertIn('id="move-or-copy-a-file"', files)
        self.assertIn('id="images-at-a-width"', files)
        self.assertIn('href="/portal/sites/file-management/"', files)
        source = (ROOT / 'src/content/docs/portal/sites/file-management.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'Hub', 'fflate', 'Open Design'):
            self.assertNotIn(word, source)

    def test_portal_mail_accounts(self):
        guide = page('/portal/sites/connectors/')
        developer = page('/portal/developer/connectors/')
        self.assertIn('id="mail-accounts"', guide)
        self.assertIn('id="a-mail-accounts-file"', developer)
        for word in ('Mail.Send', 'gmail.send'):
            self.assertIn(word, guide)
        for word in ('microsoft365', 'attachments'):
            self.assertIn(word, developer)
        self.assertIn('href="/portal/sites/connectors/#mail-accounts"', page('/portal/sites/actions/'))

    def test_portal_sms_and_slack(self):
        guide = page('/portal/sites/connectors/')
        developer = page('/portal/developer/connectors/')
        for anchor in ('text-messages-and-slack', 'messaging-accounts'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('id="a-text-message-and-a-slack-post"', developer)
        for word in ('sendSms', 'slackMessage', 'hooks.slack.com', 'clickatell'):
            self.assertIn(word, developer)
        self.assertIn('href="/portal/sites/connectors/#text-messages-and-slack"', page('/portal/sites/actions/'))

    def test_portal_form_fields(self):
        guide = page('/portal/sites/form-fields/')
        for anchor in ('what-people-see', 'a-barcode-or-qr-code', 'a-barcode-scanner', 'an-iban', 'a-signature', 'in-the-console', 'save-a-signature-as-a-file'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('90 KB', guide)
        for word in ('barcodeScanner', 'countries', 'encoding: dataUrl'):
            self.assertIn(word, page('/portal/developer/form-fields/'))
        self.assertIn('href="/portal/sites/form-fields/"', page('/portal/sites/forms/'))
        self.assertIn('href="/portal/sites/form-fields/#save-a-signature-as-a-file"', page('/portal/sites/actions/'))
        source = (ROOT / 'src/content/docs/portal/sites/form-fields.md').read_text()
        for word in ('kubectl', 'helm', 'PORTAL_', 'bwip', 'zxing', 'Open Design'):
            self.assertNotIn(word, source)

    def test_portal_bucket_folders(self):
        files = page('/portal/console/files/')
        self.assertIn('id="where-files-are-kept"', files)
        self.assertIn('id="a-folder-kept-in-a-bucket"', page('/portal/developer/files/'))
        self.assertIn('storage:', page('/portal/developer/files/'))
        self.assertIn('href="/portal/sites/connectors/#buckets"', files)
        connectors = page('/portal/sites/connectors/')
        self.assertIn('id="buckets"', connectors)
        self.assertIn('id="a-buckets-file"', page('/portal/developer/connectors/'))
        self.assertIn('kind: bucket', page('/portal/developer/connectors/'))
        for word in ('kubectl', 'helm', 'PORTAL_', 'Open Design', 'Signature V4'):
            self.assertNotIn(word, files + connectors)

    def test_portal_previews(self):
        guide = page('/portal/developer/previews/')
        for anchor in ('what-people-see', 'config-example', 'make-a-preview', 'its-people', 'see-it-as-one-of-its-people', 'sync-it-again', 'its-apps', 'when-it-ends', 'who-may-make-previews'):
            self.assertIn(f'id="{anchor}"', guide)
        self.assertIn('manager@preview.example', guide)
        self.assertIn('href="/portal/developer/previews/"', page('/portal/developer/agents/'))
        self.assertIn('href="/portal/developer/previews/"', page('/portal/console/tokens/'))
        for word in ('kubectl', 'helm', 'PORTAL_'):
            self.assertNotIn(word, guide)

    def test_portal_events(self):
        doc = page('/portal/console/events/')
        self.assertIn('<figcaption>The Events page', doc)
        self.assertIn('id="webhooks"', doc)
        guide = page('/portal/sites/apps/')
        self.assertIn('id="events"', guide)
        self.assertIn('portal-event+jwt', page('/portal/developer/apps/'))
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
        self.assertIn('portal-request+jwt', page('/portal/developer/apps/'))
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

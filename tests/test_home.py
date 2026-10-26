import re
import unittest

from docsite import DIST, page, section

TASKS = [
    ('Deploy a customer-support agent in 10 minutes', '/work/use-cases/#1-deploy-a-customer-support-bot-in-10-minutes'),
    ('Add Slack so your team can chat with the same agent', '/work/use-cases/#2-add-slack-so-your-team-can-chat-with-the-same-agent'),
    ('Build a knowledge base from your wiki and tickets', '/work/use-cases/#4-build-a-product-knowledge-base-from-internal-wiki--tickets'),
    ('Fine-tune an expert from your agent', '/develop/use-cases/#1-fine-tune-an-expert-from-your-traffic'),
    ('Run batch jobs through the API', '/develop/use-cases/#6-integrate-via-the-api-channel-for-batch-jobs'),
    ('Build a loan request and work your first case', '/keel/quickstart/'),
    ('Route cases by amount with a decision table', '/keel/builder/rules/'),
    ('Give a team a queue with a serving order', '/keel/builder/queues/'),
    ('Let an agent work a step and ask when unsure', '/keel/business/agents/'),
    ('Test a case type with scenarios before you publish', '/keel/builder/scenarios/'),
]


class Home(unittest.TestCase):
    def setUp(self):
        self.doc = page('/')

    def test_hero(self):
        self.assertIn('Surogate documentation', self.doc)
        self.assertIn('Guides, tutorials and reference for Surogate Agents and Keel.', self.doc)

    def test_product_cards(self):
        self.assertEqual(self.doc.count('data-docs="product-card"'), 2)
        self.assertIn('Two products, built to work together.', self.doc)
        for href in ('href="/work/"', 'href="/work/quickstart/"', 'href="/keel/"', 'href="/keel/quickstart/"'):
            self.assertIn(href, self.doc)

    def test_tasks_link_to_real_sections(self):
        for title, href in TASKS:
            self.assertRegex(self.doc, rf'href="{re.escape(href)}"[^>]*>[\s\S]*?{re.escape(title)}')
            path, _, anchor = href.partition('#')
            if anchor:
                self.assertIn(f'id="{anchor}"', page(path))

    def test_help_band(self):
        band = section(self.doc, 'help-band')
        self.assertIn('surogate@invergent.ai', band)
        self.assertIn('href="/work/whats-new/"', band)
        self.assertNotIn('API reference', band)

    def test_old_home_is_gone(self):
        for old in ('Multiply yourself', 'Vibecode', 'The improvement loop'):
            self.assertNotIn(old, self.doc)


if __name__ == '__main__':
    unittest.main()

import unittest

from codemod import (
    SLUG_OVERRIDES,
    drop_frontmatter_key,
    fence_states,
    rewrite_links,
    strip_leading_h1,
)


class TestFenceStates(unittest.TestCase):
    def test_marks_lines_inside_backtick_fence(self):
        lines = ['text', '```bash', '# a comment', '```', 'more']
        self.assertEqual(fence_states(lines), [False, True, True, True, False])

    def test_handles_tilde_fence(self):
        lines = ['~~~', '# inside', '~~~', '# outside']
        self.assertEqual(fence_states(lines), [True, True, True, False])

    def test_longer_closer_required_for_longer_opener(self):
        # A 3-backtick line does not close a 4-backtick fence.
        lines = ['````', '```', '# still inside', '````', 'out']
        self.assertEqual(fence_states(lines), [True, True, True, True, False])

    def test_language_tag_does_not_close_fence(self):
        lines = ['```python', '# comment', '```']
        self.assertEqual(fence_states(lines), [True, True, True])


class TestStripLeadingH1(unittest.TestCase):
    def test_removes_first_h1_and_reports_text(self):
        body = '\n# Slack channel\n\nSome prose.\n'
        new, removed = strip_leading_h1(body)
        self.assertEqual(removed, 'Slack channel')
        self.assertNotIn('# Slack channel', new)
        self.assertIn('Some prose.', new)

    def test_preserves_hash_comments_inside_code_fences(self):
        body = (
            '\n# Observe phase\n\n'
            '```bash\n'
            '# List sessions matching filters\n'
            'curl /api/sessions\n'
            '```\n'
        )
        new, removed = strip_leading_h1(body)
        self.assertEqual(removed, 'Observe phase')
        self.assertIn('# List sessions matching filters', new)

    def test_does_not_touch_a_second_h1(self):
        # skills-and-experts.md has two real H1s; only the first is the
        # title duplicate. The second is demoted by hand, not here.
        body = '\n# Skills & Tools\n\nprose\n\n# Experts\n\nmore\n'
        new, removed = strip_leading_h1(body)
        self.assertEqual(removed, 'Skills & Tools')
        self.assertIn('# Experts', new)

    def test_returns_none_when_no_h1(self):
        body = '\n## Only a subheading\n'
        new, removed = strip_leading_h1(body)
        self.assertIsNone(removed)
        self.assertEqual(new, body)

    def test_ignores_an_h1_that_only_exists_inside_a_fence(self):
        body = '\nprose\n\n```bash\n# not a heading\n```\n'
        new, removed = strip_leading_h1(body)
        self.assertIsNone(removed)
        self.assertIn('# not a heading', new)


class TestDropFrontmatterKey(unittest.TestCase):
    def test_removes_the_key_line(self):
        fm = 'title: Slack\nsidebar_position: 2\n'
        self.assertEqual(drop_frontmatter_key(fm, 'sidebar_position'), 'title: Slack')

    def test_leaves_other_keys_untouched(self):
        fm = 'title: Slack\ndraft: true\n'
        self.assertEqual(drop_frontmatter_key(fm, 'sidebar_position'), fm.rstrip('\n'))


class TestRewriteLinks(unittest.TestCase):
    def test_sibling_link(self):
        out, n = rewrite_links('See [chat](./chat.md).', 'work/tools/commands')
        self.assertEqual(out, 'See [chat](/work/tools/chat/).')
        self.assertEqual(n, 1)

    def test_parent_relative_link(self):
        out, n = rewrite_links('[skills](../library/skills.md)', 'work/tools/chat')
        self.assertEqual(out, '[skills](/work/library/skills/)')

    def test_cross_tree_link(self):
        out, n = rewrite_links(
            '[agents](../../develop/features/agents.md)', 'work/tools/chat'
        )
        self.assertEqual(out, '[agents](/develop/features/agents/)')

    def test_preserves_anchor(self):
        out, n = rewrite_links('[x](./chat.md#history)', 'work/tools/commands')
        self.assertEqual(out, '[x](/work/tools/chat/#history)')

    def test_applies_slug_override(self):
        out, n = rewrite_links('[home](../intro.md)', 'work/tools/chat')
        self.assertEqual(out, '[home](/work/)')

    def test_leaves_external_links_alone(self):
        src = '[x](https://example.com/a.md)'
        out, n = rewrite_links(src, 'work/intro')
        self.assertEqual(out, src)
        self.assertEqual(n, 0)

    def test_leaves_anchor_only_links_alone(self):
        src = '[x](#section)'
        out, n = rewrite_links(src, 'work/intro')
        self.assertEqual(out, src)
        self.assertEqual(n, 0)

    def test_leaves_root_absolute_links_alone(self):
        src = '[x](/develop/features/mcp-and-vault)'
        out, n = rewrite_links(src, 'work/library/mcp-servers')
        self.assertEqual(out, src)
        self.assertEqual(n, 0)

    def test_does_not_rewrite_inside_code_fence(self):
        body = '```markdown\n[x](./chat.md)\n```\n'
        out, n = rewrite_links(body, 'work/tools/commands')
        self.assertEqual(out, body)
        self.assertEqual(n, 0)

    def test_rewrites_two_links_on_one_line(self):
        out, n = rewrite_links(
            '[a](./chat.md) and [b](./commands.md)', 'work/tools/goals'
        )
        self.assertEqual(out, '[a](/work/tools/chat/) and [b](/work/tools/commands/)')
        self.assertEqual(n, 2)


class TestSlugOverrides(unittest.TestCase):
    def test_exactly_two_overrides(self):
        self.assertEqual(
            SLUG_OVERRIDES, {'work/intro': 'work', 'develop/intro': 'develop'}
        )


if __name__ == '__main__':
    unittest.main()

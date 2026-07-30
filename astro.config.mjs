import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// NOTE: `trailingSlash` and `build.format` are deliberately unset. Astro's
// defaults (directory format, trailing slash) are the only combination whose
// hrefs, canonical tags, sitemap entries and Pagefind results all agree on
// GitHub Pages. Setting `build.format: 'file'` bakes `.html` into every one of
// them. See specs/2026-07-30-docusaurus-to-starlight-design.md section 7.2.
export default defineConfig({
  site: 'https://docs.surogate.ai',
  integrations: [
    starlight({
      title: 'Surogate',
      description: 'Documentation for Surogate Ops — operator and builder tracks.',
      logo: {
        light: './src/assets/logo-black.svg',
        dark: './src/assets/logo-white.svg',
        alt: 'Surogate',
        replacesTitle: false,
      },
      customCss: [
        // Self-hosted, replacing the render-blocking Google Fonts @import that
        // the old custom.css opened on every page load.
        '@fontsource/inter/400.css',
        '@fontsource/inter/600.css',
        './src/styles/custom.css',
      ],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/invergent-ai/surogate',
        },
        { icon: 'x.com', label: 'X', href: 'https://x.com/surogate_ai' },
      ],
      editLink: {
        baseUrl: 'https://github.com/invergent-ai/surogate-docs/edit/main/',
      },
      components: { SocialIcons: './src/components/HeaderLogin.astro' },
      // One sidebar, two sibling top-level groups. Order and category labels
      // are carried over from the deleted sidebars.js. Inner subgroups all
      // collapse by default: the two tracks now share a single column, so the
      // ~72 entries cannot all sit expanded as they did with three sidebars.
      sidebar: [
        {
          label: 'Work — for operators',
          items: [
            'work',
            'work/quickstart',
            {
              label: 'Agents',
              collapsed: true,
              items: [
                'work/workflow/run-agent',
                'work/workflow/configure-agent',
                'work/tools/chat',
                'work/tools/commands',
                'work/tools/goals',
                'work/tools/missions',
                'work/tools/scheduled-work',
                'work/tools/deep-research',
                'work/tools/code',
                'work/tools/sub-agents',
                'work/tools/inbox',
                'work/workflow/improve-agent',
              ],
            },
            'work/workflow/review-sessions',
            {
              label: 'Skills & Tools',
              collapsed: true,
              items: [
                'work/library/skills',
                'work/library/mcp-servers',
                'work/library/integrations',
                'work/workflow/templates',
              ],
            },
            'work/library/knowledge-bases',
            {
              label: 'Channels',
              collapsed: true,
              items: [
                'work/channels/web',
                'work/channels/slack',
                'work/channels/telegram',
                'work/channels/website-widget',
                'work/channels/users',
                'work/channels/self-registration',
                'work/channels/proactive',
              ],
            },
            {
              label: 'Settings',
              collapsed: true,
              items: [
                'work/settings/profile',
                'work/settings/settings',
                'work/settings/usage',
                'work/settings/billing',
              ],
            },
            'work/tools/copilot',
            'work/monetize',
            'work/use-cases',
            {
              label: 'Reference',
              collapsed: true,
              items: ['work/reference/glossary', 'work/reference/faq'],
            },
          ],
        },
        {
          label: 'Develop — for builders',
          items: [
            'develop',
            'develop/quickstart',
            {
              label: 'The builder loop',
              collapsed: true,
              items: [
                'develop/loop/overview',
                'develop/loop/build',
                'develop/loop/observe',
                'develop/loop/train',
                'develop/loop/redeploy',
              ],
            },
            'develop/tools/dashboard',
            // Surfaced for the first time: linked four times from prose and the
            // target of the /ops/features/agents redirect, but absent from
            // every Docusaurus sidebar.
            'develop/features/agents',
            'develop/features/sessions',
            'develop/features/models',
            'develop/features/playground',
            'develop/features/hub',
            'develop/features/datasets',
            'develop/features/training',
            'develop/features/evaluations',
            {
              label: 'Compute',
              collapsed: true,
              items: [
                'develop/features/compute',
                'develop/features/connect-compute',
              ],
            },
            {
              label: 'Skills & knowledge',
              collapsed: true,
              items: [
                'develop/features/skills-and-experts',
                'develop/features/skill-optimization',
                'develop/features/knowledge-bases',
                'develop/features/mcp-and-vault',
                'develop/features/byo-llm',
                {
                  slug: 'develop/features/experts-arenas',
                  badge: { text: 'Preview', variant: 'caution' },
                },
              ],
            },
            {
              label: 'Agent capabilities',
              collapsed: true,
              items: [
                'develop/features/memory',
                'develop/features/browser',
                'develop/features/browser-profiles',
              ],
            },
            {
              label: 'Tools',
              collapsed: true,
              items: ['develop/tools/copilot', 'develop/tools/templates'],
            },
            'develop/use-cases',
            {
              label: 'Reference',
              collapsed: true,
              items: [
                'develop/reference/runtime-architecture',
                'develop/reference/tool-catalog',
                'develop/reference/event-types',
                'develop/reference/background-jobs',
                'develop/reference/coordination',
                'develop/reference/glossary',
              ],
            },
          ],
        },
      ],
    }),
  ],
});

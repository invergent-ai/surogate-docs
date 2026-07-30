import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';

// NOTE: `trailingSlash` and `build.format` are deliberately unset. Astro's
// defaults (directory format, trailing slash) are the only combination whose
// hrefs, canonical tags, sitemap entries and Pagefind results all agree on
// GitHub Pages. Setting `build.format: 'file'` bakes `.html` into every one of
// them. See specs/2026-07-30-docusaurus-to-starlight-design.md section 7.2.
export default defineConfig({
  site: 'https://docs.surogate.ai',
  // 13 /ops/* entries ported verbatim from the deleted docusaurus.config.js,
  // plus /search -- which was a real page under Algolia and sits in today's
  // sitemap, but does not exist under Pagefind's modal-only search.
  //
  // All destinations carry trailing slashes so no visitor takes two hops.
  //
  // These must stay static literals. Astro rejects prefix-rewriting wildcards
  // with InvalidRedirectDestination: only '/prefix/[...slug]': '/[...slug]' is
  // legal, and the parameter must literally be named `slug`.
  redirects: {
    '/ops': '/work/',
    '/ops/getting-started/quickstart': '/work/',
    '/ops/features/agents': '/develop/features/agents/',
    '/ops/features/skills': '/develop/features/skills-and-experts/',
    '/ops/features/knowledge-bases': '/develop/features/knowledge-bases/',
    '/ops/features/models': '/develop/features/models/',
    '/ops/features/datasets': '/develop/features/datasets/',
    '/ops/features/training': '/develop/features/training/',
    '/ops/features/evaluations': '/develop/features/evaluations/',
    '/ops/features/sessions': '/develop/features/sessions/',
    '/ops/features/compute': '/develop/features/compute/',
    '/ops/features/hub': '/develop/features/hub/',
    '/ops/features/templates': '/develop/tools/templates/',
    '/search': '/',
  },
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
      favicon: '/favicon.svg',
      // Turns any broken internal link or anchor into a build failure. This
      // replaces onBrokenLinks: 'warn', under which breakage was invisible --
      // and the remarkConfig with remark-validate-links, which was configured
      // but never wired into the build at all.
      plugins: [starlightLinksValidator()],
      head: [
        // The old config pointed favicon at img/favicon.ico and the social
        // cards at /img/social-card.jpg. Neither file ever existed, so the
        // site shipped with no favicon and broken share previews. Both are
        // now real brand assets.
        {
          tag: 'link',
          attrs: { rel: 'icon', href: '/favicon.png', type: 'image/png' },
        },
        {
          tag: 'script',
          attrs: {
            async: true,
            src: 'https://www.googletagmanager.com/gtag/js?id=G-7YRDGYZN0R',
          },
        },
        {
          tag: 'script',
          content:
            'window.dataLayer=window.dataLayer||[];' +
            'function gtag(){dataLayer.push(arguments);}' +
            "gtag('js',new Date());gtag('config','G-7YRDGYZN0R');",
        },
        {
          tag: 'meta',
          attrs: {
            name: 'keywords',
            content:
              'Surogate, AgentOps, agents, LLM, MCP, training, fine-tuning, RL, evaluations',
          },
        },
        {
          tag: 'meta',
          attrs: {
            property: 'og:image',
            content: 'https://docs.surogate.ai/og-card.jpg',
          },
        },
        { tag: 'meta', attrs: { property: 'og:image:alt', content: 'Surogate' } },
        { tag: 'meta', attrs: { property: 'og:locale', content: 'en_US' } },
        // Starlight's head builder emits og:title and og:description but NOT
        // the twitter: equivalents, so these are kept explicitly rather than
        // dropped as redundant.
        {
          tag: 'meta',
          attrs: { name: 'twitter:card', content: 'summary_large_image' },
        },
        { tag: 'meta', attrs: { name: 'twitter:site', content: '@surogate_ai' } },
        {
          tag: 'meta',
          attrs: { name: 'twitter:creator', content: '@surogate_ai' },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:title', content: 'Surogate Documentation' },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'twitter:description',
            content: 'Operator and builder documentation for Surogate Ops.',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'twitter:image',
            content: 'https://docs.surogate.ai/og-card.jpg',
          },
        },
      ],
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
                'work/settings',
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

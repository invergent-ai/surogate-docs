import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import starlightLlmsTxt from 'starlight-llms-txt';
import starlightSidebarTopics from 'starlight-sidebar-topics';

// Expressive Code shows a header strip only on titled blocks. Title every block
// with its fence language (blank when it has none) so all of them get the strip.
function languageStrip() {
  return {
    name: 'language-strip',
    hooks: {
      preprocessMetadata: ({ codeBlock }) => {
        if (codeBlock.props.title) return;
        const lang = codeBlock.language;
        codeBlock.props.title = lang && !['plaintext', 'txt', 'text'].includes(lang) ? lang : '\u00a0';
      },
    },
  };
}

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
    // Upstream renamed work/settings/settings.md to authentication.md. The old
    // URL is in the pre-migration sitemap, so point it at the renamed page
    // rather than letting it 404 — it has in fact been 404ing in production
    // already, because Docusaurus emitted work/settings.html beside a
    // work/settings/ directory and the directory wins on GitHub Pages.
    '/work/settings': '/work/settings/authentication/',
  },
  integrations: [
    starlight({
      title: 'Surogate',
      description: 'Documentation for Surogate Ops — operator and builder tracks.',
      logo: {
        light: './src/assets/logo-black.svg',
        dark: './src/assets/logo-white.svg',
        alt: 'Surogate',
        // The logo is a 3.1:1 wordmark that already reads "Surogate", so
        // rendering the site title beside it duplicates the word. The alt text
        // above carries the name for screen readers and when images fail.
        replacesTitle: true,
      },
      customCss: [
        // Self-hosted, replacing the render-blocking Google Fonts @import that
        // the old custom.css opened on every page load.
        '@fontsource/inter/400.css',
        '@fontsource/inter/500.css',
        '@fontsource/inter/600.css',
        '@fontsource/inter/700.css',
        '@fontsource/inter/800.css',
        '@fontsource/jetbrains-mono/400.css',
        '@fontsource/jetbrains-mono/600.css',
        './src/styles/tokens.css',
        './src/styles/custom.css',
      ],
      // Code stays dark in both themes, square, with no terminal window frames.
      // Every block gets a header strip: the fence's language, or blank, plus Copy.
      expressiveCode: {
        themes: ['github-dark-default'],
        useStarlightDarkModeSwitch: false,
        defaultProps: { frame: 'code' },
        plugins: [languageStrip()],
        styleOverrides: {
          borderRadius: '0',
          borderColor: 'var(--d-line)',
          codeBackground: 'var(--d-codebg)',
          codeFontFamily: "'JetBrains Mono', ui-monospace, monospace",
          uiFontFamily: "'Inter', ui-sans-serif, system-ui, sans-serif",
          frames: {
            frameBoxShadowCssValue: 'none',
            editorTabBarBackground: 'var(--d-codebg)',
            editorActiveTabBackground: 'var(--d-codebg)',
            editorActiveTabForeground: 'rgba(255, 255, 255, 0.6)',
            editorActiveTabIndicatorTopColor: 'transparent',
            editorActiveTabIndicatorBottomColor: 'transparent',
            editorTabBarBorderBottomColor: 'rgba(255, 255, 255, 0.12)',
          },
        },
      },
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
      components: { SocialIcons: './src/components/HeaderLinks.astro' },
      favicon: '/favicon.svg',
      // Turns any broken internal link or anchor into a build failure. This
      // replaces onBrokenLinks: 'warn', under which breakage was invisible --
      // and the remarkConfig with remark-validate-links, which was configured
      // but never wired into the build at all.
      // starlight-llms-txt emits llms.txt / llms-full.txt. There was no
      // AI-crawler surface before, and this is documentation about building
      // agents.
      plugins: [
        starlightLinksValidator(),
        starlightLlmsTxt(),
        // One sidebar per track. Work and Develop are Surogate Agents; Keel is its own product.
        // Each topic's items are the track's former sidebar group, unchanged and in order.
        starlightSidebarTopics([
        {
          id: 'work',
          label: 'Work',
          link: '/work/',
          items: [
            'work',
            'work/quickstart',
            'work/whats-new',
            {
              label: 'Agents',
              collapsed: true,
              items: [
                'work/workflow/run-agent',
                'work/workflow/work-with-documents',
                'work/workflow/configure-agent',
                'work/workflow/publish-agent',
                'work/workflow/landing-page',
                'work/workflow/governance',
                'work/tools/chat',
                'work/tools/office-documents',
                'work/tools/whiteboard',
                'work/tools/commands',
                'work/tools/goals',
                'work/tools/missions',
                'work/tools/scheduled-work',
                'work/tools/programs',
                'work/tools/programs-team',
                'work/tools/programs-api',
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
                'work/channels/whatsapp',
                'work/channels/discord',
                'work/channels/teams',
                'work/channels/voice',
                'work/channels/website-widget',
                'work/channels/users',
                'work/channels/self-registration',
                'work/channels/proactive',
              ],
            },
            {
              label: 'Surogate Desktop',
              collapsed: true,
              items: [
                'work/desktop/get-started',
                'work/desktop/overview',
                'work/desktop/projects',
              ],
            },
            {
              label: 'Settings',
              collapsed: true,
              items: [
                'work/settings/profile',
                'work/settings/authentication',
                'work/settings/usage',
                'work/settings/billing',
                'work/settings/members',
                'work/settings/vault',
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
          id: 'develop',
          label: 'Develop',
          link: '/develop/',
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
                'develop/features/skill-canvas',
                'develop/features/skill-optimization',
                'develop/features/knowledge-bases',
                'develop/features/mcp-and-vault',
                'develop/features/byo-llm',
                {
                  slug: 'develop/features/experts-arenas',
                  badge: { text: 'Coming soon', variant: 'caution' },
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
                'develop/features/media-generation',
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
        {
          id: 'keel',
          label: 'Keel',
          link: '/keel/',
          items: [
            'keel',
            'keel/concepts',
            'keel/quickstart',
            {
              label: 'Keel Builder',
              collapsed: true,
              items: [
                'keel/builder/sign-in',
                'keel/builder/case-types',
                'keel/builder/drafts',
                'keel/builder/designer-agent',
                'keel/builder/workflow',
                'keel/builder/steps',
                'keel/builder/flow-nodes',
                'keel/builder/data',
                'keel/builder/forms',
                'keel/builder/scenarios',
                'keel/builder/connections',
                'keel/builder/case-type-settings',
                'keel/builder/versions',
                'keel/builder/publish',
                'keel/builder/rules',
                'keel/builder/queues',
                'keel/builder/settings',
              ],
            },
            {
              label: 'The business app',
              collapsed: true,
              items: [
                'keel/business/sign-in',
                'keel/business/work',
                'keel/business/queues',
                'keel/business/cases',
                'keel/business/open-case',
                'keel/business/case-agent',
                'keel/business/agents',
                'keel/business/watch',
                'keel/business/supervisors',
              ],
            },
            'keel/systems',
            {
              label: 'Reference',
              collapsed: true,
              items: [
                'keel/reference/glossary',
                'keel/reference/node-kinds',
                'keel/reference/roles',
                'keel/reference/faq',
              ],
            },
          ],
        },
      ]),
      ],
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

    }),
  ],
});

import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
    title: 'Surogate',
    tagline: 'AgentOps Factory',
    url: 'https://docs.surogate.ai',
    baseUrl: '/',
    // Soft-fail on broken links/markdown so a single typo doesn't kill the build
    // while two parallel doc trees and the legacy training docs all coexist.
    onBrokenLinks: 'warn',
    onBrokenMarkdownLinks: 'warn',
    favicon: 'img/favicon.ico',
    organizationName: 'invergent-ai',
    projectName: 'surogate-docs',
    deploymentBranch: 'gh-pages',
    trailingSlash: false,
    markdown: {
        mermaid: true,
        format: 'detect',
    },
    themes: ['@docusaurus/theme-mermaid'],
    i18n: {
        defaultLocale: 'en',
        locales: ['en'],
        localeConfigs: {en: {label: 'English'}},
    },
    themeConfig: {
        colorMode: {
            defaultMode: 'dark',
            respectPrefersColorScheme: true,
            disableSwitch: false,
        },
        navbar: {
            title: 'Documentation',
            logo: {
                alt: 'logo',
                src: 'img/logo-black.svg',
                srcDark: 'img/logo-white.svg',
                href: '/',
            },
            items: [
                {
                    type: 'custom-modeToggle',
                    position: 'left',
                },
                {
                    href: 'https://surogate.ai',
                    position: 'right',
                    label: 'About',
                },
                {
                    href: 'https://ops.surogate.ai',
                    position: 'right',
                    label: 'Login',
                },
                {
                    href: 'https://github.com/invergent-ai/surogate',
                    position: 'right',
                    label: 'GitHub',
                },
                {
                    href: 'https://x.com/surogate_ai',
                    position: 'right',
                    label: 'Follow us on X',
                },
                {
                    type: 'search',
                    position: 'right',
                },
            ],
        },
        algolia: {
            appId: 'K46M9C3QXR',
            apiKey: '8697cfccdeb5371226efca0dec10e96f',
            indexName: 'Surogate Docs',
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: 'Work mode (operators)',
                    items: [
                        {label: 'Welcome', to: '/work'},
                        {label: 'Run an agent', to: '/work/workflow/run-agent'},
                        {label: 'Review sessions', to: '/work/workflow/review-sessions'},
                        {label: 'Use cases', to: '/work/use-cases'},
                    ],
                },
                {
                    title: 'Develop mode (builders)',
                    items: [
                        {label: 'Welcome', to: '/develop'},
                        {label: 'The builder loop', to: '/develop/loop/overview'},
                        {label: 'Skills & Experts', to: '/develop/features/skills-and-experts'},
                        {label: 'Use cases', to: '/develop/use-cases'},
                    ],
                },
                {
                    title: 'Repos',
                    items: [
                        {label: 'Runtime (surogates)', href: 'https://github.com/invergent-ai/surogates'},
                        {label: 'Training framework (surogate)', href: 'https://github.com/invergent-ai/surogate'},
                        {label: 'Artifact store (surogate-hub)', href: 'https://github.com/invergent-ai/surogate-hub'},
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} Invergent. All rights reserved.`,
        },
    },
    headTags: [
        {
            tagName: 'meta',
            attributes: {name: 'keywords', content: 'Surogate, AgentOps, agents, LLM, MCP, training, fine-tuning, RL, evaluations'},
        },
        {
            tagName: 'meta',
            attributes: {name: 'description', content: 'Documentation for Surogate Ops — operator and builder tracks. Build reliable autonomous agents.'},
        },
        {tagName: 'meta', attributes: {name: 'og:type', content: 'website'}},
        {tagName: 'meta', attributes: {name: 'og:url', content: 'https://docs.surogate.ai'}},
        {tagName: 'meta', attributes: {name: 'og:title', content: 'Surogate Documentation'}},
        {tagName: 'meta', attributes: {name: 'og:description', content: 'Operator and builder documentation for Surogate Ops.'}},
        {tagName: 'meta', attributes: {name: 'og:image', content: 'https://docs.surogate.ai/img/social-card.jpg'}},
        {tagName: 'meta', attributes: {name: 'og:image:secure_url', content: 'https://docs.surogate.ai/img/social-card.jpg'}},
        {tagName: 'meta', attributes: {name: 'og:image:alt', content: 'Surogate'}},
        {tagName: 'meta', attributes: {name: 'og:locale', content: 'en_US'}},
        {tagName: 'meta', attributes: {name: 'og:image:type', content: 'image/jpeg'}},
        {tagName: 'meta', attributes: {name: 'twitter:site', content: 'surogate_ai'}},
        {tagName: 'meta', attributes: {name: 'twitter:creator', content: 'surogate_ai'}},
        {tagName: 'meta', attributes: {name: 'twitter:card', content: 'summary_large_image'}},
        {tagName: 'meta', attributes: {name: 'twitter:url', content: 'https://docs.surogate.ai'}},
        {tagName: 'meta', attributes: {name: 'twitter:title', content: 'Surogate Documentation'}},
        {tagName: 'meta', attributes: {name: 'twitter:description', content: 'Operator and builder documentation for Surogate Ops.'}},
        {tagName: 'meta', attributes: {name: 'twitter:image', content: 'https://docs.surogate.ai/img/social-card.jpg'}},
    ],
    presets: [
        [
            '@docusaurus/preset-classic',
            {
                docs: {
                    routeBasePath: '/',
                    sidebarPath: require.resolve('./sidebars.js'),
                    remarkPlugins: [remarkMath],
                    rehypePlugins: [rehypeKatex],
                },
                blog: false,
                theme: {
                    customCss: [require.resolve('./src/css/custom.css')],
                },
                sitemap: {
                    lastmod: 'date',
                    changefreq: 'weekly',
                },
                gtag: {
                    trackingID: 'G-7YRDGYZN0R',
                },
            },
        ],
    ],
    stylesheets: [
        {
            href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
            type: 'text/css',
            integrity: 'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
            crossorigin: 'anonymous',
        },
    ],
    plugins: [
        [
            '@docusaurus/plugin-client-redirects',
            {
                // Keep the old /ops/* URLs from v1.x working by sending them
                // to the new /work/* equivalents (most direct mapping).
                redirects: [
                    {from: '/ops', to: '/work'},
                    {from: '/ops/features/agents', to: '/develop/features/agents'},
                    {from: '/ops/features/skills', to: '/develop/features/skills-and-experts'},
                    {from: '/ops/features/knowledge-bases', to: '/develop/features/knowledge-bases'},
                    {from: '/ops/features/models', to: '/develop/features/models'},
                    {from: '/ops/features/datasets', to: '/develop/features/datasets'},
                    {from: '/ops/features/training', to: '/develop/features/training'},
                    {from: '/ops/features/evaluations', to: '/develop/features/evaluations'},
                    {from: '/ops/features/sessions', to: '/develop/features/sessions'},
                    {from: '/ops/features/compute', to: '/develop/features/compute'},
                    {from: '/ops/features/hub', to: '/develop/features/hub'},
                    {from: '/ops/features/templates', to: '/develop/tools/templates'},
                    {from: '/ops/getting-started/quickstart', to: '/work'},
                ],
            },
        ],
    ],
};

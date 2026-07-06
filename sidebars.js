module.exports = {
  // Work-mode sidebar — operator-facing
  // Maps to docs/work/* — every entry is a path relative to docs/work/
  workSidebar: [
    'work/intro',
    'work/quickstart',
    {
      type: 'category',
      label: 'Workflow',
      collapsed: false,
      items: [
        'work/workflow/run-agent',
        'work/workflow/configure-agent',
        'work/workflow/review-sessions',
        'work/workflow/improve-agent',
        'work/workflow/templates',
      ],
    },
    {
      type: 'category',
      label: 'Library',
      collapsed: false,
      items: [
        'work/library/skills',
        'work/library/knowledge-bases',
        'work/library/mcp-servers',
        'work/library/integrations',
      ],
    },
    {
      type: 'category',
      label: 'Channels & users',
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
      type: 'category',
      label: 'Commands & tools',
      collapsed: true,
      items: [
        'work/tools/commands',
        'work/tools/copilot',
        'work/tools/goals',
        'work/tools/missions',
        'work/tools/scheduled-work',
        'work/tools/deep-research',
        'work/tools/code',
        'work/tools/sub-agents',
        'work/tools/inbox',
      ],
    },
    {
      type: 'category',
      label: 'Settings',
      collapsed: true,
      items: [
        'work/settings/profile',
        'work/settings/settings',
        'work/settings/usage',
        'work/settings/billing',
      ],
    },
    'work/monetize',
    'work/use-cases',
    {
      type: 'category',
      label: 'Reference',
      collapsed: true,
      items: [
        'work/reference/glossary',
        'work/reference/faq',
      ],
    },
  ],

  // Develop-mode sidebar — builder-facing
  developSidebar: [
    'develop/intro',
    'develop/quickstart',
    {
      type: 'category',
      label: 'The builder loop',
      collapsed: false,
      items: [
        'develop/loop/overview',
        'develop/loop/build',
        'develop/loop/observe',
        'develop/loop/train',
        'develop/loop/redeploy',
      ],
    },
    {
      type: 'category',
      label: 'Operate',
      collapsed: false,
      items: [
        'develop/features/agents',
        'develop/features/sessions',
        'develop/features/compute',
        'develop/features/connect-compute',
      ],
    },
    {
      type: 'category',
      label: 'Agent capabilities',
      collapsed: false,
      items: [
        'develop/features/memory',
        'develop/features/browser',
        'develop/features/browser-profiles',
      ],
    },
    {
      type: 'category',
      label: 'Library',
      collapsed: false,
      items: [
        'develop/features/models',
        'develop/features/playground',
        'develop/features/skills-and-experts',
        'develop/features/skill-optimization',
        'develop/features/knowledge-bases',
        'develop/features/mcp-and-vault',
        'develop/features/hub',
        'develop/features/byo-llm',
      ],
    },
    {
      type: 'category',
      label: 'Train',
      collapsed: false,
      items: [
        'develop/features/datasets',
        'develop/features/training',
        'develop/features/evaluations',
      ],
    },
    {
      type: 'category',
      label: 'Tools & dashboard',
      collapsed: true,
      items: [
        'develop/tools/dashboard',
        'develop/tools/copilot',
        'develop/tools/templates',
      ],
    },
    'develop/use-cases',
    {
      type: 'category',
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

  // Training-framework sidebar (existing, untouched)
  mySidebar: [
    {
      type: 'doc',
      id: 'index',
      label: 'Welcome',
    },
    {
      type: 'category',
      label: 'About Surogate',
      collapsed: false,
      items: [
        'about/how-it-works',
        'about/adaptive-training',
        'about/dsl',
        'about/automatic-differentiation',
      ],
    },
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/installation',
        'getting-started/training-modes',
        'getting-started/quickstart-pretraining',
        'getting-started/quickstart-sft',
        'getting-started/quickstart-grpo',
      ],
    },
    {
      type: 'category',
      label: 'Examples Library',
      collapsed: false,
      items: [
        'examples/index',
        {
          type: 'category',
          label: 'Pre-training (PT)',
          items: ['examples/pt/qwen3'],
        },
        {
          type: 'category',
          label: 'Fine-tuning (SFT)',
          items: [
            'examples/sft/qwen3-lora',
            'examples/sft/qwen3-qlora',
            'examples/sft/qwen3moe-lora',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'User Guides',
      collapsed: true,
      items: [
        'guides/configuration',
        'guides/datasets',
        'guides/optimizers',
        'guides/precision-and-recipes',
        'guides/qlora',
        'guides/metrics',
        'guides/moe',
        'guides/multi-gpu',
        'guides/multi-node',
        'guides/offloading',
        'guides/long-context',
        'guides/memory',
        'guides/debugging',
        'guides/rl-environments',
        'guides/rl-training',
      ],
    },
    {
      type: 'category',
      label: 'Technical Reference',
      collapsed: true,
      items: [
        'reference/benchmarks',
        'reference/python-api',
        'reference/cli',
        'reference/config',
      ],
    },
    {
      type: 'category',
      label: 'Appendix',
      collapsed: true,
      items: [
        'appendix/release-notes',
        'appendix/glossary',
        'appendix/compatibility',
        'appendix/faq',
      ],
    },
  ],
};

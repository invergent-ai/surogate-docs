module.exports = {
  // Work-mode sidebar — operator-facing. Mirrors the Work app nav:
  // Agents · Sessions · Skills & Tools · Knowledge Bases (+ Settings).
  workSidebar: [
    'work/intro',
    'work/quickstart',
    {
      type: 'category',
      label: 'Agents',
      collapsed: false,
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
    { type: 'doc', id: 'work/workflow/review-sessions', label: 'Sessions' },
    {
      type: 'category',
      label: 'Skills & Tools',
      collapsed: false,
      items: [
        'work/library/skills',
        'work/library/mcp-servers',
        'work/library/integrations',
        'work/workflow/templates',
      ],
    },
    { type: 'doc', id: 'work/library/knowledge-bases', label: 'Knowledge Bases' },
    {
      type: 'category',
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
    'work/tools/copilot',
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

  // Develop-mode sidebar — builder-facing. Mirrors the Dev app nav:
  // Dashboard · Sessions · Models · Playground · Data Hub · Datasets ·
  // Training · Evaluations · Compute. (Experts is not shipped yet — hidden.)
  developSidebar: [
    'develop/intro',
    'develop/quickstart',
    {
      type: 'category',
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
    { type: 'doc', id: 'develop/tools/dashboard', label: 'Dashboard' },
    { type: 'doc', id: 'develop/features/sessions', label: 'Sessions' },
    { type: 'doc', id: 'develop/features/models', label: 'Models' },
    { type: 'doc', id: 'develop/features/playground', label: 'Playground' },
    { type: 'doc', id: 'develop/features/hub', label: 'Data Hub' },
    { type: 'doc', id: 'develop/features/datasets', label: 'Datasets' },
    { type: 'doc', id: 'develop/features/training', label: 'Training' },
    { type: 'doc', id: 'develop/features/evaluations', label: 'Evaluations' },
    {
      type: 'category',
      label: 'Compute',
      collapsed: false,
      items: [
        'develop/features/compute',
        'develop/features/connect-compute',
      ],
    },
    {
      type: 'category',
      label: 'Skills & knowledge',
      collapsed: true,
      items: [
        'develop/features/skills-and-experts',
        'develop/features/skill-optimization',
        'develop/features/knowledge-bases',
        'develop/features/mcp-and-vault',
        'develop/features/byo-llm',
      ],
    },
    {
      type: 'category',
      label: 'Agent capabilities',
      collapsed: true,
      items: [
        'develop/features/memory',
        'develop/features/browser',
        'develop/features/browser-profiles',
      ],
    },
    {
      type: 'category',
      label: 'Tools',
      collapsed: true,
      items: [
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

  // Training-framework sidebar (the surogate trainer engine) — untouched.
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

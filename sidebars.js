module.exports = {
  // Surogate Ops user manual.
  opsSidebar: [
    {
      type: 'doc',
      id: 'ops/index',
      label: 'Welcome',
    },
    {
      type: 'doc',
      id: 'ops/getting-started/quickstart',
      label: 'Quickstart',
    },
    {
      type: 'category',
      label: 'Use cases',
      collapsed: false,
      items: [
        'ops/use-cases/customer-support',
        'ops/use-cases/internal-knowledge',
        'ops/use-cases/sales-lead-qualifier',
        'ops/use-cases/code-review',
        'ops/use-cases/training-your-own-expert',
      ],
    },
    {
      type: 'category',
      label: 'Build',
      collapsed: false,
      items: [
        'ops/features/agents',
        'ops/features/skills',
        'ops/features/knowledge-bases',
        'ops/features/models',
      ],
    },
    {
      type: 'category',
      label: 'Train',
      collapsed: true,
      items: [
        'ops/features/datasets',
        'ops/features/training',
        'ops/features/evaluations',
        'ops/features/arenas',
      ],
    },
    {
      type: 'category',
      label: 'Operate',
      collapsed: true,
      items: [
        'ops/features/monitoring',
        'ops/features/sessions',
        'ops/features/compute',
        'ops/features/playground',
      ],
    },
    {
      type: 'category',
      label: 'Distribute',
      collapsed: true,
      items: [
        'ops/features/hub',
      ],
    },
    {
      type: 'category',
      label: 'Admin',
      collapsed: true,
      items: [
        'ops/admin/projects-and-roles',
        'ops/admin/integrations',
        'ops/admin/notifications',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      collapsed: true,
      items: [
        'ops/reference/permissions-matrix',
        'ops/reference/errors',
        'ops/glossary',
        'ops/changelog',
      ],
    },
  ],

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
        'about/automatic-differentiation'
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
          items: [
            'examples/pt/qwen3',
          ],
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
        'reference/config'
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

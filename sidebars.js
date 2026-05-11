module.exports = {
  // Surogate Ops user manual — separate sidebar so it doesn't mix with the
  // Surogate Trainer docs. Activated automatically for any doc under `ops/`.
  opsSidebar: [
    {
      type: 'doc',
      id: 'ops/index',
      label: 'Welcome',
    },
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'ops/getting-started/sign-in',
        'ops/getting-started/first-run',
        'ops/getting-started/tour',
        'ops/getting-started/where-to-find-things',
      ],
    },
    {
      type: 'category',
      label: 'Concepts',
      collapsed: false,
      items: [
        'ops/concepts/work-vs-develop',
        'ops/concepts/core-objects',
        'ops/concepts/lifecycle',
      ],
    },
    {
      type: 'doc',
      id: 'ops/glossary',
      label: 'Glossary',
    },
    {
      type: 'category',
      label: 'Features',
      collapsed: true,
      items: [
        'ops/features/agents',
        'ops/features/sessions',
        'ops/features/skills',
        'ops/features/knowledge-bases',
        'ops/features/models',
        'ops/features/compute',
        'ops/features/monitoring',
        'ops/features/evaluations',
        'ops/features/arenas',
        'ops/features/playground',
        'ops/features/datasets',
        'ops/features/training',
        'ops/features/hub',
      ],
    },
    {
      type: 'category',
      label: 'Workflows',
      collapsed: true,
      items: [
        'ops/workflows/explore-as-end-user',
        'ops/workflows/deploy-an-agent',
        'ops/workflows/deploy-a-model',
        'ops/workflows/create-a-knowledge-base',
        'ops/workflows/add-a-skill',
        'ops/workflows/connect-a-cloud-backend',
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
        'ops/reference/keyboard-shortcuts',
        'ops/reference/errors',
        'ops/reference/accessibility',
      ],
    },
    {
      type: 'doc',
      id: 'ops/troubleshooting',
      label: 'Troubleshooting',
    },
    {
      type: 'doc',
      id: 'ops/faq',
      label: 'FAQ',
    },
    {
      type: 'doc',
      id: 'ops/changelog',
      label: 'Changelog',
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



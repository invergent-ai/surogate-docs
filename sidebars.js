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
      label: 'Build',
      collapsed: true,
      items: [
        'ops/features/templates',
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
        'ops/features/rl-environments',
        'ops/features/evaluations',
      ],
    },
    {
      type: 'category',
      label: 'Operate',
      collapsed: true,
      items: [
        'ops/features/sessions',
        'ops/features/compute',
        {
          type: 'category',
          label: 'Compute providers',
          collapsed: true,
          items: [
            'ops/compute-providers/aws',
            'ops/compute-providers/azure',
            'ops/compute-providers/gcp',
            'ops/compute-providers/runpod',
            'ops/compute-providers/modal',
            'ops/compute-providers/nebius',
            'ops/compute-providers/oci',
            'ops/compute-providers/vast-ai',
          ],
        },
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
      label: 'Concepts',
      collapsed: true,
      items: [
        'ops/concepts/architecture',
        'ops/concepts/studio-dashboard',
      ],
    },
    {
      type: 'category',
      label: 'Use cases',
      collapsed: true,
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
      label: 'Tutorials',
      collapsed: true,
      items: [
        'ops/tutorials/build-a-support-bot',
        'ops/tutorials/connect-cloud-and-serve-a-model',
        'ops/tutorials/train-and-promote-an-expert',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      collapsed: true,
      items: [
        {
          type: 'category',
          label: 'API Reference',
          collapsed: true,
          items: [
            'ops/api/overview',
            'ops/api/inference',
            'ops/api/hub',
            'ops/api/errors-and-rate-limits',
          ],
        },
        {
          type: 'category',
          label: 'Admin Guide',
          collapsed: true,
          items: [
            'ops/admin/overview',
            'ops/admin/teams-and-roles',
            'ops/admin/credential-vault',
            'ops/admin/data-hub-config',
          ],
        },
        'ops/reference/permissions-matrix',
        'ops/reference/errors',
        'ops/reference/troubleshooting',
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

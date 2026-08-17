import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/search',
    component: ComponentCreator('/search', '5de'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', '070'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', '0e4'),
    routes: [
      {
        path: '/',
        component: ComponentCreator('/', '622'),
        routes: [
          {
            path: '/',
            component: ComponentCreator('/', '8be'),
            routes: [
              {
                path: '/about/adaptive-training',
                component: ComponentCreator('/about/adaptive-training', 'eb9'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/about/automatic-differentiation',
                component: ComponentCreator('/about/automatic-differentiation', '884'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/about/dsl',
                component: ComponentCreator('/about/dsl', '622'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/about/how-it-works',
                component: ComponentCreator('/about/how-it-works', 'fef'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/appendix/compatibility',
                component: ComponentCreator('/appendix/compatibility', '617'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/appendix/faq',
                component: ComponentCreator('/appendix/faq', '054'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/appendix/glossary',
                component: ComponentCreator('/appendix/glossary', 'b03'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/appendix/release-notes',
                component: ComponentCreator('/appendix/release-notes', 'f50'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/develop',
                component: ComponentCreator('/develop', '87a'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/agents',
                component: ComponentCreator('/develop/features/agents', '412'),
                exact: true
              },
              {
                path: '/develop/features/browser',
                component: ComponentCreator('/develop/features/browser', 'ede'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/browser-profiles',
                component: ComponentCreator('/develop/features/browser-profiles', '46d'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/byo-llm',
                component: ComponentCreator('/develop/features/byo-llm', '7d8'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/compute',
                component: ComponentCreator('/develop/features/compute', '378'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/connect-compute',
                component: ComponentCreator('/develop/features/connect-compute', 'c04'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/datasets',
                component: ComponentCreator('/develop/features/datasets', '78b'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/evaluations',
                component: ComponentCreator('/develop/features/evaluations', 'd34'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/hub',
                component: ComponentCreator('/develop/features/hub', '744'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/knowledge-bases',
                component: ComponentCreator('/develop/features/knowledge-bases', '5f5'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/mcp-and-vault',
                component: ComponentCreator('/develop/features/mcp-and-vault', '8f9'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/media-generation',
                component: ComponentCreator('/develop/features/media-generation', '763'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/memory',
                component: ComponentCreator('/develop/features/memory', 'f3f'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/models',
                component: ComponentCreator('/develop/features/models', 'af5'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/playground',
                component: ComponentCreator('/develop/features/playground', '43a'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/sessions',
                component: ComponentCreator('/develop/features/sessions', 'c20'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/skill-optimization',
                component: ComponentCreator('/develop/features/skill-optimization', '44a'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/skills-and-experts',
                component: ComponentCreator('/develop/features/skills-and-experts', '715'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/features/training',
                component: ComponentCreator('/develop/features/training', '8ed'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/loop/build',
                component: ComponentCreator('/develop/loop/build', '4a4'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/loop/observe',
                component: ComponentCreator('/develop/loop/observe', 'fbf'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/loop/overview',
                component: ComponentCreator('/develop/loop/overview', '4b3'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/loop/redeploy',
                component: ComponentCreator('/develop/loop/redeploy', 'e62'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/loop/train',
                component: ComponentCreator('/develop/loop/train', '9f6'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/quickstart',
                component: ComponentCreator('/develop/quickstart', '869'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/reference/background-jobs',
                component: ComponentCreator('/develop/reference/background-jobs', '2e1'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/reference/coordination',
                component: ComponentCreator('/develop/reference/coordination', 'd4f'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/reference/event-types',
                component: ComponentCreator('/develop/reference/event-types', '4da'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/reference/glossary',
                component: ComponentCreator('/develop/reference/glossary', '76b'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/reference/runtime-architecture',
                component: ComponentCreator('/develop/reference/runtime-architecture', 'b7a'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/reference/tool-catalog',
                component: ComponentCreator('/develop/reference/tool-catalog', 'd4f'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/tools/copilot',
                component: ComponentCreator('/develop/tools/copilot', '3a9'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/tools/dashboard',
                component: ComponentCreator('/develop/tools/dashboard', 'eec'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/tools/templates',
                component: ComponentCreator('/develop/tools/templates', 'f52'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/develop/use-cases',
                component: ComponentCreator('/develop/use-cases', '83f'),
                exact: true,
                sidebar: "developSidebar"
              },
              {
                path: '/examples',
                component: ComponentCreator('/examples', '090'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/examples/grpo',
                component: ComponentCreator('/examples/grpo', 'cf8'),
                exact: true
              },
              {
                path: '/examples/pt/qwen3',
                component: ComponentCreator('/examples/pt/qwen3', 'c8c'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/examples/sft/qwen3-lora',
                component: ComponentCreator('/examples/sft/qwen3-lora', 'c5d'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/examples/sft/qwen3-qlora',
                component: ComponentCreator('/examples/sft/qwen3-qlora', '16b'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/examples/sft/qwen3moe-lora',
                component: ComponentCreator('/examples/sft/qwen3moe-lora', 'e11'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/getting-started/installation',
                component: ComponentCreator('/getting-started/installation', 'a6e'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/getting-started/quickstart-grpo',
                component: ComponentCreator('/getting-started/quickstart-grpo', '390'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/getting-started/quickstart-pretraining',
                component: ComponentCreator('/getting-started/quickstart-pretraining', '460'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/getting-started/quickstart-sft',
                component: ComponentCreator('/getting-started/quickstart-sft', 'e86'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/getting-started/training-modes',
                component: ComponentCreator('/getting-started/training-modes', 'a0a'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/configuration',
                component: ComponentCreator('/guides/configuration', 'fb8'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/datasets',
                component: ComponentCreator('/guides/datasets', '75c'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/debugging',
                component: ComponentCreator('/guides/debugging', '28a'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/long-context',
                component: ComponentCreator('/guides/long-context', 'bff'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/memory',
                component: ComponentCreator('/guides/memory', 'd58'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/metrics',
                component: ComponentCreator('/guides/metrics', '237'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/moe',
                component: ComponentCreator('/guides/moe', '4bf'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/multi-gpu',
                component: ComponentCreator('/guides/multi-gpu', '76b'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/multi-node',
                component: ComponentCreator('/guides/multi-node', '1e1'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/offloading',
                component: ComponentCreator('/guides/offloading', 'a1e'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/optimizers',
                component: ComponentCreator('/guides/optimizers', '84f'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/performance',
                component: ComponentCreator('/guides/performance', '82b'),
                exact: true
              },
              {
                path: '/guides/precision-and-recipes',
                component: ComponentCreator('/guides/precision-and-recipes', '64d'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/qlora',
                component: ComponentCreator('/guides/qlora', 'b1f'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/rl-environments',
                component: ComponentCreator('/guides/rl-environments', 'e44'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/guides/rl-training',
                component: ComponentCreator('/guides/rl-training', 'cc3'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/old-docs',
                component: ComponentCreator('/old-docs', '2f0'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/reference/benchmarks',
                component: ComponentCreator('/reference/benchmarks', 'c3a'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/reference/cli',
                component: ComponentCreator('/reference/cli', 'f0d'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/reference/config',
                component: ComponentCreator('/reference/config', '7d1'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/reference/python-api',
                component: ComponentCreator('/reference/python-api', 'ff4'),
                exact: true,
                sidebar: "mySidebar"
              },
              {
                path: '/work',
                component: ComponentCreator('/work', '8ae'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/proactive',
                component: ComponentCreator('/work/channels/proactive', '838'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/self-registration',
                component: ComponentCreator('/work/channels/self-registration', '264'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/slack',
                component: ComponentCreator('/work/channels/slack', 'aca'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/telegram',
                component: ComponentCreator('/work/channels/telegram', 'da8'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/users',
                component: ComponentCreator('/work/channels/users', '041'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/web',
                component: ComponentCreator('/work/channels/web', '4fd'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/website-widget',
                component: ComponentCreator('/work/channels/website-widget', 'a36'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/channels/whatsapp',
                component: ComponentCreator('/work/channels/whatsapp', 'b39'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/library/integrations',
                component: ComponentCreator('/work/library/integrations', 'c49'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/library/knowledge-bases',
                component: ComponentCreator('/work/library/knowledge-bases', 'ff5'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/library/mcp-servers',
                component: ComponentCreator('/work/library/mcp-servers', 'eba'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/library/skills',
                component: ComponentCreator('/work/library/skills', '698'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/monetize',
                component: ComponentCreator('/work/monetize', '093'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/quickstart',
                component: ComponentCreator('/work/quickstart', 'b1f'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/reference/faq',
                component: ComponentCreator('/work/reference/faq', 'da9'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/reference/glossary',
                component: ComponentCreator('/work/reference/glossary', 'fcd'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/settings/authentication',
                component: ComponentCreator('/work/settings/authentication', 'dc9'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/settings/billing',
                component: ComponentCreator('/work/settings/billing', 'b4a'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/settings/profile',
                component: ComponentCreator('/work/settings/profile', '080'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/settings/usage',
                component: ComponentCreator('/work/settings/usage', '77a'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/chat',
                component: ComponentCreator('/work/tools/chat', '96c'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/code',
                component: ComponentCreator('/work/tools/code', 'b3c'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/commands',
                component: ComponentCreator('/work/tools/commands', 'e53'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/copilot',
                component: ComponentCreator('/work/tools/copilot', '406'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/deep-research',
                component: ComponentCreator('/work/tools/deep-research', '5aa'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/goals',
                component: ComponentCreator('/work/tools/goals', 'b68'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/inbox',
                component: ComponentCreator('/work/tools/inbox', 'e19'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/missions',
                component: ComponentCreator('/work/tools/missions', '885'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/scheduled-work',
                component: ComponentCreator('/work/tools/scheduled-work', 'b6e'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/tools/sub-agents',
                component: ComponentCreator('/work/tools/sub-agents', '1c9'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/use-cases',
                component: ComponentCreator('/work/use-cases', '65c'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/workflow/configure-agent',
                component: ComponentCreator('/work/workflow/configure-agent', '86a'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/workflow/governance',
                component: ComponentCreator('/work/workflow/governance', '674'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/workflow/improve-agent',
                component: ComponentCreator('/work/workflow/improve-agent', '7f8'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/workflow/review-sessions',
                component: ComponentCreator('/work/workflow/review-sessions', '385'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/workflow/run-agent',
                component: ComponentCreator('/work/workflow/run-agent', '197'),
                exact: true,
                sidebar: "workSidebar"
              },
              {
                path: '/work/workflow/templates',
                component: ComponentCreator('/work/workflow/templates', '2ca'),
                exact: true,
                sidebar: "workSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];

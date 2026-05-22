---
slug: /develop
title: Welcome to Develop mode
sidebar_label: Welcome
sidebar_position: 1
---

# Develop mode

For designing agents, writing skills, training experts, running evaluations, integrating via API, and deploying on your own cluster. Flip to **Work mode** in the navbar if you only need to chat with deployed agents and watch sessions.

## How the platform is built

Two source-of-truth repos:

| Repo | Role | License |
|---|---|---|
| [`invergent-ai/surogates`](https://github.com/invergent-ai/surogates) | Agent runtime — harness loop, sessions, sandbox, MCP, governance, channels, memory, tools | AGPL-3.0 |
| [`invergent-ai/surogate-ops`](https://github.com/invergent-ai/surogate-ops) | Operator platform (the `ops.surogate.ai` UI itself) — REST API, billing, hub, training pipeline | AGPL-3.0 |

When you deploy an agent at `<slug>.cloud.surogate.ai`, the ops platform's Helm chart wraps the runtime image and binds your config to it. The runtime is what's actually running inside the container.

This documentation focuses on the platform surface — what you can do through `ops.surogate.ai`. For runtime internals, see the [runtime architecture reference](./reference/runtime-architecture.md).

## The builder loop

```
       ┌─────────────────────────────────────┐
       │                                     │
       ▼                                     │
┌──────────┐    ┌──────────┐    ┌──────────┐ │   ┌──────────┐
│  BUILD   │ →  │ OBSERVE  │ →  │  TRAIN   │ → │  REDEPLOY  │
│ (config) │    │(sessions)│    │ (dataset │ │   │ (new agent│
│          │    │ & evals) │    │ + train) │ │   │  version) │
└──────────┘    └──────────┘    └──────────┘ │   └─────┬────┘
                                              │         │
                                              └─────────┘
```

Most iteration lives in **build → observe**. Training experts and re-deploying happens weekly to monthly, not daily.

Start at [The builder loop overview](./loop/overview.md) for the full cycle, or jump to [Use cases](./use-cases.md) for end-to-end recipes.

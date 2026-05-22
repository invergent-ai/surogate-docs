---
title: Compute
sidebar_position: 3
---

# Compute

The Compute page surfaces what's actually running. Two tabs:

- **Cloud** — connect / disconnect cloud-GPU providers for serving models and running training
- **Workload Queue** — see active agent pods, model-serving jobs, training runs, eval runs

## Cloud — connect providers

The platform supports 8 cloud-GPU providers via [dstack](https://dstack.ai) and direct Modal integration. Each shows up as a card on the Cloud tab.

| Provider | Configuration | Best for |
|---|---|---|
| **AWS** | IAM credentials + region | EC2 GPU instances (P3/G5) |
| **Azure** | Service principal + region | NC/ND GPU VMs |
| **GCP** | Service account JSON | A100/H100 GPU instances |
| **RunPod** | API key | Spot-friendly GPU pods, cheap for batch |
| **Modal** | Direct integration (Modal token) | Python-native, fast cold starts |
| **Nebius** | API key | EU-resident GPU |
| **Oracle Cloud (OCI)** | API user + key | Enterprise compliance |
| **Vast.ai** | API key | Cheapest GPU marketplace |

Connecting a provider lets the platform spin up GPU resources for:

- **Model serving** — running a fine-tuned model behind an endpoint
- **Training** — SFT / GRPO runs
- **Synthetic data pipelines** — generating training data via teacher/judge models

To connect: click a provider card → fill in credentials → CONNECT. The platform validates with a small test run.

> :::warning Credentials = real money
> Once connected, the platform can spin up GPU instances on your behalf. Each instance type and each provider has different rates. Configure spending caps via the **BYO LLM** toggle and per-provider budget limits.
> :::

## Workload queue

The Workload Queue tab shows everything currently consuming compute:

| Column | What it is |
|---|---|
| **Agent pods** | Sessions running on agent containers (1 pod per active session, or warm-pool pods for browser fleet) |
| **Model serving** | Running fine-tuned models with their endpoints |
| **Training runs** | Active SFT / GRPO jobs |
| **Eval runs** | Running evaluations |

Filter by status, provider, agent. Click any row to drill into the underlying job's logs and metrics.

## The agent runtime

Each agent runs as a Helm release in K8s. The chart (`surogate_ops/agent_chart/` in the ops repo) wraps the `surogates` runtime image with your agent's configuration. Key concepts from the runtime:

- **Workers** — stateless pods that pop sessions off Redis and run the harness. Up to 50 concurrent sessions per worker.
- **Sandboxes** — per-session ephemeral pods that run untrusted LLM-generated code. K8s NetworkPolicy isolates them from the cluster.
- **Browsers** — separate pods for the browser-use tools. Can be warm-pooled (see below).
- **MCP proxy** — credential-injection pod that sits between sandboxes and external MCP servers.

For the full runtime architecture, see [Runtime architecture reference](../reference/runtime-architecture.md).

## Browser warm pool

The platform supports a **browser warm pool** for sub-2-second browser cold starts. Default cold start is ~60s (full K8s pod provisioning). With the warm pool:

- A pool of pre-provisioned browser pods sits ready
- First-use browser latency drops to ~2s (just attach to a pool pod)
- Falls back to per-session provisioning when the pool is at capacity

To enable: cluster admin sets `browser_fleet.enabled: true` in the platform config and deploys the `charts/browser-fleet/` Helm chart. Per-agent: set `browser.backend: fleet` in the agent's CONFIG.

🚧 The browser warm pool is cluster-admin-only — not exposed in the UI as a toggle.

## Scaling

Per-agent scaling is done from the agent's SCALE button, not from the Compute page.

The Compute page shows the **aggregate** view — total pods, total GPU usage, per-provider spend. Useful for capacity planning and cost monitoring.

## Monitoring

Each pod exposes `/metrics` for Prometheus:

| Metric | Type | Description |
|---|---|---|
| `surogates_active_sessions` | gauge | Sessions per worker |
| `surogates_events_total` | counter | Events emitted by type |
| `surogates_llm_requests_total` | counter | LLM API calls by provider/model/status |
| `surogates_llm_latency_seconds` | histogram | Per-call latency |
| `surogates_tool_calls_total` | counter | Tool calls by name/location/status |
| `surogates_tool_latency_seconds` | histogram | Per-tool latency |
| `surogates_delivery_pending` | gauge | Pending delivery outbox items |
| `surogates_sandbox_active` | gauge | Active sandbox pods |
| `surogates_session_cost_usd` | histogram | Estimated session cost |

Scrape with your existing Prometheus / Grafana setup.

## What's next

[Models](./models.md) for what runs on this compute. [Training](./training.md) for the training runs. [Skills & Experts](./skills-and-experts.md) for expert serving.

---
title: Compute
sidebar_position: 3
---

# Compute

The Compute page is where you wire up cloud GPU providers so the platform can run training jobs and serve fine-tuned models on your behalf. You don't manage Kubernetes or VM provisioning — the platform does that — but you choose **which provider** runs what.

Two tabs: **Cloud** for connecting providers, **Workload Queue** for seeing what's running. Auto-scaling **Policies** and the step-by-step provider connection walk-through (credentials per provider, browsing backend offers) live in [Connect compute](./connect-compute.md) — this page stays conceptual.

## Cloud — connect a provider

Eight providers are supported:

| Provider | Best for |
|---|---|
| **AWS** | Standard EC2 GPU (P3, G5, P4d, P5) |
| **Azure** | NC / ND VMs, enterprise compliance |
| **GCP** | A100, H100 instances |
| **RunPod** | Spot-friendly pricing, fast for batch jobs |
| **Modal** | Python-native deploys, very fast cold starts |
| **Nebius** | EU-resident GPU |
| **Oracle Cloud (OCI)** | Enterprise compliance |
| **Vast.ai** | Cheapest GPU marketplace |

Click a provider card → paste credentials → CONNECT. The platform validates with a small test job before marking the connection healthy.

> Connecting a provider gives the platform permission to spin up GPU instances **billed to your account at that provider**. Configure per-provider spending caps before pointing real workloads at it.

## What you can launch on connected providers

| Workload | Where it lands |
|---|---|
| **Training runs** | SFT / GRPO jobs. See [Training](./training.md). |
| **Model serving** | Fine-tuned models served behind OpenAI-compatible endpoints. See [Models](./models.md). |
| **Synthetic data pipelines** | Teacher/judge/worker generation. See [Datasets](./datasets.md). |

When you start any of these in the platform UI, you pick a provider; the platform handles the rest.

## Workload Queue

Real-time view of everything consuming compute on your behalf:

- Active agent pods (one per running session, normally short-lived)
- Model-serving endpoints (longer-lived)
- Training runs in progress
- Evaluation runs
- Synthetic-data pipelines

Filter by status, provider, agent. Click any row to drill into logs and metrics.

## Browser warm pool (advanced)

For agents that use the `browser_*` tools heavily, first-use latency is normally ~60s (Chromium pod cold start). The platform optionally maintains a warm pool of pre-provisioned browser pods to drop that to ~2s; subsequent calls in the same session reuse the pod.

Cluster-admin opt-in (set on the agent's CONFIG with `browser.backend: fleet`). Not exposed in the UI for self-serve toggling. Talk to your platform admin if you're shipping browser-heavy agents at scale.

## When to connect a provider vs use the bundled compute

By default, the platform runs agents and small inference on its own bundled compute (billed via your Surogate plan). You only need to connect a cloud provider when you want to:

- Host a fine-tuned expert (model serving)
- Run training jobs
- Run large synthetic-data pipelines
- Self-serve cloud-GPU spending instead of having Surogate pass it through

If none of those apply, leave the Cloud tab empty.

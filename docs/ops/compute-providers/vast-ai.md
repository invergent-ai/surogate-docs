---
title: Vast.ai
sidebar_position: 8
slug: /compute-providers/vast-ai
description: Connect Vast.ai as a Surogate Ops compute backend. Single-key auth; the cheapest GPU rates you'll find.
---

# Vast.ai

Vast.ai is a marketplace of GPU instances offered by individual providers worldwide. The price floor is typically the lowest you'll find anywhere, but the operational story is more variable than the hyperscalers — instances can be interrupted, network speeds vary, and reliability is per-host.

It's the right backend for cost-sensitive experimentation, evals, and short fine-tunes. Less appropriate for production serving where uptime guarantees matter.

## Credentials Surogate needs

One value:

- **API Key**

## Get the API key

1. Sign in to **vast.ai**.
2. **Account → API Keys → Create new key.**
3. **Name** — `surogate-ops`.
4. **Permissions** — read & write.

Copy the value. Vast.ai shows it once.

## Connect in Surogate

Compute → Cloud → **Vast.ai** tile. Paste the API key. Submit. Done.

The tile flips to **Connected** in seconds. Offers populate immediately.

## What the offer list looks like

Vast.ai offers are heterogeneous in a way that hyperscaler offers aren't. Each offer carries:

- The GPU type (A100 / H100 / 3090 / 4090 / etc.).
- The number of GPUs in the host.
- Geographic location and provider id.
- Network bandwidth (varies widely; matters for model pulls).
- Reliability score (provider-track-record-based).
- Spot vs on-demand pricing.

Surogate's scheduler ranks offers by a combination of these. You can pin to specific bands via Compute Policy — for example "only offers with reliability ≥ 95% and bandwidth ≥ 1 Gbps".

## Supported GPU types

Vast.ai's catalog is broader than any other backend:

| GPU | Notes |
|---|---|
| **H100 80GB** | Top-end. Less common but available. |
| **A100 40GB / 80GB** | Wide availability. |
| **RTX 4090 24GB** | Consumer GPU; cheap. Good for 7B–13B serving and small training. |
| **RTX 3090 24GB** | Older consumer GPU; very cheap. Same use cases as 4090. |
| **L40S 48GB / A6000 48GB** | Mid-range. |
| **Older datacenter GPUs (V100, P100, etc.)** | Cheapest possible; use only when GPU memory limits don't matter. |

Single- and multi-GPU offers both exist. Multi-GPU offers from the same physical host are usable for distributed training.

## Verify the backend works

After connecting, the Offers panel populates within seconds. If empty:

1. **API key scope.** Read-only keys list offers but can't provision; create a Read & Write key.
2. **Account credit balance.** Vast.ai requires a positive balance to provision. The balance is visible at top-right of the Vast.ai dashboard.

## Cost shape

The cheapest GPU you can rent. Per-second billing.

Practical pointers:

- **Spot saves a lot.** Vast.ai's interruptible "spot"-style pricing is usually 40-60% off on-demand for the same host.
- **Reliability scores matter.** Filter your Compute Policy to require a reliability threshold; cheap unreliable hosts cost more in time spent re-provisioning than they save.
- **Pull bandwidth is part of the cost calculus.** Pulling a 50GB model on a 100Mbps connection takes an hour. The offers panel shows bandwidth; consider it before picking a cheap-but-slow host.

## When something fails

- **Workload provisions, then the instance disappears mid-run.** The host went offline or revoked the offer. Spot-style behaviour even on on-demand offers, depending on the host's reliability. Resubmit; the scheduler picks a different host. Production training should checkpoint frequently.
- **Image pull times out.** Bandwidth on the chosen host is too low. Cancel, raise the bandwidth filter in your Compute Policy, retry.
- **Spot price spike.** Vast.ai's prices are real-time. If the Compute Policy's price ceiling is too tight, the scheduler may find no offers. Raise the ceiling or wait.
- **`401 Unauthorized`.** API key revoked or expired. Generate a new one.

## When this is the right backend

- **Eval-heavy workflows.** Per-second billing on the cheapest GPU on the market.
- **Short fine-tunes.** A 10-30 minute run on a 4090 at $0.30/hour is hard to beat.
- **Cost-bounded experimentation.** Cap your Compute Policy at a price ceiling and let the scheduler find what's available.

## When this isn't the right backend

- **Production serving.** Variable reliability hurts more than the cost savings help.
- **Compliance-sensitive workloads.** Each host is operated by an individual provider; data-residency, attestation, and audit needs aren't well-supported.
- **Multi-hour distributed training across many nodes.** The probability of one node disappearing approaches certainty as the run gets longer.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[Azure](./azure.md)**, **[GCP](./gcp.md)**, **[RunPod](./runpod.md)**, **[Modal](./modal.md)**, **[Nebius](./nebius.md)**, **[OCI](./oci.md)** — the other seven backends.

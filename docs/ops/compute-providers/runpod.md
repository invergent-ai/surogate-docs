---
title: RunPod
sidebar_position: 4
slug: /compute-providers/runpod
description: Connect RunPod as a Surogate Ops compute backend. Single-field credential; great first backend for fast iteration.
---

# RunPod

RunPod is one of the easiest backends to connect — a single API key, no IAM, no quotas to request. That makes it the right first backend for most teams: fifteen seconds from sign-up to live offers.

## Credentials Surogate needs

One value:

- **API Key**

## Get the API key

1. Sign in to **runpod.io**.
2. **Settings → API Keys → + Create API Key.**
3. **Name** — `surogate-ops`.
4. **Permission scope** — *Read & Write*. Read-only is enough to list offers but Surogate needs write to actually provision.
5. Create. Copy the value — it's shown once.

## Connect in Surogate

Compute → Cloud → **RunPod** tile. Paste the API key. Submit. Done.

The tile flips to **Connected** in seconds. Offers populate immediately.

## Supported instance types

RunPod publishes a wide catalog of GPU types across two cluster classes:

| Class | GPUs | Notes |
|---|---|---|
| **Secure Cloud** | A40, A6000, A100 40GB / 80GB, H100 80GB, H200 | Higher uptime, slightly more expensive. The default for training. |
| **Community Cloud** | Same GPU types, sourced from a community of providers | Cheaper, more variable in availability. Good for evals and short runs. |

The scheduler reads availability live from RunPod's API. Capacity in Community Cloud can flip on the order of minutes, so a queued workload may take a few retries to find an offer at a specific price.

## Verify the backend works

After connecting, the Offers panel populates within seconds. If it doesn't, two things to check:

1. **API key permission scope.** Read-only keys read offers but can't provision; create a Read & Write key.
2. **RunPod account billing.** RunPod's API gates some operations on a positive credit balance. Add credit to the RunPod account if you've never used it.

## Cost shape

RunPod prices per second of GPU use. The dashboard's per-GPU rate is what you pay; no markup from Surogate.

Practical pointers:

- **Community Cloud is cheap.** Use it for batch evals, short fine-tunes, anything where preemption-style interruption is acceptable.
- **Secure Cloud is reliable.** Use it for serving containers and production training.
- **No long-term commitments.** Unlike the hyperscalers, RunPod has no reserved-instance pricing. The on-demand rate is the rate.

## When something fails

- **Offers list empty.** Almost always the API key permission scope (Read-only). Create a Read & Write key and update the credential.
- **Workload provisions but the container fails to pull the image.** RunPod instances have variable network egress to other clouds. If you're pulling weights from `s3.studio.internal:9000` and the instance got placed in a slow-egress region, the pull may time out. Retry; the scheduler will land in a different region.
- **Sudden price spike.** Community Cloud prices vary with supply. Check the offers panel before submitting expensive runs; Compute Policies can pin you to a price ceiling.
- **`401 Unauthorized` after months of working credentials.** API key was revoked or expired on the RunPod side. Create a new key.

## When this is the right backend

- **Your first connection.** Easiest setup; gets you a working scheduler in under a minute.
- **Bursty inference traffic.** Provisioning is fast; idle cost is low.
- **Short experiments.** Per-second billing wins for runs measured in tens of minutes.
- **Cost-conscious evals.** Community Cloud is the cheapest GPU you can buy for short, interruptible workloads.

## When this isn't the right backend

- **Compliance-heavy workloads.** Community Cloud is provider-mixed; if your data has residency or attestation requirements, use a hyperscaler.
- **Multi-month reserved capacity.** RunPod doesn't offer it. The hyperscalers do.
- **Specific instance type availability.** RunPod's catalog is broad but not as deep as AWS / Azure / GCP for some niche GPU types.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[Azure](./azure.md)**, **[GCP](./gcp.md)**, **[Modal](./modal.md)**, **[Nebius](./nebius.md)**, **[OCI](./oci.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.

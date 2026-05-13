---
title: Modal
sidebar_position: 5
slug: /compute-providers/modal
description: Connect Modal as a Surogate Ops compute backend. Token-based auth; cold-start optimisation built in.
---

# Modal

Modal is a serverless-GPU platform. Compared to the hyperscalers, the model is different: instances spin up on demand in seconds, run their workload, and shut down. That's a great fit for bursty inference and short evals; less ideal for steady-state serving.

## Credentials Surogate needs

Three values from Modal:

- **Token ID**
- **Token Secret**
- **Environment** — the Modal workspace / environment identifier.

## Get the credentials

1. Sign in to **modal.com**.
2. **Account → API Tokens → New token.**
3. **Name** — `surogate-ops`.
4. **Scope** — *Read & write*.

The Token ID and Token Secret are displayed once. Copy both.

The **Environment** value is the name of the Modal environment you want Surogate to schedule under. Most accounts have one called `main` by default; check at **Account → Environments**.

## Connect in Surogate

Compute → Cloud → **Modal** tile. Paste:

- Token ID
- Token Secret
- Environment

Submit. The tile flips to **Connected**.

## Supported instance types

Modal exposes GPU types through their function-decorator interface. Surogate maps them to its workload kinds:

| GPU | Notes |
|---|---|
| **A100 40GB / 80GB** | Standard for training and large-model serving. |
| **H100 80GB** | Top-end for current workloads. |
| **T4 16GB / L4 24GB** | Cheap for smaller serving and evals. |

The scheduler queries Modal's API for current availability. Modal generally has high availability across the popular GPU types.

## Cold starts and the serverless tradeoff

Modal's main differentiator is the function-style cold start. The first call to a freshly-imported model loads the weights into the GPU; subsequent calls within a warm window reuse the loaded weights. This is great when you have unpredictable traffic — you're not paying for idle GPU between bursts.

For Surogate workloads:

- **Serving containers** — Modal serving keeps the container warm during traffic windows and tears down during idle. Latency for the first call after a tear-down is higher; for everything else it's competitive.
- **Training runs** — provisioning is fast (often under a minute). Mid-run preemption is uncommon but possible; checkpoint frequently.
- **Eval jobs** — Modal is excellent for these. The provision-run-tear-down pattern fits eval timing perfectly.

## Verify the backend works

After connecting, the Offers panel populates within a minute. If empty:

1. **Token scope.** Read & write is required to provision. Read-only lists offers but blocks provisioning.
2. **Environment name.** A typo in the environment field means Surogate authenticates but can't find anywhere to schedule. Check at **Account → Environments**.
3. **Modal account billing.** New accounts have a small free quota; beyond that, payment must be configured on the Modal side.

## Cost shape

Modal prices per second. The bill is gpu-seconds × per-second rate; no idle cost when there's no traffic.

Practical pointers:

- **Lean on serverless for inference.** Modal's pricing model rewards bursty traffic patterns.
- **Mind the cold start.** First call after idle pays the load latency; subsequent calls don't.
- **Limit concurrent runs via Compute Policy.** Modal's API doesn't enforce a hard cap by default; a runaway scheduler could spin up many parallel workloads. Cap via policy.

## When something fails

- **`401 invalid_credentials`.** Token rotated on Modal's side. Generate a new one and update the credential.
- **Workload fails immediately with "no GPU available in environment".** Either the GPU type isn't available in this environment, or you've hit a concurrency limit. Try a different GPU type or wait for a concurrent workload to finish.
- **Serving container's first call is very slow.** Cold start. Subsequent calls should be fast; if they aren't, the model is genuinely too slow on the chosen GPU type — pick a bigger one.
- **Modal billing alert mid-run.** Modal sends billing alerts as you approach a credit threshold. Surogate doesn't intercept these; configure them on the Modal account and respond there.

## When this is the right backend

- **Bursty inference.** Serverless billing is the right shape.
- **Short evals.** Eval kind workloads land here cleanly.
- **Cost-sensitive experiments.** Per-second billing on a small GPU is hard to beat.

## When this isn't the right backend

- **Steady serving traffic.** Reserved capacity on a hyperscaler is cheaper at sustained load.
- **Multi-hour training runs.** Possible but not Modal's sweet spot; the hyperscalers or RunPod's Secure Cloud are more natural.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[Azure](./azure.md)**, **[GCP](./gcp.md)**, **[RunPod](./runpod.md)**, **[Nebius](./nebius.md)**, **[OCI](./oci.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.

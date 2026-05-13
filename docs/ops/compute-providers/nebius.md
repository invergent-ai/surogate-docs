---
title: Nebius
sidebar_position: 6
slug: /compute-providers/nebius
description: Connect Nebius as a Surogate Ops compute backend. Key-pair auth, EU-hosted H100 / H200 capacity.
---

# Nebius

Nebius is an EU-hosted GPU cloud focused on AI workloads. It's a strong fit for teams with data-residency requirements that rule out US-based clouds, and the H100 / H200 supply is often more available than the hyperscalers' at competitive prices.

## Credentials Surogate needs

Three values:

- **Service Account ID**
- **Public Key ID**
- **Private key** — uploaded as a `.pem` file.

## Set up the service account

The Nebius authentication model is key-pair based, similar to OCI.

1. Sign in to the **Nebius console**.
2. **IAM → Service accounts → Create service account.**
3. **Name** — `surogate-ops-scheduler`.
4. Create.

Copy the Service Account ID from the new account's overview page.

### Grant compute permissions

Same page → **Permissions tab → Add role binding**:

- **Role** — *Compute administrator* (or a custom role with `compute.instances.create` and read on metadata).

### Generate the key pair

Either generate on your machine and upload the public key, or have Nebius generate the pair and download both:

- On your machine: `ssh-keygen -t rsa -b 4096 -m PEM -f surogate-nebius.pem`. The public key is in `surogate-nebius.pem.pub`.
- In console: **Service account → Keys → Add key → Authorized key**. Upload the public key, or download the auto-generated pair.

After upload, copy the Public Key ID from the keys list.

## Connect in Surogate

Compute → Cloud → **Nebius** tile. Provide:

- Service Account ID
- Public Key ID
- Private key (`.pem` file upload)

Submit. The tile flips to **Connected**.

## Supported instance types

Nebius's GPU offering is concentrated on a few high-end SKUs:

| Family | GPUs | Notes |
|---|---|---|
| **gpu-h100-sxm** | H100 80GB | The bread-and-butter for training. |
| **gpu-h200-sxm** | H200 141GB | Newer; larger memory makes 70B+ training easier. |
| **gpu-a100-sxm** | A100 80GB | Mature option for training and large-model serving. |
| **gpu-l40s** | L40S 48GB | Cost-effective serving for smaller models. |

Multi-GPU instances (4×, 8×) are available for distributed training. The scheduler reads availability from the Nebius API.

## Verify the backend works

After connecting, the Offers panel populates within a minute. If empty:

1. **Key authorisation.** The most common cause — the public key wasn't actually authorised on the service account. Double-check the keys tab on the service account.
2. **Region.** Nebius primarily serves EU regions; configure the regions you have capacity in.
3. **Quota.** Nebius gates higher-end SKUs on account verification. Reach out to Nebius support if H100 / H200 don't appear.

## Cost shape

You pay Nebius at their published rates. Spot-style discount tiers exist:

- **Reserved** — committed capacity at the lowest rates. Useful for steady-state serving.
- **On-demand** — standard hourly billing.
- **Spot** — preemptible, ~50% discount on on-demand. Use for training where checkpointing handles preemption.

## When something fails

- **Offers list empty.** Key authorisation failed silently. Open the service account in Nebius, confirm the public key is listed and active.
- **"InvalidSignature".** The private key uploaded to Surogate doesn't match the public key authorised on Nebius. The two must be a real pair — regenerate fresh if you're not sure.
- **Workload stays Provisioning.** Region capacity for H100 / H200 fluctuates; the scheduler will retry. If it stalls, try a different region.
- **Service account billing limit hit.** Nebius enforces account-level spend limits that can stop provisioning even with valid credentials. Check the billing tab on the Nebius side.

## When this is the right backend

- **EU data-residency requirements.** Nebius is one of the few GPU clouds with explicit EU-only hosting.
- **H100 / H200 supply.** When the hyperscalers say "we'll get back to you" on H100 quota, Nebius often has stock.
- **Cost-conscious training.** Spot rates on H100 are aggressive.

## When this isn't the right backend

- **US-based latency-sensitive serving.** EU hosting means a transatlantic hop. Use a US-based backend for US end users.
- **Highly specific instance types not in Nebius's catalog.** Their catalog is narrower than the hyperscalers'.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[Azure](./azure.md)**, **[GCP](./gcp.md)**, **[RunPod](./runpod.md)**, **[Modal](./modal.md)**, **[OCI](./oci.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.

---
title: GCP
sidebar_position: 3
slug: /compute-providers/gcp
description: Connect Google Cloud as a Surogate Ops compute backend. Service account JSON, supported instance types, troubleshooting.
---

# GCP

Google Cloud is one of the eight Surogate Ops compute backends. The credential flow is "create a service account, download a JSON key" — clean and well-documented on Google's side.

## Credentials Surogate needs

Two values:

- **Project ID** — the GCP project workloads bill to.
- **Service Account Key (JSON)** — the full JSON file from the service account, pasted or browsed in.

## Set up the service account

The four-step path from a fresh GCP project to a working credential:

### 1. Create the service account

Google Cloud Console → **IAM & Admin → Service accounts → Create service account**.

- **Name** — `surogate-ops-scheduler`.
- **Description** — `Schedules GPU workloads from Surogate Ops`.

Click **Create and continue**.

### 2. Grant roles

The service account needs to provision Compute Engine instances and read instance type metadata. Grant:

- **Compute Admin** (`roles/compute.admin`) — provisions and manages instances.
- **Service Account User** (`roles/iam.serviceAccountUser`) — required when instances run with attached service accounts.

Click **Done**.

### 3. Create the key

Open the service account's detail page → **Keys → Add key → Create new key → JSON**. The browser downloads the key file.

This file is the credential. Store it like a password — anyone with this file can spin up GPU instances on your bill.

### 4. Note the project ID

From the console's project picker at the top of the page, or from **IAM & Admin → Settings**.

## Connect in Surogate

Compute → Cloud → **GCP** tile.

- Paste the **Project ID**.
- For the **Service Account Key**, either paste the JSON content directly into the textarea, or browse the file from disk.

Submit. The tile flips to **Connected**.

## Supported instance types

GCP's GPU-equipped instance families that Surogate schedules against:

| Family | Typical GPUs | Best for |
|---|---|---|
| **A3** (a3-highgpu-8g, a3-megagpu-8g) | H100 80GB | Top-end. Eight H100s per instance is standard. |
| **A2** (a2-highgpu-1g … a2-megagpu-16g) | A100 40GB / 80GB | Training and serving across a wide range of sizes. |
| **G2** (g2-standard-*) | L4 24GB | Cheap serving for 7B–13B models. |
| **N1 with attached T4 / P100** | T4, P100 | Legacy. Use only if you have no other choice. |

The scheduler reads instance-type availability from the Compute API per region. Sizes you don't have quota for don't appear.

## Verify the backend works

After connecting, open the GCP backend's detail page. The **Offers** panel should populate within a minute.

If empty:

1. **Quota.** GPU quotas in GCP are project-level and region-level, both starting at zero. **IAM & Admin → Quotas →** filter to *GPUs (all regions)* and the specific *NVIDIA A100*, *NVIDIA H100*, etc. lines. Request a non-zero quota for the regions you care about.
2. **Region.** Broaden under the backend's settings.
3. **Roles.** *Compute Admin* covers what Surogate needs. *Compute Viewer* alone won't let the scheduler provision.

## Cost shape

You pay GCP at published rates. Surogate adds nothing.

Practical pointers:

- **Spot VMs save 60–91%.** GCP spot pricing is the most aggressive of the hyperscalers. Use spot for training where checkpointing handles preemption.
- **Sustained-use discounts and committed-use discounts** apply on the GCP side and reduce your bill without changing Surogate's offer prices.
- **Same-region everything.** Workload pulling weights from Cloud Storage in a different region pays inter-region egress; significant at training scale.

## When something fails

- **Offers list empty.** GPU quota. Request via **IAM & Admin → Quotas**.
- **"PERMISSION_DENIED on compute.instances.insert".** Service account roles too narrow. Grant *Compute Admin* and *Service Account User*, retry.
- **"Project not found".** Project ID is wrong, or the service account belongs to a different project. Service accounts are project-scoped; the project the SA lives in must match the project ID you entered.
- **Workload stays Provisioning forever.** Either quota was approved but capacity is exhausted in the region (cancel and retry), or the zone you got placed in lacks the GPU family. The scheduler will eventually rotate; if it doesn't, broaden region settings.
- **Key file rejected as malformed.** GCP keys must be the full JSON object including `"type": "service_account"`. If you pasted only one field by accident, retry with the full file content.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[Azure](./azure.md)**, **[RunPod](./runpod.md)**, **[Modal](./modal.md)**, **[Nebius](./nebius.md)**, **[OCI](./oci.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.

---
title: Azure
sidebar_position: 2
slug: /compute-providers/azure
description: Connect Azure as a Surogate Ops compute backend. Service principal setup, supported VM sizes, troubleshooting.
---

# Azure

Azure is the second of the eight cloud backends Surogate Ops supports. The credential model is the heaviest of the eight — a service principal with four values — but the operational story is solid once you're past setup.

## Credentials Surogate needs

Four values, all from the same service principal:

- **Tenant ID** — your Azure AD tenant.
- **Subscription ID** — which subscription the workloads bill to.
- **Client ID** — the service principal's application id.
- **Client Secret** — the service principal's password.

## Set up the service principal

Three places to visit, in order:

### 1. Azure AD → register an application

Azure Portal → **Microsoft Entra ID → App registrations → New registration**.

- **Name** — `surogate-ops-scheduler`.
- **Supported account types** — *Accounts in this organizational directory only*.
- **Redirect URI** — leave blank.

Register. The new application's overview page shows your **Client ID** and **Tenant ID**.

### 2. Create the client secret

On the same application page:

- **Certificates & secrets → Client secrets → + New client secret.**
- **Description** — `surogate-ops`.
- **Expires** — pick a sensible window; 12 or 24 months is typical.

Create. The secret **Value** is shown once and never again. Copy it now.

### 3. Grant the service principal contributor on the subscription

Switch to **Subscriptions** in the Azure Portal:

- Pick the subscription Surogate will schedule against.
- **Access control (IAM) → + Add → Add role assignment.**
- **Role** — *Contributor*.
- **Members** — search for the application name you registered, select it.
- Review and assign.

Copy the **Subscription ID** from the subscription's overview page.

## Connect in Surogate

Compute → Cloud → **Azure** tile. Paste:

- Tenant ID
- Subscription ID
- Client ID
- Client Secret

Submit. The tile flips to **Connected**.

The form has a deep-link to the Azure Portal for finding each value. Use it; copying GUIDs by hand is the most common source of credential errors.

## Supported VM sizes

Azure exposes GPU VMs across several series. Surogate's scheduler maps them by GPU type:

| Series | Typical GPUs | Best for |
|---|---|---|
| **ND H100 v5** | H100 80GB | Top-end training and serving. |
| **ND A100 v4** | A100 40GB / 80GB | Training and serving large models. |
| **NC A100 v4** | A100 80GB | Single-GPU training, mid-size serving. |
| **NC T4 v3** | T4 16GB | Cheap serving for small models. |

Surogate reads the available SKU list from Azure's Compute API. Sizes you don't have quota for in the chosen region don't appear in the offers list.

## Verify the backend works

After connecting, open the Azure backend's detail page. The **Offers** panel should populate within a minute with GPU SKUs across the regions you have quota in.

If empty:

1. **GPU quota.** Azure gates GPU SKUs separately from regular compute. Open Azure Portal → **Subscriptions → Usage + quotas** → filter to GPU SKUs → request a non-zero quota in the regions you care about.
2. **Region.** Surogate queries a default region set. Broaden under the backend's settings to reach SKUs that only exist in certain regions.
3. **Role assignment.** *Contributor* on the subscription is sufficient; *Reader* alone is not. If the service principal accidentally got only Reader, the offers query returns empty.

## Cost shape

You pay Azure at their published rates. Surogate doesn't add a margin.

Practical pointers:

- **Spot is cheap.** Azure spot VMs save 60–80% but can be evicted. Set Compute Policy to prefer spot for training, on-demand for serving.
- **Reservations apply.** Azure Reserved VM Instances and Savings Plans hit the bill but don't change Surogate's offer prices.
- **Egress matters.** Pulling models out of Azure to another cloud bills egress. Keep training and serving in the same region when you can.

## When something fails

- **Offers list empty.** GPU quota is the usual culprit. The Azure quota dashboard tells you exactly which SKUs in which regions you can use.
- **"InvalidAuthenticationTokenTenant".** The Tenant ID doesn't match the Subscription's tenant. The service principal lives in one tenant; the subscription is associated with one tenant. They must match.
- **"AuthorizationFailed" on instance create.** Service principal role is too narrow. Add *Contributor* on the subscription or, for tighter security, *Virtual Machine Contributor* + *Network Contributor*.
- **Workload stays Provisioning forever.** Region capacity for the requested SKU is exhausted. Cancel and resubmit; the scheduler tries another region.
- **Client Secret expired silently.** Azure secrets have a hard expiry. Set a calendar reminder a week before the secret's expiry, rotate it via App registration → Certificates & secrets.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[GCP](./gcp.md)**, **[RunPod](./runpod.md)**, **[Modal](./modal.md)**, **[Nebius](./nebius.md)**, **[OCI](./oci.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.

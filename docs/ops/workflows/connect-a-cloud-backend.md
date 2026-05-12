---
title: Connect a cloud backend
sidebar_position: 6
slug: /workflows/connect-a-cloud-backend
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Connect a cloud backend

This workflow plugs one of the eight supported cloud providers into your project so Surogate can run serving containers and training jobs on it.

<video controls width="720" muted>
  <source src="/videos/08-connect-cloud.webm" type="video/webm" />
</video>

## Prerequisites

- A working account on the target provider with at least one GPU quota.
- The provider-specific credentials below.
- Project role `editor` or higher, or system role `devops`.

## Steps

1. Switch to **Develop** mode (top-right toggle).
2. Open **/studio/compute/cloud**.
3. Click the tile for your provider, or click **Connect Cloud** in the page header. Either path navigates to `/studio/connect-cloud?provider=<name>`.
4. Fill the provider-specific credential form (see below).
5. Submit. The form returns to `/studio/compute/cloud` and the new backend shows as connected.
6. Open `/studio/backend-offers?backend=<name>` to confirm at least one GPU offer is visible. An empty offers list usually means missing IAM read permissions or no GPU quota.

## Credentials per provider

Each provider's POST endpoint is implemented in `surogate_ops/server/routes/compute.py`. Every page has a **Back to Cloud** action top-left, a deep-link to the provider's own console (labeled `<Provider> Console` or similar), and **Cancel** / **Connect** at the bottom.

### Amazon Web Services — `?provider=aws`

Page header: **Connect Amazon Web Services**. External link: **AWS Console**.

| Field | Type |
|---|---|
| **Access Key ID** | text |
| **Secret Access Key** | password |

### Microsoft Azure — `?provider=azure`

Page header: **Connect Microsoft Azure**. External link: **Azure Portal**.

| Field | Type |
|---|---|
| **Tenant ID** | text |
| **Subscription ID** | text |
| **Client ID (Application ID)** | text |
| **Client Secret** | password |

### Google Cloud Platform — `?provider=gcp`

Page header: **Connect Google Cloud Platform**. External link: **Google Cloud Console**. Has a **Browse** action to upload a JSON key file.

| Field | Type |
|---|---|
| **GCP Project ID** | text |
| **Service Account Key (JSON)** | text (paste or upload via Browse) |

### RunPod — `?provider=runpod`

Page header: **Connect RunPod**. External link: **RunPod Console**.

| Field | Type |
|---|---|
| **API Key** | password |

### Modal — `?provider=modal`

Page header: **Connect Modal**. External link: **modal.com**.

| Field | Type |
|---|---|
| **Token ID** | text |
| **Token Secret** | password |
| **Environment** | text |

### Nebius — `?provider=nebius`

Page header: **Connect Nebius**. External link: **Nebius Console**.

| Field | Type |
|---|---|
| **Service Account ID** | text |
| **Public Key ID** | text |
| **Private key .pem file** | file upload |

### Oracle Cloud Infrastructure — `?provider=oci`

Page header: **Connect Oracle Cloud Infrastructure**. External link: **OCI Console**.

| Field | Type |
|---|---|
| **User OCID** | text |
| **Tenancy OCID** | text |
| **Fingerprint** | text |
| **Home Region** | text |
| **Private Key (.pem)** | file upload |

### Vast.ai — `?provider=vastai`

Page header: **Connect Vast.ai**. External link: **Vast.ai Console**.

| Field | Type |
|---|---|
| **API Key** | password |

For the providers that use long-lived secrets (AWS, Azure, GCP, Modal, OCI), the credential is stored encrypted via the [Credential](../concepts/core-objects.md#credential) object and never displayed afterward.

## Verifying the connection

- The provider tile on `/studio/compute/cloud` shows a "connected" badge with the account name.
- `/studio/backend-offers?backend=<name>` lists at least one offer.
- A test deploy ([Workflow — Deploy a model](./deploy-a-model.md)) succeeds, picking a GPU from the new backend.

## What you cannot configure here

- Spend caps. Use [Compute → Policies](../features/compute.md#policies-tab).
- Region allow-lists. Same — Policies.

## Disconnecting

From the Cloud tab, open the backend's tile and pick Disconnect. The credential record is retained so historical jobs trace correctly, but no new workloads will be scheduled there.

## If something fails

- **403 from the provider** on submit — the credential is missing required permissions. Surogate needs read on instance-type metadata + write on instance/volume creation at minimum. Cross-check the provider's IAM docs.
- **The form saves but the tile shows zero offers** — propagation can take a few minutes for some providers. If still zero after 10 minutes, the account has no GPU quota in the queried regions.
- **A previously connected backend disappeared** — its credential was revoked or expired upstream. Re-enter the credential to restore.

## Related

- [Compute](../features/compute)
- [Models](../features/models)
- [Workflow — Deploy a model](./deploy-a-model)

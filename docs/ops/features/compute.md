---
title: Compute
sidebar_position: 3
slug: /features/compute
---

# Compute

Compute is what ties Surogate Ops to actual machines. Serving containers, training runs, eval jobs, synthetic-data pipelines — every workload draws from the cloud accounts you connect here.

The Compute page has three sub-views: **Cloud** (connected backends), **Workload Queue** (running and queued jobs), and **Policies** (allocation rules).

## Connect a cloud backend

Compute → **Cloud** → click a provider tile (or **Connect Cloud**). Eight providers are supported: AWS, Azure, GCP, RunPod, Modal, Nebius, OCI, Vast.ai.

Each provider's credential form differs. The full per-provider list is below.

| Provider | Fields |
|---|---|
| **AWS** | Access Key ID, Secret Access Key |
| **Azure** | Tenant ID, Subscription ID, Client ID, Client Secret |
| **GCP** | Project ID, Service Account Key (JSON, paste or browse) |
| **RunPod** | API Key |
| **Modal** | Token ID, Token Secret, Environment |
| **Nebius** | Service Account ID, Public Key ID, Private key (.pem upload) |
| **OCI** | User OCID, Tenancy OCID, Fingerprint, Home Region, Private Key (.pem upload) |
| **Vast.ai** | API Key |

Each form has a deep-link to the provider's own console (AWS Console, Azure Portal, etc.) for finding the values. Submit. The form returns to Cloud with the new backend marked connected.

**Verify it worked.** Open Compute → Backend Offers for that backend. If you see at least one GPU offer, you're done. Empty offers usually means missing IAM read on instance-type metadata, or no GPU quota in the queried regions.

## Workload Queue

Train runs, eval jobs, serving containers, synthetic generators — they all land here. Filter pills at the top: `all · sft · grpo · serving · eval · task · synthetic`. Each pill shows a live count.

Columns: **Pri**, **Workload**, **Type**, **Status**, **GPU**, **Location**, **Progress / ETA**, **Requested By**, and a trailing row-actions menu (Cancel, View logs).

Status goes `Queued → Provisioning → Running → Completed / Failed / Cancelled`.

## Policies

A Policy bounds where workloads can run — allowed backends, regions, instance types, spend caps, schedule windows. Policies are evaluated before a workload is scheduled; violations land the workload in **Error** with a Guardrail alert and never enter the queue.

Compute → Policies → **+ New Policy** opens the editor. The action is admin-only — non-admins see the button but clicking it is a no-op.

## When something fails

- **A connected backend lists zero offers.** Credentials are valid but the IAM role lacks instance-type metadata read, or the account has no GPU quota in the regions Surogate queries.
- **Workload stays Queued forever.** No backend has capacity for the requested GPU. Loosen the GPU requirement, or connect a provider with stock.
- **Workload fails to provision.** Open the row menu → View logs. Most often a transient provider error; retry usually clears it.

## Where to go next

- **[Models](./models.md)** — where serving workloads originate.
- **[Training Runs](./training.md)** — where SFT / GRPO workloads originate.

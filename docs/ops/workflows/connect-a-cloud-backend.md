---
title: Connect a cloud backend
sidebar_position: 6
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Connect a cloud backend

This workflow plugs one of the eight supported cloud providers into your project so Surogate can run serving containers and training jobs on it.

<video controls width="720" muted>
  <source src="/videos/08-connect-cloud.webm" type="video/webm" />
</video>

## Prerequisites

- A working account on the target provider with at least one GPU quota.
- Provider credentials in hand. The form differs per provider — see the **Credentials per provider** table below.
- Project role `editor` or higher, **or** system role `devops`. TODO(verify the exact role gate).

## Steps

1. Switch to **Develop** mode (top-right toggle).
2. Open **/studio/compute/cloud**.
3. Click the tile for your provider, or click **Connect Cloud** in the page header. Either path navigates to `/studio/connect-cloud?provider=<name>`.
4. Fill the provider-specific credential form (see the table).
5. Submit. The form returns to `/studio/compute/cloud`, with the new backend listed as connected.
6. Optional: open `/studio/backend-offers?backend=<name>` to confirm at least one GPU offer is visible. An empty offers list usually means missing IAM read permissions or no GPU quota.

## Credentials per provider

Each provider's POST endpoint is implemented in `surogate_ops/server/routes/compute.py`. Form fields TODO(verify) — observed signatures suggest:

| Provider | Auth model | Typical fields |
|---|---|---|
| AWS | IAM access key | Profile name, Access key ID, Secret access key, default Region |
| Azure | Service principal | Tenant ID, Client ID, Client secret, Subscription ID |
| GCP | Service account JSON | Project ID, Service account key (paste JSON) |
| RunPod | API token | Token |
| Modal | Token + workspace | Token, Workspace |
| Nebius | Service account | Project ID, Service account ID, Authorized key |
| OCI | User OCID + key | Tenancy OCID, User OCID, Region, Private key (paste PEM), Fingerprint |
| Vast.ai | API token | Token |

For the providers that use long-lived secrets (AWS, GCP, OCI), the credential is stored encrypted via the [Credential](../concepts/core-objects#credential) object and never displayed afterward.

## Verifying the connection

After saving:

- The provider tile on `/studio/compute/cloud` shows a "connected" badge with the account name.
- `/studio/backend-offers?backend=<name>` lists at least one offer.
- A test deploy ([Workflow — Deploy a model](./deploy-a-model)) succeeds, picking a GPU from the new backend.

## What you cannot configure here

- Spend caps. Use [Compute → Policies](../features/compute#policies-tab).
- Region allow-lists. Same — Policies.
- Per-team quotas. TODO(verify whether project-level allocation rules exist).

## Disconnecting

From the Cloud tab, open the backend's tile and pick Disconnect. TODO(verify the exact menu). The credential record is retained so historical jobs trace correctly, but no new workloads will be scheduled there.

## If something fails

- **403 from the provider** on submit — the credential is missing required permissions. Cross-check the provider's documentation; Surogate needs read on instance-type metadata + write on instance/volume creation at minimum.
- **The form saves but the tile shows zero offers** — propagation can take a few minutes for some providers. Click **Refresh** (TODO(verify the affordance)). If still zero after 10 minutes, the account likely has no GPU quota.
- **A previously connected backend disappeared** — its credential was revoked or expired upstream. Re-enter the credential to restore.

## Related

- [Compute](../features/compute)
- [Models](../features/models)
- [Workflow — Deploy a model](./deploy-a-model)

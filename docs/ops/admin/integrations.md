---
title: Integrations
sidebar_position: 2
slug: /admin/integrations
---

# Integrations

Third-party connections used across Surogate Ops: model providers, the Data Hub, identity providers, observability sinks. Each integration stores one or more **Credentials** that other parts of Surogate Ops reference by name.

The Integrations tab is hidden from the Settings sidebar for non-admin accounts. You'll see it when you have the admin permission set.

## Add an integration

Admin → Integrations. Find the row for the integration you want, click **Connect**. The provider-specific credential form opens; fill it and save. The credential is encrypted at rest and only its name is shown afterwards.

## Disconnect

Click **Disconnect** on the row. The credential record is retained so historical jobs can trace what they used, but no new wiring will reference it.

## Where credentials show up elsewhere

- **Model providers** — proxied models in [Build → Models](../features/models.md) reference these for upstream calls.
- **Cloud backends** — managed under [Operate → Compute](../features/compute.md), not here. Each backend has its own credential form.
- **Hub auth** — the **Data Hub** tab at Settings → Data Hub stores your Hub credentials. If those are missing, [Data Hub](../features/hub.md) shows zero repos even when content exists.

## Where to go next

- **[Models](../features/models.md)** — what credentials power proxied models.
- **[Compute](../features/compute.md)** — for cloud-backend credentials.
- **[Data Hub](../features/hub.md)** — for Hub auth.

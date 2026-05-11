---
title: Integrations
sidebar_position: 2
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Integrations

## What it does

`/studio/settings/integrations` lists third-party connections used by your project: model providers, the Data Hub, identity providers, observability sinks. Each connection stores one or more **Credentials** that other parts of the app reference by name.

> **Hidden for non-admin accounts.** The **Integrations** tab is not visible in the Settings sidebar for project-`viewer`-only accounts during documentation. The page is reachable by URL with limited actions. _TODO(verify visibility per system role._

## Adding an integration

1. Open **/studio/settings/integrations**.
2. Find the row for the integration you want and click **Connect**.
3. Fill in the credentials (provider-specific form). _TODO(verify per integration._
4. Save. The credential is encrypted at rest and only its **name** is shown afterwards.

## Disconnecting

Click **Disconnect** on the row. Surogate keeps the credential record (so historical jobs can still trace it) but removes any active wiring. _TODO(verify._

## Where credentials are used

- **Model providers** — proxied models reference these to make upstream calls.
- **Cloud backends** — but these are managed under [Compute → Connect Cloud](../features/compute), not here.
- **Data Hub** — see the dedicated [Data Hub configuration](#data-hub-config) below.
- **Webhooks / observability** — _TODO(verify the list._

## Data Hub config

The **Data Hub** has its own tab at `/studio/settings/hub` (and `/work/settings/hub`). It stores:

- The Hub endpoint URL (defaults to the internal Hub).
- Your Hub **API key** and **API secret** (`hub_key` / `hub_secret` on the User).

If these are missing, the [Data Hub](../features/hub) home shows zero repositories even when content exists. Re-enter the credentials and refresh.

## Related

- [Reference → Permissions matrix](../reference/permissions-matrix)
- [Compute](../features/compute) — for cloud-backend credentials.
- [Data Hub](../features/hub)

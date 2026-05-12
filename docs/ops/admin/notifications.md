---
title: Notifications
sidebar_position: 3
slug: /admin/notifications
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Notifications

## What it does

`/studio/settings/notifications` (and the equivalent **/work/settings/notifications**) is where notification preferences live — what triggers an email / webhook / in-app banner, and for whom.

> **Tab hidden for non-admin accounts.** The page is reachable by URL with limited content for project-`viewer`-only users observed during documentation. _TODO(verify visibility per system role._

## What you can configure

_TODO(verify exact controls — the page renders for the documentation account but the visible-only filter didn't catch checkboxes/toggles. Common Notification page contents likely include:_

- **Alert categories** (5xx errors, latency breaches, training failures, guardrail hits).
- **Severity thresholds** (warn vs critical).
- **Delivery channels** (in-app, email, webhook).
- **Quiet hours** / weekday filters.
- **Test send** button to verify the wiring.

## Per-user vs project-wide

Notifications can be configured **per user** (your own preferences) or **per project** (everyone on the project receives this). _TODO(verify which axis the page exposes._

## Related

- [Monitoring](../features/monitoring) — where alerts originate.
- [Integrations](./integrations) — webhook destinations are configured there.

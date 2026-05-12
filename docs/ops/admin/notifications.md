---
title: Notifications
sidebar_position: 3
slug: /admin/notifications
---

# Notifications

Configure who gets paged when something goes wrong: 5xx errors, latency breaches, guardrail hits, training failures.

The Notifications tab is hidden from the Settings sidebar for non-admin accounts. Reach it by URL with limited content, or be `admin`.

## What you can configure

Notification preferences cover:

- **Alert categories** — 5xx errors, latency breaches, training failures, guardrail hits.
- **Severity thresholds** — warn vs critical.
- **Delivery channels** — in-app, email, webhook (webhook destinations are configured in [Integrations](./integrations.md)).
- **Quiet hours** and weekday filters.
- **Test send** to verify the wiring.

## Per-user vs per-project

Notifications split into two axes:

- **Per-user** — your own preferences. Affects what you receive.
- **Per-project** — defaults for everyone on the project. New members inherit these unless they override.

## Where to go next

- **[Monitoring](../features/monitoring.md)** — where alerts originate.
- **[Integrations](./integrations.md)** — webhook destinations live there.

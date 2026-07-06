---
title: Notifications
sidebar_position: 5
---

# Notifications

Choose which platform events reach you, and over which channel, at `/work/settings/notifications` (shared with Dev mode at `/studio/settings/notifications`).

Each event type has two independent toggles — **Email** and **In-App** — grouped into four categories. Flip either switch per row.

## Deployments

| Event | Email | In-App |
|---|---|---|
| **Agent deployment succeeded** | On | On |
| **Agent deployment failed** | On | On |
| **Model serving started/stopped** | Off | On |
| **Auto-scaling events** | Off | On |

## Training

| Event | Email | In-App |
|---|---|---|
| **Training run completed** | On | On |
| **Training run failed** | On | On |
| **Checkpoint saved** | Off | On |
| **Evaluation completed** | Off | On |

## Monitoring

| Event | Email | In-App |
|---|---|---|
| **Critical alerts (agent down)** | On | On |
| **Warning alerts (high latency)** | Off | On |
| **Error rate spike** | On | On |
| **Budget threshold reached** | On | On |

## Conversations

| Event | Email | In-App |
|---|---|---|
| **Flagged conversation** | Off | On |
| **Escalation triggered** | On | On |

The **On/Off** columns above are the defaults shown for each event. Toggle **Email** and **In-App** independently to match how you want to be reached.

---
title: Monitoring
sidebar_position: 1
slug: /features/monitoring
---

# Monitoring

The live ops view for your deployed agents. Counters update via a WebSocket the app opens at sign-in; you don't have to refresh. Open it when you want to know what's happening *right now*.

## What the page shows

- **Top counters.** Total RPS, P95 latency, error rate, token usage rate.
- **Request Rate chart.** RPS over the chosen time window, stacked by agent.
- **Agent Health table.** One row per agent — RPS, P50/P95/P99, error count, CPU, MEM, sparkline. Static columns; no click-to-sort in this snapshot.
- **Alerts feed.** Live. Each alert is severity, agent or model, one-line reason. Click an alert to jump into the offending session.
- **Latency Distribution heatmap.** Rows are latency buckets, columns are time slices. Useful for spotting tail spikes.
- **Model Serving panel.** Per-model aggregates — useful when one model degrades across many agents.
- **Token Usage (24h).** Tokens per model. Quick budget check.

## Controls

- **Time range:** `5m · 15m · 1h · 6h · 24h · 7d`. The whole page re-aggregates on click.
- **Auto-refresh** toggle. On by default; off freezes the view at the current window.
- **⏸ Pause** halts the live stream without flipping Auto-refresh. Use it while writing an incident note.
- **Severity filter:** `All · 5xx · Timeout · Guardrail`. Narrows the agent table and the alerts feed.
- **Acknowledge** on each alert row — silences re-fire for the same root cause.

## Severity meanings

- **5xx** — the agent's serving endpoint returned an HTTP 500-series error to the proxy.
- **Timeout** — the agent didn't respond before the proxy timeout. Often a slow skill or MCP call; check the session trajectory.
- **Guardrail** — either a compute policy refused the workload, or a content guardrail intervened on a response.

## Read the heatmap

Latency Distribution is normalized per column. A dark cell at the top-right means a tail spike in the most recent slice for the highest-latency bucket. Cross-reference with the Alerts feed to find the offending agent.

## When the page stops updating

The WebSocket dropped. Counters freeze at the last value; new alerts don't appear. Refresh the tab — the socket reconnects on page load.

## Where to go next

- **[Sessions](./sessions.md)** — drill into a specific conversation that an alert points to.
- **[Reference → Errors](../reference/errors.md)** — the full error vocabulary.

---
title: Usage
sidebar_position: 3
---

# Usage

Current billing-period consumption:

| Metric | Counts |
|---|---|
| **Tokens** | LLM tokens in + out, all agents |
| **Web-browsing minutes** | Browser-tool time, summed per session |
| **ML compute hours** | Training + model-serving |
| **Storage** | KB + dataset + workspace storage |
| **Sessions** | Active + completed in the period |

Hover any metric for a per-agent breakdown.

## When you hit a limit

New requests return `429 Too Many Requests` until the next cycle. Agents stay running — they just refuse new traffic. Upgrade the plan, buy add-ons, or top-up credits in [Billing](./billing.md).

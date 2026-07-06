---
title: Integrations
sidebar_position: 7
---

# Integrations

Account-level connections to external tools, listed at `/studio/settings/integrations` in Dev mode.

These are platform-wide integrations, distinct from the per-agent tools and credentials (MCP servers, API credentials, model providers) that you configure on an individual agent. Each row shows the integration's status — **connected** (green dot) or **disconnected** — with a **Connect** or **Disconnect** button, and connected integrations reveal their key config values inline.

## Available integrations

| Integration | Purpose | Config surfaced when connected |
|---|---|---|
| **Hugging Face** | Import models and datasets from HF Hub | `token`, `org` |
| **Weights & Biases** | Training metrics and experiment tracking | `apiKey`, `project` |
| **Slack** | Alerts and notifications to Slack channels | — |
| **GitHub** | Code sync and agent flow version control | `token`, `org` |

Connected integrations display their stored config (with secrets masked, e.g. `hf_...****`) under the row. Disconnected integrations show a **Connect** button; connected ones show **Disconnect**.

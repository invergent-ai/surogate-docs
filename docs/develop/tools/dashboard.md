---
title: Develop dashboard
sidebar_position: 1
---

# Develop dashboard

The Develop-mode dashboard is at `/studio`. It's denser than the Work-mode dashboard — designed for builders monitoring their workspace.

## Top widgets

- **Active Agents** — running / deploying / error breakdown
- **Tokens today** — total LLM tokens consumed in the last 24h
- **Success Rate** — % of sessions completed without crashing or being denied
- **Per-agent live table** — agent, status, replicas, CPU, MEM, RPS, P99, model

## Lower sections

- **Serving Models** — fine-tuned models currently being served
- **Training Jobs** — active SFT / GRPO runs
- **Eval Runs** — active evaluation runs
- **Recent Conversations** — feed of recent sessions across all agents
  - Filter chips: All / Flagged / Negative

## Quick Actions

Seven buttons on the right side:

| Button | What it opens |
|---|---|
| **Deploy Agent** | Opens the DEPLOY NEW AGENT dialog (same as Agents → DEPLOY AGENT) |
| **Serve Model** | ADD MODEL dialog (Local Hub / HF / OpenRouter / URL) |
| **New Skill** | NEW SKILL form |
| **Start Training** | NEW TRAINING RUN form (SFT or GRPO) |
| **New KB** | NEW KNOWLEDGE BASE dialog |
| **New Dataset** | NEW DATASET picker |
| **New Eval** | NEW EVALUATION wizard |

These are shortcuts — each opens the same modal/wizard you'd reach by navigating to its respective module page.

## Daily ops habit

A common builder workflow:

1. Morning: open the dashboard.
2. Glance at success rate and error count. Drill into errors if any.
3. Check Recent Conversations → Flagged. Triage the worst sessions.
4. Quick Actions when something needs urgent attention (deploy a hot-fix agent, start a small fine-tune).

## What's next

[Copilot](./copilot.md) for the platform-driving agent. [Templates](./templates.md) for the deploy flow.

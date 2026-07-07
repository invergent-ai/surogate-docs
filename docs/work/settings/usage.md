---
title: Usage
sidebar_position: 3
---

# Usage

The **Usage** tab shows what your project has consumed this billing period, how much of each wallet is left, and a breakdown per agent and model. It's the real-time meter behind your plan — no end-of-month surprises.

## Wallet balances

Each consumable resource is a prepaid **wallet** (your plan grants a monthly balance; top-ups add more; usage drains it in real time). The tab shows the **remaining** balance for each:

| Wallet | What it meters |
|---|---|
| **Tokens** | LLM tokens (prompt + completion), across every agent |
| **Web-browsing minutes** | Agent browser-tool time (shown in hours), summed per session |
| **ML compute hours** | GPU time for training runs and model serving |

When a wallet is unlimited (an internal/enterprise allowance) or you're on **BYO LLM** for tokens, that balance is suppressed rather than showing a placeholder. When a wallet hits zero the operation stops — see [When you hit a limit](#when-you-hit-a-limit).

## Usage breakdown

A table breaks consumption down for the selected period. Group it by:

- **Agent × Model** — one row per (agent, model) pair
- **Model** — totals per model
- **Agent** — totals per agent

Each row shows token columns **Prompt**, **Completion**, and **Total**, so you can see exactly which agent and which model is spending your allowance.

## Hub storage

A separate section reports your project's **Hub storage**, grouped by repository type (models, datasets, skills, knowledge bases, and other). This is what counts against your plan's hub-storage allowance — see [Data Hub](/develop/features/hub) for what lives in each repo.

## When you hit a limit

When a wallet reaches zero, new requests that would draw on it return `429 Too Many Requests` until the next cycle. Running agents stay up — they just refuse new traffic on the exhausted resource. To keep going, upgrade the plan, add a recurring add-on, or drop in a wallet **top-up** — all from [Billing](./billing.md).

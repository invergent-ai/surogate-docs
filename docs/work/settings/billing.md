---
title: Billing
sidebar_position: 4
---

# Billing

## Plans

| Plan | Monthly | Agents | Tokens / mo | Workspace | Hub | Web browsing | Support |
|---|---|---|---|---|---|---|---|
| **Free** | $0 | 5 | 500K starter | 1 GB | 1 GB | 0.5 h | Community |
| **Standard** | $30 | 100 | 5M | 5 GB | 10 GB | 5 h | Email |
| **Pro** ⭐ | $72 | 500 | 11.5M | 20 GB | 50 GB | 15 h | Priority email |
| **Max** | $144 | 1,000 | 22M | 50 GB | 200 GB | 40 h | Priority |
| **Enterprise** | Custom | Custom | Custom | Custom | Custom | Custom | SSO, audit logs, RBAC, SLA |

Annual billing saves ~5% (Standard $29/mo, Pro $69/mo, Max $138/mo). **Running more agents costs nothing extra** — every plan includes its full concurrent-agent count; you pay for what agents *do* (tokens, compute), not how many you create.

## Wallets: how consumables work

Each consumable resource (tokens, web browsing, ML compute) is a **prepaid wallet**. Your plan grants a monthly balance; top-ups add more on demand; usage drains the wallet in real time. **When a wallet hits zero, the operation stops** — no surprise bills, no auto-upgrades. The plan-granted portion resets each billing cycle (use-it-or-lose-it); the top-up portion is cash you paid in and rolls over while your account is active.

## Top-ups (pay-as-you-go)

One-shot, never expire until used, consumed **before** plan allowance:

| Resource | Rate |
|---|---|
| Tokens | **$5.57 / 1M** |
| Web browsing | **$0.08 / hour** (10-hour minimum) |

## Add-ons (recurring)

Raise your monthly ceiling, renewing until removed:

| Resource | Rate |
|---|---|
| Extra workspace storage | **+$0.0605 / GB / month** |
| Custom domain for agent endpoints | included on paid plans |

## BYO LLM

When enabled, agents route LLM calls through your own provider (OpenAI, Anthropic, OpenRouter, self-hosted vLLM, anything OpenAI-compatible). You pay the provider; Surogate charges only for platform usage. Configure the provider per-agent in CONFIG → Model.

Disabled by default. The platform's bundled LLM endpoints are billed through the plan.

## Stripe Customer Portal

**Manage Subscription** opens Stripe — card, invoices, plan changes (prorated), pause / cancel. Changes propagate to the platform via webhook (usually instant, occasionally 30-60s lag).

## Monetize your agents

On Pro and above, you can charge end users for access to your public agents via Stripe Connect — see [Monetize your agents](../monetize.md). Earnings land in **your** Stripe account, not Surogate's; Surogate collects a small platform fee on each charge.

---
title: Billing
sidebar_position: 4
---

# Billing

## Plans

The plan cards in the app read their limits live from the platform's plan catalog, so what you see there is always what's enforced. For orientation:

| Plan | Monthly | Agents | Tokens / mo | Workspace | Hub | Web browsing | Compute | Media | Support |
|---|---|---|---|---|---|---|---|---|---|
| **Free** | $0 | 5 | 1M starter | 1 GB | 1 GB | 30 min | — | $1 | Community |
| **Standard** | $19 | 100 | 10M | 5 GB | 10 GB | 5 h | 3 h | $3 | Email |
| **Pro** ⭐ | $96 | 500 | 80M | 20 GB | 50 GB | 15 h | 15 h | $10 | Priority email |
| **Max** | $190 | 1,000 | 200M | 50 GB | 200 GB | 40 h | 40 h | $25 | Priority |
| **Enterprise** | Custom | Custom | Custom | Custom | Custom | Custom | Custom | Custom | SSO, audit logs, RBAC, SLA |

Annual billing saves a little (Standard $18/mo, Pro $90/mo, Max $180/mo). **Running more agents costs nothing extra** — every plan includes its full concurrent-agent count; you pay for what agents *do* (tokens, compute, browsing, media), not how many you create. "Media" is dollars of image & video generation per month (roughly 25 images or 2 short videos per $1).

The **Current plan** card shows your tier, price, and renewal date; cadence and payment live in the Stripe portal.

## Wallets: how consumables work

Each consumable resource (tokens, web browsing, compute credits, media generation) is a **prepaid wallet**. Your plan grants a monthly balance; top-ups add more on demand; usage drains the wallet in real time. **When a wallet hits zero, the operation stops** — no surprise bills, no auto-upgrades. The plan-granted portion resets each billing cycle (use-it-or-lose-it); the top-up portion is cash you paid in and rolls over while your account is active.

Media has its own wallet on purpose: a video generation can never silently drain your chat tokens, and an empty media wallet never stops your agents from chatting.

## Top-ups (pay-as-you-go)

One-shot, never expire until used, consumed **before** plan allowance:

| Resource | Rate |
|---|---|
| Tokens | **$2.00 / 1M** |
| Web browsing | **$0.08 / hour** (10-hour minimum) |
| Compute credits | **$2.00 / GPU-hour** (baseline GPU) |
| Media generation | **$2.00 per $1 of image/video generation** (chips: $5 / $20 / $50) |

## Add-ons (recurring)

Raise your monthly ceiling, renewing until removed:

| Resource | Rate |
|---|---|
| Extra workspace storage | **+$0.0605 / GB / month** |
| Custom domain for agent endpoints | included on paid plans |

## BYO LLM

When enabled, agents route LLM calls through your own provider (OpenAI, Anthropic, OpenRouter, self-hosted vLLM, anything OpenAI-compatible). You pay the provider; Surogate charges only for platform usage. Configure the provider per-agent in CONFIG → Model. The same goes for BYO image/video models — media generated through your own models isn't metered by Surogate.

Disabled by default. The platform's bundled LLM endpoints are billed through the plan.

## Stripe Customer Portal

**Manage Subscription** opens Stripe — card, invoices, plan changes (prorated), pause / cancel. Changes propagate to the platform via webhook (usually instant, occasionally 30-60s lag).

## Monetize your agents

On Pro and above, you can charge end users for access to your public agents via Stripe Connect — see [Monetize your agents](../monetize.md). Offers can bundle usage, browsing time, media credits, and feature packages, not just tokens. Earnings land in **your** Stripe account, not Surogate's; Surogate collects a **5% platform fee** per sale (plus standard Stripe processing fees).

Note the two-sided meter: when buyers use a monetized agent, their browsing and media draw their own purchased balances *and* your project wallets — price your offers above your own cost.

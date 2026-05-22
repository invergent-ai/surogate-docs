---
title: Billing
sidebar_position: 3
---

# Billing

## Plans

| Plan | Monthly | Tokens | Web-browse | ML compute | Storage | Support |
|---|---|---|---|---|---|---|
| **Standard** | $45 | 1M | 100 min | 5h | 5GB | Basic |
| **Pro** | $98 | 5M | 500 min | 25h | 25GB | Priority |
| **Max** | $192 | 25M | 2,500 min | 150h | 250GB | Enterprise |

Annual saves ~20%.

## Add-ons

Stackable on top of any plan, monthly renewing until removed:

- Extra LLM tokens (1M / 5M / 25M bundles)
- Extra ML compute (GPU hours)
- Extra storage (GB)
- Custom domain for agent endpoints

## Top-up credits

One-shot prepaid in $10 / $50 / $200 / $1,000 chunks. Consumed **before** plan tokens — a $200 top-up effectively delays your plan from hitting its cap by ~$200 worth of usage.

## BYO LLM

When enabled, agents route LLM calls through your own provider (OpenAI, Anthropic, OpenRouter, self-hosted vLLM, anything OpenAI-compatible). You pay the provider; Surogate charges only for platform usage. Configure the provider per-agent in CONFIG → Model.

Disabled by default. The platform's bundled LLM endpoints are billed through the plan.

## Stripe Customer Portal

**Manage Subscription** opens Stripe — card, invoices, plan changes (prorated), pause / cancel. Changes propagate to the platform via webhook (usually instant, occasionally 30-60s lag).

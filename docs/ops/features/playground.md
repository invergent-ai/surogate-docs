---
title: Playground
sidebar_position: 4
slug: /features/playground
---

# Playground

The Playground is an ad-hoc testing surface for a single Model. No agent wrapper, no skills, no knowledge base — just the bare model behind your Surogate proxy. Use it to sanity-check a model after deploying it, or to tune a system prompt before wiring it into an agent.

## When to use it

- You deployed a model and want to confirm it responds at all.
- You're crafting a system prompt and want to iterate without redeploying an agent each time.
- You want a quick head-to-head between two model versions — open two browser tabs, point each at one model, ask the same question.

## How to use it

Operate → Playground. Pick a model from the dropdown (or arrive via `?modelId=<id>`). Type into the input, adjust sampling parameters (temperature, top-p, max tokens), hit send. The response streams back.

## Differences from agent chat

- **No skills, no KB.** The model gets only what you type. Use this to isolate "is it the model, or is it the wrapping?"
- **Ephemeral sessions.** Playground sessions aren't stored under Sessions. Useful for quick iteration; not useful for audit.
- **Token usage counts.** What you do here counts toward the chosen model's usage.

## Where to go next

- **[Models](./models.md)** — to deploy or proxy a model.

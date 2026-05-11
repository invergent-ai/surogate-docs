---
title: Playground
sidebar_position: 10
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Playground

## What it does

`/studio/playground` is an ad-hoc testing surface for a single Model. Talk to the model directly, tweak sampling parameters, paste in prompts. No agent wrapper — just the bare model behind your Surogate proxy.

## When to use it

- Sanity-check that a freshly deployed Model responds at all.
- Tune a system prompt or a few-shot block before wiring it into an Agent.
- Compare two model versions head-to-head on the same prompt (open two browser tabs).

## Prerequisites and permissions

- **Read**: any project member.
- At least one deployed or proxied Model. With zero models the page shows **No models** — pick a model in [Models](./models) first.

## Where to find it

`/studio/playground` — empty unless you deep-link `?modelId=<id>` or pick one from the Model picker on the page.

## Step-by-step — Use the playground

1. Deploy or proxy a Model first ([Models](./models)).
2. Open **/studio/playground**.
3. Pick a model from the **Model** dropdown _TODO(verify) — or arrive via `?modelId=…`._
4. Type into the input. Adjust sampling parameters (temperature, top-p, max tokens). _TODO(verify exact controls._
5. Hit **Send**. The response streams back.

## Edge cases and gotchas

- Sessions in the Playground are **not** stored in `/studio/sessions` — they're ephemeral. _TODO(verify._
- The Playground uses the Model's API key automatically — you don't paste an `sk-agent-...` here.
- Token usage in the Playground is counted toward the Model's totals (visible in [Monitoring](./monitoring) → Token Usage).

## Related

- [Models](./models)
- [Monitoring](./monitoring)

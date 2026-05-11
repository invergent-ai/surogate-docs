---
title: Deploy a model
sidebar_position: 3
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Workflow — Deploy a model

<video controls width="720" muted>
  <source src="/videos/05-deploy-model-dialog.webm" type="video/webm" />
</video>

## Goal

Bring an LLM into your project so agents can call it.

## Prerequisites

- For a **Surogate-served** model: at least one connected [Cloud Backend](../features/compute) with GPU capacity.
- For a **proxied** model: a [Credential](../concepts/core-objects#credential) for the upstream provider (e.g. OpenAI, Anthropic) saved under [Admin → Integrations](../admin/integrations).
- Project role: `editor` or `owner`, or system `devops` for cloud-served models. _TODO(verify._

## Steps

1. Switch to **Develop** and open **/studio/models**.
2. Click **Deploy Model** (top-right).
3. Pick a **source**: Hub repo / external HuggingFace ID / OpenAI-compatible URL / etc. _TODO(verify._
4. For served models: pick a **Backend**, a **GPU offer**, and (optional) **Replicas** + **Quantization**.
5. Submit. The model appears under **Deploying** and moves to **Serving** when healthy.

## Verify

1. Open **/studio/playground?modelId=&lt;id&gt;** and send a test prompt.
2. Or call the proxy from outside with the model's `sk-agent-...` API key.

## Gotchas

- Quantization choices have to match the chosen GPU and the Surogate Trainer's matrix — see the trainer's [precision and recipes](/guides/precision-and-recipes) guide.
- Stopping a model with active agents causes those agents to error until the model is back. Coordinate stops in the [Monitoring](../features/monitoring) view.
- API keys (`sk-agent-...`) are **per-Model**, not per-Project. If you need scoping, create different models.

## Related

- [Models](../features/models)
- [Compute](../features/compute)
- [Playground](../features/playground)

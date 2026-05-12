---
title: Models
sidebar_position: 4
slug: /features/models
---

# Models

A Model is the LLM your agents call. Surogate Ops either serves it for you on your connected cloud compute, or proxies it to an upstream provider. Either way your agents reference the model by id, and external callers can reach it through Surogate's API.

## Where models come from

Models page → **Deploy Model**. Pick one of four sources:

- **Local Hub** — pull weights from a Hub repo. This is what you use to serve a model your team has trained. Default option.
- **🤗 Hugging Face** — paste an HF model id (e.g. `meta-llama/Llama-3.1-8B`). Requires a HF token in Integrations for gated repos.
- **OpenRouter** — proxied through OpenRouter's catalog. Requires an OpenRouter credential.
- **URL** — any OpenAI-compatible endpoint. Paste a base URL and a credential id. Works with self-hosted vLLM, Ollama, internal inference services.

The form adapts to the source. For served models, you pick a backend, a GPU offer, replicas, and (optionally) quantization. For proxied models, you point at the endpoint and the credential.

Submit. Served models land in **Deploying** while the container comes up; proxied models go straight to **Serving**.

## Status

| Status | Meaning |
|---|---|
| **Deploying** | Container being built and scheduled. Normal during first deploy. |
| **Serving** | Healthy, accepting traffic from agents and the Playground. |
| **Stopped** | You manually stopped it. Re-deploy to serve again. |
| **Error** | Container or upstream provider returning failures. |

A Model that flips from Serving to Error invalidates every agent calling it. Agents show errors in Monitoring until the model is back.

## API keys

Each model can have one or more API keys for external callers. A key is scoped to that one model — your own services, third-party tools, anything outside Surogate Ops uses it to hit the model through Surogate's API. Agents built on the model don't need a key; they call internally.

Failed authentications are negative-cached briefly to protect the upstream. A wrong key keeps failing for up to about a minute after the fix. The rotation rule: create the new key first, point clients at it, **then** revoke the old. Never delete first.

## Quantization

Served models accept several quantization options: `bf16`, `fp8`, `nvfp4`, `qfp4`, `qfp8`, `qlora`. The matrix of legal pairs depends on the GPU. Pick `bf16` if you're unsure; pick `qlora` if you're optimizing for GPU hours. The Surogate Trainer's [Precision and recipes](/guides/precision-and-recipes) guide has the full matrix.

## Cost shape

Served models reserve compute for the lifetime of the container. Stopping releases the reservation immediately. Proxied models cost nothing on Surogate's side; you pay the upstream provider directly.

The Studio dashboard's Serving Models and Training Jobs panels show coarse spend. For per-model details, use your cloud backend's own billing.

## When something fails

- **Stuck in Deploying.** Find the related `serving` workload at [Compute → Workload Queue](./compute.md) filtered to `serving`. Open the row for logs.
- **API call returns "API key not scoped for this model".** The key was created for a different model. Create a new key on this model.
- **Quantization choice rejected.** GPU type doesn't support that quantization. Pick a different GPU or a different quantization.

## Where to go next

- **[Agents](./agents.md)** — what your model powers.
- **[Compute](./compute.md)** — where served models actually run.
- **[Playground](./playground.md)** — to sanity-check a model without an agent wrapping it.
- **[Training Runs](./training.md)** — to produce the weights you serve here.

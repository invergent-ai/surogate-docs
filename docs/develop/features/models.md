---
title: Models
sidebar_position: 1
---

# Models

The Models page is where you register and serve models. Four sources, five detail tabs per model.

## Four sources

Click **DEPLOY MODEL** at the top of the Models page. Pick a source:

| Source | What it is | When to use |
|---|---|---|
| **Local Hub** | A model already in your tenant's lakeFS hub | After a training run completes, the trained model lands here |
| **Hugging Face** | Pull a model from HF Hub by repo + revision | Public models, GGUF quantized variants |
| **OpenRouter** | Use OpenRouter as the backing endpoint | Mix-and-match commercial models without paying multiple subscriptions |
| **URL** | Any OpenAI-compatible endpoint | Your own vLLM server, Anthropic, OpenAI direct, etc. |

For Hugging Face you can search by name and pick a specific quantization. For URL you provide:

- The endpoint URL (e.g. `https://expert-pool.your-cluster.svc:8000/v1`)
- The model name (passed verbatim in API calls)
- Optional API key (stored in the Vault if provided)

## The model detail page

Five tabs:

### OVERVIEW

KPIs: total tokens served, average latency, request count, error rate. Model metadata: source, revision, license, context window, tokens-per-second throughput.

### PERFORMANCE

Latency histogram (p50/p95/p99), token throughput over time, error rate over time. Compare to other models you've served.

### CONFIG

The model's serving configuration:

- **Compute** — which provider, instance type, replica count
- **GPU** — single GPU, multi-GPU, GPU memory
- **Engine** — vLLM, TGI, custom
- **Quantization** — fp16, int8, int4 (matters for HF-sourced models)
- **Max concurrent requests** — soft cap

This tab is **required** to be filled in before the model can be started.

### CONVERSATIONS

Sessions that used this model. Filter by agent, time range, quality flag. Useful for understanding model performance in production traffic.

### FINE-TUNES

Fine-tunes derived from this model. Each fine-tune shows its training run, expert it's serving (if any), success rate, and a "+ NEW FINE-TUNE" button to start another training run from this base.

## Starting a model

The START button is disabled until you've filled in CONFIG. Once CONFIG is set:

1. Click START.
2. The platform provisions GPU resources on the selected provider.
3. Model is downloaded, loaded, and exposed at an endpoint.
4. STATUS moves `creating` → `serving` over 1-10 minutes (HF download + load can be slow).

The endpoint becomes available to your agents (via the agent's Model selection) and to your expert skills.

## Stopping a model

STOP button drops the model's pods to 0. The endpoint stops responding. The model is retained — START again brings it back without re-downloading (model files cache locally).

## Serving multiple replicas

For high-traffic models, scale up:

CONFIG → Compute → Min/Max replicas. The platform auto-scales based on request rate. Each replica is a full GPU pod.

## Connecting a model to an agent

Open the agent → CONFIG → Model section. Pick the model from the dropdown.

- New sessions use the new model
- In-progress sessions keep their old model (session-start freeze)

## Models for experts

Experts (see [Skills & Experts](./skills-and-experts.md)) reference a model + endpoint in their SKILL.md:

```yaml
type: expert
model: qwen2.5-coder-7b
endpoint: http://expert-pool.your-cluster.svc:8000/v1
```

The `model` field is the name passed to the OpenAI-compatible API call; `endpoint` is the URL. Both can be set from the Models page or in the SKILL.md directly.

## BYO LLM

If you're using your own provider end-to-end (not Surogate-bundled models), enable **BYO LLM** in Settings → Billing. Your agents route LLM calls through your own provider; you pay them directly. Surogate charges only for platform usage. See [BYO LLM](./byo-llm.md).

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/models` | List models |
| `GET` | `/v1/models/{id}` | Model detail |
| `POST` | `/v1/models` | Register a model (any source) |
| `POST` | `/v1/models/{id}/start` | Provision and serve |
| `POST` | `/v1/models/{id}/stop` | Drop replicas |
| `POST` | `/v1/models/{id}/scale` | Update min/max replicas |
| `DELETE` | `/v1/models/{id}` | Unregister |
| `GET` | `/v1/models/artifacts?project_id=&hub_repo=&limit=200` | List artifacts in a lakeFS repo |

## What's next

[Skills & Experts](./skills-and-experts.md) for how to wire a fine-tuned model into an agent. [Training](./training.md) for producing one.

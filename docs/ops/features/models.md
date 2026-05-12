---
title: Models
sidebar_position: 5
slug: /features/models
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Models

`/studio/models` lists the LLMs available to your project. Each Model is either **served by Surogate** on cloud compute you have connected, or **proxied** to an upstream provider behind an OpenAI-compatible URL. Agents reference Models by id; the proxy uses `sk-agent-*` API keys scoped to a single Model.

## The list

The page header has the **Models** title and a **Filter models…** search input. Status pills filter by lifecycle: `All · Serving · Error · Stopped`. The primary action is **Deploy Model** (top-right).

Deep links:

- `/studio/models?modelId=<id>` selects a Model on load.
- `/studio/playground?modelId=<id>` opens the Playground bound to that Model.

## Deploy flow

The dialog header reads **Add Model**. The first screen is a source picker — four cards, exactly these labels:

| Source | What it expects |
|---|---|
| **Local Hub** | "From your registry". Pulls weights from a Hub repo in this project's namespace. The default option, and what serving from your own training output uses. |
| **🤗 Hugging Face** | "From HF Hub". Paste an HF model id (e.g. `meta-llama/Llama-3.1-8B`). Requires a HF token configured in [Integrations](../admin/integrations.md) for gated models. |
| **OpenRouter** | "From OpenRouter". Proxied through OpenRouter's catalog. Requires an OpenRouter credential. |
| **URL** | "From OpenAI-compatible provider". Paste a base URL and a credential id. Lets you route to any provider that speaks the OpenAI chat-completions schema (vLLM, Ollama, internal services). |

The empty state shows _"No models in Data Hub yet"_ when **Local Hub** is selected and the project's hub has zero model repos.

Picking a source unlocks the source-specific form (model id, name, deployment target, credential, replicas, quantization). The remaining buttons are **Cancel** (bottom-left) and **Add Model** (primary).

After submit, the Model lands in **Deploying** for served Models, and immediately in **Serving** for proxied ones (the proxy doesn't run a container).

## Lifecycle

| Status | Meaning |
|---|---|
| Deploying | Container being built and scheduled. |
| Serving | Healthy. Accepting traffic from agents and the Playground. |
| Stopped | You stopped it. Re-deploy to serve again. |
| Error | Container or upstream provider returning failures. |

A Model that flips from Serving → Error invalidates calls from every Agent that uses it — those Agents show errors in Monitoring until either the Model recovers or the Agents are re-pointed.

## API keys

Each Model has its own set of `sk-agent-*` keys. Keys are created from the Model detail page (TODO(verify the UI location)). The key authorizes calls to that model id only; an Agent built on the Model inherits its key implicitly.

Failed authentications (`401`/`403`) at the proxy are **negative-cached**. A wrong or revoked key keeps failing for up to a minute after the fix. Rotating a key: create the new key, point clients at it, then revoke the old one — never delete first.

## Stopping a Model

Stopping a served Model releases its compute reservation. Stopping a proxied Model just blocks calls to it through the Surogate proxy; the upstream provider is unaffected.

Coordinate stops in the [Monitoring](./monitoring) view — Agents pointing at the Model show errors until the Model is back. If your team uses the same Model across multiple Agents, flag the stop in Notifications first.

## Permissions

| Action | Role |
|---|---|
| List, open a Model | Project `viewer` and above |
| Deploy / Stop / Delete a served Model | System `devops` (or project `owner`, TODO(verify)) |
| Deploy a proxied Model | Project `editor` or above (TODO(verify)) |
| Manage API keys on a Model | Project `editor` or above (TODO(verify)) |

## Troubleshooting

- **Deploy stuck at Deploying.** Find the related `serving` workload at `/studio/compute/workload-queue?filter=serving`. Click the row to see logs.
- **`sk-agent-*` returns 403 "API key not scoped for this model".** The key was created for a different Model. Mint a new key on the right Model.
- **Quantization choice rejected.** GPU type doesn't support the chosen quantization. Pick a different GPU or a different quantization (see [Surogate Trainer → Precision and recipes](/guides/precision-and-recipes)).

## Related

- [Workflow — Deploy a model](../workflows/deploy-a-model)
- [Compute](./compute)
- [Playground](./playground)
- [Data Hub](./hub) — where the Model's weights live.

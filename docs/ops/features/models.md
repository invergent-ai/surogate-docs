---
title: Models
sidebar_position: 5
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Models

`/studio/models` lists the LLMs available to your project. Each Model is either **served by Surogate** on cloud compute you have connected, or **proxied** to an upstream provider (OpenAI, Anthropic, Together, etc.). Agents reference Models by id; the proxy uses `sk-agent-*` API keys scoped to a single Model.

## The list

The page header has the **Models** title and a **Filter models…** search input. Status pills filter by lifecycle: `All · Serving · Error · Stopped`. The primary action is **Deploy Model** (top-right).

Deep links:

- `/studio/models?modelId=<id>` selects a Model on load.
- `/studio/playground?modelId=<id>` opens the Playground bound to that Model.

## Deploy flow

The Deploy Model dialog walks these sections. The exact order depends on the source you pick.

| Section | Required | Notes |
|---|---|---|
| Source | Yes | Hub repo, external HuggingFace ID, OpenAI-compatible URL, Anthropic, etc. TODO(verify the full enum). |
| Name | Yes | Display label across `/studio/models`, agent settings, and Playground. |
| Backend | Conditional | Required for served Models, not for proxied ones. One of the connected backends from [Compute](./compute). |
| GPU | Conditional | Choose from the offers under `/studio/backend-offers?backend=<name>`. |
| Replicas | No | Integer count. Default 1. TODO(verify). |
| Quantization | Conditional | bf16, fp8, nvfp4, qfp4, qfp8, qlora. The matrix of legal pairs depends on GPU. See [Surogate Trainer → Precision and recipes](/guides/precision-and-recipes). |
| Credential | Conditional | Required when the source is a proxied provider. Pulled from [Settings → Integrations](../admin/integrations). |

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

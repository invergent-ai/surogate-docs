---
title: Training
sidebar_position: 12
slug: /features/training
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Training

`/studio/training` lists training runs (also called **experiments**) and is where you start a new one. Surogate Ops orchestrates the run on your connected compute via the [Surogate Trainer](/old-docs), the LLM training library at the platform's core. When a run completes, its resulting weights can be promoted to [Models](./models.md) or pushed to the [Hub](./hub.md).

## When to use it

- Fine-tuning an open-weights LLM (SFT, LoRA, QLoRA).
- Running RL training (GRPO) against a reward model or environment.
- Pretraining from scratch.

## Prerequisites

- A [Dataset](./datasets.md) (for SFT) or an environment-kind [Hub Repo](./hub.md) (for RL).
- A connected [Cloud Backend](./compute.md) with GPU capacity matching what you'll request.
- Project role `editor` or `owner`, or system `developer` / `devops`.

## Page layout

`/studio/training` — list + **Filter experiments…** input + **New Run** action (top-right).

Deep-link a specific run: `/studio/training?runId=<run-id>`.

## Start a training run

1. Open **/studio/training**.
2. Click **New Run**. The dialog header reads **New Training Run**.
3. The top row of the dialog is the **kind picker**, exactly two cards:

   | Kind | Description as shown in the UI |
   |---|---|
   | **SFT** | _Supervised Fine-tuning._ Pair (prompt, completion) examples become weight updates. |
   | **GRPO** | _Group Relative Policy Optimization._ RL training against a reward model or environment. |

4. Below the kind picker, three text fields:

   | Field | Type | Notes |
   |---|---|---|
   | **Name** | text | Placeholder: `CX SFT Round 5`. Becomes the run's display label and `runId` prefix. |
   | **Short description** | text | Placeholder: `CX Quality Improvement`. One-liner shown in the list. |
   | **Long description** | textarea | Placeholder: `Fine-tuning on curated CX dialogs will improve…`. Free-form notes — hypothesis, dataset, success criteria. |

5. Below that, the per-kind config: base Model picker, Dataset (SFT) or Environment (GRPO) picker, precision (bf16 / fp8 / nvfp4 / qlora), batch size, learning rate, sequence length. Trainer defaults are usually fine; see [Surogate Trainer → Precision and recipes](/guides/precision-and-recipes) for the long version.
6. Pick a GPU offer from a connected backend.
7. Submit with **Create**. The run appears under [Compute → Workload Queue](./compute.md) with kind `sft` or `grpo`. Cancel and Close abandon the dialog.

## Lifecycle

A run progresses through the standard Workload states: `Queued → Provisioning → Running → Completed / Failed / Cancelled`. The run-detail panel (right side of `/studio/training`) shows:

- **Logs** — the trainer's stdout/stderr.
- **Metrics** — loss curves, learning rate, throughput.
- **Artifacts** — the produced weights, ready to promote to a Model.

## Cancelling

From `/studio/compute/workload-queue?filter=sft` (or `grpo`), open the run's row menu and pick Cancel. The compute reservation releases immediately; partial weights are kept.

## Gotchas

- Promoting a finished run's weights to a deployed Model is a **separate explicit action** from the run detail page. Completion is not deployment.
- A failed run keeps its logs — click the row to read them.
- Multi-node runs (`multi-node` precision recipes) reserve every node before starting. If any node fails to provision, the whole run waits.
- Stacked LoRA training (LoRA on top of a LoRA adapter) is supported — see [Surogate Trainer → QLoRA](/guides/qlora) for the precise recipe.

## Related

- [Compute](./compute)
- [Datasets](./datasets)
- [Models](./models)
- [Surogate Trainer documentation](/old-docs)

---
title: Training Runs
sidebar_position: 2
slug: /features/training
---

# Training Runs

A Training Run is a model fine-tune scheduled on your compute. Surogate orchestrates the run via the [Surogate Trainer](/old-docs) — the LLM training library at the platform's core. When the run completes, the weights land in your Hub and you can promote them to a deployable Model.

## When to run training

- You've captured a few hundred clean sessions and want a model that does that specific job better than a generalist.
- Your inference bill on a frontier model is high enough that a smaller fine-tuned model would pay for itself.
- You need a specific capability (math reasoning, code review, an internal style) that a generalist doesn't reliably deliver.

## Start a run

Train → Training Runs → **New Run**. Pick the kind first:

- **SFT** — supervised fine-tuning. Pair `(prompt, completion)` examples; the model learns to produce the completion. Use when you have a labeled dataset.
- **GRPO** — group relative policy optimization. RL training against a reward model or environment. Use when you have a clear reward signal but no labeled outputs.

Fill in three text fields:

- **Name** — display label and `runId` prefix.
- **Short description** — one-liner shown in the runs list.
- **Long description** — the hypothesis, the dataset, what success looks like. Free-form notes for your future self.

Below those, the per-kind config: base model, dataset (SFT) or environment (GRPO), precision (`bf16`, `fp8`, `nvfp4`, `qlora`), batch size, learning rate, sequence length. Defaults are sensible; the [Trainer's precision and recipes](/guides/precision-and-recipes) guide explains when to deviate.

Pick a GPU offer from a connected backend. Submit.

## What happens next

The run lands in [Compute → Workload Queue](./compute.md) under kind `sft` or `grpo`. The detail panel shows:

- **Logs** — the trainer's stdout/stderr in real time.
- **Metrics** — loss curves, learning rate, throughput.
- **Artifacts** — the weights, ready to promote.

## Promote the result

When the run completes, open its detail and promote the weights to a Model. Then open your Agent → Settings → swap the Model. Redeploy. Your agent now runs on the model you just trained.

## Cancelling

From [Compute → Workload Queue](./compute.md) filtered to `sft` or `grpo`, open the row menu → Cancel. Partial weights are kept; the compute reservation releases.

## When something fails

- **Stuck in Provisioning.** No GPU available in the chosen backend / region. Loosen the GPU requirement or connect a different backend.
- **Loss diverges.** Most often a too-large learning rate. Lower it and re-run from a checkpoint if the trainer supports it.
- **Multi-node run hangs.** One node failed to provision; the run waits for the full group. Cancel and resubmit.

## Stacked LoRA, MoE, multi-node

The Surogate Trainer handles stacked LoRA training (LoRA on top of a LoRA adapter), MoE imbalance detection, and multi-node DDP via Ray. The Ops UI surfaces these as advanced fields on the run config; the [Trainer docs](/old-docs) cover the math.

## Where to go next

- **[Datasets](./datasets.md)** — where SFT inputs come from.
- **[Models](./models.md)** — where the trained weights end up.
- **[Evaluations](./evaluations.md)** and **[Arenas](./arenas.md)** — to verify before you cut over.
- **[Use cases → Training your own expert](../use-cases/training-your-own-expert.md)** — the full loop.

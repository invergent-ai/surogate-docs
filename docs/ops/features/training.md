---
title: Training
sidebar_position: 12
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Training

## What it does

`/studio/training` lists training runs (also called **experiments**) and is where you start a new one. Surogate Ops orchestrates the run on your connected compute via the [Surogate Trainer](/) (the LLM training library at the heart of the platform). When a run completes, the resulting model can be promoted to [Models](./models) or pushed to the [Hub](./hub).

## When to use it

- Fine-tuning an open-weights LLM (SFT, LoRA, QLoRA).
- Running RL training (GRPO, PPO) against a reward model or environment.
- Pretraining from scratch (rare, but supported).

## Prerequisites and permissions

- **Read**: any project member.
- **New Run**: project `editor` or higher, **or** the system role `developer` / `devops`. _TODO(verify._
- A [Dataset](./datasets) (for SFT) or an [Environment](./hub) (for RL).
- A [Cloud Backend](./compute) with GPU capacity.

## Where to find it

`/studio/training` — list + **New Run** + **New** + filter.

Deep-link a specific run: `/studio/training?runId=<run-id>`.

## Step-by-step — Start a training run

1. Open **/studio/training**.
2. Click **New Run** (top-right). _TODO(verify) — the page also exposes a smaller "New" button; confirm which opens the full form._
3. Pick a **kind** (`sft`, `grpo`, `pretraining`, …).
4. Pick the **base model** and the **dataset** / **environment**.
5. Configure precision (bf16 / fp8 / nvfp4 / qlora / etc.), batch size, learning rate, sequence length. The Trainer guides defaults; see the [Surogate Trainer docs](/) for the long version.
6. Pick a **GPU offer** from a connected backend.
7. Submit. The run appears under [Compute → Workload Queue](./compute) with kind `sft` / `grpo` / etc.

## Tabs

The Training page is filterable but does not split runs across tabs in the same way as Agents/Models. Use the **Filter experiments…** input to search by name.

## Edge cases and gotchas

- Runs hold their compute reservation until they finish or fail. **Cancel** from Compute → Workload Queue to release.
- A failed run keeps **logs**; click the run to read them.
- Promoting a run's resulting weights to [Models](./models) is a separate explicit step — completion is not deployment. _TODO(verify the promotion path._

## Related

- [Compute](./compute)
- [Datasets](./datasets)
- [Models](./models)
- [Surogate Trainer documentation](/) (the underlying library).

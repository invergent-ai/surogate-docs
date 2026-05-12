---
title: Datasets
sidebar_position: 1
slug: /features/datasets
---

# Datasets

A Dataset is a collection of training, evaluation, or fine-tuning examples. Datasets feed Training Runs and Evaluations and live in the Hub once you push them.

## Where datasets come from

Train → Datasets → **New Dataset**. Pick one of four sources:

- **From Conversations** — export sessions captured from your existing agents as supervised fine-tuning examples. This is the loop that closes the rest of Surogate: real traffic becomes training data.
- **Expert Training** — generate curated examples for a specific capability. Used as the seed for an expert-model run.
- **Upload File** — JSONL, CSV, or Parquet from local. Format inferred from extension; map columns on the next screen.
- **Synthetic Generation** — schedule a workload of kind `synthetic` that produces examples by sampling from a prompt template. Generated rows merge into the dataset when the job completes.

You can also **Import** an existing dataset from a Hub repo.

## Dataset kinds

A dataset carries a `kind` that constrains its schema:

| Kind | Used by | Shape |
|---|---|---|
| `sft` | Supervised fine-tuning runs | `{prompt, completion}` pairs, optionally with a system message |
| `eval` | Evaluations | Test cases with expected outputs or judge rubrics |
| `synthetic` | Output of synthetic generators; can feed SFT | Generator-dependent |
| `environment` | RL training | Bound to a Hub Environment repo; inherits the env's observation/action schema |

The schema is validated at write time. A dataset bound to an `environment` rejects rows that don't match the env's action space — no surprises at training time.

## Workflow

The end-to-end pattern most teams use:

1. Run an agent for a couple of weeks.
2. Flag the sessions you want the next model to imitate (and ignore the rest).
3. Train → Datasets → **New Dataset** → **From Conversations** → pick the agent, set the date range, set a quality filter.
4. The dataset is ready to feed a [Training Run](./training.md).

## When something fails

- **Large upload stalls.** The upload happens in the browser. Closing the dialog cancels it. Re-open and re-pick the file to retry.
- **Schema rejects rows.** The dataset's kind doesn't match the row format. Either re-pick the kind or reshape the rows.
- **Synthetic job stays Queued.** No compute available. Loosen the synthetic recipe's GPU requirement or connect a backend with stock.

## Where to go next

- **[Training Runs](./training.md)** — where datasets get consumed.
- **[Data Hub](./hub.md)** — to publish a dataset for reuse.
- **[Use cases → Training your own expert](../use-cases/training-your-own-expert.md)** — the end-to-end loop from captured sessions to a fine-tuned model.

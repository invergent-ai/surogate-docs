---
title: Datasets
sidebar_position: 11
slug: /features/datasets
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Datasets

A **Dataset** is a collection of training, eval, or fine-tuning examples scoped to one Project. Datasets feed Training Runs and Evaluations, and they live in the Hub once you push them. The list at `/studio/datasets` has a **Filter datasets…** input, an **Import** action, and a **New Dataset** action.

## New Dataset flow

The dialog header reads **New Dataset**. The dialog opens on a source picker — four cards, exact labels and helper text below:

| Source | Description shown in the UI |
|---|---|
| **From Conversations** | _Export from agent conversations._ Builds a dataset from sessions already captured in `/studio/sessions`. Pick the agent(s) and a date window. |
| **Expert Training** | _Generate expert training data._ Curates the highest-quality interactions for a specific capability. Used as the seed for [Training](./training.md) of an expert model. |
| **Upload File** | _Create a new dataset by uploading a file (JSONL, CSV, Parquet)._ Format inferred from extension. Schema is read on import; you map columns on the next screen. |
| **Synthetic Generation** | _Generate/Augment datasets with synthetic data._ Schedules a workload of kind `synthetic` on Compute. Generated rows merge into the dataset when the job completes. |

Cancel / Close are on every screen.

## Import flow

**Import** pulls a Dataset repo from the Hub. The dialog (header **Import Repository**, kind `Dataset`) lets you point at a HuggingFace dataset id and (optionally) a branch and a sub-path. Imports preserve the upstream version — the dataset record carries a `repo@branch` reference that Training Runs honor.

## Dataset kinds

A Dataset has a **kind** that constrains its schema:

| Kind | Used by | Schema shape |
|---|---|---|
| `sft` | Supervised fine-tuning (SFT) runs | `{prompt, completion}` pairs, optionally with system message |
| `eval` | Evaluations | Test cases with expected outputs / judge rubrics |
| `synthetic` | Output of synthetic generators; can feed SFT | Generator-dependent |
| `environment` | RL training | Bound to a Hub Environment repo; inherits observation/action schema |

The page filter searches by name. Sorting by kind is not exposed in the UI as of this snapshot.

## Permissions

| Action | Role |
|---|---|
| List, browse | Project `viewer` and above |
| New / Import / Edit / Delete | Project `editor` or `owner` |

## Gotchas

- A Dataset bound to an **Environment** Hub repo enforces the env's schema on every row added — bad rows are rejected at write time, not at training time.
- Imports from the Hub respect repo branches (a Dataset can target `repo@branch`).
- Large local uploads happen in the browser. The upload progress lives in the dialog; closing the dialog cancels the upload. Re-open and re-pick the file to retry.
- A Dataset attached to a finished Training Run is read-only — to extend it, fork into a new dataset.

## Related

- [Training](./training)
- [Hub](./hub)
- [Evaluations](./evaluations)

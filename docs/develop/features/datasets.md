---
title: Datasets
sidebar_position: 1
---

# Datasets

A dataset is a versioned corpus you use for training and evaluation. Four source types.

## NEW DATASET — four source types

Click **NEW DATASET** → pick a source:

| Source | What it is | Output format |
|---|---|---|
| **From Conversations** | Filter sessions by agent, time range, quality flags. Each session becomes a sample. | SFT / preference / conversation |
| **Expert Training Data** | Pre-existing JSONL exports from `POST /v1/skills/{name}/collect`. | SFT |
| **Upload File** | Drop a CSV / JSONL / parquet file. | Format inferred from file |
| **Synthetic Generation** | Teacher/judge/worker pattern to synthesize labeled data. | Configurable |

### From Conversations

The most common source — building a dataset from observed traffic:

1. Filter sessions in the form:
   - Agent (or all)
   - Time range
   - Quality flags (👍 only; or 👎 only for evaluation negatives; or combinations)
   - Channel filter
   - Skill / expert filter
2. Pick a format:
   - **SFT** — supervised fine-tuning. Each row = full session transcript with system prompt.
   - **Preference** — preference learning. Pairs of (chosen, rejected) responses for the same prompt.
   - **Conversation** — raw conversation logs for analysis.
3. Click CREATE.

The dataset row lands in the Hub as a versioned repo.

### Expert Training Data

If you've already triggered expert training data exports via `POST /v1/skills/{name}/collect`, those JSONLs land in `tenant-{org_id}/shared/skills/{name}/training/`. Wrap them as a dataset to use them in training runs.

### Upload File

Drop a CSV, JSONL, or parquet file. The platform inspects the file and infers the format. For arbitrary CSVs, you may need to map columns to expected fields (input, output, optional system prompt).

### Synthetic Generation

The teacher/judge/worker pattern:

- **Teacher** — generates candidate outputs (typically a strong LLM)
- **Judge** — evaluates each candidate (typically another strong LLM)
- **Worker** — produces the final formatted output

Use when you need labeled data but don't have enough real traffic.

## Dataset detail page

Four tabs:

### OVERVIEW

- ROWS count
- AVG / MIN / MAX / P95 TOKENS
- Token distribution histogram
- Column char-length stats
- Duplicates count
- PII findings (the platform scans for PII patterns)

### SAMPLES

Preview rows. Filter by split (train/eval/test). Click any row to see the full sample.

🚧 Known issue: header counter sometimes shows N samples but SAMPLES tab shows 0 rows. Workaround: navigate away and back.

### PIPELINE

A DAG showing how this dataset was built — sources, filters, transformations. Useful for tracing where data came from.

### REPOSITORY

The underlying lakeFS repo. Files, commits, branches, tags. Same operations as any Hub repo.

## SFT vs Preference vs Conversation formats

### SFT format

```jsonl
{"messages": [
  {"role": "system", "content": "You are..."},
  {"role": "user", "content": "How do I..."},
  {"role": "assistant", "content": "Here's how...", "tool_calls": [...]},
  {"role": "tool", "tool_call_id": "tc_1", "content": "..."},
  {"role": "assistant", "content": "..."}
]}
```

For supervised fine-tuning. Each line is a complete conversation.

### Preference format

```jsonl
{
  "prompt": "Explain transformers",
  "chosen": "Detailed accurate explanation...",
  "rejected": "Incorrect explanation..."
}
```

For preference learning (DPO, RLHF). Requires both good and bad examples for the same prompt.

### Conversation format

Raw transcripts for analysis. Not used directly in training.

## Dataset for evaluation

When you want a dataset specifically for **evaluation** (not training), use:

- **From Conversations** filtered by 👎 — your worst cases become your eval set
- **From Conversations** filtered by 👍 — your best cases become regression cases
- **Upload File** with hand-crafted edge cases

Then in the Evaluation wizard, reference this dataset.

## DELETE confirmation

Standard pre-flight check — if the dataset is referenced by an active training run, you'll see a warning. Cancel the training run first or wait for it to finish.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/datasets` | List |
| `GET` | `/v1/datasets/{id}` | Detail |
| `POST` | `/v1/datasets` | Create (any source type) |
| `GET` | `/v1/datasets/{id}/samples?split=train&limit=50` | Preview samples |
| `DELETE` | `/v1/datasets/{id}` | Delete (with reference check) |

## What's next

[Training](./training.md) for using a dataset to fine-tune. [Evaluations](./evaluations.md) for using a dataset to test.

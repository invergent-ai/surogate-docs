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

## Building a dataset — the builder flows

Clicking **NEW DATASET** opens the source chooser at `/studio/datasets/create`. It's a grid of cards, each routing to a dedicated builder page:

| Card | Goes to | What it does |
|---|---|---|
| **From chats** | `/studio/datasets/from-chats` | Turn real agent chats into supervised training pairs. |
| **Expert training data** | — | *Coming soon* (shows a toast). |
| **Upload files** | `/studio/datasets/upload` | Bring your own JSONL / CSV / plain-text file. |
| **Generate synthetic** | `/studio/datasets/synthetic` | Teacher generates, judge filters. |
| **Import repository** | `/studio/datasets/import` | Pull a dataset from the Hugging Face Hub. |

The datasets list also has an **Import from chats** button that jumps straight to the from-chats builder.

### From chats (simple) — `/studio/datasets/from-chats`

The seeded, single-agent form. When you arrive from a Sessions selection, it's pre-filled with those chats; otherwise it draws from the project's recent chats and focuses on the agent with the most matching chats.

Fields:

- **Dataset name** (required, lowercase-hyphens — used as the repo name). Pre-filled as `<agent>-sft-v1`.
- **Source** — read-only: `<agent> · N chats`.
- **Filters** — two checkboxes: *Only good chats — thumbs-up, resolved, not flagged* (on by default) and *Drop messages shorter than 3 words*.
- **Format** — a toggle between **SFT pairs** (user prompt → assistant reply) and **Raw messages** (full multi-turn transcript).
- **Scrub PII before training** — a toggle (on by default) that removes emails, names, and card numbers from every sample.
- **Estimated output** — `N rows · ~<tokens> tokens`.

Click **Build dataset** to kick off the build.

### From chats (advanced) — `/studio/datasets/new`

The filter-rich builder, seeded from the dashboard's "Raw material" selection or a Sessions selection. It carries a seeded-chats banner and list you can trim.

Fields:

- **Dataset name** (lowercase-hyphens, used as the repo name).
- **Agents** — chips pre-filled from the seeded chats; add more agents to widen the dataset.
- **Time range** — Last 24 hours / 7 days / 30 days / All time.
- **Quality** — pills: 👎 Negative · 👍 Positive · Flagged · All. Picking a quality also sets a recommended format.
- **More filters** — Channel and Skill / expert selects (options come from the matching sessions).
- A live **N chats → ~N samples** count, plus the seeded-chats list (each removable).
- **Format** — Eval set · Preference · SFT · Conversation, with a "Recommended for 👍/👎 chats" badge. (👎 → eval set or preference pairs; 👍 → SFT.)

Click **Build dataset**. The dataset lands in your list as `building` → `ready`, versioned in Hub.

### Upload files — `/studio/datasets/upload`

Fields:

- **Dataset name** (required, lowercase-hyphens). Pre-filled from the file name.
- **Files** — a dropzone (or *browse files*) accepting **JSONL, CSV, or .txt**. Drop one file.

Once a file is added, the page inspects it and shows a detection summary: the format (CSV / JSONL / TXT), the inferred **schema**, and the **row count**. Detected schemas include `prompt / completion`, `chat / messages`, `instruction / output`, `preference pairs`, or the first few CSV columns.

**Build dataset** uploads the file in the background and hands off to the building page.

### Import repository (Hugging Face) — `/studio/datasets/import`

Fields:

- **Repository** (required) — a Hugging Face Hub search input; enter as `org/name` (e.g. `tatsu-lab/alpaca`).
- **Subset** (optional) — config / subset name, if the dataset has one.
- **Access token** (optional) — `hf_…`, needed only for private or gated repos.
- **Destination branch** — a branch combobox; created in Data Hub if it doesn't exist (defaults to `main`).
- **Destination folder** (optional) — leave empty to import at the repo root.

**Import dataset** runs an `import_dataset` job — track it in **Compute → Workload Queue** — and hands off to the building page. This flow is gated on the Free plan (shows an Upgrade prompt).

### Generate synthetic — `/studio/datasets/synthetic`

The teacher → judge flow, surfaced as three pipeline chips: **Teacher generates → Judge scores → Keep above threshold**.

Fields:

- **Dataset name** (required).
- **What should the data teach?** (required) — a brief used as the teacher model's generation prompt.
- **Teacher model** — the strong model that writes the samples.
- **Judge model** — scores each sample; low scores are dropped.
- **Samples to generate** (default `5000`).
- **Quality threshold** (default `0.8`, range 0–1).
- **Format** — SFT pairs / Raw completions.
- **Estimated run** — `~N samples · est. <minutes> min on 2× A100`.

Clicking **Build dataset** creates an empty synthetic dataset shell, seeds the Pipeline tab's settings (row count, teacher model), and lands you on the dataset's **PIPELINE** tab — where you author and run the generation pipeline. Running that pipeline is what flips the status to `ready`.

### Build progress — `/studio/datasets/building`

The from-chats, upload, and import flows hand off to a progress page. It shows a percentage bar, a per-kind step checklist, and an estimated time remaining. Each build kind has its own steps, for example:

- **Upload**: Parse the uploaded file → Validate the schema → Pack rows → Validate & publish to repo.
- **Import**: Resolve the repository → Download files → Convert & pack rows → Validate & publish to repo.
- **From chats**: Extract messages from chats → Scrub PII → Tokenize & pack pairs → Validate & publish to repo.
- **Synthetic**: Spin up teacher & judge → Generate samples → Judge & filter by quality → Validate & publish to repo.

You can **Run in background** (return to the list) or **Cancel build** at any time. Builds that carry a real dataset id poll the backend for actual status and surface a "Build failed" state if it errors; otherwise the page lands you on the finished dataset.

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

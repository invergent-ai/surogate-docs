---
title: Datasets
sidebar_position: 1
---

# Datasets

A dataset is a versioned corpus you use for training and evaluation. Every dataset is backed by a repository in the [Data Hub](./hub.md) — the training files (`train/dataset.parquet`, plus a `dataset_dict.json` split manifest) live there, while the dataset's metadata (name, format, status, stats, pipeline) lives in the platform database. Creating, building, and deleting datasets all go through `/api/datasets`.

## Five ways to bring a dataset

Click **NEW DATASET** (or, on an empty list, **+ New dataset**) to open the source chooser at `/studio/datasets/create`. It's a grid of cards, each routing to a dedicated builder page:

| Card | Builder page | What it does | Backend |
|---|---|---|---|
| **From chats** | `/studio/datasets/from-chats` | Turn real agent conversations into supervised training pairs. | `POST /api/datasets/from-conversations` |
| **Expert training data** | *(coming soon)* | Wrap collected training data (JSONL run traces) as a dataset. | `POST /api/datasets/expert-training` |
| **Upload files** | `/studio/datasets/upload` | Bring your own JSONL / CSV / .txt file. | `POST /api/datasets/upload` |
| **Generate synthetic** | `/studio/datasets/synthetic` | Teacher model generates, judge model filters. | `POST /api/datasets/synthetic` → Pipeline tab |
| **Import repository** | `/studio/datasets/import` | Pull a dataset repo from the Hugging Face Hub. | `import_dataset` compute job |

The datasets list also has an **Import from chats** button that jumps straight to the from-chats builder.

Every finished dataset lands in your list as `building` → `ready`, versioned in the Data Hub.

---

## 1. From Conversations

The most common source: build a dataset from observed agent traffic. Two builder pages share this source — a simple seeded form and a filter-rich advanced form — and both call the same endpoint.

### From chats (simple) — `/studio/datasets/from-chats`

The single-agent form reached from the list's **Import from chats**. When you arrive from a Sessions selection it's pre-filled with those chats; otherwise it draws from the project's recent chats and focuses on the agent with the most matching chats.

Fields:

- **Dataset name** (required, lowercase-hyphens — used as the repo name). Pre-filled as `<agent>-sft-v1`.
- **Source** — read-only: `<agent> · N chats`. Change the selection back in Sessions.
- **Filters** — two checkboxes: *Only good chats — thumbs-up, resolved, not flagged* (on by default) and *Drop messages shorter than 3 words*. A "good" chat is one with no crash, policy denial, expert override, or thumbs-down.
- **Format** — a toggle between **SFT pairs** (user prompt → assistant reply) and **Raw messages** (full multi-turn transcript).
- **Scrub PII before training** — a toggle (on by default) that removes emails, names, and card numbers from every sample.
- **Estimated output** — `N rows · ~<tokens> tokens` (tokens estimated at ~290 per row).

Click **Build dataset** to kick off the build.

### From chats (advanced) — `/studio/datasets/new`

The filter-rich builder, seeded from the dashboard's "Raw material" selection or a Sessions selection. It carries a seeded-chats banner and a list you can trim.

Fields:

- **Dataset name** (lowercase-hyphens, used as the repo name).
- **Agents** — chips pre-filled from the seeded chats; add more agents to widen the dataset.
- **Time range** — Last 24 hours / 7 days / 30 days / All time.
- **Quality** — pills: **👎 Negative** · **👍 Positive** · **Flagged** · **All**. These map to real session quality flags: Negative = a thumbs-down response; Positive = a thumbs-up response; Flagged = any policy denial, expert override, crash, or thumbs-down. Picking a quality also sets a recommended format.
- **More filters** — **Channel** and **Skill** selects, with options drawn from the matching sessions.
- A live **N chats → ~N samples** count (Preference halves the count into pairs), plus the seeded-chats list (each row removable).
- **Format** — **Eval set** · **Preference** · **SFT** · **Conversation**, with a "Recommended for 👍/👎 chats" badge (👍 → SFT; 👎 or flagged → eval set).

Click **Build dataset**.

### What actually happens

Both forms POST to `/api/datasets/from-conversations` with `project_id`, `agent_id`, `num_sessions` (clamped 1–500), and a `display_name`. The server walks the agent's most-recent sessions, converts each `user.message` + `llm.response` turn into an OpenAI-style `messages` list (tool-call and tool-result turns are dropped — the sample schema is `role` + `content` today), writes them as a single parquet file in a fresh Hub repo, and persists the dataset as `format=sft`. This is synchronous: at typical session counts it finishes within the request. The Quality / Channel / Skill / Time-range filters and the Format and PII toggles shape the on-screen estimate and choose the primary agent and session count; the export itself always produces SFT `messages` for now.

## 2. Expert / collected training data

The chooser's **Expert training data** card currently shows a *"coming soon"* toast — the dedicated builder page isn't wired into Studio yet. The underlying capability exists at the API layer: `POST /api/datasets/expert-training` provisions a dataset (`format=sft`, `status=building`) tied to a skill plus teacher and judge models, and spawns a generation run. When the run completes, its collected JSONL/parquet training data lands in the dataset's Hub repo, and the dataset detail page grows a **Synthetic Runs** tab for tracking those runs. Use this to wrap training data collected from a skill's own runs as a reusable dataset once the flow ships.

## 3. Upload file — `/studio/datasets/upload`

Bring your own file. Fields:

- **Dataset name** (required, lowercase-hyphens). Pre-filled from the file name.
- **Files** — a dropzone (or *browse files*) accepting **JSONL, CSV, or .txt**. Drop a single file.

Once a file is added, the page inspects it locally and shows a detection summary — the **format** (CSV / JSONL / TXT), the inferred **schema**, and the **row count**. Detected schemas include `prompt / completion`, `chat / messages`, `instruction / output`, `preference pairs`, or the first few CSV columns / object keys.

**Build dataset** uploads the file (multipart `POST /api/datasets/upload` with `project_id`, `display_name`, and the file as `content`) and hands off to the building page. The server creates the dataset (`kind=user`, `source=manual`, `format=sft`), drops the file under `train/<filename>`, seeds a `dataset_dict.json` registering the `train` split, auto-detects the text column so stats can be computed, commits, and flips the dataset to `ready`. Parquet files are accepted at the repo layer too, even though the dropzone advertises JSONL / CSV / .txt.

## 4. Synthetic generation — `/studio/datasets/synthetic`

The teacher → judge flow, surfaced as three pipeline chips: **Teacher generates → Judge scores → Keep above threshold**.

Fields:

- **Dataset name** (required).
- **What should the data teach?** (required) — a brief the teacher model uses as its generation prompt (stored as the dataset description).
- **Teacher model** — the strong model that writes the samples (from the project's deployed models).
- **Judge model** — scores each sample; low scores are dropped.
- **Samples to generate** (default `5000`).
- **Quality threshold** (default `0.8`, range 0–1, step 0.05).
- **Format** — SFT pairs / Raw completions.
- **Estimated run** — `~N samples · est. <minutes> min on 2× A100`.

Clicking **Build dataset** calls `POST /api/datasets/synthetic`, which provisions an empty synthetic dataset shell (`kind=synthetic`, `status=building`) and an empty Hub repo. The form then seeds the dataset's Pipeline config (row count and teacher model) and lands you on the dataset's **PIPELINE** tab — not the build-progress page — where you author and run the full generation pipeline. Running that pipeline is what writes parquet into the repo and flips the status to `ready`. The teacher/judge selections here pre-seed the pipeline; the actual generation columns are authored on the Pipeline tab (see below).

## 5. Hugging Face import — `/studio/datasets/import`

Fields:

- **Repository** (required) — a Hugging Face Hub search input; enter as `org/name` (e.g. `tatsu-lab/alpaca`).
- **Subset** (optional) — config / subset name, if the dataset has one.
- **Access token** (optional) — `hf_…`, needed only for private or gated repos.
- **Destination branch** — a branch combobox; created in the Data Hub if it doesn't exist (defaults to `main`).
- **Destination folder** (optional) — leave empty to import at the repo root.

**Import dataset** spawns an `import_dataset` compute job (params: `hf_repo_id`, `hub_repo_id`, `hub_branch`, and optional `hub_path` / `hf_token` / `hf_dataset_subset`) and hands off to the building page. This is a compute job, not a `/api/datasets` call — track it in **Compute → Workload Queue**. The flow is gated on the Free plan (shows an Upgrade prompt).

---

## Build progress — `/studio/datasets/building`

The from-chats, upload, and import flows hand off to a progress page. It shows a percentage bar, a per-kind step checklist, and an estimated time remaining. Each build kind has its own steps:

- **From chats**: Extract messages from chats → Scrub PII → Tokenize & pack pairs → Validate & publish to repo.
- **Upload**: Parse the uploaded file → Validate the schema → Pack rows → Validate & publish to repo.
- **Import**: Resolve the repository → Download files → Convert & pack rows → Validate & publish to repo.
- **Synthetic**: Spin up teacher & judge → Generate samples → Judge & filter by quality → Validate & publish to repo.

You can **Run in background** (return to the list) or **Cancel build** at any time. The page runs a cosmetic progress timer and lands you on the finished dataset (resolved by name) or the list. When a build carries a real dataset id, it instead polls `/api/datasets/{id}` for the actual status, caps the bar until the dataset reports `ready`, and surfaces a **Build failed** state if it errors.

## Dataset detail page

Open a dataset to see its tabs. Overview, Samples, and Pipeline are always present; Repository appears once the dataset has a Hub repo, and a Synthetic Runs tab appears for collected-training-data datasets.

### Overview

Backed by `GET /api/datasets/{id}/stats`, which the Data Hub's stats worker computes on each commit to the underlying repo:

- KPI strip: **Rows**, **Avg / Min / Max / P95 tokens**.
- **Token Distribution** histogram (with min / p50 / p95 / max).
- **Column Char-Length** table (mean / p50 / p95 / p99 / max per string column).
- **Duplicates** — duplicate groups and affected rows.
- **PII Findings** — matches per pattern (email, US phone, SSN, credit card, IPv4).
- **Details** — format, source, created, updated.

Token-length and PII stats only appear once a text column is detected; until the first commit is processed you'll see "Stats haven't been computed for this dataset yet."

### Samples

Previews the first 20 rows via `GET /api/datasets/{id}/samples?limit=20&split=<split>`. A split selector switches between splits (default `train`, or the first available). Rows that fit the SFT/DPO chat convention render as instruction → response; other rows fall back to a generic key-value column view.

🚧 Known issue: the header counter sometimes shows N samples while the Samples tab shows 0 rows. Workaround: navigate away and back.

### Pipeline

A DataDesigner canvas for authoring a generation/transformation pipeline — this is where synthetic datasets are actually built. The header sets the **target row count** and **default model**; the column palette adds **Seed column**, **Sample from distribution**, **Generate with LLM (Text / Structured / Code)**, **Judge with LLM**, **Compute from expression**, and **Validate** columns. Edits autosave (`PUT /api/datasets/{id}/pipeline`). **Preview** runs 1–200 rows without committing (`POST .../pipeline/preview`); **Run** generates the full target (`POST .../pipeline/run`, tagged `run-<timestamp>`) and commits it to the repo. Preview/run execute as managed compute jobs; their logs are at `/api/datasets/pipeline-jobs/{jobId}/logs`.

### Repository

The underlying lakeFS repo — files, commits, branches, tags. Same operations as any Data Hub repo.

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

## Datasets for evaluation

When you want a dataset specifically for **evaluation** rather than training, use:

- **From Conversations** filtered by 👎 — your worst cases become an eval / regression set.
- **From Conversations** filtered by 👍 — your best cases become regression checks.
- **Upload file** with hand-crafted edge cases.

Then reference this dataset in the [Evaluation](./evaluations.md) wizard.

## Delete

Deleting runs a pre-flight in-use check (`GET /api/datasets/{id}/in-use`). If the dataset is referenced by an active training or synthetic run, deletion is blocked with a conflict — stop the listed runs from their detail pages first. On delete, the platform also cancels any in-flight pipeline jobs and drops the backing Hub repo.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/datasets` | List (`?project_id`, `?kind`, `?limit`) |
| `GET` | `/api/datasets/{id}` | Detail |
| `POST` | `/api/datasets` | Create (generic) |
| `PATCH` | `/api/datasets/{id}` | Update metadata |
| `DELETE` | `/api/datasets/{id}` | Delete (with in-use check) |
| `GET` | `/api/datasets/{id}/in-use` | List active + historical references |
| `POST` | `/api/datasets/from-conversations` | Build from an agent's sessions |
| `POST` | `/api/datasets/upload` | Upload a file (multipart) |
| `POST` | `/api/datasets/synthetic` | Provision a synthetic dataset shell |
| `POST` | `/api/datasets/expert-training` | Provision a collected-training-data dataset + run |
| `GET` | `/api/datasets/{id}/stats` | Overview stats |
| `GET` | `/api/datasets/{id}/samples` | Preview samples (`?split`, `?limit`) |
| `GET` / `PUT` | `/api/datasets/{id}/pipeline` | Read / save pipeline config |
| `POST` | `/api/datasets/{id}/pipeline/preview` | Preview run (1–200 rows) |
| `POST` | `/api/datasets/{id}/pipeline/run` | Full generation run |
| `GET` | `/api/datasets/{id}/pipeline/active` | In-flight pipeline job, if any |
| `GET` | `/api/datasets/{id}/pipeline/jobs/{jobId}` | Pipeline job state |
| `POST` | `/api/datasets/{id}/pipeline/jobs/{jobId}/cancel` | Cancel a pipeline job |
| `GET` | `/api/datasets/pipeline-jobs/{jobId}/logs` | Tail pipeline job logs |

Hugging Face imports run as an `import_dataset` job via the compute API, not a `/api/datasets` route.

## What's next

[Training](./training.md) to fine-tune on a dataset. [Evaluations](./evaluations.md) to test with one.

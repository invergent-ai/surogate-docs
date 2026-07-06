---
title: Evaluations
sidebar_position: 3
---

# Evaluations

Evaluations test models and agents against benchmarks. Two paths: pick from the 40 built-in benchmarks, or build a Custom Benchmark.

## The benchmarks catalog

Click **BROWSE BENCHMARKS** in the Evaluations page. 40 benchmarks grouped into 9 categories:

| Category | Examples |
|---|---|
| **Reasoning** | GSM8K, ARC-AGI, GPQA |
| **Language** | HellaSwag |
| **Knowledge** | MMLU, MMLU-Pro, MMLU-Redux, SuperGPQA |
| **Coding** | HumanEval, HumanEval+, MBPP, LiveCodeBench v6, Text-to-SQL (BIRD) |
| **Safety** | TruthfulQA, ToxiGen, Red Team, Guardrails |
| **Chat** | MT-Bench |
| **Instruction** | IFEval, IFBench |
| **Agent** | SWE-bench (Verified / Multilingual / Pro), Terminal-Bench 2.0, TAU-Bench, BFCL v4, MCP-Atlas, MCPMark, Tool Decathlon, DeepPlanning, WideSearch, VITA-Bench |
| **Vision** | MMMU, MMMU-Pro, MathVista, ChartQA, DocVQA, OCRBench, HallusionBench, RealWorldQA |

Each benchmark has its own detail page with:

- **What it measures**
- **How it works** — the test methodology
- **Strengths** — what it's good at differentiating
- **Limitations** — what it doesn't tell you
- **When to use** — pick this benchmark if you're optimising for X
- **Use cases** — agent types that benefit from this benchmark

Click **RUN EVALUATION** at the top of any benchmark detail to start a run on this benchmark.

## Custom Benchmark builder

When the built-in benchmarks don't match your use case, build a custom one:

1. **NEW EVALUATION** → **Custom Benchmark**.
2. Configure:
   - **Name** — `my-customer-support-eval-v1`
   - **Description** — what the benchmark tests
   - **Dataset** — pick a dataset (typically a 👎 corpus or hand-crafted edge cases)
   - **Metric** — exact-match | LLM-judge | regex | custom Python
   - **Judge configuration** — if using LLM-judge, which model and what prompt
3. Save. The custom benchmark is now in your benchmarks catalog.

## The 3-step NEW EVALUATION wizard

Whether built-in or custom:

### Step 1 — Select

Pick the benchmark(s). You can select multiple to run in batch.

### Step 2 — Configure

- **Target model** — the model or agent being evaluated
- **Judge LLM** — if the benchmark uses an LLM judge (most do for subjective metrics):
  - **External** — OpenRouter / Anthropic / OpenAI / your endpoint
  - **Colocated** — a model already in the platform's Models page
- **API Key** — for external judge (required; missing key causes silent failures — H3 in the audit)
- **Subset** — sample size if you want a quick run (e.g. 100 samples instead of full set)

### Step 3 — Target & Run

Confirm the target + judge + benchmark. Click RUN EVALUATION.

Creating and running are **two steps**: the wizard first saves the run as a **draft** (`POST /api/eval-runs`), then launches it (`POST /api/eval-runs/{id}/start`). A draft can be edited before it's launched, and a running eval can be halted with `POST /api/eval-runs/{id}/stop`. Both boundaries are gated: `402` if the project's plan doesn't include evaluations, or if it's out of ML-compute credits.

## What an evaluation produces

A run report with:

- **Overall score** — pass rate / accuracy / weighted score
- **Per-sample breakdown** — which samples passed/failed, with the model's actual output
- **Comparison** — if you ran the same benchmark on a previous model, side-by-side scores
- **Drift detection** — when re-running on the same model, alerts on regressions

### Export a report

A finished run can be exported as a standalone report via `GET /api/eval-runs/{id}/export?format=html` (or `format=md`). The download bundles the run's scores, compare/previous deltas, and metadata (model, judge, compute, duration) into a single HTML or Markdown file you can share outside Studio.

## Leaderboard

`GET /api/leaderboard` aggregates completed eval runs across the project (or a single project scope) into a ranked view, so you can see how each model/agent stacks up on the benchmarks you've run without opening each run individually.

## Side-by-side: A/B evaluation

A common pattern: compare two versions of your agent.

1. Build a Custom Benchmark from your 👎 corpus.
2. Run it on `agent-v1` (current production).
3. Run it on `agent-v2` (the candidate).
4. Compare per-sample scores; look at the diffs where v2 wins or regresses.

If v2 net-improves and doesn't regress on critical cases, promote it.

See [Use cases → A/B evaluation](../use-cases.md).

## LLM judge — when you need one

Many benchmarks have objective metrics (test passes/fails, math answer matches). But subjective benchmarks (helpfulness, tone, completeness) need an LLM judge:

- Higher-capability judge → better discrimination but more expensive
- Same judge across all your evals → comparable scores over time
- Be transparent about the judge's prompt — the judge's bias is your bias

## REST API

Runs live under `/api/eval-runs`; the benchmark catalog under `/api/benchmarks`; the ranked view under `/api/leaderboard`. Create and start are separate calls.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/eval-runs` | List runs |
| `GET` | `/api/eval-runs/{id}` | Run detail |
| `POST` | `/api/eval-runs` | Create (draft) — `402` if the plan lacks evaluations |
| `POST` | `/api/eval-runs/{id}/start` | Launch — `402` if out of ML-compute credits |
| `POST` | `/api/eval-runs/{id}/stop` | Stop a running eval |
| `GET` | `/api/eval-runs/{id}/scores` | Per-benchmark scores |
| `GET` | `/api/eval-runs/{id}/samples` | Per-sample breakdown |
| `GET` | `/api/eval-runs/{id}/export` | Export report (`?format=html` or `md`) |
| `GET` | `/api/benchmarks` | Benchmark catalog |
| `GET` | `/api/leaderboard` | Ranked cross-run leaderboard |

## What's next

[Hub](./hub.md) for versioned eval reports. [Use cases](../use-cases.md) for end-to-end recipes.

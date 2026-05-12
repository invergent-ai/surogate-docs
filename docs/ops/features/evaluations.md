---
title: Evaluations
sidebar_position: 3
slug: /features/evaluations
---

# Evaluations

An Evaluation is a scored run of an agent or a model against a benchmark or a fixture set. Use it to answer: *is the new version better than the old one?*

The Evaluations page is a two-pane layout — runs list on the left, detail of the selected run on the right.

## Three tabs

- **Eval Runs** — a reverse-chronological list of every single run. The default view.
- **Benchmark Suite** — reusable suites you compose runs from. A suite is a named collection of test cases with a scoring rubric (LLM judge, exact match, regex, or numeric tolerance).
- **Leaderboard** — cross-eval ranking. Pick a metric, the table sorts models or agents by that score. Only completed runs contribute.

## Start an evaluation

Click **◈ New Evaluation**. The dialog asks four things:

- **Target Model** — which model to call.
- **Compare to** — pick a previous run to power the **Comparison** tab, or leave as *— none —* for a standalone eval.
- **Cluster** — which compute pool runs the eval. Lists your connected backends plus the project-local cluster.
- **GPU** — drawn from the chosen cluster's offers.

Hit **Run Evaluation**. The run lands at the top of Eval Runs with status `Running`. It also appears in the Workload Queue under kind `eval` — cancel from there if you need to abort.

## The detail pane

Selecting a run loads four sub-tabs:

| Tab | Contents |
|---|---|
| **Results** | Headline scores per metric. Bars + numbers. |
| **Comparison** | Side-by-side scores against the run you set in *Compare to*. |
| **Samples** | Per-case drill-down: input → output → expected → judge verdict. Filter to wins, losses, errors. |
| **Details** | The run's full configuration: target, suite, suite version, dataset version, runtime params, seed. |

**Re-run** on a row repeats the same suite and target with a fresh seed (useful for variance estimation). **Export** downloads the run's results.

## When to use a suite vs ad-hoc

- **Suite** when you'll run the same evaluation repeatedly — every release, every fine-tune, every prompt change. Treat suites as your team's regression tests.
- **Ad-hoc** for one-off questions: *does the new model handle SQL better?* *Does enabling this skill change anything?*

## Where to go next

- **[Arenas](./arenas.md)** — when one eval isn't enough and you want a tournament.
- **[Datasets](./datasets.md)** — where eval fixtures live.
- **[Compute → Workload Queue](./compute.md)** — to watch or cancel a running eval.

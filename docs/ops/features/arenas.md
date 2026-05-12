---
title: Arenas
sidebar_position: 9
slug: /features/arenas
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Arenas

`/studio/arenas` is the home for **tournaments** between agents or models — multi-run evaluations that converge on a winner over time. An Arena is one orchestrated study; you can have many concurrent.

## When to use it

- Comparing two candidate model versions or agent configurations.
- Running an automated curriculum where each round seeds the next.
- Curating expert datasets through collaborative or adversarial play.

## Where it lives

- List: `/studio/arenas`. Status tabs: `All · Running · Paused · Won · Failed · Terminated`. Each tab carries a live count.
- Detail: `/studio/arenas/<arena-id>`.

> The list rendered on a fresh account is **example data** (Qwen3 convergence study, Code review duel, etc.). Your own arenas replace it after the first **+ Create Arena**.

## Create Arena flow

The dialog opens as a **multi-step wizard** — dialog header **Create Arena**, navigation via **Back** / **Next** buttons.

### Step 1 — Objective

Four objective cards, exact labels and helper text:

| Objective | Description shown in the UI |
|---|---|
| **Dataset generation** | _Curate expert-grade synthetic datasets. Coordinator applies acceptance policy and promotes accepted examples._ |
| **Collaborative** | _Participants work together toward a shared goal. Coordinator promotes cross-cutting findings._ |
| **Adversarial** | _Participants compete. Coordinator judges rounds and declares a winner._ |
| **Other** | _Hybrid or custom objective. Coordinator decides outcome._ |

### Step 2 — Identity

Single text field, placeholder `e.g. Qwen3 convergence study`. The label is the Arena's name.

### Subsequent steps

Step list TODO(verify) — observed Step 1 and Step 2 only on the test account. Expected: contestants (agents / models), benchmark or task pack, run budget, stop criteria.

The **Cancel** / **Close** affordances abandon the wizard at any step.

## Status reference

| Status | Meaning |
|---|---|
| Running | Rounds executing or queued. Compute reserved. |
| Paused | No active rounds. Compute released. Resumable. |
| Won | A contestant converged with statistical significance on the decisive metric. |
| Failed | Eval failures pushed the arena past its tolerance. |
| Terminated | Operator stopped the arena early. Cannot be resumed — open a fresh one. |

See [Lifecycle → Arena](../concepts/lifecycle.md#arena) for the full state machine.

## Reading an arena

The detail at `/studio/arenas/<arena-id>` includes:

- Round-by-round scores per contestant.
- The Coordinator's verdict on each round.
- The eval runs spawned by the arena, cross-linked to `/studio/evaluations`.
- For Dataset-generation arenas: the dataset's growing row count and the rejection rate.

## Permissions

| Action | Role |
|---|---|
| View list / detail | Project `viewer` and above |
| + Create Arena | Project `editor` or `owner` |
| Pause / Resume / Terminate | Project `editor` or `owner` |

## Gotchas

- **Won** is decided on the **headline metric** declared in Step 1. Read the per-contestant table to see whether other metrics align with the verdict.
- Pausing an arena releases compute. Resuming re-enqueues rounds and may wait for capacity again.
- Dataset-generation arenas write into a Dataset of kind `synthetic` ([Datasets](./datasets.md)). Verify the dataset's repo namespace before kicking off — outputs land there.

## Related

- [Evaluations](./evaluations) — single-run scoring that feeds arenas.
- [Datasets](./datasets) — destination for Dataset-generation arenas.
- [Models](./models)

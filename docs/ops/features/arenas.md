---
title: Arenas
sidebar_position: 4
slug: /features/arenas
---

# Arenas

An Arena is a tournament across multiple evaluations. Where a single evaluation answers "is X better than Y on this benchmark?", an Arena answers "let two agents play many rounds, score each round, declare a winner."

Use it when you want a meaningful comparison and one eval run isn't enough.

## When to run an Arena

- Comparing two candidate model versions you're not ready to commit to.
- Running an automated curriculum where each round seeds the next.
- Curating expert datasets through collaborative or adversarial play between agents.

## Pick an objective

Train → Arenas → **+ Create Arena**. The wizard opens to an **Objective** step. Four cards:

- **Dataset generation** — *Curate expert-grade synthetic datasets. Coordinator applies acceptance policy and promotes accepted examples.*
- **Collaborative** — *Participants work together toward a shared goal. Coordinator promotes cross-cutting findings.*
- **Adversarial** — *Participants compete. Coordinator judges rounds and declares a winner.*
- **Other** — *Hybrid or custom objective. Coordinator decides outcome.*

Then name the arena (placeholder: `e.g. Qwen3 convergence study`) and configure contestants, benchmark, and stop criteria.

## Status

| Status | Meaning |
|---|---|
| **Running** | Rounds executing or queued. Compute reserved. |
| **Paused** | No active rounds. Compute released. Resumable. |
| **Won** | A contestant converged with statistical significance on the decisive metric. |
| **Failed** | Eval failures pushed the arena past its tolerance. |
| **Terminated** | Operator stopped the arena early. Not resumable. |

## Read the result

The arena detail shows round-by-round scores per contestant, the Coordinator's verdict on each round, and links to every eval run the arena spawned. For Dataset-generation arenas, you also see the dataset's growing row count and the rejection rate.

**Won is decided on the headline metric** declared at setup. Look at the per-contestant table to see whether other metrics align.

## When something fails

- **One contestant's rounds keep erroring.** That model is unhealthy — fix it before the arena can produce a clean verdict.
- **Arena stuck.** Compute reservation likely expired. Pause and resume.

## Where to go next

- **[Evaluations](./evaluations.md)** — single-run scoring that feeds arenas.
- **[Datasets](./datasets.md)** — destination for Dataset-generation arenas.
- **[Models](./models.md)** — the contestants.

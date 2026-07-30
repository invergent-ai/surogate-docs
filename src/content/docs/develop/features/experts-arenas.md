---
title: "Experts & arenas"
---

An **arena** is a supervised, multi-agent run: a *coordinator* agent drives a set of *participant* agents toward an objective, and the run ends when a success **predicate** is met. It is the platform's mission-control view for agents working together (or against each other) on a goal.

This page documents the Arenas UI at `/studio/arenas`. For the conceptual model of experts and skills, see [Skills & experts](/develop/features/skills-and-experts/) — this page is the complementary "where do I watch and steer a run" surface.

:::note[Preview]
The Arenas screens are a **frontend-only preview**: they render representative sample data with no backend wiring. The layout below reflects the real UI, but the numbers are illustrative and the controls (create arena, pause/resume, terminate, steer, import to dataset) don't yet drive real runs. Treat this page as a design preview of where multi-agent runs will be watched and steered.
:::

## Arenas list

The list page shows one card per arena. The header summarizes counts (running / paused / won). Controls:

- **Filter arenas…** text box — matches on name and objective.
- Status filter chips: **All**, **Running**, **Paused**, **Won**, **Failed**, **Terminated** (each with a count).
- **+ CREATE ARENA** — opens the arena wizard.

Each card shows the objective type, objective text, live status, elapsed time, participant count and avatars, a top-line metric with a sparkline, and progress toward the predicate. Cards flag **N pending** approvals and **policy paused** states. Click a card to open its detail page.

### Objective types

| Type | What it is |
|---|---|
| **Collaborative** | Participants work together toward a shared goal. |
| **Adversarial** | Participants compete; a judge-style coordinator awards rounds. |
| **Dataset generation** | Agents generate and curate accepted examples toward a target count. |
| **Other** | Open-ended objective. |

### Success predicates

An arena ends when its predicate is satisfied. Cards render the predicate as progress:

| Predicate | Shown as |
|---|---|
| **Metric threshold** | `current / value` bar for a named metric. |
| **Dataset target** | `accepted / target` count bar. |
| **Coordinator judged** | The coordinator decides (no numeric bar). |
| **Python snippet** | A custom Python predicate (shows a snippet preview). |

## Create Arena wizard

**+ CREATE ARENA** opens a stepped wizard:

1. **Type & name** — pick the objective type and name the arena.
2. **Objective** — describe the goal and choose the predicate kind (metric threshold, coordinator-judged, or Python snippet).
3. **Coordinator** — choose a coordinator template. Options are gated by objective type, e.g. `research-coordinator` (collaborative/other), `tournament-coordinator` (adversarial), `curation-coordinator` (dataset generation), or a custom coordinator you author.
4. **Participants & authorized set** — choose the participant agents and the set of agents authorized to be activated. Initial participants are auto-added to the authorized set.
5. **Policy** — *(dataset-generation arenas only)* curation/acceptance policy.
6. **Budget & caps** — spend and resource limits.

## Arena detail page

`/studio/arenas/$arenaId` is a three-pane mission-control view. A header strip shows the objective type, workspace repo, creator, and the full objective, with lifecycle actions gated by status:

- **RESUME** (when paused), **PAUSE** (when running), **TERMINATE** (when running or paused).
- **IMPORT TO DATASET** — shown for dataset-generation arenas, to pull accepted examples into a dataset.
- **BACK** returns to the arenas list.

### Participants (left pane)

Lists the coordinator plus every participant. Each entry is an *activation* of an authored agent (its own branch, model base, iteration, headline metric, heartbeat and lease). Select one to drill in; click to filter the timeline to just that agent.

### Event timeline (center pane)

A live feed of arena events — commits, milestones, steering messages, promoted findings, blocks, approval requests, activations, accepted/rejected examples, policy changes, coverage gaps, and coordinator decisions. Can be filtered to a single participant (with a **CLEAR FILTER** button) or show "all participants · live".

### Mission / Agent (right pane)

Two toggle tabs:

- **Mission** — overall mission state for the arena.
- **Agent: `<name>`** — enabled once you select a participant; drills into that agent's activity within the arena.

An **Ask coordinator** button sits in this pane's header.

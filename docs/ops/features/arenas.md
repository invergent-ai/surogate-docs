---
title: Arenas
sidebar_position: 9
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Arenas

## What it does

`/studio/arenas` is the home for **tournaments** between agents or models — multi-run evaluations that converge on a winner over time. An Arena is one orchestrated study; you can have many concurrent.

## When to use it

- Comparing two candidate model versions or agent configurations.
- Running an automated curriculum where each round seeds the next.
- Hosting an internal "competition" for the best skill / prompt.

## Prerequisites and permissions

- **Read**: any project member.
- **+ Create Arena**: project `editor` or higher. _TODO(verify._

## Where to find it

- List: `/studio/arenas` (status tabs `All · Running · Paused · Won · Failed · Terminated`).
- Detail: `/studio/arenas/<arena-id>`. _TODO(verify) — not reachable from a fresh account; the page route exists in code._

> The list shown by default on a fresh account is **example data** (e.g. "Qwen3 convergence study", "Code review duel"). Your own arenas will replace it.

## Step-by-step — Create an Arena

1. Open **/studio/arenas**.
2. Click **+ Create Arena** (top-right).
3. _TODO(verify) — fill in name, contestants (agents/models), benchmark, run budget, stop criteria._
4. Submit. The arena appears under **Running**.

## Status filters and lifecycle

`All · Running · Paused · Won · Failed · Terminated`. See [Lifecycle → Arena](../concepts/lifecycle#arena) for the state machine.

## Edge cases and gotchas

- **Paused** arenas don't consume compute. They can be resumed at any time. _TODO(verify._
- **Won** does not mean every metric won — read the arena detail to confirm which metric was decisive.
- A **Terminated** arena cannot be resumed — open a fresh one.

## Related

- [Evaluations](./evaluations)
- [Models](./models)

---
title: Coordination & the board
sidebar_position: 6
---

# Coordination & the board

How a session becomes a strict coordinator that delegates instead of doing the work itself, and how the fan-out of workers it spawns coordinate through a shared, verified board.

## Coordinator sessions

Any session that spawns children (`spawn_worker`, `delegate_task`, or `spawn_task`) is acting as a coordinator. Two entry points turn a session into a **strict** coordinator, where the platform structurally prevents the agent from "just doing the work itself".

### Missions and auto-research

Starting a [mission](../../work/tools/missions.md) with `/mission` (or a research run with `/auto-research`) stamps the session as a strict coordinator. On creation the platform:

- sets `coordinator = true` and `strict_coordinator = true` on the session config;
- **strips implementation tools** — file I/O, terminal/process, web, browser, vision, KB reads, and artifact creation are subtracted from the effective tool set, so the model cannot fall back to direct execution;
- **preloads an orchestrator skill** — `subagent-task-orchestrator` for missions, or `arbor-coordinator` for research runs — that documents the delegate-everything playbook the tool stripping assumes.

What remains is the coordination surface: `spawn_task` / `delegate_task` / `spawn_worker`, `cancel_task` / `unblock_task`, `consult_expert`, `ask_user_question`, `memory`, `todo`, `session_search`, the skill tools, and the scheduling tools. The coordinator decomposes the goal into specialist sub-agent tasks, gates dependencies with `parents=[…]`, and ends criterion-driven rounds with a verifier task whose evidence the evaluator checks. This filtering is structural, not merely a prompt instruction — the tools are absent from the model's schema, not just discouraged.

For the operator's view of missions (dashboard, status badges, control commands) see [Missions](../../work/tools/missions.md); for the sub-agent definitions a coordinator spawns, see [Sub-agents](../../work/tools/sub-agents.md).

## The coordination board

The board is the **shared, verified context** for a fan-out of parallel sub-agents. Workers post what they learn; every member of the group — siblings, retries, and the coordinator — sees it, without the information being diluted by routing through the parent. A dead end hit by one worker becomes a note the next worker reads *before* repeating it.

### How a group forms

Group formation is automatic — there is no flag and deliberately no enable knob, because a fan-out has a board by definition:

1. On a session's **first spawn** (any of the three paths) it self-assigns `context_group_id = <its own session id>`, and the child inherits it.
2. Every later spawn — including task retries and orchestrator-role grandchildren — inherits the same id. One board per fan-out tree.
3. Board tools appear automatically for group members and never for solo sessions.

### Note types

| Type | Cap | Meaning |
|---|---|---|
| `FACT` | 200 chars | Concrete reusable knowledge, anchored to a file / symbol / endpoint / error |
| `FAIL` | 200 chars | A dead end actually hit, with the observed reason — the highest-value note for peers |
| `CLAIM` | 200 chars | A short-lived "I am working on X" to prevent overlap; expires automatically (default 300 s, renewable by re-posting) |
| `RESULT` | 400 chars | A candidate outcome with mandatory evidence: `outcome=… \| evidence=… \| risk=…` |

A new `RESULT` from the same writer supersedes its previous one. Notes can carry a `ref` pointer to expandable detail.

### Board tools

| Tool | Purpose |
|---|---|
| `share_note` | Post one or more notes (batched). Returns which were `admitted`, which claims were `renewed`, and which were `rejected` with a reason |
| `read_board` | The consolidated **current** state (supersede/expiry applied) at a decision point — inline history updates may be stale |
| `expand_note` | Follow a note's `ref` to the underlying event or artifact, bounded to 4000 chars, confined to the same group |

### Admission — nothing unverified reaches the board

`share_note` runs a two-stage gate; rejected notes are returned as tool feedback, never stored:

1. **Deterministic pre-checks** — type validity, size caps, the same prompt-injection and secret scans that guard [memory](../features/memory.md#safety), duplicate detection, claim-renewal detection, a per-writer claim cap (2 active), and a per-group note cap (300).
2. **LLM verification** — always on, using the tenant's summary model. `RESULT` evidence must describe a check *actually run* with a concrete outcome; `FACT` / `FAIL` must be specific and anchored; vague notes are rejected with a reason the model can learn from. This is **fail-closed**: if the verifier is unavailable, nothing is admitted — so everything visible on a board has passed the gate.

Admitted notes emit a `board.note` event on the writer's session for audit.

### How members read the board

- **Join snapshot** — the first iteration that sees a non-empty board appends one `board.update` with the windowed render (priority `RESULT` > `FACT` > `FAIL` > `CLAIM`, with budget reserved for `FAIL` so dead ends never scroll out).
- **Per-iteration deltas** — each iteration appends a compact `board.update` with new notes and transitions (superseded / expired / renewed). Events always append at the **end** of history, never mid-list, so the provider prefix cache and event replay stay stable.
- **Render format** — `[n42 w3f2/FAIL +2m] content`: note id (for `expand_note`), writer label (`coord` for the group root, `w<hex4>` for a worker), age, and remaining TTL for claims.

### Lifecycle

A maintenance sweeper (part of [background jobs](./background-jobs.md), ~5-minute cadence) expires lapsed claims and purges: notes of groups whose root has been terminal for over 7 days, aged superseded/expired rows, and orphaned notes whose group matches no session.

### Configuration

Board behaviour is tuned with `SUROGATES_BOARD_*` environment variables (snapshot window, delta size, claim TTL, per-writer claim cap, per-group note cap, purge age). There is no enable flag. The admission verifier reuses the tenant's existing summary model — no extra model configuration.

### API

`GET /v1/sessions/{session_id}/board` returns `{group_id, notes, render}`; it 404s when the session is not a coordination-group member.

## Relationship to missions

A mission coordinator spawning tasks is a fan-out root, so a board forms automatically: mission workers coordinate, retries inherit verified knowledge from failed attempts, and the coordinator receives live deltas instead of waiting for each `worker.complete` summary. The board can inform a worker but cannot flip a mission verdict — the judge and mission state machine are untouched.

## Related

- [Missions](../../work/tools/missions.md) — starting and tracking a coordinated goal.
- [Sub-agents](../../work/tools/sub-agents.md) — the named definitions a coordinator spawns as workers.
- [Background jobs](./background-jobs.md) — the async primitives that form a coordination group, and the board sweeper.
- [Event types](./event-types.md) — `board.note`, `board.update`, and the sub-agent events.

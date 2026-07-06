---
title: Agent memory
sidebar_position: 11
---

# Agent memory

Agents keep a small, curated store of durable facts that survives across sessions, so a user never has to repeat themselves.

This page is about an **agent's runtime memory** — what it remembers between conversations. It is unrelated to the trainer's [memory guide](../../guides/memory.md), which covers GPU memory during model training.

## What memory holds

Memory is deliberately small and file-shaped. Two Markdown files store section-delimited entries, which keeps memory human-readable, inspectable, and editable:

| File | Holds | Character limit |
|---|---|---|
| `MEMORY.md` | The agent's own notes — environment facts, project conventions, tool quirks, lessons learned | 2,200 chars total |
| `USER.md` | Who the user is — name, role, preferences, communication style | 1,375 chars total |

Entries are separated by a section sign (`§`) and can be multiline. Limits are counted in characters (not tokens) so they are model-independent.

The split maps to two `target` values the agent chooses between: `memory` (its notes) and `user` (the user profile). Priority when memory fills up is user preferences and corrections first, then environment facts, then procedural knowledge.

## What gets saved — and what doesn't

The agent writes memory proactively, without being asked, when it is worth remembering:

- **Save:** corrections ("remember this" / "don't do that again"), stable preferences and personal details, environment facts (OS, installed tools, project structure), conventions and API quirks specific to the user's setup.
- **Skip:** task progress, session outcomes, completed-work logs, temporary TODO state, raw data dumps, and anything trivial or easily re-discovered. Past-session recall is handled by session search, not memory; reusable procedures belong in a skill.

## How memory is surfaced

Memory is injected into the system prompt as a **frozen snapshot** taken when the session starts. Mid-session writes are persisted to disk immediately (durable) but do **not** change the current session's prompt — this keeps the prompt stable across all turns so the provider prefix cache stays intact. The next session picks up the updated snapshot.

## Editing memory

An agent edits memory through the built-in `memory` tool:

| Parameter | Values | Notes |
|---|---|---|
| `action` | `add`, `replace`, `remove` | |
| `target` | `memory`, `user` | Which file to write |
| `content` | string | The entry text (required for `add` / `replace`) |
| `old_text` | string | Short unique substring identifying the entry to `replace` or `remove` |

Adding an entry that already exists is a no-op, and writes that would exceed the target's character limit are rejected with a "would exceed limit" message so the agent replaces or removes an entry first.

Operators can read and edit the same entries over REST — `GET /memory` returns both targets with usage strings; `POST /memory` takes the same `action` / `target` / `content` / `old_text` shape. UI writes and agent writes land on the same underlying bytes.

## Safety

Every memory write — from the tool or the API — is scanned before storage, because memory is injected into the system prompt. Entries are rejected if they contain prompt-injection or role-hijack phrasing, secret-exfiltration payloads (curl/wget with credentials, reading `.env`/credentials files), SSH-backdoor patterns, or invisible/bidirectional Unicode characters.

## Where memory lives

Memory files are stored per agent and per user in the tenant's object storage (S3 / Garage), under the agent's slice of the memory bucket. Writes are atomic (temp file + rename) and guarded by a file lock so concurrent turns never corrupt a file.

## Idle flush

When a session goes idle long enough, an idle-session-reset background job reviews the transcript and saves anything important to `MEMORY.md` / `USER.md` before tearing down the sandbox, then emits a `session.reset` event. The session itself is untouched — the user can return and continue. See [Background jobs](../reference/background-jobs.md) and the `session.reset` row in [Event types](../reference/event-types.md).

## Related

- [Tool catalog → Memory](../reference/tool-catalog.md) — the `memory` tool at a glance.
- [Sessions](./sessions.md) — how conversations are recorded.
- [Background jobs](../reference/background-jobs.md) — the idle flush that captures memory before teardown.

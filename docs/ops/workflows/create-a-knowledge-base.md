---
title: Create a knowledge base
sidebar_position: 4
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Workflow — Create a knowledge base

<video controls width="720" muted>
  <source src="/videos/06-new-knowledge-base.webm" type="video/webm" />
</video>

## Goal

Create a searchable document store and attach it to an agent.

## Prerequisites

- Project role: `editor` or higher.
- A source for the documents (file upload, URL, Git, Hub repo). _TODO(verify supported source types._

## Steps — Create the KB

1. Switch to **Develop** and open **/studio/knowledge-bases**.
2. Click **+ New Knowledge Base** (top-right).
3. Name the KB.
4. Pick a **source**. _TODO(verify._
5. Configure source-specific settings (auth, branch, paths).
6. Pick an **embedding model**. _TODO(verify default._
7. Click the final **Create** action.
8. The KB lands in **Compiling**. Wait for it to move to **Active** (visible in the status badge).

## Steps — Attach to an agent

1. Open the agent (Develop mode) under **/studio/agents/&lt;id&gt;**.
2. Find the **Knowledge Bases** section in Settings.
3. Pick the KB from the dropdown.
4. Save. The next chat session uses the KB.

## Gotchas

- An **Active** KB with a new source push may flip back to **Compiling** during re-index. Agents keep returning the old results until re-index finishes.
- A KB stuck in **Compiling** for an unusually long time usually means a large source or a slow embedder — check **/studio/compute/workload-queue** for an `eval`/`task` job related to the KB. _TODO(verify the exact job kind._
- A KB in **Error** typically means a fetch error (auth, 404). Open the KB to see per-document status.

## Related

- [Knowledge Bases](../features/knowledge-bases)
- [Agents](../features/agents)
- [Data Hub](../features/hub) — pushing a KB to the Hub for reuse.

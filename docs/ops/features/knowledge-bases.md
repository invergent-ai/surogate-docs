---
title: Knowledge Bases
sidebar_position: 3
slug: /features/knowledge-bases
---

# Knowledge Bases

A Knowledge Base (KB) is an indexed document store that agents read at runtime. You point it at a source — your help center, your wiki, a folder of PDFs — and Surogate compiles it into an embedding index. Agents then query the KB during a conversation to ground their answers in your content.

## When to use a KB

- Your agent should answer from your own docs, not from whatever the model learned in pretraining.
- The source content changes — a wiki, a help center, a product spec — and you want answers to track edits.
- You need retrieval calls to be visible: opening a session shows which documents the agent pulled from, which makes debugging answers tractable.

## Create one

Build → Knowledge Bases → **+ New Knowledge Base**. Fill four fields:

- **Display Name** — what users see in lists and on agent settings.
- **Slug** — permanent identifier; can't be changed later.
- **Description** *(optional)* — shown on the KB card.
- **Source** — pick where the documents come from: file upload, URL, Git, S3, an existing Hub repo.

Submit. The KB lands in **Compiling** while Surogate fetches and embeds the source. When the compile finishes it flips to **Active** and is attachable to agents.

A compile workload appears in [Compute → Workload Queue](./compute.md) with kind `task`. Big sources (thousands of documents) can take minutes to compile.

## Attach to an agent

Open the agent → **Settings** → **Knowledge bases** multi-select → redeploy. Multi-select means an agent can read from several KBs at once; the agent decides which to query for each turn.

A KB in **Compiling** or **Error** state can be attached. The agent returns no retrieval results until the KB reaches **Active**.

## Re-indexing

Saving a KB triggers re-index. While the new index builds, the agent keeps hitting the previous index — there's no read-time gap. The new index swaps in atomically when the compile completes.

For sources that change frequently (a wiki on a daily edit cadence), set the compile to run on a schedule rather than re-saving by hand.

## Status

| Status | Meaning |
|---|---|
| **Compiling** | Surogate is pulling the source and building the embedding index. |
| **Active** | Index ready; queries return results. |
| **Error** | A document fetch or the indexing step failed. Open the KB to see per-document errors. |

## When something fails

- **Stuck in Compiling longer than expected.** Open [Compute → Workload Queue](./compute.md) and filter to `task`. Find the related job. If **Queued**, no compute is available. If **Failed**, click the row for logs.
- **Active but retrieval returns nothing.** Two possibilities. Either the agent isn't pinned to this KB version (redeploy), or your query is outside the KB's embedding distribution (the topic is genuinely not in the source). Open a session and look at the retrieval step to confirm.
- **Error with a 401/403 source.** A source credential expired upstream. Re-enter in the KB's settings.

## Where to go next

- **[Agents](./agents.md)** — to attach a KB.
- **[Sessions](./sessions.md)** — to read the retrieval trajectory.
- **[Data Hub](./hub.md)** — to share a KB across projects.

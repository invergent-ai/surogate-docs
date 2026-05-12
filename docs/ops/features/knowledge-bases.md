---
title: Knowledge Bases
sidebar_position: 4
slug: /features/knowledge-bases
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Knowledge Bases

A Knowledge Base (KB) is an indexed document store an agent reads at runtime. Surogate compiles documents into an embedding index, exposes it via retrieval calls inside an agent's loop, and tracks compilation status so you know whether the KB is ready.

## Lifecycle

| Status | Meaning |
|---|---|
| Compiling | Surogate is pulling sources and building the embedding index. |
| Active | Index ready. Agents using the KB get retrieval results. |
| Error | A source fetch or the indexing job failed. Per-document errors are visible inside the KB detail. |

Status filter tabs on the list page: `All · Active · Compiling · Error` with live counts.

## Where it lives

- `/studio/knowledge-bases` (builder view, full controls). Status filter, **Filter knowledge bases…** input, **+ New Knowledge Base** action.
- `/work/knowledge-bases` (operator view, browse-only). Same components, no Edit / Delete.
- Per-KB detail at `/studio/knowledge-bases/<kb-id>` (TODO(verify the route slug) — not reachable on the test account).

## New Knowledge Base flow

1. Open `/studio/knowledge-bases`.
2. Click **+ New Knowledge Base**. The dialog header reads **New Knowledge Base**.
3. Fill the dialog. Exactly these fields:

   | Field | Type | Notes |
   |---|---|---|
   | **Display Name** | text | The label across `/work` and `/studio` and on agent settings. |
   | **Slug** | text | Help text: _"unique within project"_. Stable identifier and URL segment. Cannot be changed once set. |
   | **Description (optional)** | textarea | Shown on the KB card and in tooltips. |
   | _Source picker_ | combobox | Unlabeled but required. Pick where the documents come from. |

4. Submit with **Create**. The KB lands in **Compiling** while Surogate fetches and embeds the source. The dialog has **Cancel** and **Close** controls; both abandon without saving.
5. When the compile finishes, status flips to **Active** and the KB becomes attachable to agents.

## Attaching to an Agent

1. Open the agent's settings (`/studio/agents/<id>` → Settings).
2. In **Knowledge bases**, pick the KB. Multi-select is supported.
3. Save and re-deploy. Sessions started after redeploy will have retrieval available.

A KB in **Compiling** or **Error** can be attached. The agent will simply return zero retrieval results until the KB reaches **Active**.

## Re-indexing

Saving a KB triggers re-index. On large KBs (thousands of docs) this can take minutes. The status badge updates live via the monitor socket (see [Monitoring](./monitoring) — the same channel powers both surfaces).

While re-indexing, queries continue to hit the previous index. The new index swaps in atomically on completion.

## Permissions

| Action | Role |
|---|---|
| List, browse | Project `viewer` and above |
| New / Edit / Delete | Project `editor` or `owner` (TODO(verify)) |
| Attach to an agent | Same role required to edit the agent |

## Troubleshooting

- **Stuck in Compiling for too long.** Open `/studio/compute/workload-queue?filter=task` and find the related job. If it's **Queued**, no compute is available. If it's **Failed**, click the row for logs.
- **Error with a 401/403 source error.** A source credential expired or was rotated. Re-enter under [Integrations](../admin/integrations) or in the KB's settings.
- **Active but retrieval returns nothing.** The agent isn't pinned to this KB version, or the query is outside the KB's embedding distribution. Re-deploy the agent and check the Trajectory tab in a session to see the retrieval call.

## Related

- [Agents](./agents) — to attach a KB.
- [Data Hub](./hub) — publish a KB for reuse across projects.
- [Workflow — Create a knowledge base](../workflows/create-a-knowledge-base)

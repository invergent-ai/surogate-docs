---
title: Knowledge Bases
---

A KB is a curated corpus the agent can search and read at runtime via `kb_search_pages`, `kb_list_pages` and `kb_read_page`. Where a skill teaches the agent **how** to do something, a KB tells it **what it knows**.

For the operator's view, see [Work mode → Knowledge bases](/work/library/knowledge-bases).

## How a KB works (architecturally)

![Creating a knowledge base: display name, slug, description and language](../../../../assets/screenshots/work-kb-create.png)

```
Source files (markdown, PDF, CSV)
        │
        ▼ uploaded via POST /api/knowledge-bases/{id}/sources
   ┌─────────────────────────────┐
   │   Curator (an LLM)          │
   │   Reads sources, extracts   │
   │   structured knowledge,     │
   │   deduplicates              │
   └─────────────┬───────────────┘
                 │ COMPILE (POST /api/knowledge-bases/{id}/compiles)
                 ▼
   ┌─────────────────────────────┐
   │   Wiki — searchable index   │
   │   (Hub-versioned)           │
   └─────────────┬───────────────┘
                 │
                 ▼  kb_search_pages / kb_list_pages / kb_read_page at runtime
   Agent's session context grows by relevant pages
```

The curator distills and links the material into a wiki. Hybrid search covers passages from both original sources and generated pages. Agents can read exact source passages, expand to the parent document, or follow a PDF section tree to its page ranges.

## What a KB carries

| Field | Notes |
|---|---|
| **Name** | Unique within your org |
| **Description** | Free-form |
| **Curator model** | Set in the **Configure** tab. Defaults to Surogate; see [Curator model](#curator-model). |
| **Sources** | List of files / S3 prefixes / GitHub repos / Notion pages / URLs (only File works in current builds) |
| **Status** | `error` (no successful compile yet) → `compiling` → `active` |
| **Counters** | sources, wiki pages, attached agents |

Published artifacts are versioned in Hub. Search results and reads refer to the same published content. A failed compile preserves the previous publication; changing a Hub branch alone does not roll back the search registry.

## Five source types

Five types are listed in ADD SOURCE. **Only File is enabled in current builds** — the rest are scaffolded but not yet wired.

| Type | Available | Notes |
|---|---|---|
| **File** | ✅ | Upload `.md`, `.pdf`, `.txt`, `.docx`, `.csv` |
| **S3** | 🚧 | Recursive pull from a bucket/prefix |
| **GitHub** | 🚧 | Auto-pull from a repo's docs folder with branch tracking |
| **Notion** | 🚧 | OAuth into a Notion workspace |
| **URL** | 🚧 | Crawl a domain or specific URLs |

When the other source types ship, they'll have continuous sync (re-compile on detected changes).

## Curator model

Not chosen at creation. Change it later in the **Configure** tab of the KB. The choices are **Surogate** (the default), **Surogate Pro**, and any model deployed in the KB's project. A change applies to the next compile; use **Rebuild** to redo pages an earlier model wrote.

The curator runs once per source on COMPILE. The cost is dominated by the size of the source corpus.

## Compile

```bash
curl -X POST http://localhost:8000/api/knowledge-bases/{id}/compiles \
  -H "Authorization: Bearer $TOKEN"
```

What happens:

1. For each source: read, parse, chunk
2. For each chunk: curator extracts structured knowledge
3. Per-source wiki page assembled
4. Cross-source synthesis index built
5. Wiki committed to the Hub

Compile time: 30s to several minutes per source.

### When compile fails

A failed source is marked `error` with its recorded message in the SOURCES list. Source, concept-generation, upload or publication failures leave the previous published knowledge available. Successfully prepared summaries are checkpointed for a retry; a PDF retry also recovers its extracted source and section tree.

- **Retry the failing file** — transient failures (curator LLM rate limits) are common, and files a dead compile left locked are requeued automatically on every finalize path, so retry never reports "no files to compile"
- **Reduce source size** — splitting large documents into chapters can shorten individual retries. Long PDFs use the section-tree indexer; oversized documents and sections are summarized in parts, then combined so the summary process covers the full text.
- **Check format** — corrupt PDFs and non-UTF-8 markdown choke the parser
- **Read the per-file error** — it names the actual reason

### Document identity and ingestion diagnostics

Expand **Document identity and ingestion** under a source file to see extracted
titles, identifiers, explicit editions and aliases with their source quotations.
This works across document types and languages. Filename and content claims are
kept separately; disagreements are flagged, and matching identifiers never
automatically merge documents. Edition strings are preserved without inferring
dates from codes.

Identity extraction uses a bounded sample from the beginning and end of the
source and separate optional model calls for filename and content. Quotes are checked
against extracted source text, but identity interpretation can still be incomplete
or incorrect. Agents should read the source before selecting a document or edition.

Identity extraction uses the configured base model by default; bulk summaries
keep using the summary model. Operators can set `kb_identity_llm_profile: summary`
to use the summary model for both. The base profile can cost more per source.
An identifier that exactly equals the complete filename stem is also confirmed
in code, preserving punctuation and version suffixes.

The same disclosure shows the latest ingestion attempt's warnings and failures,
including pages with no extracted text, failed or limited image captioning,
section-index fallback, rejected identity claims and missing embeddings at
publication. Diagnostic counts include a few examples. A blank PDF page can be
intentional, so inspect the original before treating it as missing content.

Published identity remains available when a later compile fails. The ingestion
report records the latest attempt, not a full history or current health status;
an embedding backfill may have repaired an earlier warning. Existing sources
receive this metadata when compiled again; rebuild the KB to populate all files.

## Detail tabs

Open a knowledge base to see four tabs: **Overview**, **Sources**, **Review** and **Configure**. Viewers can read every tab. **Build**, **Delete**, source changes and the Configure settings are disabled for them. **Retry document**, **Retry N documents** and the review buttons (**Confirm identity**, **Confirm link**, **Reject reference**, **Undo decision**, **Save decision**, **Undo latest decision**) stay clickable, but the server refuses them ([what each role can do](/work/settings/members/#what-each-role-can-do)).

### Overview

The stat cards (Sources, Wiki pages, Files, Attached to) sit above the **KB health** card. Its summary line lists only what is true: failed documents, documents with warnings, queued documents, and search entries that need embeddings. During a build it reports the build instead.

- **Needs attention** lists documents with ingestion problems, 25 per page. Each row has **Retry document** (confirmation first, because it uses model credits), **Review document** (opens the Review tab on that file) and **Referenced by** (the change-impact dialog). **Retry N documents** retries every retryable row on the page.
- **Recent builds** lists the compile runs.
- When statement conflicts are open, a line shows the count and **Review statement conflicts**.
- Health refreshes with **Refresh**, and again when the latest build or the source count changes.

**Referenced by** is also on each file in the **Sources** tab. It is read-only: confirmed links, possible matches, review decisions and wiki pages that depend on the file, the documents with incoming links (each with **Open document review**), and a warning when link extraction is incomplete. Removing a source opens this dialog in removal mode, with the impact first. If document links or reviews in the knowledge base changed since the preview, the removal is refused: the dialog shows the error and reloads the preview, so confirm again against the new one.

### Review

Two sub-tabs.

**Identities & links** is the document review queue. Filters: **Needs review**, **Decision history** or **All references**; **All issue types**, **Identity** or **Document links**; and a filename filter. To review an item:

1. For an identity item, which shows the identifiers and editions extracted from a file, tick the ones you verified and click **Confirm identity**.
2. For a link item, a reference from one document to another, pick the target document from the suggestions or by searching, then click **Confirm link** or **Reject reference**.
3. Tick "I checked the source evidence" (required for both) and optionally add a reason.

**Undo decision** reverts a decision. A decision applies to the document versions reviewed; a changed source or target needs another review.

**Statement conflicts** compares statements that disagree across documents. Filters: **Open conflicts**, **Reviewed comparisons** or **All comparisons**, plus a filename filter. Each comparison shows both quotations and a **Review decision**:

- Sources conflict, needs correction
- Both apply under different conditions
- Use statement A for this comparison
- Use statement B for this comparison
- Incorrect comparison

A reason is required, and you confirm that you checked both quotations. **Save decision** stores it, and **Undo latest decision** reverts it. Agents see unresolved disagreements and your current decision when they read either source. If the sources change, the comparison shows **Sources changed** and is archived. Statement conflicts are produced by **Semantic analysis** (see Configure).

Saving a review decision needs the editor role, like every other write on this page.

### Configure

Settings save as soon as you change them and apply to the next compile. They are locked while a build runs, and for viewers.

| Setting | What it does |
|---|---|
| **Language** | The language the wiki is written in. It also picks the OCR model for scanned PDFs. Only English and Romanian have OCR support; other languages are marked "no OCR support" and fall back to English OCR, which garbles accents. A change affects documents added afterwards until you rebuild. |
| **Curator model** | The model that reads each document and writes the wiki: **Surogate**, **Surogate Pro** or a deployed model. |
| **Vision model** | Describes figures extracted from PDFs. **Platform default** or a deployed model. It must accept images. |
| **Semantic analysis** | Extracts references and stated facts, then compares statements across documents. Feeds link review and statement conflicts. It is the slowest part of a compile. |
| **Concept pages** | Writes pages that gather what many documents say about one topic. Slow on large KBs; without them, answers that combine many documents take longer. |

**Rebuild knowledge base** appears at the bottom when the KB has sources. **Build** only processes new documents and missing search vectors. Rebuild re-curates every document from scratch, including text extraction, summaries, analysis and the wiki, so use it to apply a changed setting to documents already processed. When some documents were curated with a different curator model, language or prompt, a note says how many. The confirmation dialog shows how many documents will be processed, warns that it can take hours on a large KB and uses model credits, and says "Reviews remain valid only while their source and target versions still match." When statement comparisons are affected, it also says how many and that reviews will need re-checking. Confirm with **Rebuild everything**.

## Wiki search

After attaching a KB, agents use `kb_search_pages` for hybrid lexical/vector search across their permitted knowledge bases, then `kb_read_page` to read the matching pages. Validate retrieval by asking the attached agent representative questions and inspecting its search and read tool results.

For a known document, use `kb_search_pages(query="DOC-003", mode="documents")`
to look up an exact filename, title, identifier or explicit alias. Results make
ambiguity and filename/content conflicts explicit. Case and whitespace are
normalized; punctuation, accents and edition differences remain meaningful.
If identity lookup finds nothing, search content with `mode="passages"` (the
default). Both modes use the same permitted KB scope.

Search hits include a `passage_id` when an exact evidence passage is available. Pass it to `kb_read_page` with the returned KB ID and path. Omit it to expand the document; use `pages` for a PDF range. Reads report the published version and location.

For table headings or clauses continued around a passage, pass `context="surrounding"` together with `passage_id`. The reader keeps the passage and expands its PDF page and immediate neighbors within a budget. Markdown sources receive a window around the passage. The default is 8,000 source characters, with a maximum of 24,000; `limit` sets the budget. Each slice reports its original location and marks omitted text. Use a parent read or PDF `pages` range for further context; `surrounding` cannot be combined with `pages` or `offset`.

Deleting a source file retires its dependent searchable evidence. Existing KBs need a full rebuild to populate source passages and provenance.

The wiki browser's "Search wiki" field filters page titles locally; it does not run the agent's retrieval pipeline.

## Attach to an agent

```bash
curl -X POST http://localhost:8000/api/agents/{agent_id}/knowledge-bases \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"kb_id": "..."}'
```

The agent's system prompt gains:

```

## Available Knowledge Bases

- acme-product-docs: Product documentation, runbooks, known-issues database.
  Browse via kb_list_pages("acme-product-docs"), then kb_read_page(path).
```

Plus the agent's tool catalogue grows by `kb_search_pages`, `kb_list_pages` and `kb_read_page`.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/knowledge-bases` | List |
| `GET` | `/api/knowledge-bases/{id}` | Detail |
| `POST` | `/api/knowledge-bases` | Create. Body: `{name, display_name, description, curator_language}` |
| `DELETE` | `/api/knowledge-bases/{id}` | Delete (pre-flight: warns if attached to agents) |
| `GET` | `/api/knowledge-bases/{id}/sources` | List sources |
| `POST` | `/api/knowledge-bases/{id}/sources` | Add source (multipart for File, JSON for others) |
| `DELETE` | `/api/knowledge-bases/{id}/sources/{source_id}` | Remove source |
| `POST` | `/api/knowledge-bases/{id}/compiles` | Trigger a compile (`?rebuild=true` for a rebuild) |
| `POST` | `/api/knowledge-bases/{id}/compiles/stop` | Stop the active compile |
| `GET` | `/api/knowledge-bases/{id}/compiles` | List compiles |
| `GET` | `/api/knowledge-bases/{id}/wiki/pages` | List wiki pages |

## What's next

[MCP & Vault](/develop/features/mcp-and-vault/) for external system integration. [Datasets](/develop/features/datasets/) for the other corpus type used in training.

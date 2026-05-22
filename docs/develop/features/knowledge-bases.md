---
title: Knowledge Bases
sidebar_position: 3
---

# Knowledge Bases

A KB is a curated corpus the agent can search at runtime via `kb_search`. Where a skill teaches the agent **how** to do something, a KB tells it **what it knows**.

For the operator's view, see [Work mode → Knowledge bases](/work/library/knowledge-bases).

## How a KB works (architecturally)

```
Source files (markdown, PDF, CSV)
        │
        ▼ uploaded via POST /v1/knowledge-bases/{id}/sources
   ┌─────────────────────────────┐
   │   Curator (an LLM)          │
   │   Reads sources, extracts   │
   │   structured knowledge,     │
   │   deduplicates              │
   └─────────────┬───────────────┘
                 │ COMPILE (POST /v1/knowledge-bases/{id}/compile)
                 ▼
   ┌─────────────────────────────┐
   │   Wiki — searchable index   │
   │   (lakeFS-versioned)        │
   └─────────────┬───────────────┘
                 │
                 ▼  kb_search at runtime
   Agent's session context grows by relevant pages
```

The curator does the work of distilling, structuring, cross-referencing — agents don't read raw documents at runtime, they search the curated wiki.

## What a KB carries

| Field | Notes |
|---|---|
| **Name** | Unique within your org |
| **Description** | Free-form |
| **Curator model** | Locked at creation — can't be changed later. Default works for most cases; pick a smarter model (Claude Sonnet 4.6, GPT-5) at creation for highly technical content. |
| **Sources** | List of files / S3 prefixes / GitHub repos / Notion pages / URLs (only File works in current builds) |
| **Status** | `error` (no successful compile yet) → `compiling` → `active` |
| **Counters** | sources, wiki pages, attached agents |

The compiled wiki is versioned in the Hub — every COMPILE produces a new commit you can roll back to.

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

Locked at KB creation. Can't be changed later. Common choices:

- **Surogate default** — fine for most cases
- **Claude Sonnet 4.6** — better for highly technical content
- **GPT-5** — alternative

The curator runs once per source on COMPILE. The cost is dominated by the size of the source corpus.

## Compile

```bash
curl -X POST http://localhost:8000/v1/knowledge-bases/{id}/compile \
  -H "Authorization: Bearer $TOKEN"
```

What happens:

1. For each source: read, parse, chunk
2. For each chunk: curator extracts structured knowledge
3. Per-source wiki page assembled
4. Cross-source synthesis index built
5. Wiki committed to lakeFS

Compile time: 30s to several minutes per source.

### When compile fails

This is the single flakiest pipeline in current builds. If COMPILE returns `task failed`:

- **Retry** — many failures are transient (curator LLM rate limit)
- **Reduce source size** — split large PDFs into chapter-sized chunks
- **Check format** — corrupt PDFs and non-UTF-8 markdown choke the parser
- **Check OVERVIEW → RECENT COMPILES** for the one-line reason

Bug-track: this is the H4 issue from the audit — the platform should surface curator-side errors more clearly. Most of the time you'll see only `task failed` without detail.

## Wiki search

The same search the agent uses at runtime:

```bash
curl "http://localhost:8000/v1/knowledge-bases/{id}/wiki/search?q=refund+policy" \
  -H "Authorization: Bearer $TOKEN"
```

Returns ranked wiki pages with snippets. Pre-test your KB before attaching to an agent — if the right pages don't surface for typical queries, the curator didn't extract what you need.

## Attach to an agent

```bash
curl -X POST http://localhost:8000/v1/agents/{agent_id}/knowledge-bases \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"kb_id": "..."}'
```

The agent's system prompt gains:

```
## Available Knowledge Bases

- acme-product-docs: Product documentation, runbooks, known-issues database.
  Search via kb_search("acme-product-docs", "your query").
```

Plus the agent's tool catalogue grows by `kb_search` and `kb_query`.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/knowledge-bases` | List |
| `GET` | `/v1/knowledge-bases/{id}` | Detail |
| `POST` | `/v1/knowledge-bases` | Create. Body: `{name, description, curator_model}` |
| `DELETE` | `/v1/knowledge-bases/{id}` | Delete (pre-flight: warns if attached to agents) |
| `GET` | `/v1/knowledge-bases/{id}/sources` | List sources |
| `POST` | `/v1/knowledge-bases/{id}/sources` | Add source (multipart for File, JSON for others) |
| `DELETE` | `/v1/knowledge-bases/{id}/sources/{source_id}` | Remove source |
| `POST` | `/v1/knowledge-bases/{id}/compile` | Trigger compile |
| `GET` | `/v1/knowledge-bases/{id}/wiki` | Browse wiki |
| `GET` | `/v1/knowledge-bases/{id}/wiki/search?q=` | Search wiki |

## What's next

[MCP & Vault](./mcp-and-vault.md) for external system integration. [Datasets](./datasets.md) for the other corpus type used in training.

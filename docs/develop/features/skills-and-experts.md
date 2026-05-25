---
title: Skills & Experts
sidebar_position: 2
---

# Skills & Tools

The **Skills & Tools** page in the Develop nav has two tabs: **SKILLS** and **MCP SERVERS**. A skill is a markdown file (`SKILL.md`) the agent loads into its prompt. An **expert** is a skill whose `type` is `expert` — backed by a fine-tuned model that runs in a bounded mini-loop.

This chapter covers both. For the operator's walk-through of writing a skill in the UI, see [Work mode → Skills](/work/library/skills).

## `SKILL.md` format

Markdown with YAML frontmatter:

```markdown
---
name: code_reviewer
description: Reviews code for quality, security, and best practices
trigger: review code, code review, check this code
tools: [read_file, search_files, write_file]
type: skill                    # default; use 'expert' for model-backed
tags: [security, quality]
platforms: ["linux", "macos"]
requires_tools: [read_file]
fallback_for_tools: []
---

You are a code reviewer. When asked to review code:

1. Read the files specified by the user.
2. Check for:
   - Security vulnerabilities (OWASP top 10)
   - Performance issues
   - Code style and readability
   - Missing error handling
3. Provide specific, actionable feedback with line references.
4. Suggest concrete fixes, not just descriptions of problems.
```

### Frontmatter

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Lowercase, alphanumeric + hyphens, 1-64 chars |
| `description` | string | yes | Shown to the LLM in `skills_list` |
| `trigger` | string \| list | recommended | Keywords/phrases matched against the user message |
| `tools` | list | no | Tools this skill uses (for progressive disclosure) |
| `type` | string | no | `skill` (default) or `expert` |
| `tags` | list | no | Metadata for categorisation |
| `platforms` | list | no | Restrict to OSes `["linux", "macos", "windows"]` |
| `requires_tools` | list | no | Hidden unless ALL listed tools are available |
| `fallback_for_tools` | list | no | Hidden when ALL listed tools are available |
| `enabled` | bool | no | Default `true` |

Body text after the frontmatter is the skill's prompt content — inlined into the system prompt when the skill triggers, or returned by `skill_view` when explicitly invoked.

## The 4-layer loading model

Skills load from four layers in increasing precedence:

```
Layer 1: Platform      /etc/surogates/skills/                       (lowest)
Layer 2: User files    tenant-{org_id}/users/{user_id}/skills/
Layer 3: Org (DB)      skills table, org-wide (user_id IS NULL)
Layer 4: User (DB)     skills table, user-specific                  (highest)
```

Higher layers override by name. Org admins always win — an end user cannot override a skill the org admin has set. Setting `enabled: false` in a higher layer disables the skill entirely.

## Conditional activation

Two fields:

- `requires_tools` — skill included only if **all** listed tools are available in the agent's allowlist
- `fallback_for_tools` — skill excluded when **all** listed tools are available; only appears when at least one is missing

Use `fallback_for_tools` for graceful degradation. Example:

```yaml
---
name: manual-web-search
description: Guides the user through manual web research
fallback_for_tools: [web_search]
---
```

Only loads when the agent's `web_search` tool is denied.

Use `requires_tools` to gate skills that depend on specific tools:

```yaml
---
name: container-debug
description: Diagnoses issues inside running containers
requires_tools: [bash, docker]
---
```

The loader evaluates conditional activation after merging all four layers.

## agentskills.io / Hermes compatibility

Skills authored in the [agentskills.io](https://agentskills.io) format are loaded without modification. The loader reads conditional fields and tags from the `metadata.hermes` namespace:

```yaml
---
name: hermes-skill
description: A skill using the Hermes frontmatter convention
metadata:
  hermes:
    requires_tools: [bash]
    fallback_for_toolsets: [web_search]
    tags: [devops, ci]
---
```

Recognised hermes keys:

| Hermes key | Maps to |
|---|---|
| `requires_tools` | `requires_tools` |
| `requires_toolsets` | `requires_tools` |
| `fallback_for_tools` | `fallback_for_tools` |
| `fallback_for_toolsets` | `fallback_for_tools` |
| `tags` | `tags` |

Top-level keys win when both are set.

## Dynamic skill commands

Users invoke a skill explicitly via `/<skill-name> [args...]`:

```
/research vector databases
/babysit-prs
```

Resolution order in the harness:

1. Builtin commands (`/clear`, `/compress`, `/goal`, `/loop`, `/mission`)
2. Dynamic skill resolution
3. Plain user message if no match

For dynamic invocation, the harness calls `skill_view` server-side and inlines the body into the user message.

## Skill REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/skills?type=skill\|expert&enabled=true` | List |
| `POST` | `/v1/skills` | Create. Body: `{name, content, category?, user_id?}` |
| `GET` | `/v1/skills/{name}` | Detail |
| `PUT` | `/v1/skills/{name}` | Update. Body: `{content}` |
| `DELETE` | `/v1/skills/{name}` | Delete |

API-created skills land in the database (layer 3 or 4 depending on `user_id`). Agent-created skills (via the `skill_manage` tool) go to the tenant bucket (layer 2).

## Validation rules

| Rule | Constraint |
|---|---|
| Name | Lowercase, alphanumeric + hyphens, 1-64 chars |
| Name uniqueness | No duplicates within scope (user or org) |
| Frontmatter | Must include `name` and `description` |
| Content size | Body ≤ configured limit (default 100 KB) |
| File path | Must be within tenant's skill directory |

Validation errors return `422 Unprocessable Entity`.

## Publishing — versioning

When you PUBLISH a skill, you tag a version in the underlying lakeFS repo. Tags are immutable. Editing creates a new draft; the next PUBLISH creates `v0.1.1`, `v0.2.0`, etc.

Sessions record which version of each skill they used. You can:

- Roll back to a previous tag
- Replay sessions against a different skill version (regression testing)
- Audit "which skill version was active for session X"

---

# Experts — model-backed skills

When you set `type: expert` on a skill, you turn it into something different. The body becomes the **expert's system prompt** (not the agent's), and you specify a model + endpoint.

## Example

```markdown
---
name: sql_writer
description: Writes PostgreSQL queries from natural language descriptions
type: expert

model: qwen2.5-coder-7b
endpoint: http://expert-pool.your-cluster.svc:8000/v1
trigger: SQL queries, database schemas, PostgreSQL, data analysis

tools: [terminal, read_file, search_files]
max_iterations: 10
expert_status: draft
---

You are a PostgreSQL expert for this organisation. When given a natural
language description, write a correct, efficient query.

Rules:
- Always use explicit column names (never SELECT *)
- Use CTEs for complex queries
- Include comments explaining non-obvious joins
- Validate against the schema before returning
```

### Frontmatter for experts

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | yes | — | Expert name |
| `description` | yes | — | Shown to the base LLM |
| `type` | yes | `skill` | Must be `expert` |
| `model` | yes | — | Model name passed to the inference endpoint |
| `endpoint` | no | — | OpenAI-compatible URL (can be set at activation) |
| `trigger` | yes for routing | — | Phrases describing when to select this expert |
| `adapter` | no | — | LoRA adapter path in tenant storage |
| `tools` | no | `[]` | Tools the expert can use in its mini-loop |
| `max_iterations` | no | `10` | Max tool-call rounds before budget exceeded |
| `expert_status` | no | `draft` | `draft` / `collecting` / `active` / `retired` |

## The expert lifecycle

```
1. Define     SKILL.md with type: expert            expert_status: draft
2. Collect    POST /v1/skills/{name}/collect         expert_status: collecting
3. Train      Externally (your fine-tuning pipeline)
4. Activate   POST /v1/skills/{name}/activate        expert_status: active
5. Monitor    GET /v1/skills/{name} → expert_stats   (auto-retire if < 60%)
6. Retrain    Collect → train → activate             (loop)
```

### 1. Define

Create the SKILL.md with `type: expert, expert_status: draft`. Place in `tenant-{org_id}/shared/skills/<name>/SKILL.md` or via REST.

### 2. Collect training data

```bash
curl -X POST http://localhost:8000/v1/skills/sql_writer/collect \
  -H "Authorization: Bearer $TOKEN"
```

The platform walks the events table and exports successful trajectories as OpenAI fine-tuning JSONL. Two modes:

- **Bootstrap** (`collect_for_skill`) — walks `skill.invoked` events for this skill name. Use to train an expert from an existing prompt-based skill.
- **Improve** (`collect_for_expert`) — walks `expert.delegation → tool.call → expert.result` chains. Use once the expert is active to train on fresh successful trajectories.

Both filter tainted sessions by default (`policy.denied`, `harness.crash`, `saga.compensated`, `expert.override`).

Export lands at `tenant-{org_id}/shared/skills/{name}/training/dataset_YYYYMMDD_HHMMSS.jsonl`.

### 3. Train (external)

Your fine-tuning pipeline reads the JSONL. Compatible with:

- OpenAI fine-tuning API
- Anthropic fine-tuning (when available)
- Unsloth (local LoRA)
- Axolotl (config-driven)
- Custom training scripts using `transformers` + `peft`

Output: a fine-tuned model with an OpenAI-compatible serving endpoint.

### 4. Activate

```bash
curl -X POST http://localhost:8000/v1/skills/sql_writer/activate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "http://expert-pool:8000/v1"}'
```

After activation, the base LLM sees the expert in its system prompt under `# Available Experts`. The harness routes hard tasks matching the expert's triggers; the base LLM can also explicitly call `consult_expert("sql_writer", task="...")`.

### 5. Monitor

```bash
curl http://localhost:8000/v1/skills/sql_writer \
  -H "Authorization: Bearer $TOKEN"
```

Response includes `expert_stats`:

```json
{
  "name": "sql_writer",
  "type": "expert",
  "expert_status": "active",
  "expert_stats": {
    "total_uses": 47,
    "total_successes": 44
  }
}
```

After ≥20 invocations, the platform monitors success rate. Below the threshold (default 60%), the expert is auto-retired.

### 6. Retire / retrain

```bash
curl -X POST http://localhost:8000/v1/skills/sql_writer/retire \
  -H "Authorization: Bearer $TOKEN"
```

To retrain: collect fresh data → train → activate with new endpoint.

## The expert mini-loop

When `consult_expert(name, task, context)` is called:

```
1. Load the expert's SKILL.md
2. Make an OpenAI-compatible request to the expert's endpoint
   with model = expert.model
3. The expert can call tools from its restricted set (expert.tools)
4. Iterate up to max_iterations
5. Return the expert's final assistant message to the base LLM
6. Base LLM reviews and either accepts, modifies, or rejects
```

Bounded — can't go forever, can't escalate its tool surface, can't keep the conversation going. Just answer the delegated question.

## REST API for experts

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/skills?type=expert` | List experts |
| `POST` | `/v1/skills/{name}/collect` | Export training JSONL |
| `GET` | `/v1/skills/{name}/training-data` | List exported datasets |
| `POST` | `/v1/skills/{name}/activate` | Set status to active |
| `POST` | `/v1/skills/{name}/retire` | Set status to retired |
| `GET` | `/v1/skills/{name}/file?path=training/dataset_XYZ.jsonl` | Download a specific export |

## What's next

[Knowledge Bases](./knowledge-bases.md) for the other half of "agent's knowledge." [MCP & Vault](./mcp-and-vault.md) for external tool integration. [Datasets](./datasets.md) and [Training](./training.md) for the training pipeline.

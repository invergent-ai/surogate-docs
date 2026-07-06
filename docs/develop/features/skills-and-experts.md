---
title: Skills
sidebar_position: 2
---

# Skills & Tools

The **Skills & Tools** page in the Develop nav has two tabs: **SKILLS** and **MCP SERVERS**. A skill is a markdown file (`SKILL.md`) the agent loads into its prompt.

For the operator's walk-through of writing a skill in the UI, see [Work mode → Skills](/work/library/skills).

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
| `GET` | `/api/skills?is_expert=true&project_id=` | List (filter `is_expert` for experts only) |
| `POST` | `/api/skills?project_id=` | Create. Body: `{name, content, description, ...}` |
| `GET` | `/api/skills/{skill_id}` | Detail |
| `PATCH` | `/api/skills/{skill_id}` | Update. Body: partial skill fields |
| `POST` | `/api/skills/{skill_id}/publish` | Tag a version |
| `DELETE` | `/api/skills/{skill_id}` | Delete (409 if in use) |

Skills are addressed by `skill_id`, not by name. API-created skills land in the database (layer 3 or 4 depending on `user_id`). Agent-created skills (via the `skill_manage` tool) go to the tenant bucket (layer 2).

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

## What's next

[Knowledge Bases](./knowledge-bases.md) for the other half of "agent's knowledge." [MCP & Vault](./mcp-and-vault.md) for external tool integration. [Datasets](./datasets.md) and [Training](./training.md) for the training pipeline.

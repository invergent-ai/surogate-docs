---
title: Hub
sidebar_position: 5
---

# Data Hub

Every artifact in Surogate is a **lakeFS repository** — a git-like store with branches, commits, and tags. The Data Hub (link in the Develop sidebar) is the browser for those repos.

## What's in the Data Hub

| Artifact type | Hub repo pattern |
|---|---|
| Skills | `p-{project_id}/skill-{slug}` |
| Experts | `p-{project_id}/skill-{slug}` (same as skill; type:expert in SKILL.md) |
| Knowledge bases | `p-{project_id}/kb-{slug}-{uuid}` |
| Datasets | `p-{project_id}/ds-{uuid}` |
| Models | `p-{project_id}/model-{slug}-{uuid}` |
| Experiments | `p-{project_id}/exp-{slug}-{uuid}` |
| Environments | `p-{project_id}/env-{slug}-{uuid}` |

Each repo has:

- **Files** — the artifact contents
- **Commits** — version history
- **Branches** — parallel lines (`main` is default; you can fork for experiments)
- **Tags** — immutable named versions (e.g. `v0.1.0`, `v0.2.0`, `v0.2.0-audit`)
- **Refs** — branch or tag identifiers used to fetch specific versions

## The Hub UI

Hub page lists every repo in your project. Filters:

- **Repo type** — Models / Datasets / Skills / Experiments / Environments
- **Search** — by name
- **Tags filter** — when implemented

Click any repo to open its browser:

- **Files** — current directory, file count, sizes
- **Commits** — history with author + message + relative timestamp
- **Branches** — list of branches
- **Tags** — versioned tags
- **Info** — repo metadata
- **lakeFS://** breadcrumb — navigate up
- **branch combobox** — switch between branches/tags

Click any file to view it inline. Markdown renders, code highlights, CSV displays as a table.

## Operations

### Create a repository

**Hub → NEW REPOSITORY** → pick a type (Skill / Dataset / Model / Experiment / Environment) → name + optional description → create. The repo is initialised with a `main` branch.

### Import from Hugging Face

**Hub → IMPORT REPOSITORY** → paste HF repo URL → pick destination path in your hub → import. Files are pulled and committed to `main`.

### Tag a commit

When you PUBLISH a skill, the platform tags the current `main` commit (e.g. `v0.1.0`). You can also tag via the REST API:

```bash
curl -X POST http://localhost:8000/api/hub/repositories/{owner}/{repo}/tags \
  -d '{"branch": "main", "tag": "v0.2.0", "message": "Better example queries"}'
```

### Branch

Branches let you iterate without breaking production. Create a feature branch off `main`, edit, test, then merge.

```bash
curl -X POST http://localhost:8000/api/hub/repositories/{owner}/{repo}/branches \
  -d '{"name": "feature/refactor-prompt", "source": "main"}'
```

### Delete a repo

**Hub → repo → DELETE**. Pre-flight check warns if any agent uses an attached artifact from this repo.

## Why this matters

The Hub is what makes agent improvement durable. Three properties:

- **Reproducibility** — sessions record which version of each skill/KB/model they used. If a problem appears, you can re-run on the exact same versions.
- **Rollback** — every version is preserved. Roll back a problematic skill version with one click.
- **Diff** — see exactly what changed between two versions. Use for change reviews ("did this skill update break anything?").

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/hub/repositories` | List |
| `GET` | `/api/hub/repositories/{owner}/{repo}` | Detail |
| `GET` | `/api/hub/repositories/{owner}/{repo}/in-use` | Reference pre-flight |
| `GET` | `/api/hub/repositories/{owner}/{repo}/branches` | Branches |
| `GET` | `/api/hub/repositories/{owner}/{repo}/tags` | Tags |
| `GET` | `/api/hub/repositories/{owner}/{repo}/refs/{branch}/commits` | Commits on a branch |
| `GET` | `/api/hub/repositories/{owner}/{repo}/refs/{branch}/objects/ls?path=` | Directory listing |
| `DELETE` | `/api/hub/repositories/{owner}/{repo}` | Delete |

## What's next

[Datasets](./datasets.md) for one of the most important Hub repo types. [Training](./training.md) for what produces model repos.

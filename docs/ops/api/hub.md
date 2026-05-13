---
title: Hub API
sidebar_position: 3
slug: /api/hub
description: Git, S3, and REST surfaces for the Surogate Hub registry. Push, pull, list, manage repos and tokens.
---

# Hub API

The [Data Hub](../features/hub.mdx) is HuggingFace-compatible. Three surfaces let you reach it programmatically: a Git endpoint for repository clones and pushes, an S3-compatible endpoint for direct blob transfer, and a REST endpoint for metadata.

For the conceptual overview, see **[API overview](./overview.md)**.

## Endpoints

| Surface | Endpoint | Use it for |
|---|---|---|
| **Git over HTTPS** | `git.studio.internal:3000` | `git clone`, `git push`, `git fetch` — anything Git does. |
| **S3-compatible** | `s3.studio.internal:9000` | Direct blob upload / download, large-file transfer via Git LFS. |
| **REST** | `https://hub.studio.internal/api/v1` | Repository metadata, search, repo create / delete, member management. |

These are the in-cluster hostnames. Your admin's published a public alias for outside-cluster access.

## Authentication

All three surfaces use **Hub access tokens** — distinct from model API keys.

Create one: Settings → **Hub access tokens** → **+ New token**.  Pick a scope (read-only or read-write) and an expiry. The token is shown once; copy it before closing the dialog.

Pass the token by surface:

- **Git** — as the password in `git clone https://<token>@git.studio.internal:3000/...`. Or configure a credential helper to inject it automatically.
- **S3** — as the AWS-style access key + secret pair the Hub returns when you create an S3-style credential.
- **REST** — as `Authorization: Bearer <token>`.

## Git

The Git endpoint speaks plain Git, so every Git client works.

### Clone

```bash
git clone https://<token>@git.studio.internal:3000/<owner>/<repo>.git
```

The `<owner>` is your username, your team slug, or the project slug. The `<repo>` is the slug you set when the repo was created in **Distribute → Data Hub**.

### Push

Standard Git push:

```bash
cd path/to/local-clone
git add .
git commit -m "Add evaluation results"
git push origin main
```

Pushes are gated by the access token's scope: read-only tokens get a `403`. Pushes to a repo you don't have write rights to also get a `403`.

### Branches and tags

Standard Git semantics:

```bash
git checkout -b experiments/lora-r64
git push origin experiments/lora-r64
git tag -a v1.0 -m "Release v1.0"
git push origin v1.0
```

The branch name shows up in the Hub UI's branch dropdown, and the tag is searchable from the Tags tab.

### Git LFS

Large binary files (model weights, dataset shards) belong in LFS. The Hub has LFS enabled by default with a 10TB quota per organisation.

Initialise LFS in a new clone:

```bash
git lfs install
git lfs track "*.safetensors" "*.bin" "*.parquet"
git add .gitattributes
```

Then `git add` and `git push` work normally; LFS handles the blob upload to `s3.studio.internal:9000` behind the scenes.

## REST

The REST surface is JSON over HTTPS. Every endpoint requires `Authorization: Bearer <token>`.

### List repos

```http
GET /api/v1/repos?kind=model&page=1&page_size=50
```

Filters: `kind` (one of `model`, `dataset`, `skill`, `experiment`, `environment`), `owner`, `tag`, `search`.

Response:

```json
{
  "data": [
    {
      "id": "your-team/support-expert-v1",
      "kind": "model",
      "owner": "your-team",
      "name": "support-expert-v1",
      "created_at": "2026-05-01T12:34:56Z",
      "tags": ["sft", "8b", "support"],
      "default_branch": "main"
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 1
}
```

### Get a repo

```http
GET /api/v1/repos/{owner}/{name}
```

Returns the full repo record plus a `files` summary (paths, sizes, LFS flags).

### Create a repo

```http
POST /api/v1/repos
Content-Type: application/json

{
  "owner": "your-team",
  "name": "support-expert-v2",
  "kind": "model",
  "description": "v2 of the support expert, trained on 90-day session capture",
  "tags": ["sft", "8b", "support"]
}
```

Returns the new repo record. Equivalent to clicking **+ New Repository** in **Distribute → Data Hub**.

### Delete a repo

```http
DELETE /api/v1/repos/{owner}/{name}
```

Requires read-write scope on the repo and a confirmation header to prevent accidents:

```http
X-Confirm-Delete: yes
```

:::danger Repo delete is irreversible
The repo's branches, tags, files, and LFS objects are purged. Any model or dataset deploying from this repo starts failing immediately. There's no undo.
:::

### Import an external repo

```http
POST /api/v1/repos/{owner}/{name}/import
Content-Type: application/json

{
  "provider": "huggingface",
  "source_id": "meta-llama/Llama-3.1-8B-Instruct",
  "branch": "main",
  "subpath": "",
  "token": "hf_..."
}
```

Equivalent to the **Import** dialog in the Hub UI. The `token` is only required for gated repos.

## S3

The S3 surface is for direct blob transfer. Use it when:

- You're uploading from a pipeline (Airflow, GitHub Actions) that already speaks S3.
- You want to stream a large dataset out without going through Git LFS.

Endpoint: `https://s3.studio.internal:9000`. Path-style addressing (the bucket is part of the path, not the hostname).

```bash
aws s3 ls --endpoint-url https://s3.studio.internal:9000 s3://your-team/

aws s3 cp ./shard-00001.parquet \
  s3://your-team/datasets/sessions-2026-05/shard-00001.parquet \
  --endpoint-url https://s3.studio.internal:9000
```

Credentials are an access key + secret pair created from the Hub access tokens panel. Standard S3 auth headers apply.

## Quotas and limits

| Resource | Default | Notes |
|---|---|---|
| LFS storage per org | 10 TB | Configurable per install.  |
| File size (Git, non-LFS) | 100 MB | Larger files must use LFS or S3. |
| Repos per org | unlimited | Practical limit set by storage. |
| REST request rate | 600 / min per token | See [Errors and rate limits](./errors-and-rate-limits.md). |

## When something fails

- **`401 unauthorized` on Git push.** Token expired, or token has read-only scope. Create a new read-write token.
- **`403 forbidden`** — you don't have rights on this repo. Get the owner to add you as a member.
- **`413 payload too large` on Git push.** A non-LFS file exceeds 100 MB. Convert to LFS-tracked or move to S3.
- **LFS upload hangs.** S3 endpoint unreachable from your network. Check firewall / VPN; the LFS protocol POSTs to `s3.studio.internal:9000` after the initial HTTPS handshake to the Git server.

## Where to go next

- **[API overview](./overview.md)** — base URL, auth, request shape.
- **[Inference API](./inference.md)** — for calling models and agents.
- **[Data Hub](../features/hub.mdx)** — the UI side of repositories.
- **[Data Hub config (admin)](../admin/data-hub-config.md)** — quotas, endpoints, LFS enable state.

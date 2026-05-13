---
title: Data Hub configuration
sidebar_position: 4
slug: /admin/data-hub-config
description: Hub endpoints, storage quotas, Git LFS, member management. The admin side of the Data Hub.
---

# Data Hub configuration

The [Data Hub](../features/hub.mdx) is Surogate Ops' artifact registry. Day-to-day it's a HuggingFace-shaped UI for builders; admin's job is to keep its endpoints reachable, its storage healthy, and its membership clean.

This page is the admin side. For the builder workflow, see [Data Hub](../features/hub.mdx).

## Architecture

Three services back the Hub:

| Service | Endpoint | Protocol | Use it for |
|---|---|---|---|
| **Git server** | `git.studio.internal:3000` | Git over HTTPS | Repository clones, pushes, branch / tag operations. |
| **S3-compatible** | `s3.studio.internal:9000` | S3 | Blob storage for Git LFS, direct uploads. |
| **API server** | `https://hub.studio.internal/api/v1` | REST | Metadata, repo create / delete, member management. |

These are the in-cluster names. Your published public aliases (the names outside-cluster services use) are configured at install time and visible under Settings → Data Hub.

The three services share a common identity model with the rest of Surogate Ops. A user authorised on Surogate is authorised on the Hub by the same token; you don't manage Hub users separately.

## Storage and quotas

| Resource | Default | Configurable |
|---|---|---|
| LFS storage per organisation | 10 TB | Yes, via Settings → Data Hub → Quotas.  |
| Maximum file size (non-LFS) | 100 MB | No. Larger files must use LFS or S3 direct. |
| Maximum file size (LFS) | bounded by S3 endpoint capacity | n/a |
| Maximum repos per org | unlimited | Practical limit set by storage. |

Quotas are enforced at write time. A push that would put the org over quota is rejected with `413 quota_exhausted`; existing repos remain readable.

## Git LFS

LFS is on by default. Builders enable LFS in their clone with the standard `git lfs install` and `git lfs track` flow; the platform handles the blob upload to `s3.studio.internal:9000` transparently.

Admin controls:

- **Enable / disable LFS install-wide.** Settings → Data Hub → Git LFS.

:::danger Disabling LFS is destructive
Disabling LFS on a running install breaks every existing LFS pointer — model weights, dataset shards, anything tracked through LFS. Cloned repos start returning empty files. Don't do this without a migration plan that moves the existing LFS objects somewhere reachable.
:::
- **Per-org quota** — the 10 TB default is set per organisation.
- **Per-repo storage view** — the repo's detail in the Hub UI shows total bytes used, LFS vs non-LFS.

## Members and access

Each Hub repo has its own member list. Three roles, the same as project roles elsewhere in Surogate Ops:

- **owner** — full rights, including delete.
- **editor** — push and edit; can't change membership.
- **viewer** — read-only.

A repo can have:

- **Direct members** — individual users.
- **Team members** — added via a team; every team member inherits the role.
- **Public** — readable by every signed-in Surogate user (the default for repos in the platform-scoped namespace). Off for org and user-namespaced repos.

Membership applies to all three Hub surfaces — Git, S3, REST — uniformly.

## Endpoints exposed to your network

For admins running Surogate Ops on their own cluster, the three Hub services need to be reachable from:

- **Inside the cluster** — by every Surogate Ops service that produces or consumes artifacts (Training Runs publish here; Models pull from here; Datasets push here). The default in-cluster names handle this automatically.
- **From your CI / CD pipelines** — usually outside the cluster. Publish a public alias for `hub.studio.internal/api/v1` and `git.studio.internal:3000`; restrict by IP or by Hub access token scope.
- **From developer laptops** — the same publishing strategy as CI. Most teams add the public aliases to their developer onboarding doc.

`s3.studio.internal:9000` is more bandwidth-sensitive than the other two. If your developers are pulling tens of GB of weights, route them through a CDN or restrict by VPN.

## Hub access tokens

Tokens are scoped to a user (or a team service account) plus a read or read-write right. Created from Settings → **Hub access tokens** → **+ New token**.

Two practical rules:

1. **Service accounts should have their own tokens.** Don't share an individual developer's token with a CI pipeline; create a service-account user, give it the project memberships it needs, give it its own token. When the developer leaves, the CI keeps working.
2. **Tokens with no expiry should rotate on a cadence.** The Vault's rotation reminders apply here too — most teams rotate every 90 days for production tokens, 30 days for CI tokens that touch production.

The audit log records `hub.token_created`, `hub.token_used` (high-volume, useful for spot-checks), and `hub.token_revoked`.

## Repository kinds

Five repository kinds the Hub knows about:

| Kind | Used by | Schema |
|---|---|---|
| **Model** | Models page (deploy via Local Hub source); Training Runs (publish here) | Model weights + `config.json` + tokenizer + a model card |
| **Dataset** | Datasets page (push from); Training Runs (read from) | Examples in `.jsonl`, `.csv`, or `.parquet` + a dataset card |
| **Skill** | Skills page (publish from) | Skill bundle: markdown + dependencies |
| **Experiment** | Training Runs (full state) | Weights + config + metrics + lineage |
| **Environment** | RL training | Environment definition; bound to environment-kind Datasets |

Admin controls aren't kind-specific — every repo is governed the same way regardless of kind. The kinds drive the Hub UI's filter pills and the Surogate Ops integrations that consume them.

## Importing external repos

Builders import from HuggingFace and ModelScope through the Hub UI. Admin-relevant points:

- **External tokens** belong in the Vault, not pasted into the import dialog. The dialog accepts a Vault reference; create a `huggingface_team_token` Vault entry once and point every import at it.
- **Imported repos count against your LFS quota.** A 70B model is ~140 GB. Plan accordingly.
- **Mirror policy** — by default, imports are one-shot snapshots. Set up a scheduled re-sync if you depend on upstream updates flowing through.

## Backups and disaster recovery

The Hub's three services back onto S3-compatible storage; backup is on whoever runs the underlying object store.

- **Daily snapshots** of the Git server's metadata DB are the minimum bar.
- **Object-store replication** of `s3.studio.internal:9000` to a separate region is the bar for installs running production-critical artifacts.
- **Restore drills** — periodically restore a snapshot into a staging instance and confirm a Hub repo from the snapshot is intact.

For Surogate Ops cloud customers, the platform team owns this. For self-hosted installs, you do. See [Self-host / deployment](../deployment/self-host.md) for the operational detail.

## When this isn't worth doing

A small install with a few users and a few repos can leave most of this at defaults. The Vault-managed external tokens, the explicit rotation cadence, the published public aliases — these pay off when you have an actual ops team or actual compliance requirements. Until then, the defaults are sane.

## When something fails

- **Push returns 413 with `quota_exhausted`.** Your org has hit the LFS quota. Either purge old artifacts (the LFS storage view per repo shows the biggest consumers) or raise the quota in Settings.
- **Git clone hangs at the LFS step.** The S3 endpoint is unreachable. Verify the developer can reach `s3.studio.internal:9000`; almost always a VPN or firewall issue.
- **REST returns 401 with a token that worked yesterday.** Token rotated, revoked, or expired. Check Settings → Hub access tokens.
- **A repo's member list shows users that left the team.** The user wasn't removed from the project when they were deprovisioned. Project → Members → remove. The audit log shows who added them.
- **Imports from HuggingFace started returning 403 across the board.** Your HF token in the Vault expired. Rotate it; existing imports remain.

## Where to go next

- **[Admin overview](./overview.md)** — the wider admin surface.
- **[Data Hub](../features/hub.mdx)** — the builder side.
- **[Hub API](../api/hub.md)** — Git / S3 / REST endpoints in detail.
- **[Credential Vault](./credential-vault.md)** — where Hub-relevant external tokens live.

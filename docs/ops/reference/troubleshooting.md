---
title: Troubleshooting & FAQ
sidebar_position: 3
slug: /reference/troubleshooting
description: Cross-cutting failure modes and frequently-asked questions, with deep links into the relevant feature pages.
---

# Troubleshooting & FAQ

When something goes wrong, this page is the index. It groups the most common cross-cutting issues by surface, then deep-links into the relevant feature page for the full debugging steps.

For surface-specific failures, every feature page has its own **"When something fails"** section.

## Sign-in and accounts

### *I can't sign in — wrong password*

Use the **Forgot password** link on the sign-in form. The reset email arrives within a minute or two.

### *I invited a teammate; they never got the email*

Most often spam. The invite is from `noreply@surogate.ai`.  If it's not there, **Settings → Users → Resend invite**; that re-issues the email and invalidates the previous link. Reference: [Teams and roles → Invite a user](../admin/teams-and-roles.md#invite-a-user).

### *My account is on a temporary password*

Complete the password-change flow when you next sign in. Until you do, the API treats your account as restricted and returns `403 password_change_required` on protected calls.

## Agents

### *An agent is stuck in Deploying*

Either the compute scheduler can't find a GPU, or the serving container is taking longer than usual to come up.

1. **Compute → Workload Queue → filter to `serving` → find the workload for this agent.**
2. Read the row's status and logs.
3. The usual fixes: pick a different GPU offer, broaden the backend's region set, free up an in-flight workload that's blocking capacity.

Reference: [Agents → When it goes wrong](../features/agents.mdx).

### *An agent transitions from Running to Error*

The underlying Model is in **Stopped** or **Error** — fix the model first, then redeploy the agent.

Reference: [Models](../features/models.mdx).

### *Every chat returns an error but the agent is Running*

A required skill failed to initialize. Open the agent's **Settings**, untick the failing skill, redeploy. Then debug the skill separately.

## Models

### *Model stuck in Deploying*

Open **Compute → Workload Queue → filter `serving`** → find the row, read the logs. Most often a model-image build issue or capacity issue.

### *API key returns 401 invalid_scope*

The key was created against a different model. Each model has its own scoped keys. Create a new key on the right model.

### *Quantization choice rejected*

The chosen GPU doesn't support that quantization. Pick a different GPU or a different quantization. See [Models → Quantization](../features/models.mdx#quantization).

## Compute and backends

### *Connected backend has no offers*

1. **Quota.** The most common cause on hyperscalers — GPU quotas start at zero. Open the cloud provider's quota console and request a non-zero quota in the regions you care about.
2. **Region.** Surogate queries a default region set. Broaden under the backend's settings.
3. **IAM / role scope.** The credential's role lacks `DescribeInstanceTypes` (AWS) or the equivalent. See the per-backend page.

Per-backend references: [AWS](../compute-providers/aws.md), [Azure](../compute-providers/azure.md), [GCP](../compute-providers/gcp.md), [RunPod](../compute-providers/runpod.md), [Modal](../compute-providers/modal.md), [Nebius](../compute-providers/nebius.md), [OCI](../compute-providers/oci.md), [Vast.ai](../compute-providers/vast-ai.md).

### *Workload stays Queued forever*

No backend has capacity for the requested GPU. Loosen the GPU requirement, broaden the region set, or connect a backend with stock.

### *Workload provisions but the container immediately crashes*

GPU driver / CUDA / image mismatch. Open the workload's logs to read the failure; pick a different GPU type or update the image.

## Knowledge Bases

### *KB stuck in Compiling*

For a small site, expect a few minutes; for an enterprise wiki, an hour or more. If it's still **Compiling** after a day, the source fetch is probably timing out — check the KB's detail for per-source errors.

### *Agent retrieval returns empty results*

The KB is attached but not yet **Active**. Wait for the compile to finish. If it's already Active and still empty, your source content doesn't cover the query — add the missing documents and re-compile.

### *KB in Error state*

Open the KB; the per-source error messages are visible on its detail page. Most often a source credential expired (Confluence, Notion, etc.) — re-enter the credential.

## Training

### *Training run stuck in Provisioning*

No GPU available in the chosen backend / region. Loosen the GPU requirement or connect a different backend.

### *Loss diverges or oscillates*

Most often a too-large learning rate. Cancel, lower the learning rate by 2-4×, and re-run. Reference: [Training Runs → When something fails](../features/training.mdx).

### *Multi-node run hangs*

One node failed to provision; the run waits for the full group. Cancel and resubmit.

## Evaluations

### *Two runs of the same config give very different scores*

Likely seed variance. Increase the sample count if your custom benchmark is small, or re-run twice and average. The platform doesn't compute significance — you have to.

### *Run completes but every row is an error*

The model returned an unexpected output shape (empty strings, refusals, server errors). Open the **Samples** tab and read a few rows; the verdict column shows the underlying error.

## Arenas

### *Arena suddenly in POLICY PAUSED*

A budget cap was crossed without an approval. Open **Pending Approvals**, decide to extend the cap or terminate.

:::warning POLICY PAUSED is a hard gate
No participant runs and no compute is reserved while paused. Resolve through Pending Approvals; ignoring it leaves the arena waiting indefinitely.
:::

### *Coordinator looping on the same steering action*

Either the participant isn't acknowledging mandatory steering, or the Coordinator's logic is stuck. Pause, switch to **advisory** steering, resume.

## Sessions

### *Session shows status Active but no recent messages*

The user closed the chat but the session resource hasn't expired. Filter to **Active**; if the trace stops mid-conversation, that's a session abandoned mid-flow rather than a failure.

### *Flagged sessions aren't showing up in the dataset*

The dataset's quality filter is excluding them. Confirm the **From Conversations** filter matches the flag state (👍 only, 👎 only, all-flagged).

## API

### *401 invalid_scope*

The token is valid but doesn't grant access to the requested model or agent. Create a new key on the right resource.

### *429 rate_limited*

Back off and retry after the `retry_after_seconds` from the error body, or respect the `Retry-After` header. See [Errors and rate limits → Rate limits](../api/errors-and-rate-limits.md#rate-limits).

### *Wrong API key keeps failing even after I fixed it*

Failed authentications are negative-cached for about a minute. Wait it out.

## Hub

### *git clone hangs at the LFS step*

The S3 endpoint (`s3.studio.internal:9000`) is unreachable from your network. Almost always a VPN or firewall issue.

### *git push returns 413 payload_too_large*

A non-LFS file exceeds 100 MB. Switch to LFS-tracked, or push the artifact via S3 directly.

### *Hub LFS storage at 80%*

The platform alerts at this threshold. Either purge old artifacts from the largest-consuming repos, or raise the org's quota in **Settings → Data Hub → Quotas**.

## Build / deploy

### *Production build fails with broken-anchor warning*

Pre-existing trainer-docs anchor in `/guides/rl-environments`. Not blocking; build still succeeds.

### *Docusaurus dev server doesn't pick up new pages*

Stop the server, delete `.docusaurus/`, restart. The cache occasionally lags on big file moves.

## Where to go next

- **[Error messages](./errors.md)** — UI-side error messages catalog.
- **[Permissions matrix](./permissions-matrix.md)** — who can do what.
- **[API → Errors and rate limits](../api/errors-and-rate-limits.md)** — API-side errors.
- **[Glossary](../glossary.md)** — for terminology.

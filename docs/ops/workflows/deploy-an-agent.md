---
title: Deploy an agent
sidebar_position: 2
slug: /workflows/deploy-an-agent
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Deploy an agent

The builder path from an empty `/studio/agents` to a Running agent. End users see the result on `/work` as soon as the agent is healthy.

<video controls width="720" muted>
  <source src="/videos/04-deploy-agent-dialog.webm" type="video/webm" />
</video>

## Prerequisites

- A deployed [Model](../features/models) in **Serving** state, or a proxied Model wired to a [Credential](../admin/integrations).
- Project role `editor` or `owner` (TODO(verify)).
- Optional: at least one [Skill](../features/skills) and one **Active** [Knowledge Base](../features/knowledge-bases) you want the agent to use.

## Steps

1. Switch to **Develop** mode and open **/studio/agents**.
2. Click **Deploy Agent** (top-right of the page).
3. The dialog opens with the following sections, in order. Watch the video above for the full walkthrough.

### Section 1 — Identity

- **Name** (required) — becomes the display label across `/work`, `/studio/agents`, Sessions, and Monitoring. Choose something users will recognize.
- **Description** (optional) — shown on the agent card.

### Section 2 — Brain

- **Model** (required) — dropdown of Models in your project. Models in **Error** or **Stopped** are listed but cannot be selected (TODO(verify)).
- **System prompt** — defines the agent's persona and task. Some templates pre-fill it; otherwise write your own.

### Section 3 — Tools

- **Skills** — multi-select of [Skills](../features/skills). The agent pins to the version that exists at deploy time.
- **MCP servers** — multi-select of configured MCP servers.

### Section 4 — Memory

- **Knowledge bases** — multi-select. A KB in **Compiling** or **Error** status can be attached but won't return retrieval until it reaches **Active**.

### Section 5 — Surface

- **Greeting** (optional) — the first message shown to end users in chat.
- **Channels** — per-channel configs (web chat, API). TODO(verify the channel list).

### Submit

Click the final **Deploy** button. The dialog closes and the new agent shows up under the **Deploying** filter on `/studio/agents`. After 30–120 seconds it transitions to **Running**.

## Verifying it works

1. Open the agent at `/studio/agents/<id>` (TODO(verify the detail route)). The Overview tab shows recent activity.
2. Switch to **Work** mode. The agent appears in `/work`.
3. Click into chat and send a test message.
4. Confirm the conversation is logged at `/studio/sessions?agentId=<id>`.

## If it fails

| Symptom | Likely cause | Fix |
|---|---|---|
| Stuck in **Deploying** beyond 10 minutes | Compute scheduler can't find a GPU matching the Model's request | Check `/studio/compute/workload-queue?filter=serving` for the related job; it'll be **Queued** with a reason. |
| Transitions to **Error** | The Model is in **Stopped** or **Error** | Re-deploy the Model first, then the Agent. |
| Runs but every chat returns an error | A required Skill failed to initialize | Open the agent's settings, untick the failing skill, re-deploy. |

## After deployment

- Adjust the agent in place from `/studio/agents/<id>` → Settings. Saves create a new agent version; running sessions keep the old version until the user starts a new one.
- Add `sk-agent-*` API key access on the underlying Model — see [Models → API keys](../features/models#api-keys).
- Configure alerts in [Notifications](../admin/notifications) so the right team is paged on errors.

## Related

- [Agents](../features/agents)
- [Models](../features/models)
- [Skills & Tools](../features/skills)
- [Knowledge Bases](../features/knowledge-bases)
- [Monitoring](../features/monitoring)

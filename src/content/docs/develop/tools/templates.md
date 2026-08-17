---
title: Templates
---

The **Templates** page is a Work-mode surface (`ops.surogate.ai/work/templates`). In Develop mode the equivalent is the **DEPLOY AGENT** button on the Agents page — same dialog, same fields. Develop mode has no separate templates page.

In current builds the template catalog is nearly empty — there's a single **New Agent** card (a passthrough to the "start from scratch" path) plus an AI-driven *describe what you need* flow that's still disabled. The recommended creation path is:

1. **Templates** (Work mode) → **Start from scratch** **or** the **New Agent** card → **DEPLOY NEW AGENT** dialog, **or**
2. **Agents** (Develop mode) → **DEPLOY AGENT** button → same dialog.

## The deploy dialog

| Field | Notes |
|---|---|
| **Display Name** | Human-readable name (e.g. `Acme support bot`) |
| **Slug** | Auto-derived from the display name. Used in URLs (`<slug>.cloud.surogate.ai`). Unique within the project. |
| **Description** | Short summary. Seeds the agent's persona block on the Configure page. |
| **Model** | Defaults to `Surogate`. Switch later from Configure. |

Click **CREATE AGENT**. Status moves `deploying` → `running` in 10-90 seconds. Once running, switch to the agent's Configure page to attach skills, knowledge bases and MCP servers, and its Publish page for channels.

## Why the catalog is empty

Every workspace is different — what's a sensible default for one tenant is misleading for another. Rather than ship a fixed catalog of canned agents that drift out of date, the platform gives you an empty slate and lets the **Configure** page guide you through the same attachments you'd get from a template (Skills → Knowledge Bases → MCP Servers), with channels and end-users on **Publish**.

If you find yourself deploying the same shape repeatedly, clone an existing agent's config via the REST API rather than retyping the form.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/v1/agents` | Create an agent (same effect as the dialog) |
| `GET` | `/v1/agents/{id}` | Read a full config to clone from |
| `PATCH` | `/v1/agents/{id}` | Apply a config dict produced from a cloned source |

## What's next

[Build phase](/develop/loop/build/) for the post-create workflow. [Use cases](/develop/use-cases/) for end-to-end recipes.

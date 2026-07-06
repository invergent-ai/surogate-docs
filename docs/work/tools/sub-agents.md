---
title: Sub-agents
sidebar_position: 6
---

# Sub-agents

The **Sub-agents** page is a catalog of the specialized helper agents your agent can delegate to — each a preset bundle of system prompt, tool filter, model, and iteration cap.

Open it from an agent's left navigation (**Sub-agents**) or go to `/work/agents/<agentId>/sub-agents`.

## What a sub-agent is

A sub-agent is a named definition (an `AGENT.md` file: YAML frontmatter plus a system prompt) that a coordinator session spawns as a child with `agent_type=<name>`, applying that bundle. It lets a running agent hand a focused task — code review, research, and so on — to a purpose-built persona with its own tool permissions and model.

Sub-agents managed here are **project-wide**: shared by every agent in the project, every operator, and every session. The page shows this warning in orange near the top.

## Layout

The page is a master-detail view:

- **Left list** — sub-agents grouped by source, with a search box and a **New** button.
- **Right pane** — the full definition of the selected sub-agent, or an empty-state prompt to pick one.

### Sources

Sub-agents are grouped by where they come from:

| Group | Label | Editable |
|---|---|---|
| `user` | **My sub-agents** | Yes |
| `org` | **Organization** | Yes |
| `platform` | **Built-in** | No — read-only |

Built-in (platform) sub-agents live on the runtime filesystem and can't be edited or deleted here. Organization and user sub-agents can.

## The detail view

Selecting a sub-agent shows:

- **Header** — name, a "disabled" badge if it's off, and a description. For editable sub-agents, **Edit** and a delete (trash) button appear.
- **Meta row** — Source, and Category / Tags when set.
- **Configuration** panel — Model, Max iterations, Policy profile, Allowed tools, and Disallowed tools, when set.
- **System prompt** — the rendered prompt body.

## Creating a sub-agent

1. Click **New** at the top of the list.
2. In the **New sub-agent** dialog, fill in:
   - **Name** — must match the `name` field in the frontmatter (e.g. `code-reviewer`).
   - **Category (optional)** — e.g. `review`, `research`.
   - **AGENT.md content** — the full definition. The dialog pre-fills a template with `name`, `description`, `tools`, `disallowed_tools`, `model`, and `max_iterations` frontmatter plus a system-prompt body.
3. Click **Create**. The new sub-agent is added project-wide and selected in the detail pane.

The frontmatter fields the definition understands include `name`, `description`, `tools`, `disallowed_tools`, `model`, `max_iterations`, `policy_profile`, `category`, `tags`, and `enabled`.

## Editing and deleting

- **Edit** (editable sub-agents only) opens a dialog with the reconstructed `AGENT.md`. Replace the full content and click **Save**. The `name` in the frontmatter must stay the same. Changes apply project-wide.
- The **delete** (trash) button asks for confirmation, then permanently removes the sub-agent for every agent in the project. Coordinators that reference the deleted `agent_type` will fail on spawn.

## Searching

The search box filters by name, description, category, and model. If nothing matches, the list shows "No sub-agents match your search."

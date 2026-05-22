---
title: Copilot (⌘+/)
sidebar_position: 2
---

# Copilot (⌘+/)

The Copilot is an AI agent that drives the platform itself. Press **⌘+/** (Mac) or **Ctrl+/** (Windows/Linux) anywhere in `ops.surogate.ai`.

For the operator's view, see [Work mode → Copilot](/work/tools/copilot). This chapter has the builder details: what it can call, how it's built, and how to extend it.

## The Copilot is a sub-agent

The Copilot itself is an `AGENT.md` file in the ops repo at `surogate_ops/system_agents/surogate-platform-copilot/AGENT.md`. The runtime hosts it like any other sub-agent. Key config:

```yaml
---
name: surogate-platform-copilot
description: Surogate platform copilot — answers questions about the user's AgentOps workspace.
model: ${BASE_LLM_DEFAULT_MODEL}
max_iterations: 8
mcp_servers:
  - name: surogate-ops-copilot
    transport: http
    url_env: SUROGATE_OPS_COPILOT_MCP_URL
    credential_env: SUROGATE_OPS_COPILOT_SERVICE_TOKEN
    tool_allowlist:
      # Read surface
      - list_agents, get_agent
      - list_datasets, get_dataset
      - list_models, get_model
      - get_current_project, list_my_projects
      - list_skills, get_skill
      - list_training_runs, get_training_run, list_experiments
      - search, recent_failures
      - list_resources, read_resource, list_prompts, get_prompt
      # Write surface (v1)
      - create_skill, update_skill, delete_skill
      - create_dataset, delete_dataset
      - create_knowledge_base, delete_knowledge_base
      - list_environments, create_environment
      - create_agent, start_agent, stop_agent, scale_agent, delete_agent
      - attach_skill_to_agent, detach_skill_from_agent
      - attach_mcp_server_to_agent, detach_mcp_server_from_agent
      - attach_kb_to_agent, detach_kb_from_agent
      - deploy_model, stop_serving
      - start_training, cancel_training
disallowed_tools:
  - browser_navigate, browser_get_state, browser_click, browser_type
  - browser_press_key, browser_scroll, browser_drag, browser_wait
  - browser_screenshot, browser_close
---

You are the Surogate platform copilot. Help the user understand the state of
their AgentOps workspace using the provided tools.

Behavioral rules:
- Prefer calling tools over guessing.
- Cite resources as in-app links: `[name](/studio/training?runId={id})`, ...
- If a tool returns `{ error }`, summarize what went wrong rather than retrying blindly.
- Don't fabricate resource IDs.

Confirmation rules:
- Before `start_training` or `deploy_model`: clarify (GPU spend warning)
- Before any `delete_*`: clarify and re-quote the resource id
- Before `scale_agent` with higher replicas: clarify with delta
- Before `start_agent` on an `error` agent: clarify (triggers re-deploy)
- For routine writes (create_skill, update_skill, etc.): proceed directly
```

## What this means in practice

- **The Copilot uses your tenant's default LLM** (`${BASE_LLM_DEFAULT_MODEL}` env var). If your admin hasn't provisioned the credentials, the Copilot returns 401 ("Invalid base LLM token") — that's why the Copilot 401 from the audit happens.
- **Browser tools are explicitly denied.** The Copilot is a read-only Q&A surface, not a research agent. If you want to scrape something, use a regular agent.
- **CLARIFY-before-destructive is enforced in the prompt**, not at the tool level. The LLM is *told* to use `clarify` before destructive ops. This is the safety pattern.
- **Write tools are conditionally enabled** via the allowlist. The full destructive surface is in the allowlist of current builds — meaning the Copilot can `delete_*` your resources if you ask.
- **`read_resource` and `list_resources` are allowlisted but not implemented** in `server/copilot/tools/` — this is the M3 bug from the audit. The Copilot tries to enumerate KBs via `read_resource` and fails. Workaround: ask in a way that doesn't require enumeration.

## The Copilot's tools

The Copilot's MCP server (`surogate-ops-copilot`, hosted at `server/copilot/mcp_app.py`) exposes 30+ tools. Grouped:

### Read tools (always enabled)

- `list_agents`, `get_agent`
- `list_datasets`, `get_dataset`
- `list_models`, `get_model`
- `list_skills`, `get_skill`
- `list_training_runs`, `get_training_run`
- `list_experiments`
- `get_current_project`, `list_my_projects`
- `search` — full-text across resources
- `recent_failures` — sessions with crash/denied/etc. flags
- `list_environments`, `list_resources`, `read_resource` (broken — see above)
- `list_prompts`, `get_prompt`

### Write tools (conditionally enabled per AGENT.md allowlist)

- `create_skill`, `update_skill`, `delete_skill`
- `create_dataset`, `delete_dataset`
- `create_knowledge_base`, `delete_knowledge_base`
- `create_environment`
- `create_agent`, `start_agent`, `stop_agent`, `scale_agent`, `delete_agent`
- `attach_skill_to_agent`, `detach_skill_from_agent`
- `attach_mcp_server_to_agent`, `detach_mcp_server_from_agent`
- `attach_kb_to_agent`, `detach_kb_from_agent`
- `deploy_model`, `stop_serving`
- `start_training`, `cancel_training`

## The full-page view

Click the Copilot button (not ⌘+/) for `/copilot`. Same agent, more screen real estate. The sidebar shows conversation history; click any past Copilot session to resume.

## Extending the Copilot

The Copilot's AGENT.md ships with the platform. To customise:

- **Add a new tool**: implement in `server/copilot/tools/<your_tool>.py`, register in `mcp_registration.py`, add to the AGENT.md allowlist.
- **Adjust confirmation rules**: edit the AGENT.md body. Confirmation logic is prompt-side, not tool-side.
- **Disable a write tool**: remove from the AGENT.md allowlist.
- **Change the default model**: set `BASE_LLM_DEFAULT_MODEL` env var.

Note: editing the AGENT.md requires platform-admin access (it's in the ops repo, not a tenant artifact).

## What's next

[Templates](./templates.md) for the prebuilt agent catalog.

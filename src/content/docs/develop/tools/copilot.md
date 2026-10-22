---
title: Copilot (⌘+/)
---

The Copilot drives the platform itself on your behalf. Press **⌘+/** (Mac) or **Ctrl+/** anywhere in `ops.surogate.ai`. For the operator's introduction, see [Work mode → Copilot](/work/tools/copilot).

This chapter covers what builders should know that operators don't need: where it slots into automation, what it can and can't do, and the safety pattern that wraps destructive operations.

## What the Copilot does for you

![The Surogate Copilot panel](../../../../assets/screenshots/work-copilot-panel.png)

It exposes the platform's tools as natural-language commands. Instead of clicking through CONFIG / KNOWLEDGE & TOOLS / channels, you describe what you want and the Copilot calls the corresponding tools. There are 116 of them, served by the ops MCP server `surogate-ops-copilot` at `/api/copilot/mcp`. The Copilot's agent definition allowlists exactly those tools, so anything not registered there is invisible to it. The areas, with the main tools in each:

| Area | Main tools |
|---|---|
| Agents | `list_agents`, `get_agent`, `create_agent`, `update_agent`, `set_agent_env_vars`, `start_agent`, `stop_agent`, `scale_agent`, `delete_agent`; `attach_` / `detach_` for skills, MCP servers and knowledge bases |
| Skills | `list_skills`, `get_skill`, `create_skill`, `update_skill`, `delete_skill`, `import_skill_from_workspace`, and the skill's files (`list_skill_files`, `read_skill_file`, `write_skill_file`, `delete_skill_file`) |
| Knowledge bases | `create_knowledge_base`, `delete_knowledge_base`, `create_kb_source`, `list_kb_sources`, `add_workspace_file_to_kb`, `compile_knowledge_base`, `get_kb_compile_status`, `list_kb_wiki_pages`, `read_kb_wiki_page` |
| MCP servers | `list_mcp_servers`, `register_mcp_server`, `update_mcp_server`, `delete_mcp_server`, `list_composio_toolkits` |
| Sub-agents | `list_sub_agents`, `get_sub_agent`, `create_sub_agent`, `update_sub_agent`, `delete_sub_agent` |
| Programs | `get_programs_overview`, journeys (`create_journey`, `add_journey_step`, `review_journey`, `simulate_journey`, `activate_journey`, `pause_journey`, `send_journey_test`, `get_journey_funnel`), WhatsApp templates and forms, escalations |
| People and team | `find_people`, `add_person`, `list_program_people`, `enroll_person`, `message_person`, `get_person_timeline`, `telegram_start_link`, `set_team_member`, `get_program_settings`, `update_program_settings`, Slack lookups |
| Monetize and landing page | `get_monetize`, `create_plan`, `update_plan`, `replace_plan`, `delete_plan`, `update_monetize_settings`, `get_landing_page`, `update_landing_page` |
| Inbox and insights | `list_inbox`, `update_inbox_item`, `get_agent_insights`, `get_user_reports`, `find_sessions` |
| Datasets | `list_datasets`, `get_dataset`, `create_dataset`, `delete_dataset`, `upload_dataset_from_workspace` |
| Models and training | `list_models`, `get_model`, `deploy_model`, `stop_serving`, `list_training_runs`, `get_training_run`, `list_experiments`, `start_training`, `cancel_training`, `list_environments`, `create_environment` |
| Workspace | `get_current_project`, `list_my_projects`, `search`, `recent_failures` |
| Documentation | `search_docs`, `read_doc`, `list_docs`, `read_guide` |

Besides those, it can use a few built-in tools: `ask_user_question`, `create_artifact` (for plans, documents and tables), `todo`, and the sandbox file and terminal tools (`read_file`, `write_file`, `patch`, `search_files`, `list_files`, `terminal`), which let it read documents you attach in chat. Its browser tools are switched off.

### Looking things up

`search_docs` ranks sections of the product documentation. Its top results carry the matching section's text, so most answers need no second call. `read_doc` reads a page or one section of it by path, and `list_docs` lists every page. The documentation is a bundled snapshot of the Work and Develop pages, so it can lag the live site. When you ask from a page, the runtime tells the Copilot which doc belongs to it.

`find_sessions` finds conversations by what was said in them, across the agents you can see. `search` looks across resources by name and ID in the current project, or in every project you are a member of.

### Build guides

For each kind of build the Copilot has a playbook: `build-agent`, `build-skill`, `build-knowledge-base`, `build-sub-agent`, `connect-mcp` and `build-program`. It opens the guide with `read_guide` before building, along with the checklists and templates the guide cites. The loop is interview, inspect, plan (as an artifact you approve), build in dependency order, read each piece back, summarise with links and a test script. Its instructions forbid creating or updating an agent's prompt before an interview and an approved plan.

## How it asks before acting

Two mechanisms apply.

**It asks in the chat.** The Copilot's instructions have it ask with `ask_user_question` before spend and risky changes: `start_training`, `deploy_model`, `compile_knowledge_base`, any `delete_*`, `scale_agent` to a higher count, `start_agent` on an `error` agent, `set_agent_env_vars`, `update_agent` on `policy` or `browser_enabled`, `register_mcp_server` with `stdio`, and overwriting a skill or sub-agent. This is an instruction to the model. The tools themselves do not check for it.

**The tool refuses without `confirmed=true`.** For actions that message people, start or stop what they receive, spend money or change who can do what, the tool takes a `confirmed` argument. Without it, the tool changes nothing and returns `needs_confirmation` with the action. The Copilot then asks you, quoting the action (and the exact text, for a message), and calls again with `confirmed=true` only after your yes. These tools are:

- `activate_journey`, `pause_journey`, `delete_journey`, `remove_journey_step`, `send_journey_test`, `create_whatsapp_template`
- `enroll_person`, `update_person_enrollment` (status changes), `manage_person_contacts` (add, confirm, remove), `message_person`
- `set_team_member`, `remove_team_member`, `update_program_settings` (team, senders, destinations)
- `create_plan`, `update_plan`, `replace_plan`, `delete_plan`, `update_monetize_settings` (when changing the mode)

An approved plan does not cover these. Each one needs its own yes.

## What the Copilot won't do

- **It has no browser tool.** By design it works from the platform's own tools, not the open web. It is not a research agent.
- **It has no tools for secrets, keys or workspace billing.** It guides you to the page instead: connecting channels that need credentials, creating or revoking API keys and webhook secrets, Stripe Connect onboarding, workspace billing and plan changes, and inviting members.
- **It does not decide governance approvals.** Those stay in the Inbox.
- **It can't make images or videos.**

## Programmatic equivalents

Every Copilot operation maps to a REST API endpoint. If you're building automation, prefer the API directly — the Copilot is for interactive use, not headless pipelines. See the API reference sections under each feature ([Agents](/develop/features/agents/), [Skills & Experts](/develop/features/skills-and-experts/), [Datasets](/develop/features/datasets/), etc.).

## Failure modes you'll see

**401 "Invalid base LLM token"** — the platform's default LLM credential isn't provisioned for your tenant. Admin-side fix.

**Copilot returned `{error: ...}` and gave up** — by design. It won't retry blindly on errors. Read the error, fix the underlying issue, re-ask.

## Keyboard shortcuts

- **⌘+/** / **Ctrl+/** — open the drawer
- **Esc** — close
- **Enter** — submit
- **Shift+Enter** — newline

The drawer's header has a history menu (clock icon) — switch between past Copilot conversations, rename them, or start a new chat. Each conversation is its own session and resumes where you left off.

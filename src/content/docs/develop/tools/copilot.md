---
title: Copilot (⌘+/)
---

The Copilot drives the platform itself on your behalf. Press **⌘+/** (Mac) or **Ctrl+/** anywhere in `ops.surogate.ai`. For the operator's introduction, see [Work mode → Copilot](/work/tools/copilot).

This chapter covers what builders should know that operators don't need: where it slots into automation, what it can and can't do, and the safety pattern that wraps destructive operations.

## What the Copilot does for you

![The Surogate Copilot panel](../../../../assets/screenshots/work-copilot-panel.png)

It exposes the platform's tools as natural-language commands. Instead of clicking through CONFIG / KNOWLEDGE & TOOLS / channels, you describe what you want and the Copilot calls the corresponding tools. There are over 100 of them (served by the ops MCP server at `/api/copilot/mcp`). The Copilot's agent definition lists exactly the tools below, and a tool not on that list is not shown to the model. The areas, with the main tools in each:

| Area | Main tools |
|---|---|
| Agents | `list_agents`, `get_agent`, `create_agent`, `update_agent`, `start_agent`, `stop_agent`, `delete_agent`, plus env vars and `attach_` / `detach_` for skills, MCP servers and knowledge bases |
| Skills | `list_skills`, `get_skill`, `create_skill`, `update_skill`, `delete_skill`, `import_skill_from_workspace`, plus tools for the skill's files |
| Knowledge bases | `list_knowledge_bases`, `create_knowledge_base`, `create_kb_source`, `add_workspace_file_to_kb`, `compile_knowledge_base`, `get_kb_compile_status`, `read_kb_wiki_page`, and others for sources, wiki pages and deletion |
| MCP servers | `list_mcp_servers`, `register_mcp_server`, `update_mcp_server`, `delete_mcp_server`, `list_composio_toolkits` |
| Sub-agents | `list_sub_agents`, `get_sub_agent`, `create_sub_agent`, `update_sub_agent`, `delete_sub_agent` |
| Programs | `get_programs_overview`, `create_journey`, `add_journey_step`, `simulate_journey`, `activate_journey`, `get_journey_funnel`, and others for journeys, WhatsApp templates and forms, escalations |
| People and team | `find_people`, `add_person`, `enroll_person`, `message_person`, `get_person_timeline`, `set_team_member`, and others for program settings, Telegram start links and Slack lookups |
| Monetize and landing page | `get_monetize`, `create_plan`, `update_plan`, `update_monetize_settings`, `get_landing_page`, `update_landing_page`, and others for replacing and deleting plans |
| Voice | `get_agent_voice`, `list_voice_calls`, `list_voice_options`, `set_agent_voice`, `release_agent_voice` |
| Inbox and insights | `list_inbox`, `update_inbox_item`, `get_agent_insights`, `get_user_reports`, `find_sessions` |
| Datasets | `list_datasets`, `get_dataset`, `read_dataset`, `delete_dataset`, `upload_dataset_from_workspace` |
| Models and training | `list_models`, `get_model`, `deploy_model`, `stop_serving`, `list_training_runs`, `get_training_run`, `get_training_metrics`, `list_experiments`, `start_training`, `start_saved_run`, `update_saved_run`, `cancel_training`, `delete_training_run`, `list_environments` |
| Compute | `list_compute`, `get_compute_costs` |
| Workspace | `get_current_project`, `list_my_projects`, `search`, `recent_failures` |
| Documentation | `search_docs`, `read_doc`, `list_docs`, `read_guide` |

Besides those, it can use a few built-in tools: `ask_user_question`, `create_artifact` (for plans, documents and tables), `todo`, and the sandbox file and terminal tools (`read_file`, `write_file`, `patch`, `search_files`, `list_files`, `terminal`), which let it read documents you attach in chat. Its browser tools are switched off.

### Looking things up

`search_docs` ranks sections of the product documentation. Its top results carry the matching section's text, so most answers need no second call. `read_doc` reads a page or one section of it by path, and `list_docs` lists every page. The documentation is a bundled snapshot of the Work and Develop pages, so it can lag the live site. When you ask from a Studio page that has a doc, the page tells the Copilot which doc covers it. Pages without one give no doc hint.

`find_sessions` finds conversations by what was said in them. With no agent named it searches the current project's agents; with an agent named, only that agent. Either way you need the editor or owner role on the project (or to be a platform admin); a viewer gets no results. `search` looks across resources in the current project, or in every project you are a member of. It matches the name Studio shows, the internal name and the ID, ignoring case, among the first 100 items of each kind; in a larger project, narrow it with `kinds`. Its results, like the agent, skill, dataset and model lists, include `display_name`. `list_skills` with `scope="mine"` lists only the skills you wrote, a full page at a time.

### Agents

`get_agent` returns the agent's settings with the skills, knowledge bases and MCP servers attached to it. Long fields such as the system prompt come back shortened; with `full=true` it returns them whole (environment variable values stay hidden either way), and `update_agent` refuses a value that still carries the shortening marker, so a cut-off prompt can't be saved back over the real one. `list_knowledge_bases` lists the project's knowledge bases, to find one to attach.

`attach_kb_to_agent` takes a `mode`: `grounding` (the default for a new attach: the agent answers from the knowledge base and cites it), `grounding_nocite` (the same authority, in plain prose without citations) or `reference` (optional material it consults when it judges useful). On a knowledge base that is already attached, a given mode changes it and leaving it out keeps it. `get_agent` shows each attached knowledge base with its mode.

`attach_skill_to_agent` attaches a skill's `main` unless you name a version. A named version must be one the skill has published; otherwise the tool refuses and lists the published versions it finds. If the Hub can't be read, it says so instead.

`start_agent`, `stop_agent` and `delete_agent` run the same checks and steps as the buttons in Studio and wait for the result. Start is refused at the plan's limit for running agents or workspace storage. If delete removes the agent but a clean-up step fails (its workspace files, session data, API keys or service account), the result names that step so the Copilot can tell you.

Agents can't be scaled: they run on the shared runtime with no replicas, CPU or memory to set, and `update_agent` refuses a `resources` field. Only model deployments have replicas.

### Skills and experts

`create_skill` makes a skill from a name, description and instructions (and `max_iterations`). An expert, the license, `requires_tools` and `fallback_for_tools` come from importing a skill folder with `import_skill_from_workspace`, which also reads `max_iterations`; the other fields are set in Studio. An imported expert has no model until one is chosen in Studio.

### Phone lines

The voice tools read and change an agent's phone line (see [Voice](/work/channels/voice/)) through the same checks as the Voice screen: reading needs the viewer role, changing needs the editor role, and the Copilot changes a system agent's line only for an administrator.

- `get_agent_voice` returns the agent's number (none when it has no line), its settings and the free numbers in the pool. `list_voice_calls` lists recent calls, and `list_voice_options` lists what a line can be set to: Surogate's speech models and languages, the default lines, and the background scenes and hold music.
- `set_agent_voice` gives the agent a free number and/or changes its settings. Only what you name changes; the rest is kept. Pronunciations are added word by word, and a word set to `null` is removed. With no line and no number named, it refuses and lists the free numbers rather than picking one; a number that is taken or retired is refused before you are asked anything.
- `release_agent_voice` returns the number to the pool and keeps the settings for next time.

The Copilot can't switch a line to another speech provider: that needs your account's key, so it sends you to the Voice screen. Surogate's own speech is Romanian only, so on a line that uses it the language stays Romanian. On a line already set to another provider in Studio, it can still change the other settings. Adding numbers to the pool is for administrators.

### Build guides

For each kind of build the Copilot has a playbook: `build-agent`, `build-skill`, `build-knowledge-base`, `build-sub-agent`, `connect-mcp`, `build-program`, `build-dataset`, `run-training` and `deploy-model`. It opens the guide with `read_guide` before building, along with the checklists and templates the guide cites. The loop is interview, inspect, plan (as an artifact you approve), build in dependency order, read each piece back, summarise with links and a test script. Its instructions forbid creating or updating an agent's prompt before an interview and an approved plan.

The three ML guides cover what the tools allow:

- `build-dataset` uploads one workspace file of up to 50 MB with `upload_dataset_from_workspace`, then shows you real rows and the stats with `read_dataset` (at most 20 rows, long values and lists cut).
- `run-training` reads the project's compute with `list_compute`, which says per compute what it can train on: the exact GPUs on Modal, live offers on a cloud, the fleet's own GPUs on SSH (see [Supported GPUs](/develop/features/training/#supported-gpus)), and starts SFT, DPO and distillation runs with `start_training`. A refused start leaves the run saved: the Copilot edits it with `update_saved_run` (settings, a GPU on its own compute, a Hugging Face subset; not a GRPO run) and starts it with `start_saved_run` instead of creating another. `get_training_metrics` samples a run's metrics evenly (over the latest 20,000 rows of a kind, which covers almost every run) and says whether it is still going.
- `deploy-model` starts and stops serving an entry already on Models and switches an agent onto it.

## How it asks before acting

Two mechanisms apply.

**It asks in the chat.** The Copilot's instructions have it ask with `ask_user_question` before spend and risky changes: `start_training`, `deploy_model`, `compile_knowledge_base`, any `delete_*`, `start_agent` on an `error` agent, `set_agent_env_vars`, `update_agent` on `policy` or `browser_enabled`, `register_mcp_server` with `stdio`, and overwriting a skill or sub-agent. This is an instruction to the model. The tools themselves do not check for it.

**An unanswered question is not an answer.** A cancelled `ask_user_question` (for example [when nobody answers](/develop/reference/tool-catalog/#when-nobody-answers)) is neither a yes nor a no, for an interview question, a plan approval or a confirmation alike, and the instructions forbid acting on it. If a message or step arrived meanwhile, the Copilot deals with that first and asks again only for what is still missing; otherwise it says in one line that it is waiting and stops, without asking again in that turn.

**The tool refuses without `confirmed=true`.** For actions that message people, start or stop what they receive, spend money or change who can do what, the tool takes a `confirmed` argument. Without it, the tool changes nothing and returns `needs_confirmation` with the action. The Copilot then asks you, quoting the action (and the exact text, for a message), and calls again with `confirmed=true` only after your yes. These tools are:

- `activate_journey`, `pause_journey`, `delete_journey`, `remove_journey_step`, `send_journey_test`, `create_whatsapp_template`
- `enroll_person`, `update_person_enrollment` (status changes), `manage_person_contacts` (add, confirm, remove), `message_person`
- `set_team_member`, `remove_team_member`, `update_program_settings` (team, senders, destinations)
- `create_plan`, `update_plan`, `replace_plan`, `delete_plan`, `update_monetize_settings` (when changing the mode)
- `start_saved_run`, `update_saved_run`, `delete_training_run`
- `set_agent_voice`, `release_agent_voice` (every change to a phone line, including a settings-only edit on a connected line)

The three training-run tools and the two voice tools go one step further: their `needs_confirmation` answer carries a code tied to you, the chat and what is about to happen, and they act only when called again with that code. For a run it covers the run's current state (and, for an edit, the exact change), so the code stops working once the run starts or changes. For a phone-line change it covers the number now, the number after and the settings as they will be stored; for a disconnect, the number being released. `confirmed=true` alone changes nothing, and a yes doesn't carry over to other values. So the Copilot always receives the tool's own wording (for a delete, that a Modal run's storage and unpublished weights go too); showing it to you is still up to its instructions.

An approved plan does not cover these. Each one needs its own yes.

## What the Copilot won't do

- **It has no browser tool.** By design it works from the platform's own tools, not the open web. It is not a research agent.
- **Its instructions have it guide you, not act, for secrets, keys and workspace billing.** It links the page and explains the steps: connecting channels that need credentials, creating or revoking API keys and webhook secrets, Stripe Connect onboarding, workspace billing and plan changes, and inviting members. This is an instruction, not a missing tool: `set_agent_env_vars` can write an agent's environment variables, which carry channel keys, and the Copilot is instructed to ask you first and never echo secret values back.
- **Some knowledge-base, template and skill work is Studio-only.** Knowledge-base settings, removing a source or file, and stopping or rebuilding a compile (`compile_knowledge_base` has no stop or rebuild); creating an agent from a template (it links [Templates](/work/workflow/templates/) or offers to build one with `/build-agent`, without the template's skills); publishing skill versions, the skill canvas, test runs and optimization. Its instructions have it say where in Studio each is done.
- **No number pool or other speech providers.** It can't add numbers to the pool or switch a phone line to another provider; it sends you to the [Voice](/work/channels/voice/) screen.
- **Models beyond starting, stopping and redeploying are Studio work.** `deploy_model` starts a model, and on one that is running or starting it stops it and starts it again. No tool adds, edits, scales or deletes a model, merges or promotes an adapter, or publishes a run to the Hub; the instructions have it say where in Studio each is done.
- **No Data Hub tools.** It can't browse or change repositories, branches, tags or files; it links [Data Hub](/develop/features/hub/) and explains from its doc.
- **No RL environments or new GRPO runs.** `start_training` refuses GRPO and PPO, `update_saved_run` won't edit a GRPO run's settings, and no tool on the Copilot's list creates an environment. A GRPO run already saved in Studio can still be started or deleted with `start_saved_run` and `delete_training_run`. It walks the user through the Training page's **Environments** tab and the new-run form, and can list the project's environments.
- **No evaluation tools.** It sends the user to [Evaluations](/develop/features/evaluations/) or the run page's **Evaluate** button.
- **It does not decide governance approvals.** Those stay in the Inbox.
- **It can't make images or videos.**

## Programmatic equivalents

Every Copilot operation maps to a REST API endpoint, except the docs and guide tools (`search_docs`, `read_doc`, `list_docs`, `read_guide`), which read the documentation and build guides bundled with the Copilot. If you're building automation, prefer the API directly: the Copilot is for interactive use, not headless pipelines. See the API reference sections under each feature ([Agents](/develop/features/agents/), [Skills & Experts](/develop/features/skills-and-experts/), [Datasets](/develop/features/datasets/), etc.).

## Failure modes you'll see

**401 "Invalid base LLM token"** — the platform's default LLM credential isn't provisioned for your tenant. Admin-side fix.

**Copilot returned `{error: ...}` and gave up** — by design. It won't retry blindly on errors. Read the error, fix the underlying issue, re-ask.

## Keyboard shortcuts

- **⌘+/** / **Ctrl+/** — open the drawer
- **Esc** — close
- **Enter** — submit
- **Shift+Enter** — newline

The drawer's header has a history menu (clock icon) — switch between past Copilot conversations, rename them, or start a new chat. Each conversation is its own session and resumes where you left off.

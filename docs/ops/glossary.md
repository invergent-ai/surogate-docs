---
title: Glossary
sidebar_position: 99
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Glossary

Terms used in the Surogate Ops UI, with their one-line meaning. Sorted alphabetically.

| Term | Meaning |
|---|---|
| **Active agent** | An agent currently deployed and healthy. Counter on the Studio Dashboard. |
| **Agent** | An autonomous workflow that combines an LLM, skills/tools, knowledge bases, and conversational state. Listed under `/studio/agents` and `/work`. |
| **API key** | An `sk-agent-<id>` token, scoped to a single Model, used to call the Surogate proxy. |
| **Arena** | A controlled multi-evaluation "tournament" comparing agents or models. Lives at `/studio/arenas`. |
| **Auth identity** | A user's link to a third-party identity provider (Google, GitHub, Firebase email). One user can have several. |
| **Backend (cloud)** | A cloud compute provider connected to your project: AWS, Azure, GCP, RunPod, Modal, Nebius, OCI, Vast.ai. |
| **Backend offer** | A specific GPU/instance type available from a connected backend, with price. |
| **Benchmark suite** | A grouped set of evaluation cases. A tab on `/studio/evaluations`. |
| **Cloud account** | A specific account/project inside a cloud Backend (e.g. a single AWS account, a single GCP project). |
| **Compute** | The Studio area for cloud compute, jobs, policies. Path: `/studio/compute`. |
| **Conversation** | A user-agent exchange thread. Used interchangeably with Session in the UI. |
| **Credential** | A stored secret used by agents, jobs, or integrations. Never displayed after creation. |
| **Data Hub** | The HuggingFace-compatible internal registry. Models, datasets, skills, experiments, environments live here. Path: `/studio/hub`. |
| **Dataset** | A collection of examples used to train, eval, or seed an agent / model. |
| **Default project** | The project a user's actions land in by default. Stored as `User.default_project_id`. |
| **Deploy** | Make an agent or model active and reachable. Each Deploy creates / updates a compute job. |
| **Develop perspective** | The Studio UI for builders. `UserPerspective = "develop"`. |
| **Eval run** | A single execution of an evaluation. Tab on `/studio/evaluations`. |
| **Evaluation** | A scored run of an agent/model against fixtures or a benchmark. |
| **Expert** | A specialized small model trained on captured agent interactions for a specific task. |
| **Find Templates** | The end-user CTA on the Work dashboard that opens the template browser. |
| **GRPO** | "Group Relative Policy Optimization" — an RL training method available in Training runs. |
| **Guardrail** | A monitoring filter category on `/studio/monitoring`. |
| **Hub repo** | A single repository inside the Data Hub. Type: Models, Datasets, Skills, Experiments, Environments. |
| **Integration** | A third-party service connected to your account (Hub, Firebase, cloud providers, etc.). |
| **Job** | A workload running on cloud compute. Types: `sft`, `grpo`, `serving`, `eval`, `task`, `synthetic`. |
| **Knowledge Base (KB)** | A document store agents read from. Has lifecycle states `Active`, `Compiling`, `Error`. |
| **Leaderboard** | Cross-eval rankings of models or agents. Tab on `/studio/evaluations`. |
| **MCP Server** | A Model Context Protocol server that exposes tools to agents. Shown alongside Skills. |
| **Model** | An LLM your agents can call. Either served by Surogate or proxied. |
| **Onboarding** | The 2-step welcome flow at `/onboarding`. |
| **Operate** | The Studio sidebar group for run-time concerns: Dashboard, Agents, Sessions, Compute. |
| **Perspective** | Which UI you see: `work` or `develop`. Saved on your User record. |
| **Playground** | An ad-hoc model testing surface at `/studio/playground`. |
| **Policy (compute)** | Rules governing how/where workloads run (provider, region, instance type, cost cap). |
| **Project** | A workspace that owns agents, models, KBs, datasets, etc. and has members with project roles. |
| **Project role** | `owner` (full control), `editor` (read + write), `viewer` (read-only). |
| **Quick Action** | A starter button on the Studio Dashboard (Deploy Agent, Serve Model, New Skill, Start Training, New KB, New Dataset). |
| **Quick Start** | An end-user one-click chip on the Work dashboard (Answer support questions, Summarize meetings, Onboard a new user). |
| **Refresh token** | A 7-day opaque token issued at login alongside the JWT access token. |
| **Repo** | A Hub repo. |
| **Run** (training) | A single training job. Has a `runId` you can deep-link to. |
| **Serve / Serving** | Lifecycle state for a deployed Model. |
| **Session** | A chat session with an agent. Has a `sessionId`. |
| **SFT** | Supervised Fine-Tuning. A workload kind under Compute → Workload Queue and a training kind. |
| **Skill** | A reusable function/tool agents can call. Built in the Skill Builder. |
| **Skill template** | A starter Skill scaffold. Live in `surogate_ops/core/skills/templates/`. |
| **Status** | A lifecycle state — see [Lifecycle states](./concepts/lifecycle). |
| **Studio** | The Develop-perspective surface at `/studio/*`. |
| **Synthetic run** | A synthetic data pipeline job. Workload kind: `synthetic`. |
| **System role** | A platform-wide role on a User: `admin`, `skill_author`, `devops`, `developer`. Multiple per user. |
| **Template** | A pre-built configuration — agent template, skill template, prompt template. |
| **Tool** | Either a Skill or an MCP Server. The UI groups them as "Skills & Tools". |
| **Training run** | See **Run**. |
| **Tour** | Just-exploring path from `/onboarding`. |
| **Trajectory** | The recorded path of an agent's actions during a Session. |
| **Username** | A user's permanent identifier. Cannot be changed after sign-up. |
| **Welcome** | Step 1 of the `/onboarding` flow. |
| **Work perspective** | The end-user UI at `/work/*`. |
| **Workload queue** | The list of running and queued compute jobs at `/studio/compute/workload-queue`. |

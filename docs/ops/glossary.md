---
title: Glossary
sidebar_position: 3
slug: /glossary
---

# Glossary

Terms used in Surogate Ops, alphabetical.

- **Agent** — a deployed conversational workflow pairing a Model with skills, MCP servers, and knowledge bases.
- **API key** — a key scoped to one Model, used by external callers to reach it through Surogate's API.
- **Arena** — a tournament across multiple evaluations.
- **Backend (cloud)** — a connected cloud provider account: AWS, Azure, GCP, RunPod, Modal, Nebius, OCI, Vast.ai.
- **Backend offer** — a specific GPU/instance type available on a backend, with price.
- **Compute Policy** — an allocation rule limiting where workloads may run.
- **Conversation** — a user-agent exchange thread; used interchangeably with Session.
- **Credential** — a stored secret. Never displayed after creation.
- **Data Hub** — Surogate's HuggingFace-compatible registry.
- **Dataset** — a collection of training, eval, or fine-tuning examples.
- **Develop perspective** — the Studio UI for builders.
- **Eval run** — one execution of an evaluation.
- **Evaluation** — a scored run of an agent / model against fixtures or a benchmark.
- **Expert** — a fine-tuned specialized model.
- **GRPO** — Group Relative Policy Optimization, an RL training kind.
- **Guardrail** — a content or compute-policy intervention.
- **Hub repo** — one repository inside the Data Hub. Kinds: Model, Dataset, Skill, Experiment, Environment.
- **Job (Workload)** — a scheduled unit of compute. Kinds: `sft`, `grpo`, `serving`, `eval`, `task`, `synthetic`.
- **Knowledge Base (KB)** — an indexed document store agents read from.
- **MCP Server** — a Model Context Protocol endpoint exposing tools.
- **Model** — an LLM the agents call; either served by Surogate Ops or proxied.
- **Onboarding** — the two-step welcome flow shown on first sign-in.
- **Perspective** — Work or Develop. Toggle in the top bar switches between them.
- **Playground** — an ad-hoc model testing surface.
- **Project role** — `owner` / `editor` / `viewer`, picked when an admin invites a member.
- **Quickstart** — the first-time setup walkthrough; see [Quickstart](./getting-started/quickstart.mdx).
- **Run** (training) — a single training job.
- **Session** — a chat session with an agent.
- **SFT** — Supervised Fine-Tuning.
- **Skill** — a reusable function/tool agents can call.
- **Skill Builder** — the inline editor for skills.
- **Skill template** — a starter skill scaffold from the Templates library.
- **Studio** — the Develop-perspective UI.
- **Synthetic run** — a generated-data pipeline; workload kind `synthetic`.
- **Tool** — either a Skill or an MCP Server; the UI calls them "Skills & Tools".
- **Vault** — secure store for MCP server credentials.
- **Work perspective** — the end-user UI.
- **Workload queue** — the live job table.

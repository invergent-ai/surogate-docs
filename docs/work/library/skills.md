---
title: Skills
sidebar_position: 1
---

# Skills

A **skill** is a small markdown file that tells the agent how to handle a specific kind of request. Think of skills as reusable mini-prompts that the agent loads when relevant.

> Builders write skills more deeply — frontmatter, conditional activation, the four-layer override model. You'll find that in [Develop mode → Skills & Experts](/develop/features/skills-and-experts). This chapter is the operator's view: how to find, attach, and improve skills.

## Where skills live

**Library → Skills & Tools → SKILLS tab.** Layout:

- **Left rail** — filter box, ADD SKILL / IMPORT SKILL / NEW SKILL buttons, then the list of every skill in your tenant (each row shows the icon, name, author, last-updated)
- **Right pane** — detail for the selected skill: name + version tag, USED BY count, EDIT / PUBLISH / DELETE, tags, and inner CONTENT / REPOSITORY tabs

Platform-default skills (`skill-creator`, `pdf`, `xlsx`, …) are pulled in at agent runtime but aren't surfaced in this list — it shows only the skills your tenant has published.

Each skill has:

- A **name** (`summary-bullets`, `code-style-reviewer`)
- A **description** (one line — what it does)
- **Triggers** — keywords that activate it ("summarize", "tldr", "condense")
- **Content** — the actual instructions the LLM follows
- A **version tag** if published (`v0.1.0`, `v0.2.0`, …)
- A small **IS EXPERT** flag if the skill is backed by a fine-tuned model

## Three ways to create one

| Button | When to use |
|---|---|
| **NEW SKILL** | Write a skill from scratch in the form |
| **IMPORT SKILL** | Drop in a `SKILL.md` file or a `.zip` archive (e.g. from [agentskills.io](https://agentskills.io)) |
| **ADD SKILL** | Pick from a curated template library *(currently empty in the live build)* |

For most operators: use NEW SKILL.

## Writing a useful skill

The minimum skill:

```markdown
---
name: tldr
description: Summarize text into one tweet-length sentence
trigger: tldr, tweet-length, one-sentence summary
---

When asked to give a tldr, produce exactly one sentence of 240
characters or fewer that captures the most important fact. No
preamble, no "Sure!" prefix, no quotation marks. Just the sentence.
```

That's a working skill. Drop it in NEW SKILL, click PUBLISH, attach to an agent, done.

### Rules of thumb

1. **Be specific about output, not vibes.** "Produce 3-5 bullets, each under 20 words" beats "be thorough."
2. **Show one example.** A concrete example saves a paragraph of prose. LLMs are much better at imitating than inferring.
3. **List forbidden behaviours explicitly.** "Never include the internal ticket ID" beats hoping the agent figures it out.
4. **Keep triggers precise.** `trigger: refund request, refund policy, customer wants money back` is better than `trigger: help, refund`. Loose triggers cause cross-contamination — the skill fires on unrelated messages.

### What NOT to put in a skill

- The agent's **identity** ("You are a friendly support agent…") — that's SOUL.md (see [Improve your agent](../workflow/improve-agent.md)).
- **Long lists of facts** — those are knowledge base material (see [Knowledge bases](./knowledge-bases.md)).
- **Workflow that touches many features** — that's a use case (see [Use cases](../use-cases.md)).

## Publishing — versioning your skill

Every skill is stored in a small git-like repo (lakeFS) under your project. When you click **PUBLISH** on a skill, you create a tag like `v0.1.0`. Why this matters:

- **Immutability**: once published, the tag doesn't change. Editing creates a new draft; you have to PUBLISH again to create `v0.1.1`.
- **Rollback**: if a new version regresses, you can re-attach the previous tag.
- **Audit**: sessions record which skill version they used.

The PUBLISH dialog asks for a tag (e.g. `v0.2.0`). Use semantic versioning if you want; nothing enforces a format.

## Attach to an agent

Open the agent → **Configure** in the left nav → the **Skills & Tools** tab → **+ ATTACH SKILLS** → pick the skill.

The agent hot-reloads on the next session. Existing in-progress sessions keep their old skill list.

To remove: click **DETACH** next to the skill row.

## When the agent isn't using your skill

A common frustration: you wrote and attached a skill, the agent should be using it, it isn't. Three things to check:

1. **Did you start a NEW session?** Skill changes don't apply to in-progress sessions.
2. **Are the triggers specific enough?** The LLM compares the user's message against the triggers. Vague triggers fire on everything; overly specific triggers fire on nothing.
3. **Does the skill need a tool the agent doesn't have?** If you set `requires_tools: [terminal]` in the frontmatter but the agent's CONFIG denied `terminal`, the skill is filtered out. Either add the tool or remove the requirement.

Open the session's **SKILLS tab** — it shows which skills loaded into context. If yours isn't there, the filter is hiding it.

## Expert skills

The **IS EXPERT** flag on a skill turns it into something more powerful — a skill backed by a **fine-tuned model**. When you mark a skill as expert, you need to specify:

- A **base model** (e.g. `qwen2.5-coder-7b`)
- An **endpoint** (an OpenAI-compatible URL — yours, OpenRouter, vLLM, etc.)
- A **status** (draft → collecting → active → retired)

When the base LLM hits a request matching an expert's triggers, it calls `consult_expert` — the expert runs its own mini-loop on its own model and returns an answer. The base LLM reviews and either accepts or modifies it.

For operators, the practical takeaway: experts cost money to train and host. They're worth it when:

- A specific task happens often (say >100 times a week)
- The default model gets the task wrong often enough to be a problem
- You have someone on the team who can fine-tune a model and stand up an endpoint

The full expert lifecycle (collect → train → activate → monitor) lives in **Develop mode** — see [Skills & Experts](/develop/features/skills-and-experts) there.

## DELETE a skill

Skill detail → DELETE. A pre-flight check warns you if any agent currently has it attached. If references exist, detach first or accept the broken state.

The DELETE confirmation modal has **CANCEL focused by default** — you have to deliberately click DELETE. Safe pattern.

## What's next

If you've never built a knowledge base, read [Knowledge bases](./knowledge-bases.md). If you want a worked end-to-end example, jump to [Use cases](../use-cases.md).

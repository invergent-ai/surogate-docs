---
title: Code-review companion
sidebar_position: 4
slug: /use-cases/code-review
description: GitHub-aware assistant that reads a PR, surfaces risk, suggests reviewers, and drafts release notes.
---

# Code-review companion

A GitHub-aware assistant that reads a pull request, surfaces risk, suggests reviewers based on file ownership, and drafts release notes from the diff. Sits beside your human reviewers; doesn't replace them.

The agent's output, posted as a regular PR comment, looks like:

> **🔍 Surogate review · PR #1284**
>
> **Risk** — *medium*. Touches `payments/charge.py` (CODEOWNERS: @billing-team). New `null`-able column added to a 50M-row table without a migration plan.
>
> **Suggested reviewers** — @alex-payments (last touched this file), @maria-data (owns the migrations runbook).
>
> **Drafted release note** — *Add idempotency key to charge endpoint; rejects duplicate retries within a 60-second window.*
>
> **Concerns**
> - `charge.py:312` — exception is swallowed silently. Consider re-raising or logging.
> - Missing test for the case where the idempotency key collides across users.

## What you need

- **A model.** A reasoning-strong model with a long context window — code-review prompts get long fast. An expert fine-tune on your codebase is a future upgrade, not a day-one requirement.
- **Skills:**
  - *get_pr* — fetch the diff, file list, and metadata from the GitHub API.
  - *find_owners* — CODEOWNERS lookup for changed files.
  - *post_review_comment* — drop the assistant's writeup back on the PR.
- **An MCP server** (optional): your CI's MCP integration, so the agent can read test results and link them.
- **One knowledge base** (optional): your engineering style guide, security policy, deprecation list. The agent grounds its critique against your standards, not generic advice.

## Set it up

1. **Connect GitHub.** From Settings, connect a GitHub credential with `repo` and `read:org` scopes.
2. **Write or import the GitHub skills.** Templates library has GitHub starters; *get_pr* and *post_review_comment* are usually one-clicks from there.
3. **(Optional) connect your CI's MCP.** Build → Skills & Tools → MCP Servers tab → **Add Server**.
4. **(Optional) build the style-guide KB.** Build → Knowledge Bases → **+ New Knowledge Base**, point at the repo path containing your engineering guidelines.
5. **Deploy the agent.** Attach the skills, the MCP server, and the KB. Redeploy.
6. **Wire the trigger.** A GitHub action on PR-opened calls your agent through Surogate's API with the PR id. The agent runs and posts back to the PR.

## Try it

Open a draft PR with intentional issues — a hardcoded secret, an `any` cast, a missing test. The agent's review comment should call them out and link the relevant rule from your KB.

## Iterate

Two failure modes show up early:

- **Nitpicks.** The agent flags style issues your team doesn't care about. Tighten the style-guide KB to remove those rules.
- **Misses.** The agent missed a real bug. Add the missed pattern to the KB ("when you see X, raise Y"); the agent picks it up on the next compile.

Once you have a few hundred PR reviews of varying quality, the captured-conversations dataset trains an expert that knows what your team actually cares about. That's where this case becomes ten-times cheaper to run than a frontier model on every PR.

## Where to go next

- **[Skills & Tools](../features/skills.mdx)** — GitHub templates, MCP servers.
- **[Knowledge Bases](../features/knowledge-bases.mdx)** — for the style guide.
- **[Sessions](../features/sessions.mdx)** — to read why the agent said what it said.

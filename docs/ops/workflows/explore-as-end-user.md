---
title: Explore as an end user
sidebar_position: 1
slug: /workflows/explore-as-end-user
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Workflow — Explore as an end user

The end-user path from sign-in to running an agent. No setup required beyond completing the welcome.

<video controls width="720" muted>
  <source src="/videos/03-work-explore-templates.webm" type="video/webm" />
</video>

## Goal

Sign in, open the Work dashboard, describe what you need, and either pick a template or browse the catalogue.

## Steps

1. **Sign in** at `/login`. You'll be sent to `/onboarding` on first run — see [First-run setup](../getting-started/first-run).
2. After onboarding the **Work dashboard** opens with a "Hi &lt;your name&gt;" greeting and a "What will you automate today?" prompt.
3. **Type** what you need in the **Describe what you need** textarea. As soon as you start typing, the **Find Templates** button becomes active.
4. (Optional) Click one of the **Quick Starts** chips — *Answer support questions*, *Summarize meetings*, *Onboard a new user* — to skip the typing.
5. Click **Find Templates** to get suggested templates for your description, or click **Browse all templates** to open the full catalogue at `/work/templates`.
6. Pick a template. The agent is created (under the hood) and you land on its **Chat** page, ready to send the first message.
7. To resume an earlier chat, open **/work/sessions** and pick a session — you'll be navigated to `/work/agents/<agent-id>/chat/<session-id>`.

## What happens server-side

- "Find Templates" hits the templates API and returns suggested matches.
- Picking a template creates an Agent under your default project. (See [Agents](../features/agents).)
- Opening Chat starts a new `Session`.

## Gotchas

- If you don't see your agent after picking a template, refresh — the page updates as soon as deployment moves to **Running**, but transient deploy errors can drop the live update.
- The Work surface **redirects to /onboarding** if `agentOnboardingDone` isn't set in your browser's localStorage. Clearing site storage resets that flag.

## Related

- [Agents](../features/agents)
- [Sessions](../features/sessions)
- [First-run setup](../getting-started/first-run)

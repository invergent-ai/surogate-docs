---
title: Sessions
sidebar_position: 2
slug: /features/sessions
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Sessions

## What it does

A **Session** is one chat thread between a user and an agent. The same session list shows up in two places:

- **Work side** at `/work/sessions` — your own sessions across all agents you can run.
- **Studio side** at `/studio/sessions` — every session visible to you (across agents, useful for debugging and review).

Each session has a stable `sessionId`. You can deep-link to one with `?agentId=…&sessionId=…`.

## When to use it

- Resume a chat you started earlier.
- Audit what an agent said to a user.
- Debug an agent's reasoning trace (Studio view exposes the trajectory tab).

## Prerequisites and permissions

- **Read your own**: any signed-in user (you always see your own sessions).
- **Read other users' sessions**: project `editor` or higher. _TODO(verify)._
- **Delete / export**: project `editor` or higher. _TODO(verify)._

## Step-by-step — open a session

1. Switch to **Work** mode.
2. Open **/work/sessions**.
3. Pick a session from the list. You'll be navigated to `/work/agents/<agent-id>/chat/<session-id>` and the chat resumes from where you left off.

To browse all sessions (builder view):

1. Switch to **Develop** mode.
2. Open **/studio/sessions**.
3. Filter by agent with **Agent** dropdown (or by URL: `?agentId=<id>`).
4. Open a session — Studio sessions expose tabs for **Thread** (messages), **Trajectory** (agent reasoning + tool calls), and others depending on the agent type. _TODO(verify) — tab list._

## Field reference

The session row shows the agent name, the start time, the message count, and a status indicator. _TODO(verify) — exact columns on a populated account._

## Edge cases and gotchas

- Sessions are tied to the **agent version active when the session started**. Updating the agent doesn't rewrite history — but new messages may behave differently.
- A session can be **flagged** for review (see [Monitoring](./monitoring) → Alerts). Flagged sessions show up in the Recent Conversations panel of the Studio Dashboard.
- Deleting an agent does not delete its sessions. _TODO(verify)._

## Related

- [Agents](./agents)
- [Monitoring](./monitoring)
- [Workflow — Explore as an end user](../workflows/explore-as-end-user)

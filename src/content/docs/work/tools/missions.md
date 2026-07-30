---
title: Missions
---

The **Missions** page is a dashboard for every goal your agent is working toward — the runs you start with the `/goal` and `/mission` slash commands.

Open it from an agent's left navigation (**Missions**, under the Sessions group) or go to `/work/agents/<agentId>/missions`. The **Missions** link only appears when missions are enabled for the agent.

## What a mission is

A mission is a saved goal the agent keeps iterating on until an evaluator decides it is met. You don't create a mission from this page — you start one from a chat with `/goal` or `/mission` (see [Goals](/work/tools/goals/)). This page is where you watch and manage the missions that already exist.

## Layout

The page has a header and two panes:

- **Header** — the title "Missions" with a subtitle, plus an **ACTIVE** / **HISTORY** toggle on the right.
- **Left list** — one row per mission. Each row shows the mission description, a relative "last updated" time, a status badge, and the agent name.
- **Right pane** — the full mission dashboard for the selected mission. When a mission is selected you can open the transcript of the session it ran in.

The newest mission is selected automatically so the dashboard is never blank while missions exist. Selecting a row on the left swaps the dashboard on the right. The list refreshes every few seconds.

## Active vs. History

The **ACTIVE** / **HISTORY** toggle filters the list:

| View | Shows |
|---|---|
| **ACTIVE** | Missions that are still running or paused. |
| **HISTORY** | Missions that finished or were cancelled. |

When there are no missions in the current view, the page shows an empty state. In **ACTIVE** it reads "No missions yet — Start one with /goal or /mission in any chat." In **HISTORY** it reads "No past missions — Finished and cancelled missions show up here."

## Mission status

Each mission row carries a status badge:

| Status | Meaning |
|---|---|
| **Running · _n_/_max_** | Actively iterating; shows the current iteration out of the maximum. |
| **Needs revision** | The last evaluation asked for another pass. |
| **Paused** | Automatic continuation is stopped; the mission is retained. |
| **Satisfied** | The goal was met. |
| **Blocked** | Stopped — the agent needs external input it can't get. |
| **Failed** | Stopped — the goal was judged unreachable. |
| **Max iterations** | The iteration budget was exhausted. |
| **Cancelled** | The mission was cancelled. |

Running, needs-revision, and paused missions count as **active**; the rest are **history**.

## Starting and tracking a mission

1. In any chat with the agent, type `/goal <what you want>` (or `/mission …`) and press Enter. See [Goals](/work/tools/goals/) for how to write a good rubric.
2. Open the **Missions** page. The new mission appears at the top of the **ACTIVE** list.
3. Click the mission to open its dashboard on the right, where you can follow its progress and open the underlying session transcript.
4. When the mission is satisfied, blocked, failed, cancelled, or hits its iteration cap, it moves into **HISTORY**.

Control commands (`/goal pause`, `/goal resume`, `/goal clear`, `/goal status`) are issued from the chat, not from this page.

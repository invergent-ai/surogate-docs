---
title: The Agents page
sidebar:
  label: Agents
---

The **Agents** page shows how the agents of your case types are doing: "The agents that work steps in this project's case types". Pick an agent to see what it did over a period, the steps it works, the questions it raised, what it may use and its sessions.

Everyone on the project sees the list, the figures and the steps. Sessions, raised hands and **Export for audit** show case content, so only editors and owners see them; see [What your role lets you see](#what-your-role-lets-you-see). Keel records each case they show as your view of it.

## The list

The list, headed **Agents**, holds the agents named by the current published versions of the project's case types, by name. An agent Keel has no name for shows by its id. A draft adds no agent until it is published.

Under each name Keel says how many steps the agent works and how many of its runs are under way, such as `3 steps in 2 case types · 4 in progress`, or `1 step in 1 case type · none in progress`. A run waiting on a raised hand counts as in progress. An agent that only starts cases (an intake agent) reads `0 steps in 0 case types`.

Pick a row to open the agent. The first agent opens by default.

Under the agents, **Helpers, not on any step** lists the project's two helpers, the case agent and the designer agent. They work no step and cannot be picked. Each has a line: "Answers questions inside any case. Drafts, never moves a case." and "Drafts case types from a conversation. A person publishes." A helper switched off in Studio is marked **Off**. See [The project's helpers](/keel/builder/designer-agent/#the-projects-helpers).

With no agent named, the list says "No case type of this project names an agent yet." The helpers still show. Agents are made in Studio; **New agent**, in the page header, opens Studio in a new tab. Editors and owners see it.

## Period

**Period** offers **Last 7 days**, **Last 30 days** and **Last 90 days**. It opens on 30 days. The figures, the steps, the raised hands and the sessions are counted over the runs that started in the period, except as the sessions tabs say below.

While figures for a new period load, the last ones stay, dimmed, still named for their days, until the new ones arrive. The raised hands and the sessions do the same.

The address keeps the agent, the period, the sessions tab and the search, so you can share a link to them. Picking another agent keeps the period and the tab and clears the search.

## The agent

Its name heads the detail. Under it, once Studio answers, one line says what Studio holds of it, such as `Version 12, published 18 Oct · Pro model tier · 3 skills · 1 knowledge base`. The model reads **Pro model tier**, **Base model tier**, or **Own model** with its name. The line ends with `Off in Studio` when the agent is switched off there. **Edit agent** opens the agent in Studio in a new tab.

If Studio cannot be read, the page says "Studio's details of this agent could not be read." with **Try again**. Everything from Keel stays as it was.

## Figures

The four figures are named **Figures of** the agent, with the caption "Over the runs that started in the last 30 days."

| Figure | What it is |
|---|---|
| **Steps done · 30 days** | Runs the agent completed, including steps it drafted for a person to finish. Work items it took from a queue count when it completed them. |
| **Raised a hand** | The share of the runs of its own steps that raised a hand at least once. Work items taken from a queue are not counted. |
| **Passed checks** | Of the runs that were done or refused by a check, the share done without a refusal. |
| **Cost per step** | The cost its runs reported, divided by the runs done, in dollars. |

A figure with nothing to divide reads `—`, and a count of none reads `None`. A rate above 0 never reads `0%`; it reads `<1%`.

### Steps it works

The table **Steps it works** has a row for each step the agent works, most done first, each in its case type at its version, such as `Loan request v3`. The step's name opens the case type at that step. "Each step's contract is set in its case type"; see [Steps](/keel/builder/steps/).

| Column | What it shows |
|---|---|
| **How it works** | **Alone**; **Drafts, a person finishes**; **Works a person's step from a queue**; **Votes as a queue member**; or **Answers raised hands from a queue**. |
| **Done** | Runs of that step completed. |
| **Hand raised** | The share that raised a hand. |
| **Passed checks** | The same share, over that step's runs. |
| **Median time** | The median time from start to end of the runs done, such as `under 1 min`, `10 min`, `23 h` or `2.3 d`. |

A step no run worked in the period shows `None` and dashes.

## Raised hands

**Raised hands** lists the questions the agent's steps asked, newest first, 25 at a time: "Each question the agent asked, and how people answered." Each shows:

- the question, then its case number, the step and when it was raised, such as `LR-000001 · Check the file · 20 Oct, 09:00`;
- `Choices:` when the agent offered some;
- how it stands: `Waiting on` the queue, `Closed without an answer`, or `Answered` with the answer in quotes, who gave it and when, such as `Answered "valid up to six months" by Ana Marin, 20 Oct, 10:15`. A name Keel does not know reads `an agent` or `a person`;
- `Note:` when the person who answered added one.

**Open** goes to the hand's session. **Show more** adds the next 25. With none, the card says "It raised no hand in the last 30 days."

## What it may use

**What it may use** shows what Studio gives the agent, in four rows:

- **Skills** and **Knowledge**;
- **Tools**: the groups of tools it may use. A group with some tools never allowed reads `Browser, 1 of 2 tools`;
- **Systems**, only when the agent is connected to some. One switched off reads `name, off`.

A row with nothing says **None**. The foot names the groups it may never use: `Never: Web. A step can narrow this list, never widen it.` With no such group it says only "A step can narrow this list, never widen it."

## Sessions

**Sessions** holds one session for each step the agent works: "One session per step it works. Every tool call, file read and answer is in it." The tabs carry Keel's count of their sessions.

| Tab | What it lists |
|---|---|
| **Running** | Every session at work now, whenever it started. |
| **Hand raised** | Every session waiting on a raised hand now, whenever it started. |
| **Finished** | Sessions that started in the period and ended. |
| **Failed checks** | Sessions that started in the period and were refused at least once. |
| **All** | Sessions that started in the period, and those at work now. |

The tab **Running** opens first. An empty tab says "No session is running.", "No session has its hand raised.", "No session finished in the last 30 days.", "No session failed a check in the last 30 days." or "No session in the last 30 days."

**Search by case number, title or step** finds sessions on the open tab once you type two characters and pause. It matches a case number's start, and the case's title or the step's name anywhere. With none found, the card says `No session matches "text".`. A search narrows the list, not the tabs' counts.

Each row shows:

- **Case and step**: the case number and title, and the step.
- **Status**: **Starting**, **Working**, **Working with a person**, **Drafted, a person finishes**, **Hand raised**, **Done**, **Drafted**, **Returned to its queue**, **Stopped**, **Failed** or **Finished**.
- **Doing now**: for a running session, the item of its plan in progress, read every 30 seconds; for one with its hand raised, `Waiting on` the queue and the question; for a finished one, `Outcome` and its value, and how many checks it failed, such as `Outcome approve · 1 failed check`. A dash when there is nothing to say.
- **Started**.
- **Time · cost**: a running session's time so far, such as `41 min · $0.37`; `waiting 22 min · $0.37` for one with its hand raised; the time from start to end for a finished one. The cost shows `—` until the session reports one.
- **Watch** on a running session, **Open** on any other.

The card counts the rows, such as `1 of 4 sessions`, and **Show more** adds 25. It ends with "Finished sessions keep their full record." and **Export for audit**. While a new tab, search or period loads, the last rows stay, dimmed.

### A session

**Watch** and **Open** open the session. The page is titled with the step and the case, such as `Check the file on LR-000001`, and says `Underwriting agent · Done · read-only` under it. **Back to** *agent name* returns to the agent's page, with the period, tab and search you left. The session is read-only: it has no box to type in.

Beside the session, **This session** gives the **Case**, **Case type** with its version, **Started**, **Ended** (`Still at work` while it runs), **Time · cost**, **Tokens**, **Agent version**, and **Outcome** once it has one. **Tokens** reads `41,000 in · 3,200 out · 12,000 from cache`; the cache part is left out when none was reported. **Failed checks** and **Raised hands** cards appear only when the session had some; a failed check shows its message and its code.

While the session is at work, the page reads its record again every 30 seconds and the session is live. When it ends, the session shows as it ended. What the session shows is what [Watch](/keel/business/watch/) shows staff.

| Message | Why |
|---|---|
| **No session of this project's agents has this id.** | The link is wrong, or the session belongs to another project. **Back to agents** returns to the page. |
| **This session could not be loaded** | Keel's words follow, with **Try again**. |
| **The agent's session cannot be reached now.** | **Try again** opens the session again. |
| **Nothing to show yet.** | No entry to show has arrived yet. |

## Export for audit

**Export for audit** saves a file, one row for each run of the agent that started in the period shown, the oldest first. A row holds the run's case number, case type and version, step, session, start and end, how it ended, outcome, failed checks, raised hands, tokens, cost in dollars and the agent version. A fact a run lacks is an empty field. The tab and the search do not narrow it.

The button reads **Exporting…** and cannot be pressed again while the file is read. Keel refuses an export of more than 100,000 runs: "The export holds more than 100,000 runs; choose a shorter period." A refusal, or a file cut short, shows a short message and saves nothing.

## When a read fails

Each part of the page reads on its own. A part that fails says why, in Keel's words when it has some, and offers **Try again**. When a read took too long, Keel says "The figures took too long to read. Try a shorter period." The period stays within reach.

When Keel gave no words, the page says:

| Part | Message |
|---|---|
| The list | "The agents could not be read." |
| The figures and steps | "The agent's figures could not be read." |
| Raised hands | "The raised hands could not be read." |
| Sessions | "The sessions could not be read." |
| Studio's details | "Studio's details of this agent could not be read." |

A **Show more** that fails shows a short message and keeps the rows.

## What your role lets you see

| What | Viewer | Editor | Owner |
|---|---|---|---|
| The list, the figures, **Steps it works**, **What it may use**, **Edit agent** | Yes | Yes | Yes |
| **New agent** | No | Yes | Yes |
| **Raised hands**, **Sessions**, a session's page, **Export for audit** | No | Yes | Yes |

A viewer reads "Sessions and raised hands show case content. The project's editors and owners read them." in place of the hands and the sessions. A viewer who opens a session's address reads "Sessions are for the project's editors and owners." Keel reads none of it for a viewer. See [Roles and permissions](/keel/reference/roles/).

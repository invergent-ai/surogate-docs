---
title: Watch an agent's session
sidebar:
  label: Watch
---

**Watch** shows what an agent does on a step of a case, read-only and live. Any member of the project's staff can watch the sessions of the cases they can open.

## Opening Watch

- On a case, press **Open its session** on the card of a step an agent works, or of a step whose agent asked a question.
- On the Work page, under **Agents at work**, pick an agent and press **Watch** on a run of one of its steps. A run on a work item, which the agent took from a queue or was handed, has no **Watch**.

The page is titled **Watching** and the agent's name. Under it are the step, the case and "read-only". **Back to the case** returns to the case.

While the step is open, new entries appear as the agent works. Once the step is no longer open, the page says "This step is no longer open. Its session shows as it ended."

## What it shows

The session reads like a chat, with no box to type in:

- the step starting: "Started" and the step's name;
- the agent's own words, and its questions when it raises a hand;
- the messages people sent it, and the answers it got;
- one line for each thing the agent does, such as "Read *file*", "Wrote *file*", "Searched the case's files", "Searched the web for …", "Read a page on *site*", "Used the browser on *site*", "Ran a command", "Searched the policies", "Followed a procedure", "Handed part of the work to a helper", "Reported its result", or "Used a tool";
- the policy pages it read, such as "Read Credit policy 2026", with the page;
- its plan, as "Updated its plan: 2 of 5 done";
- "Paused", "Finished a turn", and "The agent's session failed." when it failed.

## What it does not show

Watch shows the case's work, not the agent's machinery. It never shows:

- the agent's configuration, prompt, model or cost;
- which skill it followed, or the skill's text: a skill shows only as "Followed a procedure";
- knowledge bases as such: a page read shows as its policy and page;
- tools' settings or their results, MCP servers, connections or credentials;
- the agent's thinking, or the text of its step's setup.

Keel records each time someone watches a session, as it records each time someone opens a case.

## When Watch cannot show a session

| Message | Why |
|---|---|
| **This step has no agent session.** | No agent worked this step. |
| **The agent's session cannot be reached now.** | A temporary problem. Press **Try again**. |
| **Nothing to show yet.** | The agent's session has not started, or has done nothing yet. |
| **You cannot watch this session.** | Keel refused to show it to you. |
| **This case does not exist, or it is not this project's** | The link is wrong. |

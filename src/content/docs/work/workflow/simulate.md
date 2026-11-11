---
title: Simulate
description: Draft a plan of made-up people, run them against your agent on its real channels, and fix what failed before anyone real sees it.
---

**Simulate** lets you try an agent on made-up people before real customers reach it. Each person writes to the agent through the same channel setup real customers use: its identity, skills, knowledge, tools, and on WhatsApp its forms and team alerts. Nobody real is ever written to. Each person comes with a test, and when the run is over you see which tests passed and what to change for the ones that did not.

Open it from **Simulate** under the agent in the Work sidebar. Anyone in the project can look; only editors can start a run. It is not offered on system agents such as the Copilot.
## Draft a plan

Simulate opens calm. Nothing is made up until you ask.

Type what to look at under **Anything to focus on?**, for example "returns and refunds", or leave it empty. Then press **Draft a plan**. It takes a few seconds.

The plan is a short list, one line per person:

> **Elena**, first-time buyer. WhatsApp.
> Wants to return shoes bought 40 days ago.
> Tests: explains the 30-day policy and offers store credit

Each line has the person, what they want, the channel, and **Tests**: what the agent has to do for this person to pass. Most people are ordinary, a few are awkward, and one or two push against the agent's rules. You don't set a difficulty.

If the agent has a [team](/work/tools/programs-team/), team members are lines too, with their real rights. For example: "Ioana, nurse, limited rights. Tests: is refused when she asks for a full phone number."

Change the plan until it is what you want:

- **Untick** a line to leave that person out.
- Change the **channel**. The agent's live channels come first, and only channels that can run are listed.
- Click the sentence or the test to rewrite it.
- **Add someone** takes a few words, such as "a supplier whose invoice is 40 days late", and fills in the rest.
- **Another plan** drafts a new one. Your focus stays.

Autopilot plays every person, on every channel including your website. The one exception is a voice call, marked **You play this one**: you speak as the person.

**Start N** runs the N ticked lines. If the draft fails, the page keeps your focus text and you can still **Add someone** by hand.

## Watch it run

The run opens straight away. The left side lists everyone, with where they are: writing, waiting for the agent, done, and then passed or failed on their test.

The middle shows the selected person in their real app: WhatsApp, Telegram, Slack, Teams, Discord, your website, or a phone. The agent's tool calls show inline.

- **Take over** lets you write as that person. **Hand back** gives them back to Autopilot, which carries on from where the conversation is.
- **Send the next step now** shows on anyone enrolled in a [Program](/work/tools/programs-team/). Program check-ins reach simulated people only this way.
- **End** stops the whole simulation.

You can leave the page and come back. The run keeps going.

![A run: the people on the left, one customer's WhatsApp in the middle, and how it went on the right](../../../../assets/screenshots/work-simulate-run.png)

A run ends on its own when everyone is done. Autopilot stops a person when they got what they came for, when they would give up, or when the agent stays silent for three minutes after its last turn. A person stops after 20 messages, and a run after 30 minutes.

## How it went

When everyone is done, the right side shows **How it went**, for example "4 of 6 passed". Each failed test shows:

- **Why**: one sentence. **See** scrolls the chat to that message.
- A **proposed change**, shown as before and after. It changes the identity, a skill, or a note in a knowledge base.
- **Apply** or **Skip**.

**Apply all** applies every change you did not skip. A change takes effect on the agent's next conversation, real ones included. A team problem, such as the wrong person being alerted, is fixed on the [Team](/work/tools/programs-team/) tab of Programs.

Tests that passed are listed below, folded.

**Check again** runs only the people who failed, with the same test and channel. They show ✗ to ✓ against the earlier run, so you see which changes held. A change that did not hold needs another wording or another part.

If the grading fails, the people show as done without a result and you can **Grade again**.

## What it learned

Before a plan is drafted, the page lists **What it learned**: every change made from a simulation, the test it fixed, and when. **Undo** puts the identity or skill back as it was, or removes the knowledge note. If the text was edited after the change, undo it where it was edited. Past simulations are listed too, with **Run again**.

## What is real and what is not

Simulated people write to the agent the way real ones do, but nothing real is touched.

- Tools that only read, such as a lookup, run for real.
- Tools that change something are not run. The agent gets a plausible answer, and the trace says what it would have done, for example "would have sent an email to ... (not sent)".
- Simulated people never show up in Users, Sessions or Programs, and never reach your webhooks.
- A run ends itself, and is deleted after 90 days.

## Ask the Copilot

The [Copilot](/work/tools/copilot/#testing-and-improving-an-agent) can do all of this for you. Ask it to "test my agent with three hard customers" or "see how my agent handles a refund request". It drafts the plan, runs it, and reads you the result. For each fix it shows the change and asks before applying anything. Every run it starts shows in your past simulations, marked *Started by Copilot*, so you can watch it and take over.

## Related

- [Improve your agent](/work/workflow/improve-agent/): marking real sessions, attaching resources, editing the identity
- [Team and escalations](/work/tools/programs-team/): who the agent alerts
- [Review sessions](/work/workflow/review-sessions/): what real customers did

---
title: Working with agents
sidebar:
  label: Working with agents
---

Agents work some steps of a case, alone or with a person. In the business app, agents show by name and status, beside people: in work lists, on a case's Now cards, under **Agents at work**, and on the Team page. You never see an agent's configuration, its skills or its knowledge bases.

An agent never decides where a case goes. It finishes its step with one of the step's outcomes and the fields the step asks for, with a source for each value, or it asks a person.

## When an agent asks a question

When an agent needs a person, it **raises a hand**: it asks a question, sometimes with answer choices and evidence, and its step pauses. The question goes to the queue the builders named for that step.

- It shows as an **Agent question** in the queue's **Agent questions** tab, and in **Needs me** once it is assigned to you.
- Its case shows "*Agent* asked a question" on the step.
- It waits until someone answers. A question never expires.

Answer it on the Work page: pick your answer or type one, add a note if you like, and press **Send answer**. The agent picks the step up again with your answer, and the note is kept in the case's history. See [Answer an agent's question](/keel/business/work/#answer-an-agents-question).

You can answer a question assigned to you, or one waiting unclaimed in one of your queues. You can also delegate it, or return it to its queue.

## When an agent drafts for you

On a step an agent drafts and a person finishes, the agent works first, then its draft fills your form, each drafted field marked "Drafted by *agent*. Nothing is sent until you submit." You check it, change what you need, and press **Submit**. The submission is yours: your authority and maker-checker are checked, not the agent's.

**Ask to revise** sends the agent a note and asks it to draft again. See [A step an agent drafted for you](/keel/business/open-case/#a-step-an-agent-drafted-for-you).

## Following an agent's work

### On the case

While an agent works a step, the case's **Now** card says "*Agent* is working", with how its run stands: **Starting**, **Running**, **Waiting**, or **Drafted** once it has drafted a step for its person. The card also shows the agent's plan and when it was last active, and where its question would go if it needs a person.

- **Message the agent** sends it a word while it works, such as a fact it should know. The message is kept in the case's history as your note.
- **Open its session** shows what it is doing, read-only. See [Watch](/keel/business/watch/).

### Agents at work

On the Work page, **Agents at work** lists each agent working steps of the project's cases now, with how many steps. With none, it says **No agent is at work.**

Pick an agent to list its runs, "Its steps at work, the longest first.": each with its **Case**, **Step**, **Status** and **Since**, and **Watch**, which opens the session. An agent with nothing running says it is not at work now. An agent a supervisor turned off says "Off: people work each of its steps that opens from now on."

## When an agent cannot work

- **When an agent fails for good**, people take its step: it opens as a step in the queue that gets the agent's questions, and the queue's members claim it and work it like any other step. On a step the agent drafts for a person, the person works on alone.
- **When a supervisor turns an agent off**, each of its steps that opens from then on goes to people the same way. Steps it already works carry on. See [Agents](/keel/business/supervisors/#agents).

## Authority applies to agents

Agents have authority limits too, set on the Team page like a person's. An agent with no limit in a step's scope, or one below the amount, cannot complete a step that checks authority.

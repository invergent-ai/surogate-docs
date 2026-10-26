---
title: The Work page
sidebar:
  label: Work
---

**Work** is your home page in the business app: "your items and your teams' queues". It shows what needs you, what you handed to others, what you did today, the queues you work in, and the agents at work. The page keeps itself current; there is nothing to refresh.

The page has three columns on a desktop:

- on the left, the lists you can open: **Mine**, **Team queues** and **Agents at work**;
- in the middle, the list you picked, labelled with the order it is in;
- on the right, the item you picked.

On a phone, the lists come first, and an item opens on its own with **Back**.

## Mine

| List | What it holds | Order |
|---|---|---|
| **Needs me** | Work you hold: steps assigned to you or that you claimed, items delegated to you, votes you owe, and agents' questions assigned to you. | Nearest deadline first |
| **I delegated** | Open items you handed to someone else, until they are done. | Nearest deadline first |
| **Done today** | What you did since midnight, in your time zone. | Most recent first |

Each list shows its count in the column. The **Work** row in the left rail shows the count of **Needs me** as a badge.

Unclaimed work in your queues is not in **Needs me** until you take it. Find it in your [team queues](/keel/business/queues/), or press **Get next**.

### What a row shows

Each item shows:

- its kind: **Your step**, **Delegated to you**, **Step**, **Your vote**, **Vote**, **Agent question** or **Escalation**;
- its case: number and title;
- what it needs: the step's name, an agent's question, or **A deadline was missed** for an escalation;
- why it is here, in a sentence, such as "Assigned to you", "Ana Marin handed it over", "Underwriting agent asks you", "Your vote is owed", or "Escalated to Underwriting". An agent that holds an item is named like a person, such as "Assigned to Document checker";
- its service level: **Past deadline**, with how long ago, such as **Past deadline · 2 h**; **Past goal**; **Due today**; the time left to its deadline, such as **3 d left**; or **On time** when it has no deadline. An item done shows when it was done.

## An item

Pick an item to see it on the right: its kind and service level, what it needs, its case, and:

- **Why**: why it reached you;
- **Returned**, for an item an agent gave back: why, and when, such as "Document checker returned it: The payslip is unreadable." See [When an agent returns an item](/keel/business/agents/#when-an-agent-returns-an-item);
- **Since**, **Goal**, **Deadline**: when it opened, and its service level's times;
- **Done**, for an item done.

**Open case** opens the case. Steps and votes are worked in the case, where their form and the case's files are. See [An open case](/keel/business/open-case/).

If an address points at an item the list no longer holds, the pane says so: it may have been answered, returned or handed to someone else, or it is not yours.

### Hand an item to someone else

For an item you hold, a step or an agent's question, the pane shows **Delegate** and, when the item has a queue, **Return to queue**.

- **Return to queue** puts it back in its queue, unclaimed, for someone else to take.
- **Delegate** opens **Delegate**: "Hand this item to someone on the staff or to an agent. It leaves your work and shows in I delegated until it is done." Pick a person under **People** or an agent under **Agents**, and press **Delegate**. Keel says **Handed to** and the name.

The person you pick sees it in their **Needs me** as **Delegated to you**. An agent you pick starts work on it at once; if it cannot finish it, it returns the item to you. Only some items take an agent: see [Agents in queues and as delegates](/keel/business/agents/#agents-in-queues-and-as-delegates). A vote cannot be delegated: every member of its queue votes for themselves.

When an item leaves you, returned or delegated, any draft the [case agent](/keel/business/case-agent/) made of its form for you is dropped. Whoever holds it next starts with none.

### Reassign an item

Supervisors see **Reassign** on any open item but a vote, whoever holds it. It opens **Reassign**: "Give this item to someone on the staff or to an agent. Whoever holds it now no longer does." Pick a person under **People** or an agent under **Agents**, and press **Reassign**. Keel says **Given to** and the name.

Whoever holds the item now is not offered. When there is no one to offer, the dialog says "There is no one to hand it to." Taking an item from an agent stops its work on it.

### Answer an agent's question

When an agent working a step needs a person, it raises a hand, and its question becomes an **Agent question**. You can answer it when it is assigned to you, or when it waits unclaimed in one of your queues. The item shows:

- who asks, such as "Underwriting agent asks you", and when it asked;
- the question;
- the case, and the step it paused: "*step* · paused until you answer";
- the agent's progress on that step: its plan, and when it was last active;
- the agent's **Evidence**: cards with a value and the file it comes from, which open the case on that file, and notes;
- **Your answer**: one of the agent's choices, or a text box when it gave none;
- **Note for the agent and the case history**, optional.

Press **Send answer**. "Your answer goes back to the step. The note goes to the agent and is kept in the case history." The agent resumes the step with your answer.

An agent never stops waiting by itself: a question stays open until someone answers it. See [Working with agents](/keel/business/agents/).

## Get next

**Get next** in the page header hands you your next piece of work:

1. If **Needs me** holds anything, it opens the first item there.
2. Otherwise, it takes the first unclaimed item from your team queues and opens it. It looks at your queues by their priority, and in each queue follows the queue's serving order. The item is yours from then on.

When nothing is waiting, it says **Nothing is waiting for you.** Two people pressing **Get next** at once never get the same item.

**Get next case** on the [Cases page](/keel/business/cases/) does the same, and opens the item's case.

## Team queues and agents at work

Under **Mine**, the column lists:

- **Team queues**: each queue you are a member of, with how many items are open in it, and **All queues**. See [Team queues](/keel/business/queues/).
- **Agents at work**: each agent at work on the project's cases now, on its own steps or on work items, with how many. See [Working with agents](/keel/business/agents/#agents-at-work).

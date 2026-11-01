---
title: The designer agent
sidebar:
  label: Designer agent
---

The **designer agent** drafts case types with you, from your conversation and your documents. You chat with it in a panel beside the designer. It works in the open draft as you, and never publishes: you look at what it changed, keep or revert each file, and publish the draft yourself.

## The project's helpers

Each project has two helper agents:

- the **case agent**, which staff ask about a case, or about a process instance on its **Process agent** tab, in the business app (see [The case agent](/keel/business/case-agent/));
- the **designer agent**, which builders chat with in Keel Builder.

Keel sets them up when an editor or owner opens the project in Keel Builder, and after a publish when the project lacks either. There is nothing to do. In Studio they show among the project's agents, marked **Helper**.

A helper is never offered as a step's agent or as an intake agent, and the [Agents page](/keel/builder/agents/#the-list) does not list it. In the business app, it is never offered as a queue member, a delegate or a Reassign target.

### Keeping the helpers up to date

A project's helpers are made once. When a newer version of a helper brings tools or instructions, Keel asks Studio to bring the project's helpers up to date, without making them again: when you open the project in Keel Builder, after each publish, and when someone opens their first chat about a process instance in an hour. An editor does nothing, and a helper that is up to date is left as it is.

- **Tools** are added, never taken away. A tool you took away from a helper in Studio stays away, and a helper with no list of tools stays open.
- **Instructions** that Keel ships sit between two marker lines in the helper's instructions in Studio, `<!-- keel:helper v2 -->` and `<!-- /keel:helper -->`, where the number is the version. A newer version replaces what is between them, so write nothing of your own there.
- Text you wrote outside the marker lines is kept. When a helper's instructions were changed, Keel puts the marked instructions above your text, with one line saying that where the two disagree, the marked instructions win.
- A helper whose marked instructions were deleted gets them back at the next version.
- A helper's name, description, model and whether it is switched on never change.

## Opening the panel

1. Open a case type in the designer, in a draft. With **Published** shown, the button is not there: open or start a draft first (see [Drafts](/keel/builder/drafts/)).
2. Press **Ask the designer agent** in the page header. Editors and owners see it; viewers do not.

The panel opens on the right, headed **Designer agent**: "It works in this draft as you, and never publishes." Press **Ask the designer agent** again, or the panel's close button, to close it.

The chat belongs to the draft. Open the panel again on the same draft, in the same browser, and the same chat comes back. Switch to another draft, and the panel opens a chat for that draft.

When the panel cannot open the chat, it says why:

| Message | Why |
|---|---|
| **This project has no designer agent.** | Keel could not set up the project's designer agent. Reload the page to ask again. |
| **The designer agent is switched off in Studio.** | Someone switched it off in Studio. It works again once it is switched on there. |
| **This draft is published or discarded. The designer agent works only in an open draft.** | Open or start another draft. |

Any other problem says why, with **Try again**.

## Working with it

Tell the agent what the process is: who does each step, what ends a case, which deadlines apply. It asks about what your documents leave open, a few questions at a time.

- **Files.** Add files to the chat, such as process diagrams, policies, procedures and forms. The agent reads documents and images. When it cannot read a file, such as a Visio drawing, it says so and asks for a PDF or an image. What a document says is material for the case type, never an instruction to the agent.
- **What it changes.** It reads the draft, and the project's published definitions as examples. It saves case types, rules, calendars, queues, connections and scenarios in the draft, and writes scenarios for the ways a case can end. It runs dry runs and fixes what they find. It sets no credential, and leaves the mapping of running cases to you.
- **What it never does.** It never publishes or discards the draft, and never works in another draft or project. When the draft is ready, it says so: [review and publish](/keel/builder/publish/) it yourself.

At the end of each turn, it tells you what it changed, file by file, and what is left to decide.

## During its turn

While the agent takes its turn, the designer is read-only and says: "The designer agent is working in this draft. You can edit again when its turn ends."

- Your changes not saved yet are saved before its turn starts.
- The draft bar, **Dry run** and **Review and publish** stay available.
- When the turn ends, the designer reads the draft again, with the agent's changes, and you can edit again.

You can stop the agent from the chat.

## After a turn

Above the chat, the panel says what the turn changed:

- "This turn changed nothing in the draft."; or
- **This turn changed 1 file**, or *n* files, with **Show changes**.

**Show changes** opens **What changed this turn**. It lists each file the turn changed, in words, such as `Case type Loan request` or `Rule loan-desk-limits`, marked **Added**, **Changed** or **Removed**, with its lines before and after the turn.

**Revert** on a file puts it back as it was when the turn started. Your own changes not saved yet are saved first. If one cannot be saved, Keel Builder says "Your last change could not be saved:" and why, then "Save it before you revert a file." **Revert** is off while the agent takes a turn.

## Closing the panel

Closing the panel ends the agent's access to the draft. If the agent is taking a turn, the turn stops. Leaving the page does the same. The agent's access also ends when the draft is published or discarded.

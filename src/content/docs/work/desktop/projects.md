---
title: Projects in Surogate Desktop
sidebar:
  label: Projects
---

:::note
Projects here are not the projects of Studio. A Studio project is the workspace you and your team share, with its members, agents and billing (see [Members and roles](/work/settings/members/)). A project in Surogate Desktop is one piece of ongoing work: a conversation that plans it, and threads that do it.
:::

A project in [Surogate Desktop](/work/desktop/overview/) is a coordinator chat plus the threads it hands work to. You talk to the coordinator about what you want. It splits the work into threads. Each thread is its own chat, with its own work to do. You can follow them all from one place, answer the ones that need you, and mark them done.

Projects are in Surogate Desktop only. The agent's web app has no Projects page.

## What you need

The agent must have **Multi session** on. It is a switch in the agent's **Configure** page, under **Capabilities**, and it is on by default. People who can edit the agent can change it (see [Capabilities](/work/workflow/configure-agent/#capabilities)). With it off, the agent keeps one conversation per user and has no projects. The agent answers project requests with "This agent keeps a single conversation, so it has no projects."

## Create a project

Open **Projects** in the sidebar, then press **New project**. The dialog asks for:

- **Name.** Up to 256 characters.
- **Goal.** What the project is for, up to 2000 characters. The coordinator and its threads see it.
- **Folder.** Press **Choose…** and pick a folder on this computer. The coordinator works in the folder itself. Each thread works in a copy of it. Surogate shows its usual sheet to confirm the folder and choose **Work freely** or **Ask every time** (see [Approvals](/work/desktop/overview/#approvals)). The threads ask the same way. The same folders are refused as for any chat (see [Folders that are refused](/work/desktop/overview/#folders-that-are-refused)). The field shows only when the agent lets chats work on folders of this computer. Otherwise the project lives in the cloud.

Press **Create project**. Its conversation opens.

The sidebar lists your projects under **Projects**. A dot on a project's mark means a thread is waiting on you. The **Projects** page shows them as cards, with a search box and **Sort by** **Activity**, **Created** or **Name**.

### Project settings

The gear in the project's header opens **Project settings**. It has the same **Name** and **Goal**, and:

- **Instructions.** How the project's threads work: the tone, the format, what to leave out. A thread started after a change follows it. A thread already started keeps the instructions it began with.
- **The conversation's model** and **The threads' model.** Choose **The agent's own**, **Basic** or **Pro**. The dialog notes that a model above your plan's runs as your plan's.

**Archive project…** is in the same dialog. It removes the project and its threads from your list. The files the project made, and the agent's memory of it, are kept.

## The coordinator and its threads

The coordinator does not do the work itself. It plans, hands work out and keeps track. It does not make documents either: a Word, Excel, PowerPoint or PDF file is a thread's job.

Ask for what you want in the project's conversation. The coordinator answers with threads:

- **Proposed threads.** A card lists each proposed thread with its title and goal. Press **Start** on the ones you want, or **Start all**. The card then says **Started**, with **View thread**. A project that works in a folder on your computer always proposes: only you can start its threads, from their cards.
- **Started by the coordinator.** In a project in the cloud, the coordinator can also start a thread itself. Ask it to propose first when you want to approve each one.

A thread the coordinator proposes for your own computer, in a project that has no folder, shows **Allow** (to work in a folder of this computer) or **Run in the cloud instead**.

Each thread is a full chat, with its own sandbox, working on one piece of the project. In a project with a folder, a thread works in its own copy of it. When the thread's turn ends, its changes are applied to the folder. The copy keeps threads from tripping over each other's files.

A thread saves the files it makes under `threads/<title>/`, where `<title>` is the thread's title. They appear in the project's **Library**.

A thread cannot start deep research, auto research or experiments yet. Ask for those outside a project.

## Follow the threads

The **Overview** button in the project's header opens a panel beside the conversation. Its **Threads** tab groups the project's threads:

| Group | What is in it |
|---|---|
| **Waiting on you** | Threads that need your reply or approval, or that failed. A row says why: **Question**, **Approval**, **Failed**, **Computer away** or **Files** |
| **Working** | Threads that are running now |
| **Idle** | Threads that finished their turn and wait for more |
| **Resolved** | Threads you marked done |

A row shows the thread's title, its status, its progress when it keeps a to-do list, how long ago it changed and the first files it touched. A dot on **Overview** means something waits on you.

The **Library** tab lists the files you add to the project and the files its threads produce.

### Reporting back

A thread reports to the coordinator when each of its turns ends. The coordinator reads the report and tells you where the work stands. Cards for started threads in the conversation show the thread's group and files too.

### Answering a thread

When a thread has a question, it waits under **Waiting on you**. Click its row to read it beside the conversation, and **Open** to show it in the main window. Answer it there, in the thread. A message to the coordinator does not answer the thread.

### Resolve and reopen

Press **Resolve** on a thread's row when its work is done. A thread still working is stopped first. It moves to **Resolved**, and **Reopen** takes it back out.

A new message to a resolved thread reopens it, from you or from the coordinator. A thread with no activity for 7 days counts as resolved on its own.

## Threads and sub-agents

[Sub-agents](/work/tools/sub-agents/) are helpers an agent calls on inside its own chat. You do not talk to them. A thread is different:

- It is a chat of its own that you can open and talk to.
- It is kept in the project after it finishes, and you can bring it back.
- It stays in view, in the groups above, until you resolve it.

## If the computer or the folder is away

A thread on a computer that is off or offline shows **Computer away** and carries on when the computer is back (see [When the computer is away](/work/desktop/overview/#when-the-computer-is-away)).

If a project's folder can no longer be reached on its computer, the Overview says why and offers **Use this computer for this project**. It moves the project to this computer and a folder you choose here. Threads started before keep their copies where they were made. New threads work in the new folder.

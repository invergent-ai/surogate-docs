---
title: Processes
---

The **Processes** page lists the project's [BPMN processes](/keel/processes/): "Upload, check and publish this project's BPMN processes." Press a row to open the process: its drawing, its file, the problems the checks found in it, its versions and its connections.

Draw a process on its page, in a draft, or make the file in a modeller such as Camunda Modeler or bpmn.io and upload it here.

## The list

| Column | What it shows |
|---|---|
| **Process** | The name, with the key under it. |
| **Version** | The current published version, such as `v2`. |
| **Published** | When the current version was published, and by whom; **Not published** for a process only drafts hold. |
| **Open drafts** | The open drafts that change this process. Each is a link that opens the process in that draft. **Cannot be read now** when the drafts could not be read. |
| **Running instances** | How many instances are open on each version, newest first, such as `3 on v2 · 1 on v1`; **None** when no instance is open. |

A process that exists only in a draft is listed too, under its key made readable. It opens in the newest draft that holds it. With no process at all, the page says **No processes yet**, and editors and owners read "Start one with New process." If the list cannot be read, the page says why, with **Try again**.

## New process

Editors and owners see **New process** in the page header. It is turned on once the list is read.

1. Press **New process**. **Start from** offers **A BPMN file**, the default, and **An empty diagram**. With a file, the dialog says: "Its file is saved in a draft as you upload it. Nothing published changes until the draft is published."
2. With **A BPMN file**, choose the **BPMN file**: "A BPMN 2.0 file from a modeller such as Camunda Modeler or bpmn.io, at most 5,000,000 bytes." With **An empty diagram**, type the process's **Name** instead. The dialog then says: "Its diagram is saved in a draft as you change it. Nothing published changes until the draft is published."
3. Check the **Key**. It fills in from the file: the name the file gives its process, else the process's id, else the file's name without its extension; from an empty diagram, it fills in from the **Name**. It is made into a key: lower case, without accents, with each run of other characters as `-`. When a process of the project has that key already, `-2`, `-3` and so on are added. Change it if you need to.
   - A key is letters, digits, `-` and `_`, starting with a letter or a digit. The dialog says so, "A key is letters, digits, - and _, starting with a letter or a digit.", when yours is not.
   - It says "A process has this key already." when you type the key of a published process, or of one the draft you pick holds.
4. Pick the **Draft** to put it in: **A new draft**, or one of the open drafts. A new draft asks for a **Draft title**, which starts as `New process: <the process's name>`, or the key when the file's process has no name; for an empty diagram, `New process: <the Name>`.
5. Press **Create**.

Create is turned on once a file is chosen, or a **Name** typed, its key is good, and the draft's processes are read; for a new draft, its title is not empty too. Keel saves the file in the draft exactly as you chose it, and the new process opens in that draft. Nothing published changes until the draft is published.

An empty diagram is a process named as you typed, with one start event. Keel's checks find two problems in it at once, which the Problems section lists: `Process_loan-review needs an end event` and `StartEvent_1 has no flow leaving it: every path must end at an end event`, with your process's key in place of `loan-review`. Draw the rest, as [Changing the diagram](#changing-the-diagram) says.

If the draft cannot be made, the dialog says why, in Keel's words when Keel gave them, else "The draft could not be started. Try again." If Keel refuses the file, the dialog says why, in Keel's words when they are for people, such as "A file is at most 5000000 bytes.", or "This draft is published or discarded." when the draft is no longer open, and stays open. Press **Create** again: a draft already made for it is used again, and no second one is made. If the process was saved but cannot be opened, the dialog says "The process could not be opened. Try again."

## A process's page

The page's header shows the process's name and, under it, its published version: for example **Version 2 published 20 Oct 2026 · 3 instances running on it**, or **Not published yet**. While the draft's file is shown, the name is the one that file gives its process. Under the header are a breadcrumb back to **Processes** and the [draft bar](/keel/builder/drafts/), then the tabs:

| Tab | What it holds |
|---|---|
| **Diagram** | The drawing of the file, and in a draft, the problems found in it. |
| **Versions** | Every published version, what each changed, and its file. |
| **Connections** | The connections the process calls, and their credentials. |

On the right of the header, everyone sees **Download**. Editors and owners also see **Upload a file**, with no draft open **Change the diagram**, and in a draft, **Dry run** and **Review and publish**. See [Dry run and publish](/keel/builder/publish/).

On the Diagram tab, a process that is not published, opened with no draft or in a draft that has no file for it, says **This process is not here**: "Open it in the draft that holds it." A draft that has no file for a published process says **The draft has no file for this process.**

### Upload a file

**Upload a file** puts a BPMN file in the draft as this process's file. It is kept exactly as you chose it, down to its bytes: Keel Builder does not read it or change it first.

With no draft open, Keel Builder asks for one first: the **Start a draft** dialog offers a **Title**, such as `Change Loan review`. Press **Start draft**, and the file is saved in the new draft. Cancel, and nothing is uploaded.

Once the file is saved, a message says `Uploaded loan-review.bpmn.` with the file's name, and the page shows the draft's file, on the Diagram tab even when you uploaded from another tab. If Keel refuses the file, a message says why, in Keel's words when they are for people, or "This draft is published or discarded." when the draft is no longer open, and the page stays as it was. A file you choose while another is on its way waits for it.

### Download

**Download** saves the file the page shows, as Keel has it, byte for byte. In a draft it is the draft's file, saved as `<key>.bpmn`; if a change to the diagram is waiting to be saved, it is saved first, and if it cannot be, a message says `Not saved:` and why, and nothing is downloaded. For a published version it is that version's file, saved as `<key>-v<version>.bpmn`, such as `loan-review-v2.bpmn`. A file Keel Builder cannot draw downloads like any other. If Keel refuses, a message says why and nothing is saved.

## The Diagram tab

The tab draws the file as the modeller laid it out. Drag the drawing to move it. The mouse wheel moves it up and down, and with Shift sideways. Hold Ctrl (⌘ on a Mac) while you turn the wheel, or pinch on a touchpad, to zoom. It opens fitted to the tab and centred. On a phone the tab is shorter: drag with one finger to move the drawing, pinch with two to zoom it, and touch outside the drawing to scroll the page.

The tab shows the file of the draft when a draft is open, else the current published version. When it shows a published version in a draft, or a version that is not the current one, `Version 2, as published.` says so, with **Show the draft's file** in a draft, or **Show the current version** when the version is not the current one.

In place of a drawing, the tab says why there is none:

- **This file cannot be read as a BPMN 2.0 file.** The file is not well-formed XML, or is not a BPMN 2.0 file.
- **This process's file has no diagram layout.** The file has no diagram, so there is nothing to draw.
- **This file could not be drawn.** The drawing could not make sense of the file.

If the file cannot be read from Keel, the tab shows Keel's words, or "The process's file could not be read.", with **Try again**. The page does the same when it cannot read the project's processes, "The project's processes could not be read.", or the draft, in Keel's words.

### Changing the diagram

In a draft, editors and owners change the drawing on this tab. Nothing is saved with a button: see [Saving](#saving-a-change).

**When you can change it.** The tab is the modeller when all of these hold:

- you are an editor or an owner, and a draft is open;
- the tab shows the draft's file, not a published version;
- you are not on a phone;
- the designer agent is not taking its turn in the draft;
- the file is in UTF-8, and a change would not alter part of it.

Otherwise the drawing is only read, and a sentence above it says why when there is one:

| The sentence | When |
|---|---|
| **Change the diagram on a larger screen.** | On a phone. |
| **The designer agent is working in this draft. You can edit again when its turn ends.** | While the designer agent takes its turn. |
| **This file is not in UTF-8, so it cannot be changed here. Upload it in UTF-8 to change it here.** | The file's bytes are not valid UTF-8. |
| **Changing the diagram here would change part of this file: …. Change it where it was made and upload it again.** | Keel Builder cannot write the file back whole. The sentence names what it would alter, such as `bpmn:conditionExpression on line 122`, `the reference to ghost` or `its encoding, ISO-8859-1`, joined by `;`. |

A viewer reads the drawing with no sentence, as does a published version.

On the Diagram tab of a published process, with no draft open and its current version shown, editors and owners see **Change the diagram** in the page header, but not on a phone. It asks for a draft, as an upload does: the **Start a draft** dialog offers a **Title**, such as `Change Loan review`. Press **Start draft**, and the process opens in the new draft, ready to change. In a draft, on the other tabs, with an older version shown, and for a process that only a draft holds, the button is not there.

**What you can draw.** Keel Builder offers only what Keel runs. Beside the drawing, the palette has the hand, lasso, space and connect tools, then **Create start event**, **Create end event**, **Create gateway**, **Create user task**, **Create timer intermediate catch event**, **Create expanded sub-process**, **Create pool/participant** and **Create group**. A picked element has a context pad. A flow node that is not an end event has **Append end event**, **Append gateway**, **Append user task** and **Append timer intermediate catch event**; an event-based gateway has **Append receive task**, **Append message intermediate catch event** and **Append timer intermediate catch event**; an end event has none. Most elements also have **Change element**, **Add text annotation**, a connect handle and a delete handle. What Keel does not run is not offered: a plain task, a throw event, a signal, conditional or compensation event, a data object or a data store. **Change element** lists only the kinds Keel runs; for a user task: **Service task**, **Receive task**, **Manual task**, **Business rule task**, **Sub-process (collapsed)** and **Sub-process (expanded)**. On a timer boundary event it also offers **Toggle non-interrupting**.

A file from another modeller can hold elements Keel does not run, such as a script task. They stay drawn, you can delete them or change them into a kind Keel runs, and a vendor's settings on them stay in the file through every change.

On the drawing, **Delete** removes what is picked, **Ctrl+Z** takes the last change back and **Ctrl+Y** does it again (**⌘** on a Mac), and **E** renames the picked element in place. **Undo** and **Redo**, above the drawing, do the same; each is off while there is nothing to take back or do again. An undo is a change like any other, and is saved. A file drawn afresh, after **Load the latest**, an upload, or the end of the designer agent's turn, has nothing to undo.

Keel runs one pool: a second pool cannot be drawn on a drawing that has one. Lanes, pools, text annotations and groups are drawn with the pointer only; once drawn, the panel names them and deletes them. A lane's name is the queue of the tasks in it: see [Lanes](/keel/processes/#what-keel-runs).

#### Saving a change

There is no save button. Each change is saved to the draft as the process's file a moment after you make it, as it is for any other change in the draft: the [draft bar](/keel/builder/drafts/#saving) says **Saving…**, then **Saved**, or **Not saved:** and the reason, with **Try again**, which sends the latest drawing. Your drawing stays as you changed it until it is saved. When someone else saved the draft meanwhile, the bar warns "This draft changed since you opened it. Each of your saves replaces the whole file as you have it.", your save is still made, and it replaces the process's file as they saved it. **Load the latest** reads the draft again and draws its file as it is then.

The first change to a file made in another modeller rewrites the whole file in Keel Builder's layout. A file that holds XML comments says so before you change it: "This file holds XML comments. Your first change here drops them; its elements, their settings and its layout stay." Its elements, their settings, a vendor's attributes and elements, and the diagram's layout are kept. Only the comments and the file's line layout change, so [Review and publish](/keel/builder/publish/#review-and-publish) can show many lines changed after the first change of an uploaded file. **Upload a file** still keeps a file byte for byte.

#### The panel

Beside the drawing, the column holds a panel, the Problems and **Elements**. The panel is headed by the kind of the picked element, such as **User task**, with its id under it, or by **Process** when none is picked. A viewer reads it and changes nothing, and so does an editor while the drawing cannot be changed (on a phone, during the designer agent's turn, for a file this page cannot write back, and for a published version). Where the drawing can be changed, a field is saved when you leave it, or press Enter in a one-line box: Escape puts the old value back. A box in the middle of typing is not a change.

An element's panel has:

- **Name**, or **Text** for a text annotation;
- **Delete**;
- on a flow node that is not an end event, a **Next element** pick with **Add after**, which adds that kind after the element, joined to it, and picks it: **User task**, **Manual task**, **Service task**, **Receive task**, **Business rule task**, **Exclusive gateway**, **Parallel gateway**, **Event-based gateway**, **Timer catch event**, **Message catch event**, **Subprocess**, **End event**, **Terminate end event** or **Error end event**; and a **Connect to** pick with **Connect**, which joins it to another element of its process or subprocess. If the drawing refuses, a message says "Nothing can be added after this element." or "These two cannot be connected.";
- on a task or a subprocess, a **Boundary event** pick with **Attach**: **Timer**, **Timer that does not interrupt** or **Error**. If it cannot be attached, "A boundary event cannot be put on this element.";
- for a user or manual task: "Its queue, outcomes and what it writes are not set here yet. Keel's checks list what it needs."; for a service task: "What it calls is not set here yet. Keel's checks list what it needs."; for a business rule task: "Its rule is not set here yet. Keel's checks list what it needs."

A task's settings are written in the file for now: see [Keel's settings in the file](/keel/processes/#keels-settings-in-the-file). A change made in the panel keeps them.

**The process.** With nothing picked, the panel has:

- **Name**: the name the page's header shows;
- **Queue**, **None** or one of the project's queues, published or in the draft: "Tasks that name no queue and lie in no lane go to this queue."
- **Calendar**, **None** or one of the project's calendars, published or in the draft: "The working hours that business timers and deadlines count."
- **Knowledge**, the knowledge bases as chips, each with a remove button, and an **Add** menu: "The knowledge bases the process's agent tasks may use." With none: "Its agent tasks use no knowledge."
- **Variables**, a table of **Variable**, **Type**, **Required** and **Personal data**, one row for each variable the process declares, with **Add variable**. With none, **No variables yet**: "A process keeps only the variables it declares."

If the project's queues, calendars or knowledge bases cannot be read, the panel says "The project's queues could not be read.", "The project's calendars could not be read." or "The project's knowledge bases could not be read.", each with **Try again**.

Press a variable, or **Add variable**, to open the dialog, which is the [case type's field dialog](/keel/builder/data/) with variable's words: **Add variable** for a new one, the variable's label otherwise. It has a **Name** for a new variable, a **Label**, a **Type** and what the type takes, **Required** and **Personal data**, and **Save**. The types are the case type's, without **File**, at every depth. A name is refused with "A variable name is lower-case letters, digits and _, starting with a letter.", "A variable has this name already." or `<name> is a reserved word.`. **Remove variable** takes the variable out of the file at once.

**A sequence flow.**

- Leaving an exclusive gateway, and not its default: **Condition**, a box for a CEL condition: "A CEL condition over the process's variables, such as amount <= 250000.0. The gateway takes the first flow whose condition holds, in the file's order." A blank condition takes it away.
- A gateway's default flow reads "The default flow of *the gateway*: taken when no condition holds." and has no condition.
- Any other flow reads "Only a flow that leaves an exclusive gateway carries a condition."

**An exclusive gateway** has **Default flow**: **None** or one of the flows that leave it, such as **Large · Sequence flow**: "Taken when no other flow's condition holds."

**A timer event** (a timer catch event, or a timer boundary event):

- **Timer**: **After a duration** or **At a date**. The kind you pick is kept in the panel until you type its value, so the file never holds a date made of a duration.
- **Duration**: "An ISO 8601 duration, such as PT2H or P3D." or **Date**: "A date and time with its offset, such as 2026-11-03T12:00:00+02:00, or a CEL expression over the variables."
- **Business time**: "Counts working time on the process's calendar." With no calendar on the process, it also says "The process has no calendar: pick one in its settings."
- On a boundary event, **Interrupting**: "An interrupting timer withdraws the activity; one that does not interrupt starts its path beside it."

**A message catch event or a receive task:**

- **Message**: one of the file's messages by name, **None**, or **A new message**. A new one asks for a **Message name**, and **Add message** adds it to the file and picks it. "The instance waits for a message of this name."
- **Writes**: the variables the message may write, as chips, with an **Add** menu: "The variables a message may write." With none: "The message writes no variable."

**An error end event or an error boundary event:**

- **Error**: one of the file's errors as *name* · *code* (the code alone when it has no name), or **A new error**, and on a boundary first **Any error**. A new one asks for an **Error name** and an **Error code**, says "An error needs a code." while the code is blank, and **Add error** adds it to the file and picks it.
- "Thrown when the path reaches this end." on an end event. On a boundary: "Catches the error of this code thrown inside the activity; Any error catches every code."

#### Elements, and the keyboard

The drawing takes the keyboard when it is focused, but its palette and context pad do not. So everything you draw is also reached without the pointer or the canvas. **Elements**, under the Problems, lists every element the drawing draws in the file's order, such as **Review the loan · User task**: its name, else its id, then its type. Type in **Find an element** to narrow it; with no match it says "No element matches." Press an element to pick it: the panel shows it and the address keeps it. A viewer sees the list too. Then use the panel's **Add after**, **Connect to** and **Attach** to draw. Everything but lanes, pools, text annotations, groups and the start event can be drawn this way; a start event is made from the palette.

#### Problems while you change

The checks still run by themselves for editors and owners, but not after every change: they wait until the draft is saved and you have stopped changing the diagram for a moment, so a minute of drawing sends a few checks, not one for each save. Meanwhile the Problems section says **You changed the draft since this dry run.** and the drawing marks nothing, so no mark sits on an element you moved, changed or deleted. A problem at an element you deleted names it in words, such as `score`, and is not a button, until the next check.

### Problems

In a draft, the drawing has a **Problems** section beside it, with how many problems the checks found in this process. It lists what the checks found in this process: the problems in its file, and those Keel placed at it, such as one in its connection file. Problems in other files, such as a case type, are not listed.

The checks run by themselves. Editors and owners need not press **Dry run**: opening the draft's file checks the draft, unless it was checked already as it is now, and when the draft changes, as it does after an upload or **Load the latest**, it is checked again. While it runs, the section says **Checking the draft…** A viewer reads "Only the project's editors and owners run the draft's checks." and no check is run.

Each problem shows:

- **Error**, which stops a publish, or **Warning**, which does not, such as a vendor's setting Keel ignores;
- Keel's message;
- its place. A problem at an element of the drawing names it, such as **Score the applicant · Script task**: its name, else its id, then its type. Press it to pick the element. A problem at the process reads **The process**. A problem at an element the drawing does not draw, such as **Documents · Message**, at a place Keel names in its own words, or in another file of the process, is listed but is not a button. A problem in another file of the process names that file, such as `bureau · Process connection checking/bureau` for a connection file.

The drawing marks the elements the problems name: an element with an error has a red outline and a red glow, one with only a warning an amber outline and glow. The element you picked is drawn in the focus colour with a glow of its own, and the drawing moves to it.

Picking an element, from a problem or by pressing it on the drawing, shows its problems only, under **At Score the applicant · Script task**, with **Show every problem**. An element with none reads **No problem at Application in · Start event.** Press the drawing's background, or **Show every problem**, to list every problem again. The address keeps the element, so you can send a colleague a link to it.

The section also says:

- **You changed the draft since this dry run.** when the draft changed since the checks ran. The list is the older run's, and the drawing marks nothing, until the checks run again.
- **Keel found no problem in this process.** when there is none.
- Keel's message, with **Try again**, when Keel refused to run the checks. They are not run again by themselves for that state of the draft: press **Try again**.

From the **Dry run** panel in a case type's designer, a problem Keel placed at a process links to the process, such as **Process loan-review**, with the element it names picked.

## The Versions tab

Each publish that stored a version of the process is a row, newest first: `v2 · 20 Oct 2026 · Ana Pop · Tighten KYC`, that is, the version, the day, who published it and the draft's title. Beside it, how many instances run on that version: `3 instances running`, `1 instance running`, or **No instances running**. With no publish, the tab says **Not published yet.**

Press a row to open it:

- **Download v2** saves that version's file as `loan-review-v2.bpmn`.
- **Show the diagram** opens the Diagram tab on that version.
- Under them, what the version changed in the process's file, as its lines: the file before the publish against the file after it, with three unchanged lines beside each change. A version that did not change it says "This version did not change" and the process's name, such as "This version did not change Loan review."

If the publishes cannot be read, the tab says why, in Keel's words, or "The project's publishes could not be read."; if what a version changed cannot, "What this version changed could not be read." Each comes with **Try again**.

## The Connections tab

The tab says: "The connections this process calls, with their credentials. Its connection files are changed in a draft." Each connection of the process shows its **Base URL** and **Authentication**, read-only, as published, and its credentials as the [Connections tab](/keel/builder/connections/#credentials) of a case type shows them:

- **Set credential**, or **Replace credential** when one is set, and **Delete credential**, which asks first. Editors and owners see them; a viewer reads the credentials only. The dialog is **Set the *kind* credential of *connection***, and the page says **Credential set. It is not shown again.**
- Each credential shows its kind, the hosts it is sent to, who set it and when, never its secret.
- A connection with no credential says **No credential is set.**, and one that authenticates with **None**, **It sends no credential.**
- If setting or deleting a credential is refused because your installation keeps no credentials, the tab then says **Credentials are off in this installation.** and removes the credential buttons.

Under them, **Who changed credentials** lists the changes to this process's credentials, newest first, such as "Ana Marin set the API key credential of bureau for bureau.example · 20 Oct, 09:00". With none, "No one has changed a credential of this process yet."

A process with no connection says **This process has no connection yet.** If the connections cannot be read, the tab says why, in Keel's words, or "The connections could not be read.", with **Try again**. A process's connection files are saved in a draft through the API: see [A process's connections](/keel/processes/#a-processs-connections).

## Review and publish

In **What changes** on the [review page](/keel/builder/publish/#review-and-publish), a process's file reads **Process Loan review**: the name the draft's file gives its process, else the name the published file gives it, else the key. Beside it are **Added**, **Changed** or **Removed**, and the file's lines, main's against the draft's. A changed connection file of a process reads **Process connection** and its process and name, such as **Process connection checking/bureau**.

When you open **Review and publish** from a process, the page's link back reads **Back to the process**, and leads to the process in the draft. After the publish, the page that confirms it offers **Back to the process** too, leading to the published process.

## Who can do what

| | Viewer | Editor | Owner |
|---|---|---|---|
| See the list, a drawing, its versions and connections | Yes | Yes | Yes |
| **Download** a file | Yes | Yes | Yes |
| **New process**, **Upload a file**, **Change the diagram** | No | Yes | Yes |
| Change a draft's diagram, and set the process, an element, a flow, a timer, a message or an error in the panel | No | Yes | Yes |
| Read the panel and **Elements** | Yes | Yes | Yes |
| Run the draft's checks, **Dry run**, publish | No | Yes | Yes |
| Set, replace and delete a connection's credential | No | Yes | Yes |

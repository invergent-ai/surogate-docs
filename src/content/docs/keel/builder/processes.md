---
title: Processes
---

The **Processes** page lists the project's [BPMN processes](/keel/processes/): "Upload, check and publish this project's BPMN processes." Press a row to open the process: its drawing, its file, the problems the checks found in it, its versions and its connections.

You cannot model or change a process in Keel Builder yet. Make the file in a modeller such as Camunda Modeler or bpmn.io and upload it here.

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

1. Press **New process**. The dialog says: "Its file is saved in a draft as you upload it. Nothing published changes until the draft is published."
2. Choose the **BPMN file**: "A BPMN 2.0 file from a modeller such as Camunda Modeler or bpmn.io, at most 5,000,000 bytes."
3. Check the **Key**. It fills in from the file: the name the file gives its process, else the process's id, else the file's name without its extension. It is made into a key: lower case, without accents, with each run of other characters as `-`. When a process of the project has that key already, `-2`, `-3` and so on are added. Change it if you need to.
   - A key is letters, digits, `-` and `_`, starting with a letter or a digit. The dialog says so, "A key is letters, digits, - and _, starting with a letter or a digit.", when yours is not.
   - It says "A process has this key already." when you type the key of a published process, or of one the draft you pick holds.
4. Pick the **Draft** to put it in: **A new draft**, or one of the open drafts. A new draft asks for a **Draft title**, which starts as `New process: <the process's name>`, or the key when the file's process has no name.
5. Press **Create**.

Create is turned on once a file is chosen, its key is good, and the draft's processes are read; for a new draft, its title is not empty too. Keel saves the file in the draft exactly as you chose it, and the new process opens in that draft. Nothing published changes until the draft is published.

If the draft cannot be made, the dialog says why, in Keel's words when Keel gave them, else "The draft could not be started. Try again." If Keel refuses the file, the dialog says why, in Keel's words when they are for people, such as "A file is at most 5000000 bytes.", and stays open. Press **Create** again: a draft already made for it is used again, and no second one is made. If the process was saved but cannot be opened, the dialog says "The process could not be opened. Try again."

## A process's page

The page's header shows the process's name and, under it, its published version: for example **Version 2 published 20 Oct 2026 · 3 instances running on it**, or **Not published yet**. While the draft's file is shown, the name is the one that file gives its process. Under the header are a breadcrumb back to **Processes** and the [draft bar](/keel/builder/drafts/), then the tabs:

| Tab | What it holds |
|---|---|
| **Diagram** | The drawing of the file, and in a draft, the problems found in it. |
| **Versions** | Every published version, what each changed, and its file. |
| **Connections** | The connections the process calls, and their credentials. |

On the right of the header, everyone sees **Download**. Editors and owners also see **Upload a file**, and in a draft, **Dry run** and **Review and publish**. See [Dry run and publish](/keel/builder/publish/).

On the Diagram tab, a process that is not published, opened with no draft or in a draft that has no file for it, says **This process is not here**: "Open it in the draft that holds it." A draft that has no file for a published process says **The draft has no file for this process.**

### Upload a file

**Upload a file** puts a BPMN file in the draft as this process's file. It is kept exactly as you chose it, down to its bytes: Keel Builder does not read it or change it first.

With no draft open, Keel Builder asks for one first: the **Start a draft** dialog offers a **Title**, such as `Change Loan review`. Press **Start draft**, and the file is saved in the new draft. Cancel, and nothing is uploaded.

Once the file is saved, a message says `Uploaded loan-review.bpmn.` with the file's name, and the page shows the draft's file, on the Diagram tab even when you uploaded from another tab. If Keel refuses the file, a message says why, in Keel's words when they are for people, and the page stays as it was. A file you choose while another is on its way waits for it.

### Download

**Download** saves the file the page shows, as Keel has it, byte for byte. In a draft it is the draft's file, saved as `<key>.bpmn`. For a published version it is that version's file, saved as `<key>-v<version>.bpmn`, such as `loan-review-v2.bpmn`. A file Keel Builder cannot draw downloads like any other. If Keel refuses, a message says why and nothing is saved.

## The Diagram tab

The tab draws the file as the modeller laid it out. Drag the drawing to move it. The mouse wheel moves it up and down, and with Shift sideways. Hold Ctrl (⌘ on a Mac) while you turn the wheel, or pinch on a touchpad, to zoom. It opens fitted to the tab and centred. On a phone the tab is shorter: drag with one finger to move the drawing, pinch with two to zoom it, and touch outside the drawing to scroll the page.

The tab shows the file of the draft when a draft is open, else the current published version. When it shows a published version in a draft, or a version that is not the current one, `Version 2, as published.` says so, with **Show the draft's file** in a draft, or **Show the current version** when the version is not the current one.

In place of a drawing, the tab says why there is none:

- **This file cannot be read as a BPMN 2.0 file.** The file is not well-formed XML, or is not a BPMN 2.0 file.
- **This process's file has no diagram layout.** The file has no diagram, so there is nothing to draw.
- **This file could not be drawn.** The drawing could not make sense of the file.

If the file cannot be read from Keel, the tab shows Keel's words, or "The process's file could not be read.", with **Try again**. The page does the same when it cannot read the project's processes, "The project's processes could not be read.", or the draft, in Keel's words.

### Problems

In a draft, the drawing has a **Problems** section beside it, with how many problems the checks found in this process. It lists what the checks found in this process: the problems in its file, and those Keel placed at it, such as one in its connection file. Problems in other files, such as a case type, are not listed.

The checks run by themselves. Editors and owners need not press **Dry run**: opening the draft's file checks the draft, unless it was checked already as it is now, and when the draft changes, as it does after an upload or **Load the latest**, it is checked again. While it runs, the section says **Checking the draft…** A viewer reads "Only the project's editors and owners run the draft's checks." and no check is run.

Each problem shows:

- **Error**, which stops a publish, or **Warning**, which does not, such as a vendor's setting Keel ignores;
- Keel's message;
- its place. A problem at an element of the drawing names it, such as **Score the applicant · Script task**: its name, else its id, then its type. Press it to pick the element. A problem at the process reads **The process**. A problem at an element the drawing does not draw, such as **Documents · Message**, at a place Keel names in its own words, or in another file of the process, is listed but is not a button. A problem in another file of the process names that file, such as `bureau · Process connection checking/bureau` for a connection file.

The drawing marks the elements the problems name: an element with an error has a red outline and a red glow, one with only a warning an amber outline and glow. The element you picked has a glow of its own, and the drawing moves to it.

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
| **New process**, **Upload a file** | No | Yes | Yes |
| Run the draft's checks, **Dry run**, publish | No | Yes | Yes |
| Set, replace and delete a connection's credential | No | Yes | Yes |

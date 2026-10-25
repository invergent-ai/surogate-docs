---
title: Office documents
---

Word documents, spreadsheets, presentations and PDFs in an agent's workspace open in an office editor beside the chat. Everyone with a document open edits it together, and the agent can work in the same document live: each change it makes appears under its name.

This page is the reference. For step-by-step tasks, see [Work with documents](/work/workflow/work-with-documents/).

If an office file in the chat offers only a download, with *Preview not available. Download the file to open it.*, the editor is not available on this platform: ask your administrator.

## Opening a document

Open **Files** above the composer to see the chat's workspace, and click a file, or click a file the conversation names. It opens in the editor in the file pane beside the chat, in your light or dark theme. The editor is the same in Studio's Work chat, in the agent's own web app and in [Surogate Desktop](/work/desktop/overview/).

| Files | In the editor |
|---|---|
| `.docx`, `.xlsx`, `.pptx`, `.pdf` | Open for editing |
| `.doc`, `.odt`, `.rtf`, `.xls`, `.ods`, `.ppt`, `.odp` | Open read-only (the editor converts them to show them) |

A document also opens read-only when the chat is read-only: a scheduled run's conversation, or a chat you can read but not write in.

Documents in a folder on a computer connected through Surogate Desktop open too. Your saves land on the computer, and wait there if it is offline or has not yet allowed the save. A file over 50 MB on a computer does not open in the pane: open it from its folder on the computer instead.

### The file pane

| Control | What it does |
|---|---|
| **Download** | Downloads the file as the workspace holds it, that is, as of its last save |
| **Full screen** | Fills the screen with the pane. **Exit full screen** or Esc leaves it |
| **Close file** | Closes the pane. A document you close stays closed while the agent goes on editing it |

Downloading and printing are also allowed from the editor's own menus. Notices about saves appear under the pane's header (see [Save notices](#save-notices)).

## Editing and saving

What you type is saved back into the workspace file as you work: you don't press Save. A document the agent edited is saved when its turn ends.

Everyone with the document open sees each other's edits as they happen, each under their own name.

While a document is open in the editor, the editor is the only thing that writes it. The agent changes it through its editor session; a file write to it with `write_file` or `patch` is refused. If the file changed some other way meanwhile, for example on the computer it lives on, your edits are not lost: they are saved to a copy beside it, named like `report (edited 2026-10-25 14.30 UTC).docx`, and the editor reopens the file as it now is.

### Save notices

A notice about a file on a computer names the computer; the table writes *your computer* in its place.

| Notice | What it means |
|---|---|
| *This document changed outside the editor. Your edits were saved to …* | The file changed while it was open. Your edits are in the copy the notice names. |
| *Your latest changes could not be saved yet.* | A save failed. Your edits are still in the editor, and the save is tried again. |
| *Saving to your computer once it is back online.* | The file is on a computer that is offline. The save lands when it is back. |
| *Saving to your computer… If it asks, allow the save there.* | The computer's user is asked to allow the save in Surogate Desktop. |
| *Your computer declined the save. Your changes are still here; the next save asks again.* | The computer's user said no to this save. |
| *The document is still being saved; try again in a moment.* | The document's last save is still landing. Open it again in a few seconds. |

The same moments are recorded in the session's events as `office.conflict`, `office.save_failed`, `office.save_waiting` and `office.saved` (see [Event types](/develop/reference/event-types/)).

## What the agent can do live

In a Word document (`.docx`), spreadsheet (`.xlsx`), presentation (`.pptx`) or PDF (`.pdf`), the agent works through its own editor session, alongside you:

- **`office_read`** reads the document as it stands, with everyone's latest edits: an outline of its blocks (a spreadsheet's sheets, a presentation's slides, a PDF's pages and form fields), one block, range, slide or page in full, or a search for words. It also gives the comment threads, in Word the tracked changes by author, and who else has the document open.
- **`office_edit`** changes the document, or creates it: a missing `.docx`, `.xlsx`, `.pptx` or `.pdf` is created blank and opens in your pane.

| Document | What `office_edit` does |
|---|---|
| Word | Inserts, replaces, deletes and moves blocks, and re-words quoted text keeping its formatting. Headings, lists and tables use the document's own styles. Adds charts (bar, column, line, pie and more) and pictures from the workspace, and plants placeholder sections that say what will go there, then fills them one by one. Adds comments. |
| Spreadsheet | Sets cells and live formulas, formats ranges, adds charts (column, bar, line, pie, area, doughnut, scatter), and adds, renames or deletes sheets. |
| Presentation | Adds or rebuilds whole slides, built as native shapes you can edit; changes one shape's text and keeps its place and style; sets speaker notes; reorders and removes slides. |
| PDF | Fills form fields, adds text or checkbox fields, adds, removes or rotates pages, places notes or stamps, and redacts text. |
| Comments | Replies to and resolves comment threads, in every type. Only in Word does it start a new comment. |

When the agent edits a document, it opens beside the chat by itself, once per document, unless you are looking at another file; on a phone the chat stays in view. Each call's changes appear whole, under the agent's name, and the agent says a short line in the chat between calls. In **Simple** view a call shows as *Edited report.docx*.

### Rules and limits

- **Your edits win.** All the changes in one call apply together or not at all. If you changed the part the agent was about to edit, nothing applies: the agent reads the document again and works from your version.
- **Time.** An edit can take up to five minutes (a deck's slides are measured first). One that times out may still have applied, and the agent is told to read the document again.
- **Pictures** come from the workspace: PNG or JPEG up to 5 MB each, SVG too on slides, and at most 12 MB in one call.
- **Slides** don't shrink to fit. A slide whose text does not fit its boxes is refused, and the agent splits it over two slides.
- **PDFs.** A PDF's existing text cannot be changed. A redaction is permanent once the document is saved. A new PDF with content, and merging, splitting or encrypting PDFs, are done with the `pdf` skill, as a new file (see [Files the agent builds with scripts](#files-the-agent-builds-with-scripts)).
- **Protected Word documents.** A document protected with Restrict Editing, in Word or in the editor, refuses the agent's edits. Only you can lift the protection.
- **Busy.** If the platform has as many documents open for agents as it can hold, the agent is told *The office service has as many documents open as it can hold; try again in a minute.*
- **Idle sessions.** The agent's editor session on a document closes after 10 minutes without a call, and the agent leaves the document's list of editors.

### Where the agent edits live

The agent has `office_read` and `office_edit` only in a chat that shows documents beside it:

- the web chat, Studio's Work chat and Surogate Desktop, including a chat on a folder of your computer;
- a project's threads. `office_edit` reaches the project's real document, never a thread's copy;
- a chat your own app creates through the API with `"config": {"file_pane": true}` (see [Show the workspace and editor in your own app](/develop/features/sessions/#show-the-workspace-and-editor-in-your-own-app)).

The agent does not have them on Slack, Telegram, WhatsApp, Discord, Teams or a phone call, in the website widget, in a chat your app creates through the API without `file_pane`, in a project's coordinator or a `/mission` chat, or when the agent uses an allowed-tools list (the two tools can't be named in it). There it builds files with scripts instead.

### Tracked changes

In Word, turn on track changes for everyone (in the editor's **Collaboration** tab, **Track Changes**, *ON for me and everyone*) and the agent's edits arrive as tracked changes under its name, for you to accept or reject. `office_read` reports how many tracked changes each author has.

## Comment mentions

In a Word document, spreadsheet, presentation or PDF open in the file pane, type `@` in a comment or a reply and pick the agent from the list. The comment shows the agent's address, which ends in `@agent.invalid`; no mail is ever sent to it.

1. The mention reaches the chat as your message, quoting the comment and naming the file.
2. The agent posts *On it, I'll reply here when done.* in the comment's thread.
3. It does the work with `office_read` and `office_edit`.
4. It replies in the thread with the result only, in one or two sentences (at most 400 characters), and resolves the thread. Its reasoning stays in the chat.

If the agent cannot do what the comment asks, it says why in the thread and leaves it open.

The agent is offered in the mention list only in a chat where it has the office tools, and only in a document you can edit. Mentions work in Studio's Work chat as in the agent's own web app. A mention never answers a question the agent is waiting on in the chat. If a mention cannot reach the chat, the pane says *The agent was not told about your comment: …* with the reason.

## Templates for new files

When the agent creates a new Word document, spreadsheet or presentation, it starts from a template of the kind you asked for instead of a blank page:

| Type | Templates |
|---|---|
| Word | Report, letter, meeting minutes, proposal, FAQ, how-to guide |
| Spreadsheet | Budget, invoice, tracker |
| Presentation | Slide kinds: title, statement, big number, cards, table, chart, timeline, closing. Deck outlines for a pitch, an onboarding and a review, used when you don't list the slides |

The agent adapts the sections to your request. It drafts what you asked for but did not detail as a proposal and says so in the chat, for you to check. It leaves out names, dates, figures and other specifics you did not give it; a section that needs them comes out shorter. A spreadsheet template's sample rows go in only when you gave no rows, and the agent says in the chat that they are samples. A new PDF is created blank.

You do not pick a template yourself: ask the agent for the kind of document you want.

## Files the agent builds with scripts

Where the agent has no live editor tools, it still makes and changes office files, with built-in skills and scripts in its sandbox. The result is a file in the workspace, which the agent hands you when it is done; you don't watch it being built or edit it alongside the agent.

| Skill | What it covers | Offered |
|---|---|---|
| `office` | Drafting, filling, editing and commenting on documents live with `office_edit` | Only where the agent has `office_edit` |
| `docx`, `xlsx`, `pptx` | Building and changing Word documents, spreadsheets and decks with scripts | Only where the agent does not have `office_edit` |
| `pdf-forms` | Filling in a PDF form, adding notes, redacting, and adding, removing or rotating pages, with scripts | Only where the agent does not have `office_edit` |
| `pdf` | Creating a PDF with content, merging, splitting, watermarking, encrypting and decrypting, extracting tables or images, OCR of a scanned PDF | Always |
| `pdf-reading` | Reading a PDF that `read_file` cannot read well: figures, layout, attachments, form values | Always |

Where it has `office_edit`, the agent makes and changes `.docx`, `.xlsx` and `.pptx` files only through it, so that you can watch and edit, and a `write_file` or `patch` to a `.docx`, `.xlsx`, `.pptx` or `.pdf` is refused, whether it is open or not. Reading any of them with `read_file` still works.

## What's next

- [Work with documents](/work/workflow/work-with-documents/): the tasks, step by step.
- [Run an agent](/work/workflow/run-agent/): the chat and its workspace.
- [Tool catalog](/develop/reference/tool-catalog/#office-documents): `office_read` and `office_edit`.

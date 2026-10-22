---
title: Office documents
---

Word documents, spreadsheets, presentations and PDFs in an agent's workspace open in a full office editor right beside the chat. You can edit them there, and the agent can write into a Word document, spreadsheet, presentation or PDF live while you watch, each change appearing under its name.

The editor needs a document server on your platform (see [Self-hosted platforms](#self-hosted-platforms)). Without one, an office file in the workspace pane offers only a download: *Preview not available. Download the file to open it.*

## Opening a document

Click an office file in the [workspace pane](/work/workflow/run-agent/#the-workspace-pane) (in **Advanced** chat mode, or wherever the pane is shown): it opens in the editor in the file pane, in your light or dark theme. The pane's header has **Download**, **Full screen** (Esc leaves it) and **Close file**. The same editor opens in Studio's chat and in the agent's own web app.

| Files | In the editor |
|---|---|
| `.docx`, `.xlsx`, `.pptx`, `.pdf` | Open for editing |
| `.doc`, `.odt`, `.rtf`, `.xls`, `.ods`, `.ppt`, `.odp` | Open read-only (the editor converts them to show them) |

A document also opens read-only when the chat itself is read-only, and in a scheduled run's conversation. Documents in a folder on a computer connected through Surogate Desktop open too; your saves land on the computer, and wait there if it is offline or has not yet allowed the save.

## Editing and saving

What you type is saved back into the workspace file: the editor saves as you work, and a document the agent edited is saved when its turn ends. Everyone with the document open sees each other's edits as they happen; you appear under your own name.

While a document is open in the editor, the editor is the only thing that writes it. If the file changed some other way meanwhile, your edits are not lost: the pane says *This document changed outside the editor. Your edits were saved to …* with the name of the copy. *Your latest changes could not be saved yet.* means a save is still pending.

## What the agent can do live

In a Word document (`.docx`), spreadsheet (`.xlsx`), presentation (`.pptx`) or PDF (`.pdf`), the agent works through its own editor session, alongside you:

- **`office_read`** reads the document as it stands, with everyone's latest edits: an outline of its blocks (a spreadsheet's sheets, a presentation's slides, a PDF's pages), one block, range, slide or page in full, or a search for words, plus its comment threads and, in Word, tracked changes, and who else has it open.
- **`office_edit`** changes it. In Word, headings, lists and tables use the document's own styles.
  - Word: insert, replace, re-word in place keeping the formatting, delete or move blocks, and add comments. It can also add charts (bar, column, line, pie and more) and images from the workspace, and plant placeholder sections that say what will go there before filling them in one by one.
  - Spreadsheet: sets cells, formulas and formats, adds charts and manages sheets.
  - Presentation: writes slides and speaker notes.
  - PDF: fills form fields, adds, removes or rotates pages, places notes or stamps and redacts text. It cannot change a PDF's existing text.
  - Comments: in the other types, reply to and resolve existing threads only.

When the agent edits a document, it opens beside the chat by itself, unless you are looking at another file; on a phone the chat stays in view. Each call's changes appear whole, under the agent's name, and the agent says a short line in the chat between calls. A missing `.docx`, `.xlsx`, `.pptx` or `.pdf` is created blank.

Your edits win. All the changes in one call apply together or not at all, and if you changed the part the agent was about to edit, nothing applies: the agent reads the document again and works from your version. An edit gets two minutes; one that times out may still have applied, and the agent is told so.

## Comment mentions

In a Word document, spreadsheet, presentation or PDF open in the file pane, type the agent's name after `@` in a comment (or a reply) to call it. The mention reaches the chat as your message, quoting the comment. The agent answers in that comment's thread, and resolves the thread when it is done. The agent is offered in the mention list only in a chat where it has the office tools, and only in a document you can edit. A mention never answers a question the agent is waiting on in the chat.

## Templates for new files

When the agent creates a new Word document, spreadsheet or presentation, it follows a template of the kind you asked for instead of starting from a blank page. Word has report, letter, meeting minutes, proposal, FAQ and how-to guide; spreadsheets have budget, invoice and tracker; presentations have slide layouts (title, statement, big number, cards, table, chart, timeline, closing). The agent adapts the sections to your request and drafts what you describe, but leaves out names, dates and figures you did not give it. A new PDF is created blank. You do not pick a template yourself; ask the agent for the kind of document you want.

## Self-hosted platforms

The editor is the Euro-Office document server, installed with the `charts/office` Helm chart from the surogate-ops repository (the document server, its converters and RabbitMQ; it needs its own Postgres database and an S3-compatible bucket for its file cache). The agent runtime is pointed at it with the `SUROGATES_OFFICE_*` settings, and shares its JWT secret.

Live editing by the agent needs one more service beside it, `runtime-office`, which runs the agent's editor sessions in a headless browser (each open document takes roughly 0.5–0.7 GB). Without it, people can still open and edit documents, but `office_read` and `office_edit` do not exist. Open documents are stored back at least every 5 minutes, so the stored file lags the live one by at most that.

## What's next

- [Run an agent](/work/workflow/run-agent/) — the chat and its workspace pane.
- [Tool catalog](/develop/reference/tool-catalog/) — every tool the agent can call.

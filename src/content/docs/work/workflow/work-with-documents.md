---
title: Work with documents
---

You can work on Word documents, spreadsheets, presentations and PDFs together with your agent, right in the chat. The document opens beside the conversation, the agent writes into it while you watch, and you can edit, comment and ask for changes as you would with a colleague.

This page walks through the common tasks. For what each part does in detail, see [Office documents](/work/tools/office-documents/).

## What you need

- A chat in Studio's Work chat, the agent's own web app or [Surogate Desktop](/work/desktop/overview/).
- The document editor on your platform. If an office file only offers a download, with *Preview not available. Download the file to open it.*, the editor is not available on this platform: ask your administrator.

On Slack, Telegram, WhatsApp, Discord, Teams, a phone call or the website widget there is no document pane. The agent still makes and changes documents there, with scripts, and sends you the finished file (see [Files the agent builds with scripts](/work/tools/office-documents/#files-the-agent-builds-with-scripts)).

## Open a document

1. In the chat, open **Files** above the composer.
2. Click the document. It opens in the editor beside the chat.

To bring in a document of your own, click **Upload files** on the **Files** tab, or attach it with **Add** (`+`) in the composer. A file the agent names in the conversation opens with a click too.

`.docx`, `.xlsx`, `.pptx` and `.pdf` files open for editing. Older formats (`.doc`, `.xls`, `.ppt`, `.rtf` and OpenDocument files) open read-only.

## Ask the agent for a new document

1. Say what you want, the kind of document and, if it matters, the file name and length:

   > Draft a two-page project proposal in proposal.docx for moving our support team to a four-day week. The team is 12 people, the pilot starts on 2 March and runs for three months.

2. The agent creates the file, and it opens beside the chat. It starts from a template of that kind (a report, a proposal, a budget, a pitch deck and so on) and fills one section, block of cells or slide at a time.
3. When it is done, the agent says in one line what it did and what it drafted for you to check.

Give the agent the facts: names, dates, figures. It does not make up specifics you did not give, so a section that needs them comes out shorter. A part you asked for but did not detail, such as the steps of a plan, it drafts as a proposal and tells you so. A new spreadsheet gets sample rows only when you gave no rows, and the agent says they are samples.

## Watch and steer the agent's edits

- Each edit appears whole, under the agent's name. Between edits, the agent writes a short line in the chat, such as *Building the pricing slide.*
- The document opens by itself on the agent's first edit, unless you are looking at another file. If you close it, it stays closed while the agent goes on.
- To change course, press **Stop** while the agent works, then send your correction. The edits it already made stay in the document.
- You can also steer from inside the document: change it yourself, or leave a comment that mentions the agent (see below).

## Edit alongside the agent

1. Click into the document and type, as in any office editor. Your edits appear for the agent and everyone else at once, under your name.
2. Keep going while the agent works. If you change the part it was about to change, your version stays: the agent reads the document again and works from yours.

Your edits save as you work. If you are editing the very cells or slide the agent wants to change, it waits or asks you, so work on another part while it finishes that piece.

## Comment and mention the agent

1. Add a comment on the words, cell, slide or page you want changed.
2. In the comment, type `@` and pick the agent from the list. The comment shows its address, which ends in `@agent.invalid`.
3. After the address, write what you want, for example *shorten this paragraph to two sentences and keep the figures*, and post the comment.
4. The agent posts *On it, I'll reply here when done.* in the thread, and your comment appears in the chat as your message.
5. When it is done, the agent replies in the thread with the result and resolves the thread. If it cannot do it, it says why and leaves the thread open.

You can mention the agent in a reply in an existing thread too. The agent is in the list only in a document you can edit, in a chat where it can edit documents live.

## Review the agent's changes in Word

- **Track its changes.** Before you ask for changes, open the editor's **Collaboration** tab and set **Track Changes** to *ON for me and everyone*. Each edit the agent makes then shows as a tracked change under its name. Accept or reject them in the same tab.
- **Ask for comments instead of edits.** For example: *Read section 3 and comment wherever a figure disagrees with budget.xlsx.* The agent adds comment threads on the words they are about, and you decide what to change.
- **Read its replies.** The agent's answers in comment threads state only the result. Its reasoning is in the chat.

## Fill in a PDF form

1. Upload the PDF, or attach it to your message.
2. Open it from **Files**.
3. Ask the agent to fill it, and give it the answers:

   > Fill in forms/application.pdf: full name Ana Silva, start date 2 March 2027, department Support, and tick "I agree".

4. Check the fields in the editor, and correct any yourself.

The agent fills the form's own fields, and ticks or clears checkboxes. A form with no fields to fill can get new text or checkbox fields where you need them. The agent cannot change a PDF's existing text. A redaction removes the text for good once the document is saved.

## Download or open full screen

The file pane's header has three buttons:

- **Download** saves the file as the workspace holds it, that is, as of its last save.
- **Full screen** fills the screen with the document. Press Esc or **Exit full screen** to leave it.
- **Close file** closes the pane.

## When a save is pending or the file changed

| You see | What to do |
|---|---|
| *Your latest changes could not be saved yet.* | Nothing at once: your edits are still in the editor, and the save is tried again. Keep the document open. If the notice stays, tell your administrator. |
| *Saving to your computer once it is back online.* | The file is on a computer that is offline. Start Surogate Desktop on it; the save lands when it is back. |
| *Saving to your computer… If it asks, allow the save there.* | Allow the save in Surogate Desktop on that computer. |
| *This document changed outside the editor. Your edits were saved to …* | The file changed some other way while it was open, for example in another app on your computer. Your edits are in the copy the notice names, beside the original, and the editor now shows the original as it is. Compare the two and keep what you need. |
| *The document is still being saved; try again in a moment.* | Wait a few seconds and open it again. |
| *The agent was not told about your comment: …* | The mention did not reach the chat. Check the reason, then post the comment again or ask in the chat. |

## Prompts that work well

- *Write a one-page summary of meeting-notes.md in summary.docx, with the decisions first.*
- *Make a budget in offsite-budget.xlsx for a three-day offsite for 20 people: venue 4,000, catering 45 per person per day, travel 6,000. Totals as formulas.*
- *Build a six-slide deck in decks/q3-review.pptx reviewing Q3 from the figures in q3.xlsx. One chart, and a closing slide with the two decisions we need.*
- *In sales.xlsx, add a Total column and a column chart of the totals by region.*
- *In proposal.docx, shorten the Background section to 150 words and keep every figure.*
- *Go through contract.docx and comment wherever a date or amount differs from terms.xlsx. Don't change the text.*
- *In decks/q3-review.pptx, change the title of slide 4 to "The North brings a third of all orders".*

Name the file, give the facts, and say the length or the number of slides when it matters.

## What's next

- [Office documents](/work/tools/office-documents/): the reference for the editor, the agent's tools, mentions, templates and the skills it uses without the editor.
- [Run an agent](/work/workflow/run-agent/): the chat and its workspace.

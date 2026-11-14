---
title: Actions
description: Lists of actions that run when something happens, such as a form being sent; values worked out with CEL expressions.
---

An action list is a short program of the portal's. It runs when something happens. For now that is a form being sent ([After it is sent](/portal/sites/forms/#after-it-is-sent)), or a [logic flow](/portal/sites/flows/) being called; later, endpoints and scheduled jobs run them too. Each action does one thing: works out a value, logs a line, tells the person something, sends them elsewhere.

The console does not edit action lists yet. For now, this is set in the site's configuration: see [Developer: Actions](/portal/developer/actions/).

## What people see

A person who sends a form sees what its actions tell them. Here a resident has filed a building permit request. The form's actions worked out the fee with a [logic flow](/portal/sites/flows/), gave the request a number, kept it as a record, and told the person:

![A building permit request after it was sent: a green notice, "Request CAS-2026 was registered. Estimated fee: 1020 lei.", and under it the message with the request's number and the fee.](../../../../assets/screenshots/portal-request-sent.png)

- The notice at the top comes from a notice action ([UI actions](#ui-actions)). The text under it comes from a message action, which tells the person something and ends the run.
- A notice or a message can put in a value an earlier action set: here the request's number and the fee.
- A redirect action would have sent the person to another page instead.

**In the console,** the form's reviewers see each run of its actions under **Runs** on [Forms](/portal/console/forms/#runs): when it ran and whether it is done, failed or waiting.

![The Forms page with Runs open: the last run of the Building permit request form, marked Done, above the request that started it.](../../../../assets/screenshots/portal-forms-runs.png)

## An action list

A form has an action list for the moment it is sent and kept; a flow, a job and an endpoint have lists of their own. Every action does one kind of thing, and may also have:
- a note, for whoever reads the list;
- a condition: an expression that must be true for the action to run;
- actions run after it succeeds;
- actions run when it fails; the list then goes on;
- a stop: the run ends after this action. A message or a redirect, which ends the run, can be let go on instead;
- an error message: what the person is told if the run fails at this action, in each language.

## Expressions

Values are worked out with [CEL](https://cel.dev), the expression language Keel uses too. An expression can read:
- what was sent, by the field's key;
- the submission's id;
- the person who sent it (id, name, email and roles), or nothing for a visitor;
- the site and the language;
- when the run started;
- the values earlier actions set;
- the portal's [named values](/portal/sites/values/).

Whole numbers are integers, the others decimals; the two mix in arithmetic, so a price times 1.19 works whatever was typed. Reading a field that was not sent is an error: check first that it was sent. Reading a name that is not one of these is refused when the configuration is saved. Beside CEL's own functions there are functions to replace text, to encode text for an address, to take a slice of a list or text, to sort a list, and to round a number, or round it down or up.

## The actions

Extensions add more: the [document actions](/portal/sites/document-actions/) make and read PDF, Word, Excel and CSV files and barcode images, and the [file management actions](/portal/sites/file-management/) copy, move and rename files and make and unpack ZIP archives.

- Work out values, and keep them for later actions.
- Run actions together: an error handler of the group catches theirs.
- Run actions for each item of a list, or a number of times.
- Fail with a message.
- End the run.
- Write a line in the run's log, as information or as a warning.
- Wait up to 5 seconds.
- Read JSON text into a value, or write a value as JSON text.
- Tell the person something, in each language, and end the run. The text can put in a value an action set.
- Send the person to another page, and end the run.
- Run a [logic flow](/portal/sites/flows/#call-a-flow) and keep its outputs.
- Run one of the portal's [endpoints](/portal/sites/endpoints/#private-endpoints) and keep its answer.
- Run an [app's action](#app-actions) and keep its outputs.
- Start a case or process in [Keel](/portal/sites/keel/#start-cases-from-the-portal), or send it a message or signal.
- Ask one of your [agents](/portal/sites/assistants/) for an answer, a summary or a knowledge-base article, and keep it.
- Call a service through a [connector](/portal/sites/connectors/#call-a-service).
- Send a [text message](/portal/sites/connectors/#text-messages-and-slack) through Twilio or Clickatell once the run ends well.
- Post to a [Slack channel](/portal/sites/connectors/#text-messages-and-slack) once the run ends well.
- Send an [email](/portal/sites/connectors/#email) once the run ends well, through the portal's mail server or [your own mail account](/portal/sites/connectors/#mail-accounts), with files.
- Send a [notification](/portal/sites/notifications/) to people of the portal once the run ends well.
- Make [hashes, signatures and random values](/portal/sites/connectors/#hashes-signatures-and-random-values).
- List a [folder](#files)'s files, read a file, write a file (a [signature](/portal/sites/form-fields/#save-a-signature-as-a-file) too), and delete a file.

A redirect goes to a page of the same site, or to another https site the form names.

## Ask an agent

An action can ask one of the agents connected to the portal (an agent with its key: see [Assistants](/portal/sites/assistants/)) and keep the answer. Only a [job](/portal/sites/jobs/) asks an agent: an agent's answer takes longer than a form, an endpoint or a [flow](/portal/sites/flows/) waits. To summarize what a form receives, have the form create a record, and ask the agent from a job that starts when that record is created.

- The task is to answer the prompt (when left out), to summarize it, or to write a knowledge-base article from it, with a title and sections. The answer comes in the prompt's language.
- The prompt is an expression giving the words, up to 50,000 characters.
- The answer is kept as text, for later actions.

Each ask is a conversation of its own, and its use is billed to the agent's project. A run asks agents at most 5 times. It waits at most 90 seconds for an answer, and stops waiting ten seconds before the run's own time is up, so that an error handler can still run. An answer is at most 256 KB. When the agent cannot answer, or stops to ask a question of its own, the run fails there, and an error handler sees why. A failed run is not run again.

## Files

The file actions work on one of the portal's [folders](/portal/console/files/#folders).

- **Who may do what:**
  - Someone who edits the folder does what they could under Files in the console.
  - Anyone else, a visitor too, may only make a new file, and never in a public folder. A file of the same name already there makes the action fail.
- **Names:** a file's name is lower-case letters, digits, dots, `-` and `_`, with an extension the portal keeps.
- **Limits:**
  - a file is at most 700 KB;
  - a run reads at most 50 times and changes files at most 20 times;
  - a listing gives at most 1,000 names.

A file written stays written, even if a later action fails.

## Records

These actions work on the records of a [data model](/portal/sites/data-models/). They act as the person whose run it is, a visitor too, with the model's permissions.

- Add a record.
- Change the fields given.
- Delete a record.
- Read one record.
- Find records by filterable fields, in an order, at most 100.

Each change is made at once: when a later action fails, what was changed stays. A run makes at most 20 changes and 50 reads. A [named value](/portal/sites/values/) never reaches records. A flow's test uses its own records, which the test lists by model.

## UI actions

A form's actions can tell the page what to do once everything else is done. These do not end the run, and at most 10 count:

- Show a notice above the thanks, with its text in each language and a tone: information, success or warning. The text can put in a value an action set.
- Start a [user guide](/portal/sites/guides/) that applies to this page.
- Reload the page after a moment.

A redirect wins over them: the person goes elsewhere first. A form sent again answers what it answered the first time; one sent from an offline device shows none of them.

## When something fails

An action that fails runs its error handler actions, and the list goes on. Without them, the failure goes up to the enclosing group's error handler, and otherwise ends the run. Inside an error handler, the error's message says what went wrong.

A run stops after 10 seconds or 10,000 steps, a loop goes over at most 1,000 items, and a value is at most 1 MB. When the portal is very busy, a run may not start; the form is still kept, and the person is told that what follows could not be done. Each run is kept for 30 days, with its log; reviewers see them under **Runs** on [Forms](/portal/console/forms/#runs).

## App actions

An approved app can give actions of its own, such as sending an SMS.

- **What it takes:** the inputs the app's manifest declares; the portal checks them when the files are published. A connector of the app's type, when the action needs one: an administrator sets its credentials under **Connectors**.
- **What it gives:** the action's outputs, kept for later actions.
- **Where:** in a form, flow, job or endpoint that may change records, never in a GET endpoint or one anyone may call, and never in a flow's tests. A run calls at most 10.
- **When it fails:** the app is not approved, it does not answer in time, or it answers what its manifest does not say. The run's error handler reads why.

To write one, see [Build an app](/portal/developer/build-an-app/#actions).

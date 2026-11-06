---
title: Surogate DMS FAQ
sidebar:
  label: FAQ
---

Answers to the questions the DMS's messages and empty screens raise.

## Signing in and seeing documents

### I signed in and I see no folder
Your account exists but nobody has given you a role yet, or the role does not reach the folder. Ask your administrator for a grant. See [Roles and permissions](/dms/admin/roles/).

### Why is Upload missing?
The **Upload** button shows only in folders where you may file documents, and not in a closed dosar. **Import** under **Bring in** shows only to people who may file documents.

### Why is a page missing from my sidebar?
The sidebar lists only the pages your roles allow. See [Sign in and find your way](/dms/work/sign-in/).

### The sign-in page says my account is deactivated
An administrator deactivated it. Ask them to reactivate it. The other sign-in messages are in [Sign in and find your way](/dms/work/sign-in/).

## Working with documents

### Why can I not validate this document?
A document needs a type and its required fields before it can be validated. The page says what is missing.

### Why can I not edit or add a version?
A document can be edited only while it is a draft or validated, and not while someone else has it checked out. See [The life of a document](/dms/work/lifecycle/).

### Why can I not archive this document?
Archiving needs the permission to archive, and the document's file must have passed its reception. A document that failed shows **Not accepted** and its **Archive** tab says why; an electronic archivist can accept it into the archive with a written reason.

### Why does a document ask me for a reason?
It holds a category of personal data that asks for a reason for access. The reason goes into the audit log. See [Personal data](/dms/work/personal-data/).

### Why do I not see a document in a search or a collection?
You see only documents you may read. Documents with personal data need the permission **Access to documents with personal data**.

## The registry

### I do not see the Registry section
The section shows when you hold at least one of the permissions **Sees registrations**, **Registers documents**, **Cancels registrations** or **Manages the registers**. Ask your administrator for a grant. See [Registers and address lists](/dms/admin/registers/).

### Can I change a registration number?
No. A number never changes and is never given to another registration, even when the registration is cancelled. When the kind, the register or the type is wrong, cancel the registration and register it again. See [Registering documents](/dms/work/registry/).

### Why does **Download with the number** give a message?
Only a PDF that is not encrypted and has no signatures gets a numbered copy, because the stamp on the first page would break a signature. Download the original and the receipt instead.

### Where do I see what is addressed to my unit?
In **Registry** › **For my unit**. It lists the registrations addressed to the units where you hold a position in the org chart. See [Finding registrations](/dms/work/registry-lists/).

## Capture

### I do not see the Capture section
**New capture** and **My captures** show when you hold **Uploads documents** somewhere, or **Process captures**. **To process**, **To validate** and **Separator sheets** show when you hold **Process captures**. Ask your administrator for a grant. See [Capturing documents](/dms/work/capture/).

### Why is To process empty or missing?
It lists the captures of the channels of the units where you hold **Process captures** and **Access to documents with personal data** both. Ask your administrator for both in the unit of the channel. **To process** also lists the captures you sent or printed yourself, and **My captures** lists only those.

### Why did my scan not split?
A PDF that carries a signature or is password protected is never cut. A sheet of a profile that was switched off stops the capture and says so. A channel with **Separators** off reads the sheets and cuts nothing. See [Separator sheets and registration labels](/dms/admin/separator-sheets/).

### Why does a capture wait?
A sentence on the capture says what is wrong and what to do. See [Processing captures](/dms/work/capture-inbox/#when-a-capture-waits).

### Where are the captures of my printer?
In **Capture** › **My captures**. A unit's printer sends its captures to **To process** instead.

## What the DMS does not do

The DMS does not offer these:

- editing the older Office formats (`.doc`, `.xls`, `.ppt`, `.odt`) in the browser, two people editing one file at once, and printing from the viewer;
- deleting a single document: a document can be archived, and dosare are deleted together after a selection;
- following a document, and sending or sharing a document by link or by e-mail;
- approval workflows of its own (a flow that spans people and systems runs in Keel: see [Workflows and cases with Keel](/dms/work/workflows/));
- scanning from the program of a scanner on your computer (TWAIN and WIA), printing labels in the language of a label printer (the DMS makes PDFs), and printing to the DMS printer from a phone (photograph the pages with **New capture** instead);
- creating accounts, setting passwords or a second factor: sign-in belongs to your institution's sign-in service.

## Pages for IT teams

The page **API integration** under **Administration** is for the IT team that connects other systems to the DMS. It is not described in this guide. The page **Keel integration** is: see [Keel integration](/dms/admin/keel-integration/).

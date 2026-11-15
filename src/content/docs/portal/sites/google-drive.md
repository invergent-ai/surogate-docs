---
title: Files in Google Drive
description: List, send, keep, share and throw away files in Google Drive from jobs, and make Google Docs from a template, such as a contract filled with a client's details.
---

The portal's **Google Drive** extension works with files in [Google Drive](https://drive.google.com). A job sends the CVs a careers form received to a shared drive; another makes a contract from a Google Doc template and keeps it as a PDF in the portal; an administrators' page lists a folder. As with every extension, it is open to every tenant of the portal.

## Connect Google Drive

A **Google Drive** connector signs in one of two ways. In both, turn on the **Google Drive API** and the **Google Docs API** in the Google Cloud project first.

**As a service account.** Best for a Google Workspace.

1. In the Google Cloud console, make a service account and a JSON key for it.
2. A service account keeps no files of its own. Either make it a member of a **shared drive** your steps use, or let it act as a Workspace user: the Workspace's administrator delegates it the scope `https://www.googleapis.com/auth/drive` (domain-wide delegation).
3. On **Connectors**, make a connector of the kind **Google Drive**, signing in as **A service account**. To act as a user, write their address under **User it acts as**.
4. Set the credential: paste the key file whole.

**As a Google account.** Best for a single Google account, outside a Workspace.

1. In the Google Cloud console, make an **OAuth client** of type **Web application**. Publish its consent screen, or make it **Internal** in a Workspace: an app left in testing loses the accounts connected to it after seven days.
2. On **Connectors**, make a connector of the kind **Google Drive**, signing in as **A Google account, connected here**, with the client's id. Copy the address under **Address Google sends you back to** into the client's **Authorized redirect URIs**, exactly as written. Save.
3. Choose **Connect a Google account**, give the client's secret, and allow Drive on Google's page. Leave Drive ticked: without it, nothing is kept. The connector's page then names the account connected.

**Test** asks Google who the connector is in Drive; nothing is changed. It also tells you when an API is not turned on.

The account's sign-in ends if it is not used for six months, if someone takes it back in their Google account, or if the client's secret changes: steps then say so, and you connect again.

## The actions

- **List a Drive folder** keeps the files of a folder: their ids, names, kinds, sizes, links and whether each is a folder, and whether there are more. A folder is named by its id, as Drive shows it in its address; `root` is the account's own My Drive. **Name contains** matches the start of a word in the file's name.
- **Send a file to Drive** sends a file of the portal's folders to a Drive folder, at most 10 MB. A file of the same name in that folder is kept, and the step fails, unless you tick **Replace a file of that name**: the new file is sent, then the old one goes to the trash. **Make it a Google Docs, Sheets or Slides file** turns a Word, Excel, PowerPoint, OpenDocument, text or CSV file into Google's own kind.
- **Keep a Drive file** keeps a Drive file in a portal folder. A Google Docs, Sheets or Slides file is kept as the kind you choose: a Doc as PDF, Word, OpenDocument or text; a Sheet as PDF, Excel, OpenDocument or CSV (its first sheet); Slides as PDF, PowerPoint, OpenDocument or text. The portal file's name ends with that kind's extension, such as `contract.pdf`.
- **Make a Google Doc from a template** copies a Google Doc into a folder, with the name you give, and puts each value where the template says `{{name}}`, such as `{{client}}`. It keeps the new Doc's id and link, and the placeholders it did not find. A value that holds braces is put in as written.
- **Share a Drive file** shares a file with one email address (to read, comment or edit), telling them by email unless you untick it, or with **anyone with the link**, to read or comment only.
- **Move a Drive file to the trash** moves a file to Drive's trash, from which it can be restored. A folder is never moved, since its trash would take everything in it.

Each step keeps what Google answered, so the next steps can use a file's id or link: send a file, then share it; make a Doc, then keep it as a PDF.

## Who may do what

- **Administrators** and **jobs** use every action.
- **A job started by anything but time** (a record, a person's change, mail, a payment, an app's event, a page request) does not share or move files to the trash: what started it was written by others. It still lists, sends, keeps and makes Docs.
- **Forms anyone may send and endpoints anyone may call** use none of these actions. A careers form keeps its files in the portal; a job started by the new record sends them to Drive.
- The folders and templates a step names are written in the step, never taken from what a person typed. A file's id can come from an earlier step or a record.

A service account or connected account reaches every file it may see in Drive. A job that keeps a file named by a record keeps whatever that record names: give the account only the folders the site needs.

## Limits

- Files of at most 10 MB, each way. Google exports a Doc, Sheet or Slides file of at most 10 MB.
- A list keeps at most 1,000 files (100 when you say nothing).
- A template takes at most 50 values.
- Each run makes a new Doc from a template, so a run tried again makes a second one.
- At most two calls at once for each connector; a run makes at most 20 extension calls.

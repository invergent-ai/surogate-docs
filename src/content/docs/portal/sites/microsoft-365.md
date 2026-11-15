---
title: Files in OneDrive and SharePoint
description: List, send, keep, share and recycle files in a OneDrive or a SharePoint library from jobs, through Microsoft 365.
---

The portal's **Microsoft 365** extension works with files in a user's OneDrive or a SharePoint site's document library, through Microsoft Graph. A job files a careers form's CVs in the HR site; another keeps a Word contract from SharePoint as a PDF in the portal; an administrators' page lists a folder. As with every extension, it is open to every tenant of the portal.

Documents are edited in the portal's own document management, not in Microsoft 365 for the web.

## Connect Microsoft 365

The portal signs in as an app of your Microsoft Entra directory, never as a person.

1. In Microsoft Entra, register an app and give it a client secret. Keep the directory (tenant) id, the app's id and the secret.
2. Give the app Microsoft Graph **application** permissions, with an administrator's consent:
   - a user's OneDrive: `Files.ReadWrite.All`;
   - a SharePoint site: `Sites.ReadWrite.All`, or better `Sites.Selected` with that one site granted to the app, so it reaches nothing else.
3. On **Connectors**, make a connector of the kind **Microsoft 365 (OneDrive or SharePoint)**, with the directory id and the app's id. Under **Works in**, choose **A SharePoint site's document library** and write the site's address without `https://`, such as `contoso.sharepoint.com/sites/hr`; or choose **A user's OneDrive** and write the user's sign-in name.
4. Set its credential: the client secret.

**Test** asks Microsoft for a token and finds the library; nothing is changed. Permissions given to the app take a few minutes to apply; **Test** again after.

A connector works in one library: a site's default **Documents** library, or one user's OneDrive for work or school. Personal OneDrive accounts are not reached. When the secret expires, steps say so: make a new one in Entra and set it.

## The actions

- **List a OneDrive or SharePoint folder** keeps the files and folders of a folder: their ids, names, sizes, links and whether each is a folder, and whether there are more. A folder is named by its path in the library, such as `/Candidați/2026`; `/` is the library's top.
- **Send a file to OneDrive or SharePoint** sends a file of the portal's folders, at most 10 MB, into a folder that must already be there: a path written wrong never makes folders. A file of the same name is kept, and the step fails, unless you tick **Replace a file of that name**: then the file keeps its id and its sharing, and gains a new version. A folder of that name is never touched.
- **Keep a OneDrive or SharePoint file** keeps a file of the library in a portal folder, as it is, or as a **PDF** Microsoft makes of a Word, Excel, PowerPoint, OpenDocument, RTF or CSV file (the portal file's name then ends `.pdf`). Folders, OneNote notebooks and shortcuts to other libraries are not downloaded.
- **Share a OneDrive or SharePoint file** shares a file or folder with one email address, to read or to edit (telling them by email if you tick it), or makes a link for **the organization** or for **anyone**, who may only read. Whether outside people and links for anyone are allowed is the Microsoft 365 tenant's own policy.
- **Move a OneDrive or SharePoint file to the recycle bin** moves a file to the library's recycle bin, from which it can be restored. A folder is never moved.

Each step keeps what Microsoft answered, so the next steps can use a file's id or link.

## Who may do what

- **Administrators** and **jobs** use every action.
- **A job started by anything but time** (a record, a person's change, mail, a payment, an app's event, a page request) does not share, replace or recycle files: what started it was written by others. It still lists, sends new files and keeps them.
- **Forms anyone may send and endpoints anyone may call** use none of these actions. A careers form keeps its files in the portal; a job started by the new record sends them on.
- Folder paths are written in the step, never taken from what a person typed. A file's id can come from an earlier step or a record: a job keeping a file a record names keeps whatever that record names in the connector's library. Use a dedicated app with `Sites.Selected` and give it only the site the portal needs.

## Limits

- Files of at most 10 MB, each way; PDFs Microsoft makes of at most 10 MB.
- A list keeps at most 1,000 items (100 when you say nothing).
- When Microsoft asks the portal to slow down, the step says how many seconds to wait; it is not tried again on its own.
- At most two calls at once for each connector; a run makes at most 20 extension calls.

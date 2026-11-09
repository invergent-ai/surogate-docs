---
title: Versions
description: Every saved change to a portal's sites is a version you can look back at and undo.
---

Every time a change to the portal's sites is saved, the portal keeps it as a version: what changed, who saved it and when. **Versions** lists them, newest first, and lets you undo one. Saves from [Pages](/portal/console/pages/) and from the design studio are versions too. **Versions** is for administrators, on a portal whose site files the portal keeps; the page is not in the menu otherwise.

![The Versions page: three saved changes, the newest marked Live, each with who saved it and an Undo button.](../../../../assets/screenshots/portal-versions.png)

## What the list shows

- Each version's description, who saved it and when.
- **Live** marks the version visitors see now. Usually it is the newest. If the newest could not go live, the page says **The newest version is not live yet**; press **Make it live** to try again.
- **Moved into the portal** is the version the portal started from, when the sites were moved in. It cannot be undone.
- **Undid an earlier change** is an undo.
- **Changed outside the console** is a change your implementation team made directly.
- **Show older versions** brings in the ones further back.

## Undo a change

1. Press **Undo** beside the version.
2. The portal says what undoing it will do. If later changes touched the same files, it names them: undoing puts them back to what they were before this change too. Undoing the very first version leaves the sites with no pages, and the portal says so.
3. Press **Undo** to confirm.

Undoing never deletes history. The files that version changed go back to what they were before it, as a new version, which you can undo in turn.

If someone saved a change while you were deciding, the portal asks you to look at the newest versions first, then try again. If undoing would break the site, nothing changes and the page lists what is wrong.

Saving, undoing and moving into the portal are all in the [audit log](/portal/console/audit/).

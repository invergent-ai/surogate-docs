---
title: Access
description: Check who may view or edit a site, page or placement, and why, and add editors.
---

On **Access**, an administrator checks who may see or edit the portal's sites, pages and placements, and adds editors. Who may *view* a page is chosen in the site's settings, on the page's **Settings** tab and in each block: see [Who sees a page](/portal/sites/permissions/).

## Check someone's access

1. Under **Check access**, choose **A person** and type their **Email**, or choose **Anonymous visitor** for someone who has not signed in.
2. Choose **View** or **Edit**.
3. In **Site, page or placement**, choose what to check.
4. Press **Check**.

The console says **Allowed** or **Not allowed**. When access is allowed, it lists the steps that allowed it: for example, the site lets everyone view it, and the page lets the group **Funcționari** view it.

![Check access for ana@example.ro on the page main/intranet: Allowed, with the steps down to the group Funcționari.](../../../../assets/screenshots/portal-access-check.png)

## Check access to data, endpoints and sections

Under **Check access to data, endpoints and sections**, choose what to check:

- **Records**: type the person's **Email** (leave it empty for a visitor), choose the **Model**, the **Verb** (**Read**, **Add**, **Change** or **Remove**) and, if you like, a **Record id**. With a record, the answer is for that record; without one, it says whether the person may do the verb on some records.
- **Endpoint**: choose the endpoint. The answer says whether the person, or a visitor, may call it.
- **Console section**: choose the **Section** and the **Level**. The answer says whether the person's roles open it.

Press **Check**. The console says **Allowed** or **Not allowed**. When it is allowed, the steps say which role gave it and, for records, which rule held:

![Check access to data: ana.pop@example.com may change a sheet of her county, by the role DSP/DMS user and the rule on the sheet's entity.](../../../../assets/screenshots/portal-access-check-record.png)

## Add editors

Editors may edit a site or a page, and so they can also see it, whatever its files say about viewing.

1. Under **Editors added here**, press **Add editors**.
2. Choose **Person** and type their **Email**, or choose a **Group** or an **Organization**. An organization includes the organizations below it.
3. In **Site or page**, choose what they may edit.
4. Press **Add**.

![The Add editors dialog: the group Funcționari, for the page main/servicii.](../../../../assets/screenshots/portal-access-add-editors.png)

To take the right away, press the bin next to the editors and confirm. Editors also go when the person, group or organization is deleted, or when the site or page is removed from the site's files.

Administrators always edit and see everything; they need no entry here.

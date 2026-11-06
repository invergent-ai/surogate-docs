---
title: Surogate DMS quickstart for administrators
sidebar:
  label: Quickstart for administrators
---

This page takes a new installation to one that staff can use: the org chart, the people, the nomenclator, the folders, the document types and the roles, in the order the DMS needs them. It takes about an hour with your institution's data at hand.

The pictures were taken in a demo city hall, Example City Hall, with made-up people and documents. You are Elena Marin, the first administrator.

You need:

- the sign-in details of the first administrator; your operator makes you the first administrator, and sets up the accounts of the people in your institution, the institution's name and the internal certificate authority;
- the list of your units and positions, and the e-mail addresses of your staff;
- the nomenclator your institution's National Archives approved, as an Excel file, with its approval number and date.

## 1. Sign in

Sign in with your e-mail address and password. A new installation has an empty **My desk** and, in the sidebar, the **Archive** and **Administration** sections.

![My desk of the first administrator on a new installation](../../../assets/screenshots/dms-desk-first-admin.png)

## 2. Build the org chart

Open **Administration** › **Org chart**. Add the **Unit types** your institution uses (for example Directorate, Department and Office) in the panel on the right.

![The Org chart page with the unit types and no units yet](../../../assets/screenshots/dms-org-unit-types.png)

Press **New unit at the top level**, name the unit, choose its type and, if you like, give it a short code. Add subunits and positions from the menus on each unit. See [The org chart](/dms/admin/org-chart/).

## 3. Add the people and name the holders

Open **People** and press **Add a person**: an **Email address** and a **Display name**. The person is "Pending" until they first sign in.

![The Add a person dialog](../../../assets/screenshots/dms-people-add.png)

On the org chart, open the menu of a position, choose **Holder…** and choose the person who holds it.

![Choosing the holder of the position Secretary General](../../../assets/screenshots/dms-org-holder.png)

When you are done, the chart shows every position with its holder, and "Vacant" where nobody holds it.

![The whole org chart with positions and holders](../../../assets/screenshots/dms-org-chart.png)

## 4. Put the nomenclator in force

Open **Nomenclator**. A new installation has none.

![The Nomenclator page before any edition](../../../assets/screenshots/dms-nomenclator-empty.png)

Press **Import an edition**, choose the Excel file and give the edition a name. Choose the unit of every compartment the DMS could not match, fill in the **Approval number** and **Approval date**, and press **Put in force**.

![The dialog asking for confirmation before edition 2026.1 is put in force](../../../assets/screenshots/dms-nomenclator-force.png)

![Edition 2026.1 in force, with its entries](../../../assets/screenshots/dms-nomenclator-in-force.png)

See [The nomenclator](/dms/admin/nomenclator/).

## 5. Make the folders and the dosare

Open **Folders** and press **New folder at the root**. A folder at the root belongs to a unit. Inside it, add the dosare: each has an entry of the nomenclator, a year and a closing rule.

![The New folder dialog at the root, for the Finance Department](../../../assets/screenshots/dms-folders-new-root.png)

You can also set a dosar's entry from its page in the library.

![The entry of the dosar Contracts 2026: Entry, Year of the dosar and Closes](../../../assets/screenshots/dms-dosar-entry.png)

## 6. Define the document types

Open **Document types** and press **New type**. Give it a name, a default folder and its fields.

![The type Contract with its six fields](../../../assets/screenshots/dms-types-contract.png)

## 7. Grant roles

Open **Roles and permissions**, choose a role and press **Grant the role**. Choose who gets it (a **Person**, a **Position** or a **Unit**) and where it applies.

![Granting the role Standard user to the unit Urban Planning Department and its subunits](../../../assets/screenshots/dms-roles-grant.png)

## 8. Check the alert rules

Open **Archive** › **Alerts** and look at the **Rules** tab. The working hours decide when work on documents counts as unusual.

![The Rules tab of Alerts with the working days and hours](../../../assets/screenshots/dms-alerts-rules.png)

## 9. Check as a staff member

Ask a colleague who holds only **Standard user** to sign in and open their folders. If they see no folder, check their grant: [Roles and permissions](/dms/admin/roles/).

## 10. Read the audit log

Open **Audit log** and filter the **Entries** by a person to see what they did.

![The audit log of the entries of one person](../../../assets/screenshots/dms-audit-entries.png)

## Next steps

- [Set up a new department](/dms/examples/new-department/) repeats these steps for one department.
- [Roles and permissions](/dms/admin/roles/) explains grants.
- [The Archive overview](/dms/archive/overview/) is where an archivist starts.
- [The capture quickstart](/dms/quickstart-capture/) sets up a channel and a flow for scanned paper.

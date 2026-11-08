---
title: Users
---

**Users** lists the people who can sign in to this portal. You need the **Administrator** role (on the main portal, **Install administrator**).

## Find a user

Type part of a name or an email in **Search by name or email**. The list follows as you type. When nothing matches, the page says **No user matches.**; press **Clear the search** to see everyone.

The list shows 50 users at a time. Use **Previous** and **Next** to move between pages. A disabled account carries the label **Disabled**.

## Add a user

1. Press **New user**.
2. Type their **Email** and **Name**. They sign in with this email.
3. **Password (optional)**: at least 12 characters. Leave it empty for someone who signs in with your organisation's account.
4. Fill in the portal's own fields, if it has any (a badge number, a department, a phone). Fields marked **Required** must be filled in.
5. Press **Create user**.

If the email is already used, the console says **A user with this email already exists.**

## A user's page

Press a user in the list to open their page. The top shows their name, email, the date they were added, and **Active** or **Disabled**.

### Details

Change the **Name** or the portal's own fields and press **Save**.

### Roles

Tick or untick **Administrator** and press **Save roles**. On the main portal there is also **Install administrator**. See [Roles](/portal/reference/roles/).

A portal always keeps at least one active administrator. Removing the role from the last one says **This is the portal's last active administrator. Give the role to someone else first.**

### Password

Type a **New password** of at least 12 characters and press **Set password**. The person's other sessions end: they sign in again with the new password. Their tokens keep working.

### Disable and enable

Press **Disable** at the top, then **Disable** again in the question **Disable** *name***?** A disabled person can no longer sign in, and their tokens stop working. Press **Enable** to let them back in.

You cannot disable the last active administrator.

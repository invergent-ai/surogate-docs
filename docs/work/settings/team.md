---
title: Team & users
sidebar_position: 6
---

# Team & users

Manage every account on the platform from the **Users** tab at `/work/settings/users` (shared with Dev mode at `/studio/settings/users`). This tab is **visible to admins only**.

## The users table

Each row is one account, with these columns:

| Column | Notes |
|---|---|
| **User** | Avatar, username, and display name. Username is immutable. |
| **Email** | Login email, or "—" if none. |
| **Roles** | The account's assigned roles (see below), or "—" if none. |
| **Auth** | How the user signs in — `firebase` or `local`. |
| **Last login** | Relative time, or "Never". |
| **Created** | When the account was created. |

Above the table you can **search** by username, email, or name, and **filter by role**. Use **Clear filters** to reset. The table paginates at 25 users per page.

## Roles

| Role | Label |
|---|---|
| `admin` | **Admin** |
| `skill_author` | **Skill author** |
| `devops` | **DevOps** |
| `developer` | **Developer** |

A user can hold any combination of roles. Admin roles are shown with a highlighted badge.

## Row actions

Each row exposes four actions:

- **Edit** — opens a dialog to change the account's **Display name**, **Email**, **Title**, **Company**, **Bio** (capped at 180 characters), and **Roles**. Username is immutable and passwords are managed by the user. For Firebase users, a note warns that changing the email here does **not** update Firebase.
- **Billing** — opens the per-user billing dialog.
- **Impersonate** — sign in as that user to reproduce what they see. Disabled for yourself and for other admins (admins cannot be impersonated). Starts an impersonation session and navigates to `/work`.
- **Delete** — permanently removes the account after a confirmation prompt. This cannot be undone.

> This tab manages **existing** accounts. There is no invite-by-email flow here; new end users typically arrive via self-registration when BYO Firebase auth is configured for the project (see [Project settings](./project.md)).

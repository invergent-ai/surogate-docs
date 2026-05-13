---
title: Teams and roles
sidebar_position: 2
slug: /admin/teams-and-roles
description: System roles, project roles, teams as a grouping primitive. Invite, deprovision, audit access.
---

# Teams and roles

Two role surfaces, separately scoped: **system roles** that apply across the whole Surogate Ops install, and **project roles** that apply to a single agent / model / KB / dataset. Teams are the grouping primitive that ties them together.

This page is the full reference. For the daily-admin overview, see [Admin overview](./overview.md).

## System roles

Set when a user is invited; editable later from Settings → Users.

### admin

The role with no ceiling.

An admin can:

- Manage all users (invite, edit, deprovision).
- Manage all teams.
- Edit Compute Policies.
- Read and rotate every entry in the Credential Vault.
- Manage the Data Hub configuration (quotas, LFS, endpoints).
- Read the full audit log.
- Do everything `skill_author`, `devops`, and `developer` can do.

Practical guidance: have at least two admins. Solo-admin instances become bricked if the one admin leaves or loses their account.

### skill_author

Build-track. The role for people writing skills, building agents, training models, curating datasets.

A skill_author can:

- Create and edit skills, including expert skills backed by deployed models.
- Create and edit agents.
- Deploy models (subject to Compute Policy).
- Schedule training runs.
- Create and push to Hub repositories.
- Run evaluations and arenas.

A skill_author can't:

- Invite or deprovision users.
- Edit Compute Policies.
- Edit the Credential Vault (they can *use* it through skills they author, not edit entries).
- Read the audit log.

### devops

Operate-track. The role for the people keeping the platform healthy without being involved in product development.

A devops user can:

- Restart serving containers and cancel any workload.
- View every session across every project.
- Edit any backend configuration in Compute → Cloud.
- Read (not edit) the Credential Vault.
- Read the audit log.

A devops user can't:

- Invite or deprovision users.
- Create or edit skills, agents, training runs.
- Edit policies (read-only).

The split between admin and devops is what lets you give an SRE team operational access without giving them user-management power.

### developer

Default for most teammates. The read-mostly, build-in-their-own-projects role.

A developer can:

- Be invited as a member on projects, with a project role determining what they can do there.
- Read their own sessions and projects.
- Create personal projects (subject to install settings).
- Consume models the install makes available.

A developer can't:

- See projects they aren't a member of.
- Manage other users.
- Edit any global setting.

## Project roles

Set per user per project. Three values: **owner**, **editor**, **viewer**.

| Role | Read settings | Edit settings | Manage members | Delete |
|---|---|---|---|---|
| owner | ✓ | ✓ | ✓ | ✓ |
| editor | ✓ | ✓ | — | — |
| viewer | ✓ | — | — | — |

Multiple owners are supported and recommended — solo-owner projects become unowned when the owner leaves.

## Teams

Teams are a way to grant the same project role to many users at once. Without teams you'd be adding each user to each project individually; with teams you add the team and every team member inherits the project role.

A team has:

- A **slug** (URL-safe, permanent).
- A **display name**.
- A **member list** of users.
- **No system role of its own** — every team member's system role is set on the user, not on the team.

Adding a team to a project: project → **Members** → **+ Add team** → pick the team and the project role. The team's members are now project members at that role; new team members added later inherit automatically.

Removing a team from a project is the reverse; existing per-user grants (someone added individually as well as via the team) remain.

## Invite a user

Settings → **Users** → **+ Invite**.

Fields:

- **Email** — required.
- **System role** — pick from `admin`, `skill_author`, `devops`, `developer`. Default is `developer`.
- **Teams** — optional. Pre-add to one or more teams; the invite shows the team list to the new user.
- **Message** — optional free-text shown in the invitation email.

The invite sends an email with a one-time link valid for seven days. If it expires, re-invite the same email; the previous invite is invalidated.

## Edit a user

Settings → **Users** → click into the user → edit:

- **System role** — changes apply on next request; existing tokens refresh within minutes.
- **Teams** — add or remove.
- **Status** — *Active* or *Disabled*. Disabling preserves history but prevents sign-in.

You can't edit a user's email. To migrate someone's email, deprovision the old account and re-invite with the new email; the audit log keeps both records linked.

## Deprovision a user

The right way to remove someone:

1. Settings → Users → user → **Disable**. They can't sign in.
2. Audit log → filter to this user → review their last 30 days of actions for anything mid-flight.
3. Project membership → remove them from sensitive projects.
4. Credential Vault → rotate any credential this user might have seen.
5. After thirty days, the user is fully purged from active state; the audit-log entries remain.

Don't delete users immediately. The two-step disable-then-delete pattern preserves the audit trail and gives you a window to roll back a mistaken deprovisioning.

## Single sign-on

Surogate Ops supports SSO via OAuth (Google, GitHub) and SAML for enterprise installs.

Once SSO is enabled:

- New users sign up through the SSO provider; their email is the email the provider sends.
- Existing email-based users continue to work; they can link their account to SSO from Settings → Profile.
- Disabling a user on the SSO provider doesn't automatically disable them in Surogate. Set the Surogate user to *Disabled* in Settings → Users to be sure.

## Audit hooks

Every user-management event lands in the audit log:

- `user.invited` — including the system role and team list.
- `user.role_changed` — old role and new role.
- `user.disabled` / `user.enabled`.
- `team.created` / `team.deleted`.
- `team.member_added` / `team.member_removed`.
- `project.member_added` / `project.member_removed` — including the project role and whether it was via a team.

The audit log is queryable from Settings → Audit log (admin only). Filter by user, by event type, by time range.

## When this isn't worth doing

A single-user install doesn't need teams. A two-person install probably doesn't either — adding users individually to two or three projects is fast and clear. Teams pay off at around five or more users, where the bookkeeping of per-user-per-project grants starts to add up.

## When something fails

- **An invited user never got the email.** Check their spam folder; the email is from `noreply@surogate.ai`.  If they still don't have it, re-invite — that issues a fresh email and invalidates the old link.
- **A user's role change "didn't take."** Their token may still be cached. Have them sign out and back in. The server side is consistent within seconds; the client-side token refresh is the variable.
- **A team change didn't propagate to a project.** Confirm the team is actually attached to the project (Project → Members → Teams tab). If it's attached, the propagation is immediate; if it's not, the team grants aren't applied.
- **Audit log shows an action by a user you don't recognise.** Check the timestamp and the IP / device fields. If you can't explain it, disable the user immediately and rotate any credential they might have touched.

## Where to go next

- **[Admin overview](./overview.md)** — the wider admin surface.
- **[Credential Vault](./credential-vault.md)** — where the secrets that users see through skills live.
- **[Permissions matrix](../reference/permissions-matrix.md)** — the structured table of who-can-do-what.

---
title: Roles
---

Surogate Portal has two roles for its console. People without a role can still sign in and manage their own [tokens](/portal/console/tokens/).

| Role | Where | What it allows |
|---|---|---|
| **Administrator** | Any tenant | Manage the tenant's users, groups, organizations, sign-in providers and [access](/portal/console/access/). Administrators see and edit every site and page. |
| **Install administrator** | The main portal (the default tenant) | Everything an administrator does on the main portal, and create and manage tenants. |

On the main portal, managing users and sign-in takes the **Install administrator** role. A plain **Administrator** there sees only **My tokens**.

When you change your own roles, the console's pages follow at once.

Every tenant keeps at least one active administrator: you cannot remove the role from, or disable, the last one.

Roles are set on a user's page, under [Roles](/portal/console/users/#roles).

Roles can also come from a directory or a sign-in provider, through [group mappings](/portal/console/group-mappings/). Those are kept apart from the ones given by hand, and the next sign-in or sync updates them.

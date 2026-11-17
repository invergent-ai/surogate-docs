---
title: Roles
---

Surogate Portal's roles are made in the console: see [Roles](/portal/console/roles/). Every portal starts with four of them, and you can add as many as you need.

| Role | Where | What it allows |
|---|---|---|
| **Administrator** | Any tenant | Everything: the tenant's users, roles, groups, organizations, sign-in, [access](/portal/console/access/) and every section of the console. Administrators see and edit every site and page. |
| **Developer** | Any tenant | The sections that build a portal, at **Edit**. It can be renamed, changed and deleted. |
| **Manager** | Any tenant | People and roles at **Edit**; the audit log and access at **View**. It can be renamed, changed and deleted. |
| **User** | Any tenant | Nothing in the console. Every new account has it. It can be renamed, changed and deleted. |
| **Install administrator** | The main portal (the default tenant) | Everything an administrator does on the main portal, and create and manage tenants. |

On the main portal, managing users and sign-in takes the **Install administrator** role. A plain **Administrator** there sees only **My tokens**.

A person holds one or more roles, and has the rights of each. Roles are set on a user's page, under [Roles](/portal/console/users/#roles), and in the **New user** dialog, which asks for at least one.

When you change your own roles, the console's pages follow at once. A person who is not an administrator cannot change their own roles.

Every tenant keeps at least one active administrator: you cannot remove the role from, or disable, the last one. The **Administrator** role cannot be deleted.

A [service account](/portal/console/service-accounts/) can hold any role of its tenant, except the install administrator's; what each of its tokens may do is then limited by the token's scopes too.

Roles can also come from a directory or a sign-in provider, through [group mappings](/portal/console/group-mappings/). Those are kept apart from the ones given by hand, and the next sign-in or sync updates them. A mapping can give any role the tenant has made.

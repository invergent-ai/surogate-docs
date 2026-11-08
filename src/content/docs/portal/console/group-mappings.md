---
title: Group mappings
description: Turn your directory's or identity provider's groups into portal groups and roles.
---

A group mapping turns a group a person has elsewhere into a portal group or role. A directory's groups give, for example, everyone in `cn=editors,ou=groups,dc=example,dc=ro` the portal group **Editors**, and everyone in `cn=portal-admins,...` the **Administrator** role.

Mappings are kept per directory and per sign-in provider, at the bottom of its window.

1. Press **Add mapping**.
2. Type the outside group: for a directory, the group's DN; for a provider, the group's name or ID as the provider sends it.
3. Choose the portal group or role it gives.
4. Press **Save mappings**.

Upper and lower case do not matter, nor do spaces after the commas of a DN.

## When mappings apply

- A directory's mappings apply at every sign-in through it, and at every sync.
- A provider's mappings apply at every sign-in through it. The provider must send the groups: set **Groups claim** (OpenID Connect) or **Groups attribute** (SAML) on the provider.

Each time, the person gets exactly the groups and roles the mappings give them, and loses the ones that no longer apply.

## Mapped and hand-given access

Groups and roles an administrator gives by hand are never touched by mappings. On a user's page, the **Roles** card shows the roles given by hand as tick boxes, and lists below them the ones a directory or provider gives. A group's **Members** card shows members a directory gave as **From** the directory; only the directory can take them away.

The portal always keeps one active administrator: a mapping never takes the role from the last one.

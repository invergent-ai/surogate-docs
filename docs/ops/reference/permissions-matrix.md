---
title: Permissions
sidebar_position: 1
slug: /reference/permissions-matrix
---

# Permissions

Three project roles, granted on the **+ Invite** dialog at [Admin → Projects & Teams](../admin/projects-and-roles.md):

- **Viewer** — read-only.
- **Editor** — read plus create / edit on the project's resources.
- **Owner** — everything an editor can do, plus project-level controls (rename, archive, member management).

A separate **admin** permission unlocks workspace-level surfaces. Admins see additional Settings tabs and can edit compute policies and integrations.

## Project resources

Admin overrides every cell in this table.

| Action | viewer | editor | owner |
|---|:-:|:-:|:-:|
| List, open, chat with agents | ✓ | ✓ | ✓ |
| Deploy / edit / delete agents | ✗ | ✓ | ✓ |
| List, open models | ✓ | ✓ | ✓ |
| Deploy / stop / delete models | ✗ | ✓ | ✓ |
| List, read skills | ✓ | ✓ | ✓ |
| New / import / edit / delete skills | ✗ | ✓ | ✓ |
| List, open knowledge bases | ✓ | ✓ | ✓ |
| New / edit / delete KBs | ✗ | ✓ | ✓ |
| Browse Hub repos | ✓ | ✓ | ✓ |
| New / import / delete Hub repos | ✗ | ✓ | ✓ |
| List datasets | ✓ | ✓ | ✓ |
| New / import / edit / delete datasets | ✗ | ✓ | ✓ |
| List training runs | ✓ | ✓ | ✓ |
| Start / cancel training runs | ✗ | ✓ | ✓ |
| List arenas, evaluations | ✓ | ✓ | ✓ |
| Start an arena or evaluation | ✗ | ✓ | ✓ |
| Read own sessions | ✓ | ✓ | ✓ |
| Read other users' sessions | ✗ | ✓ | ✓ |
| Use Playground | ✓ | ✓ | ✓ |
| Read Monitoring | ✓ | ✓ | ✓ |
| Acknowledge alerts | ✗ | ✓ | ✓ |

## Admin-only

These actions require the workspace-level admin permission, regardless of project role.

- Connect or disconnect a cloud backend.
- Edit a Compute Policy.
- Add or edit Integration credentials.
- Manage workspace members (add / remove / change roles).

## Sidebar visibility

The Settings sidebar adapts to your permission set.

| Tab | Visible to |
|---|---|
| **Profile** | Everyone signed in |
| **Data Hub** | Everyone signed in |
| **Projects & Teams** | Admins |
| **Integrations** | Admins |
| **Notifications** | Admins |

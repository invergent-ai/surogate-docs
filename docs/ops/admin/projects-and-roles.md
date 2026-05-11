---
title: Projects, members and roles
sidebar_position: 1
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Projects, members and roles

Surogate Ops runs every object inside a **Project**. Access is gated by two parallel role models — a system role on the User and a per-project role on the membership.

## The two role axes

Defined in `surogate_ops/core/db/models/platform.py`:

```python
class UserRole(enum.Enum):           # system roles (multi-role per user)
    admin
    skill_author
    devops
    developer

class ProjectMemberRole(enum.Enum):  # project roles (one per (user, project))
    owner
    editor
    viewer
```

### System roles

| Role | Typical scope |
|---|---|
| `admin` | Platform-wide. Manages users, system integrations, all projects. Overrides every project-level limit. |
| `skill_author` | Authoring rights on Skills and skill templates. |
| `devops` | Compute. Connecting/disconnecting Cloud Backends, editing Compute Policies, watching the Workload Queue. |
| `developer` | Default for new sign-ups (`surogate_ops/core/db/repository/auth.py:119`). Build agents, models, KBs, datasets, training runs in projects they're a member of. |

A user can hold several system roles at once. The seeded admin account has username `surogate` (constant in `surogate_ops/server/auth/authentication.py:16`).

### Project roles

| Role | Permits |
|---|---|
| `owner` | Full control of the project plus member management. |
| `editor` | Read + create/update on project resources. |
| `viewer` | Read-only. |

Each `(user, project)` pair has exactly one project role, stored in `project_members`.

### How they combine

Effective permission on a given action is the **more permissive** of the two. A `developer` (system) who is `viewer` on Project A and `owner` on Project B can edit B's resources but not A's. A system `admin` overrides every project role on every project.

## Where to manage projects

`/studio/settings/projects` — the **Projects & Teams** page.

> The **Projects & Teams** tab is hidden from the Settings sidebar for project-`viewer`-only accounts. Reach it by URL with limited actions, or assume the user has system `admin` to see it in the navigation. TODO(verify visibility per system role).

## Page contents

Header: **Settings · Projects & Teams**.

Actions:

- **+ New Project** (top-right). Opens the project creation dialog.
- Per-row **⋯** menu. TODO(verify items: Archive, Rename, Delete).
- Per-row **+ Invite** to add a member.
- Per-row **Edit** for renaming / colors / archive status.

## Create a project

1. Open `/studio/settings/projects`.
2. Click **+ New Project**.
3. Fields:
   - **Name** — display label.
   - **Color** — chip used to distinguish projects in the UI.
4. Submit. The project is created with you as `owner`. A `hub_namespace` is auto-generated from the project's id (`Project.hub_namespace` event listener in `models/platform.py`).

## Invite a member

1. On the project's row, click **+ Invite**.
2. Enter a **username or email**.
3. Pick a **project role**: `viewer`, `editor`, or `owner`.
4. Submit.

TODO(verify whether an invite emails the user or adds them immediately. Observed behavior on the test account is unclear).

## Change a member's role

Open the project, find the member row, click **Edit** or **⋯**. TODO(verify the exact controls per member).

## Archive a project

A project with `status = active` can be set to `archived`. Archived projects drop out of default lists; their data is retained. Unarchive from the same menu. TODO(verify the route).

## Default project

`User.default_project_id` decides where newly created objects land. Switch project from the top bar (TODO(verify the exact control — observed in screenshots but not interactive on the test account)).

## Removing a user

The platform-level remove-user action is system `admin` only. A project `owner` can only remove members from their own projects. TODO(verify the cascade: do the user's owned objects move, or are they reassigned?).

## See also

- [Reference → Permissions matrix](../reference/permissions-matrix) — full per-feature breakdown with cells marked `TODO(verify)` where we couldn't confirm against the test account.
- [Admin → Integrations](./integrations) — system-level service connections.
- [Admin → Notifications](./notifications) — per-user and per-project alert preferences.

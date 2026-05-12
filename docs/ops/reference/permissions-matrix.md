---
title: Permissions matrix
sidebar_position: 1
slug: /reference/permissions-matrix
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Permissions matrix

## How permissions work in Surogate Ops

Two role axes apply at the same time — see [Admin → Projects, members and roles](../admin/projects-and-roles) for the long version.

- **System roles** on the User (multi-role): `admin`, `skill_author`, `devops`, `developer`.
- **Project roles** on `(user, project)`: `owner`, `editor`, `viewer`.

A user's effective permission on a given action is **the more permissive** of the two — for example, a system `admin` overrides project-level limits.

## Where checks happen

- **At the API**: backend routes audited so far gate on `Depends(get_current_subject)` (authenticated) only. Per-route role checks were **not** found at the FastAPI router layer. Authorization for project resources happens **inside service/repository code** via project membership.
- **In the UI**: a few tabs are hidden for non-admin users (Settings → Projects / Integrations / Notifications all hidden for project-`viewer`-only accounts). The rest of the UI is mostly uniform — destructive actions fail with a 403/404 when called by a viewer.

> Because this documentation was produced from a project-`viewer`-only account, the matrix below is **based on code reading + UI observation for `viewer` only**. Cells marked `?` are `TODO(verify)`.

## The matrix

### Project resources

The columns are **project roles**. System role `admin` overrides everything in this table.

| Action | viewer | editor | owner |
|---|:-:|:-:|:-:|
| List / open agents | ✓ | ✓ | ✓ |
| Deploy / edit / delete agent | ✗ | ✓ ? | ✓ |
| List / open models | ✓ | ✓ | ✓ |
| Deploy / stop / delete model | ✗ | ✓ ? | ✓ |
| List skills | ✓ | ✓ | ✓ |
| New / import / edit / delete skill | ✗ | ✓ ? | ✓ |
| List / open KBs | ✓ | ✓ | ✓ |
| New / edit / delete KB | ✗ | ✓ ? | ✓ |
| Browse hub repos | ✓ | ✓ | ✓ |
| New / import / delete hub repo | ✗ | ✓ ? | ✓ |
| List datasets | ✓ | ✓ | ✓ |
| New / import / edit / delete dataset | ✗ | ✓ ? | ✓ |
| List training runs | ✓ | ✓ | ✓ |
| New training run | ✗ | ✓ ? | ✓ |
| Cancel training run | ✗ | ✓ ? | ✓ |
| List arenas / evaluations | ✓ | ✓ | ✓ |
| Create arena / new evaluation | ✗ | ✓ ? | ✓ |
| Read sessions (own) | ✓ | ✓ | ✓ |
| Read sessions (other users') | ✗ ? | ✓ ? | ✓ |
| Use Playground | ✓ ? | ✓ ? | ✓ |
| Read monitoring | ✓ | ✓ | ✓ |
| Acknowledge alerts | ✗ | ✓ ? | ✓ |

### Compute & integrations

These usually require **system `devops`** or **system `admin`**. Project-level access is independent.

| Action | viewer | editor | owner | devops | admin |
|---|:-:|:-:|:-:|:-:|:-:|
| View Cloud tab | ✓ | ✓ | ✓ | ✓ | ✓ |
| Connect a cloud backend | ✗ | ? | ? | ✓ | ✓ |
| Disconnect a cloud backend | ✗ | ? | ? | ✓ | ✓ |
| View Workload Queue | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cancel any workload | ✗ | ? | ✓ ? | ✓ | ✓ |
| Edit policies | ✗ | ? | ? | ✓ | ✓ |
| Add / edit Integration credentials | ✗ | ? | ? | ✗ ? | ✓ |
| Configure Hub credentials (own) | ✓ | ✓ | ✓ | ✓ | ✓ |

### Settings tabs visible in the sidebar

This is **UI visibility only** — the page renders for all roles at the URL, but the sidebar entry is hidden.

| Tab | viewer | editor | owner | devops | admin |
|---|:-:|:-:|:-:|:-:|:-:|
| **Profile** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Data Hub** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Projects & Teams** | ✗ obs | ? | ? | ? | ✓ |
| **Integrations** | ✗ obs | ? | ? | ? | ✓ |
| **Notifications** | ✗ obs | ? | ? | ? | ✓ |

Legend: ✓ = allowed, ✗ = denied, ? = TODO(verify), `obs` = directly observed in the docs test account.

## Account-wide actions

| Action | admin | other roles |
|---|:-:|:-:|
| Add / remove users | ✓ | ✗ |
| Set system roles on users | ✓ | ✗ |
| Force a password reset on any user (`must_change_password`) | ✓ | ✗ |
| Read any project's data | ✓ | only if a member |
| Manage the default `surogate` admin account | ✓ | ✗ |

## Related

- [Admin → Projects, members and roles](../admin/projects-and-roles)
- [Reference → Errors](./errors) — the 401 / 403 vocabulary thrown by the auth layer.

---
title: Admin overview
sidebar_position: 1
slug: /admin/overview
description: What an admin does in Surogate Ops — teams, integrations, credentials, audit. The roles, surfaces, and operational duties.
---

# Admin overview

This chapter is for the people who run Surogate Ops for everyone else. The work isn't visible to most users: roles get granted, credentials live in a vault, audit logs accumulate, the Hub keeps growing. Done well, the rest of the team never thinks about any of it.

If you're a builder or an operator, you can skip this chapter. If you're the person other people email when something stops working, this is your section.

## What an admin owns

Five concrete responsibilities:

1. **People** — invite teammates, set their roles, deprovision them on the way out.
2. **Credentials** — the [Credential Vault](./credential-vault.md). Anything an MCP server, a skill, or an integration needs to talk to the outside world.
3. **Hub configuration** — quotas, LFS state, endpoint visibility for the [Data Hub config](./data-hub-config.md).
4. **Compute policies** — what backends, regions, instance types, and spend caps are allowed. The detail lives in [Compute](../features/compute.mdx); admin's job is to set the policy and own the cap escalations.
5. **Audit** — knowing what happened, when, by whom. Reviewing the log, especially around access changes.

The five often blur — onboarding a new team usually touches all of them in the same afternoon. The pages in this chapter are organised around the surface each one lives in.

## Roles at a glance

Two role surfaces, separately scoped:

### System roles

Apply across the whole Surogate Ops install. Set per user when they're invited (or later from Settings → Users).

| Role | What they can do |
|---|---|
| **admin** | Everything. The only role that can edit Compute Policies, manage the Credential Vault, deprovision users, and read the audit log. |
| **skill_author** | Build and publish skills, build agents, write to the Hub, run training. Can't manage other users, can't edit policies. |
| **devops** | Operate the platform — restart serving containers, view all sessions, configure backends — without the build privileges of skill_author or the user-management privileges of admin. |
| **developer** | Build agents and consume models, run sessions. The default role for most teammates. Read-mostly outside their own projects. |

### Project roles

Apply to a single project (an agent, a model, a knowledge base, a dataset). Set per user per project.

| Role | What they can do |
|---|---|
| **owner** | Full rights on the project: edit settings, add / remove members, delete. |
| **editor** | Edit settings and content; can't change membership. |
| **viewer** | Read-only. Can see sessions, metrics, model artifacts; can't change anything. |

A user can be `developer` system-wide and `owner` on a specific project. That's the common shape for individual contributors.

## The admin surface

Most admin work lives under **Settings**, accessible from the user-menu in the top-right of Studio.

- **Profile** — your own profile. Not really an admin page; lives here for convenience.
- **Users** — list of everyone, with role, last login, deprovision controls.
- **Teams** — group users into teams for project membership. (A team can be added to a project once; every team member inherits the project role.)
- **Integrations** — third-party connections (Hugging Face token, OpenRouter, Slack, etc.).
- **Credential Vault** — see [Credential Vault](./credential-vault.md).
- **Compute Policies** — see [Compute](../features/compute.mdx).
- **Data Hub** — see [Data Hub config](./data-hub-config.md).
- **Audit log** — read-only view of every admin-significant event.

## Day-one checklist for a new install

When you stand Surogate Ops up for a new team, do these in order. Each step assumes the previous one is done.

1. **Set up your own user.** Sign up; verify your email.
2. **Confirm you're admin.** If you're the first user to sign up, you'll have been auto-granted admin. Confirm in Settings → Users.
3. **Connect at least one cloud backend.** [Compute → Cloud](../features/compute.mdx). Without this nothing serves.
4. **Set the default Compute Policy.** Cap monthly spend and pin allowed regions. This is the gate that keeps a runaway training job from running up four figures of bill overnight.
5. **Invite the team.** Settings → Users → **+ Invite**. Send each invite with the right system role.
6. **Create your first project.** A project is the natural unit for an agent or a model your team owns collectively.
7. **Add team members to the project** at the appropriate project role.
8. **Connect external integrations.** Hugging Face token, Slack, GitHub — anything skills will need to call.

After day one, the admin work is mostly maintenance: provisioning new users, rotating credentials, reviewing audit on a cadence, watching the Hub's LFS quota.

## Day-to-day admin cadence

A rough cadence that works for most teams:

- **Daily** — glance at the Pending Approvals queue (Arenas crossing budget thresholds), respond to the ones that block work.
- **Weekly** — review the audit log for the week. Flag anything unexpected (a sudden burst of model deploys, a user added to a sensitive project).
- **Monthly** — review Compute spend per backend against the policy caps; tighten or loosen.
- **Quarterly** — rotate long-lived credentials in the Vault. Rotate the Hub access tokens for any service account.

## When this isn't worth doing

A single-person hobby instance doesn't need most of this. Skip the Vault, skip teams, skip the audit log. Your one admin user is also the only user, so role granularity buys nothing.

Once you have two users, set up Teams. Once you have an integration credential more sensitive than a Hugging Face read-token, set up the Vault. Once you have a real cost in your monthly bill, set up Compute Policies.

The pattern is: add admin overhead exactly when the lack of it would cost more than the overhead.

## When something fails

- **A user can't sign in.** Settings → Users → find them → check status. Most often the invite expired (resend) or the SSO connection broke for them specifically.
- **A user has a role they shouldn't.** Settings → Users → edit → save. The change applies on their next request; tokens issued under the old role expire within minutes.
- **Audit log is empty when it shouldn't be.** Either the time range is too narrow, or audit was disabled for that period. Audit is on by default; check Settings → Audit log → settings.
- **Credential Vault entry "stuck" deleting.** A skill or MCP server is still resolving against it. Find the dependents (the Vault detail lists them), unwire them, then delete.

## Where to go next

- **[Teams and roles](./teams-and-roles.md)** — the full reference for users, teams, system roles, project roles.
- **[Credential Vault](./credential-vault.md)** — how secrets get into Surogate and out to MCP servers and skills.
- **[Data Hub config](./data-hub-config.md)** — quotas, endpoints, LFS.
- **[Compute](../features/compute.mdx)** — the operational surface for backends and policies.
- **[Permissions matrix](../reference/permissions-matrix.md)** — the structured table of who-can-do-what.

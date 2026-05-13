---
title: Credential Vault
sidebar_position: 3
slug: /admin/credential-vault
description: Secrets resolved by the MCP proxy at runtime — vault scopes (platform / org / user), rotation, audit.
---

# Credential Vault

The Credential Vault is where any secret a Surogate Ops skill or MCP server needs at runtime lives. API keys for third-party services, OAuth refresh tokens, signed-private-key blobs — anything you don't want pasted into a skill's markdown body. The Vault stores them encrypted, and the MCP proxy resolves them only when a skill that's authorised to use them actually fires.

It exists because the alternative — every skill author pasting their own copy of every credential — has every failure mode you'd expect.

## The model

Three pieces:

1. **An entry.** One secret, with a name and a scope. Created by an admin.
2. **A scope.** Which skills and which users can resolve the entry. One of three values (below).
3. **A resolution.** A skill or MCP server, at runtime, asks the proxy for `vault://<entry-name>`. The proxy checks the scope, returns the secret if authorised, returns an error otherwise. The skill never sees the raw value before that resolution and never stores it.

## Scopes

Three scope levels. The right scope is the smallest one that does the job.

### platform

Every skill, every MCP server, every user in the install can resolve this entry.

Use for credentials that are genuinely platform-wide and not sensitive — for example a shared Hugging Face read token used to pull public-but-gated models.

Don't use for anything that would be a problem if every user could see it.

### org

Resolvable only by skills and MCP servers owned by a specific organisation (or team). A user belonging to that organisation can use the entry through any skill they author; a user outside the organisation can't.

Use for the bulk of credentials — your team's GitHub PAT, your team's Salesforce API key, the OpenRouter token that powers your team's serving.

### user

Resolvable only by skills and MCP servers a specific user owns. Other users in the same organisation can't access it.

Use for individually-licensed credentials (the developer's personal Anthropic API key for a hobby skill) and for credentials that genuinely belong to one person and shouldn't propagate.

A user-scoped entry that should propagate as the user moves jobs isn't user-scoped — it's a misuse of the scope and a planning trap. Make it org-scoped from the start.

## Create an entry

Settings → **Credential Vault** → **+ New entry**.

Fields:

- **Name** — short, slug-shaped. The thing skills will reference as `vault://<name>`. Permanent once created.
- **Scope** — `platform`, `org` (select which), `user` (select which).
- **Type** — `string` (a single value) or `json` (a structured blob — typically for OAuth tokens or service-account keys).
- **Value** — the secret. Shown once during create; never displayed again.
- **Description** — for your future self. The entry's purpose, the upstream account, the rotation date.

Submit. The entry is encrypted and stored. The plaintext leaves your browser once; nobody (not even admins) reads it back from the UI after that.

:::warning Value is shown once
The Vault never displays a secret's value after the initial create. If you close the dialog without copying the value, you have to delete the entry and create a new one — there's no "show me" button. This is by design.
:::

If you need to verify the value, the only way is to use it through a skill.

## Use an entry from a skill

The skill's markdown body references the entry by name:

```yaml
secrets:
  github_token:
    vault: github-team-pat
```

When the skill executes, the MCP proxy looks up `vault://github-team-pat`, checks the calling user against the entry's scope, and injects the resolved value into the skill's `github_token` variable.

The skill body never contains the raw token. Anyone reading the skill source sees `vault://github-team-pat`; only at execution time, for an authorised caller, does the real value land in memory.

## Rotation

Rotation is the same shape as every other key rotation in Surogate Ops: create-new, point-clients-at-new, then revoke-old.

Concrete steps for a token like GitHub's:

1. Generate a new PAT in GitHub's settings.
2. In Surogate: Vault → **+ New entry** with the new name (`github-team-pat-2026-05` or similar) and the new value.
3. Update each skill that referenced the old name to reference the new name. (You can also rotate in place by editing the value of an existing entry — see below — but the rename approach makes the rotation visible in the audit log.)
4. Once you've confirmed every dependent skill is using the new entry, delete the old entry.
5. Revoke the old PAT on GitHub.

### Rotation in place

If you don't want to rename, you can edit an entry's value:

Vault → entry → **Edit value** → paste the new value.

This is faster but harder to audit — the old value is gone the moment you save. If anything depends on the old value still working, the rename approach is safer.

### Scheduled rotation

For credentials with a clear rotation cadence — production keys you want rotated every 90 days — set a rotation date on the entry. The Vault sends a reminder to the entry's owner (or to all admins, for platform-scoped entries) seven days before the date.

## Delete an entry

Vault → entry → **Delete**.

The Vault refuses to delete an entry that has live dependents — at least one skill or MCP server referencing it. The entry detail page lists every dependent; un-wire them first.

:::danger Deletion is irreversible
The encrypted value is purged within seconds and there's no recovery path. If the entry is still in active use by a skill or MCP server, those callers will start failing immediately. Always rotate before delete, never the other way around.
:::

## MCP server scopes

The same scope model applies to MCP servers themselves, not just to the secrets the MCP servers use.

When you register an MCP server in **Build → Skills & Tools → MCP Servers**:

- **platform** — every user in the install can attach the server to their agents.
- **org** — only users in the specified organisation can.
- **user** — only the registering user can.

The MCP server's *transport* (HTTP or Stdio), *auth method* (None / OAuth / API Key / Bearer Token), and *timeout* are all configured at registration time. The auth-method's credential typically resolves to a Vault entry — that's the integration point between MCP scopes and Vault scopes.

## Audit

Every Vault action is audit-logged:

- `vault.entry_created` — name, scope, owner.
- `vault.entry_resolved` — name, calling skill, calling user. (The resolved value is never logged.)
- `vault.entry_edited` — name, who edited.
- `vault.entry_deleted` — name, who deleted.
- `vault.entry_rotated` — name, who rotated.

The resolution events are high-volume — every skill execution that references a Vault entry produces one. Filter by `vault.entry_resolved` to find a misuse (a skill resolving a value at a frequency that doesn't match the expected workflow).

## When this isn't worth doing

For a single-developer hobby instance, the Vault is overkill. Paste secrets directly into skill bodies; you're the only person who reads them. The pain starts the moment a second person is involved — then the Vault is the difference between *"my key is now in three places I have to remember"* and *"my key is in one place."*

## When something fails

- **Skill returns "vault entry not found".** The skill is referencing a name that doesn't exist, or the calling user isn't authorised by the entry's scope. Check the name and the scope.
- **Vault returns "stuck deleting".** A dependent skill or MCP server is holding a reference. Open the entry's detail page, follow the dependents list, unwire them, retry.
- **Audit shows resolutions you can't explain.** A skill is referencing the entry that you didn't expect. Trace through the skill list filtered by `references vault://<name>`. If it's not a skill you authored, ask the author. If it's a skill nobody recognises, disable the entry immediately and investigate.
- **Edit value didn't take effect.** Skill executions started before the edit saw the old value; new executions see the new one. Cached executions in flight will finish with the old value. Wait a beat and retry.

## Where to go next

- **[Admin overview](./overview.md)** — the wider admin surface.
- **[Skills & Tools](../features/skills.mdx)** — how skills reference Vault entries.
- **[Teams and roles](./teams-and-roles.md)** — who's allowed to do what.

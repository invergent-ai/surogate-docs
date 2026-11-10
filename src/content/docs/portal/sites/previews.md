---
title: Preview a change
description: Show a change to a portal before it is saved, on a preview of its own, with fake people for each role and no real personal data.
---

A preview is the portal from a version of its site files, or from a folder you have not pushed yet. It has its own address and fake people only, so you, a reviewer or a coding agent can see the change as an employee, a manager or a partner would. It expires by itself.

## Make a preview

From a config folder on your machine:

```sh
portal preview create --dir ./portal-config --ttl 120
```

Or from a version of the site's files: `main` for the newest, or a version's id from the [Versions](/portal/console/versions/) page:

```sh
portal preview create main
```

The answer says:
- where the preview is: an address of its own, such as `https://p-7kc12n68t8.preview.example.ro`, with each site's address;
- until when it lives: a day unless `--ttl` gives other minutes, from 5 to a week;
- who is in it;
- how its sync went.

If the files have problems, the preview is kept with them, and the command lists them and exits 1. Fix them and [sync it](#sync-it-again).

A preview's first site by name is at its address, and each other site under its name, such as `/docs`. A portal keeps at most 10 live previews.

## Its people

Without anything more, a preview has three people:

| Person | Email | In |
| --- | --- | --- |
| Employee | `employee@preview.example` | |
| Manager | `manager@preview.example` | the group **Managers** |
| Partner | `partner@preview.example` | the organization **Partners** |

To use others, add `previews.yaml` at the top of the config folder:

```yaml
people:
  - { email: maria@example.com, name: Maria Ionescu, groups: [Managers], organizations: [Acme/HR], fields: { department: HR } }
  - { email: ion@example.com, name: Ion Popa }
groups: [Auditors]
```

- Every group and organization named is made, an organization's parents too: `Acme/HR` makes `Acme` and `HR` in it.
- `fields` are the portal's user fields.
- Every address must be on a domain kept for examples: `example`, `example.com`, `example.net`, `example.org`, `test`, `invalid`, `localhost`, or a domain under one of them. Any other address could be a real person's, so nothing is made. [`portal check`](/portal/sites/check-a-site/) says so before you try.
- Keep names and other details made up too.

People are made once, with the preview. A later sync keeps them, and says so when `previews.yaml` changed: make a new preview to use the new people.

## See it as one of its people

People in a preview have no password. Sign in as one from the command line:

```sh
portal preview sign-in <id> manager@preview.example
```

This prints a session cookie for the preview's address, for a browser or a script. A coding agent takes screenshots instead, through the portal's [MCP server](/portal/sites/agents/#connect-the-mcp-server):

| Tool | What it does |
| --- | --- |
| `create_preview` | makes a preview from a version or from a folder inside the agent's project |
| `list_previews` | the live previews |
| `sync_preview` | syncs one again, from its version, another version or a folder |
| `delete_preview` | deletes one now |
| `screenshot` | with `preview` and `as`, a picture of a preview's page as one of its people, such as `manager@preview.example` |
| `read_logs` | with `preview`, the preview's own sync history and audit log |

## Sync it again

```sh
portal preview sync <id>                     # its version again
portal preview sync <id> main                # the newest version, from now on
portal preview sync <id> --dir ./portal-config
```

A sync changes the preview's pages and apps; its people and its expiry stay as they are. A preview made from a folder needs a version or a folder each time.

## Its apps

A preview runs the apps its files name, with the approvals the portal itself gave them. An app the portal never approved waits, as it would in the portal. Apps are reached at public addresses, or at the addresses of apps the portal already approved.

A preview has its own issuer, which `create` answers with the keys' address. An app checks the issuer of what the portal sends it. So an app answers a preview only when it is set up with that preview's issuer, as an app under development is. An app set up for the portal refuses a preview's requests.

## When it ends

```sh
portal preview list
portal preview delete <id>
```

When a preview expires, its address answers nothing at once. Within ten minutes it is removed with everything in it: its people, sessions and logs.

## Who may make previews

Making previews needs a token with the **Make preview environments** [scope](/portal/console/tokens/#scopes). **Full access** does not include it. An administrator gives it by name, for example to a coding agent's [service account](/portal/console/service-accounts/), beside **Read how the portal is built**.

A token with only this scope reads nothing of the portal's people and changes nothing in the portal. The portal's audit log records each preview made, synced, signed in to and deleted.

Previews are served at an address your install's administrator sets. Without it, making a preview is refused with `previews_off`.

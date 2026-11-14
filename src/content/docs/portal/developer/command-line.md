---
title: The command line
description: The portal command, for the console's work from a terminal or a script.
---

The `portal` command does from a terminal what the console does, and moves a site's files in and out. It acts with a [token](/portal/console/tokens/), and can do only what the token's scopes allow. Give it the portal's address with `--url`. `portal --help` lists every command and names the variable it reads the token from. Every command takes `--json` for scripts.

## The site's files

```
portal config pull <dir>
portal config push <dir> -m "<message>" [--onto-latest]
portal config sync <tenant>
```

- `pull` and `push` move the site's files between a folder and the portal: see [Pull and push](/portal/developer/#pull-and-push).
- `sync` reads a tenant's kept files again and makes the newest version live, as **Make the newest version live** does on [Tenants](/portal/console/tenants/#kept-by-the-portal). It is for install administrators.

`portal check`, `portal dev` and `portal preview` work on a folder of your own: see [Check a site](/portal/developer/check-a-site/), [Develop locally](/portal/developer/develop-locally/) and [Preview a change](/portal/developer/previews/).

## Tokens

```
portal tokens create <name> --scope tenant:read
```

Without `--scope`, the token has only **Your own account**. See [My tokens](/portal/console/tokens/#scopes) for the scopes.

## Tenants

With an install administrator's token:

```
portal tenants add-admin <tenant> <email> --name "<name>"
```

See [Give a tenant an administrator](/portal/console/tenants/#give-a-tenant-an-administrator).

## Service accounts

With an administrator's token:

```
portal service-accounts create <slug> --name "<name>" [--role administrator]
portal service-accounts token <slug> <token name> --scope <scope>
portal service-accounts client <slug> --scope <scope> [--audience <app>]
```

See [Service accounts](/portal/console/service-accounts/).

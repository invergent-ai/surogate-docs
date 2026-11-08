---
title: Tenants
---

A tenant is a separate portal in the same install, with its own addresses, users, sign-in and settings. **Tenants** is for **install administrators**, on the main portal's console.

The list shows every tenant. The one marked **Default tenant** is the main portal: it answers on every address no other tenant has claimed.

## Create a tenant

1. Press **New tenant**.
2. **Slug**: a short name in lower-case letters, digits and hyphens, starting with a letter, such as `primaria-sector-1`.
3. **Name**: the tenant's name, as people know it.
4. Press **Create tenant**.

## Sites and addresses

Open a tenant to see its **Sites**. A site answers at one or more addresses: a domain name and, optionally, a path such as `/intranet`.

1. Press **New site** and give it a **Slug** and a **Name**.
2. Under the addresses, type a **Host** such as `www.example.ro` and, if you need one, a **Path prefix**. Press **Add address** for more.
3. Press **Create site**.

The tenant's console is then at `/_portal/admin/` on these addresses, and its administrators sign in there.

## Config

The **Config** card connects the tenant to the place its pages and apps are kept. Your implementation team gives you the **Repository address** and the **Branch or tag**. Press **Sync now** to bring in their latest changes: the card says whether the new config is live or what is wrong with it.

## Give a new tenant its first administrator

A new tenant has no users yet. Add its first administrator from the command line with an install administrator's [token](/portal/console/tokens/):

```
portal tenants add-admin <tenant> <email> --name "<name>"
```

The command prints a first password once. Give it to the person over a safe channel; they sign in on the tenant's console and change it there, or an administrator sets another one from [Users](/portal/console/users/#password).

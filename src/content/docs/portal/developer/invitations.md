---
title: Invitations
description: The invitations block of a site's file, which says whether its editors invite people, into which groups and for which email domains.
---

The configuration behind [Invitations](/portal/console/invitations/). That page covers inviting people, what the person sees, following the invitations sent and what happens to them later.

## Let a site's editors invite

A site says in its `site.yaml` whether its editors invite people, into which groups, and for which email domains.

In the site's `site.yaml`:

```yaml
invitations:
  editors: true
  groups: [Members]
  domains: [primarie.ro]
```

- `editors`: whether the site's editors invite people. When left out, only administrators do.
- `groups`: the groups, by name, that editors may invite people into, 10 at most. Names the portal does not have are left out.
- `domains`: when given, the email domains editors may invite, matched exactly: `primarie.ro` does not cover `mail.primarie.ro`.

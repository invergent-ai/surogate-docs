---
title: Who sees a page
description: Restrict a site, a page or a part of a page to signed-in people, a group, an organization or administrators.
---

Each site, page and placement (an app placed on a page) can say who may see it. You write it in the site's files, next to the page itself, so the change is reviewed and published like any other change to the site.

## Restrict a page

Add `permissions` to the page's file:

```yaml
path: /intranet
title: { ro: Intranet, en: Intranet }
layout: one-column
permissions:
  view: [group:Funcționari]
regions:
  main:
    - { id: news, app: content }
```

Only members of the group **Funcționari** see this page now. Everyone else:

- if they have not signed in, goes to the sign-in page, and back to the page afterwards;
- if they have signed in, sees **You do not have access to this page.**

## Who you can name

| Write | Means |
|---|---|
| `everyone` | anyone, signed in or not |
| `signed-in` | anyone who has signed in to this portal |
| `user:ana@example.ro` | one person, by email |
| `group:Funcționari` | the members of a [group](/portal/console/groups/) |
| `organization:Primăria/Direcția IT` | the members of an [organization](/portal/console/organizations/) and of every organization below it, named from the top, joined by `/` |
| `role:administrator` | the portal's administrators |

Put several in the list to let any of them in: `view: [group:Funcționari, organization:Primăria/Direcția IT]`.

A group or organization is named as it is in the console. If you rename it there, change the files too: a name that matches nothing lets nobody in.

## Sites, pages and parts of a page

- A **site**'s `permissions` apply to all its pages. Write them in `site.yaml`.
- A **page** can only narrow what its site allows. On a site for signed-in people, a page with `view: [everyone]` is still for signed-in people.
- A **placement** can only narrow its page. People who may not see it get the page without it:

```yaml
regions:
  main:
    - { id: list, app: content }
    - id: internal-notes
      app: content
      permissions:
        view: [group:Funcționari]
```

With no `permissions`, everyone may see the site, the page or the placement. `view: []` lets in only editors and administrators.

## Editors

`edit` names who may edit a site or a page:

```yaml
permissions:
  view: [signed-in]
  edit: [group:Redactori]
```

Editors and administrators always see what they edit. `everyone` and `signed-in` cannot be editors. Administrators can also add editors on the console's [Access](/portal/console/access/) page, which also checks who may see what, and why.

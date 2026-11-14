---
title: Who sees a page
description: Restrict a site, a page or a part of a page to signed-in people, a group, an organization or administrators.
---

Each site, page and placement (an [app](/portal/sites/apps/) placed on a page) can say who may see it. It is part of the site, so a change to it goes live like any other change to the site.

## What people see

A visitor who opens a page meant for people signed in goes to the sign-in page, and comes back to the page after signing in:

![The sign-in page, "Portal administration: Sign in to manage the portal", with Email, Password and the Sign in button, which a visitor reaches from a page for people signed in.](../../../../assets/screenshots/portal-permission-sign-in.png)

Someone signed in who may not see the page reads **You do not have access to this page.** A part of a page that someone may not see is simply left out: they get the page without it.

Administrators check who may see what, and why, on the console's [Access](/portal/console/access/) page:

![Check access for a person on the page main/intranet: Allowed, with the steps down to the group Funcționari.](../../../../assets/screenshots/portal-access-check.png)

## Restrict a page

A page can be limited to a group, such as the group **Funcționari**. Only its members see that page. Everyone else:

- if they have not signed in, goes to the sign-in page, and back to the page afterwards;
- if they have signed in, sees **You do not have access to this page.**

For now, this is set in the site's configuration: see [Developer: Who sees a page](/portal/developer/permissions/#a-page-for-a-group).

## Who you can name

A site, a page or a placement can name:

- **Everyone**, signed in or not;
- **Anyone signed in** to this portal;
- one person, by email;
- the members of a [group](/portal/console/groups/);
- the members of an [organization](/portal/console/organizations/) and of every organization below it;
- the portal's **Administrators**.

Name several to let any of them in.

A group or organization is named as it is in the console. If you rename it there, change where the site's configuration names it too: a name that matches nothing lets nobody in. For now, this is set in the site's configuration: see [Developer: Who sees a page](/portal/developer/permissions/#who-you-can-name).

## Sites, pages and parts of a page

- A **site**'s limits apply to all its pages.
- A **page** can only narrow what its site allows. On a site for signed-in people, a page open to everyone is still for signed-in people.
- A **placement** can only narrow its page. People who may not see it get the page without it.

With no limit set, everyone may see the site, the page or the placement. A list that names no one lets in only editors and administrators. For now, this is set in the site's configuration: see [Developer: Who sees a page](/portal/developer/permissions/#sites-pages-and-parts-of-a-page).

## Editors

A site or a page names who may edit it. Editors and administrators always see what they edit. Everyone, and anyone signed in, cannot be editors. Administrators can also add editors on the console's [Access](/portal/console/access/) page, which also checks who may see what, and why. The same settings, as files in the site's configuration, are in [Developer: Who sees a page](/portal/developer/permissions/#editors-and-bloggers).

## Bloggers

A site or a library names who may write [blog posts](/portal/sites/blogs/), their own only. Bloggers write posts of the blog types alone, and never change anyone else's posts or any other content; editors and administrators may blog too. Everyone, and anyone signed in, cannot be bloggers. The console's Access page adds editors, not bloggers. For now, this is set in the site's configuration: see [Developer: Who sees a page](/portal/developer/permissions/#editors-and-bloggers).

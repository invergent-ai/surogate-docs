---
title: Apps
---

An app puts something on the portal's pages: a news list, a form, a clock. Your implementation team builds or chooses the apps and [places them on pages](/portal/sites/apps/) in the site's files. **Apps** is where an administrator decides whether each app may run, and what it may know about the people using the portal.

![The Apps page: one app approved and one waiting, with their widgets, where they come from and what each asks to know.](../../../../assets/screenshots/portal-apps.png)

## What you see

For each app:

- its name, its version, the address it comes from, and its status;
- **Widgets**: the parts of a page it offers. A widget **rendered by the app's server** is made by the app and sent to the portal. A widget that **runs in the browser** is a program the visitor's browser loads from the app.
- where its widgets that run in the browser load their programs from;
- **What it runs on the portal's server**: its [hooks](/portal/sites/apps/#hooks), such as a check of each person created or changed on the console or through the API, and what it sees of them;
- **What it may know**: what the portal tells the app about the person looking at the page.

| It asks for | The portal tells the app |
|---|---|
| Nothing about the person | nothing |
| Who the person is | their id and name |
| Their email | their email address |
| Their profile fields | the profile fields your portal has |
| Their roles | their roles in the portal, such as administrator |

## Approve an app

An app shows nothing on the pages until you approve it. People who may edit a page see **This app is waiting for an administrator's approval.** where it would be. Visitors see the page without it.

1. Read what the app asks to know.
2. Press **Approve**. The dialog lists it again, with what it runs on the portal's server and the addresses it comes from.
3. Press **Approve** in the dialog. The app shows on the pages at once.

![The approval dialog lists what the app will be told.](../../../../assets/screenshots/portal-app-approve.png)

Approving decides what the portal **sends** the app, and what it may run on the portal's server. A widget that runs in the browser runs with the visitor's authority, like any program on the page, and a hook runs with what its app may know about people; the approval trusts the address the app comes from for whatever it serves there. Approve only apps you trust.

An app's check can refuse a change to a person, with a message on the field it names. If an app's checks stop working and block changes, **Revoke** its approval: its checks stop at once.

## When an app changes

The status says whether the app needs you again:

- **Approved**: it runs, and is told what you approved.
- **New permissions**: a new version asks to know more, or to run something new on the portal's server. What it adds is marked **New**. It shows nothing until you approve again.
- **Waiting for approval**: it has never been approved, or it now comes from another address. It shows nothing until you approve it.

A new version that asks for the same things, or less, stays approved. If the app changed while you were reading, approving it is refused: look at it again and approve what it is now.

If an app shows **Its manifest has not been read yet**, the portal has not yet read from the app what it offers. Whoever manages tenants presses **Sync now** on the tenant's [Config](/portal/console/tenants/#config) card.

## Revoke an app

Press **Revoke** and confirm. The app stops showing on the pages at once. Approve it again to bring it back. **Revoke** is there whenever an approval is held, also for an app waiting for new permissions.

When the site's files remove an app, its approval goes too. An app added later under the same name waits for approval.

Each approval and revoke is in the [audit log](/portal/console/audit/), with who did it and what the app was told.

Apps can also send and take [events](/portal/console/events/): an approval also decides what an app is told about the person an event is about.

## For the apps' developers

At the bottom of the page, **For the apps' developers** shows the portal's **Issuer** and **Keys** for this tenant. An app's developers set both in the app's configuration, so the app can check that each request comes from this portal. Give them these two values when they set up an app.

## Change a widget on a page

People who may [edit](/portal/sites/permissions/#editors) a page see a small menu on each widget:

- **Preferences** opens the widget's settings, such as a greeting or a number of items. Press **Save**, and everyone sees the change. A field left empty goes back to what the site's files say; a required one cannot be left empty. **Reset to defaults** goes back to what the site's files say for every field.
- **Help** shows the app's help for the widget, if it has one.
- **Back to the section** leaves the settings or the help.

The menu also has **Maximize**, so the widget fills the page, and **Minimize**, which leaves only its title. Anyone who sees a maximized or minimized widget, editor or not, can **Restore** it.

A change made with **Preferences** stays with that widget on that page. If the site's files remove the widget or put another one in its place, the change goes too.

---
title: Members and roles
---

The **Members** tab lists the people in your active project and what each of them may do. Every member has one of three roles: **Viewer**, **Editor** or **Owner**. Owners add people, change roles and remove members. Anyone can leave.

The tab is in Settings, at `/work/settings/members` (shared with Dev mode at `/studio/settings/members`). Every member of the project sees it. It always shows the active project, so switch projects first if you want another one (see [The project switcher](#the-project-switcher)).

## What each role can do

Roles rank Viewer, then Editor, then Owner. Each role can do everything the one before it can.

| What | Viewer | Editor | Owner |
|---|---|---|---|
| See the project's agents, datasets, knowledge bases, skills, models, training runs and evaluations | Yes | Yes | Yes |
| Create, edit and delete them, start and stop agents, run training and evaluations, save keys in the Vault. This covers anything that spends credits | No | Yes | Yes |
| Chat with an agent, or in the Playground | No | Yes | Yes |
| Open the project's **Sessions** (conversations) | No | Yes | Yes |
| Continue a session | No | Only sessions they started | Only sessions they started |
| See who is in the project, and leave it | Yes | Yes | Yes |
| Add or remove members, change roles, rename the project | No | No | Yes |
| See and cancel **Paused work** | No | No | Yes |
| Read the project's sign-in settings (**Authentication**) and change them | No | No | Yes |
| See the plan, credits and [usage](/work/settings/usage/) | Yes | Yes | Yes |
| Change the plan, update the payment method, top up, change add-ons | No | No | Yes |
| Set up payouts for [monetized agents](/work/monetize/) | No | No | Yes |
| Create, edit and delete a monetized agent's offers | No | Yes | Yes |

Platform administrators pass every one of these checks, in every project.

### Viewers

A viewer can look around but not touch. Controls that would change something are switched off, with the hint **Viewers can't change this project**. The chat, the Playground and the **Sessions** page show that message instead of their content.

**Viewers can't open the project's conversations.** A session holds a member's chat with the agent, and the platform keeps it from viewers entirely. Make someone an editor if they need to read sessions.

### Editors

An editor works in the project: builds and edits agents, runs training and evaluations, chats, and reads every member's sessions. An editor can't touch members, billing or the project's own settings. Billing controls show **Only owners can change this**.

### Owners

An owner can do everything an editor can, plus manage the people, the billing and the project's own settings. The person who creates a project is its first owner. A project always keeps at least one owner.

### Who can continue a session

Anyone who can read a session can open it, but only the person who started it can continue it. Sending a message, answering the agent, taking over its browser, and archiving or deleting the session are all limited to its starter. Everyone else sees **Only the person who started this session can continue it** under the chat box. A session started by one of your end users on a channel has no member as its starter, so members read it but don't continue it here.

The platform copilot's conversations are private to each person. Other members, including owners, don't see them.

## Adding someone

You need the **Owner** role.

1. Open **Settings**, then **Members**.
2. In the row above the table, type the person's username or email in **Username or email**.
3. Pick their role. The picker starts on **Editor**.
4. Choose **Add member**.

The person must already have a Surogate account. The match is exact, so a part of a name or email finds nothing. If the add is refused, the form keeps what you typed and shows why:

| Message | Meaning |
|---|---|
| **No account has that username or email.** | Nobody matches exactly. |
| **That account is deactivated.** | The account exists but is switched off. |
| **That person is already a member of this project.** | Change their role in the table instead. |
| **Surogate Hub could not be reached, so nothing changed. Try again.** | The change didn't go through. Try again. |

## The members table

The table shows each member's name, email, role, and when and by whom they were added. Owners also get a role picker on every row, and a **Remove** button on every row except their own. To leave yourself, use **Leave project** (below).

Change a role by picking another one in the row. It applies at once. You can change your own role, for example to hand ownership on and step down. Demoting the last owner is refused with **A project needs an owner. Make another member an owner first.**

Above the table, owners also see **Project name** with a **Rename** button.

Removing someone asks you to confirm, then takes away their access to the project. Adding, removing and changing roles are also applied to the person's groups in the project's [Data Hub](/develop/features/hub/).

## Leaving a project

**Leave project** is under the table, for every role. It asks you to confirm and then removes you from the project. Your schedules and missions in it are paused, and the project disappears from your list. If you were the only owner, you can't leave until you make another member an owner.

## Paused work

Work in a project runs as the person who started it. When that person can no longer run work there, the platform pauses it so it doesn't keep spending the project's credits. This happens when a member:

- is removed,
- leaves, or
- is made a **Viewer**.

Their running sessions, schedules and [missions](/work/tools/missions/) are all paused.

Promoting someone back to editor does **not** resume anything. Their paused work stays paused.

Owners see the paused schedules and missions in a **Paused work** list under the members table. It appears only when something is paused. Each row shows the **Kind** (Schedule or Mission), the **Title**, the **Member** and when it was **Paused**. Choose **Cancel** on a row, then **Cancel work** to confirm. A cancelled schedule or mission can't be resumed. Choose **Keep** to leave it as it is.

## The project switcher

In Dev mode, the top of the navigation shows the active project and your role in it. Choose it to open a list of your projects, each with your role. Pick one to switch. Everything in the app, including the Members tab, then shows that project.

The list ends with **New project**, which asks for a **Name** and a **Color**. You become its owner. In enterprise mode, only platform administrators are offered **New project**.

The Work navigation has no switcher. Work uses the project you last picked, which your browser remembers, so switch in Dev mode first.

## In enterprise mode

Enterprise installations differ in three ways. Only platform administrators create projects. The **Billing** tab is hidden. The **Authentication** tab is hidden too. Members and roles work as described above.

Platform administrators also get the **Users** and **Phone numbers** tabs in Settings. This page doesn't cover them.

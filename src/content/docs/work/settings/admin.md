---
title: Admin settings
---

Platform administrators get two more tabs in Settings: **Users**, to manage every account on the installation, and **Phone numbers**, the pool of numbers agents take for the [Voice channel](/work/channels/voice/). Nobody else sees them. This holds in every mode.

To be an administrator, a user needs the **Admin** role. Project roles (see [Members and roles](/work/settings/members/)) don't grant it.

## Users

**Users** lists every platform account, 25 to a page. These are the people who sign in to Surogate, not an agent's end users (see [Users](/work/channels/users/)). From here you can edit an account, change its billing, impersonate it, or switch it off or delete it.

Each row shows the username and display name, email, roles, how the user signs in (**Auth**), last login (**Never** if they haven't signed in) and when the account was created.

Find people with the search box, which matches username, email and name. Use the role filter to show only **Admin**, **Skill author**, **DevOps** or **Developer** accounts. **Clear filters** resets both.

Each row has four actions: **Edit**, **Billing**, **Impersonate** and **Delete**. On enterprise installations, a **New user** button sits next to the filters.

### Edit

**Edit** opens a dialog with these fields:

- **Display name**, **Email**, **Title**, **Company** and **Bio** (180 characters at most). The username can't be changed. For a user who signs in through Firebase, changing the email here doesn't change it in Firebase.
- **Transaction fee %**: Surogate's cut of each sale when this user [monetizes an agent](/work/monetize/). Leave it empty to use the platform default of 5%. Enter a number from 0 to 100, with up to two decimals.
- **Roles**: toggle **Admin**, **Skill author**, **DevOps** and **Developer**. Removing **Admin** from the last admin is refused.
- **Active**: clear it to switch the account off. The user keeps all their data but can't sign in. This is how you off-board someone, because deleting a user who owns projects is refused. The last admin and your own account can't be deactivated.
- **Reset password**, on enterprise installations only. It issues a one-time password, shown once, and signs the user out everywhere. They must change it at next sign-in.

### Billing

**Billing** opens the user's projects. Pick one if there is more than one; the dialog says so if the user isn't in any project. Changes apply to the project you picked, and **they don't call Stripe**. If the project has an active Stripe subscription, a banner warns that Stripe keeps billing the old plan and quantities until the subscription is cancelled or updated in the Stripe dashboard.

The dialog has four sections:

| Section | What it sets |
|---|---|
| **Plan** | Free, Standard, Pro, Max, Enterprise or Staff, then **Save plan**. |
| **Credits top-up** | For each of **Tokens**, **Browser minutes**, **Compute credits** and **Media credits**, it shows the plan balance and the top-up balance. Enter a whole number above zero and choose **Add**. |
| **Bring-your-own LLM** | A switch (**Active** or **Inactive**) with **Save BYO**. |
| **Add-ons** | The quantity of **Extra concurrent agents**, **Extra workspace GB** and **Extra hub GB**, then **Save**. On the Enterprise and Staff plans the section says add-ons have no effect. |

### Impersonate

**Impersonate** opens the app as that user, in Work. A banner at the top reads "You are impersonating" followed by their username, with a **Stop impersonating** button that returns you to **Users**. The button is switched off for your own row and for any user who is an admin.

### Delete

**Delete** asks you to confirm, then removes the account for good. It is refused for:

- your own account;
- the seed admin and the system copilot user;
- the last admin;
- a user who still owns projects or has memberships. Reassign or remove those first, or deactivate the account instead.

### New user

On enterprise installations, **New user** creates a local account. Enter a **Username** and **Display name**, and optionally an **Email** and a **Project** with the user's **Role in project**. Surogate shows a one-time password. Copy it then, because it isn't shown again, and the user must change it at first sign-in. SaaS installations don't have this button, because people sign up themselves.

## Phone numbers

**Phone numbers** is the pool of numbers that agents pick from when you [set up the Voice channel](/work/channels/voice/). Numbers are bought from the carrier by hand, so this is where they enter Surogate. Add a number once the carrier has assigned it to the platform's trunk.

To add one, type it in international format in **New number** (for example `+40371235713`), optionally give it a **Label**, and choose **Add number**. A number that is already in the pool is refused.

The table shows each number, its label and its **Agent**: the agent that holds it, or **Free**. Two controls act on a row:

- **Active** switches the number on or off. An inactive number is no longer offered to agents that don't have it. An agent that already holds it keeps it.
- **Remove** deletes it from the pool. A number an agent holds can't be removed. Disconnect it from that agent first.

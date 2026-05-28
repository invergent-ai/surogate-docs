---
title: Self-registration
sidebar_position: 6
---

# Let end users sign up for your agent

By default, only users you create by hand under [Users](./users.md) can sign in to one of your agents. Self-registration flips that: visitors land on the agent's login page, click *"Continue with Google"* (or sign up with email + password), verify their email, and walk straight into the agent.

Surogate doesn't run the sign-up system itself. You bring your own [Firebase Authentication](https://firebase.google.com/products/auth) project, point Surogate at it, and Firebase handles passwords, OAuth handshakes, password resets, and verification emails. Your end users' credentials live in your Firebase project — Surogate never sees them.

You only need to set this up **once per project**. After that, every agent in the project can be opted in or out individually.

## Who can use it

Self-registration is **available on the Standard plan and above**. Projects on the Free plan see the configuration screen but can't edit it — there's an inline upgrade prompt on the Settings tab.

You need to be the **project owner** to configure Firebase. Editors and viewers can see whether self-registration is on for an agent but can't change the project-level Firebase settings.

## The big picture

Three things to get right, in order:

1. **Create a Firebase project** in the Firebase Console and write down a handful of public config values.
2. **Paste those values into Surogate** under **Settings → Firebase Auth**. Pick which sign-in methods you want offered (Google, GitHub, Email/Password).
3. **Flip the toggle on each agent** under **Configure → Users → Allow self-registration**. Restart the agent so the new config is picked up by its web app.

## Step 1 — Create a Firebase project

1. Sign in to the [Firebase Console](https://console.firebase.google.com).
2. Click **Create a new Firebase project** and pick a name that reflects the audience for your agents (e.g. `acme-agents`).
3. Enable or disable Gemini / Google Analytics — your call. Neither affects self-registration.
4. Once the project is created, click the gear icon → **Project settings** → scroll to **Your apps** → click the **`</>` Web** button.
5. Give the web app a nickname, skip the Firebase Hosting offer, and register. Firebase shows you a config snippet that looks like this:

   ```js
   const firebaseConfig = {
     apiKey: "AIza...",
     authDomain: "acme-agents.firebaseapp.com",
     projectId: "acme-agents",
     appId: "1:1234567890:web:abcdef...",
     messagingSenderId: "1234567890"
   };
   ```

   Leave this tab open — you'll copy these values in the next step.

:::info
These values are **not secret**. Firebase web config is designed to ship in client code; the real security boundary is in Firebase's sign-in providers and authorized-domain list, not in hiding the `apiKey`. Pasting them into Surogate is safe.
:::

## Step 2 — Tell Surogate about your Firebase project

1. Open **Settings → Firebase Auth** (the card sits on the project Settings page; if it's missing you're on the Free plan — upgrade first).
2. Fill in:

   | Surogate field | Firebase value |
   |---|---|
   | Firebase project ID | `projectId` |
   | Auth domain | `authDomain` |
   | API key | `apiKey` |
   | App ID *(optional)* | `appId` |
   | Messaging sender ID *(optional)* | `messagingSenderId` |

3. Click **Save Firebase**. A green *configured* badge appears once the values stick.

The card stays editable — change a value and click *Save Firebase* again any time. Click *Remove Firebase* to disconnect (existing self-registered users keep their database rows but can no longer sign in until you re-add the config or issue them local credentials).

## Step 3 — Choose sign-in methods

Firebase has dozens of sign-in providers. Surogate surfaces three:

| Provider | What your user does | What you need to do |
|---|---|---|
| **Google** | Clicks *"Continue with Google"*, picks an account, done. | Nothing on the GitHub side — just enable Google in the Firebase Console. |
| **GitHub** | Clicks *"Continue with GitHub"*, authorizes the OAuth app, done. | Register a GitHub OAuth App and paste its Client ID + Secret into Firebase. See *Wiring GitHub* below. |
| **Email/Password** | Types email + password into the existing login form. | Toggle it on in the Firebase Console. Firebase manages the passwords. |

Toggle the providers you want on the Settings tab's *Providers* row.

:::warning
The Surogate toggles only control which buttons appear on your agent's login page. Each provider also has to be **enabled in the Firebase Console** under **Authentication → Sign-in method**. If a user clicks *Continue with Google* and you forgot the Console step, Firebase rejects the request with `auth/operation-not-allowed`.
:::

### Wiring GitHub (optional)

1. Go to [github.com/settings/developers](https://github.com/settings/developers) → **New OAuth App**.
2. Fill in:
   - **Application name** — what your users will see on the GitHub consent screen (e.g. *Acme Agents*).
   - **Homepage URL** — your agent's URL.
   - **Authorization callback URL** — Firebase shows this when you enable the GitHub provider; it looks like `https://<your-auth-domain>/__/auth/handler`.
3. Hit **Register application**, then copy the Client ID + generate a Client secret.
4. Back in Firebase Console → **Authentication → Sign-in method → GitHub** → paste the Client ID and Secret → **Save**.
5. Flip the GitHub switch on in Surogate.

## Step 4 — Authorize your agents' domains

Firebase only lets sign-ins happen from domains it knows about. By default it allows `localhost` and your Firebase project's own `*.firebaseapp.com` domain, which is enough for the Console preview but **not** for your real agent.

1. Firebase Console → **Authentication → Settings → Authorized domains**.
2. Add the public hostname where your agent's web app is served (e.g. `support.acme.com` or `agent-smith.cloud.surogate.ai`).

Skip this step and your users will see *"This domain is not authorized."* the moment they click any sign-in button.

## Step 5 — Turn the switch on for an agent

1. Open the agent you want self-registration enabled for.
2. **Configure** in the left nav → scroll to the **Users** section.
3. Flip **Allow self-registration**.

The switch is disabled until your project has a Firebase config saved. If you see an info icon next to a disabled switch, click it to jump straight to the Settings page.

Restart (or stop + start) the agent. Self-registration is picked up at deploy time, so the toggle won't take effect on the live web app until the agent restarts.

:::tip
You can have a mix: Agent A allows self-registration while Agent B stays admin-only. The Firebase project is shared across all your agents in the project, but each agent decides independently whether to surface the sign-up buttons.
:::

## What end users see

When self-registration is on, the agent login page shows:

- The familiar email + password form, with a **Sign in** button.
- Buttons for any social providers you enabled (Google, GitHub).
- A small **"New here? Create an account"** link below the form if you enabled Email/Password.

A first-time user can either click a social provider (one-tap, no password) or switch into create-account mode, type an email and password, and hit **Create account**.

### Email verification

When a user creates an account with Email/Password, Firebase sends them a verification email. Until they click the link in that email they can't sign in — the login page shows *"Check your inbox (and spam folder) for a verification email, then sign in again."* with a **Resend verification email** button next to it.

Once they verify, they sign in normally and land in the agent. Social sign-ins (Google, GitHub) are pre-verified by the provider, so those users skip the verification step entirely.

### Manual users still work

If you've created users by hand under [Users](./users.md), they keep signing in with their local password as before. Self-registration adds options on top — it doesn't replace anything.

## Troubleshooting

### Verification emails go to spam

Firebase sends from `noreply@<your-project>.firebaseapp.com`, a shared sender domain. Gmail and Outlook routinely flag it.

Fix it for good in the Firebase Console:

1. **Authentication → Settings → Public-facing name** — set this to a real name (e.g. *Acme Agents*).
2. **Authentication → Templates → Email address verification → ✏️ → Customize domain** — verify a subdomain you own (e.g. `auth.acme.com`). Firebase walks you through the DNS records to add.

After verification, the from-address becomes `noreply@auth.acme.com` signed with DKIM aligned to your domain — and emails land in the inbox, not spam.

For a fully custom email pipeline, set up an SMTP sender like SendGrid, Postmark, AWS SES, or Mailgun, and point Firebase at it under **Authentication → Templates → SMTP settings**.

### "Continue with Google" fails with `auth/operation-not-allowed`

You enabled the Google toggle in Surogate but not in the Firebase Console. Open **Authentication → Sign-in method → Google** in the Firebase Console, flip **Enable**, set a project support email, save. The Surogate toggle just controls whether the button appears; Firebase still needs to know the provider is allowed.

### "This domain is not authorized"

The hostname your agent's web app runs on isn't in Firebase's authorized-domains list. Add it under **Authentication → Settings → Authorized domains**.

### The toggle stays disabled even though I configured Firebase

Three things to check, in order:

1. **You're on the Free plan.** Self-registration requires Standard or above — the Settings tab shows an upgrade banner. Upgrade and the toggle becomes editable.
2. **You're not the project owner.** Editors and viewers can see the toggle but can't flip it. Ask the project owner.
3. **You configured Firebase but didn't save it.** Re-open **Settings → Firebase Auth** and confirm the green *configured* badge is showing. If not, click **Save Firebase**.

### Self-registered users were locked out after I removed Firebase

Removing the project's Firebase config also disables Firebase login. Their database row still exists — go to **Configure → Users → + ADD USER** and re-issue local credentials by entering the same email, or restore the Firebase config.

### A user complains they never got the verification email

On the login page, switch to create-account mode (you might already be seeing the notice from a recent attempt), then click **Resend verification email**. If that returns *"Too many attempts. Please wait a moment and try again."* — Firebase rate-limited; wait a few minutes.

Also worth telling them to check the spam folder, especially before you've set up a custom auth domain (see above).

## Removing self-registration later

Two scopes:

- **Stop offering it on one specific agent** — flip **Allow self-registration** off on the agent's Configure → Users section and restart the agent. People who already signed up for that agent keep working; only new sign-ups are blocked.
- **Stop offering it across the whole project** — click **Remove Firebase** on the Settings page. Every agent in the project goes back to admin-only login, and previously self-registered users can no longer authenticate via Firebase until you restore the config (their rows are preserved; you can issue them local credentials in the meantime).

The Firebase project itself is yours — Surogate doesn't touch it. Deleting your Firebase project deletes all your users; the same applies if you cancel Firebase billing.

## A word on security

- The Firebase web config you paste into Surogate is **public client config**, by design. Anyone who inspects your agent's web app can see it. Real protection comes from:
  - Firebase Authorized Domains restricting where sign-ins can happen
  - Provider-level OAuth client secrets that never leave Firebase
  - Surogate's own server-side check of every Firebase ID token before creating a session
- **Email verification is required** for any new email/password account. Surogate refuses to log in unverified users so a typo in the email field can't grant access to a stranger's inbox.
- **Manually-created users are isolated from Firebase users**, even when their emails match. Creating a manual user whose email is already linked to a Firebase account requires an explicit override so admins don't accidentally shadow a real signed-up user.

## What's next

If you want to charge those self-registered users for using the agent, see [Monetize your agents](../monetize.md). Otherwise loop back to [Improve your agent](../workflow/improve-agent.md).

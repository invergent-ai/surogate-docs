---
title: Sign in
sidebar_position: 1
slug: /getting-started/sign-in
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Sign in

Open **https://ops.surogate.ai/login** and pick one of these three options.

<video controls width="720" muted>
  <source src="/videos/01-sign-in.webm" type="video/webm" />
</video>

## Option 1 — Username or email + password

Use this if your admin created a local account for you, or if you already have a username/password.

1. Enter your **username or email** in the first field.
2. Enter your **password**.
3. Tick **Remember me** to stay signed in on this browser.
4. Click **Sign in**.

If the password was a temporary one set by your admin, you'll be redirected to **/change-password** on first sign-in. You must pick a new password to continue.

## Option 2 — Google or GitHub

Click **Google** or **GitHub** under "Or continue with". You'll be taken through your provider's normal OAuth flow. On your **first** sign-in via a provider, you'll then be sent to **/complete-signup** to pick a username and a fallback password — the username becomes your in-app identity and cannot be changed later.

## Option 3 — Sign up (Firebase email)

1. Click **Sign up** at the bottom of the form.
2. Enter your email and pick a password.
3. Check your inbox and click the verification link.
4. Return to **/login** and sign in with the same email + password.

## Forgot password

Forgot password is **only available for Firebase accounts** (signed up with email + password, Google, or GitHub).

1. Enter the **email address** on the account in the first field.
2. Click **Forgot password?**
3. Check your inbox. If the email is registered, a Firebase reset link will arrive.

If you signed up with a local username instead of an email, password reset must be done by an admin.

## What happens after sign-in

The app redirects to `/`, which then sends you to the surface matching your **perspective**:

- New users default to **Work mode** at `/work`.
- Builders / developers can switch to **Develop mode** at `/studio` from the **Work / Develop** toggle in the top bar.

If you haven't completed the 2-step welcome yet, you'll be sent to `/onboarding` first — see [First-run setup](./first-run).

## Error messages you may see

| Message | What it means |
|---|---|
| "Wrong password." | The username/email exists but the password didn't match. |
| "No account exists with this email." | No Surogate account is linked to that email. |
| "No account exists with this username." | The username isn't registered. |
| "Check your email and verify the account, then sign in again." | Firebase signup completed but the email isn't verified yet. |
| "Please enter both username/email and password" | One of the two fields is empty. |
| "Enter your email address above to reset your password." | Forgot-password requires an email, not a username. |
| "Password change required" (403 from the API) | Your account is on a temporary password — finish the change-password flow first. |

More error messages are catalogued in [Reference → Error messages](../reference/errors).

## Related

- [First-run setup](./first-run)
- [The five-minute tour](./tour)
- [Where to find things](./where-to-find-things)

---
title: Sign in with your organisation account
sidebar:
  label: Sign-in providers
---

On **Sign-in**, an administrator connects the portal to your organisation's accounts, such as Microsoft Entra ID, Keycloak or Google Workspace. People then sign in with the account they already have. The portal uses OpenID Connect, which these services all offer.

## Before you start

Register the portal as an application with your organisation's sign-in service. You need from it:

- the **issuer**: the service's https address, such as `https://login.microsoftonline.com/<your directory>/v2.0`;
- a **client ID** and a **client secret** for the portal.

The service asks you for the portal's **callback URL**. The console shows it while you add the provider (step 3 below), so you can copy it from there.

## Add a provider

1. On **Sign-in**, press **New provider**.
2. **Display name**: the name on the sign-in button, for example "Entra ID" for **Continue with Entra ID**.
3. **Slug**: a short name in lower-case letters, digits and hyphens, such as `entra`. As soon as you type it, the console shows the **Callback URL**. Press **Copy** and register it with your sign-in service.
4. **Issuer**, **Client ID** and **Client secret**: from your sign-in service.
5. **Scopes**: leave `openid email profile` unless your service asks for others. They must include `openid`.
6. **Create the account at first sign-in**: on, anyone your service lets in gets an account the first time they sign in. Off, only people you already added as [users](/portal/console/users/) can sign in.
7. **On**: untick it to keep the provider ready but hidden from the sign-in page.
8. Press **Add provider**.

People are matched by email: someone whose organisation email is already a user of the portal signs in as that user.

## Change or delete a provider

Press a provider in the list to edit it. The **Client secret** field is empty: leave it empty to keep the saved secret, or type a new one to replace it. Press **Save**.

To delete it, press **Delete provider** in the same window and confirm. People can no longer sign in with it; their accounts stay, and they can still sign in with a password if they have one.

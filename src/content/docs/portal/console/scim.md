---
title: SCIM provisioning
description: Let Microsoft Entra ID, Okta or another identity system create, update and disable the portal's people and groups.
---

With SCIM, your identity system keeps the portal's people and groups up to date by itself: people it assigns to the portal get an account, changes to their name or email follow, and people it removes are disabled.

## Connect your identity system

1. On **Directories**, in the **SCIM provisioning** card, press **New SCIM token**.
2. Name it after the system that will use it, such as "Entra ID", and press **Create token**.
3. Copy the token and the **SCIM address**: the token is shown this once.
4. In your identity system's provisioning settings, enter the SCIM address as the tenant URL and the token as the secret token.

## What SCIM does here

- A person the identity system creates gets an account with their email. If someone already has that email in the portal, SCIM takes over their account, except an administrator's.
- Turning a person off, or deleting them, in the identity system disables them in the portal. Their account stays. If the identity system creates them again, they get the same account back.
- People are found by the user name the identity system sends, even when it is not an email.
- Groups the identity system pushes appear in **Groups**; only SCIM changes their members and names. A pushed group with the name of a group you made by hand takes that group over.
- A person from SCIM has their name and email managed by the identity system. They sign in with a sign-in provider, often the same system through [SAML or OpenID Connect](/portal/console/sign-in-providers/).

Revoke a token with **Revoke** in the card. The system that uses it can no longer provision anyone.

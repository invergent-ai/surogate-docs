---
title: Surogate Portal
sidebar:
  label: Welcome
---

Surogate Portal runs an institution's websites and portals: the public site, the intranet, the services people use after they sign in. One install can hold many portals, each with its own addresses, people and settings. These portals are called **tenants**.

Every portal has a **console** at `/_portal/admin/` on its own address, for example `https://www.example.ro/_portal/admin/`. In the console, the portal's administrators manage:

- **Users**: the people who can sign in, with their roles and passwords.
- **Groups**: sets of people you give the same access.
- **Organizations**: your structure of departments, offices and teams.
- **Sign-in**: the organisation accounts people can sign in with, such as Microsoft Entra ID or Keycloak.

Everyone who signs in to the console also has **My tokens**, for the command line and for scripts.

## Who this guide is for

- **Administrators** of a portal: the people who manage its users and sign-in.
- **Install administrators**: the people who run the whole install and create its tenants.
- Anyone who needs a token for the command line.

Start with the [quickstart](/portal/quickstart/). The roles are explained in [Roles](/portal/reference/roles/).

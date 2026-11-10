---
title: Connectors
description: Setting, removing and testing the credentials of the portal's connectors.
---

**Connectors** shows administrators the portal's [connectors](/portal/sites/connectors/), grouped by their `group`. Each shows its name, its address, how it signs in, and whether it is connected. A connector each person connects themselves shows how many people did.

## Set credentials

**Set credentials** asks for what the connector's sign-in needs: a token, a user name and password, a key, or a secret. They are kept sealed, and they are never shown again. To change them, set them again. **Remove** forgets them, after asking; actions that use the connector then fail until it is connected again.

Credentials hold to the connector as it was when they were set. If its address or sign-in changes in the portal's files, it shows **Not connected** until they are set again.

## Test

**Test** calls the connector's test path with its credentials, and says what it answered and how long it took. A connector can be tested once every 2 seconds.

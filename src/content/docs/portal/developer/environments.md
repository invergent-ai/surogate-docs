---
title: Environments
description: The environments file that names the portals a portal sends versions to, and the connector that holds each key.
---

The configuration behind [Environments](/portal/sites/environments/). That page covers sending a version from one portal to another, what travels, and how the key is made.

## The environments file

In `environments.yaml`, at the top of the portal's files:

```yaml
production:
  name: { ro: Producție, en: Production }
  url: https://portal.primaria.ro
  key: production-key
```

The key's connector is a file of its own, `connectors/production-key.yaml`:

```yaml
name: { ro: Cheia pentru Producție, en: Key for Production }
kind: secret
```

- `production`: the environment's id.
- `name`: what the console calls it.
- `url`: the other portal's address.
- `key`: the secret connector holding the key, here `production-key`.

The rules for each key:

- The id (`production`): lowercase letters, digits and dashes, starting with a letter. At most 10 environments.
- `name`: what the console calls it, in Romanian, English or both.
- `url`: the other portal's address, with no path. Inside the same cluster, its service address works too, such as `http://portal.portal.svc`.
- `key`: a secret [connector](/portal/developer/connectors/#a-connectors-file) of this portal, holding the key Production takes the version with.

The key opens only for the address `environments.yaml` names. If the address changes, set the key again. The key is for sending versions alone: no action may use it, and Keel, the DMS or an agent may not name it too.

Once the file is published, make the key as [Make the key](/portal/sites/environments/#make-the-key) says, and set its value on Test under **Connectors**, as the secret of the connector `environments.yaml` names.

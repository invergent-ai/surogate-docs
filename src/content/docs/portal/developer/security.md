---
title: RSA keys and DKIM checks
description: The generateRsaKeys and verifyDkim actions, and a web connector signing in as a Google Cloud service account, as the site's configuration writes them.
---

What these do, and their limits, are on [RSA keys and DKIM checks](/portal/sites/security/) and [Connectors: Google APIs](/portal/sites/connectors/#google-apis).

## Make a key pair

```yaml
- type: generateRsaKeys
  bits: "2048"
  keepIn: dkim-key
  into: keys
```

`keepIn` names a secret connector (`kind: secret`) where the private key is sealed. `into` keeps `{publicKey, dkimRecord}`. `bits` is an expression: 2048, 3072 or 4096; 2048 when left out.

## Check a DKIM record

```yaml
- type: verifyDkim
  domain: vars.domain
  selector: "'mail'"
  publicKey: vars.keys.publicKey
  into: dkim
```

`into` keeps `{found, records, revoked, matches, record}`; `matches` is null without `publicKey`.

A form with `public: true`, or an endpoint with `access: public` or a `cache`, may not use either: `security_public`.

## A Google service account connector

In `connectors/sheets.yaml`:

```yaml
name: { ro: Foi, en: Sheets }
kind: http
baseUrl: https://sheets.googleapis.com/v4
auth:
  type: google
  scopes:
    - https://www.googleapis.com/auth/spreadsheets
  subject: ana@primaria.ro
```

- `baseUrl`: https on `googleapis.com`. `scopes`: 1 to 20. `subject`: optional, the Workspace person it acts as. `perUser` is not taken.
- A connector with a `subject` is never called from what anyone may reach: `google_public`.
- Its credential is `serviceAccountKey`, the key's JSON file, set in the console.

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

## Encrypt and decrypt

```yaml
- type: aesEncrypt
  connector: cheie-cnp          # a secret connector of 32 bytes in base64
  text: form.cnp
  aad: "'responsabil-1'"        # optional associated data
  inputEncoding: text           # or base64
  into: cnpCriptat
- type: aesDecrypt
  connector: cheie-cnp
  text: vars.cnpCriptat
  aad: "'responsabil-1'"
  outputEncoding: text          # or base64
  into: cnp
- type: rsaEncrypt
  connector: rsa-insp           # a secret connector with the pair; or publicKey: "-----BEGIN PUBLIC KEY-----…"
  text: form.mesaj
  into: sigilat
- type: rsaDecrypt
  connector: rsa-insp
  text: vars.sigilat
  into: mesaj
```

`connector` is a reference, never an expression. AES output is base64 of `IV(12) ‖ ciphertext ‖ tag(16)`. RSA is OAEP with SHA-256. `rsaEncrypt` takes `connector` or `publicKey`, one of the two. `aesDecrypt` and `rsaDecrypt` are refused in a public form or endpoint, and take an optional `who`, an expression for a list of up to 20 principals (`"['group:HR', 'user:ana@example.ro']"`) that alone may read the text. What they return is replaced by `[sensibil]` in the run's log, in its errors and in the outcome kept in the history.


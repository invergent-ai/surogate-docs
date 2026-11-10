---
title: Connectors
description: Named connections to outside services that action lists use by name; their credentials are set in the console, never written in files.
---

A connector is a named connection to a service outside the portal: a CRM, a payments provider, a public register. [Action lists](/portal/sites/actions/) and [logic flows](/portal/sites/flows/) use it by name. Where it goes and how it signs in are written in the portal's files. Its credentials are set in the console, and are never written in files.

## A connector

A connector lives in `connectors/<id>.yaml`:

```yaml
name:
  ro: CRM
  en: CRM
group: sales
kind: http
baseUrl: https://crm.example.ro/api/v2
auth:
  type: bearer
timeoutMs: 3000
test:
  method: GET
  path: /ping
```

- `kind`: `http` for a service the portal calls. `secret` for a key the portal signs with, which makes no calls.
- `baseUrl`: where every call starts, with http or https, and with no query or credentials in it.
- `auth`: how calls sign in:
  - `none`;
  - `bearer`: a token;
  - `basic`: a user name and password;
  - `{ type: header, name: X-Api-Key }`: a key in a header.
- `timeoutMs`: how long a call waits, at most 10,000 ms. It is 5,000 when left out.
- `group`: groups connectors in the console.
- `test`: the connection test, a GET or HEAD to a path under the base address.
- `perUser: true`: each person connects their own account. See [Each person's own account](#each-persons-own-account).

## Credentials

Administrators set a connector's credentials under [Connectors](/portal/console/connectors/). They are kept sealed, and they are never shown again or written in a run's log.

Credentials belong to the connector as it was when they were set. If the base address, the auth or the header changes in the files, the connector counts as not connected until its credentials are set again. A change to the files can never send them somewhere else.

Credentials go only over https, unless the portal is installed to reach private networks.

## Call a service

```yaml
- type: http
  connector: crm
  method: POST
  path: '"/clients/" + form.client'
  query:
    lang: locale
  body: "{'name': form.name, 'email': form.email}"
  into: answer
- type: message
  text:
    ro: "Client {{ vars.answer.body.id }}"
    en: "Client {{ vars.answer.body.id }}"
```

- **The call:**
  - `method` is GET (when left out), POST, PUT, PATCH or DELETE.
  - `path` is added under the base address. It can never climb above it or reach another site.
  - `query` values are text, numbers or true or false.
  - `headers` may add headers of your own, but not the sign-in header or the request's own.
  - `body` goes as JSON when it is an object or list, and as text when it is text. GET and DELETE send none.
- **The answer** lands in `vars.<into>` as `status`, `headers` and `body`. A JSON body is read into values.
- **When it fails:**
  - An answer that is not 2xx is an error, unless its status is listed in `okStatus`. The answer is still kept, so `onError` can read it.
  - The portal does not follow redirects.
  - It does not reach private network addresses unless it is installed to.
- **Limits:**
  - a call stops at the connector's `timeoutMs`;
  - an answer or body is at most 1 MB;
  - a run makes at most 20 calls.

## Email

```yaml
- type: email
  to: form.email
  subject: '"We received your request"'
  text: '"Your reference is " + vars.reference'
```

- **Addresses:** `to` is an address or a list of them. A run sends to at most 10 addresses, or 2 when nobody is signed in.
- **When it goes:** the email leaves only once the whole run ends well. If a later action fails, nothing is sent.
- **Limits:** a portal sends mail to at most 500 addresses an hour.
- **When nothing can be sent:** if the portal has no mail server, the action fails with "The portal sends no email."

## Hashes, signatures and random values

| Type | What it does | Takes |
|---|---|---|
| `hash` | A sha256, sha384 or sha512 hash | `algorithm`, `from`, `encoding` (`hex` or `base64`), `into` |
| `hmac` | A signature with a `secret` connector's key, at least 32 bytes long | `connector`, `algorithm`, `from`, `encoding`, `into` |
| `randomToken` | 16 to 64 random bytes, as text | `bytes` (32 when left out), `into` |
| `uuid` | A random id | `into` |

`hmac` signs whatever the list gives it. Do not sign what a visitor typed unless that is the point.

## Each person's own account

A connector with `perUser: true` signs in as each person, with the account they connected under **Your connections** on their [account](/portal/console/account/#your-connections). When nobody is signed in, or the person has not connected, the action fails with "The connector is not connected."

A [named value](/portal/sites/values/) kept for the whole portal or a site never uses a person's own connector. No named value sends email.

## In tests

A [flow's tests](/portal/sites/flows/#tests) never reach out. Each web call is answered by the test's `mocks`, and each email is listed in the result, never sent:

```yaml
tests:
  - name: finds the client
    inputs: { id: "7" }
    mocks:
      crm:
        - method: GET
          path: /clients/7
          body: { name: Ana }
    expect:
      outputs: { name: Ana }
```

A mock matches the call's method and its path, without the query. A call that no mock answers fails the test. In a test, `hmac` signs with a fixed test key, never the connector's secret.

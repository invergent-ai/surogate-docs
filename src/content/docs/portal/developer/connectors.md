---
title: Connectors
description: The files that define a portal's connectors, and the actions that call a service, send mail, texts and Slack posts, or sign.
---

The configuration behind [Connectors](/portal/sites/connectors/). That page covers what the console shows of a connector, how its credentials are set and tested, and what each kind of connector does.

## A connector's file

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
- `perUser: true`: each person connects their own account. See [Each person's own account](/portal/sites/connectors/#each-persons-own-account).

The other kinds of connector:

- `mailbox` is a mail address a [job](/portal/sites/jobs/#when-mail-arrives) reads (see [A mailbox's file](#a-mailboxs-file));
- `mail` is a mail account (see [A mail account's file](#a-mail-accounts-file));
- `sms` and `slack` send text messages and Slack posts (see [A text message and a Slack post](#a-text-message-and-a-slack-post));
- `bucket` names a bucket of an S3-compatible storage service (see [A bucket's file](#a-buckets-file));
- `ftp` is an FTP, FTPS or SFTP server (see [A file server's file](#a-file-servers-file)).

A connector with `perUser: true` signs in as each person, with the account they connected under **Your connections**. When nobody is signed in, or the person has not connected, the action fails with "The connector is not connected."

Credentials are never written in these files. They are set in the console, and hold to the connector as it was when they were set: if its `baseUrl`, `auth` or header changes, it counts as not connected until they are set again.

## Call a service from an action list

In an action list, such as a form's `actions`:

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

## Send an email from an action list

```yaml
- type: email
  to: form.email
  subject: '"We received your request"'
  text: '"Your reference is " + vars.reference'
```

- `to` is an address or a list of them. A run sends to at most 10 addresses, or 2 when nobody is signed in.
- `subject` and `text` are expressions.

Through your own mail account, with a file:

```yaml
- type: email
  connector: town-mail
  to: form.email
  subject: '"Your certificate"'
  text: '"The certificate is attached."'
  attachments:
    folder: certificates
    names: '["adeverinta-" + vars.number + ".pdf"]'
```

- `connector`: a mail account connector.
- `attachments.folder`: the folder the files are in; `attachments.names`: an expression giving their names, as a list.
- **Your own mail account:** with `connector`, the email goes out through one of your [mail accounts](/portal/sites/connectors/#mail-accounts) instead of the portal's mail server, as its sender.
- **Files:** `attachments` attaches up to 10 files of a [folder](/portal/console/files/), at most 10 MB together, or 2.5 MB through Microsoft 365. They go as they were when the run ended, even if they change before the email leaves. Only the folder's editors can attach its files: a form a visitor sends that attaches files fails, and sends nothing.

## A text message and a Slack post

`sendSms` sends a text message through Twilio or Clickatell, and `slackMessage` posts to a Slack channel, each through its connector. Their limits are on [Text messages and Slack](/portal/sites/connectors/#text-messages-and-slack).

```yaml
- type: sendSms
  connector: sms
  to: form.phone
  text: '"Cererea " + vars.number + " a fost înregistrată."'
- type: slackMessage
  connector: team
  text: '"Cerere nouă: " + vars.number'
```

In `connectors/sms.yaml`, a Twilio account, and in `connectors/team.yaml`, a Slack webhook:

```yaml
name: { ro: SMS primărie, en: Town texts }
kind: sms
provider: twilio
from: "+40700000000"
accountSid: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

```yaml
name: { ro: Echipa, en: Team }
kind: slack
```

- `provider`: `twilio` or `clickatell`.
- `from`: the sender: an international number; for Twilio also a Messaging Service's SID (`MG…`); for Clickatell also a name of 3 to 11 letters and digits.
- `accountSid`: Twilio's account SID, as its console shows it.
- A connector of kind `sms` names Twilio or Clickatell and the sender: a number, a Twilio Messaging Service, or a Clickatell sender name. Set Twilio's auth token or Clickatell's API key under **Connectors**; **Test** reads the account without sending anything.
- A connector of kind `slack` is a Slack incoming webhook. Create one in Slack for the channel, and paste its address, `https://hooks.slack.com/services/…`, under **Connectors**. It has no Test: a test would show in the channel.

## Hashes, signatures and random values

| Type | What it does | Takes |
|---|---|---|
| `hash` | A sha256, sha384 or sha512 hash | `algorithm`, `from`, `encoding` (`hex` or `base64`), `into` |
| `hmac` | A signature with a `secret` connector's key, at least 32 bytes long | `connector`, `algorithm`, `from`, `encoding`, `into` |
| `randomToken` | 16 to 64 random bytes, as text | `bytes` (32 when left out), `into` |
| `uuid` | A random id | `into` |

`hmac` signs whatever the list gives it. Do not sign what a visitor typed unless that is the point.

## A mail account's file

In `connectors/<id>.yaml`, a Microsoft 365 account:

```yaml
name: { ro: Poșta primăriei, en: Town mail }
kind: mail
provider: microsoft365
from: anunturi@primaria.ro
directory: 3f2a9c4e-0d1b-4e7a-9b5c-8d6e7f001122
clientId: 7c1e5a2b-4f3d-4c9e-8a7b-6d5e4f003344
```

- `provider`: `smtp`, `microsoft365` or `google`.
- `from`: the address the email is sent from.
- `directory` and `clientId`: Microsoft 365's directory (tenant) id and the app's id, as Microsoft Entra shows them.
- `fromName`: the sender's name, in Romanian and English (SMTP and Google).
- `timeoutMs`: how long the service may keep the portal waiting, up to 60,000 ms; 30,000 when left out.

An SMTP server takes `host`, `port` (587 when left out) and `security`: `starttls` (when left out), `tls` (port 465), or `none`, only for a server on your own network. Google Workspace takes only `provider` and `from`.

## A mailbox's file

In `connectors/<id>.yaml`:

```yaml
name: { ro: Cereri prin e-mail, en: Requests by email }
kind: mailbox
protocol: imap        # or pop3
host: mail.primaria.ro
folder: INBOX         # IMAP only; INBOX when left out
```

- `protocol`: `imap` or `pop3`.
- `host`: the mail server.
- `folder`: the folder to read; IMAP only, `INBOX` when left out.
- **Port:** 993 for IMAP and 995 for POP3 when left out.
- **Security:** `tls` by default. IMAP also takes `starttls`. The mail server needs a certificate the portal trusts, and `none` works only for a server on your own network when the portal allows that.

## A bucket's file

In `connectors/<id>.yaml`:

```yaml
name: { ro: Arhiva în cloud, en: Cloud archive }
kind: bucket
endpoint: https://s3.eu-central-1.amazonaws.com
bucket: primaria-archive
region: eu-central-1
```

- `endpoint`: the service's address, `https://` and a host, with no path. For Cloudflare R2: `https://<account id>.r2.cloudflarestorage.com`.
- `bucket`: the bucket's name, as the service shows it.
- `region`: the bucket's region; `auto` when left out, as R2 takes.
- `virtualHosted`: `true` to reach the bucket as a host of its own (`primaria-archive.s3.example.com`); left out, it is part of the path, which most services take.
- `timeoutMs`: how long one request waits, up to 60,000 ms; 30,000 when left out.

A bucket connector takes no `baseUrl`, `auth`, `test` or `perUser`: it is the portal's own.

## A file server's file

In `connectors/<id>.yaml`, an SFTP server:

```yaml
name: { ro: Server registratură, en: Registry server }
kind: ftp
protocol: sftp
host: sftp.primaria.ro
hostKey: SHA256:f2IO2+GZU5y3N8JriSY+2TfVUBjyih6+yr7OnJVUFt8
directory: /registratura
```

- `protocol`: `sftp`, or `ftp` for FTP and FTPS.
- `host`: the server's name or address, with no scheme or port.
- `hostKey`: the server's key fingerprint, as `ssh-keygen -lf` prints it, or a list of up to five.
- `directory`: where the actions' paths start; when left out, where the server signs in.
- `auth: key` signs in with a private key instead of a password.
- `port`: 22 for SFTP when left out.
- `timeoutMs`: how long the server may keep the portal waiting, up to 60,000 ms; 10,000 when left out.

An FTPS server:

```yaml
name: { ro: Server FTP, en: FTP server }
kind: ftp
protocol: ftp
host: ftp.primaria.ro
security: starttls
```

- `security`: `starttls` (when left out) secures the connection after it opens; `tls` secures it from the start, on port 990; `none` sends everything in clear, only to a server on your own network.

A file server connector takes no `baseUrl`, `test` or `perUser`: it is the portal's own.

## A test that mocks the service

In a flow's file (`flows/<id>.yaml`), under `tests`:

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

- `mocks`: for each connector, the answers its web calls get, by `method` and `path`.
- `body`: what the mock answers.
- `expect`: what the test must see.

A mock matches the call's method and its path, without the query. A call that no mock answers fails the test. In a test, `hmac` signs with a fixed test key, never the connector's secret.

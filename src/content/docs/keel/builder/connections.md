---
title: Connections and credentials
sidebar:
  label: Connections
---

A **connection** is another system a case type's [system steps](/keel/builder/steps/#a-system) call: its base URL, how calls authenticate, and the credential they send. Connections belong to the case type, so the case's history shows the case type making the call, not a borrowed account. The **Connections** tab holds them.

## The list

The left of the tab lists the case type's connections by name, each with its base URL. In a draft, the list is the draft's; with no draft open, it is the published connections, read-only. Editors and owners press **New connection** and give it a name: "It is made in the draft. Its calls need a base URL next."

## A connection

| Setting | What it is |
|---|---|
| **Base URL** | Where every call of the connection goes, such as `https://core.example.com/api`. A step's path is added to it. |
| **Authentication** | **None**, **API key**, **Basic**, **Bearer token** or **OAuth2 client credentials**. |
| **Header** | For an API key: the header the key is sent in. |
| **Token URL**, **Scope**, **Audience**, **Client authentication** | For OAuth2 client credentials: where Keel gets a token, the scope and audience it asks for, and whether the client authenticates by **basic** or **post**. |
| **Idempotency-key header** | The header that carries each write's idempotency key, so the system can tell a retry from a new request. "Empty for none." |
| **Default timeout (seconds)** | How long a call may take when its step does not say. |

A connection that sends a credential must use `https`; the dry run refuses one that does not.

These settings are part of the draft and are published with it.

## Credentials

The credential is the secret a connection sends: an API key, a username and password, a bearer token, or an OAuth2 client's ID and secret. Credentials are not part of any draft: they are set on the **published** connection, and apply at once.

Under **Credentials**, editors and owners see:

- **Set credential**, or **Replace credential** when one is set. The dialog, **Set the *kind* credential of *connection***, asks for the secret's parts. "Keel keeps it sealed for the connection's hosts. It is not shown again." After you save, the tab says **Credential set. It is not shown again.**
- **Delete credential**, which asks first: "Calls that need it fail until a new one is set."

Each credential shows its kind, the hosts it is sent to, and who set it and when. A credential is sent only to the hosts the connection had when it was set: after you publish a connection with a base URL on another host, set its credential again.

When the connection is new in a draft, the section says **Publish this connection before setting its credential.** A connection that authenticates with **None** says **It sends no credential.**

If your installation keeps no credentials, the tab says **Credentials are off in this installation.** Ask your administrator.

## Who changed credentials

Under the connections, **Who changed credentials** lists the case type's credential changes, newest first: who set, replaced or deleted which credential, of which connection, for which hosts, and when. With none, "No one has changed a credential of this case type yet."

## A process's connections

A [BPMN process](/keel/processes/) calls other systems through connections of its own, the files `process-connections/<process>/<name>.json`. A process's connection holds the settings above. It is made and changed in a draft on the **Connections** tab of the process's page, as [Processes](/keel/builder/processes/#the-connections-tab) says, and is published with it. It is not a case type's: this tab never lists it, and a case type and a process of one key keep their connections and credentials apart. Keel's list of connections names a process's as `process:<process>/<name>`.

Its credentials are set on the published connection, as a case type's are, on the **Connections** tab of the process's page, [Processes](/keel/builder/processes/#the-connections-tab): the same **Set credential**, **Replace credential** and **Delete credential**, and the list of who changed them. The API sets and deletes them at `/api/build/projects/{project}/processes/{process}/connections/{name}/credentials/{kind}`, with `PUT` and `DELETE`: see [A process's connections](/keel/processes/#calling-other-things).

---
title: API endpoints
description: The portal's own REST endpoints, written as files, each running a list of actions and answering as they say.
---

An API endpoint answers other programs, apps and pages at an address of the portal: a count of requests, a list of open cases, a record added from another system. It is written as a file, runs a list of [actions](/portal/sites/actions/), and answers as they say.

## Write an endpoint

Each endpoint is a file `endpoints/<id>.yaml`:

```yaml
path: /requests/count
method: GET
access: public
parameters:
  status: { type: text, required: true, max: 40 }
actions:
  - type: findRecords
    model: requests
    where: { status: params.status }
    into: found
  - type: respond
    body: '{"count": size(vars.found)}'
onError:
  - type: respond
    status: 400
    body: '{"error": error.message}'
```

It is called at `https://<your portal>/_portal/endpoints/requests/count?status=new`.

- `path` is lower-case words joined by `/`. `method` is GET, POST, PUT, PATCH or DELETE. Two endpoints may share a path when their methods differ.
- `description` says what it is for, in the console.

## Parameters

`parameters` names what a call gives, each with its `type`:

| Type | A value such as |
|---|---|
| `text` | `new` (at most `max` characters, 1000 when left out) |
| `number` | `12.5` |
| `integer` | `12` |
| `boolean` | `true` |
| `date` | `2026-11-10` |
| `uuid` | a record's id |
| `json` | any JSON |

A GET or DELETE call gives them in the address; the others in a JSON body. A parameter the endpoint does not take, one given twice, one of the wrong type, or a required one missing is refused with 400 before anything runs. One not given is `null`.

## Its actions and its answer

The actions read `params`, the person calling as `user`, `vars` and `values`, and may call [flows](/portal/sites/flows/). The answer is the `respond` action's:

- `body` gives JSON, with `status` (200 by default);
- `kind: text` gives the body as text;
- `kind: redirect` with `to` sends the caller to a page of the site, or to an address `redirects` names.

Nothing after `respond` runs. With no `respond`, the answer is empty (204). When the list fails, `onError` runs, reading `error.message`; without an answer from it, the caller gets a 500 with the action's error message.

An endpoint never sends mail and never signs with a connector's secret. A GET endpoint, and one anyone may call, never adds, changes or deletes records or files.

## Who may call it

- `public`: anyone. Visitors may call it 60 times a minute from one address.
- `signed-in`: a person signed in to the portal, or a program with a token that holds **Call the portal's API endpoints**.
- `token`: only a program with such a token.
- `private`: only the portal's own actions. See [Private endpoints](#private-endpoints).

A call from a page of the portal, as the person signed in, sends the page's CSRF token as the other API calls do.

## Keep answers, and other sites

`cache: { seconds: 60 }` keeps a public GET endpoint's answer for that long, for everyone. It is then always made as a visitor. A change to the portal's files makes it again.

`cors: { origins: ["https://app.example.ro"] }` lets pages of those sites call the endpoint from the browser; a public endpoint may name `"*"`.

## Private endpoints

A private endpoint does work the portal's forms, flows, jobs and other endpoints share, and no one outside calls it:

```yaml
path: /requests/save
method: POST
access: private
parameters:
  status: { type: text, required: true }
actions:
  - { type: createRecord, model: requests, values: { status: params.status }, into: made }
  - { type: respond, status: 201, body: '{"id": vars.made.id}' }
```

Asked for from outside, it answers as an endpoint that is not there. It takes no `cors`, `cache` or `redirects`.

An action list calls it, or any other endpoint of the portal, with `callEndpoint`:

```yaml
- type: callEndpoint
  endpoint: save
  params: { status: '"new"' }
  okStatus: [409]
  into: saved
```

- **What it is given:** `params` gives the endpoint's parameters, each of its type; the portal checks them when the files are published.
- **What comes back:** `vars.saved` holds `status` and `body`, and `location` for a redirect. An answer outside 200–299 and `okStatus` fails the action; its answer is still kept for `onError`.
- **As whom:** the endpoint runs as the person the calling list runs as, or as a visitor, on the same site. An endpoint for people signed in needs a person; one for programs with a token is never called this way.
- **Where:** a form, flow, job or endpoint that may change records calls endpoints. A GET endpoint, or one anyone may call, does not.
- **Limits:** a run calls at most 5 endpoints. Endpoints call one another at most three deep, and ten times in all, within the caller's time.

Each call is in the endpoint's calls, naming what called it.

## Its calls

**Endpoints** in the console lists every endpoint with who may call it, and the last calls: how each ended, its answer's status and how long it took. **Log** shows a call's log. Only its errors are kept, unless the endpoint has `debug: true`; what it answered is never kept.

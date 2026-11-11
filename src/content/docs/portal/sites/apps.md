---
title: Apps on a page
description: Name an app in the site's files, place its widgets on pages, set their preferences, and build an app the portal can show.
---

An app is a program deployed on its own, next to the portal. It tells the portal what it offers in a **manifest**: a small JSON file at an address of its own. You name the app in the site's files and place its **widgets** on pages. An administrator then [approves](/portal/console/apps/) it before it shows.

## Name an app

Each app has a file in `apps/`, named after its id:

```yaml
# apps/hello.yaml
id: hello
name: Hello
manifest: { url: http://hello.apps.svc:8090/portal-app.json }
```

The address is `http:` or `https:`, without a user name or password. Whoever may change the site's files decides which addresses the portal reads, inside your network too.

Each sync reads every app's manifest and checks it. If an app cannot be reached, or its manifest is wrong, the sync is refused and the pages stay as they were. When an app publishes a new manifest, the next sync brings it in, even with no change to the files.

## Place a widget

A placement names the app and the widget, and can set the widget's preferences:

```yaml
regions:
  main:
    - id: welcome
      app: hello
      widget: greeting
      preferences: { greeting: Bun venit }
    - { id: clock, app: hello, widget: clock }
```

- `widget` can be left out when the app has only one.
- `preferences` are checked against what the widget accepts. A value that does not fit makes the sync refused, with the file and the field.
- A placement's `id` is unique on its page, in lower-case letters, digits and hyphens. It appears in the page's address when someone changes the widget.

[Who sees a page](/portal/sites/permissions/) also applies to placements.

Text a page holds itself needs no app: it is an [HTML block](/portal/sites/layouts/#an-html-block).

## Preferences

What a widget shows is set by its preferences, in this order, field by field:

1. the default from the app's manifest;
2. the value in the site's files;
3. the value an editor saved with **Preferences** on the page, as long as it still fits. A field the editor leaves empty goes back to the site's value.

Preferences in a widget that runs in the browser reach the visitor's browser. Never put a secret in a preference.

## Build an app

This section is what the portal asks of an app. To start from a working one, with a library that does the checks below, see [Build an app](/portal/sites/build-an-app/).

The app serves its manifest as JSON:

```json
{
  "id": "hello",
  "name": "Hello",
  "version": "1.0.0",
  "permissions": ["person"],
  "widgets": {
    "greeting": {
      "title": { "ro": "Salut", "en": "Greeting" },
      "render": { "fragment": { "url": "/fragment", "timeoutMs": 2000 } },
      "modes": ["view", "help"],
      "windowStates": ["normal", "maximized", "minimized"],
      "preferences": {
        "type": "object",
        "properties": {
          "greeting": { "type": "string", "title": "Greeting", "default": "Hello", "maxLength": 40 }
        },
        "required": ["greeting"]
      }
    },
    "clock": {
      "title": "Clock",
      "render": {
        "component": { "module": "https://cdn.example.ro/clock.js", "tag": "hello-clock" }
      }
    }
  }
}
```

- `id` is the app's id, as in `apps/<id>.yaml`.
- `version` changes with each release. A version that asks to know more waits for a new approval.
- `permissions` is what the app needs to know about the person: `person` (id and name), `person.email`, `person.fields` (profile fields), `person.roles` (portal roles, such as administrator). The last three need `person` too. Ask only for what the app uses.
- Addresses in the manifest can be relative to the manifest's own address.
- The manifest is at most 256 KB, and is served directly, without a redirect.
- A new manifest can stop the syncs of the sites that use the app. A second widget makes placements without `widget` wrong. A new required preference without a default makes placements that do not set it wrong. The sync is refused until the site's files say which widget, or give the value; the pages stay as they were.

### Two kinds of widget

A **fragment** is HTML the app's server makes. For each placement, the portal sends a `POST` with JSON to the widget's `url` and puts the answer in the page.

- The `url` is on the same origin as the manifest, since the portal's server calls it, often from inside the same network.
- The app answers within `timeoutMs`: from 100 to 10000 ms, 3000 if left out. A widget that answers late, or with an error, shows **This section is not available right now.**, and the rest of the page still shows.
- The answer is HTML, at most 1 MB. Scripts in it do not run: the portal's pages allow scripts only from the portal itself and from approved apps' modules.

The body tells the app:

| Field | What it is |
|---|---|
| `tenant`, `site`, `locale` | where the page is and its language |
| `page.path` | the page's path |
| `placement` | `id`, `widget`, `preferences`, `mode`, `windowState` |
| `person` | only what the app's approval allows, and only when someone is signed in |
| `portal` | `issuer` and `jwks`: a hint for a developer setting the app up, never what the app checks against |

With it comes an `Authorization: Bearer` token, signed by the portal (ES256). The app trusts the body only after checking the token against two values set in its own configuration: the tenant's **issuer** and **keys** address, shown on the console's [Apps](/portal/console/apps/#for-the-apps-developers) page. Never take them from the body: anyone who can reach the app could send a body naming their own keys. The portal's keys serve all its tenants, so the issuer is what tells one tenant's request from another's.

- `iss` is the tenant's issuer, `typ` is `portal-request+jwt` and `aud` is `app:<id>`. It is valid for 60 seconds.
- `placement`, `widget`, `mode`, `windowState`, `site` and `page` repeat the body's.
- `bsha` is the SHA-256 of the exact body bytes, base64url. Compare it with the body you received.

`portalVerifier` in the [developer kit](/portal/sites/build-an-app/#check-what-the-portal-sends) checks all of this.
- `sub` is the person's id, when the person is sent.

A **component** is a [web component](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) the visitor's browser runs.

- `module` is an absolute `https:` address (`http:` only for `localhost`). The page loads it once as a JavaScript module.
- `tag` is the custom element's name, with a hyphen.
- The page renders `<tag data-portal-placement="…">` with a `<script type="application/json" data-portal-props>` inside it. The props are `placement`, `widget`, `preferences`, `mode`, `windowState`, `locale` and, when allowed, `person`.

### Preferences a widget accepts

`preferences` describes them, in a small part of JSON Schema:

- `type: object` with up to 30 `properties`, each a `string`, `number`, `integer` or `boolean`;
- each with a `title` (text, or `{ ro, en }`), and optionally a `description` and a `default`;
- `enum` for a choice of strings (1 to 50), `maxLength` for text (1 to 2000, 500 if left out), `minimum` and `maximum` for numbers;
- `required`, the properties that must have a value.

Nesting, lists, `pattern` and `format` are not accepted.

### Modes and window states

A widget can be shown in **modes**:

- `view`: the widget itself, for everyone.
- `edit`: for people who may edit the page. If the widget lists `edit` in `modes`, the app is asked for its own form. Otherwise, the portal shows a form made from the widget's preferences.
- `help`: for people who may edit the page, if the widget lists `help`.

And in **window states**, for anyone who sees it: `normal`, `maximized` (it fills the page) or `minimized` (its title only). A widget allows all three unless it lists fewer in `windowStates`; `modes` is `view` alone unless it lists more. Anyone who maximized or minimized a widget can restore it.

The mode and window state are in the page's address, per placement: `?p_welcome_mode=help` or `?p_clock_state=maximized`. The app receives them in `placement.mode` and `placement.windowState`.

## Events

An app can send events and take them. An administrator joins an event to an app that takes it on the console's [Events](/portal/console/events/) page, and the portal checks the two fit.

### Declare them

The manifest's `events` lists what the app **emits** and what it **receives**, each with the fields it carries:

```json
"events": {
  "emits": {
    "deal.won": {
      "title": { "ro": "Contract câștigat", "en": "Deal won" },
      "schema": { "type": "object", "properties": { "id": { "type": "string" } }, "required": ["id"] }
    }
  },
  "receives": {
    "welcome": {
      "schema": { "type": "object", "properties": { "id": { "type": "string" } }, "required": ["id"] },
      "webhook": { "url": "/events/welcome" }
    },
    "zone.set": {
      "schema": { "type": "object", "properties": { "zone": { "type": "string" } } },
      "browser": true
    }
  }
}
```

- A name is lower-case words joined by dots or hyphens, such as `deal.won`; an app declares at most 50 each way.
- `schema` takes the same fields as a widget's preferences, without `default`; `title` is optional. An event is at most 32 KB.
- An emitted event with `browser: true` is sent by the app's components on the page; without it, by its server.
- A receiver takes events at its `webhook`, on the manifest's own origin, in its components on the page with `browser: true`, or both.

A receiver **fits** an event when every event of that kind gives it what it needs:

- every field the receiver requires, the event requires;
- a field both have is of the same type; a whole number fits a number;
- if the receiver has a list of values (`enum`), the event has one too, with no other values;
- the receiver's `maxLength`, `minimum` and `maximum` are no stricter than the event's.

A receiver also has to be able to get the event: an event the app's server sends reaches a receiver's `webhook`, and one its components send reaches receivers with `browser: true`. The console offers only receivers that fit and can get the event.

A receiver gets only the fields it declares.

The portal's own events are `portal/user.created`, `portal/user.updated`, `portal/user.erased`, `portal/user.signed_in`, `portal/config.activated`, `portal/app.approved` and `portal/app.revoked`, and what happens in [Keel](/portal/sites/keel/#when-something-happens-in-keel): `portal/keel.case.opened`, `portal/keel.case.stage_entered`, `portal/keel.case.closed`, `portal/keel.case.reopened`, `portal/keel.process.started`, `portal/keel.process.ended` and `portal/keel.process.cancelled`. The first four carry `{ id }` and are about that person; an app approved to know who the person is is told so with them. The app id `portal` cannot be used.

### Send an event from the app's server

The app's server sends events with a token from an OAuth client of a [service account](/portal/console/service-accounts/). The client needs the **Publish events** scope, and the app ticked under **Publish events as**. A server sends only events declared without `browser: true`, and no client may send the portal's own events.

```http
POST /_portal/api/events
Authorization: Bearer <token>
Content-Type: application/json

{ "app": "crm", "event": "deal.won", "payload": { "id": "D-17" } }
```

When the event is about a person, name them in the `X-Portal-Acting-Person` header, by id or email; the client then also needs **Act for a person**. When that person is erased, the events about them are erased too.

The portal answers `202` once the event is kept. It then sends it to every app wired to it and every webhook that takes it, trying again for a day when a receiver fails.

### Take events at a webhook

The portal sends `POST` to the receiver's `webhook` with JSON:

| Field | What it is |
| --- | --- |
| `id` | the delivery's id; the same on each try, so a repeat can be dropped |
| `eventId` | the event's id, as the portal answered whoever sent it; the same for every receiver |
| `type` | the event, such as `portal/user.created` |
| `receiver`, `tenant`, `occurredAt` | which receiver, which tenant, and when it happened |
| `payload` | the fields the receiver declares |
| `person` | only as far as the app's approval allows, and only for an event about a person |

With it comes an `Authorization: Bearer` token, typed `portal-event+jwt`. Check it as you check a fragment's token: against the tenant's issuer and keys from the app's own configuration, with `aud` `app:<id>`, and `bsha` the SHA-256 of the exact body.

Answer with a `2xx` within the timeout (`timeoutMs`, 3000 if left out). Anything else is tried again after 1 minute, 5 minutes, 30 minutes, 2, 6, 12 and 24 hours; a `410` stops it at once. Events can arrive more than once and in any order. If the receiver's manifest changes before an event is sent, the event is sent only if the receiver still takes it.

### Events between components

On a page where a wire joins two components (both declarations `browser: true`), a component sends an event with:

```js
this.dispatchEvent(new CustomEvent("portal:emit", {
  bubbles: true,
  composed: true,
  detail: { event: "zone.changed", payload: { zone: "Europe/London" } },
}));
```

The portal checks the payload and sends `portal:event` to each placement of the wired app on the page, with `detail: { type, receiver, source, payload }`. The sender does not get its own event. Events in the browser carry no person and never reach a server; any script on the page could send one, so treat them as input, not as proof.

### Webhooks for any service

Services that are not apps take events at a [webhook](/portal/console/events/#webhooks) an administrator adds. Each request carries `webhook-id`, `webhook-timestamp` and `webhook-signature`, as [Standard Webhooks](https://www.standardwebhooks.com/) says: the signature is `v1,` and the base64 HMAC-SHA256 of `<webhook-id>.<webhook-timestamp>.<body>`, keyed with the base64-decoded part of the secret after `whsec_`. Standard Webhooks libraries check it for you.

## Hooks

An app can run small checks and changes on the portal's own server, in a sandbox, at **hook points**:

| Hook point | Runs when |
| --- | --- |
| `user.validate` | someone creates or changes a person on the console or through the API, to refuse the change |
| `user.transform` | the same, to change the person before they are saved |
| `preferences.validate` | an editor saves the preferences of one of the app's widgets |

```json
"hooks": {
  "user.validate": { "module": "/hooks/names.wasm", "export": "validate" }
}
```

- `module` is a WebAssembly module on the manifest's own origin; `export` is the function to call.
- `timeoutMs` is how long the hook may take, 10 to 1000 ms, 100 if left out.
- `onError` is what happens when the hook fails: `refuse` (the default) refuses the change, `allow` lets it through.
- A hook about people needs the `person` permission. It sees a person's email only with `person.email`, and their fields only with `person.fields`.

Hooks run only for apps an administrator [approved](/portal/console/apps/), and an approval includes the hook points. The approval trusts the app's address for the code it serves there, which may change with each sync. Disabling a person, or people added by a provisioning system, a directory or a sign-in provider, runs no hooks.

### What a hook gets and answers

Each call gets JSON and answers JSON:

- **Validate hooks** get `{ tenant, operation, user }` (or, for preferences, `{ tenant, site, page, placement, widget, preferences }`) and answer `{ "problems": [{ "field": "name", "message": "A name cannot hold <." }] }`, or `{}` when all is well. The portal shows each message on the field it names: `name`, `email`, one of the portal's own fields by its key, or a preference's key; anything else above the form.
- **Transform hooks** get the same and answer `{ "user": { "name": "…", "fields": { … } } }`. They may change the name, and the fields only with `person.fields`; a field set to `null` is removed. The email and roles never change.

Transforms run first, one app after another; then every validate runs on the result. A request spends at most two seconds on hooks. A hook that fails three times in a row is left alone for a minute, then tried again.

### Build a hook

Any language that compiles to WebAssembly works, such as Rust, AssemblyScript, Zig or C. The module:

- is on the manifest's own origin;
- imports its memory from the portal as `env.memory`, with a maximum of at most 256 pages (16 MiB), and imports nothing else; each call's memory starts at the size the module declares, so declare what its data and stack need;
- has no memory or start function of its own, and at most one small table;
- exports `alloc(len) → ptr`, which the portal calls to get room for the input;
- exports each hook function as `(ptr, len) → i64`: the portal writes the input's JSON at `ptr` and the function answers where its own JSON output is, as `ptr << 32 | len`. The output is at most 64 KB.

Each call runs in a fresh instance with fresh memory, in a separate process the portal stops when the time is up. The portal reads the module when the site's files are synced and keeps it, so a new version of the module takes effect with the next sync.

Usual build settings: in Rust or C, link with the memory imported and capped at 16 MiB (`--import-memory`, `--max-memory=16777216`) and a small stack; in AssemblyScript, `--importMemory --maximumMemory 256 --runtime stub --use abort=`, so it imports nothing but the memory.

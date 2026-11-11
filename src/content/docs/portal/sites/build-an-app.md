---
title: Build an app
description: Start an app from a working one, check what the portal sends it, send events, and type its code against its manifest.
---

An app for the portal is a program of your own that serves a manifest, widgets and, if it needs them, events and hooks. [Apps on a page](/portal/sites/apps/) describes what the portal asks of an app. This page shows how to build one with the portal's developer kit: a starting app and a library, `@invergent/portal-app-sdk`, that does the checks for you.

## Start from a working app

```sh
npm create portal-app my-app -- --name "My app"
cd my-app
bun install
bun test
```

The folder must be new or empty. The app's id is the folder's name, unless `--id` says otherwise: lower-case letters, digits and hyphens, starting with a letter.

The new app has:

- `portal-app.json`, its manifest: a **Greeting** widget its server renders, a **Counter** widget that runs in the browser, a `user.validate` hook, an event it sends and two it takes;
- `server.ts`, which serves the manifest, the greeting, the counter's script and the hook, and takes the `welcome` event;
- `src/widget.ts`, the counter, a web component;
- `hooks/validate.wat`, the hook's source, and `hooks/validate.wasm`, built from it (`bun run build:hook`);
- `src/portal-types.ts`, the types of the manifest's preferences and events;
- `portal-config/apps/<id>.yaml`, the file that names the app in the site's files;
- its own tests.

To see it on a portal:

1. Start it with the tenant's **Issuer** and **Keys** from the console's [Apps](/portal/console/apps/#for-the-apps-developers) page. Its README says how.
2. Copy `portal-config/apps/<id>.yaml` into the site's files, under `apps/`, with the address where the app serves its manifest. Place its widgets on a page.
3. Sync, then [approve](/portal/console/apps/) the app on the console.

On your own machine, [Develop locally](/portal/sites/develop-locally/) does steps 2 and 3's sync for you, again on every change.

## Check what the portal sends

Every request the portal sends an app carries a token. Check it before you trust the body:

```ts
import { PortalRequestError, portalVerifier } from "@invergent/portal-app-sdk/server";

const portal = portalVerifier({
  app: "my-app",
  issuer: "urn:surogate-portal:tenant:…", // from the console's Apps page
  jwksUrl: "https://portal.example.ro/_portal/.well-known/jwks.json",
});

// A widget the app's server renders
const { claims, json } = await portal.verify(request, { kind: "fragment" });

// An event to one of the app's receivers
const event = await portal.verify(request, { kind: "event", receiver: "welcome" });
```

- `verify` takes the request as it came in, or its headers and its exact body. It checks the portal's signature, the token's type, the tenant, the app, its lifetime, and that the token signs this very body. For an event it also checks the receiver and the delivery's id.
- It answers the token's `claims` and the body as `json`. Otherwise it throws `PortalRequestError`, whose `reason` says what did not match; answer `401`.
- The issuer and the keys' address come from the app's own configuration, never from the request. For an app used by several tenants, give `issuer` a list, or a function that decides.
- Make one verifier and keep it: it keeps the portal's keys for a few minutes, and fetches them again when the portal starts using a new one.
- An event can arrive more than once. `claims.delivery` is the same on each try: drop a delivery you already handled.

The library runs on Bun, Node 20 and later, Deno and edge workers.

### Webhooks for any service

A service that takes events at a [webhook](/portal/console/events/#webhooks) checks them with the webhook's secret:

```ts
import { verifyWebhook } from "@invergent/portal-app-sdk/server";

const { id, json } = await verifyWebhook({ secret, headers: request.headers, body: await request.text() });
```

It refuses a body that is not the one signed, and a delivery more than five minutes from now.

## Send events from the app's server

```ts
import { PortalClient, PublishError } from "@invergent/portal-app-sdk/server";

const portal = new PortalClient({
  portalUrl: "https://portal.example.ro",
  clientId,
  clientSecret,
  scope: "events act-as",
});

await portal.publishEvent({
  app: "my-app",
  event: "deal.won",
  payload: { id: "D-17" },
  actingPerson: "ana@example.ro",
});
```

- The client is one of a [service account](/portal/console/service-accounts/)'s, with **Publish events**, and the app ticked under **Publish events as**. `actingPerson` needs **Act for a person**.
- `portalUrl` is an address of the tenant the events are for.
- The client keeps its token and asks for a new one before it expires.
- When the portal refuses, `publishEvent` throws `PublishError`, with the portal's `code`: for example `event_not_declared` for an event the manifest does not declare, or declares as sent in the browser.

## Write a web component

```ts
import { type PortalEvent, PortalElement } from "@invergent/portal-app-sdk/browser";
import type { Preferences } from "./portal-types.ts";

class Counter extends PortalElement<Preferences["counter"]> {
  render() {
    const step = this.props?.preferences.step ?? 1;
    // … draw the widget, then, when something happens:
    this.emit("counted", { count: step });
  }

  onPortalEvent(event: PortalEvent) {
    if (event.receiver === "reset") {
      // … check event.payload before using it
    }
  }
}

customElements.define("my-app-counter", Counter);
```

- `this.props` holds what the portal rendered into the widget: its placement, preferences, mode, window state, language and, when the app may see them, the person.
- `this.emit` sends one of the app's browser events. It goes only where an administrator [wired](/portal/console/events/) it; with no wire on the page, it goes nowhere.
- `onPortalEvent` receives the events wired to the widget. Any script on the page could send one: check what it says before acting on it.
- `propsOf`, `emit` and `onEvent` do the same for any element, without the base class.

Style the widget with the colours and fonts the page sets from the site's design, such as `var(--foreground)`, `var(--primary)` and `var(--font-body)`, so it looks like whichever site it is placed on. See [Give a site its look](/portal/sites/design/#for-apps).

## Form fields and options

An app can add to the portal's forms: a field type it draws itself, such as a signature pad, and option lists for a form's selects, read from its backend. Declare them in the manifest:

```json
"forms": {
  "fields": {
    "signature": {
      "title": { "ro": "Semnătură", "en": "Signature" },
      "module": "/forms/signature.js",
      "tag": "crm-signature",
      "value": { "type": "string", "maxLength": 20000 }
    }
  },
  "options": {
    "counties": { "title": "Counties", "url": "/options/counties", "timeoutMs": 3000 }
  }
}
```

**A field** is a web component on the app's own origin. The form draws its tag, and sets its `value` property to what was entered so far. When the person changes it, the element dispatches a `change` event with `detail: { value }`. The value is a text (`maxLength`, 10,000 unless said), a number (`minimum`, `maximum`) or `true`/`false`, as `value` declares. The portal refuses anything else when the form is sent.

**Options** are asked of the app's server by the portal, never by the browser. The portal POSTs `{ tenant, site, locale, form, field, person? }`, signed as a `portal-options+jwt` token. Check it with `verify(request, { kind: "options" })`; the claims name the site, the form and the field, and `sub` the person when the app may see them. Answer with `{ "options": [{ "label": "Iași", "value": "is" }] }`: 1 to 500 options, each label and value 1 to 200 characters, no value twice. The portal keeps the answer a minute for the same person and field. A choice is checked against the list the portal fetched when the form is sent.

While the app is not approved, forms that use its fields or options are not offered. Forms place them in their file; see [Forms](/portal/sites/forms/#fields-from-apps).

## Actions

An app can give the portal's action lists actions its server runs, such as sending an SMS. Declare each with what it takes and what it answers:

```json
"actions": {
  "send": {
    "title": { "ro": "Trimite SMS", "en": "Send an SMS" },
    "inputs": {
      "type": "object",
      "properties": { "to": { "type": "string", "maxLength": 20 }, "text": { "type": "string" } },
      "required": ["to", "text"]
    },
    "outputs": { "type": "object", "properties": { "id": { "type": "string" } } },
    "url": "/actions/send",
    "timeoutMs": 5000,
    "connector": "gateway"
  }
}
```

The portal POSTs `{ call, tenant, site, locale, action, inputs, person?, credentials? }` to the action's URL, signed as a `portal-action+jwt` token. Check it with `verify(request, { kind: "action", action: "send" })`: it refuses a token for another action, and the same call a second time. Answer `{ "outputs": { "id": "m-1" } }`, as the outputs say, within the timeout (at most 10 seconds) and 256 KB. Inputs and outputs are flat: texts, numbers and yes or no, no lists. `person` is there when the app may see the person, without their portal fields.

A site's lists call it with `appAction`; see [Actions](/portal/sites/actions/#app-actions).

## Connector types

An action that needs an account at another service, such as an SMS gateway's key, names a connector type of the app:

```json
"connectors": {
  "gateway": { "title": "SMS gateway", "fields": ["apiKey", "sender"] }
}
```

An administrator makes a connector of that type and sets its fields in the console. Each call of an action that names the type gets them as `credentials`. They are sent only to your app, over https unless your app runs on the same machine, and only while the connector still names your app and type at the same address.

## Start jobs

The events your server publishes (those without `browser: true`) can start a site's [jobs](/portal/sites/jobs/#when-an-app-sends-an-event). Publish as in [Send events from the app's server](#send-events-from-the-apps-server); each event starts each job that waits for it once.

## Types from the manifest

`src/portal-types.ts` gives each widget's preferences, each event's payload and the person their own type, so the editor and the compiler hold the code to the manifest. A field that is required, or has a default, is always there.

After a change to the manifest and a sync, write the types again from what the portal took:

```sh
portal apps types my-app --out src/portal-types.ts
```

It needs a token that may read the tenant.

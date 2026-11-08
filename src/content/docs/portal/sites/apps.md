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

## Preferences

What a widget shows is set by its preferences, in this order, field by field:

1. the default from the app's manifest;
2. the value in the site's files;
3. the value an editor saved with **Preferences** on the page, as long as it still fits. A field the editor leaves empty goes back to the site's value.

Preferences in a widget that runs in the browser reach the visitor's browser. Never put a secret in a preference.

## Build an app

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

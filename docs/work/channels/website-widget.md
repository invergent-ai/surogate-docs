---
title: Website widget
sidebar_position: 4
---

# Website widget

The Website widget embeds the agent as a chat bubble on your own domain — marketing site, SaaS app, customer portal.

## What you need

Nothing external. The platform issues a **publishable key** when you enable the channel.

## Configuration

Open the agent → **Configure** in the left nav → the **Channels** tab → toggle **Website** ON. The form expands:

| Field | What it does |
|---|---|
| **Publishable Key** | Auto-generated. Masked by default — click **SHOW** to reveal, **COPY** to clipboard. The COPY button is **disabled until you save** — the key isn't deployed yet. **ROTATE** to invalidate the current key and generate a new one. |
| **Allowed Origins** | Exact-match URLs where the widget will be embedded. Format: `scheme://host[:port]`. Add `https://www.acme.com` and `https://acme.com` if you serve both. No wildcards. |
| **Session Message Cap** | Max messages per visitor session. `0` = no cap. Useful for cost control on a public-facing widget. |
| **Embed code** | Click to reveal the JavaScript snippet. |

Click **SAVE CHANNELS**.

## The embed code

You paste a script tag into your site's HTML, typically before `</body>`:

```html
<script src="https://widget.surogate.ai/v1/widget.js"
        data-agent-slug="acme-support-bot"
        data-publishable-key="pk_live_..."
        defer></script>
```

Drop into any page on an allowed origin. A chat bubble appears in the bottom-right corner. Click → chat opens.

## Anonymous vs identified visitors

By default visitors are anonymous — each browser session has a UUID stored in localStorage. Subsequent visits resume the same Surogate session.

To link a logged-in user from your site to a Surogate user:

```js
window.Surogate.identify({
  email: "user@example.com",
  external_id: "your-internal-user-id",
});
```

Now the same person using your widget and using your Slack bot for the same agent shares one set of sessions.

## When the widget says "origin not allowed"

Check the browser console — the widget logs the rejected origin. The most common cause: your Allowed Origins list doesn't include the exact URL the page is served from. Add it → SAVE → reload the page.

No wildcards: `https://*.acme.com` doesn't work. You need each subdomain individually.

## When the COPY button is greyed out

You haven't saved the channel config yet. Click **SAVE CHANNELS** first. The key isn't deployed (and the platform won't accept widget connections with it) until then.

## Rotating the key

If your key leaks (it ended up in a public GitHub repo, etc.):

1. Agent → Configure → Channels → Website → **ROTATE**.
2. Confirm. The old key is invalidated immediately.
3. Update your site with the new key.

## What's next

If you need end-user accounts, see [Users](./users.md).

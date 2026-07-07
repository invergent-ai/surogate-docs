---
title: Website widget
sidebar_position: 4
---

# Website widget

The Website widget embeds the agent as a chat bubble on your own domain — marketing site, SaaS app, customer portal.

## What you need

Nothing external. The platform issues a **publishable key** (prefixed `surg_wk_…`) when you enable the channel.

## Configuration

Open the agent → **Configure** in the left nav → the **Channels** tab → find the **Website** card → **Connect**. The connect screen asks for your **Allowed origins**, then you click **Enable widget**.

| Field | What it does |
|---|---|
| **Allowed origins** | Exact-match URLs where the widget will be embedded. Format: `scheme://host[:port]`. Add `https://www.acme.com` and `https://acme.com` if you serve both. Bare domains get `https://` added automatically. No wildcards. |

Once enabled, the **Manage** screen shows:

- **Embed code** — the script snippet, with a **Copy** button.
- **Allowed origins** — the same editor; add/remove auto-saves.
- **Messages per chat** — max messages per visitor chat. `0` = no limit. Useful for cost control on a public-facing widget.
- **Advanced → Publishable key** — the generated key (shown read-only).
- **Turn off** — stops the bubble appearing on your site; your key and settings stay in place.

Changes on the Manage screen save automatically — there is no separate save button.

## The embed code

Copy the snippet from the Manage screen and paste it before `</body>` on your site. It looks like this:

```html
<script src="https://cdn.jsdelivr.net/npm/@invergent/website-widget@2/dist/surogates-widget.global.js"></script>
<script>
  SurogatesWidget.mount({
    apiUrl: "https://acme-support-bot.cloud.surogate.ai",
    publishableKey: "surg_wk_...",
  });
</script>
```

`apiUrl` is the agent's endpoint and `publishableKey` is the key from the Advanced section. Drop the snippet into any page on an allowed origin. A chat bubble appears in the bottom-right corner. Click → chat opens.

If you don't manage the site yourself, send the snippet to whoever does.

## Visitors are anonymous

Each browser session gets a UUID stored in localStorage, so subsequent visits from the same browser resume the same Surogate session. The widget doesn't require your visitors to have Surogate accounts.

## When the widget says "origin not allowed"

The page's exact URL isn't in your **Allowed origins** list. Add it on the Manage screen (it auto-saves) and reload the page.

No wildcards: `https://*.acme.com` doesn't work. You need each subdomain individually.

## Charging for a public agent

The widget is the buyer-facing surface for a public agent, so it's where monetization takes effect: if the embedded agent is monetized, visitors hit a paywall (subscriptions and/or token packs) before they can chat. See [Monetize your agents](../monetize.md) to set that up.

## What's next

If you need end-user accounts, see [Users](./users.md).

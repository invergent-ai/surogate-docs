---
title: Payments with Stripe
description: Take payments and subscriptions through Stripe Checkout, call Stripe's API from forms and jobs, and run jobs when Stripe says a payment succeeded.
---

The portal's **Payments** extension takes payments through [Stripe](https://stripe.com): a form opens a Stripe Checkout page where the person pays or subscribes, a job or a signed-in person's form calls Stripe's API for customers, subscriptions and refunds, and a job runs when Stripe says something happened, such as a payment that succeeded. As with every extension, it is open to every tenant of the portal.

## Connect your Stripe account

On **Connectors**, make a connector of the kind **A Stripe account**. Set its credential: Stripe's secret key, from Stripe's Dashboard under **Developers → API keys**. Prefer a restricted key (`rk_…`) that may do only what your steps do. **Test** reads the account's balance; nothing is changed.

To run jobs on Stripe's events, tick **It hears Stripe's events**. The connector's page then shows the address Stripe sends its events to. In Stripe's Dashboard, under **Developers → Webhooks**, add an endpoint with that address. Choose **snapshot** events, of the API version **2024-06-20**, and the event types your jobs use. Then set the endpoint's signing secret (`whsec_…`) as the connector's credential, with the secret key. A connector holds one signing secret: events of your own account and of connected accounts need two endpoints, and two connectors. Events of test mode never run a live key's jobs, nor live events a test key's.

## Open a Checkout

In an action list, **Open a Stripe Checkout** makes a Stripe Checkout page and keeps its address; a **Go to a page** step then sends them there. For a form, add `https://checkout.stripe.com` under **Other sites it may send people to**.

- **Pay once, or subscribe.**
- **Items:** a list, each a Stripe price (`{price: "price_…", quantity: 1}`) or a price written here (`{name, amount, currency, quantity}`, with `interval` — day, week, month or year — for a subscription). The amount is a whole number in the currency's smallest unit: 1999 for 19.99 lei. A payment has up to 100 items, a subscription up to 20.
- **Address after paying** and **Address when the person gives up**: https addresses on one of the portal's own sites. Stripe puts the Checkout's id where the address says `{CHECKOUT_SESSION_ID}`.
- **Stripe customer** (`cus_…`) or **The person's email**, not both; and **Metadata**, up to 50 names, which go with the payment or subscription too.
- **Connected account** (`acct_…`): for Stripe Connect, the account the Checkout is made on.

A Checkout is opened once for a run, even when the run is tried again. **Once for** makes it once for a value of yours, such as an order's number, whichever run asks. Visitors open at most 600 Checkouts an hour on a portal; a refused attempt is not counted.

## Call Stripe

**Call Stripe** calls Stripe's API: GET, POST or DELETE, a path under `/v1/` such as `/v1/customers` or `/v1/refunds`, and parameters as a map, and keeps Stripe's answer. It is made only by someone signed in or a job: never from a public form, nor from a person seen as someone else. A POST is made once for a run, as a Checkout is.

When Stripe refuses a call, the step fails with Stripe's own words. The connector's key never appears in them.

## When Stripe sends an event

A job can start for each event of the types it names, such as `checkout.session.completed` or `invoice.paid`, or `*` for all, that a connector hearing Stripe's events receives. In the job editor, **It runs** is **When Stripe sends an event**. The run reads the event's `trigger.type` and its object, `trigger.object`; an object over 64 KB gives only its id and kind, so read it again with **Call Stripe**.

- Each event runs the job once, even when Stripe sends it again. Events can arrive in any order: read the current state from Stripe when it matters.
- An event is checked by Stripe's signature, within 5 minutes. A payment by a slower method completes later: listen to `checkout.session.async_payment_succeeded` too.
- When the job already has 100 events waiting, Stripe is asked to send it again later, so none is lost.
- An event caused by the job's own call to Stripe runs the job one step deeper; past three, it stops.

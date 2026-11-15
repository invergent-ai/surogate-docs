---
title: Payments with Stripe
description: The stripe connector, the stripeCheckout and stripeCall actions, and the stripe job trigger, as the site's configuration writes them.
---

What these do, and their limits, are on [Payments with Stripe](/portal/sites/payments/).

## A Stripe connector

In `connectors/pay.yaml`:

```yaml
name: { ro: Plăți, en: Payments }
kind: stripe
webhooks: true
```

- `webhooks`: true when the connector hears Stripe's events at `/_portal/hooks/stripe/<connector>`. Its credentials are then `secretKey` and `webhookSecret`; otherwise `secretKey` only. Credentials are set in the console.

## Open a Checkout

```yaml
- type: stripeCheckout
  connector: pay
  mode: payment
  items: '[{"name": "Taxă de autorizare", "amount": 15000, "currency": "ron", "quantity": 1}]'
  successUrl: '"https://primaria.ro/plata/gata?id={CHECKOUT_SESSION_ID}"'
  cancelUrl: '"https://primaria.ro/plata"'
  email: form.email
  metadata:
    cerere: submission.id
  into: checkout
- type: redirect
  to: vars.checkout.url
```

- `mode`: `payment` or `subscription`. `items`, `successUrl`, `cancelUrl`: expressions. Optional: `customer` or `email`, `metadata`, `account`, `once`.
- `into` keeps `{id, url}`.

## Call Stripe

```yaml
- type: stripeCall
  connector: pay
  method: POST
  path: '"/v1/refunds"'
  params: '{"payment_intent": trigger.object.payment_intent}'
  into: refund
```

- `method`: GET, POST or DELETE. `path`: under `/v1/`. `params`: a map, sent in Stripe's form (nested names in brackets). Optional: `account`, `once`, `into`.

## A job on Stripe's events

```yaml
trigger:
  stripe:
    connector: pay
    on: [checkout.session.completed, checkout.session.async_payment_succeeded]
site: main
runAs: user:registratura@primaria.ro
actions:
  - type: updateRecord
    model: requests
    id: trigger.object.metadata.cerere
    values:
      paid: "true"
```

- `on`: 1 to 50 event types, or `*`. The run reads `trigger.id`, `trigger.type`, `trigger.created`, `trigger.livemode`, `trigger.account` and `trigger.object`.

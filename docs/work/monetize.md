---
title: Monetize your agents
sidebar_position: 90
---

# Monetize your agents

Charge end users for the right to chat with one of your public agents. You decide the price; the payment goes straight into your Stripe account; Surogate keeps a small platform fee.

## What it is

Three roles:

| Role | What they do |
|---|---|
| **You** (the builder) | Created an agent and want to charge for it. |
| **Your buyer** | Pays you to use the agent. Doesn't need a Surogate account. |
| **Surogate** | Hosts the agent, brokers the payment via Stripe, and enforces the token budget on every message. |

Four things you'll work with:

| Term | Meaning |
|---|---|
| **Monetization mode** | How your agent charges: free, subscription, token packs, or both. |
| **Offer** | A specific plan or pack you sell (e.g. *$10/month for 1M tokens*). |
| **Entitlement** | What a specific buyer has bought from you — their subscription status and remaining token balance. |
| **Token balance** | The pool of tokens a buyer can spend on messages with your agent. |

## Who can use it

**Pro plan or higher.** The feature isn't available on Free or Standard. If you're on a lower plan, the Monetize tab shows an upgrade prompt instead of the editor.

| Plan | Agent commerce |
|---|---|
| Free | — |
| Standard | — |
| Pro | ✅ |
| Max | ✅ |
| Enterprise | ✅ |

Upgrade under [Settings → Billing](./settings/billing.md).

## Set up your agent

You'll need a project on the **Pro plan or higher** with **BYO Firebase Auth** configured (see [Self-registration](./channels/self-registration.md)). The platform operator must have completed the platform-side Stripe Connect setup; if Stripe Connect isn't enabled platform-wide, the Monetize tab returns *"Stripe Connect is not configured."*

### Step 1 — Connect your Stripe account

Open the agent's **Configure** page and click the **$ Monetize** tab. You'll see a **STRIPE CONNECT** block with `Status: not_connected`. Click **CONNECT STRIPE** and follow Stripe's onboarding:

- Verify your identity (passport / driving licence depending on country).
- Link a bank account (Stripe uses Plaid-style instant verification where available).
- Answer a short questionnaire about your business.

Stripe redirects you back to Surogate when you're done. The status flips from `not_connected` to **Active** once Stripe has cleared you for charges, and the **OPEN DASHBOARD** button (next to CONNECT STRIPE) becomes active. If anything is still pending you'll see exactly which step to finish.

A few things worth knowing:

- **One Stripe account per project**, not per agent. If you monetize more than one agent in the same project they all share the same Stripe account and the same payout schedule.
- Your buyers' payments land in **your** Stripe balance, not Surogate's. Stripe pays you out on your normal schedule (daily by default).
- The buyer's card statement shows **your** business name — you're the merchant of record on each charge.

### Step 2 — Set up buyer sign-in

Your buyers need a way to sign in before they can pay. Surogate uses **Firebase Authentication** for this — the same setup you use to let end users [self-register](./channels/self-registration.md).

Under **Settings → ⚙ Settings tab → Firebase Auth**, configure your project's Firebase account. Choose which sign-in providers to offer (email/password, Google, GitHub). You can use the same Firebase project for both agent self-registration and commerce.

If you skip this step the buyer paywall shows *"buyer authentication is not configured."*

### Step 3 — Pick a monetization mode

Back on the Monetize tab, the **MODE** radio group has four choices:

| Mode | When to use it |
|---|---|
| **FREE** | No charge. The default. |
| **SUBSCRIPTION** | Buyers must hold an active subscription to send any message. Best for *all you can eat* pricing. |
| **TOKEN PACKS** | Pay as you go. Buyers top up a balance and the agent burns tokens per message. Best for casual users. |
| **BOTH** | Buyers can subscribe *or* buy packs. Subscription tokens get spent first; top-up tokens kick in when those run out. |

You can change the mode at any time. Existing offers and existing buyers carry over — the change only affects the paywall the buyer sees next time they visit. The page shows a *Monetization updated* toast after each change.

### Step 4 — Create offers

Once you've picked a mode (anything other than FREE), the right editors appear under the STRIPE CONNECT block. The fields stay **disabled** until Stripe is connected.

**Subscription plan** — a recurring monthly or yearly charge. Fields:

- **NAME** — defaults to `Monthly access`; shown on the paywall and on the buyer's card statement
- **PRICE (USD)** — defaults to `10`
- **TOKENS INCLUDED** — defaults to `1,000,000`
- **INTERVAL** — combobox, `Monthly` or `Yearly`

Click **ADD PLAN**. Each period the buyer pays, they get a fresh batch of tokens. Unused tokens from the previous period **do not roll over**.

**Token pack** — a one-time purchase. Fields:

- **NAME** — defaults to `Top-up pack`
- **PRICE (USD)** — defaults to `5`
- **TOKENS INCLUDED** — defaults to `500,000`

Click **ADD PACK**. Top-up tokens **never expire** — buyers keep them until they spend them, even if they later cancel a subscription.

A few rules:

- You can create as many offers as you want. Stripe creates a corresponding product and price on your account for each one.
- **Prices are immutable** once created. To change a price, deactivate the old offer and add a new one — Stripe doesn't allow editing prices because existing subscribers would be silently affected.
- **Deactivating** an offer hides it from new buyers but doesn't cancel existing subscriptions. Subscribers keep their current price until they cancel themselves.
- You can sell in any currency Stripe supports; the editor defaults to USD. Buyers can be charged in their local currency automatically (Stripe handles the conversion).

## What your buyers experience

When a buyer visits one of your public agents:

1. **Paywall.** If the agent is monetized they see your offers — plans on the left, token packs on the right (or whichever your mode allows).
2. **Sign in.** They sign in with their Firebase account (Google, email/password, whatever providers you enabled). If they don't have one yet, the same flow lets them register.
3. **Checkout.** They click Subscribe or Buy and land on Stripe Checkout. They pay with card, Apple Pay, Google Pay, SEPA, iDEAL — anything you've enabled. Buyers in non-USD countries see prices auto-converted to their currency.
4. **Use the agent.** Their tokens are deducted as they chat. If they run out, the next message is rejected with a *please top up or subscribe* message.
5. **Manage subscription.** A **Manage subscription** button appears on the paywall once they've bought anything. It takes them into Stripe's hosted Customer Portal, where they can cancel a subscription, update their payment method, and download past invoices.

You don't have to build any of this UI. The paywall component, Stripe Checkout, and the Customer Portal are all provided.

## How tokens are spent

Each buyer has two balances per agent:

- **Subscription balance** — tokens granted by their current subscription period. Resets each period.
- **Top-up balance** — tokens from one-time pack purchases. Never resets; only spent down.

When the buyer sends a message:

1. Surogate estimates how many tokens the request will cost.
2. If their total balance is at least the estimate, the request goes through.
3. Tokens are deducted **subscription balance first, then top-up balance**.

A buyer with both kinds will burn their monthly grant before eating into their pay-as-you-go pool. If they're short on tokens, the message is rejected with a clear error so they know to top up. Their card is never charged for a message — only at Checkout time.

## Subscription lifecycle

| Event | What happens |
|---|---|
| **Renewal succeeds** | Buyer's subscription balance resets to the offer's token amount for the new period. Top-up balance untouched. |
| **Renewal fails** | Stripe marks the subscription as `past_due` and retries on a schedule (typically up to 3 weeks). The paywall tells the buyer to update their card via the Customer Portal; once Stripe charges successfully, service resumes automatically. |
| **Buyer cancels** | Subscription stays active until the end of the current period. When it ends, their subscription balance drops to zero. Top-up balance is preserved — they can keep using leftover top-up tokens or top up again without re-subscribing. |
| **Buyer disputes a charge** | Stripe handles disputes via Smart Disputes (it auto-submits a counter using the payment metadata so you don't miss the deadline). You can override and submit your own evidence anytime before the deadline. |

## Fees

| Charge | Who pays |
|---|---|
| Surogate platform fee | You. A small percentage of each subscription renewal and each token pack purchase is automatically split off to Surogate. The exact percentage is on your billing page. |
| Stripe processing fees | You. Standard Stripe rates apply — typically 2.9% + $0.30 in the US, with discounts for SEPA / EU recurring. |
| Tax (VAT / GST / sales tax) | Buyers, where applicable. Stripe Tax (free, built in) tells you when you cross a registration threshold in any country. You're responsible for registering and remitting; Stripe gives you the data. |
| Currency conversion | Buyer pays a ~1% fee when Stripe converts to their local currency at checkout. |
| Chargeback fees | You (~$15 per chargeback). Smart Disputes reduces how often you lose them. |
| Buyer support | You. Buyers pay you, so support questions reach you, not Surogate. The Customer Portal handles cancellations / card updates automatically. |

## FAQ

**What if I downgrade off Pro after creating offers?**
Existing offers stay in the database but the Monetize editor locks and the buyer-facing paywall rejects new checkouts with an *upgrade required* message. Existing subscribers keep their subscriptions and can keep using their tokens — downgrading doesn't retroactively break what they paid for. Re-upgrade to unlock everything again.

**Can I use a single Stripe account across multiple Surogate projects?**
No — one connected Stripe account per project. If you want to share payouts across projects you'd need to handle that on the Stripe side (e.g. consolidate to a single business bank account).

**Can a buyer try the agent before paying?**
Not through the paywall. If you want free trials, the right pattern is a separate *free demo* agent in the same project set to mode = free, then a paid agent that's monetized.

**Can I let some buyers use the agent for free?**
Not directly — there's no per-buyer override. Workaround: give them their own access via your own custom flow that bypasses the paywall, or set up a free demo agent.

**What if my buyer asks for a refund?**
You handle refunds directly via your Stripe dashboard. Stripe refunds the buyer; the corresponding token grant on Surogate isn't automatically clawed back, so it's your call whether to disable that buyer's access. For chargebacks (where the buyer goes to their bank instead of you), Smart Disputes counter-submits automatically.

**How fast do I get paid?**
Stripe's default is daily payouts with a 2-day rolling reserve in most countries. You can change the schedule in your Stripe dashboard.

**Can I sell in currencies other than USD?**
Yes — Stripe supports 135+ currencies. The editor defaults to USD; you can set prices in another currency by adjusting the offer. Stripe also auto-converts to the buyer's local currency at checkout regardless of which currency the price is set in (the buyer pays in their currency, you settle in yours).

**Where do I see how much I've earned?**
In your Stripe dashboard (Express dashboard if that's the account type you onboarded with). It shows every charge, every payout, every dispute, and every refund. Surogate doesn't aggregate this — your Stripe account is the source of truth for your earnings.

## Platform setup (one-time, by the Surogate operator)

This section is for the operator running the Surogate platform — it covers turning the agent-commerce feature on for the entire platform so individual builders can use it. **Skip if you're a builder configuring your own agent** — the platform operator has already done this.

The setup happens in two places: the Stripe Dashboard (one-time Stripe Connect config) and the Surogate server config (one secret to add). About 20 minutes end-to-end.

### A. Enable Stripe Connect

1. **Stripe Dashboard → Connect → Get started.**
2. **Business model:** pick **Platform** (the left option — *Merchants will collect payments directly*). The Marketplace option does **not** match the architecture and will not work.
3. **Account type:** pick **Express**. Gives builders a slim Stripe-hosted dashboard scoped to their own funds; you keep platform-level Dashboard access.
4. **Platform public details:** fill in your platform's name, logo, and support URL. Builders see these during Express onboarding and on emails Stripe sends about their payouts.

### B. Configure onboarding options

**Settings → Connect → Onboarding options:**

| Tab | Setting | Value |
|---|---|---|
| **Countries** | Tick every country you want to onboard builders in. | Be generous — adding later forces re-verification of existing builders. |
| **Capabilities** | Payments + Transfers | **Both required.** Direct charges fail without either. |
| **OAuth** | OAuth toggle, redirect URIs | **Skip both.** OAuth is the legacy *connect existing Stripe account* flow; we use Account Links instead. The *you must define a redirect URI* warning is misleading and safe to ignore. |
| **Tax** | Show tax during signup | **ON** (default). Free Stripe Tax for Connect — monitors each builder's tax registration thresholds. Zero conversion impact per Stripe data. |
| **Regional → Singapore** | Connected-account declaration | *"None of my platform's connected accounts are used to facilitate financial services, rewards-based crowdfunding or receive donations."* |
| **Regional → Japan** | Installment Sales Act question | **No** unless Surogate has actually lost a Japanese consumer-protection lawsuit. |
| **Climate programs** | Optional Stripe Climate contribution | Off by default; flip on later if you want. |
| **Public details** | Collect public details | **ON** with all four fields (statement descriptor, support email, support phone, support address). Buyer receipts/invoices show the builder's contact info, not Surogate's. |

### C. Configure Connect-wide settings

**Settings → Connect:**

| Section | Setting | Value |
|---|---|---|
| **Connect → Settings → Branding** | Logo + brand colour | Shown on every Express onboarding screen and Customer Portal. |
| **Connect → Settings → Branding → Statement descriptor** | Platform-side descriptor | `SUROGATE` (≤22 chars). Appears on the platform half of split charges. |
| **Connect → Payment methods** | Allow connected accounts to customize their own | **ON**. Set defaults to Card + Apple/Google Pay + SEPA + iDEAL + Bancontact. Builders override per-account. |
| **Connect → Adaptive Pricing** | Enable for connected accounts | **ON**. Auto-converts prices to the buyer's local currency at checkout — ~30% conversion lift on non-domestic buyers. Allow builders to toggle. |
| **Connect → Disputes** | Smart Disputes auto-respond | **ON**. Free safety net — Stripe auto-submits a counter at the deadline. ~25% win-rate improvement vs no response. Allow builders to toggle. |
| **Connect → Payouts → External accounts** | Require at least one bank account | **Yes**. Forces builders to supply a payout destination during onboarding. |
| **Connect → Payouts → External accounts** | How to collect bank details | **Financial Connections + Allow saved bank accounts**. Instant Plaid-style verification; cuts payout failures ~15×. |
| **Connect → Payouts → External accounts** | Allow debit cards | **No**. Bank-only is the legitimate-merchant default. |
| **Connect → Payouts → Statement descriptor** | What builders see on their bank statement | `SUROGATE PAYOUT` or similar. |

### D. Configure the Customer Portal defaults

**Connect → Settings → Customer portal defaults.** This is the Portal config every new Express account inherits — your buyers' *Manage subscription* button drops them into this Portal scoped to the builder's connected account.

| Feature | Enable? |
|---|---|
| Update payment methods | ✓ |
| Update billing address | ✓ |
| View invoices | ✓ |
| Cancel subscriptions | ✓ |
| Switch plans | Optional |
| Pause subscriptions | ✗ |

Builders can override these per-account from their Express dashboard.

### E. Add the connected-account webhook endpoint

**Stripe Dashboard → Developers → Webhooks → + Add endpoint.**

- **Endpoint URL:** `https://<your-host>/api/commerce/stripe/connect/webhook`
- **Listen to:** **Connected accounts** (this is what separates this endpoint from the platform-billing one)
- **Events to subscribe to:**
  - `account.updated`
  - `checkout.session.completed`
  - `customer.subscription.created`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`
  - `invoice.paid`
  - `invoice.payment_failed`

Stripe shows the webhook signing secret (`whsec_…`) after you create the endpoint. You'll need it for the next step.

### F. Add the secrets to your Surogate config

Add to `~/.surogate/config.yaml` (or wherever your `ServerConfig` lives):

```yaml
# The same Stripe secret key the platform billing already uses.
stripe_secret_key: sk_live_xxx

# The signing secret from the webhook you just created in step E.
stripe_connect_webhook_secret: whsec_xxx

# Optional — platform fee percentages, defaults are 10.0 each.
stripe_connect_subscription_fee_percent: 10.0
stripe_connect_token_pack_fee_percent: 10.0
```

Restart the server. The boot log line `Stripe Connect agent commerce enabled` confirms it's wired correctly. If you instead see `Stripe Connect agent commerce disabled — stripe_secret_key or stripe_connect_webhook_secret is unset`, double-check both values are present and non-empty.

### Smoke test

Once enabled, the fastest end-to-end test:

1. As an admin, bump a test project to **Pro** plan via `/api/billing/projects/{id}/plan`.
2. Open the project's agent → **Monetize** tab → click **Connect Stripe** and complete Express onboarding with Stripe's test-mode dummy data (SSN `000-00-0000`, routing `110000000`, account `000123456789`).
3. Set the agent's mode to **Both** and create one subscription offer ($10/mo, 1M tokens) and one token pack ($5, 500k tokens).
4. As a buyer, sign in via Firebase and complete a subscription checkout with test card `4242 4242 4242 4242`.
5. Verify the buyer can chat with the agent and that tokens decrement on each message.
6. Click **Manage subscription** → land in the connected account's Customer Portal → cancel → confirm subscription status goes to `canceled` and top-up balance is preserved.

If all six steps work, the platform is set up correctly.

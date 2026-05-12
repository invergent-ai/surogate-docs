---
title: Sales lead qualifier
sidebar_position: 3
slug: /use-cases/sales-lead-qualifier
---

# Sales lead qualifier

Inbound contact-form submissions land in a queue, and the agent triages them: enriches the company, scores against your ICP, drops the qualified ones into your CRM with a suggested rep, kicks the rest into a nurture sequence.

The Surogate Ops welcome page literally suggests this case in the *Describe what you need* placeholder. It's the obvious build.

## What you need

- **A model.** General-purpose. Reasoning matters more than knowledge here.
- **Two or three skills:**
  - *lookup_company* — enrich from your data provider (Clearbit, Apollo, ZoomInfo).
  - *create_opportunity* — write into Salesforce or HubSpot.
  - *route_to_rep* — pick a sales rep based on territory or vertical. Or fold this into *create_opportunity*.
- **An ICP definition.** A short knowledge base with one document: who counts as a qualified lead for your team. Industry filters, employee count range, revenue thresholds, deal-breakers.

## Set it up

1. **Build the ICP knowledge base.** A single doc is enough — the agent reads it on every call to ground its score.
2. **Write the skills.** Build → Skills & Tools → **New Skill** for each. Use the templates library for Salesforce / HubSpot starter skeletons.
3. **Deploy the agent.** Name it something visible to your sales ops team — they'll be the ones tweaking it.
4. **Attach.** Open Settings, multi-select your skills and the ICP KB, redeploy.
5. **Wire the form.** Your contact form POSTs to a webhook; the webhook calls the agent through Surogate's API; the agent does its work; the response confirms what happened.

## Try it

Submit a test lead — one that's clearly in-ICP and one that's clearly not. Open each resulting session: the in-ICP one should show *lookup_company* → *create_opportunity*. The out-of-ICP one should skip the opportunity and write a note instead.

## Iterate

Sales-ops reviews the agent's calls in Sessions. They'll flag two kinds of mistake:

- **False positives.** The agent qualified a lead that wasn't a fit. Add the disqualifying criterion to the ICP doc.
- **False negatives.** A real lead got bounced. Same fix.

After a few weeks, you'll have a labeled dataset of correct vs incorrect calls. That dataset is exactly what you'd use to fine-tune a smaller, faster expert that runs much cheaper at the volumes lead-qualification needs.

## Where to go next

- **[Skills & Tools](../features/skills.md)** — Salesforce / HubSpot starter templates.
- **[Sessions](../features/sessions.md)** — to review qualified vs not.
- **[Training your own expert](./training-your-own-expert.md)** — when volume justifies a custom model.

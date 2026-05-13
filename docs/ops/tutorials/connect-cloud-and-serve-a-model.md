---
title: Connect a cloud and serve a model
sidebar_position: 2
slug: /tutorials/connect-cloud-and-serve-a-model
description: From zero compute to a serving model in under an hour — credentials, offers, deploy, verify, agent wiring.
---

# Connect a cloud and serve a model

This tutorial takes you from a Surogate Ops account with no compute connected to a model serving on your own cloud in roughly forty-five minutes. The bulk of the time is the first deploy waiting for the serving container to come up; once that's warm, every subsequent model takes seconds.

It's the second tutorial because it's the moment where Surogate Ops graduates from a chat-with-a-hosted-model surface into the platform the rest of this manual assumes. From here you own the inference, the bill, and the ceiling — your only limit is how much GPU you can pay for.

## What you'll have at the end

- A connected cloud backend with live GPU offers.
- A model serving on that backend, reachable from the Playground and from any agent you wire to it.
- An agent rebuilt on top of the new model so end users hit your weights, not someone else's.
- A working mental model of compute policies, quantization, and where cost actually lives.

## Before you start

- A Surogate Ops account.
- Credentials for one of the eight supported cloud backends: AWS, Azure, GCP, RunPod, Modal, Nebius, Oracle Cloud Infrastructure, Vast.ai. RunPod and Vast.ai are the easiest for a first run — just an API key, no IAM ceremony.
- A clear idea of what you want to serve. Suggestions for a first deploy: `Qwen/Qwen3-8B-Instruct` for a strong general-purpose chat model on a single A100, or `meta-llama/Llama-3.1-8B-Instruct` if you have a Hugging Face token. Either runs comfortably in `bf16` on one 80GB GPU.
- A budget cap in your head — say, fifty dollars for the tutorial. Surogate's Compute Policies can enforce this for you later; for now, just keep an eye on the dashboard.

## Step 1 — Connect the backend

Studio → **Compute → Cloud**. You see a grid of eight provider tiles plus a **Connect Cloud** button. Click the tile for your chosen provider.

Each provider has its own credential form. The fields you'll be asked for, by provider:

| Provider | Fields |
|---|---|
| **RunPod** | API Key |
| **Vast.ai** | API Key |
| **AWS** | Access Key ID, Secret Access Key |
| **Azure** | Tenant ID, Subscription ID, Client ID, Client Secret |
| **GCP** | Project ID, Service Account Key (JSON, paste or browse) |
| **Modal** | Token ID, Token Secret, Environment |
| **Nebius** | Service Account ID, Public Key ID, Private key (.pem upload) |
| **OCI** | User OCID, Tenancy OCID, Fingerprint, Home Region, Private Key (.pem upload) |

Each form has a deep-link to the provider's own console for finding the values — *Open AWS Console*, *Open GCP Console*, and so on. Use it. Don't copy credentials from a stale wiki.

If this is RunPod or Vast.ai you're done in fifteen seconds. If this is AWS, allocate ten minutes: you'll need an IAM user with at least `AmazonEC2FullAccess` and `IAMReadOnly`, plus an access key for that user.

Submit the form. The tile flips to **Connected**.

## Step 2 — Verify the backend has offers

A connected backend with no GPU offers is useless. Click into the backend's detail page; you should see an **Offers** panel listing every GPU type your account is eligible for, with current price per hour.

If the offers list is empty, three things to check:

1. **Quota.** Your AWS / GCP / Azure account may have no GPU quota at all in the regions Surogate queries. Open the provider console, request quota for the GPU you care about (A100 80GB and H100 80GB are the most useful), wait for approval, retry.
2. **Region.** Some providers default-restrict queries to specific regions. Open the backend's settings and broaden the region set.
3. **IAM scope.** AWS in particular needs read access to instance-type metadata. Without it the offers query silently returns empty. Tighten or loosen the IAM policy as needed.

For RunPod and Vast.ai you should see offers immediately — those providers don't gatekeep on quota the way the hyperscalers do.

## Step 3 — Pick a model

Studio → **Build → Models → Deploy Model**. The dialog opens to a source picker with four cards:

- **Local Hub** — pull weights from a Hub repo you (or your team) already have.
- **🤗 Hugging Face** — paste an HF model id.
- **OpenRouter** — proxy through OpenRouter's catalog.
- **URL** — any OpenAI-compatible endpoint.

For this tutorial, pick **Hugging Face** and paste `Qwen/Qwen3-8B-Instruct`. (If you've already pulled a model into your Hub, **Local Hub** is the natural choice; the rest of the steps are the same.)

The next screen adapts to the source. For a served Hugging Face model you'll see:

- **Backend** — the cloud you connected in step 1.
- **GPU offer** — drawn from the offers list. For an 8B model, an A100 40GB is plenty; an A100 80GB is cheaper-per-token because of better batching headroom.
- **Replicas** — start with 1 for the tutorial. Production usually wants 2+ for redundancy.
- **Quantization** — `bf16` is the safe default. `fp8` doubles throughput on hardware that supports it but takes a small quality hit. `qlora` is for when you're cost-bound and willing to sacrifice some quality.
- **HF Token** (optional) — only required if the repo is gated. Set the token under Settings → Integrations first if you'll be pulling multiple gated repos.

Submit. The model lands at the top of the Models list with status **Deploying**.

## Step 4 — Watch the first deploy

This is the slowest step on purpose. The first time Surogate pulls a model on your backend, several things happen:

1. The scheduler provisions the GPU instance (a few minutes on a hyperscaler; under a minute on RunPod).
2. The serving container builds and pulls cached layers (about a minute).
3. The model weights download from the source (a few minutes for an 8B; closer to fifteen for a 70B).
4. The container starts serving and reports healthy.

Total: anywhere from five to twenty minutes the first time. The serving image and the weights cache; the next deploy of the same model on the same backend lands in seconds.

While it deploys, open **Compute → Workload Queue** and filter to `serving`. Your deploy is the row with status **Provisioning** then **Running**. The detail panel shows logs streaming live; if anything goes wrong, the failure message is there before the status flips to **Error**.

When the Models list status flips to **Serving**, the model is reachable. Don't move on until it does.

## Step 5 — Sanity-check in the Playground

Operate → **Playground**. Pick your new model from the dropdown.

The Playground is deliberately stripped down — no skills, no knowledge base, no agent system prompt. Just you and the bare model behind Surogate's proxy. Type a question, set the sampling parameters (the defaults are fine), hit send. The response streams back.

Three things worth checking before trusting the deploy:

1. **The model responds at all.** No 504, no 502, no silence.
2. **Token count looks right.** The sidebar shows input and output tokens. If it's stuck at zero, the model isn't running; check the Workload Queue.
3. **Speed feels right.** First-token latency under a second; tokens-per-second visible to the eye. Slower than that usually means the GPU is undersized for the model — pick a bigger offer and redeploy.

If you want a quick head-to-head, open two Playground tabs against two different models and ask the same question in both. It's the cheapest comparison Surogate gives you.

## Step 6 — Wire the model into an agent

A model alone isn't a product. Time to attach it.

Studio → **Build → Agents → Deploy Agent**. Four fields:

- **Display Name** — *Internal Q&A on Self-hosted Qwen* or similar.
- **Slug** — permanent, URL-safe identifier.
- **Description** — one sentence about what the agent does.
- **Model** — pick the model you just deployed.

Submit. The agent's first deploy reuses your already-warm serving container, so it lands in single-digit seconds.

If you already have an agent (say, from [Tutorial: Build a support bot](./build-a-support-bot.md)), the workflow is almost identical: open the agent's **Settings** tab, change the **Model** dropdown to your new self-hosted one, redeploy. End users get the same chat surface; under the hood they're now hitting your weights.

## Step 7 — Note where the cost actually lives

Two cost lines matter:

- **The model's serving container.** Reserved for the life of the deploy — running idle still costs money. Stop the model from the Models list when you're done; restart it later if you need it again.
- **Per-call inference.** Once the container is up, each call uses GPU time. The dashboard's **Serving Models** panel shows a coarse cost graph; for per-second detail use the cloud backend's own billing.

A few practical pointers from teams running this in production:

- **Don't deploy a 70B model for an MVP.** An 8B fine-tuned model serves orders of magnitude cheaper and is often better at your specific job.
- **Pick `bf16` until you have a reason not to.** The other quantizations save money but the regression risk is real until you've measured it.
- **Set a Compute Policy.** Settings → [Compute Policies](../features/compute.mdx). A policy capping monthly spend per backend is the safety net that stops a stuck workload from running up four figures of overnight bill.

## Step 8 — Clean up if this was just an experiment

If you don't plan to keep the model around, three actions:

1. **Stop the model.** Build → Models → row menu → **Stop**. The serving container releases. The Hub repo stays; you can redeploy in seconds later.
2. **Cancel any orphan workloads.** Compute → Workload Queue → filter `serving` → cancel anything still listed.
3. **Optionally disconnect the backend.** Compute → Cloud → tile menu → **Disconnect**. The credentials are removed from Surogate; the cloud account isn't touched on the provider side.

If you're keeping the model, none of this is necessary — just remember the container is billing while it's up.

## When this isn't worth doing

Self-hosting is only the right answer when the economics flip. Until then, proxying a hosted model is cheaper, faster to ship, and easier to operate. Two situations where you should keep proxying:

- **Pre-MVP.** You don't know yet whether the agent's job is genuinely needed. Pay-per-token on a proxied model is a lower fixed cost than serving anything.
- **Bursty traffic.** A serving container costs the same when it's idle. If your traffic is ten requests a day in spikes, proxying wins every time.

The two situations where self-hosting starts to pay:

- **Steady traffic of more than a few requests per minute.** Container utilization rises; per-call cost drops below the proxied alternative.
- **You've trained a custom model.** Then you can't proxy it — you have to serve it. Which is what the next tutorial sets you up for.

## What you've learned

- How to connect any of the eight supported cloud backends, and what each one's credential form looks like.
- How to verify a backend is healthy enough to deploy on.
- How to deploy a model from Hugging Face onto your own compute, with the right GPU and quantization.
- How to sanity-check in the Playground.
- How to wire the model into a new or existing agent.
- Where the cost lives, and how to stop it when you don't need the container.

You now own the inference. The next tutorial closes the loop by training a model on your own data so the inference is doing your specific job, not a generalist one.

## Where to go next

- **[Tutorial: Train and promote an expert](./train-and-promote-an-expert.md)** — fine-tune a model on your captured sessions and serve the result.
- **[Compute](../features/compute.mdx)** — the deep reference for cloud backends, the workload queue, and compute policies.
- **[Models](../features/models.mdx)** — the deep reference for sources, statuses, quantization, and API keys.
- **[Playground](../features/playground.mdx)** — for ad-hoc model testing.

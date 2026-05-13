---
title: Train and promote an expert
sidebar_position: 3
slug: /tutorials/train-and-promote-an-expert
description: The full loop — captured sessions to dataset to SFT run to evaluation to flipped agent. The reason Surogate exists.
---

# Train and promote an expert

This is the tutorial the rest of the manual builds toward. You take an agent that's been running on a frontier model for a few weeks, turn its captured sessions into a training dataset, fine-tune a smaller open-weights model on that dataset, evaluate the result, and flip the agent over so end users hit the cheaper, faster, more on-brand expert.

It's the loop that justifies running Surogate over just calling a hosted API. Done once, it pays for itself in a month or two. Done as a habit — a new expert every quarter as your captured sessions accumulate — it compounds.

The first time through takes roughly three hours of your time and one to three hours of wall clock for the training run itself. Subsequent runs are mostly wall-clock; the operator steps land in twenty minutes.

## What you'll have at the end

- A training dataset built from real sessions your agent served, formatted as supervised fine-tuning examples.
- A trained 8B-class model running on your own compute, fine-tuned on the work your agent actually does.
- Evaluation evidence — at minimum a head-to-head against the old model on a benchmark you care about — that the expert is good enough to ship.
- An agent rebuilt on the expert, serving end users.
- The mental model for how to do this routinely.

## Before you start

- An agent that's been running for at least a couple of weeks. The longer it's been running, the more flagged sessions you have to work with. Three hundred clean sessions is the practical floor; a thousand is comfortable.
- A connected cloud backend with at least one A100 or H100 offer. If you haven't done this yet, run [Tutorial: Connect a cloud and serve a model](./connect-cloud-and-serve-a-model.md) first.
- A budget in your head. An 8B SFT run on one A100 80GB for two hours is roughly twelve dollars on most providers; double that if you want to repeat with different hyperparameters.
- A reasonable base model in mind. `Qwen/Qwen3-8B-Instruct` and `meta-llama/Llama-3.1-8B-Instruct` are both strong starting points; pick the one your team already trusts.

## Step 1 — Triage your sessions

Open **Operate → Sessions** in Studio. Filter the list down to your agent.

You're looking for the sessions worth learning from. Three useful filters:

- **Flagged 👍** — sessions you (or your team) marked as good. These are the gold standard. The model will learn to produce more responses like these.
- **Flagged 👎** — sessions you marked as bad. Don't include these in the training set verbatim — they're the failure cases you're trying to escape — but it's worth reading a sample to understand what the new model needs to do differently.
- **Recency** — the last few weeks is usually a better signal than the first week, which often has setup noise.

If you don't have many flagged sessions, do a quick flagging pass right now. Open twenty random sessions, flag each one 👍 or 👎 based on whether the last response was the kind of response you want shipping. Twenty manually-rated sessions, plus a quality filter on the rest of the corpus, is a workable starting set.

Make a note of:

- **The agent slug** — you'll need it in the next step.
- **The date range** — typically *last 30 days* or *last 90 days*.
- **The flag policy** — most teams pick *flagged 👍 only* for the first expert run. Subsequent runs can broaden as you build confidence.

## Step 2 — Build a dataset from conversations

Studio → **Train → Datasets → New Dataset**. Pick **From Conversations**.

The form is short:

- **Agent** — the agent slug from step 1.
- **Date range** — your chosen window.
- **Quality filter** — *Flagged 👍 only* is the safe default. You can also pick *All non-flagged sessions excluding 👎* for a noisier but larger set.
- **Format** — leave as the default (`prompt + completion`). The dataset will land as kind `sft`.

Submit. Surogate exports the matching sessions, formats them as `(prompt, completion)` pairs, and writes a new dataset to your Hub. A few hundred sessions takes under a minute; a few thousand takes a few minutes.

When the dataset shows up in the Datasets list, click into it to preview. Three things to check:

1. **Row count.** Should be in the low hundreds at minimum, ideally a thousand or more. Less than a hundred is too few — circle back to step 1 and flag more sessions.
2. **Average completion length.** If it's wildly skewed (some completions one word, some thousands of tokens), the model will overfit to the long ones. Most teams trim to a reasonable max length at this stage by editing the dataset's transform config.
3. **A sample of rows.** Click *Preview* and read ten rows. If most of them look like the kind of response you want to ship, the dataset is good. If half of them are noise, your quality filter is too loose — re-create the dataset with a tighter filter.

The dataset lives in your Hub as a Dataset-kind repo. You can share it across teams or push it to another Surogate Ops install. Don't worry about that now; just make a note of the repo path for the next step.

## Step 3 — Schedule the SFT run

Studio → **Train → Training Runs → New Run**. Pick **SFT**.

Top of the form:

- **Name** — *Support Expert v1*, *PR Reviewer v1*, whatever names your team uses. The name is the runId prefix in logs and artifacts; pick something you'll recognise on a metrics dashboard six months later.
- **Short description** — one line; shown in the runs list.
- **Long description** — paragraphs. Write your hypothesis here: *this run should produce a model that handles tier-1 support refunds as well as the frontier model at 1/20th the inference cost*. Your future self will thank you.

Below the descriptions, the per-kind config:

- **Base model** — `Qwen/Qwen3-8B-Instruct` or `meta-llama/Llama-3.1-8B-Instruct`. Larger bases are better, smaller bases serve cheaper; 8B is the practical sweet spot for first runs.
- **Dataset** — the one you just built.
- **Precision** — `bf16` is the safe default. Pick `qlora` if you're optimising for GPU hours; it costs about half but the resulting model converges slightly slower. The Surogate Trainer's [Precision and recipes](/guides/precision-and-recipes) page has the full matrix.
- **Batch size** — leave at the default. The trainer auto-sizes batch to fit the GPU.
- **Learning rate** — leave at the default. Edit only if you have a specific reason.
- **Sequence length** — match the typical session length in your dataset. 2048 is plenty for most support traffic; 4096 if you have long chats.

Then the compute step:

- **Backend** — the cloud you connected.
- **GPU offer** — one A100 80GB or one H100 80GB is the sweet spot for an 8B fine-tune. The dropdown shows current price per hour.
- **Replicas** — 1 for a tutorial. Multi-node distributed training is a topic for a later run.

Submit. The run lands in the Workload Queue under kind `sft` with status **Queued**, then **Provisioning** as the GPU comes up, then **Running** once training starts.

## Step 4 — Watch the metrics

Click into the run's detail. Three tabs:

- **Logs** — the trainer's stdout in real time. Useful for debugging if anything goes sideways; mostly verbose noise on a healthy run.
- **Metrics** — loss curves, learning rate, throughput, gradient norms. This is the tab you'll watch.
- **Artifacts** — initially empty; the run writes intermediate checkpoints here, then a final artifact at the end.

What a healthy SFT run looks like:

- **Loss** — starts somewhere between 1.5 and 3.0 depending on the base, drops smoothly, plateaus near the end. A flat or rising loss is the sign of a bad hyperparameter — usually too-high learning rate.
- **Throughput** — should be steady. Sudden drops are usually data-pipeline stalls (the trainer is faster than the dataset loader). One-shot drops aren't worrying; sustained drops suggest a too-large batch or sequence length.
- **Gradient norm** — should stay in a small range. Spikes above an order of magnitude usually signal NaN risk; if you see them often, lower the learning rate.

For an 8B run on one A100 with a thousand-row dataset, total wall time is typically forty-five minutes to two hours, depending on epoch count and sequence length. You can leave the tab open or come back later; the run will email you when it completes if you've connected an integration.

If the loss diverges, cancel the run, lower the learning rate by 2-4x, and try again. The cost of a re-run at this scale is small compared to the time spent inspecting a busted model.

## Step 5 — Promote the artifact to a Model

When the run completes, the **Artifacts** tab shows a final model repository — a path like `your-team/support-expert-v1@<commit>`. Click **Promote to Model**.

A familiar dialog opens, pre-populated. You're deploying a model from **Local Hub**:

- **Backend** — same one you trained on, or a different one if your serving traffic lives elsewhere.
- **GPU offer** — an 8B model serves comfortably on smaller hardware than it trained on. An L40S or even a T4 (with appropriate quantization) is often enough.
- **Replicas** — 1 to start; scale up when traffic warrants.
- **Quantization** — `bf16` to match training. `fp8` is fine if your hardware supports it.

Submit. The model lands in the Models list as **Deploying**, then **Serving**. First deploy of a freshly-trained model usually takes two to five minutes; subsequent deploys are seconds.

## Step 6 — Evaluate before flipping

This is the step that separates *"the training run worked"* from *"the model is shipping"*.

Studio → **Train → Evaluations → New Evaluation**. Two runs:

1. **Old model on your eval suite.** Set *Target Model* to the model your agent is currently using; pick your team's evaluation suite (or, if you don't have one yet, `MT-Bench` for chat-style work, `HumanEval` for code-style work — see [Evaluations](../features/evaluations.mdx) for the full catalog of built-in benchmarks).
2. **New expert on the same suite.** Same suite, target the new model you just promoted.

When both runs complete, open the new run's detail and switch to the **Comparison** sub-tab. The table shows scores side by side with a signed delta.

Three outcomes:

- **Expert wins decisively.** Move to step 7.
- **Expert ties or wins narrowly.** Re-run both with a different seed to check for noise. If the second pair confirms a win, ship; if it flips, the expert isn't reliably better and you need a richer dataset or different hyperparameters.
- **Expert loses.** Open **Samples** filtered to **losses** and read the failure cases. Most often the dataset was missing a category (the expert never learned that style of question). Augment the dataset and re-train.

For a more rigorous test, run an [Arena](../features/arenas.mdx) instead of a one-shot eval — it's the right tool when one number isn't enough. For a first expert, the eval comparison is usually sufficient evidence.

## Step 7 — Flip the agent over

Open your agent in Studio → **Build → Agents**. Click **Settings**.

In the **Model** dropdown, switch from the old model to the expert. Click **Save**. The agent redeploys; a few seconds later end users are hitting your weights.

The chat surface in **Work** mode is unchanged — same URL, same UI, same sessions. The underlying model is new.

A small thing worth doing right after the flip: ask the agent the same three questions from your [first support-bot tutorial](./build-a-support-bot.md) and check that the answers feel right. It's the cheapest smoke test you'll ever run.

## Step 8 — Watch the first week of production traffic

The expert is shipping. For the first week, two things matter:

- **Refusal rate.** Sometimes an expert over-specialises and starts refusing questions outside the training distribution. Compare the refusal rate in **Sessions** (filter to errors / refused) against the old model's baseline. If it's higher than acceptable, you need a broader dataset next time around.
- **Quality on long-tail questions.** Your training set covered the typical cases. The unusual ones are the failure surface. Spend twenty minutes a day for the first week flagging long-tail sessions; those flags feed the *next* round of training.

If you're happy with the production traffic, you've completed the loop. The next iteration is the same loop with more, better-flagged data.

## Common pitfalls

- **Training on too few examples.** Less than a hundred rows produces a model that's worse than the base. Don't ship that. Either flag more sessions or skip the run.
- **Training on noisy examples.** A few dozen flagged-bad rows mixed into the training set will teach the model to produce flagged-bad responses. Tight quality filter beats large dataset.
- **Skipping the eval step.** A model that looks good in the Playground can still regress on benchmarks. Run the comparison.
- **Flipping the agent without warning the team.** Even a strict improvement changes behaviour. Tell the people using the agent before you flip; they'll catch regressions you don't.
- **Forgetting to stop the old model.** When you flip the agent, the old model's serving container keeps running — and keeps billing — until you stop it. Build → Models → row menu → **Stop**.

## When this isn't worth doing

- **Fewer than a few hundred clean sessions.** Garbage in, garbage out. Run the agent longer, flag more, then come back.
- **The agent's job is genuinely open-ended.** Specialisation helps narrow tasks; it hurts broad ones. If your agent is the team's general-purpose assistant, don't fine-tune it; just call a stronger frontier model.
- **You're not paying for inference yet.** Until cost is real, the loop is overkill. Run on a proxied frontier model until the bill justifies the work.

## What you've learned

The end-to-end loop:

1. **Capture** — flag the sessions worth learning from.
2. **Distill** — turn those sessions into a dataset.
3. **Train** — fine-tune an open-weights model on the dataset.
4. **Evaluate** — confirm the expert is actually better.
5. **Ship** — swap the agent's model over.

You'll run this loop again. Every quarter is a reasonable cadence; some teams run it monthly. Each iteration produces a slightly better, slightly cheaper model than the last, because each iteration trains on slightly higher-quality data than the last.

That compounding is the actual product Surogate is selling. Everything else — the agents, the skills, the knowledge bases — is the surface that makes the loop possible.

## Where to go next

- **[Training Runs](../features/training.mdx)** — the deep reference for SFT and GRPO.
- **[Evaluations](../features/evaluations.mdx)** — the deep reference for benchmarks, suites, and comparison.
- **[Arenas](../features/arenas.mdx)** — when one eval isn't enough verification.
- **[Datasets](../features/datasets.mdx)** — the four sources and the schema rules.
- **[Models](../features/models.mdx)** — to manage the result.

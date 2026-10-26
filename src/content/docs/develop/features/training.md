---
title: Training
sidebar:
  label: Training
---

The Training page launches fine-tuning runs. Four methods can be created and started — **SFT**, **DPO**, **GRPO** and **DISTILL** — and the method picker offers exactly those four. Each is documented in depth below.

> **Studio vs. the engine.** Pretraining (PT) is handled directly by the `surogate` engine CLI (`surogate sft` / `surogate grpo` and friends) and is not exposed in the Studio training pipeline. Full fine-tuning is available for SFT and DISTILL: turn **Enable LoRA** off (see below). DPO and GRPO are LoRA only. `PPO` exists in the API schema but is rejected at run-create time with *"PPO not yet supported"*.

**DPO** and **DISTILL** both ride the SFT path rather than having a pipeline of their own: DPO is an SFT config plus a `loss: {type: dpo}` block over `{prompt, chosen, rejected}` rows, and DISTILL is an SFT config plus a `distillation:` block naming a teacher model. Run-create rejects either one if that block is missing.

## The methods

![The four training methods: supervised fine-tune, preference, reinforcement, and distillation](../../../../assets/screenshots/dev-training-methods.png)

### SFT — Supervised Fine-Tuning

![An SFT run: the experiment it belongs to, the base model, and the dataset](../../../../assets/screenshots/dev-training-sft-source.png)

Standard supervised fine-tuning from labeled trajectories. Most common path.

Configuration:

```
Method: SFT
Base model: qwen2.5-coder-7b (a HF model id, or a Data Hub repo@ref)
Dataset: my-conversations-2026q1 (a local Dataset, or an HF dataset id)
Training parameters (carried in the run's config):
  - Epochs / max steps
  - Learning rate
  - Batch size
  - Precision: BF16 | FP8 | NVFP4
  - Adapter: LoRA (set lora + lora_rank in config) or Full
Compute:
  - Backend: dstack (kubernetes / cloud) or Modal
  - Accelerators: e.g. RTX-PRO-6000:1 on Modal, or GPU:2 on an SSH fleet
  - Spot instances + region (optional)
```

Training runs on Blackwell sm_120 GPUs only: the RTX PRO 6000 and the RTX 50-series (on Modal, only the RTX PRO 6000). See [Supported GPUs](#supported-gpus).

**Full fine-tune is the Enable LoRA toggle turned off.** The new-run form shows it as an **Adapter** switch (**LoRA** by default, or **Full**) for SFT and DISTILL. On the run's **Configuration** tab, turning it off dims the rank, alpha, dropout and target-module controls. DPO has no switch and GRPO's is locked on (both below).

Use when:

- You have a dataset of (input → expected output) pairs
- You want a model that mimics the patterns in your data
- The base model gets the right structure but wrong details

![Hyperparameters, adapter and precision, and the cloud backend the run lands on](../../../../assets/screenshots/dev-training-sft-hyperparams.png)

### DPO — Direct Preference Optimisation

Trains on **preferences** rather than on a single target answer. Each row gives the model a prompt with two completions — one preferred, one not — and the objective pushes probability toward the preferred one relative to a frozen copy of the base model.

DPO rides the SFT path: it is an SFT config plus a `loss` block, dispatched to its own trainer entrypoint (`surogate dpo`).

Configuration:

```
Method: DPO
Base model: ...
Dataset: rows of {prompt, chosen, rejected}
Preference loss (config.loss):
  - type: dpo             (required — run-create rejects a DPO run without it)
  - dpo_beta              How hard to pull away from the reference model (> 0)
  - reference_free        Score without a frozen reference copy
  - target_margin         Required gap between chosen and rejected (needs reference_free)
  - length_norm           Normalise by completion length
  - span_mask             Score only the spans that differ
```

Four constraints are enforced before a run can start, and each mirrors the trainer:

- **LoRA is required.** Each pair is scored against the frozen base, so there has to be a base to freeze. A full fine-tune has no reference to compare against; use SFT for that. The form therefore hides the **Adapter** switch and the **Enable LoRA** toggle for DPO.
- **`per_device_train_batch_size` must be even.** A chosen/rejected pair is two rows, so an odd batch would split a pair across steps.
- **`target_margin` requires `reference_free: true`.** The margin is defined against a reference-free score.
- **Dataset entries are `type: preference`**, or carry no type at all. Any other value parses and then fails inside the container.

Use when:

- You have pairs of better/worse answers rather than single correct ones
- The quality you want is comparative — tone, helpfulness, style
- SFT gets the shape right but you want to push it away from a specific failure mode

### GRPO — Group Relative Policy Optimisation

Reinforcement learning from rewards. Newer, more complex.

Configuration:

```
Method: GRPO
Base model: ...
RL Mode: Environment | RULER
Environment: (Environment mode) — a registered environment with deterministic rewards
RULER judge: (RULER mode) — a dataset of prompts + a system prompt, scored by an LLM judge
GPU blocks: inference_blocks (vLLM) + trainer_blocks (+ judge_blocks for a colocated judge)
Other RL hyperparameters
```

Use when:

- You have a clear reward signal (math correctness, code compiles, ...)
- The desired behaviour can be measured, not just imitated
- You want exploration beyond your training data

**GRPO needs at least two GPUs**, one for the rollout server and one for the
trainer, which is why it is the only method with a GPU block split. On an SSH,
Kubernetes or cloud fleet the fleet size is taken from the block split rather
than fixed when you pick the instance. It cannot run on Modal (see
[Supported GPUs](#supported-gpus)).

GRPO is also LoRA only for now. Its **Enable LoRA** toggle is shown but locked on, and its tooltip says full-parameter RL is not available yet: train an adapter, or full fine-tune with SFT and start the GRPO run from that model.

#### RL Modes

The backend resolves exactly two GRPO reward paths:

- **Environment** — the run points at a registered verifiers environment (`config.environment_id`) that computes deterministic rewards. Example: math problems where correctness is verifiable.
- **RULER** — an LLM judge scores each rollout. The dialog supplies a dataset of prompts plus a system prompt (`config.ruler_task_args`), which the platform wires into a built-in `ruler_task` environment. The judge can be **external** (your own OpenAI-compatible endpoint + API key) or **colocated** (a vLLM judge that runs on the training fleet and consumes its own GPU blocks). Good for subjective rewards (helpfulness, tone).

### DISTILL — Knowledge Distillation

Compresses a large **teacher** model into a smaller **student** by training the student to reproduce the teacher's output distribution, not just the dataset's answers. The teacher's "nearly right" alternatives carry information a hard label throws away.

DISTILL rides the SFT path: it is an SFT config plus a `distillation:` block naming the teacher. Run-create rejects a DISTILL run without one.

#### The capture pass

A distillation run has **two phases**, and the first is usually the longer one:

```
1. Capture   The teacher is loaded and run once over the whole dataset.
             For every token it records its top-K next-token logprobs into a
             .kd sidecar file, stored alongside the tokenised shards.
2. Train     The student trains on those sidecars. The teacher is gone by now;
             it is not held in memory during training.
```

Capture happens **once**, not per epoch, and its cost scales with the teacher's size and the dataset, not with your epoch count. On a reference run a 1.7B teacher over ~295k tokens took about 100 seconds on one L4, against 70 seconds for the training that followed.

Two consequences worth planning around:

- **The teacher must fit on one card.** Capture loads the whole teacher onto a single device and does not shard it, so adding GPUs does not make a larger teacher fit. The run form warns when the teacher looks too large for the selected GPU.
- **Sidecars are large.** Roughly `6 × top_k` bytes per token. At the default `top_k: 64` that is ~384 bytes per token, which is far bigger than the token shards themselves — a 295k-token dataset produces about 113 MB. The storage table on the run form estimates this before you start.

Configuration:

```
Method: DISTILL
Base model: the student — the model you are training
Dataset: any SFT-shaped dataset
Distillation (config.distillation):
  - teacher_model         Required. Must share the student's tokenizer.
  - top_k                 Logprobs stored per token, 1..1024 (default 64)
  - temperature           Softens the teacher's distribution, > 0
  - kd_weight             Weight of the KD (KL) term, >= 0
  - ce_weight             Weight of the plain cross-entropy term.
                          Defaults to 1 - kd_weight.
```

#### The objective, and the two loss curves

A distillation run minimises `ce_weight × loss + kd_weight × kd_loss`, and the run's Overview shows both halves:

- **KD Loss** — how close the student is to the teacher's distribution. This is the half distillation is for.
- **Training Loss (CE)** — plain cross-entropy against the dataset's own answers, exactly as in SFT.

At the default 0.50/0.50 weights cross-entropy is only half the objective, and the **Pure distillation** preset (`ce_weight: 0`) takes it out entirely. So a climbing CE curve on a distillation run is not necessarily a failing one — check KD Loss, which is the half that matters.

Use when:

- You want a small model that behaves like a much larger one
- You have the larger model available and the budget to run it once over your data
- Plain SFT on the same data plateaus below the quality you need

## Supported GPUs

Training runs on **Blackwell sm_120 GPUs** only: the RTX PRO 6000 and the RTX 50-series. Picking anything else is refused when you press Start, before any instance is provisioned, and Studio says so under the compute picker as soon as you select it. Serving and evaluations are not restricted this way.

What that leaves on each compute:

| Compute | Training GPUs |
|---|---|
| **Modal** | Only the RTX PRO 6000. Its other GPUs (B200, H200, H100, A100, L40S, A10, L4, T4) are refused for training. Modal runs the RTX PRO 6000 as a single GPU, so GRPO, which needs two, cannot run there: Start refuses it before anything is provisioned. Run GRPO on an SSH, Kubernetes or cloud fleet. |
| **SSH or Kubernetes fleet** | Whatever Blackwell sm_120 cards its hosts or nodes have. A GPU name Studio does not recognise, such as a generic `GPU:1`, is not checked. |
| **Cloud** (dstack) | Offers on RTX PRO 6000 or RTX 50-series cards. Datacenter Blackwell (B200, B300) is a different architecture and is refused. |

## Training run lifecycle

Creating a run and launching it are **two separate steps**: `POST /api/training-runs` records a queued run (and validates the request), then `POST /api/training-runs/{id}/start` submits it to compute. This lets you create a run, tweak its config, and only then launch.

```
1. Create        Click NEW RUN, fill the form → a queued run is recorded
2. Start         Click START → pre-start validation runs, then GPUs are provisioned
3. Run           Training executes (5min to days depending on dataset + model size)
4. Monitor       Logs, metrics, rollouts, checkpoints via the run detail page
5. Complete      Does not appear on Models by itself: publish it, then add it on Models
6. Optional      Activate as an expert via the expert lifecycle
```

To serve a finished run, see [Local Hub](/develop/features/models/#local-hub).

Two guardrails run at these boundaries:

- **Plan-tier gating (402).** If the project's plan doesn't include training, both create and start return `402` with an "upgrade in Settings → Billing" message.
- **Pre-start validation (422).** START runs the same validator that drives the frontend's Start button; if the config has errors (missing GPU blocks, unset dataset, etc.) it returns `422` and the run stays queued.
- **Dataset check (422).** **Start** checks each local dataset before provisioning or reserving credits. It refuses the run if the dataset is missing, in another project, not **ready** (the message gives its status and says to wait for the build or pick another), has no stored copy (re-create or re-upload it), or lacks a column its declared type needs. The `422` lists each problem as `datasets: ...`. A dataset of auto type with no recognised column only warns. DISTILL also gets a teacher tokenizer check and GRPO an environment check. If a check can't run (for example the Hub is slow), Start proceeds.

### Experiments and the Data Hub

![An experiment groups runs and becomes its own Data Hub repository](../../../../assets/screenshots/dev-training-new-experiment.png)

Every run belongs to an **experiment**, and each experiment maps to a repo in the Data Hub. Individual runs are **branches** in that repo — the platform creates the experiment repo on first use and a per-run branch at create time, then commits the run's artifacts (checkpoints, metrics) to that branch as training progresses.

## Run detail page

The tab set depends on the method.

| Tab | What it shows | Methods |
|---|---|---|
| **Overview** | Status and progress, the loss charts, throughput, and the training log. A DISTILL run also charts KD Loss here | All |
| **Configuration** | Base model, hyperparameters, adapter and precision, compute. The method's own card lives here too: Preference Loss for DPO, Distillation for DISTILL | All |
| **Datasets** | What it trains on | SFT, DPO, DISTILL |
| **Checkpoints** | Saved steps you can resume or merge from | SFT, DPO, DISTILL |
| **Lineage** | Where the weights and the data came from | SFT, DPO, DISTILL |
| **Environment** | The registered environment the run scores against | GRPO, Environment mode |
| **Rollouts** | Periodically sampled rollouts with prompt, completion, reward and advantage — from `GET /api/training-runs/{id}/rollouts` | GRPO |
| **Repository** | Files and commits in the run's Data Hub branch | All |

### Header actions

The buttons at the top of the run detail page depend on the run's status. Viewers without edit access see them disabled.

| Button | Shown when | What it does |
|---|---|---|
| **Start** / **Retry** | Queued (Start), failed or cancelled (Retry) | Launches the run |
| **Stop** | Provisioning or running | Aborts the run |
| **Publish to Hub** | Completed, and the run's artifacts are not yet in the Hub | Commits them to the run's Hub branch |
| **Evaluate** | Completed | Opens the new-evaluation wizard; for a LoRA run, its adapter is already selected |
| **Merge** or **Promote** | Completed (LoRA runs) | Needs the run published first (**Publish to Hub**); without that the dialog does nothing. Writes the merged model to a new Hub repository (you pick repo name and branch). **Merge** when the adapter still needs merging (background job; **Force** skips the 30B-parameter cap); **Promote** when the trainer already merged it (copies weights, no GPU). Disabled while a merge is in flight or done |
| **Clone** | Any status | Asks for a name, then creates a new queued run in the same experiment with the same base model, datasets, configuration and compute. Press **Start** on the copy when ready |
| **Delete** | Any status | Deletes the run after a confirmation |

## Stopping a run

STOP button on the run detail page (`POST /api/training-runs/{id}/stop`). This aborts the upstream dstack or Modal job and marks the run cancelled. Partial training is lost; checkpoints already committed are preserved. A failed or cancelled run can be started again from its detail page — the restart wipes prior metrics/logs/rollouts so the retry's series don't collide with the previous attempt.

## RL Environments

For GRPO Environment mode, you need a registered environment. The Hub has an `Environments` repo type for these.

An environment is a **[verifiers](https://github.com/willccbb/verifiers) package**, not a class implementing a gym-style step loop. It is a Python package whose `__init__.py` exposes a `load_environment(...)` function:

```python
# my_environment/__init__.py
def load_environment(**kwargs):
    ...  # returns a verifiers environment
```

The platform stages that package into the training container before training starts, so a missing or unloadable environment stops the run early rather than part-way through.

There are two ways to get one:

- **Fork a catalogue entry.** The platform ships curated environments: grade-school maths, multiple choice, science questions, and calculator tool use. Adding one copies its implementation into your project as a new Hub repo, with its arguments in an editable `CONFIG` dict beside it. From that point it is an ordinary environment of yours, and you can change it. See [The Environments tab](#the-environments-tab).
- **Bring your own.** Push a verifiers package to an `Environments` repo in the Hub.

### The Environments tab

The Training page has three tabs: **Experiments**, **Runs** and **Environments**. The Environments tab lists your project's environments with a search box. Each row shows the name and module, a domain chip, the version, and a status pill. Click a row to open it. The row's **...** menu has **Rename** and **Delete**.

The tab header has two buttons, **Browse environments** and **+ New environment**. Everything except **Browse environments** is editor-only (including **Add to project**, the row menu, **Validate**, **Publish**, **Save** and **Delete**); viewers see it disabled.

- **Browse environments.** Opens the catalogue, grouped into category cards by domain. Open a card, or search by name or description, then click an entry to preview what the model sees, how it is scored and its configuration. **Add to project** copies it into your project as an editable environment.
- **+ New environment.** **Start from a curated environment** picks a catalogue entry and **Add to project**. **Start from a template** scaffolds source you edit yourself: **Single-turn QA**, **Code + Tests**, **Multi-turn Agent** or **Blank**. Give it a **Module name** (lowercase, fixed after creation), a **Display name**, a **Domain** (Math, Code, Reasoning, Tool use or Custom, only a label for filtering) and a description, then **Save draft**.

Opening an environment shows its repository with an **Info** tab. The header has **Validate**, **Publish**, **Save** (name and description) and **Delete**. Viewers see read-only fields.

### Validation

Validation imports the environment in the trainer image and builds it, so problems show up before a run has provisioned GPUs. It takes a few minutes. It starts by itself when you add a catalogue entry and when you **Publish** a version, and you can start it with **Validate** (it asks first). The result is tied to the commit that was checked. The header shows a chip and the **Info** tab lists the issues, with long tracebacks behind **Show details**.

| Chip | Meaning |
|---|---|
| **Validation queued** / **Validating…** | The check is waiting or running |
| **Validated** | It imported and built |
| **Validation failed** | The environment is broken; the issues say why |
| **Could not be checked** | The check itself didn't run (for example the cluster was unavailable). This says nothing about your environment |
| No chip | It has never been validated. This is true of every environment created before validation existed, and of a fresh template until you validate or publish it |

Only **Validation failed** blocks a GRPO run. Creating a GRPO Environment run against a failed commit is refused (`400` from the API) with an error that names the first problems and points to the environment's page. Changing a run's environment or version is checked the same way, while saving other settings on a run that already points at a failing version still works. The check happens when the run is created or its environment is changed, not again at **Start**, so an environment that fails after that is still startable. Publishing a failed version asks for confirmation, and the dialog warns that it can't be selected for a run.

Constraints:

- An environment may import only what the trainer image already ships. There is no installer for an environment's own dependencies, so a package needing something outside that set will not run.

## REST API

Runs live under `/api/training-runs`; experiments under `/api/experiments`. Create and start are separate calls, and there is no `/cancel` — use `/stop`.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/training-runs` | List runs |
| `GET` | `/api/training-runs/{id}` | Run detail |
| `POST` | `/api/training-runs` | Create (queued) — `402` if the plan lacks training |
| `POST` | `/api/training-runs/{id}/start` | Launch — `422` if the config fails validation |
| `POST` | `/api/training-runs/{id}/stop` | Stop / abort |
| `GET` | `/api/training-runs/{id}/metrics` | Metrics series |
| `GET` | `/api/training-runs/{id}/rollouts` | GRPO rollouts (prompt / completion / reward) |
| `GET` | `/api/experiments` | List experiments |
| `POST` | `/api/experiments` | Create an experiment (provisions its Hub repo) |

## What's next

[Evaluations](/develop/features/evaluations/) for testing what you trained.

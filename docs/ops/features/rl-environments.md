---
title: RL Environments
sidebar_position: 5
slug: /features/rl-environments
description: Define the world an RL training run trains in. Four starter templates, four domains, the verifiers library.
---

# RL Environments

A Surogate **Environment** defines the world an RL training run trains in — the observation space, the action space, and the reward function. Without an environment, a GRPO run has nothing to optimise against; with one, you can train models that reliably pass tests, win games, or hit any other measurable target.

This page is the reference for the Environment surface. The training side is in [Training Runs](./training.mdx); the conceptual loop is in [Architecture](../concepts/architecture.md).

## When you need an Environment

Three concrete shapes:

- **Verifiable code generation.** The reward is "did the produced code pass the tests". The environment is a sandbox that runs the code and reports pass/fail.
- **Math and reasoning with checkable answers.** The reward is "did the produced answer match the expected one". The environment compares with a tolerance.
- **Tool-using agents you want to train end-to-end.** The reward is task-completion across multiple tool calls. The environment exposes the tools and the success predicate.

If your reward is a single judge model rating a single output, you probably don't need an Environment — a `score/N` evaluation in a benchmark works. Environments are for multi-step, programmatically-checkable problems.

## Where Environments live

Environments are **Hub repositories of kind `environment`**. Like models and datasets, they're versioned, sharable, and importable. The training run references the environment by repo path; the dataset that feeds the run inherits the environment's observation / action schema.

In Studio: **Distribute → Data Hub → filter kind = Environment**. New environment: **+ New Repository → kind = Environment**.

## Four starter templates

When you create a new Environment, the wizard offers four templates:

### Single-turn QA

The simplest shape. The agent receives one question; outputs one answer; the environment compares against the expected answer and emits a reward.

Use for: math, factual recall, classification.

The reward function is a Python `verify(prediction, expected) -> reward` you customise. Defaults: exact-match, numeric tolerance, set membership.

### Code + Tests

The agent receives a coding problem; outputs code; the environment runs the code against a hidden test suite in a sandbox and emits pass-rate as reward.

Use for: HumanEval-style training, internal-library refactor training, anything where you have tests.

Backed by the `verifiers` library's sandbox runner. The training run spawns sandbox containers per rollout; reward is `passing_tests / total_tests`.

### Multi-turn Agent

The agent operates over many turns. The environment maintains state, exposes tools, evaluates trajectories against a success predicate.

Use for: ReAct-style agents, multi-step tool use, dialog training.

The reward can be terminal (only at episode end) or per-turn (a small shaping signal at each step). Per-turn shaping makes training faster but introduces reward hacking risk; terminal is safer but harder to learn from.

### Blank

Empty scaffold. You write the observation space, the action space, the step function, the reward, the success predicate. Use when none of the above fits.

## Domains

Each environment carries a **domain** tag. The domain is a hint to humans and to the training UI; it doesn't change the environment's runtime behaviour.

The five domains:

- **Math** — arithmetic, algebra, calculus, contest math.
- **Code** — programming problems with executable tests.
- **Reasoning** — multi-step logical / commonsense / planning tasks.
- **Tool use** — agent operates over a set of tools; reward measures task completion.
- **Custom** — anything else.

Filter the Environment catalog by domain to find existing ones to reuse.

## The `verifiers` library

Surogate Ops uses the open-source `verifiers` library as the runtime substrate for environment evaluation. Concretely:

- Your environment exports a `load_environment()` entry point that returns a `verifiers.Environment` instance.
- The trainer calls `env.reset()` to start an episode, `env.step(action)` to advance, `env.score(trajectory)` to compute the final reward.
- Custom environment authors implement these methods; template-based environments fill them in for you.

The library reference is on the verifiers GitHub repository. The Surogate Trainer's [RL Environments guide](/guides/rl-environments) covers the integration end-to-end.

## Sandbox + pytest reward pattern

The Code + Tests template uses a specific pattern worth knowing:

1. The agent produces code as its action.
2. The environment writes the code into a sandbox container alongside a test file (provided when you author the environment).
3. The container runs `pytest`, capturing the result.
4. The environment parses pytest output into a `passed / total` ratio.
5. The reward is the ratio (optionally scaled, capped, or transformed via a custom function).

The sandbox is short-lived — spawned per rollout, torn down after scoring. Each rollout's container is isolated; one rollout's mistakes can't poison another's.

## ReAct env pattern

The Multi-turn Agent template ships with a ReAct-style scaffold:

- The agent's action is either a tool call (with structured arguments) or a final answer.
- The environment exposes a tool registry; tool calls return results that become the next observation.
- The episode ends when the agent emits a final answer or hits a turn limit.
- The reward function scores the final answer (or, optionally, the trajectory shape — e.g., reward partial credit for using the right tools even if the answer was wrong).

This is the right scaffold for training agents that need to learn when to use which tool.

## Editor

The Environment editor is **LakeFS-backed**: every save creates a versioned commit. The file tree shows the environment's source, the test suite (for Code + Tests), the system prompts, and any auxiliary fixtures.

Two important fields on the environment's settings:

- **Module name** — the Python module path that exports `load_environment`. **Immutable after create.** Pick carefully.
- **Display name** — the human-readable name shown in the Hub and in training-run dropdowns. Editable.

## Bind a dataset

An Environment-kind Hub repo can have one or more **Dataset-kind repos** bound to it. The dataset carries the seed prompts (one row per training example) that the environment will run against; the environment provides the schema the dataset's rows must match.

Binding: in the Datasets page, **New Dataset → Environment → pick the env repo**. The dataset's `kind` is `environment`, and its schema is inherited from the env.

Write-time validation: rows that don't match the env's action / observation schema are rejected at dataset-push time, not at training time.

## Use in a GRPO training run

[Training Runs](./training.mdx) → **New Run → GRPO**:

- **Environment** — pick from your Environment-kind Hub repos.
- **Dataset** — pick from the env-bound datasets.
- **Base model** — the model to fine-tune.
- **GRPO sub-mode** — one of:
  - **Environment** — the environment scores trajectories; the trainer optimises directly against the reward.
  - **Agent** — a separate reward-model agent rates trajectories; useful when the env can't produce a numeric reward directly.
  - **RULER** — a Surogate-specific reward shaping mode designed for sparse-reward environments.

Submit. The run lands as a `grpo` workload in the [Compute Workload Queue](./compute.mdx).

## Sharing an environment

Like every Hub repo, an Environment can be shared across teams. Two patterns:

- **Org-internal sharing.** Add team members or other org users as repo members at editor or viewer. They see the environment in the env picker and can use it in their training runs.
- **Cross-install publishing.** Push the environment's repo to a HuggingFace mirror via the Hub's outbound sync. Other Surogate installs (and any HuggingFace user) can then pull and import it.

For reusable environments — generic math, generic code-test scaffolds — publishing is the right move. For domain-specific environments tightly coupled to your team's data, keep them private.

## When this isn't worth doing

- **The task isn't programmatically verifiable.** If a human can score the output but no code can, an Environment isn't the right shape — use an LLM-judge evaluation instead.
- **One-shot tasks.** Single-turn tasks with checkable answers can train via SFT on a dataset of `(prompt, answer)` pairs and an eval to verify; an Environment is overkill.
- **You don't have a reliable reward.** GRPO on a noisy reward learns the noise. Make the reward function rigorous before you train against it.

## When something fails

- **Environment "load failed" at training time.** The `load_environment` entry point doesn't import. Check the module name field; check the environment's source.
- **Sandbox containers fail to start.** The runtime image the environment pulls isn't available on the chosen backend. The default sandbox image lives at ; mirror it into your registry if needed.
- **Reward is always 0 or always max.** The verify function is broken. Test it locally before pointing a training run at it.
- **GRPO run loss looks fine but the trained model doesn't improve at eval time.** Reward hacking — the model found a way to maximise reward that doesn't match the intended task. Inspect a sample of trajectories; tighten the reward function.

## Where to go next

- **[Training Runs](./training.mdx)** — to launch a GRPO run against an Environment.
- **[Datasets](./datasets.mdx)** — to build the seed dataset bound to an Environment.
- **[Architecture](../concepts/architecture.md)** — the broader training loop.
- **[Surogate Trainer → RL Environments guide](/guides/rl-environments)** — the trainer-side integration in depth.

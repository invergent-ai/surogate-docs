---
title: Training
sidebar_position: 2
---

# Training Runs

The Training page launches fine-tuning runs. Two methods, each with their own configuration.

## Two methods

### SFT — Supervised Fine-Tuning

Standard supervised fine-tuning from labeled trajectories. Most common path.

Configuration:

```
Method: SFT
Base model: qwen2.5-coder-7b (or any HF model)
Dataset: my-conversations-2026q1
Training parameters:
  - Epochs: 3
  - Learning rate: 2e-5
  - Batch size: 8
  - LoRA rank: 16 (if using LoRA)
Adapter: qlora | full | lora
Compute: AWS-A100-x1 | local-A100 | ...
```

Use when:

- You have a dataset of (input → expected output) pairs
- You want a model that mimics the patterns in your data
- The base model gets the right structure but wrong details

### GRPO — Group Relative Policy Optimisation

Reinforcement learning from rewards. Newer, more complex.

Configuration:

```
Method: GRPO
Base model: ...
RL Mode: Environment | Agent | RULER
Environment: (if Environment mode) — a registered environment with deterministic rewards
Reward function: (if Agent mode) — an LLM-judged reward
Rules: (if RULER mode) — runtime rule-based rewards
Other RL hyperparameters
```

Use when:

- You have a clear reward signal (math correctness, code compiles, ...)
- The desired behaviour can be measured, not just imitated
- You want exploration beyond your training data

#### RL Modes

- **Environment** — registered deterministic-reward environments. Example: math problems where correctness is verifiable.
- **Agent** — another LLM judges each rollout. Good for subjective rewards (helpfulness, tone).
- **RULER** — runtime rule-based rewards. Lightweight, deterministic, configurable.

## Training run lifecycle

```
1. Create        Click NEW RUN, fill the form
2. Provision     Platform spins up GPU on selected provider
3. Run           Training executes (5min to days depending on dataset + model size)
4. Monitor       Logs, metrics, checkpoints via the run detail page
5. Complete      Final model lands in Models page as a new entry
6. Optional      Activate as an expert via the expert lifecycle
```

## Run detail page

| Tab | What it shows |
|---|---|
| **OVERVIEW** | Status, dataset, base model, hyperparameters, ETA, current epoch |
| **LOGS** | Real-time training log output |
| **METRICS** | Train loss, eval loss (if eval split), learning rate, throughput |
| **CHECKPOINTS** | Per-epoch model snapshots |
| **OUTPUT** | The final trained model with its endpoint when serving starts |

## Cancelling a run

CANCEL button on the run detail page. Partial training is lost; checkpoints are preserved.

## RL Environments

For GRPO Environment mode, you need a registered environment. The Hub has an `Environments` repo type for these.

An environment is a Python class implementing:

```python
class MyEnvironment:
    def reset(self) -> Observation:
        ...

    def step(self, action) -> tuple[Observation, Reward, Done, Info]:
        ...

    def compute_reward(self, trajectory) -> float:
        ...
```

The platform ships several built-in environments (math, code-execution, multi-step planning). Custom ones live in `tenant-{org_id}/shared/agents/environments/`.

🚧 The RL Environments page in the UI shows an empty "No environments yet" sidebar in current builds; this surface is partially wired.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/training-runs` | List |
| `GET` | `/v1/training-runs/{id}` | Detail |
| `POST` | `/v1/training-runs` | Create |
| `POST` | `/v1/training-runs/{id}/cancel` | Cancel |
| `GET` | `/v1/training-runs/{id}/logs` | Stream logs |

## What's next

[Evaluations](./evaluations.md) for testing what you trained.

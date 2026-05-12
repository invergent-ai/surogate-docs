---
title: Data Hub
sidebar_position: 1
slug: /features/hub
---

# Data Hub

The Hub is Surogate's HuggingFace-compatible registry. Models, datasets, skills, experiments (training runs), and environments all live here as versioned Git-like repositories with branches and tags. The rest of Surogate Ops reads and writes the Hub under the hood — your training run's weights end up here, your datasets push here, your skills publish here.

## When the Hub matters

- You want to share a model, dataset, or skill across teams.
- You want versioned artifacts for reproducibility (which dataset trained which model on which date).
- You want to mirror an external HuggingFace repo into your registry.

## Repository kinds

A Hub repo is one of:

- **Model** — weights and a model card. Training Runs publish here. Models page deploys from here.
- **Dataset** — examples plus a dataset card. Datasets page publishes here. Training Runs read from here.
- **Skill** — a published, importable skill bundle.
- **Experiment** — a training run's full state: weights, config, metrics, lineage.
- **Environment** — RL environment definition; bound to Datasets of kind `environment`.

## Create a repo

Distribute → Data Hub → **+ New Repository**. Fields:

- **Name** — becomes the repo slug.
- **Kind** — Model / Dataset / Skill / Experiment / Environment. Defaults to Model.
- **Description** — short, shown on the repo card.
- **Tags** — space-separated, used by the **Tags** filter on the Hub home.

Submit. The empty repo opens with a file tree.

The dialog has no public-vs-private toggle. Sharing happens by adding members.

## Import an external repo

Distribute → Data Hub → **Import**. Pick **HuggingFace** or **ModelScope**, pick the kind (Model / Dataset / Skill / Experiment / Environment), type the repo id (e.g. `meta-llama/Llama-3.1-8B`), then optionally:

- **Token** — for gated repos.
- **Branch** — defaults to `main`.
- **Sub-path** — restrict the import to a subfolder.

Submit. The repo lands in the Hub with a snapshot of the chosen branch.

## How other parts of Surogate Ops use the Hub

- **Models page** → **Deploy Model** → source **Local Hub** picks a model repo from here.
- **Training Runs** publish their resulting weights as an Experiment-kind repo.
- **Datasets** push to a Dataset-kind repo.
- **Skills** published from the Skill Builder land in a Skill-kind repo.

## Where to go next

- **[Models](./models.md)** — where Hub model repos get served.
- **[Datasets](./datasets.md)** — where Hub dataset repos get imported.
- **[Admin → Integrations](../admin/integrations.md)** — Hub auth.

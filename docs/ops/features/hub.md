---
title: Data Hub
sidebar_position: 13
slug: /features/hub
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Data Hub

## What it does

The **Data Hub** is the project's HuggingFace-compatible registry. It stores Models, Datasets, Skills, Experiments (training runs), and Environments under versioned Git-like repositories with branches and tags. Surogate's other surfaces (Models, Datasets, Training, Skills) read and write the Hub under the hood.

## When to use it

- Sharing a Model / Dataset / Skill across projects or teams.
- Versioning experiment artifacts (weights, configs, metrics) for reproducibility.
- Mirroring an external HuggingFace repo into your project.

## Prerequisites and permissions

- **Read**: any project member.
- **New Repository / Import / Delete**: project `editor` or higher. _TODO(verify._

## Where to find it

- Hub home: `/studio/hub`.
- A single repo: `/studio/hub/<namespace>/<repo>`.
- Hub configuration (auth, endpoint): `/studio/settings/hub` and `/work/settings/hub`.

## Page layout

The Hub home has:

- A **Search repositories…** input.
- Type tabs: `All · Models · Datasets · Skills · Experiments · Environments · Tags`.
- A **Refresh** button (re-fetches state).
- An **Import** button (pull an external repo into your Hub namespace).
- A **+ New Repository** button (create an empty repo).

## Import an existing repo

1. Open **/studio/hub**.
2. Click **Import**. The dialog header reads **Import Repository**.
3. Pick a source provider — two cards: **HuggingFace** and **ModelScope**.
4. Pick the kind — currently `model` selected by default.
5. Type a repo id. The example shown in the picker is `meta-llama/Llama-3.1-8B`.
6. Optional fields:

   | Field | Type | Notes |
   |---|---|---|
   | **Token** | password | Placeholder `hf_…`. Required for gated repos. |
   | **Branch** | text | Defaults to `main`. Toggle the branch-suggestions chip for autocomplete. |
   | **Sub-path** | text | Placeholder `e.g. variant-a/`. Restrict import to a subfolder. |

7. Submit with **Import**. The repo lands at `/studio/hub/<namespace>/<repo>` with a snapshot of the specified branch.

## Create a new repo

1. Click **+ New Repository**. The dialog header reads **New Repository**.
2. Fill the fields, in order:

   | Field | Type | Notes |
   |---|---|---|
   | **Name** | text | Placeholder `my-model`. Becomes the repo slug under `/studio/hub/<namespace>/<name>`. |
   | **Kind** | combobox / select | Five options: `Model`, `Dataset`, `Skill`, `Experiment`, `Environment`. Defaults to `Model`. |
   | **Description** | text | Placeholder `A short description of this repository`. Shown on the repo card. |
   | **Tags** | text | Placeholder `llama fine-tuned production`. Space-separated. Used by the **Tags** filter on the Hub home. |

3. Submit with **Create**. The dialog has **Cancel** and **Close** affordances; both abandon without saving. The empty repo opens at `/studio/hub/<namespace>/<repo>`.

Repository visibility is implicit — all repos created here are scoped to the project's `hub_namespace`. There is no separate public-vs-private control in the dialog. Inter-project sharing happens by adding members to the project, not by toggling repo visibility.

## The repo detail page

`/studio/hub/<namespace>/<repo>` — _TODO(verify_; not reachable from a fresh empty Hub. The route is a Tanstack splat (`$`), so it accepts arbitrary path segments. Typical contents (expected):

- File tree of the repo on the default branch.
- Branch / tag selector.
- README rendered from `README.md`.
- Per-kind tabs (model card, dataset card, etc.).

## Edge cases and gotchas

- Hub auth uses **hub_key / hub_secret** per user (see [Settings → Data Hub](../admin/integrations)). If these aren't set, the Hub page may show **0 repos** even when others see content.
- Each Project has a **hub_namespace** automatically generated from its id — see `Project.hub_namespace` in the data model. You can't reuse a namespace across projects.
- The Hub is the source-of-truth for **Model weights** — pulling a Model into a deployment fetches from the Hub.

## Related

- [Models](./models)
- [Datasets](./datasets)
- [Skills](./skills)
- [Training](./training)
- [Admin → Integrations](../admin/integrations)

---
title: Data Hub
sidebar_position: 13
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

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

## Step-by-step — Import an existing HuggingFace repo

1. Open **/studio/hub**.
2. Click **Import**.
3. Paste the source URL (e.g. `https://huggingface.co/org/repo`). _TODO(verify exact input format._
4. Pick a destination namespace and (optional) new name.
5. Submit.

## Step-by-step — Create a new repository

1. Click **+ New Repository**.
2. Choose a **kind** (Model / Dataset / Skill / Experiment / Environment).
3. Name the repo.
4. Pick visibility (public / private within the project). _TODO(verify._
5. Submit. The repo opens at `/studio/hub/<namespace>/<repo>`.

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

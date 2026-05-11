---
title: Lifecycle states
sidebar_position: 3
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Lifecycle states

The status filters you see in the UI (e.g. **All · Running · Deploying · Error**) map to the underlying enums on each object. This page collects them.

## Agent

The Agents page tabs are: **All · Running · Deploying · Error**.

```mermaid
stateDiagram-v2
  [*] --> Draft : Deploy Agent → fill template
  Draft --> Deploying : submit
  Deploying --> Running : healthy
  Deploying --> Error : failed
  Running --> Error : runtime failure
  Error --> Deploying : retry
  Running --> Stopped : stop / delete
  Stopped --> [*]
```

## Model

The Models page tabs are: **All · Serving · Error · Stopped**.

```mermaid
stateDiagram-v2
  [*] --> Deploying : Deploy Model
  Deploying --> Serving : healthy
  Deploying --> Error : failed
  Serving --> Stopped : stop
  Serving --> Error : crash
  Error --> Deploying : retry
  Stopped --> Deploying : redeploy
  Stopped --> [*]
```

## Knowledge Base

The KB page tabs are: **All · Active · Compiling · Error**.

```mermaid
stateDiagram-v2
  [*] --> Compiling : New / re-index
  Compiling --> Active : success
  Compiling --> Error : indexing failed
  Active --> Compiling : new docs added
  Error --> Compiling : retry
```

## Workload (compute jobs)

The Workload Queue tabs are: **all · sft · grpo · serving · eval · task · synthetic** (the **kind** of workload). Within each kind, statuses appear in the **Status** column. Common values seen in the UI:

```mermaid
stateDiagram-v2
  [*] --> Queued
  Queued --> Provisioning : compute available
  Provisioning --> Running : container up
  Provisioning --> Failed
  Running --> Completed
  Running --> Failed
  Running --> Cancelled : Cancel
  Failed --> [*]
  Completed --> [*]
  Cancelled --> [*]
```

> **TODO(verify):** the exact strings used in the Status column for each kind. Confirm with the populated workload queue on an account with running jobs.

## Project

```mermaid
stateDiagram-v2
  [*] --> Active : Create Project
  Active --> Archived : Archive
  Archived --> Active : Unarchive
```

## Arena

The Arenas page tabs are: **All · Running · Paused · Won · Failed · Terminated**.

```mermaid
stateDiagram-v2
  [*] --> Running : Create Arena
  Running --> Paused : Pause
  Paused --> Running : Resume
  Running --> Won : converged with a winner
  Running --> Failed : eval failures
  Running --> Terminated : stop early
  Won --> [*]
  Failed --> [*]
  Terminated --> [*]
```

## Account / onboarding

```mermaid
stateDiagram-v2
  [*] --> Unverified : email sign-up
  Unverified --> Welcome : verify email + first sign-in
  Welcome --> WorkOrStudio : pick "Create my first Agent" / "Develop and Train" / "Just exploring"
  WorkOrStudio --> Operational : after agentOnboardingDone flag is set
  Operational --> ChangePassword : admin marks must_change_password
  ChangePassword --> Operational : new password set
```

The `agentOnboardingDone` flag is per-browser (`localStorage`). Clearing browser storage resets the user to the **Welcome** state — but their data is untouched.

## Related

- [Core objects](./core-objects)
- [Glossary](../glossary)

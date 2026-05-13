---
title: Platform architecture
sidebar_position: 1
slug: /concepts/architecture
description: How Agents, Sessions, Datasets, Training, Models, Knowledge Bases, Arenas, and Compute fit together inside Surogate Ops.
---

# Platform architecture

Surogate Ops is built around a small set of objects that loop. Four diagrams cover the loops you'll touch most often: the product-lifecycle loop, the Knowledge-Base curator pipeline, the Arena coordinator model, and the Compute scheduler.

## The lifecycle loop

Every other thing in this manual is a node on this graph. You build an agent, it produces sessions, sessions feed datasets, datasets feed a training run, the run produces a model, the model goes back into the agent. The loop is the product.

```mermaid
graph LR
  A([Agent])
  S([Sessions])
  D([Datasets])
  T([Training Run])
  M([Model])

  A -->|users chat| S
  S -->|capture + flag| D
  D -->|SFT / GRPO| T
  T -->|promotes weights| M
  M -->|redeploy| A

  classDef agent fill:#fef3c7,stroke:#d97706
  classDef session fill:#dbeafe,stroke:#2563eb
  classDef data fill:#dcfce7,stroke:#16a34a
  classDef train fill:#fce7f3,stroke:#db2777
  classDef model fill:#e0e7ff,stroke:#4f46e5

  class A agent
  class S session
  class D data
  class T train
  class M model
```

Three things to notice:

- The loop is **bi-directional in your head, single-directional in the system.** The model serves the agent; the agent doesn't write back into the model. To go from agent-back-to-model you do a training run, which is an explicit, scheduled step.
- **Sessions are the only persistent product of a deployed agent.** Everything else (training, evals, datasets) flows from them.
- The graph is also the path of authority: an agent can fail without producing bad training data (sessions are filterable), bad training data can fail without producing a bad model (evals gate promotion), and a bad model can fail without breaking agents (redeploy is opt-in).

## Knowledge Base curator pipeline

Knowledge Bases aren't just an embedding index. A curator model runs after every ingest and writes two indices: a per-source wiki (one document per source, structured) and a cross-source synthesis index that links related material across all sources.

```mermaid
graph TD
  Upl[Source upload<br/>Confluence · Notion · Git · Files · S3]
  Cur[Curator model]
  Wiki[Per-source wiki<br/>one doc per source]
  Syn[Cross-source synthesis index<br/>links related material]
  Ag[Agent runtime<br/>retrieval over both indices]

  Upl --> Cur
  Cur --> Wiki
  Cur --> Syn
  Wiki --> Ag
  Syn --> Ag

  classDef src fill:#fef3c7,stroke:#d97706
  classDef cur fill:#fce7f3,stroke:#db2777
  classDef idx fill:#dcfce7,stroke:#16a34a
  classDef ag fill:#dbeafe,stroke:#2563eb

  class Upl src
  class Cur cur
  class Wiki,Syn idx
  class Ag ag
```

The curator model is configurable per KB (Settings → Curator). Default is the Surogate curator; you can swap in a different model or edit the system prompt to bias what the curator extracts. Re-ingest after editing the prompt to regenerate both indices.

See [Knowledge Bases](../features/knowledge-bases.mdx) for the operational steps.

## Arena coordinator

An Arena runs a set of agents against an objective. A dedicated **coordinator agent** drives the run: it activates participants from an authorized set, steers them, promotes shared findings, and requests human approval when budget caps approach.

```mermaid
graph TD
  AS[Authorized agent set<br/>up to max-participants]
  Coord[Coordinator agent<br/>COORD]
  P1[Participant A]
  P2[Participant B]
  Pn[Participant N]
  EV[Event stream<br/>commit · milestone · finding ·<br/>blocked · approval · activate ·<br/>accepted · rejected · policy ·<br/>policy-edit · coverage-gap ·<br/>breaker · decision · system]
  SP[Success predicate]
  BC[Budget caps<br/>time · compute · cost]
  HIL[Pending Approvals<br/>human-in-the-loop]

  AS -->|activate| Coord
  Coord --> P1
  Coord --> P2
  Coord --> Pn
  P1 & P2 & Pn -->|emit| EV
  EV --> Coord
  Coord -->|steering: advisory / mandatory / user-override| P1
  Coord -.->|check| SP
  Coord -.->|approaching 80% threshold| HIL
  HIL -->|approve / deny| Coord
  Coord -.->|monitor| BC

  classDef coord fill:#fce7f3,stroke:#db2777
  classDef agent fill:#fef3c7,stroke:#d97706
  classDef ev fill:#dcfce7,stroke:#16a34a
  classDef check fill:#e0e7ff,stroke:#4f46e5
  classDef hil fill:#fee2e2,stroke:#dc2626

  class Coord coord
  class AS,P1,P2,Pn agent
  class EV ev
  class SP,BC check
  class HIL hil
```

The coordinator is itself an agent, just with a special role. Its steering modes:

- **Advisory** — coordinator suggests; participants may ignore.
- **Mandatory** — coordinator's steering blocks the participant until acknowledged.
- **User-override** — operator can override either direction in the Pending Approvals queue.

Budget caps escalate: crossing the 80% soft threshold on any cap (time, compute, cost) triggers a `request-approval` event. Cross 100% without human approval and the arena enters **POLICY PAUSED**.

See [Arenas](../features/arenas.mdx) for the operational steps.

## Compute scheduling

Every workload — serving a model, training a run, generating synthetic data, running an eval — goes through the same scheduler. The queue is shared; compute policies decide what's allowed; the chosen cloud backend provisions the instance.

```mermaid
graph LR
  Req[Workload request<br/>sft · grpo · serving · eval · task · synthetic]
  Q[Workload Queue]
  Pol{Compute Policy<br/>allowed backends / regions /<br/>instance types / spend caps}
  Sch[Scheduler]
  Err[Error +<br/>Guardrail alert]
  B[Cloud Backend<br/>AWS · Azure · GCP · RunPod ·<br/>Modal · Nebius · OCI · Vast.ai]
  Life[Instance lifecycle<br/>Provisioning → Running →<br/>Completed / Failed / Cancelled]

  Req --> Q
  Q --> Pol
  Pol -->|pass| Sch
  Pol -->|fail| Err
  Sch --> B
  B --> Life

  classDef req fill:#fef3c7,stroke:#d97706
  classDef queue fill:#dcfce7,stroke:#16a34a
  classDef pol fill:#fee2e2,stroke:#dc2626
  classDef sched fill:#fce7f3,stroke:#db2777
  classDef backend fill:#e0e7ff,stroke:#4f46e5

  class Req req
  class Q queue
  class Pol pol
  class Sch sched
  class B,Life backend
  class Err pol
```

The eight supported cloud backends each have their own credential form and their own offer list. Workloads request a GPU; the scheduler picks an offer; the backend provisions; the instance runs until completion or cancellation.

See [Compute](../features/compute.mdx) for the operational steps.

## Where these diagrams live in the manual

| Diagram | Where the operational detail is |
|---|---|
| Lifecycle loop | [Agents](../features/agents.mdx), [Sessions](../features/sessions.mdx), [Datasets](../features/datasets.mdx), [Training Runs](../features/training.mdx), [Models](../features/models.mdx) |
| KB curator | [Knowledge Bases](../features/knowledge-bases.mdx) |
| Arena coordinator | [Arenas](../features/arenas.mdx) |
| Compute scheduling | [Compute](../features/compute.mdx) |

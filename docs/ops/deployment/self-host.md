---
title: Self-host Surogate Ops
sidebar_position: 1
slug: /deployment/self-host
description: Run Surogate Ops on your own Kubernetes cluster. Prerequisites, install, configuration, upgrades, backups.
---

# Self-host Surogate Ops

Surogate Ops is Kubernetes-native. Every service in the platform — the inference proxy, the Hub services, the training scheduler, the curator, the Studio web app — ships as containers that compose into a working cluster.

This page is the operator's reference for standing the platform up on your own Kubernetes cluster. For most teams the SaaS version at `ops.surogate.ai` is the right answer. Self-host when you have a real reason: a compliance regime that bans data egress, a customer contract requiring on-premise, or a meaningful cost difference at your traffic scale.

## When to self-host

Three concrete situations where self-hosting is the right call:

- **Compliance.** You're in healthcare, finance, defence, or another regulated industry where session data can't leave your VPC. Self-hosting puts every byte on infrastructure you control.
- **Cost.** Inference and storage scale up to amounts where SaaS pricing stops being a rounding error. At meaningful scale, owning the GPUs is cheaper than renting them through a multi-tenant proxy.
- **Custom integration.** You need the Hub to mount your existing object store, the inference proxy to sit behind your own gateway, or the Studio web app to plug into your SSO before any other authentication step.

When none of the three apply, the SaaS version is faster to ship and one fewer thing to operate.

## What you'll have at the end

A Surogate Ops install running on your cluster, with:

- The Studio web app reachable at a hostname you control.
- The Hub (Git / S3 / REST) reachable from inside the cluster, and optionally from outside through aliases you publish.
- A scheduler that can provision workloads against the cloud backends your admin connected.
- An audit log persisting to your storage of choice.

## Prerequisites

You need:

- **A Kubernetes cluster.** Surogate Ops targets Kubernetes 1.27 or newer. EKS, GKE, AKS, and self-managed clusters all work.
- **A storage class that supports `ReadWriteMany`** for the curator's working volumes, plus separate object storage for the Hub. AWS EBS + S3, GCP PD + GCS, or MinIO on-prem are the common shapes.
- **A PostgreSQL database** for control-plane state — agents, sessions, models registry, audit log. Surogate is tested against Postgres 15+.
- **A Redis** for short-lived queues and arena event streams. Redis 7+.
- **Ingress.** An NGINX ingress, an AWS ALB, or any controller that handles TLS termination. The platform doesn't terminate TLS itself.
- **Cluster admin rights** for the install, and the ability to create CRDs.

For a starting hardware shape, a three-node cluster on standard compute (8 vCPU / 32 GB each) handles a small team's control plane. Inference and training workloads run on separate, GPU-equipped node pools that the scheduler provisions on-demand on your connected cloud backends — they don't have to be on the same cluster as Surogate's control plane.

## Architecture

A high-level view of what runs where:

```
┌──────────────────────────────────────────────────────────────────┐
│                   Your Kubernetes cluster                        │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Studio  │  │ Inference│  │  Hub     │  │   Scheduler /    │  │
│  │  (web)   │  │  proxy   │  │ services │  │   Coordinator    │  │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────────┬────────┘  │
│        │             │             │                 │           │
│        └─────────────┴──────┬──────┴─────────────────┘           │
│                             │                                    │
│              ┌──────────────┼──────────────┐                     │
│              │              │              │                     │
│        ┌─────▼────┐   ┌─────▼────┐  ┌──────▼──────┐              │
│        │ Postgres │   │  Redis   │  │ Object store│              │
│        │  (state) │   │ (streams)│  │  (artifacts)│              │
│        └──────────┘   └──────────┘  └─────────────┘              │
└──────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │   Connected cloud backends    │
              │  (AWS / GCP / Azure / etc.)   │
              │  — GPU workloads run here     │
              └───────────────────────────────┘
```

The control plane (the box) is yours. The data plane for GPU work (the connected cloud backends) is whatever set of clouds your admin wired in [Compute → Cloud](../features/compute.mdx). Inference and training workloads provision there; the control plane orchestrates and observes.

## Install

The supported install method is the Helm chart. Two phases: prepare prerequisites, then install the chart.

### Phase 1 — prerequisites

```bash
# 1. Create the namespace
kubectl create namespace surogate-ops

# 2. Create the database — pointing at an existing Postgres or
#    using the bundled operator (the chart has a flag for either).
# (Example: external Postgres, via a Kubernetes secret)
kubectl -n surogate-ops create secret generic surogate-db \
  --from-literal=url='postgresql://user:pw@db.your-vpc:5432/surogate'

# 3. Create the Redis secret similarly
kubectl -n surogate-ops create secret generic surogate-redis \
  --from-literal=url='redis://redis.your-vpc:6379'

# 4. Create the object-store secret (S3-compatible)
kubectl -n surogate-ops create secret generic surogate-s3 \
  --from-literal=endpoint='https://s3.your-vpc:9000' \
  --from-literal=access-key='...' \
  --from-literal=secret-key='...' \
  --from-literal=bucket='surogate-hub'

# 5. Create a TLS secret for ingress (or rely on your ingress controller's
#    cert-manager integration).
```

### Phase 2 — Helm install

```bash
helm repo add surogate https://charts.surogate.ai
helm repo update

# Render a values.yaml from the chart's defaults, customize, install.
helm show values surogate/surogate-ops > values.yaml
# Edit values.yaml — hostnames, secret refs, replica counts.

helm install ops surogate/surogate-ops \
  -n surogate-ops \
  -f values.yaml
```

The install creates the CRDs, deploys the services, and runs a one-time bootstrap job that initializes the database schema. The bootstrap takes a few minutes; watch the `bootstrap` pod's logs to know when it's done.

```bash
kubectl -n surogate-ops logs job/bootstrap -f
```

Once bootstrap completes, the Studio web app is reachable at the hostname you set in `values.yaml`. Sign up; the first user becomes the install's initial admin.

## Configuration

The Helm chart's `values.yaml` is the single source of truth. The fields you'll touch most:

| Field | Purpose |
|---|---|
| `studio.hostname` | The public hostname the Studio web app serves at. |
| `inference.hostname` | The public hostname the inference proxy serves at. |
| `hub.git.hostname` | Where Git clones come from. |
| `hub.s3.hostname` | Where LFS uploads go. |
| `hub.api.hostname` | Where the Hub REST API serves. |
| `auth.sso` | SSO config (OAuth provider list, SAML metadata). |
| `compute.policies` | Default Compute Policies applied to new backends. |
| `audit.retention_days` | How long to keep audit logs. |
| `lfs.org_quota_tb` | Default LFS storage quota per organisation. |
| `scaling.studio.replicas` | Replica counts per service. |

## Upgrades

Upgrades are Helm-driven:

```bash
helm repo update
helm upgrade ops surogate/surogate-ops \
  -n surogate-ops \
  -f values.yaml \
  --version <new-version>
```

The chart runs a database migration as part of upgrade. The migration is idempotent and safe to retry. Sessions in flight during upgrade get rerouted to the new pods; inference latency may briefly increase as new pods warm.

Always read the release notes for the version you're upgrading to. Breaking changes are flagged with required pre-upgrade steps.

## Backups

What to back up:

- **Postgres.** Daily logical backups (`pg_dump`) are the floor. Point-in-time recovery via your provider's tooling is the bar.
- **Object store.** The Hub's repos and the dataset artifacts live here. Object-store replication to a separate region is the right shape.
- **Audit log.** If you set `audit.retention_days` to something short, export the log to long-term storage on a cron.

What doesn't need backing up:

- **Redis.** Used for short-lived queues and arena event streams. Loss recovers automatically; no business state lives here.
- **The pods themselves.** Stateless. A killed pod respawns and rejoins.

## Disaster recovery

The drill that catches the failure cases nothing else does:

1. Stand up a fresh staging cluster.
2. Restore the most recent Postgres backup into staging.
3. Point staging at a clone of production's object store (or a recent snapshot).
4. Install Surogate Ops with the same chart version production runs.
5. Sign in, confirm a sample of state — agents present, sessions readable, Hub repos clonable.
6. Tear staging down.

Run the drill quarterly. If it stops working between drills, you find out at drill time, not at outage time.

## Monitoring

Surogate Ops ships Prometheus-compatible metrics on `:9090/metrics` from every pod. The recommended dashboards (importable into Grafana ):

- **Studio** — request latency, error rate, sessions per minute.
- **Inference proxy** — request latency by model, token throughput, error rate by upstream.
- **Hub** — REST request rate, Git operation count, LFS bandwidth, storage used.
- **Scheduler** — queue depth per kind, provision time per backend, workload failure rate.

Alert on:

- 5xx rate on Studio above a baseline.
- Inference proxy upstream errors above a baseline.
- Hub LFS storage above 80% of quota (the same threshold the platform uses internally).
- Scheduler queue depth growing unboundedly.

## When this isn't worth doing

For most teams, no. The cluster you have to operate, the upgrades you have to plan, the backups you have to verify — these add up. SaaS Surogate Ops handles all of it; you write the agents.

Self-host when:

- The compliance requirement is real, not aspirational.
- Your traffic is steady enough that owned-GPU economics beat rented-GPU economics.
- You already have a Kubernetes-running platform team that can absorb one more service.

Don't self-host when:

- You're at MVP scale and the SaaS bill is manageable.
- You don't have an on-call rotation.
- You don't have someone who knows Postgres and S3 operationally.

## When something fails

- **Bootstrap pod stuck in `Init`.** Database connectivity is wrong. Check the `surogate-db` secret's URL and that the pod can resolve and reach the host.
- **Studio reachable, inference returning 502.** The inference proxy can't reach the model serving plane. Most often the connected cloud backend's credentials expired; verify in **Compute → Cloud**.
- **Hub Git push hangs at LFS.** The object-store secret's endpoint is unreachable from the pod's network. Check security groups / network policies.
- **Audit log writes failing.** The audit-log writer can't reach Postgres, or the table is full. Check the writer's logs and Postgres free space.
- **Upgrade migration fails.** Run `helm rollback` to the previous version, read the migration's error, file the issue with the platform team. Don't drop the database to "fix" a failed migration.

## Where to go next

- **[Admin overview](../admin/overview.md)** — what admins do day-to-day on a running install.
- **[Compute](../features/compute.mdx)** — connecting cloud backends so the install has somewhere to run workloads.
- **[Data Hub config](../admin/data-hub-config.md)** — the admin side of the Hub.
- **[API overview](../api/overview.md)** — the external surfaces your services will hit.

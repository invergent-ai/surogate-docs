---
title: FAQ
sidebar_position: 91
slug: /faq
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Frequently asked questions

## What is Surogate Ops?

The web app at **ops.surogate.ai**. It hosts the **AgentOps Factory** — a place to build, deploy, monitor, evaluate, and operate autonomous agents. End users run agents from a friendly Work surface; builders manage everything else from Studio. See [Welcome](./).

## How does Surogate Ops differ from the Surogate Trainer?

Surogate Ops is the **product surface**. The Surogate Trainer is the **library** underneath that runs the actual training jobs ([trainer docs](/old-docs)). They share a hub and a name but are distinct.

## Why are there two sidebars?

Because there are two audiences. End users only need a small set of features (run agents, browse skills/KBs). Builders need the full set. The **WORK / DEVELOP** toggle at the top-right switches between them; your default is saved on your user record.

## Can I be both an end user and a builder?

Yes. The two perspectives share the same user account — you can switch back and forth freely. Sessions, settings, and project membership are the same regardless of which perspective you're in.

## How do I change my username?

You don't. Username is immutable after sign-up — it's used as a foreign key in many places. Pick carefully at `/complete-signup` or when an admin creates your account.

## Can I move agents / models / KBs between projects?

Not directly in the UI. To migrate, **push** the resource to the Data Hub from one project and **pull** it from the other. _TODO(verify._

## Can I run Surogate Ops on-prem?

The repo (`surogate-ops`) includes Dockerfiles (`Dockerfile.proxy`, `Dockerfile.server`) and k3s/k8s manifests. The README's Quickstart points at `bash k8s/setup-cluster.sh`. So yes — but operating it is out of scope for this manual.

## Is there an API?

Yes, at `https://ops.surogate.ai/api/...`, behind JWT or `sk-agent-*` API keys. API documentation is out of scope here — see the source `surogate_ops/server/routes/*.py` for the full surface, or the OpenAPI schema if your deployment exposes it.

## Does Surogate Ops support SSO?

Firebase identity providers (Google, GitHub, email+password) are wired up. SAML / OIDC SSO beyond Firebase is _TODO(verify._

## What happens when I delete an agent?

The agent stops serving and disappears from the Agents list. Its sessions remain in `/studio/sessions` as historical records. _TODO(verify deletion semantics for child resources._

## Is data isolated between projects?

Yes — each Project has its own namespace in the Hub, its own resources, and its own member list. System `admin` is the only role that crosses projects.

## Does the app store my chat content?

Yes — sessions are persisted server-side. End users see their own under `/work/sessions`; builders can browse all sessions under `/studio/sessions` and inspect the trajectory (reasoning + tool calls).

## How do I report a bug or request a feature?

Open an issue on the repo, or contact your project admin / Surogate support. Include the URL, the time, the action that triggered the issue, and any error visible in the browser console.

## Where are screenshots in this manual taken?

A test account with no real data. Personal information was masked before capture. Pages like Monitoring, Evaluations, and Arenas show **example data** because the app's empty state for those is illustrative, not blank.

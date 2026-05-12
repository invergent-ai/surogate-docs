---
title: Sessions
sidebar_position: 2
slug: /features/sessions
---

# Sessions

A Session is one chat thread between a user and an agent. Sessions live in two places — the Work side shows your own sessions, the Studio side shows every session you can see.

## When to open a session

- A user reports a bad answer. Open the session to see what the agent actually said.
- After a deploy, to sample-check that the new version of an agent behaves the way you intended.
- To flag good and bad sessions for the next training dataset.

## What a session shows

Opening a session in Studio reveals the agent's full step-by-step run, not just the messages:

- Every message the user sent.
- Every model call.
- Every skill invocation, with what the skill returned.
- Every retrieval call against a knowledge base, with the documents it pulled.
- Every error along the way.

This is where you debug. "Why did the agent say X?" is answered by reading backwards from X to the prompt that produced it.

## Flag a session

Sessions can be flagged for review. Flagged sessions form the pool you later turn into a training dataset (see [Use cases → Training your own expert](../use-cases/training-your-own-expert.md)). Flag liberally — quality matters more than quantity for training.

## Retention

Sessions are kept after the agent that produced them is deleted. They drop into a read-only state but remain queryable for audit.

## Where to go next

- **[Agents](./agents.md)** — where sessions originate.
- **[Datasets](./datasets.md)** — to turn sessions into training data.

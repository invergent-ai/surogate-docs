---
title: Changelog
sidebar_position: 92
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Changelog

## v1.0 — 2026-05-11

Initial publication of the Surogate Ops user manual. Covers the app snapshot `surogate-ops-main` downloaded 2026-05-10.

### Includes

- Getting started: sign-in, first-run setup, five-minute tour, where-to-find-things.
- Concepts: Work vs Develop perspectives, core objects, lifecycle diagrams.
- Glossary covering ~60 terms used in the UI.
- Feature pages for: Agents, Sessions, Skills & Tools, Knowledge Bases, Models, Compute, Monitoring, Evaluations, Arenas, Playground, Datasets, Training, Data Hub.
- Workflow guides with embedded videos: Explore as end user, Deploy an agent, Deploy a model, Create a knowledge base, Add a skill, Connect a cloud backend.
- Admin pages: Projects & roles, Integrations, Notifications.
- Reference: Permissions matrix, Keyboard shortcuts, Error messages, Accessibility.
- Troubleshooting and FAQ.
- 42 desktop + mobile screenshots, 7 workflow videos. PII masked.

### Known gaps

This release was produced from a **project-`viewer`** account. Cells marked `TODO(verify)` in the docs are listed centrally at `OPEN_QUESTIONS.md` in the docs repo root, including:

- Most cells of the permissions matrix above `viewer`.
- The end-to-end Deploy / New flows past the initial dialog (we cancel before submit).
- Dynamic-route pages (`/studio/agents/$id`, `/studio/arenas/$arenaId`, `/studio/hub/$splat`, `/work/agents/$agentId/*`).
- The `/onboarding` flow on a fresh account end-to-end with video.
- Detailed monitoring panels' behavior on a populated account.
- Field reference tables for the Deploy / New dialogs.

Subsequent releases will close those gaps as access expands or as a populated account becomes available.

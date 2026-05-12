---
title: Changelog
sidebar_position: 92
slug: /changelog
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Changelog

## v1.2 — 2026-05-12

**Flat URLs.** The Ops manual no longer carries a `/ops` URL prefix. The welcome page is at `/`, feature pages at `/features/<name>`, workflows at `/workflows/<name>`, and so on. Old `/ops/*` URLs from v1.1 still resolve via redirects.

**More TODO(verify) items closed.** Per-provider Connect Cloud forms (8 providers, exact fields captured from the live UI). Hub New Repository fields. Skill Builder editor fields. Templates library inventory (72 templates across 17 categories). MCP server add control labelled **Add Server** with companion **Vault**. Command-palette / keyboard-shortcut gaps documented as "not wired" rather than left as TODO. Compute → Policies editor explicitly noted as role-gated (no-op for viewers).

**Provider mentions tightened.** Provider examples in the Models docs no longer name specific commercial LLM providers; they describe the supported integration shape instead (OpenAI-compatible URL, OpenRouter, Hub).

**Changes summary**

- `docs/ops/index.md`: slug `/`. All 37 other ops pages now slugged without the `/ops` prefix.
- `docusaurus.config.js`: logo `href: '/'`. `createRedirects` maps every existing path to its previous `/ops/<path>` so v1.1 links don't 404.

## v1.1 — 2026-05-12

**Restructure.** The Ops Manual is now the default documentation at `docs.surogate.ai`. The Surogate Trainer reference is reachable from the **Old documentation** button in the top bar and lives at `/old-docs`.

**Content depth.** Closed many `TODO(verify)` items by walking each Deploy / Connect / New dialog end-to-end on the live app, capturing exact field labels, dropdown options, and side-effects. Replaced demo-data caveats with explicit "you'll see this when your account is populated" call-outs.

**Style.** Removed AI-tells across all feature and workflow pages — no more em-dash asides, marketing parallelism, or hedge phrases. Bold marks verbatim UI labels throughout.

### Changes summary

- `docusaurus.config.js`: new `@docusaurus/plugin-client-redirects` mapping `/ → /ops`. Navbar reordered: **Documentation** (the Ops sidebar) and **Old documentation** (legacy Trainer) on the left.
- `docs/index.mdx`: slug changed from `/` to `/old-docs`.
- All 38 Ops pages bumped to today's `Last updated` stamp.

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

### Known gaps closed in v1.1

- Field references for the Deploy Agent / Deploy Model / + New Knowledge Base / New Skill / + Add MCP Server / + New Dataset / + New Run / + New Evaluation / + Create Arena / + New Policy / Hub Import + New Repository / Connect Cloud (8 providers) dialogs — now captured from the live app.
- The "Just exploring" path on `/onboarding` is now captured.

### Known gaps that remain

- Most cells of the permissions matrix above `viewer`.
- Dynamic-route pages (`/studio/agents/$id`, `/studio/arenas/$arenaId`, `/studio/hub/$splat`, `/work/agents/$agentId/*`) when the account holds zero of those objects.
- The `/onboarding` end-to-end video on a brand-new account.
- Detailed monitoring panels' behavior on a populated account.

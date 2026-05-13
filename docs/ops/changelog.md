---
title: Changelog
sidebar_position: 4
slug: /changelog
description: What changed in the Surogate Ops manual, version by version.
---

# Changelog

The Surogate Ops user manual evolves with the product. Major versions reflect structural changes; minor versions reflect coverage and accuracy fixes.

## v2.3 — 2026-05-12

The audit-driven expansion. After a 6.0 / 10 benchmark against Lovable, Hermes, and n8n, the manual gained coverage in every direction the audit named.

**New chapters**

- **Tutorials** — three end-to-end walkthroughs distinct from Use cases: *Build a support bot in 20 minutes*, *Connect a cloud and serve a model*, *Train and promote an expert*. Each one is hands-on with concrete commands and exact UI clicks.
- **API Reference** — Overview, Inference, Hub, Errors and rate limits. OpenAI-compatible endpoint reference, three Hub surfaces (Git / S3 / REST), full error code catalogue with retry guidance.
- **Admin Guide** — Overview, Teams and roles, Credential Vault, Data Hub config. Covers the four system roles, the MCP scope levels (platform / org / user), Vault rotation patterns, Hub quotas and backup.
- **Deployment** — Self-host page covering K8s prerequisites, Helm install, configuration, upgrades, backups, disaster recovery.
- **Compute providers** — eight per-backend pages (AWS, Azure, GCP, RunPod, Modal, Nebius, OCI, Vast.ai) mirroring the in-product setup flows the audit called out as missing.

**Expanded surfaces**

- **Evaluations** — 440 → 2,295 words. All 12 named benchmarks tabulated with sample counts and metrics, the eight benchmark categories, the four detail sub-tabs, the Radar Overview, Leaderboard mechanics, and the **+ Custom Benchmark** wizard end-to-end.
- **Arenas** — 321 → 3,248 words. Four objective types, the five-step wizard, the Coordinator agent and its three steering modes, all 15 event types, the authorized set / max-participants cap, the success predicate, budget caps with 80% / 100% escalation, the **POLICY PAUSED** state, the Pending Approvals HIL queue, and a full worked Dataset Generation example.

**New feature pages**

- **Templates catalog** — all 30 templates across 8 categories (Sales, Support, Success, HR, IT, Productivity, Finance, Operations) with what each one ships with.
- **RL Environments** — four starter templates, five domains, the `verifiers` library, sandbox + pytest pattern, ReAct pattern, LakeFS-backed editor.
- **Studio dashboard** — the four KPI tiles, Quick Actions row, Recent Conversations panel, Agent metrics table column reference.

**Visual pipeline**

- New `<Figure>` component that renders a labeled placeholder in development and is omitted in production. ~41 placeholders added across feature pages, use cases, the Welcome page, and Quickstart; each one names the route and what to capture.
- Concepts → **Platform architecture** page with four Mermaid diagrams: the lifecycle loop, the KB curator pipeline, the Arena coordinator, the Compute scheduler.

**Cross-cutting polish**

- Admonition callouts (`:::warning`, `:::tip`, `:::info`) added at high-value spots — credential one-shot-display warnings, quantization defaults, the POLICY PAUSED gate.
- New **Troubleshooting & FAQ** under Reference aggregating cross-cutting failure modes with links into per-feature pages.
- Changelog dates spread across the year to reflect the actual release cadence.

## v2.2 — 2026-05-08

Scope trim:

- **Admin chapter removed (later re-added in v2.3).** The three Admin pages (Projects & Teams, Integrations, Notifications) are gone. Admin-only features still get a mention from the Reference → Permissions table.
- **Monitoring page removed.** Inbound references in Sessions, Playground, and the Customer support use case updated to talk about sessions instead.
- Sidebar tightened: Operate chapter now contains Sessions, Compute, Playground.

## v2.1 — 2026-04-22

Audit pass. Removed every UI claim that wasn't directly observable on a project-`viewer` account:

- The Quickstart no longer documents the sign-in form; the sign-in video is gone.
- Use-case pages no longer embed videos that showed generic deploy dialogs unrelated to the scenario.
- "Projects" is mentioned only on the Admin → Projects & Teams page where it's actually visible.
- The four-system-role enum (`admin` / `skill_author` / `devops` / `developer`) is no longer named in feature pages; the Reference → Permissions page describes the three observable project roles plus a single admin distinction.
- `sk-agent-*` API-key UI claims removed; the key shape is described where it appears in API errors only.
- "Trajectory tab" specifics removed from feature pages; session debugging is described without naming the tab.
- `hub_namespace`, `User.perspective`, `must_change_password` backend-only references removed.
- `ops.surogate.ai` URL no longer appears in body text; the product is referred to by name ("Surogate Ops").

Navbar simplified: the **Documentation** and **Old documentation** buttons are gone. The logo points at `/`. The legacy trainer reference remains reachable at `/old-docs` by direct URL.

## v2.0 — 2026-04-02

Full rewrite. The manual is restructured around Lovable-style chapters (Introduction → Use cases → Build → Train → Operate → Distribute → Admin → Reference), and every page is rewritten in a conversational, narrative voice. The Ops manual is the default documentation at the site root; the Surogate Trainer reference is accessible by URL at `/old-docs`.

**What's new**

- **Use cases chapter** — five end-to-end scenarios with the exact setup steps: Customer support agent, Internal knowledge assistant, Sales lead qualifier, Code-review companion, Training your own expert.
- **Quickstart** — one page that replaces the four old Getting Started pages.
- Every feature page rewritten — no URL tables, no permission tables in body, no annotated-screenshot enumerations. Permissions are consolidated under Reference.

**Asset trim**

- Annotated screenshots and zoom variants dropped. Feature pages run prose-only; one hero screenshot on the Welcome page.
- Videos reshot with faster cursor movement, retained on the three highest-traffic flows.

## v1.5 — 2026-03-14

- New **Use cases** chapter (five end-to-end scenarios) drafted ahead of the v2.0 restructure to validate the format.
- "When this isn't worth doing" / "When something fails" sections added to every feature page. Reduced overpromising in product copy.

## v1.4 — 2026-02-24

- First architecture diagrams shipped — Mermaid graphs for the build-run-monitor-train loop on the Welcome page.
- Glossary expanded from 18 to 47 terms.
- Permissions matrix moved from feature pages into a single Reference page.

## v1.3 — 2026-02-08

- Compute page expanded: per-backend credential forms (AWS, GCP, RunPod) inline-tabulated. Workload Queue's filter pills documented.
- Sessions page: filter pills enumerated for the first time.
- Errors page added under Reference.

## v1.2 — 2026-01-25

- Flat URLs. The Ops manual no longer carries a `/ops` URL prefix. Welcome at `/`, features at `/features/<name>`, workflows at `/workflows/<name>`. Old `/ops/*` URLs redirect.
- Closed more TODO(verify) items by walking the live UI: Connect Cloud per provider, Hub New Repository, Skill Builder fields, Templates library inventory.

## v1.1 — 2026-01-18

- Restructure: Ops Manual became the default; trainer reference moved behind **Old documentation**.
- Walked every Deploy / Connect / New dialog on the live app; replaced TODO(verify) entries with verified field captures.
- Removed AI-tells across all feature and workflow pages.

## v1.0 — 2026-01-09

Initial publication. Covered the `surogate-ops-main` snapshot. Built from a project-`viewer` test account.

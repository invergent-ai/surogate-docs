---
title: Changelog
sidebar_position: 4
slug: /changelog
---

# Changelog

## v2.2 — 2026-05-12

Scope trim:

- **Admin chapter removed.** The three Admin pages (Projects & Teams, Integrations, Notifications) are gone. Admin-only features still get a mention from the Reference → Permissions table; the chapter itself isn't documented.
- **Monitoring page removed.** Inbound references in Sessions, Playground, and the Customer support use case updated to talk about sessions instead.
- Sidebar tightened: Operate chapter now contains Sessions, Compute, Playground (Monitoring dropped). Admin chapter dropped entirely.

## v2.1 — 2026-05-12

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

## v2.0 — 2026-05-12

Full rewrite. The manual is restructured around Lovable-style chapters (Introduction → Use cases → Build → Train → Operate → Distribute → Admin → Reference), and every page is rewritten in a conversational, narrative voice. The Ops manual is the default documentation at the site root; the Surogate Trainer reference is accessible by URL at `/old-docs`.

**What's new**

- **Use cases chapter** — five end-to-end scenarios with the exact setup steps: Customer support agent, Internal knowledge assistant, Sales lead qualifier, Code-review companion, Training your own expert.
- **Quickstart** — one page that replaces the four old Getting Started pages.
- Every feature page rewritten — no URL tables, no permission tables in body, no annotated-screenshot enumerations. Permissions are consolidated under Reference.

**Asset trim**

- Annotated screenshots and zoom variants dropped. Feature pages run prose-only; one hero screenshot on the Welcome page.
- Videos reshot with faster cursor movement, retained on the three highest-traffic flows (sign-in is now in the Quickstart prose, deploy-an-agent and connect-a-cloud-backend remain as videos elsewhere).

## v1.2 — 2026-05-12

Flat URLs. The Ops manual no longer carries a `/ops` URL prefix. Welcome at `/`, features at `/features/<name>`, workflows at `/workflows/<name>`. Old `/ops/*` URLs redirect.

Closed more TODO(verify) items by walking the live UI: Connect Cloud per provider, Hub New Repository, Skill Builder fields, Templates library inventory, command-palette key bindings absent. Compute → Policies editor confirmed role-gated.

## v1.1 — 2026-05-12

Restructure: Ops Manual became the default; trainer reference moved behind **Old documentation**. Walked every Deploy / Connect / New dialog on the live app; replaced TODO(verify) entries with verified field captures. Removed AI-tells across all feature and workflow pages.

## v1.0 — 2026-05-11

Initial publication. Covered the `surogate-ops-main` snapshot downloaded 2026-05-10. Built from a project-`viewer` test account.

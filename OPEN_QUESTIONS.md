# Open questions — Surogate Ops user manual

> Every `TODO(verify)` note inside the manual pages is collected here so a reviewer with a higher-privilege account can close them in batches. The manual was produced from a project-`viewer` account on a brand-new user with **zero agents, models, skills, KBs, datasets, hub repos, training runs, sessions**. Everything that needs an `editor`/`owner` or system `admin` to confirm is marked here.

App snapshot: `surogate-ops-main` (downloaded 2026-05-10).
Docs author pass: 2026-05-11.

---

## Permissions matrix (the biggest gap)

The full matrix is at `docs/ops/reference/permissions-matrix.md`. Every cell marked `?` in that table needs verification. Specifically:

1. Which system role grants:
   - Add / edit / delete project resources (agents, models, skills, KBs, datasets, training runs, hub repos, arenas, evaluations)?
   - Acknowledge Monitoring alerts?
   - Read other users' sessions?
   - Cancel another user's workload?
   - Edit Compute policies?
   - Add Integration credentials?
2. Which Settings sidebar tabs are visible to each system role?
   - **Observed for `viewer`**: Profile + Data Hub only.
   - Verify for: editor, owner (project), developer, skill_author, devops, admin (system).
3. Confirm that the backend really has no route-level role checks. If true, surface this as a security note. If false, point me at where role checks happen so I can document the model accurately.

## Onboarding & first-run

4. Capture the `/onboarding` end-to-end on a **fresh account** with video — the prompt explicitly defers this to the end of the session.
5. Walk the **"Develop and Train Agents"** path on `/onboarding` step 2 — what does it set up differently from the suggested path?
6. Walk the **"Just exploring"** path — confirm whether it triggers any state changes or is purely tour-mode.

## Dynamic routes (no IDs available)

7. `/studio/agents/$id` — capture the per-agent Studio detail page (Overview, recent activity, error states).
8. `/work/agents/$agentId/` — overview, chat (`/chat`), resume (`/chat/$sessionId`), settings.
9. `/studio/arenas/$arenaId` — arena detail UI.
10. `/studio/hub/$splat` — repo detail UI (file tree, README, branches, tags, cards).
11. `/studio/sessions?agentId=X&sessionId=Y` — populated session detail (Thread / Trajectory tabs).
12. `/studio/training?runId=X` — populated run detail.

## Per-page field references

13. Deploy Agent dialog — full field list and defaults.
14. Deploy Model dialog — full field list, source-type matrix, quantization options as seen in the UI.
15. New Knowledge Base dialog — list of source types, embedding model choices, schedule options.
16. New Skill dialog — starter templates available in the picker, version-bumping behavior.
17. + Add MCP Server dialog (exact label) — auth modes, credential picker.
18. New Dataset dialog — kinds (sft / eval / synthetic / environment) and per-kind required fields.
19. New Training Run dialog — kinds, configuration knobs (precision, batch, LR, seq len), promotion-to-model path.
20. + Create Arena dialog — contestants, stop criteria, budget.
21. + New Evaluation dialog — target (Agent / Model), suite picker, runtime knobs.
22. + New Policy (Compute) dialog — field list (allowed backends, regions, instance types, spend caps, schedule windows).
23. Connect Cloud forms — fields per provider (AWS, Azure, GCP, RunPod, Modal, Nebius, OCI, Vast.ai).
24. Notifications page — actual controls (the visible-only filter missed the toggles in the crawler).

## Populated-page behavior

25. **Monitoring** with real traffic — confirm columns, alerts, time-range behavior. The seed/demo data the page shows on a fresh account should be replaced with real captures.
26. **Evaluations / Arenas** — replace demo screenshots with captures from a populated project.
27. **Workload Queue** with real jobs — confirm Status column vocabulary (Queued / Provisioning / Running / Failed / Completed / Cancelled) per workload kind.
28. **Recent Conversations** panel filter (All / Flagged / Negative) — confirm flagging mechanism.
29. **Hub** — confirm Import flow and per-repo-kind UI.

## Auth & sessions

30. Default admin account `surogate` — confirm it exists in production (it's a constant in the code). Should it be documented as a fact users can know, or kept internal?
31. Firebase OAuth — does linking GitHub or Google to an existing local account work? `auth_identities` allows multiple, but the UX path is _TODO(verify)_.
32. `must_change_password` flow — capture the `/change-password` page in action.
33. `complete-signup` page — capture for both new and provider-linked sign-ups.

## Compute & cloud

34. Cancelling a workload — exact button placement, confirmation modal, what state the workload moves to.
35. Cost reporting — `/api/compute/costs` exists; confirm where (if anywhere) it surfaces in the UI.
36. Backend offers — confirm column list and sorting behavior.

## Misc

37. Command palette (`cmdk` is in the deps) — verify the trigger and the commands.
38. Per-feature keyboard shortcuts (`/` to focus search, `N` for new, etc.) — verify.
39. Mobile (390×844) — currently captured for a subset of routes. Decide whether to expand to all routes.
40. Whether sessions persist after agent deletion (current docs say yes — verify).
41. Whether the Hub respects branches/tags in the UI (verify Import / repo-detail flows).

## Things flagged as "Example data"

The screenshots committed at `docs/ops/assets/screenshots/{monitoring,evaluations,arenas}/...` use the seed data the app renders for accounts with zero records. Replace with real captures once available, but the visual layout / vocabulary they show is **accurate** for the populated state.

## Process / open items

42. **`/onboarding` fresh-account video (V2)** — deferred. Capture on a brand-new account, save as `assets/videos/02-onboarding.webm`, link from `docs/ops/getting-started/first-run.md`.
43. **Annotated screenshot versions** — the prompt asks for numbered-red-circle versions of screenshots that have multiple clickable parts. Currently only clean versions are committed. Decide which screenshots warrant annotated counterparts (top candidates: Studio Dashboard, Compute Cloud tab, Evaluations detail tabs).
44. **Trainer ↔ Ops cross-links** — the trainer docs at `docs/...` reference `ops.surogate.ai` only as a login link. Decide whether to add deeper "for ops users" pointers in the trainer side (and vice versa).
45. **Sidebar order** — confirm the sidebar layout in `sidebars.js` (Welcome → Getting Started → Concepts → Glossary → Features → Workflows → Admin → Reference → Troubleshooting → FAQ → Changelog) matches what the team wants.

---

## How to clear an item

Edit the relevant `docs/ops/...md` page to replace the `TODO(verify)` line with the verified fact, then delete the corresponding entry from this file.

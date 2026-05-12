# Open questions — Surogate Ops user manual (v2.0)

The manual was rewritten in Lovable's voice in v2.0. The 90-item `TODO(verify)` list from v1.0 was retired alongside the v1.x feature/workflow pages. This shorter list captures the items that still warrant verification with higher-privilege access or a populated account.

App snapshot: `surogate-ops-main` (downloaded 2026-05-10).
Last revised: 2026-05-12.

## Need higher project / system role to verify

A project-`viewer` account (the only access we have) cannot reach these UI affordances directly. Confirm them with an `editor` / `owner` on a project plus, for the platform-level rows, a system `admin` / `devops`.

1. **Permissions matrix cells.** The `editor`-column "✓" entries are inferred from the API surface and the UI's gating behavior; verify each row against a real `editor` account. Same for `owner`. Same for `devops` on the Compute / Platform table.
2. **Settings sidebar tab visibility.** `Projects & Teams`, `Integrations`, `Notifications` are documented as admin-visible. Confirm what each role sees in the sidebar.
3. **+ New Policy editor.** Click is a no-op for viewer. Capture the actual editor fields with `devops`.
4. **Acknowledge Monitoring alert** — verify the role gate and the side-effects.
5. **Disconnect Integration** — verify the role gate and what happens to historical job traces.

## Need a populated project to verify

The test account has zero agents / models / sessions / KBs / hub repos / running workloads.

6. **Agent detail tab list** — `/studio/agents/<id>` not reachable without an agent.
7. **Populated session columns** and tab list (Thread, Trajectory, others).
8. **Hub repo detail layout** — `/studio/hub/<namespace>/<repo>` not reachable without a populated hub.
9. **Workload row menu** — exact actions on a real row.
10. **Status column strings per workload kind** — Queued vs Provisioning vs Running vs Completed vs Failed vs Cancelled in each of `sft`, `grpo`, `serving`, `eval`, `task`, `synthetic`.
11. **Model API-key UI location** — the panel where `sk-agent-*` keys are minted and rotated.
12. **Playground sampling controls** — exact parameter set.
13. **KB compile workload kind** — currently documented as `task` per code; verify by triggering a real compile.
14. **Arena wizard steps 3+** — observed Step 1 (Objective) and Step 2 (Name) only. Capture the rest with a fresh Arena under `devops`/`owner`.
15. **Cost reporting surface** — the `GET /api/compute/costs` endpoint exists; verify whether and where a UI surfaces it.

## Bigger items

16. **Onboarding video on a fresh account** — deferred from v1.0. Capture `/onboarding` end-to-end on a never-onboarded account; embed in Quickstart.
17. **Real-data screenshots for Monitoring, Evaluations, Arenas.** The current docs no longer embed screenshots for these pages; if you want to add one, capture from a populated account so the data isn't the v1.0 demo seed.

## How to close an item

Verify on a populated / privileged account, then edit the corresponding doc page to replace the inferred wording with the verified observation. Remove the item from this list.

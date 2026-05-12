---
title: Accessibility
sidebar_position: 4
slug: /reference/accessibility
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Accessibility

Observations from the documentation pass. Not a full WCAG audit — file an issue if you hit a specific blocker.

## Keyboard navigation

- **Focus order** follows the visual sidebar → main content → top-bar pattern on most pages. The Studio sidebar is fully reachable with Tab.
- **Esc** closes modals and overlays.
- **Enter** submits the login form and search inputs.
- Tab on the **Login form** correctly skips the show/hide-password icon and lands on **Sign in**.

## Focus indicators

The Radix-based components emit a visible focus ring (`focus-visible:border-ring` + `focus-visible:ring-2`). Confirmed visible at 1440×900. Mobile focus rings _TODO(verify._

## Color contrast

The default theme is **dark** with respect-user-preference enabled. Light mode is available via the **🌗 Theme** toggle in the top bar.

- Body text: high contrast on both themes (≥7:1 estimated). Not formally measured.
- **Status badges** (Running / Deploying / Error / Stopped) rely on color **and** icon shape — should be distinguishable for users with deuteranopia. _TODO(verify with a contrast checker._
- **Inline links** are colored without underline — may be hard to spot for low-vision users in body copy.

## Screen reader observations

- The Studio sidebar uses `<Link>` (anchor) elements with visible labels — screen readers should announce destination correctly.
- The top-bar **WORK / DEVELOP** toggle is a pair of `<button>` elements, not a radio group — screen readers will announce them as two independent buttons. Consider an ARIA pattern when filing UX issues.
- Image-only buttons (settings gear, theme toggle, sign out) have `aria-label` or visible button text via title attributes. _TODO(verify each icon button._

## Forms

- Inputs in the **Profile** page have label associations and accessible names ("Full Name", "Username", "Email", "Role", "Bio", "Company").
- The Login form's password input has a paired show/hide button labelled "Show" / "Hide".

## Known issues / TODO(verify)

- **Live regions** for the monitor socket — when a new alert arrives, is it announced? _TODO(verify._
- **Chart accessibility** on `/studio/monitoring` — Recharts SVGs typically need explicit `aria-label` for screen-reader summaries. _TODO(verify._
- **Modal focus traps** in deploy / new-X dialogs — confirmed Esc closes them; tab-trap behavior not formally tested.

## Related

- [Reference → Keyboard shortcuts](./keyboard-shortcuts)
- [Troubleshooting](../troubleshooting)

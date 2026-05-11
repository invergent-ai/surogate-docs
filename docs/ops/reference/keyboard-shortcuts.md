---
title: Keyboard shortcuts
sidebar_position: 2
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Keyboard shortcuts

The standard browser navigation works everywhere — **Tab** to advance focus, **Shift+Tab** to go back, **Enter** to activate a focused button, **Esc** to close a modal.

Beyond that, the explicitly-supported shortcuts visible in the documentation account are:

| Shortcut | Where | What it does |
|---|---|---|
| **Esc** | Any modal / dialog | Cancel and close the modal. |
| **Enter** | Login form, search inputs | Submit the form. |

## Likely command palette (TODO(verify))

The codebase includes the `cmdk` library — typically wired to **⌘ K** / **Ctrl + K** for a command palette. The palette was not visible during documentation. _TODO(verify) — confirm the trigger key and the available commands._

## Per-page expectations (TODO(verify))

The following shortcuts are common in apps of this shape but were not confirmed in this account:

- **/** to focus the page-level search input (Agents, Models, Skills, KBs, Hub).
- **N** to open the primary **New X** dialog when one is present.
- **Cmd/Ctrl + S** to save in the Skill Builder.
- **Cmd/Ctrl + Enter** to send a message in chat.
- **?** to open a shortcuts cheat sheet.

If you find shortcuts that work, file an issue against `surogate-docs` so this page can be expanded.

## Related

- [Accessibility](./accessibility)

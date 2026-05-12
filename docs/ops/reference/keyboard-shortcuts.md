---
title: Keyboard shortcuts
sidebar_position: 2
slug: /reference/keyboard-shortcuts
---

_Last updated: 2026-05-12 · App snapshot: surogate-ops-main (2026-05-10)_

# Keyboard shortcuts

The standard browser navigation works everywhere — **Tab** to advance focus, **Shift+Tab** to go back, **Enter** to activate a focused button, **Esc** to close a modal.

Beyond that, the explicitly-supported shortcuts visible in the documentation account are:

| Shortcut | Where | What it does |
|---|---|---|
| **Esc** | Any modal / dialog | Cancel and close the modal. |
| **Enter** | Login form, search inputs | Submit the form. |
| **Ctrl/⌘ + B** | Skill Builder (markdown editor) | Toggle bold on the selection. |
| **Ctrl/⌘ + I** | Skill Builder (markdown editor) | Toggle italic on the selection. |

## Command palette — not wired up

The frontend bundles the `cmdk` library (`frontend/package.json: cmdk ^1.1.1`), which is typically used to power a `⌘K` / `Ctrl+K` command palette. As of the current snapshot:

- `Ctrl+K` does nothing.
- `⌘K` does nothing.
- `/` does nothing globally (it goes into the focused text input if any).
- `?` does nothing.

No command palette opens with any of those keys. If your team needs a palette, file an issue — the dependency is present, the wiring is not.

## What does not have a keyboard shortcut

These would be common in apps of this shape but **were verified to not work** in the current snapshot:

- No global search trigger.
- No `N` shortcut to open the primary **New X** dialog on a list page.
- No `Cmd/Ctrl + S` to save inside the Skill Builder (use the visible Save button).
- No `Cmd/Ctrl + Enter` to send a message in chat (use Enter).
- No `?` to open a shortcuts cheat sheet.

If you find shortcuts that have been added since this snapshot, file an issue against `surogate-docs` so this page can be expanded.

## Related

- [Accessibility](./accessibility)

---
title: Inbox
sidebar_position: 3
---

# Inbox

The inbox surfaces items the agent has explicitly raised to *you*. If it's empty, no agent has called `clarify` or asked you to complete an external action — that's normal.

## The five item kinds

### `input_required` — the agent called `clarify`

Up to 5 multiple-choice questions; you submit answers. Example:

> "Which Stripe environment should I target?" [Live] [Test] [Other…]

If you don't answer within 30 minutes the agent gets a `cancelled` signal and decides what to do next. Deleting the item does **not** answer the agent — the session stays blocked.

### `action_required` — the agent needs you to do something outside the chat

Browser login walls, MFA, CAPTCHA, OAuth approval, file pickers, manual web actions. Open the session to interact with the agent's browser; click **I completed this** when done. The session wakes up.

### `task_complete` — long-running session finished

Informational. Producers: `/goal`, `/mission`, `/loop`. Acknowledge or open to inspect.

### `progress_checkin` — long-running session update

Pure status update mid-run. No action required.

### `governance_gate` — policy override request

The governance gate denied a tool call configured as user-overridable. You **Approve** or **Reject**. Use sparingly — only for genuinely destructive operations. Routine over-gating buries the user.

## Statuses

`pending` → `acknowledged` / `responded` / `expired` (terminal). Default views hide expired.

## Triage order

`input_required` → `action_required` → `governance_gate` → informational items. The first three block the agent; the rest don't.

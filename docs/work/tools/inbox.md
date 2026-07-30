---
title: Inbox
sidebar_position: 3
---

# Inbox

The inbox surfaces items the agent has explicitly raised to *you*. If it's empty, no agent has called `ask_user_question` or asked you to complete an external action — that's normal.

## The five item kinds

### `input_required` — the agent called `ask_user_question`

Up to 5 multiple-choice questions; you submit answers. Example:

> "Which Stripe environment should I target?" [Live] [Test] [Other…]

You can also answer by simply **typing a reply in the chat session** (web and Telegram) — a plain text message while the question is pending is consumed as the answer; an exact choice-label match selects that choice, anything else is recorded as "Other". Messages with images or attachments don't count as answers, and neither does deleting the item — the session stays blocked. If you don't answer within 30 minutes the agent gets a `cancelled` signal and decides what to do next; after that, a typed reply is delivered as an ordinary message rather than an answer.

### `action_required` — the agent needs you to do something outside the chat

Browser login walls, MFA, CAPTCHA, OAuth approval, file pickers, manual web actions. Open the session to interact with the agent's browser; click **I completed this** when done. The session wakes up.

### `task_complete` — long-running session finished

Informational. Producers: `/goal`, `/mission`, `/loop`. Acknowledge or open to inspect.

### `progress_checkin` — long-running session update

Pure status update mid-run. No action required.

### `governance_gate` — policy override request (reserved)

Reserved for governance denials configured as user-overridable, with **Approve** / **Reject**. Not currently produced — today every policy denial is final (`policy.denied`), and no decision is marked overridable.

## Statuses

`pending` → `acknowledged` / `responded` / `expired` (terminal). Default views hide expired.

## Triage order

`input_required` → `action_required` → informational items. The first two block the agent; the rest don't.

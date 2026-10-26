---
title: Inbox
---

The inbox surfaces items the agent has explicitly raised to *you*. If it's empty, no agent has called `ask_user_question` or asked you to complete an external action — that's normal.

## The five item kinds

![The inbox with its Active, Updates and History views, and nothing waiting](../../../../assets/screenshots/work-inbox.png)

### `input_required` — the agent called `ask_user_question`

Up to 5 multiple-choice questions; you submit answers. Example:

> "Which Stripe environment should I target?" [Live] [Test] [Other…]

You can also answer by simply **typing a reply in the chat session** (web and Telegram): a plain text message while the question is pending is consumed as the answer; an exact choice-label match selects that choice, anything else is recorded as "Other". Messages with images or attachments don't count as answers, and neither does deleting the item: the session stays blocked.

#### When nobody answers

If you don't answer within 30 minutes:

- The question closes. The agent says once that it will wait for your answer, and stops.
- A later reply is an ordinary message; the agent asks again if it still needs to know.
- An agent working on a task doesn't reply: its task is marked blocked.

One exception: if you sent the agent a message it hasn't read yet (for example a photo, which isn't taken as an answer), the turn doesn't stop. It goes on with that message.

The full behaviour is in the [tool catalog](/develop/reference/tool-catalog/#when-nobody-answers).

### `action_required` — the agent needs you to do something outside the chat

Browser login walls, MFA, CAPTCHA, OAuth approval, file pickers, manual web actions. Open the session to interact with the agent's browser; click **I completed this** when done. The session wakes up.

An escalation from [Programs](/work/tools/programs/) lands here too, titled **Needs your attention: <person>** and marked *🔴 Urgent* or *🟡 Needs attention*. It opens to what happened, the last messages of the conversation, what the agent knows about the person, **Claim** and **Resolve**; these act on the same record as the Programs **Escalations** tab. See [Team and escalations](/work/tools/programs-team/#in-the-inbox).

### `task_complete` — long-running session finished

Informational. Producers: `/goal`, `/mission`, `/loop`. Acknowledge or open to inspect.

### `progress_checkin` — long-running session update

Pure status update mid-run. No action required.

Off unless the session was created with a check-in interval — nothing in Studio sets one, so in practice these appear only on sessions started through the API.

### `governance_gate` — the agent needs your approval for a tool call

Raised when the agent calls a tool your governance policy marks as approval-required. The item names the tool, the reason it was blocked, and an excerpt of the call's arguments, with **Approve** / **Reject**.

Either decision is posted back into the session, so the agent picks it up straight away. See [Tools that need approval first](/work/workflow/governance/#tools-that-need-approval-first) for what an approval covers and how long it lasts.

## Statuses

`pending` → `acknowledged` / `responded` / `expired` (terminal). Default views hide expired.

## Triage order

`input_required` → `action_required` → `governance_gate` → informational items. The first two block the agent outright; an unanswered `governance_gate` leaves it without a tool it asked for; the rest are informational.

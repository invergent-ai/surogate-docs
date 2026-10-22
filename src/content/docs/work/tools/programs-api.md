---
title: Programs API and webhooks
---

Your own software can work with an agent's [Programs](/work/tools/programs/): enrol people into a journey, change or end their follow-up, read the steps they got and their answers, read escalations, and hear about each of these as it happens through one signed webhook. People you reach only inside your own app can be followed too: their steps are handed to your app, and your app reports back.

## Keys and access

The Programs API uses the agent's own API keys, the same ones its OpenAI-compatible API takes. Open the agent → **Publish** → **Channels** → the **Web chat & API** row under **Live** → **API access**. Create a key there if you have none (it is shown once), then scroll to **Programs API**:

- **Endpoint** shows the **Base URL**, `https://<your Studio host>/api/v1/agents/<agentId>`, and a `curl` example.
- **What each key may do** sets, per key: **No access to journeys**, **Read people, steps and escalations** (`journeys:read`), or **Read, enroll and change people** (`journeys:write`, which includes read). A key with no access keeps working on the chat API only.
- **Webhook**, below.

Send the key as a Bearer token:

```bash
curl https://<your Studio host>/api/v1/agents/<agentId>/journeys \
  -H "Authorization: Bearer surg_sk_..."
```

| Status | Means |
|---|---|
| `401` | No key, or not a valid key. |
| `404` | The agent does not exist, or the key belongs to another agent. |
| `403` | The key lacks the scope; grant it under **API access**. |

## Naming a person

In a request body, name a person by **exactly one** of:

| Field | Value |
|---|---|
| `user_id` | The person's id on this agent. |
| `phone` | Their WhatsApp number with country code, e.g. `+40712000103`. |
| `slack` | Their Slack member id, e.g. `U0123ABCD`. |
| `telegram` | Their Telegram chat id (they must have started the bot). |
| `api` | Your own id for someone you reach only through your app, e.g. `ext-42`. |

In a path, use the user id, or `phone:+40…`, `slack:U…`, `telegram:123`, `api:ext-42`.

## Endpoints

All paths are under the Base URL.

| Method and path | Scope | What it does |
|---|---|---|
| `GET /journeys` | read | The agent's journeys, each with its `slug`, `name`, `status`, `timezone` and steps. |
| `GET /enrollments` | read | People enrolled, filtered by `journey` and `status`, paged with `limit` (up to 200) and `cursor`. |
| `POST /enrollments` | write | Enrol a person (below). |
| `GET /enrollments/{person}/{journey}` | read | One person's enrollment in one journey. |
| `PATCH /enrollments/{person}/{journey}` | write | Change it: `status` (`active`, `paused`, `ended`) with `status_reason`, `anchor_date`, `anchor_approximate`, `phase`, `timezone`, `preferred_channel`. |
| `GET /steps` | read | Steps sent, oldest first, filtered by `since`, `journey` and `person`, paged. |
| `GET /escalations` | read | Escalations, filtered by `since` and `state` (`open` or `resolved`), paged. |
| `POST /messages/{message_id}/status` | write | Your app reports a message's `status`: `delivered`, `read` or `failed` (with `error`). Answers `200` with `message_id`, `status` and `tracked`; `409` only in the first minute after delivery, while the platform catches up — retry then. |
| `POST /people/{person}/messages` | write | Your app passes on the person's reply: `text`, optional `in_reply_to` and `form`. |

Paged lists return `{"items": [...], "next_cursor": "..."}`; pass `next_cursor` back as `cursor` until it is `null`. The OpenAPI schema lists these under the tag *journeys public API*.

### Enrolling a person

```bash
curl -X POST https://<your Studio host>/api/v1/agents/<agentId>/enrollments \
  -H "Authorization: Bearer surg_sk_..." -H "Content-Type: application/json" \
  -d '{
    "person": {"phone": "+40712000103"},
    "name": "Ion Pop",
    "journey": "onboarding",
    "anchor_date": "2026-10-20",
    "timezone": "Europe/Bucharest",
    "consent": {"granted": true, "text": "Agreed to follow-up messages on WhatsApp at sign-up"},
    "contacts": [{"person": {"api": "ext-daughter"}, "name": "Ana", "relation": "daughter"}]
  }'
```

- `journey` is the journey's key (its slug), as shown under its name on the Journeys tab.
- `anchor_date` is day 0. A step on day -1 goes out the day before it.
- `consent.granted` must be `true`: enrolling records that **you** collected the person's consent to be contacted, on each handle you give, with your key and `consent.text` as the record.
- A handle the agent does not know yet makes a new person of this agent. Enrolling someone again updates their enrollment and makes it active.
- `contacts` (up to 10) links people who answer for them, as confirmed contacts.
- Everything is checked before anything is written: a refused enrolment (an unknown timezone, a preferred channel they cannot be reached on, a team member as the person) creates no person, contact or consent.

The response is the enrollment: the person with their handles, the journey, `status`, `anchor_date`, `day` (negative before the anchor), `timezone`, `preferred_channel`, `current_step`, `next_send_at`, `last_reply_at` and `enrolled_by` (`api` for an enrolment made through this API).

### A step

Each step sent (one per recipient) reads:

```json
{
  "id": "…", "journey": "onboarding", "step": {"id": "…", "name": "First week check"},
  "person_user_id": "…", "recipient_user_id": "…", "channel": "whatsapp",
  "created_at": "2026-10-27T07:00:12Z",
  "delivery": "delivered", "delivery_error": null, "read_at": "2026-10-27T07:04:40Z",
  "response": "completed", "label": "green", "form": {"rating": "4"},
  "deadline_at": "2026-10-28T07:00:12Z", "escalation": "none", "reason": null,
  "session_id": "…"
}
```

`delivery` is one of `queued`, `accepted`, `delivered`, `failed`, `undelivered`, `skipped`, `canceled`. `response` is one of `not_started`, `awaiting_reply`, `replied`, `in_progress`, `completed`, `declined`, `incomplete`, `no_reply_by_deadline`, `answered_by_other`, `skipped_by_agent`. `label` is the label the agent recorded for the answer.

## Webhook

Under **Web chat & API → API access → Programs API → Webhook**, give an HTTPS **URL** on a public address, tick the **Events** you want (all by default), and **Turn on the webhook**. The **signing secret** (`whsec_…`) is shown **once**, in that response; copy it before you click **I've saved it**. Afterwards you can **Send a test** (a `ping` event), **Rotate secret** (the old one stops signing at once), untick **Send events** to pause, or **Remove** it. **Recent deliveries** lists each post with its status, HTTP answer and tries; a failed one has **Retry now** (except a `message.deliver`, which has already gone to the person another way).

| Event | Sent when |
|---|---|
| `person.enrolled` | Someone enrolled. |
| `person.ended` | Someone finished or left (once per enrollment). |
| `step.sent` | A step was sent (accepted, delivered or read). |
| `step.answered` | A step was answered and closed (completed, declined or answered but not finished), with its `label` and `form`. |
| `escalation.raised` | An escalation was raised. |
| `escalation.resolved` | An escalation was resolved. |
| `message.deliver` | A message to deliver in your app (see [People in your own app](#people-in-your-own-app)). |

Each post is a JSON body:

```json
{"id": "<delivery id>", "type": "step.answered", "created_at": "…", "agent_id": "…",
 "data": {"person": {"user_id": "…", "name": "Ion Pop", "handles": {"whatsapp": "40712000103"}},
          "step": { … }}}
```

`data` carries `person` plus `enrollment`, `step` or `escalation` depending on the event. Events are read from the moment the webhook is created (looking back at most 14 days).

A `2xx` answer means delivered. Anything else is retried after **30 s, 2 min, 10 min, 1 h and 6 h**, then marked failed. Delivery records are kept 30 days.

### Verifying a post

Every post carries:

| Header | Value |
|---|---|
| `X-Surogate-Event` | The event type. |
| `X-Surogate-Delivery` | The delivery id, the same on every retry. |
| `X-Surogate-Timestamp` | Unix seconds when it was signed. |
| `X-Surogate-Signature` | `v1=` followed by the hex HMAC-SHA256 of `"{timestamp}."` + the raw body, keyed with your secret. |

Check the signature on the raw body, refuse timestamps older than five minutes, and ignore an `id` you have already handled:

```python
import hashlib, hmac, time

def verify(secret: str, headers: dict, raw_body: bytes) -> bool:
    timestamp = headers["X-Surogate-Timestamp"]
    if abs(time.time() - int(timestamp)) > 300:
        return False
    expected = "v1=" + hmac.new(
        secret.encode(), f"{timestamp}.".encode() + raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, headers["X-Surogate-Signature"])
```

## People in your own app

A person enrolled with an `api` handle is reached through your app instead of a messaging channel:

1. When the agent writes to them (a step, an alert, a message from the team), your webhook gets a `message.deliver` event whose `data` holds the `text`, the `external_id` (your id), the kind (`step`, `alert`, `message` or `form`) and a `message_id`.
2. Show it in your app, then report what happened: `POST /messages/{message_id}/status` with `delivered`, `read` or `failed`. A failed message moves the step to the person's next channel, if they have one.
3. When they answer, `POST /people/api:<your id>/messages` with their `text` (and `form` answers, if any). It answers the step waiting for them and wakes the agent. The same rules apply as on any other channel: a bare STOP opts them out of messages through your app, and an answer to a question the agent asked is taken as the answer. A message the safety screen refuses is answered `422` with the reason. A reply from someone who would need a plan on a [monetized](/work/monetize/#people-you-bring-in-never-need-a-plan) agent is kept but not answered, and you get `402` with a `code` and the business's `notice` to show them; people you enrolled never need one.

If your webhook stays unreachable after its retries, the message is failed and the step tries the person's other channels. Removing the webhook, switching it off, or unticking `message.deliver` does the same for messages still waiting, so the agent tries the person's other channels. Other events wait until the webhook is on again.

## What's next

- [Programs](/work/tools/programs/) — journeys, steps and the People tab.
- [Team and escalations](/work/tools/programs-team/).

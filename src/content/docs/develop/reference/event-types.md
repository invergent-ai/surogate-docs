---
title: Event types
---

The Sessions UI's EVENTS tab and the `GET /v1/sessions/{id}/events` API both return a stream of typed events. This page lists what you'll see and what each event tells you. The authoritative list is the harness `EventType` enum.

## Conversation

| Type | When | Payload |
|---|---|---|
| `user.message` | Input was added to the session | `content`. Channel messages carry a `source` **object** (`platform`, `chat_id`, `chat_type`, `user_id`, `user_name`, `thread_id`, `ts`) plus a `principal_user_id` / `principal_service_account_id` stamp. Server-generated messages carry `synthetic` instead (e.g. `outcome_continuation`) |
| `llm.request` | One LLM call started — the agent may make many per turn | — |
| `llm.delta` | A streamed token chunk. Very high volume; filter it out when reading a timeline | — |
| `llm.heartbeat` | The upstream went quiet past the heartbeat interval but is still inside the stale-timeout window — the model is reasoning silently, the stream is not dead | — |
| `llm.thinking` | An extracted reasoning block (provider-dependent) — the complete snapshot for the iteration, not a delta | `reasoning` |
| `llm.response` | The model answered. **The user-visible text is `message.content`** — there is no separate final-answer event | `message` (`{role, content, tool_calls?}`), `model`, `input_tokens`, `output_tokens`, `reasoning_tokens`, `cache_read_tokens`, `finish_reason`, `context_window`; `cost_usd` when the serving model has a catalog rate, `cost_unpriced_model` when it does not |
| `ask_user_question.response` | The user answered an `ask_user_question` prompt | `tool_call_id`, `responses` |
| `channel.form` | The agent sent a WhatsApp form with `send_form`. It is delivered to the channel, and it is the record a submitted form's `flow_token` is checked against | `form`, `flow_token`, `interactive` |
| `iteration.summary` | One LLM iteration finished — a one-line imperative recap | — |
| `turn.summary` | The final iteration of a turn finished — recap plus curated artifact list | — |

## Tool execution

| Type | Payload |
|---|---|
| `tool.call` | `tool_call_id`, `name`, `arguments` (path-sanitized — the workspace absolute path is replaced with `__WORKSPACE__`), plus `checkpoint_hash` on file-mutating tools |
| `tool.result` | `tool_call_id`, `name`, `content` (the result body, often JSON-encoded), `elapsed_ms` |

**Tool errors ride in `tool.result`** — there is no `tool.error` event. A failure shows up as a `content` like `{"error": "Tool execution failed: …"}`. A rejection that never reached the tool at all — a governance denial or an allow-list block — carries `elapsed_ms: 0`.

For most debugging, the EVENTS tab's TOOLS sub-view filters these for you. Programmatically there is no server-side filter — pull the log and select on `event.type` yourself (see [Querying via the API](#querying-via-the-api)).

## Skills and plan

| Type | When | Payload |
|---|---|---|
| `skill.invoked` | The harness expanded a `/<skill> …` user message: it loaded the skill server-side and inlined the body before the LLM saw the message. The original text stays in the preceding `user.message` | `skill`, `raw_message`, `staged_at` (workspace path where the skill's supporting files were staged, or `null`); a SkillOpt rollout adds `override_source`, `skillopt_run_id`, `candidate_id`. Emitted at most once per user message — crash-recovery re-expansion does not re-emit |
| `todo.updated` | The agent wrote its plan via the `todo` tool. The full list is written every time, so recovery reads the latest row rather than folding a delta log | `todos` |
| `skill.step` | The agent marked a step of a procedure skill as started, completed or skipped, with `skill_step`. The skill canvas replays a session over the skill's graph from these | `skill`, `step`, `status`, `tool_call_id` |

A skill the SKILLS tab shows as loaded but with no `skill.invoked` was simply never slash-invoked — the model was free to reach for it and didn't.

## Sub-agents, project threads and the board

When a session starts sub-agents with `agent`, their outcomes flow back as events in the parent's log.

| Type | When |
|---|---|
| `delegation.start` | A sub-agent's child session was created and queued | `child_session_id`, `goal`, `depth`, `agent_type` |
| `delegation.complete` / `delegation.failed` | The sub-agent's run ended well, or failed or timed out |
| `delegation.stale` | A foreground sub-agent went quiet past a threshold (once per child) |
| `agent.notification` | A background sub-agent, background command or monitor ended or reported. The session reads it as a notification at its next model request; it wakes a session at rest | `agent_id`, `kind`, `status`, `summary`, `result`, `usage` |
| `worker.spawned` / `worker.complete` / `worker.failed` | A project's thread started, reported a turn, or failed: the coordinator reads each as a notification, the thread's files in a `<files>` block |
| `thread.proposed` | A project's coordinator proposed a thread for the user to start, with `agent` and `propose: true`. The cards are drawn from this event | `proposal_id`, `threads` |
| `coordinator.message` | A project coordinator's follow-up to one of its threads. The thread reads it as a message typed into it, but it is never the user's | `content` |
| `history.redo` | A project thread was told to redo its change to files its landing left out | `files` |
| `history.redo_held` | The wake for a thread's redo was held back, by its user's limit or because ops was unreachable. The thread rests and its next turn redoes the change | `redo` |
| `board.note` | A note passed admission on the writer's session |
| `board.update` | The rendered snapshot or delta that re-enters a reader session's conversation on replay |

See [Coordination](/develop/reference/coordination/) for how the board admits notes.

## Missions and research

Emitted on the coordinator chat session; the mission dashboard polls them.

| Type | When |
|---|---|
| `mission.defined` | A mission was created |
| `mission.evaluation.start` / `mission.evaluation.end` | One mission evaluation pass |
| `mission.continuation` | The mission queued another round |
| `mission.paused` / `mission.resumed` / `mission.cancelled` | Operator-driven mission state changes |
| `mission.refinement_proposed` | The evaluator proposed a new rubric instead of a verdict, and the mission paused to wait for a decision. This event is where `/mission accept` reads the new rubric from. Payload: `mission_id`, `old_rubric`, `proposed_rubric`, `evidence`, `held_verdict`, `explanation` |
| `mission.amended` | The operator accepted the proposed rubric with `/mission accept`. Payload: `mission_id`, `old_rubric`, `new_rubric`, `evidence`, `typed_at` |

## Governance

| Type | When |
|---|---|
| `policy.denied` | A tool call was blocked by the governance gate. Payload: `tool`, `reason`, `timestamp` |
| `policy.allowed` | Two shapes. Gate pass-through, emitted only when the deployment enables `governance.log_allowed` (off by default; doubles event volume): `tool`, `check: "governance_gate"`, `timestamp`. Approved retry of a gated call: `tool_name`, `reason: "human approval"`, `tool_call_id` |
| `disclosure.presented` | A messaging channel (Slack / Telegram / WhatsApp) posted the AI disclosure as the first message of a new conversation. Payload: `level`, `channel`, `delivery: "channel_message"` |
| `disclosure.confirmed` | A web user accepted the disclosure banner. Payload: `level`, `source: "web_banner"` |
| `security.injection_blocked` | The prompt-injection detector refused a user message sent through the sessions API (web chat, API channel, and comment mentions in office documents, which go the same way); `/code` commands are not screened. The request gets a 422 and no `user.message` is recorded, so this event is what shows the block in the timeline. Payload: `source` (`web_channel` or `api_channel`), `explanation`, `threat_level`, `confidence`, `injection_type`, `matched_patterns` (up to 10), `content_preview` (first 2000 characters) |

A denial of a tool named in the policy's `require_approval` list is **overridable**: alongside `policy.denied` it emits `inbox.governance_gate` and hands the model `policy_blocked_overridable` rather than a hard error, so the call can be retried after a human decides.

The two `disclosure.*` events are the Art. 50 compliance evidence trail — see [Governance & AI disclosure](/work/workflow/governance/).

## Saga (multi-step rollback)

When the agent's CONFIG has Saga enabled:

| Type | When |
|---|---|
| `saga.start` | Saga activated at session start. Payload: `saga_id`, `session_id`, `timestamp` |
| `saga.step_begin` / `saga.step_committed` / `saga.step_failed` | Per-step tracking. Payload: `saga_id`, `step_id`, `tool_name`, `state`, `timestamp`, plus `tool_call_id`, `arguments`, `compensation_tool`, `compensation_args`, `checkpoint_hash`, `result`, `error` when set |
| `saga.compensate` | A rollback fired. Payload: `saga_id`, `steps_rolled_back`, `reason`, `timestamp`, and `failed_steps` when present — **a non-empty `failed_steps` is the escalation signal**: a compensation step itself failed and an operator must intervene |
| `saga.complete` | Saga finished. Payload: `saga_id`, `status`, `steps_executed`, `timestamp` |

There is no `saga.escalated` event. Escalation is a saga *state*, surfaced through `failed_steps` on `saga.compensate`.

## Experts and feedback

| Type | When | Payload |
|---|---|---|
| `expert.delegation` | The base LLM called `consult_expert` | `expert`, `task` (truncated to 500 chars), `tools`, `max_iterations` |
| `expert.result` | The expert finished successfully | `expert`, `success` (always `true`), `iterations_used`, `content` (the deliverable) |
| `expert.failure` | The expert errored or exhausted its iteration budget | `expert`, `success` (always `false`), `iterations_used`, `error` |
| `expert.endorse` / `expert.override` | A **user or judge** rated an `expert.result` thumbs-up / thumbs-down through the feedback endpoint — not a decision the base LLM makes | `expert`, `target_event_id`, `rating` (`up` / `down`), `source` (`user` / `judge`), `rated_by_user_id` or `rated_by_service_account_id`, plus `reason`, `rationale`, `score`, `criteria` when supplied |
| `user.feedback` | The same thumbs, but on a regular `llm.response`. Consumed by training-data selection to filter rated trajectories | Same payload, minus `expert` |

## Outcomes (`/goal`)

| Type | When | Payload |
|---|---|---|
| `user.define_outcome` | A goal was set **through the API** — `POST /v1/sessions/{id}/events`. The `/goal` command does not emit this | `description`, `rubric` (`{type, content}`), `max_iterations` (clamped to 20), `outcome_id`, `processed_at` |
| `outcome.defined` | The goal was saved on the session by `/goal`. The API path emits `user.define_outcome` instead | `outcome_id`, `description`, `rubric`, `max_iterations` |
| `span.outcome_evaluation_start` / `span.outcome_evaluation_ongoing` | The evaluator span opened around one turn | `outcome_id`, `iteration`; `start` also carries `response_event_id` |
| `span.outcome_evaluation_end` | The evaluator returned a verdict | `outcome_id`, `outcome_evaluation_start_id`, `iteration`, `result` (`satisfied`, `needs_revision`, `blocked`, `failed`, `max_iterations_reached`, or `paused` when the evaluator returned unparseable output too many times in a row), `explanation`, `feedback`, `parse_failed` |
| `outcome.continuation` | A continuation was queued. The synthetic `user.message` that follows carries `synthetic: "outcome_continuation"` | `outcome_id`, `iteration`, `status_event_id` |
| `outcome.paused` | The goal was paused by `/goal pause` — the only thing that emits this | `outcome_id`, `reason` (always `user-paused`) |
| `outcome.cleared` | The goal was removed by `/goal clear` | `outcome_id` (`null` when nothing was active) |

## Inbox

The agent raised something to the user:

| Type | What it surfaces |
|---|---|
| `inbox.input_required` | An `ask_user_question` prompt |
| `inbox.action_required` | An external action needed (browser login, MFA, etc.) |
| `inbox.task_complete` | An informational completion |
| `inbox.governance_gate` | An overridable policy denial awaiting a human decision. Payload: `tool_name`, `tool_call_id`, `arguments_excerpt`, `deny_reason`, `policy_id`. Answer with `POST /v1/inbox/{item_id}/respond` and `{"decision": "approve"}` or `{"decision": "reject"}`; approving mints an approval grant keyed to that exact call, which the retry consumes |
| `inbox.progress_checkin` | A long-running-session status update |

## Browser and coding-agent runs

| Type | When |
|---|---|
| `browser.provisioned` / `browser.destroyed` | An agent browser was allocated or torn down |
| `browser.unavailable` | A browser tool ran on a local-folder session's computer that has no supported browser |
| `browser.control_granted` / `browser.control_returned` | A user took over the live browser view, then handed control back |
| `code.run_started` | A `/code` run began. Carries the source user-event id for crash-recovery idempotency |
| `code.run_progress` | Coalesced streamed output from the coding agent. Web UI only — never delivered to channels |
| `code.run_channel_update` | A throttled "still working" heartbeat, emitted only for channel sessions so a Slack or Telegram user isn't left silent for the minutes a run takes |
| `code.run_result` | The final message plus token usage |

Credentials never appear in any `code.*` payload.

## Local computer and documents

Emitted on sessions that work in a folder on a user's computer, and on sessions with an open document editor.

| Type | When | Payload |
|---|---|---|
| `device.waiting` | The session's work is waiting on its computer: it is offline, or it is making the thread's first copy of the folder | `device_id`, `device_name`, `reason` (`offline` or `copying`), plus `folder` for `copying` |
| `device.resumed` | The wait ended | `device_id` |
| `office.saved` | A save from the document editor that had been waiting for its computer landed | `path` |
| `office.save_waiting` | A save waits for the computer its file is on. Said when the wait starts and again if its reason changes | `path`, `computer`, `reason` (`offline`, or `waiting` for the computer's user to allow it) |
| `office.save_failed` | A save from the document editor failed | `path`, plus `status` or `attempts`; or `reason: "declined"` and `computer` |
| `office.conflict` | The file changed outside the editor, so the save landed as a sibling copy and the editors were told to reload | `path`, `conflict_path` |

## Lifecycle

| Type | When |
|---|---|
| `harness.wake` | A worker acquired the session's lease and began processing — the first event of every turn. Payload: `worker_id`, `cursor`. The background memory/skill review re-uses this type with `review_memory` / `review_skills` instead of `cursor` |
| `session.pause` / `session.resume` / `session.complete` / `session.fail` | Session-level transitions |
| `session.stopped` | A channel `/stop` aborted the running turn out-of-band. Unlike `pause`, the session stays `active` |
| `session.model_escalated` | The model was swapped mid-turn to get past a provider behaviour the current model could not (today: repeated empty completions), so the tier change is visible in cost attribution. Payload: `reason`, `model` (the model escalated to) |
| `session.title_updated` | Auto-title landed on the session outside the chat-turn flow, so SSE subscribers can patch it in place |
| `harness.crash` | The runtime raised and the turn died |
| `harness.recovered` | The orphan sweeper found a session abandoned by a dead worker (hard-killed — SIGKILL, OOM, pod eviction). No exception was raised; the event documents the gap and triggers the retry path on the next wake |
| `context.compact` | The session's context window was compressed automatically |
| `artifact.created` | A `create_artifact` call produced an inline chat artifact. The event carries metadata only; fetch the body from the artifacts API |
| `loop.result` | A scheduled loop run's final answer, delivered inline on the parent session — see [Background jobs](/develop/reference/background-jobs/) |

## Reserved names

These are declared in the `EventType` enum but have **no producer in the runtime today** (some are still carried in client-side type unions). Do not build on them.

`session.start`, `session.reset`, `memory.update`, `artifact.updated`, `ambient.tick`, `ambient.post`, `sandbox.provision`, `sandbox.execute`, `sandbox.result`, `sandbox.destroy`, `research.dispatched`, `research.merged`, `research.pruned`, `research.report`.

## Querying via the API

```bash
# Stream live (SSE) — this is what /events is; it takes only `after`
GET /v1/sessions/{id}/events?after=<last_id>

# Read back as JSON (user JWT only — there is no /v1/api/ alias)
GET /v1/sessions/{id}/events/poll?after=<last_id>&limit=50
```

There is **no server-side type filter** — `?type=` is silently ignored on both routes. Pull the page and filter client-side on `event.type`. Service-account tokens reach the SSE route under `/v1/api/sessions/{id}/events` but cannot reach `/poll`.

See the API reference for full schemas. For Slack and Telegram channel sessions, the same events stream is available — channel adapters just translate the user-visible portion into the channel's native format.

## Stability

Event type names and their documented payload keys are a stable contract. **Adding new keys is safe**; renaming or removing requires a deprecation cycle. If you're querying programmatically, prefer reading specific keys (`event.data.tool`) over depending on the full payload shape.

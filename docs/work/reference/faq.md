---
title: Troubleshooting & known issues
sidebar_position: 2
---

# Troubleshooting & known issues

Known platform bugs and non-obvious failure modes. Pure UI-orientation issues (where things are, what buttons do) are covered in the relevant chapters.

## Agents

**Stuck on `deploying` past 90s.** Check the agent's Overview page for the most recent error message. Force-restart via STOP → START.

**Develop mode shows "No agents" but they exist.** Known cache bug. Reload the page; Work mode is unaffected.

## Sessions

**Agent doesn't respond.** Check in order: agent is `running`, you haven't hit a rate limit (Settings → Usage), no `policy.denied` / `harness.crash` events in EVENTS, prompt isn't being blocked by the prompt-injection guard.

**Response was wrong.** Thumb-down the turn, then in EVENTS check which tool calls fired (or didn't fire when they should have) and SKILLS to see which skills loaded. Most "wrong answer" issues are missing KB content or a skill that didn't trigger.

**Message rejected with `delimiter_attack`.** The prompt-injection guard flagged triple-backtick fences. Use 4-space-indented code blocks instead.

## Skills

**Published a skill, agent isn't using it.** Skill changes apply to **new sessions only**. Start a new chat. If still not firing, the `trigger` keywords likely don't match how users actually phrase the request — make them more specific.

**REPOSITORY tab shows 0 files after publish.** Known cache issue — navigate away and back. The files exist.

## Knowledge bases

**COMPILE fails with `task failed`.** Usually transient (curator LLM rate limit). Retry. If it persists: reduce source size (split large PDFs), verify the source is well-formed UTF-8, and check OVERVIEW → RECENT COMPILES for the one-line reason.

**CSV upload shows 0 samples.** Known issue. Workaround: convert to a markdown-formatted summary and re-upload.

**Agent doesn't use the KB.** Check the KB status is `active` (compiled successfully). In EVENTS, check whether the LLM called `kb_search` — if not, it didn't think the KB was relevant. Adjusting SOUL.md to mention the KB explicitly helps.

## Channels

**Slack bot is silent.** Verify bot scopes (at minimum `app_mentions:read`, `chat:write`, `im:read`, `im:write`, `channels:history`, `groups:history`, `files:read`). Re-install the app after adding scopes. Confirm Socket Mode is on and the App-Level Token has `connections:write`.

**Telegram bot replies once then stops.** Another instance is consuming Telegram updates. Stop the other instance — Telegram only delivers each update once.

**Website widget says "origin not allowed".** Page URL isn't in the Allowed Origins list. Add the exact URL → SAVE. No wildcards.

**COPY button on the publishable key is disabled.** SAVE CHANNELS first — the key isn't deployed until then.

## Copilot

**401 "Invalid base LLM token".** Admin-side config issue — the platform's default LLM credentials aren't provisioned for your tenant.

**Copilot loops on `read_resource`.** Known bug — the tool is in the Copilot's allowlist but unimplemented. Phrase the question to avoid enumeration, e.g. "What KBs does `customer-support-bot` have?" instead of "list my KBs".

## Billing

**Upgraded but limits didn't increase.** Stripe webhooks usually deliver instantly; can lag 30-60s. Refresh the Billing tab.

**Top-up credits don't show in Usage.** They show on a separate line — they're consumed before plan tokens.

**BYO LLM enabled but agent still uses Surogate's model.** Per-agent CONFIG → Model overrides the global toggle. Update each agent.

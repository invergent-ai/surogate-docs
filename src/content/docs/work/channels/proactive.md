---
title: Proactive engagement
---

Let an agent do more than answer when spoken to — build context from everything in a channel and, when it is confident it will help, reach out on its own.

These behaviors are grouped under SUROGATE MATE and are configured per channel. Today they apply to [Slack](/work/channels/slack): open the agent's Slack channel and use the SUROGATE MATE section. The toggles there set the agent-level default, which applies to every Slack channel the agent is in; individual channels can override the default.

## The settings

| Setting | UI label | What it does |
|---|---|---|
| `follow_enabled` | FOLLOW THE CHANNEL | Build durable context from *all* channel activity, not just messages that @mention the agent. |
| `ambient_enabled` | AMBIENT MODE | Let the agent take initiative and post on its own when it is confident it is worth it. |
| `digest_enabled` | — | Stores a preference (with an optional schedule) for periodic digests. See the note below. |

All three default to off. Turning them on is a per-channel choice you make in the SUROGATE MATE settings.

## Follow the channel

With FOLLOW on, the agent ingests the channel's activity — not only the messages that mention it — and folds it into durable context. The practical effect is continuity: because the agent has been "listening", anyone can pick up a thread and the agent already has the background, instead of only knowing the messages addressed directly to it.

Follow controls context-building only. It does not, on its own, make the agent speak up unprompted — that is what Ambient mode adds.

## Ambient mode

With AMBIENT on, the agent periodically reviews a followed channel and decides whether to post proactively — for example nudging on a quiet thread, following up on a delegated task, or flagging something relevant. It is designed to stay quiet unless it is confident, so it is not chatty by default.

Each review is gated before anything is posted. A message only goes out when all of these hold:

| Guard | Default | Meaning |
|---|---|---|
| Confidence | `0.7` | The agent's own confidence that a post is worth it must clear this threshold. |
| Posts per day | `10` | A per-channel cap on proactive posts in a day. |
| Minimum gap | `600 s` | Minimum time between two proactive posts in the same channel. |
| Review cadence | `1800 s` | How often the agent reviews the channel for something worth posting. |
| Quiet-thread window | `120 min` | How long a thread is left alone before it counts as "quiet". |

Confidence is necessary but never sufficient: even a confident decision is dropped if the rate limits would be exceeded or the proposed message is empty. Ambient posts go out through a dedicated, gated path rather than the agent's normal reply flow.

## Digests

The `digest_enabled` setting (and an optional `digest_schedule`) is present in the Surogate Mate settings and stored per channel, but it is not yet surfaced as a toggle in the Studio channel settings, and the runtime does not currently act on it. Treat it as reserved: turning it on records the preference but does not, on its own, produce periodic digests today.

## Enabling

1. Connect [Slack](/work/channels/slack) for the agent and open its channel settings.
2. In SUROGATE MATE, turn on FOLLOW THE CHANNEL so the agent builds context from the channel.
3. Turn on AMBIENT MODE to let it post proactively. The guard values above apply per channel; the section's toggles set the agent-wide default, which a specific channel can override.

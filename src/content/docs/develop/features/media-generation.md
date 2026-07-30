---
title: Media generation
---

Agents can generate images and videos through two built-in tools:

| Tool | What it does |
|---|---|
| `generate_image` | Image from a text prompt, optionally image-to-image. Saved to the session workspace and shown inline. |
| `generate_video` | Video from a text prompt, optionally first-frame image-to-video. Blocks until rendered (polling, ~10-minute cap), saved to the workspace. |

## Wiring a model

Each tool needs a model for its role, set under **Configure → Model**:

- **Image model** / **Video model** — pick your own (BYO), or leave **Platform default** to use the platform preset.
- With neither a per-agent pick nor a platform preset, the matching tool is **dropped from the agent's toolset entirely** — the LLM never sees an unusable tool.

A wired image or video model is also the prerequisite for selling **media credits** on the agent's offers — see [Monetize](/work/monetize#browsing-time-and-media-credits).

## How it's billed

Media generation has its own prepaid wallet — **media credits**, denominated in dollars of provider spend — so a video can never silently drain your chat-token grant, and an empty media wallet never stops the agent from chatting.

- **Images** (platform model): a flat few cents per image (default $0.04), checked and debited on generation. A failed upstream request debits nothing.
- **Videos** (platform model): submit pre-checks about $1 of headroom; the completed job debits its actual reported provider cost, exactly once.
- **BYO image/video models are not metered by Surogate** — you pay your provider directly.

Your plan grants media credits monthly ($1 on Free up to $25 on Max — roughly 25 images or 2 short videos per dollar), and you can top up under **Settings → Billing** (Media chips, $2.00 per $1 of generation). Balances show as the **Media** meter under **Settings → Usage**.

On monetized agents that sell media credits, each buyer's generation is additionally metered against **their** purchased credits — held before generating, settled at the actual price, released on failure. See [Monetize](/work/monetize#browsing-time-and-media-credits).

## Troubleshooting

| Symptom | Meaning |
|---|---|
| The agent says it can't generate images/videos and the tool is absent | No model is wired for that role — pick one under Configure → Model, or ask the platform operator about presets |
| `media_budget_exhausted` | The **project's** media wallet is empty — top up under Settings → Billing or wait for the monthly reset; nothing was generated or charged |
| `media_credits_exhausted` | The **buyer's** media credits are spent — the agent shares their buy link; nothing was generated or charged |
| `media budget check unavailable` | The metering plane was unreachable — the tool fails closed; try again shortly, nothing was charged |

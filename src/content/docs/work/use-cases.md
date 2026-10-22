---
title: Use cases
---

Five end-to-end walk-throughs you can adapt for your own work. Each one combines several Work-mode features.

For more complex multi-step recipes (fine-tune an expert, build an MCP server, A/B evaluations), switch to **Develop mode**.

---

## 1. Deploy a customer-support bot in 10 minutes

**What you'll do**: stand up an agent that answers customer questions from your product docs, then attach it to your website.

**You'll need**: your product docs as markdown / PDF files (5-20 docs is plenty to start).

### Steps

**1. Build a knowledge base.**

- Library → Knowledge Bases → **NEW KNOWLEDGE BASE**.
- Name `acme-product`, brief description, leave curator model as default.
- SOURCES → ADD SOURCE → upload each markdown / PDF, one at a time.
- COMPILE. Wait 30s–3min. Status: `active`.
- Verify in the WIKI tab — search a typical question, confirm relevant content surfaces.

**2. Create the agent.**

- Templates → **Start from scratch** → **DEPLOY NEW AGENT** dialog.
- Display name: `Acme support bot`. Slug: `acme-support-bot`. Description: "Support agent grounded in product docs."
- Click CREATE AGENT. Status moves `deploying` → `running` in ~30s.

**3. Attach the KB.**

- Open the agent → **Configure** in the left nav → the **Knowledge Bases** tab → **+ ATTACH KNOWLEDGE BASE** → pick `acme-product` → confirm.

**4. Test it.**

- Click **New chat** in the agent's left nav (between Publish and Inbox).
- Ask 5 representative questions: pricing, features, "how do I…?", troubleshooting, refund policy.
- Open the session afterwards from **Sessions** in the WORK sidebar — confirm the agent called the KB tools (`kb_list_pages` / `kb_read_page`) and grounded its answers.

**5. Customise the persona.**

- Configure → **Identity** tab → edit the DESCRIPTION (short summary) and the **SOUL.md** textarea (full persona). Replace the default with something like:

```markdown
# Acme Support Agent

You are the Acme Corp customer support assistant. Speak as "we" when
referring to Acme. Be warm, concise, technically literate.

When the knowledge base doesn't have an answer, say:
"I don't have that information. Let me get a human on this." Then
recommend the user open a ticket via the `escalate` skill.

Never disclose internal ticket IDs. Never make legally binding statements.
```

- SAVE.

**6. Publish to your website.**

- Publish → the **Channels** tab → toggle **Website** ON.
- Add your domain to Allowed Origins (e.g. `https://acme.com`, `https://www.acme.com`).
- SAVE.
- COPY the publishable key. Click **Embed code** to reveal the script tag.
- Paste the script tag into your website's HTML before `</body>`.

Your support bot is live. Visitors hit a chat bubble in the bottom-right. The bot answers from your KB.

### Follow-up

- Review sessions daily for the first week. Thumb-down anything bad.
- For bad sessions, check which skill should have fired but didn't — write or fix one.
- Add new KB sources as your product evolves; click COMPILE to refresh.

---

## 2. Add Slack so your team can chat with the same agent

**You'll need**: ability to create a Slack app in your workspace.

### Steps

**1. Create the Slack app.**

- [api.slack.com/apps](https://api.slack.com/apps) → Create New App → From scratch → name it (e.g. `acme-support`) → pick your workspace.
- Bot Scopes (OAuth & Permissions): `chat:write`, `app_mentions:read`, `im:read`, `im:write`, `channels:history`, `groups:history`, `files:read`, `users:read`.
- Event Subscriptions → Enable → paste the Request URLs Surogate shows you (see [Slack](/work/channels/slack/)).
- Basic Information → copy the App ID and Signing Secret.
- Install to workspace → copy Bot User OAuth Token `xoxb-…`.

**2. Configure in Surogate.**

- Open `acme-support-bot` → Publish → the **Channels** tab → toggle **Slack** ON.
- Paste App ID, Signing Secret and Bot Token.
- Defaults are fine for most: Require @mention ON, Reply in Thread ON.
- SAVE.

**3. Verify.**

- In Slack, DM the bot. Say *"What plans do we offer?"* — it should respond using the same KB as the web version.
- Add the bot to a channel: `/invite @acme-support`. @mention it: `@acme-support refund policy?`. It replies in the thread.

**4. Link Slack identities to Surogate users (optional).**

- If you want the same person on Web and Slack to share sessions, have them sign in to `acme-support-bot.cloud.surogate.ai` once. The bot DMs them a pairing link the first time they message it on Slack.

### Follow-up

- Watch the Sessions list — Slack-channel sessions show up alongside Web-channel sessions.
- Set up `Free Response Channels` if you want the bot to answer everything in a dedicated `#acme-help` channel without @mention.

---

## 3. Triage bad sessions

**Goal**: find what's broken about your agent and fix it in batches.

### Steps

**1. Mark a week's worth of traffic.**

- Each morning, open Sessions → filter by your agent.
- Skim the THREAD of each session. Thumb-down obviously bad answers (wrong, off-tone, hallucinated). Thumb-up clearly good ones.
- It's OK to mark only a sample — every ~5 sessions is enough to spot patterns.

**2. After a week, filter to thumb-down sessions.**

- Sessions → filter chip **👎**.
- Open each session and look for the failure mode:
  - **The agent didn't search the KB**: it answered from training data instead of looking up the fact. Likely a skill or KB attachment problem.
  - **The agent searched the KB but the KB returned junk**: source quality issue. Update or refine the KB content.
  - **The agent searched the right thing but ignored the result**: persona may be overriding KB content. Tighten the description.
  - **The agent used a tool that did the wrong thing**: tool-allowlist issue or skill missing.
  - **The agent crashed or got into a loop**: runtime issue — escalate to admin.

**3. Bucket the failures**.

By cause: "missing facts," "wrong tone," "wrong tool," "wrong workflow." Each bucket has a different fix.

**4. Apply fixes in batches.**

- "Missing facts" → add KB sources, recompile.
- "Wrong tone" → edit the agent's description on the Configure page.
- "Wrong workflow" → write a skill (or update an existing one).
- "Wrong tool" → detach problem skills/MCP servers on the Configure page.

**5. Verify**.

- Start a fresh session and re-ask the questions that produced the worst thumb-downs. An existing session keeps the config it started with, so it will not show the change.
- Compare against the old session side by side — both stay in the Sessions list.
- For more than a handful of cases, score them as a batch instead: see the follow-up below.

### Follow-up

- Build an evaluation set from your worst sessions (Develop mode → Datasets → "From conversations" → filter by 👎).
- Use that set to test every future change before rolling out.

---

## 4. Build a product-knowledge base from internal wiki + tickets

**Goal**: a KB that combines your product wiki (Confluence / Notion / GitHub markdown) with your support ticket history.

### Steps

**1. Gather the content.**

- Export product wiki pages as markdown (one per topic).
- Export the last 6 months of resolved support tickets as a CSV with columns: `subject`, `body`, `resolution`, `category`.
- Filter to tickets with high-quality resolutions (excludes "see above," "fixed it," noise).

**2. Create the KB.**

- Library → Knowledge Bases → NEW KNOWLEDGE BASE → name `acme-support-corpus`.
- Default curator model is fine for most cases. For very technical content (legal, medical), pick a smarter curator at creation — it's locked after.

**3. Upload sources.**

- SOURCES → ADD SOURCE → upload markdown wiki pages one at a time.
- Then upload the tickets CSV.
- COMPILE. Wait — large corpuses can take 5+ minutes per source.

**4. Verify the wiki.**

- Open the KB → **Wiki** tab → search a real customer question. Confirm:
  - Wiki page surfaces if the answer is in the docs
  - Ticket resolution surfaces if there's a relevant past case
  - Cross-source synthesis page combines both

**5. Attach to your support bot.**

- Open `acme-support-bot` → Configure → **Knowledge Bases** tab → + ATTACH KNOWLEDGE BASE → `acme-support-corpus`.

### Follow-up

- Refresh the ticket CSV monthly. Delete the old source, upload the new one, COMPILE.
- When S3/GitHub/Notion source types ship, switch to continuous sync.

---

## 5. Use the Copilot to do platform admin

**Goal**: get familiar with the Copilot for the daily one-off questions that don't deserve a full UI tour.

### Examples to try

Press **⌘+/** anywhere in `ops.surogate.ai` and ask:

| Question | What the Copilot does |
|---|---|
| *"What agents do I have, and how many sessions did each have yesterday?"* | Calls `list_agents` and `recent_failures`, summarises |
| *"Show me my customer-support-bot's attached skills and KBs."* | Calls `get_agent` |
| *"Find sessions where the agent thumb-downed in the last 7 days."* | Filters the sessions list, presents links |
| *"Create a skill called `weekly-summary` that produces 5-bullet summaries."* | Generates the skill content, calls `create_skill`, returns the new skill ID |
| *"Attach `acme-product` KB to `acme-support-bot`."* | Calls `attach_kb_to_agent` |
| *"Scale `acme-support-bot` to 3 replicas."* | Calls `clarify` first (confirmation card), then `scale_agent` |
| *"Delete the `test-summarizer-bot` agent."* | Calls `clarify` (re-quotes the resource ID), then `delete_agent` |

### Behaviours to expect

- **Confirmation cards** before destructive ops or anything that costs money. Click Yes or No.
- **Links to in-app pages** in responses — clicking jumps you to that resource.
- **Errors are returned as text** ("Couldn't find a knowledge base named X") rather than the Copilot retrying blindly.

### Behaviours to avoid

- Don't expect the Copilot to browse the web. By design it's read-only Q&A over your platform; if you ask it to research something external, it'll politely refuse.
- Don't expect it to know across orgs. It operates inside your current project.

---

## Where to go from here

You've covered everything an operator needs day-to-day. If you want to:

- **Build agents from scratch, attach custom tools, write skills in code** → switch to **Develop mode** (top-right pill in the navbar).
- **Train a fine-tuned expert from your traffic** → Develop mode → [Skills & Experts](/develop/features/skills-and-experts) and [Training](/develop/features/training).
- **Run an A/B evaluation of two versions of your bot** → Develop mode → [Evaluations](/develop/features/evaluations).
- **Integrate the API channel into your data pipelines** → Develop mode → [Use cases](/develop/use-cases) → "API channel pipeline."

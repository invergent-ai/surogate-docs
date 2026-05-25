---
title: Quickstart
sidebar_position: 2
---

# Quickstart

Deploy a custom agent with attached skill + KB + scoped tool envelope, then call it from a Python script. **~15 minutes.**

This walks the full build → expose surface — UI for design, REST API for integration. If you only need the operator workflow, [Work mode → Quickstart](/work/quickstart) is faster.

## 1. Write a skill

**Library → Skills & Tools → NEW SKILL**:

```markdown
---
name: triage-incident
description: Classify an incident report and produce a structured triage card
trigger: triage, classify incident, alert, priority, severity
tools: [read_file, web_search]
---

When given an incident report, output ONLY a JSON object with:
- severity: "P1" | "P2" | "P3" | "P4"
- category: short string (e.g. "auth", "database", "ml-inference")
- summary: one sentence, under 80 chars
- suggested_owner: team name or "unassigned"
- next_step: one short imperative sentence

Examples:
Input: "API responses timing out for 12 customers, started 5min ago"
Output:
{"severity": "P1", "category": "api-availability",
 "summary": "API timeouts affecting 12 customers since 5min ago",
 "suggested_owner": "platform-oncall", "next_step": "Check API gateway health"}

No prose outside the JSON.
```

Click **SAVE** → **PUBLISH** as `v0.1.0`.

The skill is now versioned in the Hub at `p-{project}/skill-triage-incident` with `v0.1.0` as its first tag.

## 2. Compile a knowledge base

**Library → Knowledge Bases → NEW KNOWLEDGE BASE**:

- Name: `incident-runbooks`
- Curator model: default
- **CREATE**

Add sources (`SOURCES → ADD SOURCE`): drop in 3–10 markdown files that describe your incident-response procedures.

Click **COMPILE**. Wait until status flips to `active`. Search the **WIKI** tab for a typical question to confirm the curator extracted what you need.

## 3. Deploy an agent

In Develop mode, open **Agents** in the left nav → **DEPLOY AGENT** at the top of the list. Fill the dialog:

- **Display Name** — `Incident Bot`
- **Slug** — `incident-bot` (becomes `incident-bot.cloud.surogate.ai`)
- **Description** — `Triage incoming incidents, ground answers in runbooks`
- **Model** — leave as `Surogate`

Click **CREATE AGENT**. Wait for status `running`.

(From Work mode the equivalent path is Templates → **Start from scratch** → same dialog.)

## 4. Configure it

In Develop mode, with the agent selected, open the **KNOWLEDGE & TOOLS** tab in the detail panel:

- **+ ATTACH SKILL** → `triage-incident@v0.1.0`
- **+ ATTACH KNOWLEDGE BASE** → `incident-runbooks`

Then open the **CONFIG** tab → **Tool Access** section:

- **Allowed**: `kb_search`, `kb_query`, `read_file`, `web_search`, `create_artifact`
- **Denied**: `terminal`, `execute_code`, `write_file`, `patch` (this agent shouldn't be running code)

Open **CONFIG** → **SOUL.md**:

```markdown
# Incident Triage Bot

You are an incident-triage assistant for the platform team. You return
structured triage cards via the `triage-incident` skill, and ground
recommendations in the `incident-runbooks` knowledge base.

When users describe an incident, ALWAYS:
1. Output a triage card (via `triage-incident`)
2. Search `incident-runbooks` for the closest matching runbook
3. Include a one-line link to the runbook in your response

Never invent an oncall name. If you don't know who owns it, write
"suggested_owner": "unassigned".
```

**SAVE CONFIG**. New sessions pick up the changes.

## 5. Smoke-test from the UI

Click **CHAT** → paste an incident description:

> *"PagerDuty firing — 'auth-service' returning 502 to 30% of requests for the last 10 minutes."*

Confirm in the EVENTS tab:

- The skill triggered (you'll see `skill.invoked` for `triage-incident`)
- `kb_search` fired against `incident-runbooks`
- The response is structured JSON + a runbook reference

If not, check SKILLS tab — did the skill load? Are the triggers specific enough? Iterate.

## 6. Get a service-account token

For programmatic access, ask your admin for a service-account token via:

```bash
curl -X POST https://ops.surogate.ai/v1/admin/service-accounts \
  -H "Authorization: Bearer $ADMIN_JWT" \
  -d '{"org_id": "<your-org-uuid>", "name": "incident-pipeline"}'
```

Returns the token **once** as `surg_sk_...`. Store it; you can't retrieve it again. Tokens are valid only on `/v1/api/*` routes; no SSE, no inbox.

## 7. Call the agent from Python

```python
import os, time, requests, json

TOKEN = os.environ["SUROGATE_SA_TOKEN"]
BASE = "https://ops.surogate.ai/v1/api"

def triage(incident_text: str) -> dict:
    # Submit the prompt
    r = requests.post(
        f"{BASE}/prompts",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={
            "agent_slug": "incident-bot",
            "prompt": f"Triage: {incident_text}",
            "context": {"source": "pagerduty-webhook"},
        },
    )
    session_id = r.json()["session_id"]

    # Poll for completion
    while True:
        s = requests.get(
            f"{BASE}/sessions/{session_id}",
            headers={"Authorization": f"Bearer {TOKEN}"},
        ).json()
        if s["status"] in ("completed", "failed"):
            break
        time.sleep(3)

    # Extract the final response (the skill returns a JSON card)
    events = requests.get(
        f"{BASE}/sessions/{session_id}/events",
        headers={"Authorization": f"Bearer {TOKEN}"},
    ).json()
    final = next(e for e in events if e["type"] == "assistant.final")
    return json.loads(final["data"]["content"])


card = triage("API responses timing out for 12 customers since 5min ago")
print(card)
# {'severity': 'P1', 'category': 'api-availability', ...}
```

Add an `Idempotency-Key` header to the `POST /prompts` call to dedupe webhook retries within 24h.

## What you've built

- A **versioned skill** in the Hub (rollback-able)
- A **compiled KB** the agent searches at runtime
- A **scoped agent** with a tight tool envelope and explicit persona
- A **programmatic interface** via service-account token + REST

That's a real production-shape integration. From here you can:

- Pull thumb-downed sessions into a [dataset](./features/datasets.md) and [evaluate](./features/evaluations.md) future agent versions
- Promote the skill to an [expert](./features/skills-and-experts.md) once you have ≥100 successful trajectories
- Add an MCP server to talk to PagerDuty, Linear, your data warehouse, etc. — see [MCP & Vault](./features/mcp-and-vault.md)
- See [Use cases](./use-cases.md) for richer recipes (A/B evaluation, synthetic data, Saga rollback flows)

---
title: Use cases
---

Seven multi-step end-to-end recipes for builders. Each one combines several Develop-mode features.

For simpler operator-facing recipes, see [Work mode → Use cases](/work/use-cases).

---

## 1. Fine-tune an expert from your traffic

**Goal**: a regular skill works OK but the base LLM gets it wrong N% of the time. You want to replace the skill with a fine-tuned expert.

**Prerequisites**:
- ≥100 successful sessions matching the skill's trigger in the last 90 days
- A way to host the fine-tuned model (vLLM endpoint, OpenAI fine-tune, Anthropic, OpenRouter — anything OpenAI-compatible)

### Steps

**1. Verify you have signal**.

In Sessions, filter by:
- Quality flag: 👍
- Time range: last 90 days
- Skill: `<your-skill>` (the SKILLS tab on each session must show your skill triggered)

You need a corpus of clean trajectories. Aim for ≥100 sessions for a viable training run.

**2. Convert your skill to an expert (draft state)**.

Library → Skills & Tools → your skill → EDIT. Add to the frontmatter:

```yaml
type: expert
model: qwen2.5-coder-7b
endpoint: ""                # leave blank until trained
trigger: SQL queries, ...
tools: [terminal, read_file]
max_iterations: 10
expert_status: draft
```

PUBLISH a new version (e.g. `v0.1.0`).

**3. Collect training data**.

```bash
curl -X POST http://ops.surogate.ai/v1/skills/<name>/collect \
  -H "Authorization: Bearer $TOKEN"
```

The platform exports successful trajectories to `tenant-{org_id}/shared/skills/{name}/training/dataset_YYYYMMDD_HHMMSS.jsonl`.

Verify:

```bash
curl http://ops.surogate.ai/v1/skills/<name>/training-data \
  -H "Authorization: Bearer $TOKEN"
```

You should see the JSONL file with row counts. If row counts are low (under 100), iterate on agent behaviour to generate more 👍 sessions before training.

**4. Train externally**.

Download the JSONL:

```bash
curl "http://ops.surogate.ai/v1/skills/<name>/file?path=training/dataset_XXXXX.jsonl" \
  -H "Authorization: Bearer $TOKEN" -O
```

Train with your preferred pipeline:

```bash
# OpenAI fine-tuning
openai api fine_tunes.create -t dataset.jsonl -m gpt-4o-mini-2024-07-18

# Unsloth LoRA
python train.py --dataset dataset.jsonl --base unsloth/Qwen2.5-Coder-7B --output ./expert
```

Serve the resulting model behind an OpenAI-compatible endpoint:

```bash
vllm serve Qwen/Qwen2.5-Coder-7B \
  --enable-lora --lora-modules expert=./expert --port 8000
```

**5. Activate**.

```bash
curl -X POST http://ops.surogate.ai/v1/skills/<name>/activate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"endpoint": "http://your-vllm-host:8000/v1"}'
```

Status moves from `draft` to `active`. The base LLM now sees the expert in `# Available Experts`.

**6. Verify it works**.

Open a chat with an agent that has this skill attached. Send a trigger-matching prompt. Check EVENTS:

```
expert.delegation       expert=<name>, task=<...>
tool.call               terminal(...)
expert.result           "..."
```

If the expert's output is good, the base LLM should call it consistently. If not, you may need to retrain on a larger or better dataset.

**7. Monitor**.

After ~20 invocations, check:

```bash
curl http://ops.surogate.ai/v1/skills/<name> -H "Authorization: Bearer $TOKEN"
```

Look at `expert_stats.total_successes / total_uses`. Retirement is a deliberate act, not an automatic one — when the rate stops justifying the expert, retire it with `POST /v1/skills/{id}/retire` and the agent falls back to the base model for that task.

**8. Retrain**.

Periodically run a fresh `collect` → train → activate cycle to keep the expert sharp on recent traffic.

---

## 2. Build a custom skill with conditional tool activation

**Goal**: a skill that activates only when specific tools are available. Useful for tool-dependent workflows.

### Steps

**1. Identify the dependency**.

Say you want a `kubectl-diagnose` skill that runs `kubectl describe ...` and analyses the output. It requires the `terminal` tool (or an MCP server that exposes `kubectl`).

**2. Write the skill**.

```markdown
---
name: kubectl-diagnose
description: Diagnose K8s pod issues by running kubectl describe and analysing output
trigger: pod is failing, k8s issue, debug pod, kubectl, why isn't this running
tools: [terminal]
requires_tools: [terminal]
---

When asked to diagnose a Kubernetes pod issue:

1. Use `terminal` to run `kubectl describe pod <name>` (ask the user for the pod name if not given).
2. Identify the failure mode:
   - **ImagePullBackOff** → image registry / authentication issue
   - **CrashLoopBackOff** → check `kubectl logs --previous`
   - **Pending** → check node taints / resource requests
   - **OOMKilled** → memory limit too low or memory leak
3. For each finding, suggest a concrete fix (kubectl command or YAML diff).

Format your response as:
**Finding**: brief description
**Cause**: technical explanation
**Fix**: specific action to take
```

**3. Publish**.

POST `/v1/skills` with the content. Then publish a tag.

**4. Attach to agents that have `terminal`**.

For agents that have `terminal` in their allowlist, the skill loads. For agents where `terminal` is denied (e.g. customer-support agents), the skill is filtered out via `requires_tools`. This is exactly what you want — the skill can't fire in contexts where its tool isn't available.

**5. Test**.

Open a chat with an agent that has `terminal`. Ask: *"My nginx pod is failing, can you check?"*

Watch the SKILLS tab — `kubectl-diagnose` should load and invoke. EVENTS should show `tool.call: terminal` with `kubectl describe ...`.

If the same prompt to an agent without `terminal` doesn't trigger the skill (or triggers but errors), the conditional activation is working.

---

## 3. Build an MCP server with OAuth

**Goal**: connect to an internal API that uses OAuth 2.1. The agent should be able to call your API safely without seeing the credentials.

### Steps

**1. Set up your MCP server**.

Use the [MCP SDK](https://modelcontextprotocol.io/sdk) to build a server that:
- Exposes tools matching your API (`create_ticket`, `list_users`, etc.)
- Accepts an OAuth bearer token in the `Authorization` header
- Optionally implements `MCP-Resource-Discovery` for the platform's `list_resources`

Deploy the MCP server somewhere accessible (your own K8s cluster, behind a domain like `mcp.acme.com`).

**2. Register the OAuth client in your IDP**.

For Surogate's MCP proxy to authenticate, register a client in your OAuth provider:
- **Client ID** + **Client Secret**
- **Redirect URI**: the platform automatically configures localhost redirect for PKCE; you may need to allowlist `http://localhost:*/callback`
- **Scopes**: minimal set needed by your tools

**3. Add the MCP server in Surogate**.

Library → Skills & Tools → MCP SERVERS → ADD SERVER:

```yaml
name: acme-internal-api
transport: http
url: https://mcp.acme.com
auth: oauth
oauth:
  client_id: <your-client-id>
  client_secret: <your-client-secret>
  scope: read write
```

**4. Store the client secret in the Vault**.

VAULT → ADD CREDENTIAL:

```
Name: acme_internal_secret
Value: <your-client-secret>
```

In the MCP server config, change `client_secret: <your-client-secret>` to:

```yaml
client_secret_ref: acme_internal_secret
```

**5. Enable the server**.

Click ENABLE. The platform connects, runs the security scan against the tool definitions, and registers passing tools. First time, the OAuth flow opens a browser to authorize:

- A localhost server starts
- Browser opens to `https://your-idp.com/authorize?...&code_challenge=...`
- You approve in browser
- Token comes back to localhost
- Platform caches the token in `/var/lib/surogates/tokens/`

Subsequent calls auto-refresh.

**6. Attach to an agent**.

KNOWLEDGE & TOOLS → MCP Servers → + Attach server → `acme-internal-api`.

The agent now sees the tools from your MCP server. Test:

```
User: Create a Jira ticket about the recent outage with priority P1.
Agent: I'll create the ticket. [calls create_ticket(...)]
Agent: Ticket ABC-123 created.
```

**7. Audit credential access**.

Query the tenant audit log:

```sql
SELECT * FROM audit_log
WHERE org_id = $1 AND type = 'credential.read'
  AND data->>'name' = 'acme_internal_secret'
ORDER BY created_at DESC;
```

Confirms when the secret was resolved and by which MCP proxy instance.

---

## 4. A/B evaluation of two agent versions

**Goal**: compare a new version of your agent against the current production version on a custom benchmark.

### Steps

**1. Build a Custom Benchmark from your 👎 corpus**.

Datasets → NEW DATASET → From Conversations:
- Filter: agent=`acme-support-bot`, thumb_down=true, last 30 days
- Format: SFT or Conversation
- Name: `acme-support-failures-2026q1`

**2. Wrap as an evaluation benchmark**.

Evaluations → NEW EVALUATION → Custom Benchmark:
- Name: `acme-support-regression-suite`
- Dataset: `acme-support-failures-2026q1`
- Metric: LLM-judge (Claude Sonnet)
- Judge prompt: *"Did the agent's response accurately address the user's question? Score 0 (no) to 10 (yes). Brief explanation."*

**3. Deploy the candidate agent**.

Either:
- Clone `acme-support-bot` as `acme-support-bot-v2` and apply your changes
- Or use a feature branch in the Hub

**4. Run the evaluation on the current production agent**.

Evaluations → `acme-support-regression-suite` → RUN EVALUATION:
- Target: `acme-support-bot` (production)
- Judge LLM: Claude Sonnet (your existing OpenRouter key)
- API Key: `<openrouter_key>`

Wait for results. Each sample shows model output + judge score + judge reasoning.

**5. Run the same evaluation on the candidate**.

Same benchmark, target = `acme-support-bot-v2`. Same judge.

**6. Compare**.

Open the two run reports side-by-side. Look at:
- **Aggregate score** — does v2 beat v1?
- **Per-sample comparison** — where does v2 win, where does it lose?
- **Critical regressions** — any samples where v2 scored lower than v1 by ≥3 points?

**7. Decide**.

If v2 net-improves and doesn't have critical regressions: promote v2.

If v2 regresses on important cases: iterate. Possibly add a skill or adjust the SOUL.md based on what v1 did right that v2 lost.

---

## 5. Synthetic data pipeline (teacher / judge / worker)

**Goal**: you don't have enough labeled traffic for fine-tuning. Generate labeled training data via LLMs.

### Steps

**1. Define the task and unlabeled inputs**.

Say you want to train a sentiment classifier. You have 10,000 customer support tickets (the raw text) and need labeled sentiment.

**2. Build the synthetic dataset**.

Datasets → NEW DATASET → Synthetic Generation:

- **Inputs source**: paste a CSV / JSONL of unlabeled examples, or reference an existing dataset
- **Teacher**: a strong LLM (Claude Opus 4.7) that generates a candidate label per input
- **Judge**: a second LLM (Claude Sonnet 4.6) that scores the teacher's output 1-10
- **Worker**: a smaller model that produces the final formatted output
- **Threshold**: discard samples where judge score < 7

Click GENERATE.

**3. Monitor the pipeline**.

PIPELINE tab shows the DAG. As the pipeline runs:
- Teacher generates candidates
- Judge scores them
- Worker formats the surviving candidates
- The final dataset is written to the Hub

**4. Inspect quality**.

Open SAMPLES → click random rows → verify the labels are reasonable. If the teacher is unreliable, switch to a stronger model and re-run.

**5. Train**.

NEW RUN with the synthetic dataset as input. SFT method, base model of your choice.

**6. Combine with real traffic**.

If you also have a few hundred real labeled examples, combine them with synthetic data in the same training run. Real data is gold; synthetic data fills the gaps.

---

## 6. Integrate via the API channel for batch jobs

**Goal**: your nightly pipeline needs an agent to process 1,000 customer cases without a human in the loop.

### Steps

**1. Get a service-account token from an admin**.

```bash
# Admin issues a token
curl -X POST http://ops.surogate.ai/v1/admin/service-accounts \
  -H "Authorization: Bearer <admin-jwt>" \
  -d '{"org_id": "...", "name": "nightly-classifier-pipeline"}'

# Response: token is returned ONCE
# {"id": "...", "token": "surg_sk_..."}
```

The token starts with `surg_sk_`. Save it securely.

**2. Make sure the agent has the right setup**.

Agent `classifier-bot` needs to:
- Be `running`
- Have the right skills attached
- Have a tool envelope including `create_artifact` (so the response is structured)

**3. Write your pipeline**.

```python
import json
import requests
from time import sleep

SA_TOKEN = "surg_sk_..."  # from secret store
BASE = "http://ops.surogate.ai/v1/api"
H = {"Authorization": f"Bearer {SA_TOKEN}"}

def classify_case(case):
    # Submit. The token fixes the agent — the body carries no agent selector.
    resp = requests.post(
        f"{BASE}/prompts",
        headers=H,
        json={
            "prompt": f"Classify this support case: {case['text']}",
            "idempotency_key": case["case_id"],
            "metadata": {"pipeline": "nightly-batch", "version": "v3"},
        },
    )
    session_id = resp.json()["session_id"]

    # Poll for a terminal status
    while True:
        s = requests.get(f"{BASE}/sessions/{session_id}", headers=H).json()
        if s["status"] in ("completed", "failed"):
            break
        sleep(5)

    # Read the log. Events are SSE; the answer is the LAST llm.response.
    answer, etype = None, None
    with requests.get(
        f"{BASE}/sessions/{session_id}/events", headers=H, stream=True
    ) as r:
        for line in r.iter_lines(decode_unicode=True):
            if line.startswith("event:"):
                etype = line.split(":", 1)[1].strip()
                if etype in ("session.done", "stream.timeout"):
                    break
            elif line.startswith("data:") and etype == "llm.response":
                answer = json.loads(line.split(":", 1)[1])["message"].get("content") or answer
    return answer


# Process the batch
with open("cases.jsonl") as f:
    for line in f:
        case = json.loads(line)
        case["classification"] = classify_case(case)
        print(json.dumps(case))
```

The event-read contract — SSE only under `/v1/api/`, no `assistant.final` type, stream caps — is spelled out in [Sessions → API channel sessions are different](/develop/features/sessions/#api-channel-sessions-are-different).

**4. Idempotency**.

`idempotency_key` is a **body field**, not a header. An `Idempotency-Key` header is ignored and you get a duplicate session.

Keys are scoped per org and never expire. The first call returns `deduplicated: false` with a new session; a repeat returns `deduplicated: true` with the original `session_id` and enqueues no new work. Keys from different orgs never collide.

Use `metadata` for pipeline passthrough — it lands on `sessions.config['pipeline_metadata']`, which is what you join results back on.

**5. Submit in batches**.

One round-trip carries up to **100** prompts:

```python
rows = [json.loads(line) for line in open("cases.jsonl")][:100]

resp = requests.post(
    f"{BASE}/prompts:batch",
    headers=H,
    json={"prompts": [
        {
            "prompt": f"Classify this support case: {row['text']}",
            "idempotency_key": row["case_id"],
            "metadata": {"pipeline": "nightly-batch"},
        }
        for row in rows
    ]},
)
for row, result in zip(rows, resp.json()["results"]):
    row["session_id"] = result["session_id"]   # None when result["error"] is set
```

Each entry is accepted or rejected independently — one bad prompt does not fail the rest, and a rejected slot comes back with `error` set and `session_id: null`. The response preserves input order, so you can zip it straight onto your source rows. The call returns a 500 only when *every* entry failed.

**6. Concurrency**.

The platform supports parallel API requests. Run with concurrency:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=10) as ex:
    futures = {ex.submit(classify_case, c): c for c in cases}
    for f in as_completed(futures):
        # ...
```

Watch rate limits: the default is 300 requests/min, counted per org **and** agent in a fixed 60s window, and overridable per tenant with the governance setting `rate_limit_rpm`. The platform returns `429` if you exceed.

**7. Monitor**.

API-channel sessions show up in the Sessions list with `channel=api`. You can filter and audit them like any other sessions.

For pipeline-side monitoring, use the SQL view:

```sql
SELECT status, count(*) FROM sessions
WHERE org_id = $1
  AND channel = 'api'
  AND created_at > now() - interval '24 hours'
GROUP BY status;
```

**8. Record judge grades back onto the session**.

If the pipeline scores its own outputs, write the grade back so training-data selection can weight on it:

```python
requests.post(
    f"{BASE}/sessions/{session_id}/events/{event_id}/feedback",
    headers=H,
    json={
        "rating": "up",                              # required — "up" or "down"
        "score": 0.82,                               # optional float, 0.0–1.0
        "criteria": {"accuracy": 1.0, "tone": 0.5},  # float values only
        "rationale": "Correct label, slightly verbose.",
    },
)
```

`event_id` is the numeric event id — the `id:` line of the SSE stream, or `events.id` in SQL. It must name an `llm.response` or an `expert.result` event; anything else is a 400. Feedback on an `llm.response` emits `user.feedback`; on an `expert.result` it emits `expert.endorse` or `expert.override` depending on the rating.

Feedback posted with a service-account token is stored with `source: "judge"`, while a user JWT posting to the `/v1/…` route gets `source: "user"` — so judge grades stay separable from human 👍/👎 when you build a training set. Repeat calls from the same principal are no-ops: the existing rating is returned unchanged.

---

## 7. Saga rollback flow (multi-step external mutation)

**Goal**: an agent that creates resources across multiple external systems. If any step fails, prior steps must roll back automatically.

### Steps

**1. Identify the operation**.

Example: "create a customer in Salesforce, then a project in Jira, then send a welcome email." If the email step fails, you don't want a half-set-up customer.

**2. Configure MCP servers with declared undo tools**.

For each MCP server that mutates external state, the server must expose an undo tool:

- `create_salesforce_customer` ↔ `delete_salesforce_customer`
- `create_jira_project` ↔ `delete_jira_project`
- `send_email` (no undo — can't unsend; mark as escalation-only)

The MCP server's tool definition signals which undo tool corresponds to which forward tool.

**3. Enable Saga on the agent**.

CONFIG → Saga → toggle ON. Settings:
- `default_step_timeout: 300`
- `default_max_retries: 2`

**4. Have the agent execute the flow**.

The agent calls each MCP tool in order. The platform tracks each call as a saga step.

**5. Failure case**.

If `send_email` fails:
1. Saga detects step failure
2. Platform calls `delete_jira_project` to undo the previous step
3. Platform calls `delete_salesforce_customer` to undo the first step
4. Workspace is back to pre-flow state
5. The session emits **one** `saga.compensate` event per saga, carrying `steps_rolled_back` and the rollback `reason` — not one per undo
6. The session METADATA's `saga.compensated` flag is set

**6. Escalation case**.

If `send_email` fails AND `delete_jira_project` ALSO fails (e.g. the Jira API is down):
1. The saga transitions to `escalated`
2. The `saga.compensate` event carries a non-empty `failed_steps` list naming the undo calls that themselves failed
3. An operator resolves it by hand — escalation emits no dedicated event and raises no inbox item (`inbox.governance_gate` belongs to the approval gate, not to saga)

**7. Observability**.

Query saga state:

```sql
SELECT
  s.id, s.status, s.created_at,
  count(*) FILTER (WHERE e.type = 'saga.step_begin') AS steps_started,
  count(*) FILTER (WHERE e.type = 'saga.step_committed') AS steps_committed,
  count(*) FILTER (WHERE e.type = 'saga.compensate') AS compensations,
  bool_or(e.type = 'saga.compensate'
          AND jsonb_array_length(coalesce(e.data->'failed_steps', '[]'::jsonb)) > 0)
    AS escalated
FROM sessions s
LEFT JOIN events e ON e.session_id = s.id
WHERE s.org_id = $1
  AND e.type LIKE 'saga.%'
GROUP BY s.id
ORDER BY s.created_at DESC
LIMIT 100;
```

**8. Read-only tools are excluded**.

Saga doesn't track `read_file`, `search_files`, `web_search`, `skills_list` — they don't mutate state. Sequential execution is forced only when state-mutating tools are involved.

---

## Where to go from here

You've covered the main builder workflows. For more depth:

- [Runtime architecture](/develop/reference/runtime-architecture/) — the surogates runtime under the hood
- [Tool catalog](/develop/reference/tool-catalog/) — every built-in tool with parameters
- [Event types](/develop/reference/event-types/) — the full event log enum
- [Glossary](/develop/reference/glossary/) — every term in one place

Or back to [The builder loop overview](/develop/loop/overview/) for the iteration cycle.

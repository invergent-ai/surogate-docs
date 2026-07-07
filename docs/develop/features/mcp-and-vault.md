---
title: MCP & Vault
sidebar_position: 4
---

# MCP & Vault

The **Model Context Protocol** (MCP) is an open standard for connecting LLMs to external tools and data. Surogate ships a full MCP client + a credential-injecting proxy + security scanning.

You manage MCP servers in **Skills & Tools → MCP SERVERS tab** (Develop or Work mode). The Vault button at the top of that tab opens the credential store.

## Architecture

```
Sandbox / Worker
    │
    │  MCP tool call
    ▼
MCP Proxy (separate K8s service)
    │
    │  injects credentials from vault
    ▼
External MCP Server (stdio or HTTP)
```

The proxy is the trusted credential broker:

- Sandboxes can only reach the MCP proxy (K8s NetworkPolicy enforces this)
- The proxy holds credentials in memory (fetched from the Vault on connection)
- Outbound calls to MCP servers carry injected headers/args without the sandbox ever seeing secrets

This is the structural fix for "what if my agent leaks an API key" — the agent literally cannot access keys, even if fully prompt-injected.

## Two transports

### Stdio

Launch the MCP server as a subprocess; communicate via stdin/stdout. Configuration:

```yaml
mcp_servers:
  github:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_TOKEN_REF: github_token   # resolved from Vault
    timeout: 120
```

Best for: locally-installable CLI-like tools, MCP servers shipped as npm packages.

### HTTP / StreamableHTTP

Connect to a remote MCP server over HTTP:

```yaml
mcp_servers:
  jira:
    transport: http
    url: "https://mcp.acme.com/jira"
    auth: oauth
    oauth:
      client_id: "surogates-agent"
      scope: "read write"
    timeout: 120
```

Best for: cloud-hosted MCP servers, shared infrastructure across tenants.

## MCP client features

| Feature | Description |
|---|---|
| **Auto-reconnect** | Exponential backoff with up to 5 retries on connection loss |
| **Sampling** | MCP servers can request LLM completions back through the client |
| **Environment filtering** | Only explicitly allowed env vars passed to stdio servers |
| **Credential stripping** | Secrets scrubbed from error messages |
| **Per-server timeout** | Configurable per server |
| **Thread safety** | Dedicated background event loop for MCP connections |

## OAuth 2.1 PKCE for protected servers

```
1. Agent needs to call an OAuth-protected MCP tool
2. MCP client checks for cached tokens (on disk)
3. If no valid token:
   a. Start ephemeral localhost HTTP server for redirect
   b. Open browser to authorization URL with PKCE challenge
   c. User approves in browser
   d. Callback server receives authorization code
   e. Exchange code for access + refresh tokens
   f. Store tokens on disk for reuse
4. Attach access token to MCP requests
5. Auto-refresh when token expires
```

Configuration:

```yaml
mcp_servers:
  salesforce:
    url: "https://mcp.salesforce.com/mcp"
    auth: oauth
    oauth:
      client_id: "pre-registered-id"
      client_secret: "secret"
      scope: "api refresh_token"
      redirect_port: 0                # auto-pick available port
      client_name: "Surogates Agent"
      token_dir: "/var/lib/surogates/tokens"
```

## The credential vault

The **Vault** button on the MCP Servers tab opens the credential store:

| Field | Notes |
|---|---|
| **Name** | Reference name (e.g. `github_token`) — used in MCP server configs as `<NAME>_REF: name` |
| **Value** | Write-only. You set it, and later **Update** it (store a new value) or **Remove** it — but the value is never displayed back to you. The list API returns names + timestamps only, never the secret. |
| **Scope** | Project-scoped (= org). Credentials belong to the project; every MCP server in the project can reference them. |

System-owned credentials (used by platform/system agents) are protected: the API refuses to delete them (`403`), and a credential still consumed by a running agent's MCP server can't be deleted until you stop the consumer (`409`, in-use conflict).

### How references work

In an MCP server config:

```yaml
mcp_servers:
  github:
    env:
      GITHUB_TOKEN_REF: github_token       # ← reference
```

At runtime, the MCP proxy:

1. Sees `GITHUB_TOKEN_REF: github_token`
2. Resolves `github_token` from the Vault
3. Substitutes the actual value in the outbound request

The sandbox never sees the value. Credentials don't appear in logs, error messages, or agent contexts.

### Encryption

Vault credentials are encrypted at rest with Fernet (AES-128-CBC + HMAC-SHA256). The symmetric key lives in a K8s cluster secret.

## MCP server config layers

| Layer | Location | Managed by |
|---|---|---|
| Platform | `/etc/surogates/mcp/servers.json` | Platform operator |
| Org | `tenant-{org_id}/shared/mcp/servers.json` | Org admin |
| User | `tenant-{org_id}/users/{uid}/mcp/servers.json` | End user |

Last-wins precedence by server name.

## Security scanning

Every MCP tool definition is scanned before registration:

| Threat | What it catches |
|---|---|
| **Invisible Unicode** | Zero-width chars, bidi marks in tool names/descriptions |
| **Prompt injection** | Deceptive descriptions that trick the LLM |
| **Hidden HTML** | HTML comments with invisible instructions |
| **Tool poisoning** | Descriptions that manipulate the LLM into dangerous behaviour |
| **Rug-pull** | Tool definitions that change between connections (SHA-256 fingerprinting) |

Tools failing scanning are not registered. Scan results land in the tenant audit log:

```sql
SELECT * FROM audit_log
WHERE type = 'mcp.tool_scan'
  AND org_id = $1
ORDER BY created_at DESC;
```

## Rug-pull detection

If a server returns a different tool definition on reconnect (different fingerprint), the scanner emits a warning. Common cause: the upstream MCP server got updated. Review the diff before re-enabling.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/mcp-servers` | List (filter by `project_id`, `enabled`, `layer`) |
| `GET` | `/api/mcp-servers/composio/catalog` | Live Composio toolkit catalog |
| `GET` | `/api/mcp-servers/{id}` | Detail with connected tools |
| `POST` | `/api/mcp-servers` | Add server |
| `PATCH` | `/api/mcp-servers/{id}` | Update config (including the `enabled` toggle) |
| `GET` | `/api/mcp-servers/{id}/in-use` | List agents referencing this server |
| `DELETE` | `/api/mcp-servers/{id}` | Remove server (409 if attached to a running agent) |
| `GET` | `/api/credentials` | List Vault entries (names + timestamps only, never values) |
| `POST` | `/api/credentials` | Store a credential (same name overwrites — this is how "Update" works) |
| `GET` | `/api/credentials/{name}/in-use` | List MCP servers referencing this credential |
| `DELETE` | `/api/credentials/{name}` | Remove (403 if system-owned, 409 if in use) |

There is no dedicated `/enable` endpoint — enabling/disabling is a `PATCH` that flips the `enabled` flag. Tool security scanning happens in the MCP proxy at tool-discovery time, not as a synchronous call on this API. Updating a credential is a `POST` with the same name (the store upserts); there is no `PUT`.

## What's next

[Hub](./hub.md) for the artifact versioning layer. [Datasets](./datasets.md) and [Training](./training.md) for the training pipeline. [Use cases](../use-cases.md) → "Build an MCP server with OAuth."

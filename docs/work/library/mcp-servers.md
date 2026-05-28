---
title: MCP servers
sidebar_position: 3
---

# MCP servers

The **Model Context Protocol (MCP)** is an open standard for connecting LLMs to external systems — your CRM, your ticketing tool, GitHub, internal APIs, anything that speaks MCP.

You wire it up once in the Library; any agent in your tenant can attach it.

## The MCP servers tab

**Library → Skills & Tools → MCP SERVERS tab.**

The header shows how many MCP servers are **enabled** (in this build I see "1 MCP servers enabled" with the test server I created during the audit). Below that: a list of every server in your tenant. Each row shows:

- Name (`test-context7`, `github-readonly`, etc.)
- Transport (HTTP or stdio)
- Scope (PLATFORM / ORG / USER)
- URL
- Auth method
- Number of exposed tools
- Number of agents connected

Click any server to open its detail panel.

## Adding a server

Click **ADD SERVER** at the top of the list. The form:

| Field | Required | Notes |
|---|---|---|
| **Name** | Yes | Lowercase, hyphens, alphanumeric (e.g. `linear-tickets`, `github-readonly`) |
| **Description** | No | What this server provides |
| **Transport** | Yes | **HTTP** for cloud-hosted, **stdio** for local subprocess |
| **URL** (for HTTP) | Yes | The MCP server's endpoint (e.g. `https://mcp.linear.app/mcp`) |
| **Command** + args (for stdio) | Yes | The shell command to launch the server (e.g. `npx -y @modelcontextprotocol/server-github`) |
| **Auth Method** | Yes | **None** / **OAuth** / **API Key** / **Bearer Token** |
| **Timeout (seconds)** | No | Default 120 |

Click **ADD SERVER**. The server is created in a `disabled` state until you trigger a security scan.

### Choosing transport

- **HTTP / StreamableHTTP** — for cloud-hosted MCP servers. The platform's MCP proxy talks to them over HTTP. Best when the server is somewhere remote (SaaS connectors, your internal API, third-party MCP services).
- **stdio** — for locally-installed tools that launch as subprocesses. Good for CLI-like tools, MCP servers shipped as npm packages.

If in doubt, HTTP is the more modern choice.

## Configuring authentication

Most MCP servers need credentials. Four options:

### None

No auth. Use only for public, read-only MCP servers (the `context7` MCP I tested in my audit is a public example — no creds needed to fetch documentation).

### OAuth

For servers that require an OAuth 2.1 PKCE flow (Salesforce, Slack, GitHub, most enterprise SaaS). When the agent first calls a tool from this server, the platform opens a browser, you sign in / approve, and tokens are cached on disk.

Configure:
- **Client ID** (registered with the MCP server)
- **Client secret** (sometimes required)
- **Scope** (e.g. `read write`)
- **Token directory** (where the platform stores tokens)

### API Key

A static key the platform passes as a header. Stored in the **Vault** so the agent's sandbox never sees it.

### Bearer Token

A long-lived bearer token. Same as API key in practice — stored in the Vault, injected by the proxy.

## The Vault

The **VAULT** button at the top of the MCP servers tab opens a credential store. This is where you store API keys, OAuth secrets, and other tokens the MCP proxy needs to authenticate to upstream servers.

Each credential has:
- **Name** (used to reference it from MCP server configs — e.g. `GITHUB_TOKEN_REF: github_token`)
- **Value** (masked by default; SHOW to reveal, COPY to clipboard, ROTATE to replace, DELETE to remove)

> :::info Credentials never reach the sandbox
> The agent's sandbox is the most untrusted component in the platform. Credentials live in the Vault and are injected by the MCP proxy as it forwards calls — even a fully prompt-injected agent can't exfiltrate them.
> :::

## Enabling and scanning a server

After adding a server: click **ENABLE**. The platform:

1. Connects to the MCP server using the configured auth.
2. Lists every tool the server exposes.
3. Runs each tool definition through a **security scanner** that checks for:
   - Invisible Unicode (zero-width, bidi marks)
   - Hidden HTML comments
   - Prompt-injection patterns
   - Tool-poisoning descriptions
   - Schema abuse
4. Computes a SHA-256 fingerprint for each tool.
5. Registers each tool that passes.

The detail panel shows the result: **Exposed Tools** count, security-scan status.

> :::warning Known state-machine quirk
> Sometimes the detail panel shows DISABLE (implying the server is enabled) but the security scan reads "Not scanned — enable the server to trigger tool scanning." If this happens, click DISABLE then ENABLE again to force a fresh scan.
> :::

## Attaching to an agent

Open the agent → **Configure** in the left nav → the **Skills & Tools** tab → **+ Attach server…** combobox → pick the MCP server.

The agent's tool catalogue grows by however many tools that server exposes. The LLM sees them in `skills_list` style — name + description per tool.

To remove: click the **X** next to an attached server in the same section.

## Editing a server

Server detail → **EDIT**. Same form as ADD SERVER but pre-filled. Most fields can change; transport and URL are the structural ones — if you change them, behaviour is essentially "deleted old, added new."

## Deleting a server

Server detail → **DELETE**. The pre-flight check warns you if any agent has it attached.

## Rug-pull detection

The security scanner fingerprints every tool definition. If a server returns a different tool definition on reconnect (the same tool name with different behaviour), the platform flags it as a **rug-pull**. Common cause: the upstream MCP server got updated. Review the diff before re-enabling.

## What MCP gives you in practice

| You want to... | Add an MCP server for... |
|---|---|
| Create / read GitHub issues | `@modelcontextprotocol/server-github` (npm) |
| Look up customer accounts in Salesforce | A Salesforce MCP server |
| Read internal docs from Confluence / Notion | Confluence / Notion MCP servers |
| Get current data from your data warehouse | A SQL MCP server (Postgres, Snowflake, etc.) |
| Send messages to Slack channels from inside an agent | A Slack MCP server (different from the Slack channel — this is for outbound) |
| Integrate your internal API | Build a custom MCP server (see [Develop mode → MCP & Vault](/develop/features/mcp-and-vault)) |

## What's next

If you've covered the Library, head to [Channels](../channels/web.md) to publish the agent. Or jump to [Use cases](../use-cases.md) for end-to-end recipes.

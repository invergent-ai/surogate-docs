---
title: Assistants
description: The agents.yaml file, the assistant and website chat widgets, the console's help, builder and tagger agents, and the proposals API.
---

The configuration behind [Assistants](/portal/sites/assistants/). That page covers what people see in a chat with an agent, who the agent talks with, and how the agent is connected and used.

## The agent and its key

A secret connector holds the agent's key, such as `connectors/helper-key.yaml`:

```yaml
name: { ro: Cheia asistentului, en: The assistant's key }
kind: secret
```

The agents are named in `agents.yaml`, at the top of the portal's files:

```yaml
helper:
  url: https://helper-x1.cloud.surogate.ai
  agent: 7c1e9a52-3b4d-4e5f-8a6b-1c2d3e4f5a6b
  key: helper-key
  name: { ro: Asistentul primăriei, en: City Hall's assistant }
```

- `url`: where the agent answers, its own address. Inside the same cluster, the agents' service address works too.
- `agent`: the agent's id, as Studio shows it.
- `key`: the connector holding the agent's key.
- `name`: what the portal calls the agent; optional.

The portal talks to an agent with the agent's own API key: copy it in Studio, as [Connect your agents](/portal/sites/assistants/#connect-your-agents) says. Name the agent here, with a secret [connector](/portal/developer/connectors/#a-connectors-file) for the key. Publish the files, then set the key's value in the console under **Connectors**.

The key opens only for the agent and address `agents.yaml` names. If you change either, set the key again. No action can use the key.

## The assistant on a page

In a page's file (`sites/<site>/pages/<page>.yaml`), the portal's `assistant` widget:

```yaml
regions:
  main:
    - id: ask
      app: portal
      widget: assistant
      preferences:
        agent: helper
        title: { ro: Întrebați-ne, en: Ask us }
```

- `agent`: an agent `agents.yaml` names.
- `title`: the heading above the chat; optional. Without it, the agent's `name` is the heading; with neither, the chat has no heading.

The widget works once the agent is named in `agents.yaml` with its key: see [The agent and its key](#the-agent-and-its-key).

## The chat for visitors

The agent's website, in `agents.yaml`:

```yaml
helper:
  url: https://helper-x1.cloud.surogate.ai
  agent: 7c1e9a52-3b4d-4e5f-8a6b-1c2d3e4f5a6b
  website:
    publishableKey: surg_wk_…
```

- `publishableKey`: the website channel's key.
- `url`: the agent's own public https address, as the embed code names it. When the agent's `url` is already that address, leave it out.
- An agent used only for visitors needs no `key`.
- A key minted again, or the channel turned off, stops the chat until `agents.yaml` has the new key.

The portal's `website-chat` widget, one on a page, in a region of the page's file:

```yaml
- id: help
  app: portal
  widget: website-chat
  preferences:
    agent: helper
    title: { ro: Întrebați-ne, en: Ask us }
    welcome: { ro: Bună! Cu ce vă putem ajuta?, en: Hi! How can we help? }
    accent: "#4f46e5"
```

- `title`: the chat's heading. Without it, the agent's `name`, or "Assistant".
- `welcome`: a greeting before the first message, up to 500 characters.
- `accent`: the chat's colour, as `#rrggbb`.
- `position`: `bottom-right` (when left out) or `bottom-left`.

One `website-chat` widget on a page. Set up the channel in Studio first, as [A chat for visitors](/portal/sites/assistants/#a-chat-for-visitors) says.

## The console's agents

The help agent, the builder and the tagger, each with its own key connector, in `agents.yaml`:

```yaml
console-help:
  url: https://console-help-x1.cloud.surogate.ai
  agent: 2d4f6a8c-1b3e-4c5d-9e7f-0a1b2c3d4e5f
  key: console-help-key
  help: true
console-builder:
  url: https://builder-x1.cloud.surogate.ai
  agent: 9a1c3e5b-7d2f-4b6a-8c0e-2f4a6b8c0d1e
  key: console-builder-key
  builder: true
tagger:
  url: https://tagger-x1.cloud.surogate.ai
  agent: 5e7a9c1b-2d4f-4a6b-8c0d-1e2f3a4b5c6d
  key: tagger-key
  tags: true
```

- `help: true`: the console's Help. On one agent at most.
- `builder: true`: Describe a change. On one agent at most, never the help agent.
- `tags: true`: Suggest tags. On one agent at most, never the help agent.
- Each of them needs its `key`.

The rules for each:

- **The help agent** is kept for the console alone. No page's assistant names it, no job's `askAgent` asks it, it has no `website`, and no other agent in `agents.yaml` is the same agent under another name.
- **The builder:** one agent at most is the builder, and it needs its key. Like the help agent, the builder belongs to the console alone, and it is never the help agent too.
- **The tagger:** one agent at most is the tagger, and it needs its key. The console's help agent cannot be the tagger.

What each does is on [Help in the console](/portal/sites/assistants/#help-in-the-console), [Describe a change](/portal/sites/assistants/#describe-a-change) and [Suggest tags for content](/portal/sites/assistants/#suggest-tags-for-content).

## The portal as a tool of an agent

The portal serves an MCP server at `/_portal/mcp`. An agent reaches it with a token of a [service account](/portal/console/service-accounts/), as [Give an agent the portal as a tool](/portal/sites/assistants/#give-an-agent-the-portal-as-a-tool) says. The token's scopes are:

- `mcp`: **Use the portal as a tool of an agent**;
- `data`: **Read and change records of the data models, as the person may**, for an agent that should read records;
- `proposals`: **Propose changes**, for the console's builder.

## Propose a change through the API

An agent proposes through the portal's API, with a token holding **Propose changes** (`proposals`), given by name only:

1. `GET /_portal/api/proposals/base` gives the newest version and the files a proposal may change.
2. `POST /_portal/api/proposals` with `title`, an optional `description`, `baseVersion` and `changes`: each file's new text, or `null` to remove it.
3. `GET /_portal/api/proposals/<id>` shows where it stands, the note included.

A token proposes and withdraws; it never approves, whatever else it holds. What an administrator does with a proposal is on [Proposed changes](/portal/console/proposals/).

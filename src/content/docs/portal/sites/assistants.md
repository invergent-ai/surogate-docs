---
title: Assistants
description: Put a chat with one of your Surogate agents on a page, for the people signed in to the portal.
---

An assistant is a chat with one of your Surogate agents, on a page of the portal. A person signed in opens it and talks with the agent, which answers with everything it has: its skills, its tools and its knowledge. Each person sees only their own chats, and the agent keeps what it remembers of each person apart from everyone else.

## Connect your agents

The portal talks to an agent with the agent's own API key. Make one in Studio: open the agent, then **Channels → Web → Manage**, and copy the key. It starts with `surg_sk_`. Studio shows it once.

1. In the portal's files, add a secret [connector](/portal/sites/connectors/) for the key, such as `connectors/helper-key.yaml`:

   ```yaml
   name: { ro: Cheia asistentului, en: The assistant's key }
   kind: secret
   ```

2. Name your agents in `agents.yaml`, at the top of the portal's files:

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

3. Publish the files. Then, in the console under **Connectors**, set the key's value.

The key opens only for the agent and address `agents.yaml` names. If you change either, set the key again. No action can use the key.

## Place an assistant

Place the portal's `assistant` widget on a page:

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
- `title`: the heading above the chat; optional. Without it the chat has no heading, and its frame is named after the agent.

## What people see

- **A person signed in:** the chat, in a frame of its own, so neither the site's styles nor the chat's reach the other. They can start a new chat, or go back to one of their earlier chats; the first message names each one.
- **Visitors:** a prompt to sign in.
- **An administrator seeing the portal as someone else:** no chat.

## Who the agent talks with

The agent is told the person's name and email when a chat starts. Its memory of what one person said stays with that person: no one else's chat reaches it.

The agent's usage is billed to the agent's project, as all its work is. The portal keeps the list of each person's chats. The agent keeps the chats themselves, and records each turn.

When a person forgets a chat, it leaves their list in the portal. The agent still keeps the chat, with the person's name and email, as it keeps all its work.

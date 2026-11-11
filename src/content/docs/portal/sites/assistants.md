---
title: Assistants
description: Put a chat with one of your Surogate agents on a page, for the people signed in to the portal or for any visitor.
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
- `title`: the heading above the chat; optional. Without it, the agent's `name` is the heading; with neither, the chat has no heading.

## What people see

- **A person signed in:** the chat, in a frame of its own, so neither the site's styles nor the chat's reach the other.
  - They can start a new chat, go back to one of their earlier chats, or forget the one open. The first message names each chat.
  - The portal's own words follow the page's language; the chat's own controls are in English.
- **Visitors:** a link to sign in, which brings them back to the page.
- **People who may not see any page with the assistant:** no chat. An agent is reachable only from the pages that place it, for the people who may see them.
- **An administrator seeing the portal as someone else:** no chat.

## Who the agent talks with

The agent is told the person's name and email when a chat starts. Its memory of what one person said stays with that person: no one else's chat reaches it.

Each person may start 20 chats in ten minutes and send 40 messages in five, so that no one holds the agent from everyone else.

If you make the agent a new key in Studio, everyone's memory with the agent starts afresh: it belongs to the key.

The agent's usage is billed to the agent's project, as all its work is. The portal keeps the list of each person's chats. The agent keeps the chats themselves, and records each turn.

When a person forgets a chat, it leaves their list in the portal. The agent still keeps the chat, with the person's name and email, as it keeps all its work.

## A chat for visitors

A page can also carry a chat for its visitors, signed in or not: the agent's website channel, the chat Surogate draws on any website. It floats in a corner of the page, and opens when the visitor clicks it.

1. **Turn on the website channel in Studio.** Open the agent, then **Channels → Website**. Turn it on and add every address the portal serves the page on to its allowed origins.
   - Each origin is matched exactly, scheme, host and port: `https://portal.primaria.ro` and `https://www.portal.primaria.ro` are two.
   - The chat refuses a page on any address not in the list.
   - Set a limit on the messages of one chat there too: without one, a chat has none.
   - **Save.** Then copy the publishable key, which starts with `surg_wk_`, and the agent's address from the embed code.

2. **Give the agent its website in `agents.yaml`:**

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

3. **Place the portal's `website-chat` widget,** one on a page:

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

**What visitors and the agent keep:**
- The chat runs on the agent's runtime, which stores each conversation as it stores all the agent's work.
- A visitor's chat lasts while they stay on the page. Going to another page starts a new chat.
- The agent's memory of a visitor stays with that visitor, through a cookie the agent's address sets in their browser for a year. Mention it in your cookie notice.
- Browsers that block cookies of other sites, as Safari does, may not keep that memory, or the chat, when the agent's address is not the portal's.

**The publishable key:**
- It is made to sit in a page.
- The allowed origins stop other websites' pages from using it, but not a program that calls the agent directly.
- All the chat's visitors share the agent's limit on how fast it answers.
- A key minted again, or the channel turned off, stops the chat until `agents.yaml` has the new key.

The page is the same for every visitor, so it stays as fast as any public page.

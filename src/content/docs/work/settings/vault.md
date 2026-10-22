---
title: Vault
---

The **Vault** holds the keys and tokens your project's agents use: API keys for tools, channel tokens, coding-agent and git credentials. Each key has a name. You save the value once; Surogate encrypts it and never shows it again.

Open **Settings**, then **Vault**. The tab is in both Dev and Work mode and shows the active project's keys, so switch projects first to see another's.

## Who can change it

Everyone in the project can open the tab and see which keys exist. To change anything you need the project [**Editor** role](/work/settings/members/#what-each-role-can-do). For a **Viewer**, **Add key** is switched off with the hint **Viewers can't change this project**, and the **Update** and **Remove** buttons don't show.

## The key list

The header counts the keys (**3 keys**). Each row shows the key's name, then **Used by** the agent, user or part of Surogate that uses it, or **Not used**, and when it was added.

Two kinds of key don't show a way to change them:

- Keys that belong to one agent's own account, such as an agent's git token. They are listed for information only, with no **Update** or **Remove**.
- Tokens the platform mints for itself. These aren't listed at all.

An empty vault says so. Keys also land here by themselves when you connect a tool or a channel.

## Add a key

1. Choose **Add key**.
2. Enter a **Name**, for example `GITHUB_TOKEN`, and the **Value**. The value field is masked.
3. Choose **Save**. A message confirms **Saved** and the name.

Both fields are required. Saving under a name that already exists replaces its value.

## Replace a key's value

Choose **Update** on the key's row, enter the new value and choose **Save**. The name stays the same, so everything that refers to the key picks up the new value. Choose **Cancel** on the row to close the field.

## Remove a key

Choose **Remove**. Before it deletes anything, Studio checks what still uses the key and lists any running agent's tools and any active channel that does. Stop those agents or disconnect the channel first; a key in use can't be removed. A key owned by a system agent is refused too.

## Where keys are used

A key is stored by name and everything else refers to it by that name, so the agent's sandbox never holds the value.

- **MCP servers.** Adding a remote MCP server with an **API key** saves the key here, named after the server, and the server keeps only a reference. The proxy adds the key to each call. See [MCP servers](/work/library/mcp-servers/) and [MCP & Vault](/develop/features/mcp-and-vault/). The **Vault** entry on the MCP Servers tab and the **Key vault** button on an agent's **Tools** section both open this tab.
- **Model deploy forms.** Models that Surogate only forwards to (an OpenRouter or URL model) pick their API key from the vault. See [Models](/develop/features/models/#the-key-picker).
- **Voice providers.** Each speech provider's key for the [Voice channel](/work/channels/voice/#language-and-voice) is chosen from the vault, apart from **Hugging Face or your own server**, where it is optional.

If you remove a key that a voice line or model still points to, that line or model stops working. Replace the value with **Update** instead when you only want to rotate a key.

---
title: Voice channel
sidebar:
  label: Voice
---

Your agent answers phone calls. Callers dial a number, the agent greets them, listens and talks back, and every call is a conversation on the Voice channel. This page covers receiving calls.

## What you need

- The project [**editor** role](/work/settings/members/#what-each-role-can-do). Viewers can read but not change it. For a system agent you need to be an administrator.
- A free number. You pick one of the numbers Surogate provides. You can't bring your own number. If none is free, the page says "No free numbers right now. An admin adds them under Settings → Phone numbers."
- For any language other than Romanian: a speech provider. A hosted provider needs your account's key saved in the project's Vault; for **Hugging Face or your own server** a key is optional. See [Language and voice](#language-and-voice).

## Configuration in Surogate

Open the agent → [**Publish** → **Channels**](/work/workflow/publish-agent/#channels) → **Voice** under **Add a channel** → **Connect**.

1. Under **Number**, open **Phone number** and choose a number.
2. Adjust the sections below, or leave the defaults.
3. Click **Save and connect**. The status at the top changes from **Off** to **Active**, and calls to the number now reach this agent. (Once connected, the button reads **Save**.)

An agent has one number, and a number belongs to one agent at a time. If someone else takes the number first, or an admin retires it meanwhile, Surogate says *This number was just taken. Choose another one.* Choosing a different number and saving frees the old one.

## Language and voice

**Language** is the language the agent answers in. Surogate's own speech is included for Romanian only. For any other language, connect a provider.

Listening and speaking are set separately:

- **Hears callers with** turns speech into text. Choices: **Surogate, Romanian, included**, ElevenLabs, Cartesia, Deepgram, OpenAI, Gradium, and **Hugging Face or your own server**.
- **Speaks with** turns the agent's answers into speech. The same choices, plus Fish Audio.

With **Surogate, Romanian, included**, the only extra choice is **Voice**: **Female** or **Male**. Surogate refuses to save another language with its own speech.

With any other provider you use your own account, so it is billed by, and callers' audio is sent to, that provider. Each side shows:

- **Server URL**, for **Hugging Face or your own server** only: an OpenAI-compatible address such as `https://your-endpoint/v1`.
- The provider's **key**, chosen from the project's Vault. A key is needed for every provider except **Hugging Face or your own server**, where it is optional. **Test** checks that the provider accepts it and shows *Connected* or the reason it didn't.
- **Model**, from a list, or typed in for **Hugging Face or your own server**.
- For **Speaks with**: the voice. **Choose a voice** opens a list of the account's voices, with a preview, a search and an **Any language** box. ElevenLabs, Cartesia, Gradium and Fish Audio also have a **Library** tab next to **My voices**. For **Hugging Face or your own server** you type the voice name your server uses.

A line whose key is missing from the Vault can't be saved. If a key is removed later, callers hear two beeps and the call ends (**Provider unavailable**).

## How it answers

**Greeting** is the first thing callers hear, up to 500 characters. Leave it empty to use the default for the language. Say it is an AI assistant, as the default does.

### Phone lines it says on its own

Open **Phone lines it says on its own** to reword the fixed sentences the agent says without waiting for its model. Each is up to 300 characters, and an empty one plays the default for the language. For a language with no defaults, callers hear English unless you write the lines.

| Line | When it is said |
|---|---|
| **While it looks something up** | When the agent starts a lookup without a word. |
| **When the caller goes quiet** | Asked once, after the silence set in [Call limits](#call-limits). |
| **When the call ends on its own** | At the time limit, or after the caller stayed silent. |
| **When one answer fails** | The call goes on |
| **When the call cannot start** | Hangs up |
| **When every line is taken** | Hangs up (busy line) |
| **Reading out choices** | When the agent offers choices. Keep `{}` where the choices go. |
| **After an urgent alert on a call** | How to confirm an urgent alert phoned out (say yes or press 1). Not used on calls you receive. |

## Background sound

What callers hear around the agent. The default is **Silent**: only the voice. Or pick one of 13 places, each with a preview:

"Clinic front desk"; "Dental practice"; "Pharmacy counter"; "Restaurant reservations"; "Hotel reception"; "Beauty salon"; "Car service"; "Accounting or law office"; "Bank or insurance desk"; "Sales or support team"; "Delivery or taxi dispatch"; "School office"; "Small business, home office".

When a place is chosen, these appear:

- **Room**: **Off**, **Low** or **Normal**. The quiet sound of the place under the call. Default **Normal**.
- **Background events**: **Off**, **Rare** or **Normal**. Short sounds far away, such as a door or a phone in another room. **Rare** is about two a minute and **Normal** about four. Default **Rare**.
- **Typing and writing**: keys and clicks while the agent checks something, and a pen while the caller gives a name or a number. On by default.
- **Hold music**: **Off**, **Soft piano**, **Acoustic guitar** or **Calm ambient**. It plays only when a lookup takes longer than about eight seconds, and stops the moment the agent answers. Default **Off**.

If the sounds can't be loaded, Studio says so and the line works without them.

## Call limits

| Setting | What it does | Allowed | Default |
|---|---|---|---|
| **Longest call** | Ends the call politely after this. | 30 to 3600 seconds | 600 |
| **Silence before asking if they are still there** | Asked once, then it waits. | 5 to 300 seconds | 30 |
| **Then hang up after** | If the caller still says nothing. | 5 to 300 seconds | 15 |

Studio refuses a value outside the range and doesn't save it.

## Pronunciations

How names should sound. Fill **Written as** and **Said as** (each up to 64 characters), for example "Nvidia" said as "Envidia", then click **Add pronunciation**. You can add up to 100. The list shows the first 12 as chips; **Show all** opens the rest, a search box appears once there are more than 12, and the cross on a chip removes it.

## Callers

**Remember callers** is off by default. When it is on, the agent keeps what a caller said for their next call from the same number. A call with a hidden number is never remembered, and since a number can be faked, the agent never treats it as proof of identity.

## Try it

No **Try it** link: call the number from a phone. Until the first call, the screen says *No calls yet. Call* followed by the number *to try it.*

## Recent calls

Once a number is connected, **Recent calls** lists the latest calls, newest first, up to 50. It also lists calls the agent placed, such as a [Programs](/work/tools/programs/) step or an urgent alert; for those, **Caller** shows the person called.

| Column | Shows |
|---|---|
| **When** | When the call ended, or *In progress*. |
| **Caller** | The caller's number, or *Hidden number*. |
| **Length** | Minutes and seconds. |
| **Outcome** | One of the four below. |

- **Completed**: The call took place and ended.
- **Lines busy**: Every line was taken, so the caller heard the busy line and the call ended.
- **Error**: The call couldn't start; the caller hears the **When the call cannot start** line, or two beeps if speech setup failed.
- **Provider unavailable**: Your provider's key is missing or unreadable, or the provider failed mid-call (for example a revoked key, no credits, an outage). Two beeps.

## Limits

- Calls on the line at once are capped platform-wide; further callers hear the busy line (**Lines busy**).

## Reconnecting and disconnecting

- **Disconnect** asks for confirmation. The number goes back to the pool for other agents, and Recent calls is hidden.
- To connect again, open the Voice screen, choose a number and click **Save and connect**. The settings you had are still there.

## With the Copilot

The [Copilot](/work/tools/copilot/#phone-lines) can read a line, its recent calls and the free numbers, give an agent a number, change its settings and disconnect it. It can't switch the line to another speech provider, since that needs your key. It asks you to confirm each change first.

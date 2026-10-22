---
title: Surogate Desktop
sidebar:
  label: Surogate Desktop
---

Surogate Desktop is an app for your computer. It lets your agent work on a folder you choose, use your own browser and show you the web apps it starts. You chat with the agent as usual. The agent still thinks in the cloud; the app is its hands on your machine.

## Get it

On Linux (Ubuntu 24.04 LTS or a later LTS release, 64-bit Intel or AMD), run:

```bash
curl -fsSL https://surogate.ai/desktop/install.sh | bash
```

The script asks for `sudo` once. Then open Surogate from your applications. [Sign in](#sign-in) and start a chat on a folder (see [Working on a folder](#working-on-a-folder)).

Options go after `bash -s --`, as in `curl -fsSL https://surogate.ai/desktop/install.sh | bash -s -- --uninstall`:

- `--version <x.y.z>` installs that release, to go back to an earlier one.
- `--uninstall` removes Surogate Desktop. It asks before it deletes your sign-in and the agent's browser profiles. Your folders are never touched.
- `--ca-cert <file>` makes Surogate Desktop, the agent's browser and its commands trust your company's certificate authority (a PEM file). Use it if your network inspects encrypted traffic. Give the file to `curl` as well:

  ```bash
  curl --cacert company-ca.pem -fsSL https://surogate.ai/desktop/install.sh | bash -s -- --ca-cert company-ca.pem
  ```

Today Surogate Desktop is available for Linux. macOS and Windows builds aren't published yet.

Surogate Desktop checks for updates when it starts and every 6 hours. When one is ready, the sidebar says **Update available** and **Restart to update** installs it. An administrator on the computer has to approve the install. Without one, the sidebar says "An administrator needs to install this update."

## Sign in

The first time, the app asks for your agent's address (for example `https://agent.example.com`). Paste it and press **Connect**, then **Continue in your browser** and sign in there. The computer joins that one agent, so the app works with a single agent at a time.

Signing in adds the computer to the agent's list under [Settings > Devices](#devices).

## What it does

Point a chat at a folder and the agent reads, writes and organizes the files in it and runs commands there. It drives a browser already installed on your computer, in a profile of its own, and can open the web apps it starts once you allow it. A project is a coordinator chat that hands work to threads, each a chat of its own. See [Projects](/work/desktop/projects/).

## Working on a folder

Start a new chat in the app. When the agent lets chats work on folders of a computer and has **Multi session** on (see [Capabilities](/work/workflow/configure-agent/#capabilities)), the line under the composer says the chat works in a folder on this computer. **Choose another folder** and **Use the last folder** on that line switch between picking a folder and the one you used last. Otherwise the line says why, and the chat works in the cloud.

When you send the first message, Surogate shows a sheet, **Work in** the folder, where you:

1. Check the folder, or press **Change…** to pick another.
2. Choose how it works: **Work freely** or **Ask every time** (see [Approvals](#approvals)).
3. Press **Use this folder**.

The agent sees only this folder. Its file tools reach nothing else of yours. Its commands run in a small virtual machine on your computer, with the folder shared into it only while the chat is working. That is slower on a computer without hardware virtualization (Intel VT-x or AMD-V, turned on in the firmware settings), but it still works.

The sheet also says that the files the agent reads and what its commands print go to the agent in the cloud and can stay in the conversation.

### Folders that are refused

Surogate refuses a folder, and says why, when it:

- is your home folder, or holds it (including `/`).
- is, holds or lies inside a credentials folder in your home: `.ssh`, `.aws`, `.gnupg`, `.kube`, `.docker`, `.azure` or `.config/gh`.
- is, holds or lies inside the app's own data or cache, or where the agent's browser runs.
- is inside one of the computer's system folders, or one where the sandbox keeps its own tools (such as `/usr` or `/etc`).
- has `*`, `?`, `[` or `]` in its path.

A folder that is missing, or is not a folder, is refused too.

## Approvals

Each chat has a mode. The bar for the chat shows it as **Works freely** or **Asks every time**.

| Mode | What it does |
|---|---|
| **Work freely** | Runs commands and changes files without asking first. This is what the sheet starts on. |
| **Ask every time** | Asks you before each command, each file change and each input to a running command. |

In **Ask every time**, reading never asks: looking at files, listing folders, searching and checking on a running command go through.

Two things ask in both modes:

- **Network access.** Commands reach the package registries they need, and the computer's own services stay out of reach of both the commands and the browser. Any other site, your local network included, asks. **Allow** covers the connections waiting now; later ones ask again. **Allow all its ports for this chat** lets that site through on every port for the rest of the chat. In the browser's prompt, **Allow for this chat** does the same for the browser.
- **The browser.** The first time a chat uses your browser, and each time it would open a port of the chat's own web app in it.

In **Ask every time**, every action the agent takes on a page asks too: opening an address, running a script, clicking, typing, dragging, uploading a file, and downloads. Reading the page does not.

Switch the mode from the bar. Going to **Asks every time** is immediate. Going to **Works freely** opens Surogate Desktop's own confirmation, because only the app can make a chat less safe. An action's prompt also has **Allow and stop asking**, which allows that action and makes the chat work freely.

In **Work freely**, downloads from a page and the agent's uploads happen without a prompt.

## Your browser

The agent drives Chrome, Edge, Brave or Vivaldi, in a profile of its own, apart from yours. The Snap build of Chromium is not supported, and neither is Firefox. Choose the browser in Surogate's **Settings**, under **Browser** (**Agent's browser**). A change applies the next time the agent's browser starts.

You can take the browser over at any moment and hand it back. While you hold it, the agent waits.

To preview a web app the agent started, allow the port when Surogate asks.

## When the computer is away

If the computer is off, asleep or offline, a chat that needs it shows **Waiting for** and the computer's name. The work pauses. When the computer is back, it carries on. An operation that already ran is not run again.

Past 20 waiting chats, a new local operation fails at once with "Too many sessions are waiting for" the computer.

Quit the app and the computer goes away too. To keep it available, leave **Keep running when the window is closed** on in Settings (it keeps Surogate in the tray), and turn on **Start at login**.

## Devices

In the agent's web app, open **Settings** and the **Devices** tab. It shows only for an agent that lets chats work on folders of a computer.

- **Computers** lists each computer that can work on folders through this agent, with when it was added, reauthorized and last seen. **Revoke** stops it at once and cancels what it was doing. Its chats say **Local access revoked** until you restore the computer in Surogate on that computer.
- **Surogate Desktop sign-ins** lists each sign-in with **End**, which signs that Surogate Desktop out. You see the list only when your own sign-in to the web app is less than 10 minutes old; otherwise it asks you to sign in again.

When a computer is added or reauthorized, a banner in the web app says "`<computer>` can now work on folders of your computer through `<agent>`" for 7 days. **Review** opens the Devices tab. Dismissing the banner hides it in that browser only.

## Around the app

- **Tray.** The tray menu has **Show Surogate**, **Quick entry**, the computer's name, **Settings…** and **Quit Surogate**.
- **Quick entry.** A small window to start a new chat from anywhere. On Linux the shortcut is Ctrl+Alt+Space in an X11 session. In a Wayland session there is no shortcut: open it from the tray.
- **Notifications.** When Surogate's window is hidden or behind another app, it notifies you of new items in your inbox, of a chat that finished, and when it needs an answer ("Surogate is asking you something"). Clicking one opens that chat. A flood of them becomes one notice that opens the inbox.
- **Settings.** Appearance, **Start at login**, **Keep running when the window is closed**, **Developer mode**, your account, **This computer** (name, connection, sandbox), **Browser** and **Folders and permissions**. **Folders and permissions** lists each folder chats work on and each chat on it, with its mode, the sites it may reach, its use of the browser, the ports of its own servers the browser may open and its background processes. **Take back** withdraws an allowance and **Stop** ends a process.
- **Uninstall.** See the options under [Get it](#get-it).

## Limits and good to know

- **Company networks.** Programs in the sandbox use the system's certificates, which include your company's CA, but Java keeps its own store. Add the CA there yourself if the agent's Java programs need it. A proxy your computer must name is not used for the connection to Surogate: if that proxy is your only way out, the computer cannot be linked.

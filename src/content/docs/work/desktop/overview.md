---
title: Surogate Desktop
sidebar:
  label: Surogate Desktop
---

Surogate Desktop is an app for your computer. It lets your agent work on a folder you choose, use your own browser and show you the web apps it starts. You chat with the agent as usual. The agent still thinks in the cloud; the app is its hands on your machine. You watch it work and step in whenever you want.

## What you can do with it

- **Work on your real files.** Point a chat at a folder, and the agent reads, writes and organizes what is in it: documents, spreadsheets, code or data. No uploads and no syncing. The work happens where your files already are. See [Working on a folder](#working-on-a-folder).
- **Let it run commands, safely.** Builds, scripts, data processing, file conversions. The agent runs them in a sandbox on your computer, not on your computer itself.
- **Browse with your own browser.** The agent drives Chrome, Edge, Brave or Vivaldi, already installed on your computer, in a profile of its own. Downloads land in the chat's folder. Take the browser over at any moment, and hand it back when you are done. See [Your browser](#your-browser).
- **Preview what it builds.** When the agent starts a web app in its sandbox, it can open it in the browser for you to see, once you allow it.
- **Run several jobs at once.** A project is a coordinator chat that hands work to threads, each a chat of its own. Each thread works in its own copy of your folders, so threads never trip over each other. When a thread's turn ends, its changes land in your folder. If someone changed the same file meanwhile, the thread asks you. Press **Stop**, and the turn's changes are taken back. See [Projects](/work/desktop/projects/).

## Safe by design

- **Nothing runs directly on your computer.** Every command runs in a lightweight virtual machine that Surogate Desktop starts for you. A chat's folder joins it only while that chat is working, and files you protect stay read-only there.
- **The agent sees only what you give it.** The file tools see the chat's folder and nothing else of yours.
- **You decide what reaches the network.** Commands reach the package registries they need, and your computer's own services stay out of reach of both the commands and the browser. For any other site, your local network included, the agent asks you first. A chat can also be set to work freely (see [Approvals](#approvals)).
- **You stay in control of the browser.** In a chat that asks every time, you approve each download and each file the agent gives a page. Taking the browser over pauses the agent until you hand it back.
- **Signed updates.** Every release is signed, and your computer installs only releases signed by Surogate's key.

## Requirements

- Ubuntu 24.04 LTS or a later LTS release, on a 64-bit Intel or AMD computer.
- Hardware virtualization (Intel VT-x or AMD-V), turned on in the firmware settings. Without it Surogate Desktop still works, but runs the agent's commands several times slower.
- For browsing: Google Chrome, Microsoft Edge, Brave or Vivaldi. The Snap build of Chromium is not supported.
- A Surogate account.

Today Surogate Desktop is available for Linux. macOS and Windows builds aren't published yet.

## Install

Run:

```bash
curl -fsSL https://surogate.ai/desktop/install.sh | bash
```

The script asks for `sudo` once. Then open Surogate Desktop from your applications, [sign in](#sign-in) and start a chat on a folder (see [Working on a folder](#working-on-a-folder)).

Surogate Desktop keeps itself up to date. It checks for updates when it starts and every 6 hours. When one is ready, the sidebar says **Update available** and **Restart to update** installs it. An administrator on the computer has to approve the install. Without one, the sidebar says "An administrator needs to install this update."

Options go after `bash -s --`:

- `--version <x.y.z>` installs that release, to go back to an earlier one:

  ```bash
  curl -fsSL https://surogate.ai/desktop/install.sh | bash -s -- --version <x.y.z>
  ```

- `--uninstall` removes Surogate Desktop. It asks before it deletes your sign-in and the agent's browser profiles. Your folders are never touched.

  ```bash
  curl -fsSL https://surogate.ai/desktop/install.sh | bash -s -- --uninstall
  ```

### On a company network

If your network inspects TLS traffic, or your servers use a certificate authority of their own, give the installer your company's CA certificate (a PEM file) with `--ca-cert`. Give the file to `curl` as well:

```bash
curl --cacert company-ca.pem -fsSL https://surogate.ai/desktop/install.sh | bash -s -- --ca-cert company-ca.pem
```

Surogate Desktop, your Chrome, Edge and Brave, and the commands the agent runs then all trust it.

## Good to know

- **Free-working chats don't ask about files.** In a chat set to **Work freely**, a page's downloads are saved and the agent's uploads are made without a prompt. Set the chat to **Ask every time**, and you approve each one.
- **A project thread works without your secrets and build output.** A thread's copy of a folder leaves out `.env` files, dependency folders such as `node_modules/` and `.venv/`, build output, caches and editors' temporary files, and none of them lands from the thread either. For work that needs them, such as running the project's own install or tests that read its `.env`, use a chat on the folder.
- **Java does not trust your company's CA.** Programs in the sandbox use the system's certificates, which include it, but Java keeps its own. Add the CA to Java's store yourself if the agent's Java programs need it.
- **A proxy your computer must name is not used for the connection to Surogate.** The app's window goes through it. If that proxy is your only way out, the computer cannot be linked.
- **A site can open a preview you allowed.** A link or a redirect on another site can open your allowed preview in a tab, as any site can open any address. Nothing else from that site reaches your preview.

## If it asks you to reinstall

Rarely, an update or the installer stops with a message that ends "remove Surogate Desktop with --uninstall, and install it again". It means the files that check updates on your computer are not as an install leaves them. Do what it says:

```bash
curl -fsSL https://surogate.ai/desktop/install.sh | bash -s -- --uninstall
curl -fsSL https://surogate.ai/desktop/install.sh | bash
```

Your folders stay as they are.

## Sign in

The first time, the app asks for your agent's address (for example `https://agent.example.com`). Paste it and press **Connect**, then **Continue in your browser** and sign in there. The computer joins that one agent, so the app works with a single agent at a time.

Signing in adds the computer to the agent's list under [Settings > Devices](#devices).

## Working on a folder

Start a new chat in the app. When the agent lets chats work on folders of a computer and has **Multi session** on (see [Capabilities](/work/workflow/configure-agent/#capabilities)), the line under the composer says the chat works in a folder on this computer. **Choose another folder** and **Use the last folder** on that line switch between picking a folder and the one you used last. With **Multi session** off, no line is shown and the chat works in the cloud. If the agent can't use folders on this computer, the line says why and the chat works in the cloud.

When you send the first message, Surogate shows a sheet, **Work in** the folder, where you:

1. Check the folder, or press **Change…** to pick another.
2. Choose how it works: **Work freely** or **Ask every time** (see [Approvals](#approvals)).
3. Press **Use this folder**.

The agent sees only this folder, and its commands run in the sandbox (see [Safe by design](#safe-by-design)). The sheet also says that the files the agent reads and what its commands print go to the agent in the cloud and can stay in the conversation.

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

- **Network access.** Any site beyond the package registries, your local network included, asks (see [Safe by design](#safe-by-design)). **Allow** covers the connections waiting now; later ones ask again. **Allow all its ports for this chat** lets that site through on every port for the rest of the chat. In the browser's prompt, **Allow for this chat** does the same for the browser.
- **The browser.** The first time a chat uses your browser, and each time it would open a port of the chat's own web app in it.

In **Ask every time**, every action the agent takes on a page asks too: opening an address, running a script, clicking, typing, dragging, uploading a file, and downloads. Reading the page does not.

Switch the mode from the bar. Going to **Asks every time** is immediate. Going to **Works freely** opens Surogate Desktop's own confirmation, because only the app can make a chat less safe. An action's prompt also has **Allow and stop asking**, which allows that action and makes the chat work freely.

## Your browser

The agent's browser profile is apart from yours. Firefox is not supported. Choose the browser in Surogate's **Settings**, under **Browser** (**Agent's browser**). A change applies the next time the agent's browser starts.

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
- **Uninstall.** See `--uninstall` under [Install](#install).

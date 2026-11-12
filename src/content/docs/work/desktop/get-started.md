---
title: Get started with Surogate Desktop
sidebar:
  label: Get started
---

This page takes you from installing [Surogate Desktop](/work/desktop/overview/) to an agent working on a folder of your computer, then to a first project. It takes about ten minutes.

You need a Surogate agent that you can sign in to, and its address (for example `https://agent.example.com`). For the agent to work on your folders, its **Multi session** switch must be on, which is the default (see [Capabilities](/work/workflow/configure-agent/#capabilities)).

## 1. Install the app

On Ubuntu 24.04 LTS or later, run:

```bash
curl -fsSL https://surogate.ai/desktop/install.sh | bash
```

The script asks for `sudo` once. Then open **Surogate** from your applications.

:::note
Builds for macOS and Windows aren't published yet. See [Requirements](/work/desktop/overview/#requirements) for what each one will need.
:::

## 2. Connect to your agent

The first time it opens, the app shows **Connect to your agent**.

1. Paste your agent's address and press **Connect**.
2. Press **Continue in your browser**. Your browser opens the agent's sign-in page.
3. Sign in there, then come back to the app.

Your computer now belongs to that agent's list of computers. You can see it, and revoke it, in the agent's web app under [Settings > Devices](/work/desktop/overview/#devices).

## 3. Start a chat on a folder

1. Press **New** in the sidebar.
2. Check the line under the composer. It says that the chat works in a folder on this computer. If it offers **Choose another folder**, the chat would use the folder you used last: press it to pick a new one.
3. Type what you want done with the folder, for example "Sort these invoices into one folder per month and list the ones without a date", and send it.
4. Pick the folder when the app asks for it. Surogate then asks **Work in** that folder. Press **Change…** there to pick another.
5. Under **How it works in this folder**, choose **Work freely** or **Ask every time**. For a first try, choose **Ask every time**: you then see each command and each file change before it happens.
6. Press **Use this folder**.

The agent reads the folder and works on it. Its commands run in a sandbox on your computer, and the agent sees no other folder of yours. Some folders are refused, such as your home folder or a credentials folder (see [Folders that are refused](/work/desktop/overview/#folders-that-are-refused)).

## 4. Answer its requests

While the agent works, it asks you when it needs you:

- **In Ask every time**, each command and each file change waits for your answer. Reading files never asks.
- **In both modes**, a site beyond the package registries asks first, your local network included. So does the first use of your browser in a chat.

For a command or a file change, **Allow once** lets that one through, and **Deny** refuses it. **Allow and stop asking** lets it through and makes the chat work freely. For a site, **Allow** lets through the connections waiting now. The bar of the chat shows its mode, and you can change it there at any time (see [Approvals](/work/desktop/overview/#approvals)).

## 5. Let it use your browser

Ask for something on the web, for example "Download last month's statements from the supplier portal into this folder".

The agent opens your own Chrome, Edge, Brave or Vivaldi, in a profile of its own, apart from yours. Downloads land in the chat's folder.

To step in, for example to sign in to a site, press **Take over** in the chat. The agent pauses until you press **Hand back**. **Show browser** brings its window to the front.

To choose which browser it uses, open **Settings**, then **Browser**.

## 6. Start a project

A project is a coordinator chat that splits a larger goal into threads, each a chat of its own.

1. Press **Projects** in the sidebar, then **New project**.
2. Give it a **Name** and a **Goal**, for example "Prepare the quarterly report from the files in this folder".
3. Press **Choose…** to pick the project's folder, confirm it on the **Work in** sheet, then press **Create project**.
4. In the project's conversation, ask for the work. The coordinator answers with a card of proposed threads.
5. Press **Start** on the threads you want.
6. Press **Overview** in the project's header to follow the threads. Threads that need your answer are under **Waiting on you**. Open one and answer it there, in the thread.
7. When a thread's work is done, press **Resolve** on its row.

Each thread works in its own copy of the folder. When a thread's turn ends, its changes land in the folder. See [Projects in Surogate Desktop](/work/desktop/projects/) for the details.

## 7. Keep it available

The agent can only work on your folders while the app runs. If the computer sleeps or the app quits, the chats that need it wait and carry on when it is back.

- In **Settings**, leave **Keep running when the window is closed** on. The app then stays in the tray when you close its window.
- Turn on **Start at login** so that the app starts with your computer.
- Use **Quick entry** to start a chat from anywhere: press Ctrl+Alt+Space in an X11 session, or open it from the tray.

## Next steps

- [Surogate Desktop](/work/desktop/overview/): what the app can do, how it keeps your computer safe, and every setting.
- [Projects in Surogate Desktop](/work/desktop/projects/): the coordinator, its threads and the Overview panel.

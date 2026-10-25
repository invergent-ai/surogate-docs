---
title: Case types
---

The **Case types** page lists the project's case types: "Draw, check and publish this project's case types." Press a row to open that case type in the designer.

## The list

| Column | What it shows |
|---|---|
| **Case type** | The name, with the key under it. |
| **Version** | The current published version, such as `v3`. |
| **Published** | When the current version was published, and by whom; **Not published** for a case type only drafts hold. |
| **Open drafts** | The open drafts that change this case type. Each is a link that opens the designer in that draft. |
| **Running cases** | How many cases are open on each version, newest first, such as `41 on v3 · 2 on v2`; **None** when no case is open. |

A case type that exists only in a draft is listed too, under its key made readable. It opens in the newest draft that holds it.

## Create a case type

Editors and owners see **New case type** in the page header.

1. Press **New case type**.
2. Type a **Name**, such as `Loan request`.
3. Check the **Key** and the **Number prefix**. Both fill in from the name; change them if you need to.
   - The key identifies the case type. It is letters, digits, `-` and `_`, starting with a letter or a digit, and no other case type may have it.
   - The number prefix starts every case number, such as `LR-000001`. It is up to 32 letters, digits, `-` and `_`. Two case types of a project cannot share a prefix.
4. Pick the **Draft** to make it in: **A new draft**, or one of the open drafts. A new draft asks for a **Draft title**, which starts as `New case type: <name>`.
5. Press **Create**.

The new case type has one stage, **First stage**, with nothing in it, and no fields. The designer opens on it in the draft. Nothing published changes until the draft is published.

## The designer

The designer's header shows the case type's name and, under it, its published version: for example **Version 3 published 12 Oct 2026 · 41 cases running on it**, or **Not published yet**. In a draft, editors and owners also see **Dry run** and **Review and publish** on the right.

Under the header are a breadcrumb back to **Case types** and the [draft bar](/keel/builder/drafts/), then the designer's tabs:

| Tab | What it holds |
|---|---|
| **Workflow** | The stage board, each stage's flow, and the panel of the node you pick. See [Workflow](/keel/builder/workflow/). |
| **Data** | The case type's fields. See [Data](/keel/builder/data/). |
| **Forms** | The layout of each step's form and of the start form. See [Forms](/keel/builder/forms/). |
| **Scenarios** | Stored test cases that every dry run plays. See [Scenarios](/keel/builder/scenarios/). |
| **Connections** | The other systems its system steps call, and their credentials. See [Connections](/keel/builder/connections/). |
| **Settings** | Name, number prefix, calendar, service level, knowledge, intake agents, case events, title and summary. See [Case type settings](/keel/builder/case-type-settings/). |
| **Versions** | Every published version, and moving running cases. See [Versions](/keel/builder/versions/). |

The address of the page keeps the tab, the draft, and what is open on it, so you can copy a link to a node or a form and paste it to a colleague.

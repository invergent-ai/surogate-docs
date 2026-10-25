---
title: Drafts
---

Every change in Keel Builder is made in a **draft**. A draft holds changed copies of the project's definitions: case types, rules, calendars, queues, scenarios, connections and mappings of running cases. Nothing published changes until the draft is published. A project can have several open drafts at once.

## The draft bar

The designer, the **Rules** page and the **Queues** page show a draft bar under their header. It starts with a chip that says what you are looking at:

- **Version 4 · draft**: the version a draft would publish, in the designer;
- **Version 3**, or **Published**: the published definitions, with no draft open;
- **Draft: *title***, on the Rules and Queues pages.

Press the chip to open its menu:

- each open draft, by title, and **Published**: pick one to show it;
- **New draft…**: start another draft (editors and owners);
- **Discard this draft**: throw the open draft away (see below).

## Starting a draft

There are three ways:

- **New case type** makes a new draft for the case type, unless you pick an open one. See [Case types](/keel/builder/case-types/#create-a-case-type).
- **New draft…** in the draft bar's menu.
- Change something while **Published** is shown. Keel Builder asks for a draft first: the **Start a draft** dialog offers a **Title**, such as `Change Loan request`, `Change rules` or `Change queues`. Press **Start draft**, and your change is made in the new draft. Cancel, and the change is dropped.

## Saving

There is no save button. Each change is saved to the draft a moment after you make it. Beside the chip, the bar says:

- **Saving…** while a change is on its way;
- **Saved** once the draft has it;
- **Not saved:** and the reason, with **Try again**, when a save failed. Your change stays on screen until it is saved.

If the draft was published or discarded while you worked, the bar offers **Open another draft** instead of **Try again**.

While a change is not saved, the browser warns you before you close or reload the page.

## When someone else saves the same draft

Several builders can work in one draft. When someone else saved the draft since you opened it, a warning says: **This draft changed since you opened it. Each of your saves replaces the whole file as you have it.**

Each save replaces the whole file, such as the whole case type, so the last save of a file wins. Press **Load the latest** to read the draft again. If you have changes that are not saved yet, Keel Builder asks first, because loading drops them.

## Seeing what a draft changes

The **Review and publish** page lists, file by file, what the draft changes compared with what is published. See [Dry run and publish](/keel/builder/publish/).

When the published definitions changed after the draft started, because another draft was published, the dry run says **Main changed** and the review page offers **Update from main**.

## Discarding a draft

**Discard this draft** in the draft bar's menu asks **Discard *title*?**: "Its changes are lost. Nothing published changes." Press **Discard**.

The project's owners can discard any draft. An editor can discard a draft they created. A viewer cannot discard, even a draft they created while they were an editor.

## Who can do what

| | Viewer | Editor | Owner |
|---|---|---|---|
| See drafts and their files | Yes | Yes | Yes |
| Start a draft, change it, dry run it | No | Yes | Yes |
| Publish a draft | No | Yes | Yes |
| Discard a draft | No | Their own | Any |

---
title: Polls
description: Ask a page's readers one question at a time, and show the results as the poll says.
---

The portal's `poll` widget asks a question with two to ten answers. People signed in vote once each, and the results are shown as the poll says.

## Place a poll

```yaml
regions:
  aside:
    - id: question
      app: portal
      widget: poll
      preferences: { zone: Europe/Bucharest }
```

- `zone`: the time zone a poll's closing time is read in, such as `Europe/Bucharest` (when left out).

Each `poll` widget keeps polls of its own. Its polls belong to the widget: moving it to another page, or giving it another `id`, leaves them behind. A page with a poll is made for each reader and never kept in a cache.

## Open a poll

Those who [edit the page](/portal/sites/permissions/) see **New poll**. A poll has:

- a question of up to 300 characters;
- 2 to 10 answers, one a line, each up to 200 characters and each said once;
- when the results are shown: **Always**, **Once a person votes**, or **Once the poll closes**;
- when it closes, as a day and a time in the widget's time zone, within a year; left empty, it stays open until an editor closes it.

One poll is open at a time. Opening a new one while another is open asks the editor to tick that they know the open one closes; the closed one moves to **Past polls**. A poll cannot be changed once opened: close it and open another. Editors **Close the poll** at any time, and **Delete the poll** with its votes once they tick that they know it goes. A widget keeps at most 200 polls; delete old ones to open more.

When opening is refused, the widget says what was wrong and the form opens again with what was written, kept for a week.

## Vote

People signed in who may see the page choose an answer and **Vote**; while the poll is open, **Change my vote** replaces their answer. Visitors see the question and are asked to sign in. Once the poll closes, no vote is taken.

## Results

Results show each answer's votes and share. Until a poll says they may be seen, they are not in the page at all: a poll shown **Once a person votes** shows them to each person after they vote, and one shown **Once the poll closes** after it closes. Closed polls show their results to everyone, and editors always see them. No one sees who voted for what.

**Past polls** lists the 20 latest closed polls with their results.

## What happens to them later

When a person is erased from the portal, their votes stay counted, without them, and their drafts go. The answers they gave are part of what they get when they ask for their data.

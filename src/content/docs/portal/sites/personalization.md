---
title: Personalization
description: Group people into segments by who they are or how they visit, and show some blocks of a page, or a group of them, only to a segment.
---

A page can show different blocks to different people. A town hall shows "Pay your taxes online" to signed-in residents, a short welcome to everyone else, and an "Install the app" banner to visitors on phones. You do it in two steps: make **segments**, groups of people defined by rules, then choose who each block is shown to.

## Segments

In the console, **Segments** lists the tenant's segments and how many people with an account each holds now. **New segment** makes one:

- **Name**, in each language, and an **Id** (blocks name the segment by it).
- **Holds people who meet** **All the rules** or **Any of the rules**.
- **Rules**, one per row, each of a kind:
  - **Signed in**: signed in, or not signed in.
  - **In the group**: a group of the portal's, including groups a directory or SCIM keeps.
  - **Role**: administrators.
  - **In the organization**: an organization, which holds the people of every organization under it too.
  - **A field of theirs**: one of the [user fields](/portal/console/users/) *is*, *is not*, *contains* (text), *is more than* or *is less than* (numbers and dates), *is filled in* or *is empty*. Text is compared without regard to case.
  - **The page's language**.
  - **Their device**: a phone, a tablet or a computer. An iPad that asks for desktop sites counts as a computer.

The language and device rules hold for visitors who are not signed in too; every other rule needs a signed-in person. The count on **Segments** is of people with an account: exact, or "up to" and "at least" when a segment turns on the language or device of the page being shown.

A segment that blocks are shown to cannot be removed: change those blocks first.

## Show a block to a segment

In the page editor, open a block's row. **Show to** chooses:

- **Everyone who may see it**, by default;
- **Only these segments**: people in any of the segments ticked;
- **Everyone except these segments**.

A group of blocks works the same way, for all its blocks: this is how a page has variants. Put each variant in a group shown to its segment, and one more group shown to everyone except them. Someone in two segments sees both groups, so make segments that do not overlap when only one variant should show.

**Show to chooses what people are shown, not what they may see.** A block's text shown only to a segment is still the page's: what must stay hidden uses **Who sees this block** (see [Who sees and who edits](/portal/console/pages/#who-sees-and-who-edits)). Search never finds the text of a block shown only to some segments.

## Pages and caches

Pages for signed-in people are never kept by shared caches. For visitors, a page is kept as usual unless it shows a block to a segment with a device rule: then it is made for each visitor and never kept. A segment-only block on a busy public page with a device rule costs that page its place in the cache.

## Limits

- At most 100 segments, each with at most 20 rules; a block shown to at most 10 segments.
- Blocks shown to segments are for pages and page templates, not for the blocks people add to their own dashboards. On a dashboard, a person arranges a block shown to segments only when it is shown to them.
- The count on **Segments** reads up to 50,000 people; past that it says "at least".

---
title: Personalization
description: Group people into segments by who they are, the pages they visited or how they visit, and show some blocks of a page, or a group of them, only to a segment.
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
  - **Pages they visited**: a page of a site that remembers pages, or any page under it (the home page `/` counts alone), at least so many times in the last so many days (up to 395). See [Remembered pages](#remembered-pages).
  - **The page's language**.
  - **Their device**: a phone, a tablet or a computer. An iPad that asks for desktop sites counts as a computer.

The language and device rules hold for visitors who are not signed in too; every other rule needs a signed-in person. The count on **Segments** is of people with an account: exact, or "up to" and "at least" when a segment turns on the language or device of the page being shown, or on the pages people visited.

A segment that blocks are shown to cannot be removed: change those blocks first.

## Show a block to a segment

In the page editor, open a block's row. **Show to** chooses:

- **Everyone who may see it**, by default;
- **Only these segments**: people in any of the segments ticked;
- **Everyone except these segments**.

A group of blocks works the same way, for all its blocks: this is how a page has variants. Put each variant in a group shown to its segment, and one more group shown to everyone except them. Someone in two segments sees both groups, so make segments that do not overlap when only one variant should show.

**Show to chooses what people are shown, not what they may see.** A block's text shown only to a segment is still the page's: what must stay hidden uses **Who sees this block** (see [Who sees and who edits](/portal/console/pages/#who-sees-and-who-edits)). Search never finds the text of a block shown only to some segments.

## Remembered pages

A site remembers the pages signed-in people visit only when you turn it on: in **Sites**, open the site, and under **Personalization** tick **Remember the pages signed-in people visit**. Then:

- Each page a signed-in person opens is counted once per view, per day, by the page's own path: the home page by its path, an entry by the display page that shows it. Visitors who are not signed in are never remembered, nor an administrator seeing the portal as someone.
- Days are counted by calendar day in UTC: "the last 1 day" is since midnight UTC.
- What is kept is kept 13 months, then removed. Turning the setting off removes what the site kept as soon as the change is live. A site's pages that a segment's **Pages they visited** rule names cannot stop remembering until that rule is changed or removed.
- A segment's **Pages they visited** rule can then use it.

**Tell your people.** Remembering pages is personal data: say so in your privacy notice. Each person sees the pages kept of the last 30 days on their account page (**My account**, **Pages you visited**), clears them, or stops sites remembering theirs; stopping removes what was kept at once. A person's data export lists the pages kept, and erasing them removes them.

An administrator sees a person's segments and the pages they visited on the person's page under **Users**: **Profile**, **Show the profile**. Each look is kept in the audit log.

## Recommended pages

On a site that remembers pages, place **Recommended pages** in the page editor (in the portal's widgets): a short list of the site's pages a person may want next, titled **Recommended for you** unless you write another **Title**, with up to 10 **Pages shown** (5 by default).

- For a signed-in person who lets sites remember their pages: the pages that other people who visited the same pages also visited, leaving out those the person visited; then the site's most visited pages.
- For anyone else, including someone seeing the portal as a person: the site's most visited pages, the same for every visitor.
- Only pages the person may see, never a personal dashboard, a page that shows entries, or the page they are on. Entries themselves are not recommended.
- **Privacy.** A page is recommended only when at least five other people visited it in the last 30 days, and a site recommends nothing until twenty people's pages are remembered. On a site where anyone can make an account, someone making several accounts could still learn a little about what others visit: weigh that before placing it there.
- The list shows nothing until there is enough to recommend.

## Pages and caches

Pages for signed-in people are never kept by shared caches. For visitors, a page is kept as usual unless it shows a block to a segment with a device rule: then it is made for each visitor and never kept. A segment-only block on a busy public page with a device rule costs that page its place in the cache.

## Limits

- At most 100 segments, each with at most 20 rules; a block shown to at most 10 segments.
- Blocks shown to segments are for pages and page templates, not for the blocks people add to their own dashboards. On a dashboard, a person arranges a block shown to segments only when it is shown to them.
- The count on **Segments** reads up to 50,000 people; past that it says "at least".

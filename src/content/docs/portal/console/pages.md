---
title: Pages
description: Build a site's pages in the console, with its page tree and an editor for each page's title, address, layout and content.
---

**Pages** builds the portal's sites in the console. It shows each site's pages as a tree. For each page you set its title, its address and its layout, and arrange what each part of the layout holds. Every save is a [version](/portal/console/versions/) you can undo.

**Pages** is for administrators, and for the people who hold a right over some page, on a portal whose site files the portal keeps. It is not in the menu otherwise. See [Who may add, move and remove pages](#who-may-add-move-and-remove-pages). A new site, and a site's name, languages and home page, are made on [Sites](/portal/console/sites/).

The **Menus** tab builds the site's [menus](/portal/sites/menus/); the **Fragments** and **Page templates** tabs hold what pages share.

## The page tree

Each site lists its pages by address. A page sits under the page above it: `/servicii/taxe` under `/servicii`. The home page is marked **Home page**. A page file the portal cannot read is marked **Cannot be read**; fix or remove it where the site's files are edited.

- **Edit** opens a page in the editor.
- **New page** opens the editor for a new page of that site. The one on a page's row makes a page under it, with its address already begun.
- A page published on a schedule shows where it stands: **Scheduled** with the time, **Published until** with the time, **Published** or **Expired**. A page with no schedule shows nothing.

![The page tree of a site: the home page, a page scheduled for 01.12.2026 08:00, a page with pages under it, and a page marked Expired.](../../../../assets/screenshots/portal-pages-tree.png)

## Edit a page

- **Address**: where the page is, such as `/despre`. The site's home page keeps its address. Changing another page's address asks first: links to the old address stop working, and settings made on the page itself start again. When the page holds a widget people write in, the question adds that what they wrote stays at the old address, and the page no longer shows it.
- **Title**: one per language of the site.
- **Layout**: the portal's `one-column` or `two-column`, or one of the site's own [layouts](/portal/sites/layouts/).

**Search and sharing** sets how [search engines and link previews](/portal/sites/seo/) show the page: a description in each language, [keywords](#keywords), a share image, and **Hide from search engines**.

The page's **Settings** also hold [who sees, edits, adds, moves and removes](#who-sees-and-who-edits), when the page is [published](#publish-on-a-schedule), and whether it is in the site's [main menu](/portal/sites/menus/#show-a-page-in-the-menu).

Under them, each part of the layout lists what it holds, in order:

- **Add text** adds a text block, one text for each of the site's languages. See [Write text](#write-text).
- **Add content…** shows the site's [content](/portal/console/content/#show-content-on-a-page) of one type: its newest entries, or one entry.
- **Add a widget…** adds one of [the portal's own widgets](#the-portals-widgets) or one of the apps' widgets. A portal widget has its settings in its row. When an app's widget needs a setting to work, the editor asks for it; the app's widget has its other settings on the page itself, from its menu.
- **Add tabs** adds [tabs](#tabs).
- **Remove** takes a block or widget off the page.

**Save** stays off until something changed and every title, every text and every required setting is filled in.

## Who sees and who edits

Who sees and who edits a page, and who sees each block, are chosen with the picker described in [Choose who](/portal/sites/permissions/#choose-who). **Add…** opens the choices, and **Remove** takes one away.

- **Who sees this page**, on the page's **Settings** tab. By default it is **Whoever sees the site**. It says: "It only narrows who sees the site." It offers no **Everyone**: a page cannot be wider than its site.
- **Who edits this page**, on the same tab. By default it is **The site's editors**. It says: "In addition to the site's editors."
- **Who sees this block**, in each block's row. By default it is **Whoever sees the page**. It says: "It only narrows who sees the page, or the group the block is in." People who may not see a block get the page without it.

Removing the last one chosen under **Who sees this page** or **Who sees this block** leaves **Only editors and administrators**, never more people. **Back to the default** returns to the default on purpose.

**Show to**, in each block's row, shows the block only to some [segments](/portal/sites/personalization/), or to everyone except them. It chooses what people are shown, not what they may see.

**Experiment**, in each block's row, makes the block (or group) one version of an [experiment](/portal/sites/experiments/): choose the experiment, then its **Version**. The block is shown only to the people who see that version. An experiment whose goal is this page is not offered.

## Publish on a schedule

A page can be published from a time, until a time, or both. On the page's **Settings**, **Publication** has **Published from** and **Published until**. Both are optional, to the minute, and typed in Bucharest's time, whatever the time zone of your computer. The portal keeps them in UTC.

![The Publication part of a page's settings: Published from 12/01/2026, 08:00 AM, and Published until left empty.](../../../../assets/screenshots/portal-pages-publication.png)

Outside the time it is published, a page is nothing to the people who do not edit it:

- its address answers **page not found**, not "no access";
- it is in no [menu](/portal/sites/menus/), no `sitemap.xml`, no search of the site, and no list's link to its entries;
- the people who edit the page, and the administrators, still see it, with a band that says when it is published or that it expired.

The change happens by itself, within a minute of the time, with no save and no job to set up. A cache that keeps pages for visitors is told to keep them no longer than the next change.

Some rules keep it safe:

- **The home page cannot be scheduled**: the site would be left without one. The save is refused with the reason, and so is making a scheduled page the site's home page on [Sites](/portal/console/sites/).
- **Published until** must be later than **Published from**. A time that has already passed is allowed for **Published until**: the page is expired as soon as it is saved, and the editor says so before you save.
- A time that does not exist, such as 03:30 on the night the clocks go forward, is refused at the field.
- Pages under a page do not take its schedule. Each page has its own; when a page has expired, its item and the items under it leave the menu.
- A form placed on a page that has expired still opens at its own address.
- **Preview** shows the page whatever its schedule.

## Keywords

**Search and sharing** has **Keywords** for each language of the site. Type a word and press **Enter** or a comma; each word has a button to remove it.

![The Search and sharing tab of a page: description in each language, Keywords in each language as tags (medical waste, reporting, guide; deșeuri medicale, raportare, ghid), and the share image.](../../../../assets/screenshots/portal-pages-keywords.png)

- At most 20 words in a language, each 1 to 50 characters, with no `<`, `>` or `"`. The same word typed twice, in capitals or not, is kept once.
- Once there are keywords in one language, there must be some in each of the site's languages, as for the description.
- The page's head carries them in the visitor's language: `<meta name="keywords" content="medical waste, reporting, guide">`. A page with none of its own takes the site's, set on [Sites](/portal/console/sites/) under **Search engines**.
- A page hidden from search engines keeps its keywords, and says it is not to be listed.

## Tabs

**Add tabs** adds a container of tabs to a part of the page, or to a group. It starts with two tabs.

![The page editor with a Tabs container: three tabs, each with its label in two languages, who sees it, and its own blocks; the third tab is for the platform's administrators only.](../../../../assets/screenshots/portal-pages-tabs-editor.png)

- Each tab has a **label** in each language, 40 characters at most, and its own blocks: text, content, a widget, a form, a listing, a group, as anywhere else on the page. Blocks move into a tab as they move between parts of the page.
- A container has from 2 to 12 tabs. **Add tab**, **Move the tab up**, **Move the tab down** and **Remove** change them.
- **Who sees the tab** uses the usual choice of people, and the container has its own **Who sees this block**. A tab nobody may see is not in the page at all, its label included.
- Tabs inside tabs are not allowed: the editor does not offer them, and a file that has them is refused. Tabs can be in a group, and a tab can hold a group, within the four levels groups may nest.
- A page people arrange for themselves cannot hold tabs.

What visitors get is a set of tabs you can use from the keyboard:

![A page with tabs as a signed-in supplier sees it: two tabs, Reports to validate and County situation; the third, for administrators, is not there.](../../../../assets/screenshots/portal-pages-tabs-site.png)

- The arrow keys move among the tabs and **Enter** or **Space** opens the one in focus. The first tab a person may see is open at first.
- The open tab is in the address (`#tab-…`), so a link or a refresh opens the same tab. An address that names a tab the person cannot see, or that is not there, opens the first.
- A tab that is not open is hidden, not removed: a form in it keeps what was typed, and a list in it works when the tab is opened.
- When only one tab is left for a person, its content shows with no tab bar. When none is left, the container is not there.
- Without scripts, the tabs are sections one after another, each with its label as a heading.
- On a narrow screen the tabs scroll sideways.

## Who may add, move and remove pages

Seeing a page and editing it are not the only rights. Three more are chosen with the same [people picker](/portal/sites/permissions/#choose-who), on a page's **Settings**:

![A page's Settings: Who sees this page, Who edits this page, Who adds pages under this page, Who moves this page and Who removes this page, each with "Only administrators, unless the site says otherwise."](../../../../assets/screenshots/portal-pages-rights.png)

- **Who adds pages under this page**: they make pages whose address is this page's address and more, such as `/dsp/instructions` under `/dsp`. It covers the pages under it that name nobody of their own.
- **Who moves this page**: they change its address, which puts it under another page.
- **Who removes this page**: they remove it. The pages under it stay where they are.
- **Who edits this page** now means the page's content and its properties: titles, layout, search and sharing, publication, keywords, tabs and its place in the menu.

A site has the same three choices for all its pages, on [Sites](/portal/console/sites/#who-may-add-move-and-remove-pages), the first one covering the first level too. They are **Only administrators** when left alone. A page can give more than the site, for its own pages: "the DSP staff add pages under `/dsp`". The nearest page above a place that names anybody decides; if none does, the site does.

How the rights work together:

- **Moving** a page needs the right to move it, and the right to add pages under the place it goes to, or on the first level.
- The home page is moved and removed by administrators only.
- A save is checked as a whole, against the rights of the person who makes it. A change outside them refuses the whole save, naming the page and the right missing: "You may not move the page /dsp/b". Nothing is half done.
- **Only administrators** change who sees, edits, adds, moves and removes a page, and who sees a block or a tab on it. Others see the choices and cannot change them, so nobody gives themselves a right. A block moved out of a tab only some people see, or a tab given up its restriction, would show to more people: such a save is refused. A block added to a restricted tab is as restricted as the tab. **Versions** and undoing a version stay with administrators too.
- The page editor offers someone only the forms they may send and the data models they may read. A form or a data model they may not use is refused on the page, naming it; those the page already uses stay as they are.
- A chat block, an assistant or a website chat, gives the agent to everyone who sees the page. Someone puts there only an agent they already reach, through a page they see; any other agent is refused, naming it.
- Someone who may only move or remove a page sees its address and title in the page editor, and nothing of what is on it: no blocks, no rights and no preview. Moving it changes its address and nothing else.

**Pages** is in the menu of every person who holds at least one of these rights over at least one page. They see the pages they hold a right on, and, greyed and with no action, the pages above them. **Edit**, **New page** (under a page), **Remove page** and the address field are there only where the person holds that right.

![The Pages screen of a person who is not an administrator: the DSP dashboard with its two pages under it, Edit and New page only where they hold the right, and no Menus, Fragments or Page templates.](../../../../assets/screenshots/portal-pages-editor-view.png)

## Write text

A text block's text is written as in a word processor. Select text, then use the toolbar above it:

- **Bold**, **Italic**, **Underline**, **Strikethrough** and **Code**.
- **Heading 2**, **Heading 3** and **Heading 4**, and **Paragraph** for ordinary text. The page's title is its only top heading.
- **Bulleted list**, **Numbered list**, **Quote**, **Code block** and **Horizontal line**.
- **Link** puts a link on the selected text. Type its **Address**:
  - a page of the site, such as `/despre`;
  - a web address (`https://` is added when you leave it out);
  - an email address or a phone number, which mails or calls.
  
  Tick **Open in a new tab** when it should. Addresses the portal does not take, such as the console's own, are refused with the reason.
- **Remove link**, **Undo** and **Redo**.

![A text block open in the page editor: the toolbar above its text, "Cine suntem" as a heading and two paragraphs; beside it, the page as visitors see it.](../../../../assets/screenshots/portal-rich-text.png)

**Edit as HTML** shows the text's HTML, for those who want it. It holds what an [HTML block](/portal/sites/layouts/#an-html-block) may hold.

A text written with markup the editor cannot keep, such as a class, a table or a picture, opens as HTML, with a note. It stays HTML, so nothing written by hand is ever rewritten. The same editor writes [fragments](#fragments) and content's [rich text](/portal/console/content/#write-an-entry).

## The portal's widgets

The portal has widgets of its own, such as a listing, a poll or a calendar. The page editor places each one and sets it in a form. No file needs to be written by hand.

### Add one

1. In the part of the page where it goes, press **Add…**, then **Add a widget…**.
2. Under **The portal's**, choose the widget. It is added to that part of the page, or to that group. The apps' widgets are in a group of their own.
3. Open its row. Its settings are there.
4. Set what you need, then **Save**.

A setting the widget cannot work without, such as the **Data model** of a **Listing**, must be filled in before you can save.

![The page editor with a Poll opened: its Time zone, Europe/Bucharest, and its Classes; beside it, the page as visitors see it.](../../../../assets/screenshots/portal-widget-poll-set.png)

### When one cannot be added

A widget the portal cannot serve is listed, but you cannot choose it. The list says why:

- **needs Keel**: the portal is not connected to [Keel](/portal/sites/keel/#connect-keel). This holds for **My work** and **Work overview**.
- **needs a DMS**: the portal is not connected to a [DMS](/portal/sites/documents/#connect-the-dms). This holds for **Documents** and **Document**.
- **needs an agent**: no agent fits yet. See [Assistants](/portal/sites/assistants/#connect-your-agents) for naming agents. This holds for **Assistant** and **Website chat**.
- **one per page**: the page has a **Website chat** already. A page holds one, in any part or group.

### The widgets

Each widget has a page in the guide. It says what people see and what each setting does.

- **Listing** shows a data model's records as a table. See [Listings](/portal/sites/listings/#place-a-listing).
- **Figures** shows a model's figures as tiles and bars. See [KPIs](/portal/sites/kpis/#show-them).
- **My work** shows each person the work Keel holds for them. See [Keel](/portal/sites/keel/#my-work).
- **Work overview** shows the headline figures of a Keel project. See [Keel](/portal/sites/keel/#the-overview).
- **Notifications** shows each person's notifications. See [Notifications](/portal/sites/notifications/#where-people-find-them).
- **Comments** and **Rating** let people signed in comment and give stars. See [Comments and ratings](/portal/sites/comments/#place-the-widgets).
- **Activity** shows posts, comments and published entries. See [Activity](/portal/sites/activity/#what-people-see).
- **Blog** shows the posts of one blog type. See [Show a blog](/portal/sites/blogs/#show-a-blog).
- **Blogs** shows the newest posts of several sites and libraries. See [Show several blogs](/portal/sites/blogs/#show-several-blogs).
- **Bloggers** lists who blogged lately. See [Recent bloggers](/portal/sites/blogs/#recent-bloggers).
- **Forum** is a board of topics, or of questions and answers. See [Forums and Q&A](/portal/sites/forums/#place-a-forum).
- **Wiki** is a wiki, or a knowledge base. See [Wikis and knowledge bases](/portal/sites/wiki/#place-a-wiki).
- **Calendar** is a calendar of events. See [Calendars](/portal/sites/calendar/#what-people-see).
- **Announcements** shows what a site's editors want people to know. See [Announcements](/portal/sites/announcements/#what-people-see).
- **Poll** asks readers one question at a time. See [Place a poll](/portal/sites/polls/#place-a-poll).
- **Documents** shows the documents of a DMS folder. See [Show a folder](/portal/sites/documents/#show-a-folder).
- **Document** shows one DMS document and its versions. See [Show one document](/portal/sites/documents/#show-one-document).
- **Assistant** is a chat with one of your agents, for people signed in. See [Assistants](/portal/sites/assistants/#connect-your-agents).
- **Website chat** is a chat with an agent for any visitor. See [A chat for visitors](/portal/sites/assistants/#a-chat-for-visitors).

### Settings

![A Calendar opened in the page editor: Who adds events, The page's editors, with the note that they always may; Time zone; View, Month.](../../../../assets/screenshots/portal-widget-calendar-set.png)

- A setting left at its default is not saved with the page. The widget uses the portal's default.
- A setting that names something, such as a data model or an agent, is a list of what the portal has. A setting that asks for several things, such as **Columns**, uses its default when you tick none. The row says what that default is.
- **Assistant** warns that **Who sees this block** is who may chat with the agent and use what it can do. Set it with that in mind.
- A portal widget the console has no settings for says **Set in the site's files**. The editor keeps it as it is written.

### Remove one

**Remove** asks first when the widget is one that people write in: **Comments**, **Rating**, **Activity**, **Forum**, **Wiki**, **Calendar** or **Poll**. What people wrote stays in the portal, but no page shows it.

- A **Poll**, **Calendar**, **Wiki**, **Forum** or **Activity** widget keeps what people wrote in it for itself. A new one starts empty. It never shows what was written in one you removed.
- **Comments** and **Rating** belong to the page, or to the entry it shows, not to the widget. Put them back on the page, and what people wrote shows again.

### When a widget's setting is refused

When a save is refused because of a widget's setting, the problem is listed above the page. Press it to open the widget. The problem also shows at the setting itself. Nothing is saved until every problem is fixed.

## Move what a page holds

Drag a block or widget by its handle onto another one to put it before it, or onto **Drop here** to put it at the end of a part. With the keyboard, use **Move up**, **Move down**, or **Move to** to send it to the end of another part.

When you choose a layout without one of the page's parts, what that part held moves to `main`, and the editor says so.

## Fragments

A fragment is text kept once and shown on many pages, such as opening hours or a contact box. Change it once, and every page that holds it changes.

Each site lists its fragments under its pages. **New fragment** asks for:
- an id, such as `program`: lower-case letters, digits and hyphens, fixed once saved;
- a name and the text in each of the site's languages, written as a page's [text](#write-text).

**Edit** changes a fragment. In the page editor, **Add a fragment…** places one in a part of the page. It shows as **Fragment:** and its name, with nothing to fill in.

**Remove** takes a fragment off the site. When pages or templates still hold it, the confirmation names them, and the removal is refused until the fragment is taken off them.

## Page templates

A page template is a page's starting point: a layout and what its parts hold.

- **Save as template**, in the page editor, keeps the page's layout and blocks as a template. It asks for an id and a name in each language. The page's address and titles stay with the page.
- When you make a **New page**, **Start from** offers the site's templates.
- **Remove** takes a template off the site; pages made from it keep what they hold.

## Search

**Add a search box** puts the site's search in a part of the page: a box, and the results below it. See [Search](/portal/sites/search/) for what it finds and for whom.

## Forms

**Add a form** puts one of the portal's forms in a part of the page; it offers the forms the site offers, at most five on a page. People who may not send the form do not see it. See [Forms](/portal/sites/forms/) for writing a form and saying who sends it.

## Display pages

A display page shows one entry at a time: each published entry of a content type gets its own address, the page's address followed by the entry's. A display page at `/stire` shows the entry `program-de-iarna` at `/stire/program-de-iarna`.

1. Make a page, such as `/stire`, and choose a type under **One entry at a time**, **Shows one entry of**. Choose a type *from* a library to show that library's entries.
2. Under **Add content…** in a part of the page, choose **The entry shown here**. It shows the whole entry. To show one field alone, such as its image in a wide part, choose it under **Part of the entry**.
3. Add anything else the page needs, such as a list of the newest entries beside it.

What visitors see:
- The page takes the entry's title, in their language or else in the site's main one. Search engines and link previews see the entry's address, title and first image.
- The page's own address shows nothing: only the entries' addresses do. In the page tree it shows as `/stire/…`.
- A draft, or an address no entry has, shows the site's "page not found".
- Lists of the type on the site link each entry's title to its address.
- If a page of the site has the same address as an entry, visitors see the page.

The home page and personal dashboards cannot be display pages, and a site has one display page per type and library. Choosing **No entries** removes the parts that showed the entry; choosing another type shows those parts as the whole entry. **Save as template** leaves them out, since a template shows no type of entries. **Preview** shows a display page with the newest published entry.

Apps on a display page are told the page's address, not which entry it shows.

## Personal dashboards

A page can be a personal dashboard: each person signed in arranges it for themselves. Under **Personal dashboard** in the editor, tick **People arrange this page for themselves**, then tick what they may add: the apps' widgets that need no settings, and the site's fragments.

A dashboard is only for people signed in. If the page was open to everyone, ticking the box lets only people signed in see it.

On the page, people see **Customize this page**. There they can:
- move a section up or down, or to another part of the page;
- remove a section;
- add one of the sections the page offers;
- go back to the page as it is made.

Each person's changes are theirs alone. A section you add to the page later shows for everyone, where you put it. A section you take off the page goes from everyone's dashboard. A person holds at most 30 sections.

Sections on a dashboard have no menu on the page itself: set their settings here, in the editor. An administrator seeing the portal as someone sees that person's dashboard but cannot change it.

## Preview before saving

**Preview** shows the page as it is being edited, before anything is saved, as visitors would see it. Choose **Phone**, **Tablet** or **Desktop** to see it at that width, and the language to see it in. Press **Preview** again after more changes.

Only the portal's administrators can open a preview, and only for a quarter of an hour. A preview shows only what anyone may see, and is never shown to search engines. An app that is not live yet shows as waiting.

When the page cannot be shown as it is, the editor lists what is wrong, as it does when a save is refused.

## When a save is refused

- **Problems**: the save would break the site, so nothing is saved. The editor lists what is wrong. Pressing a problem in a [widget's setting](#when-a-widgets-setting-is-refused) opens the widget.
- **Someone saved this site meanwhile**: another administrator saved first. **Load the newest** shows the page as it is now. Your changes to it are lost, so the editor asks first.

**Remove page** takes the page off the site, after asking. The home page cannot be removed. Undo the version on [Versions](/portal/console/versions/) to bring a page back.

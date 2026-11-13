---
title: Blogs
description: Let the people a site names write their own posts, and show them as a blog, an aggregator of several blogs, and a list of who blogged lately.
---

A blog is a [content type](/portal/sites/content-types/) whose entries are posts. Each post is written by one person, who is its author, and its date is the day it was first published. The people a site names as its bloggers write their own posts in the console; three widgets show them on pages.

## What people see

A blog page lists the newest posts. Each shows its title, linked to the post's own page, its author and its date, and a short text under it. Beside it, the recent bloggers: who first published posts lately, and how many posts each.

![A blog page: the posts "How to file the request online" and "What we learned from the autumn fair", each with its author, its date and a short text, and in the side column the recent blogger with 2 posts.](../../../../assets/screenshots/portal-blog-journal.png)

A post has a page of its own, with its author, its date and its text:

![A post's own page: its title as the heading, the author and the date above the text, and a link back to all posts.](../../../../assets/screenshots/portal-blog-post.png)

## Name the bloggers

A site, or a [library](/portal/sites/content-types/#libraries), names its bloggers under `permissions.blog`, as it names its [editors](/portal/sites/permissions/#bloggers): see the [config example](#the-bloggers).

Bloggers find **Content** in the console, with the site's blog types alone:

![The console's Content page filtered to the Journal type: two published posts, each with Edit.](../../../../assets/screenshots/portal-blog-console.png)

There they write, publish, unpublish and delete their own posts, and bring back an earlier version of them; they never see or change anyone else's posts or any other content. The site's editors see and change every post. A post is published as soon as its blogger publishes it: there is no review before it shows. Name as bloggers the people you trust to speak on the site.

Someone who stops being a blogger, or a type that stops being a blog, leaves the posts where they are: they stay published, with their author, and the site's editors look after them.

## Make a blog type

Mark a content type with `blog: true`: see the [config example](#a-blog-type).

A blog type's template may place two values a post has besides its fields: `_author`, the author's name, and `_published`, the day it was first published. Give the type a [display page](/portal/sites/content-types/#display-pages) on each site that shows its posts, so each post has its own address.

The author of a post is the person who created it. Marking an existing type `blog: true` makes whoever created its entries their authors, administrators included. A post whose author was erased from the portal has no author.

The console's content type builder keeps `blog: true` as the file says it; set it in the file.

## Show a blog

The portal's `blog` widget shows a blog type's posts: see the [config example](#a-blog-on-a-page).

Each post shows its title, linked to its own page, its author with their [handle](/portal/console/users/#handle), and its date; the summary and the image show in the page's language when the field has one. A post published again keeps its first date and its place.

A blog lists a post only when its site has a display page for its type that the viewer may see: without one, the blog shows nothing.

Add `?author=` and a handle to the page's address, such as `/blog?author=ana.pop`, to show one author's posts; every blog on that page then shows only theirs, with a link back to all posts. A handle nobody has shows no posts.

## Show several blogs

The `blogs` widget shows the newest posts of several sites and libraries together (see the [config example](#several-blogs)).

A post shows only when its site has a display page for its type that the viewer may see; it links to that page, on its own site's address, and says which site it is on. A post nobody may see from here is left out, and so are the posts of a site with no address of its own.

## Recent bloggers

The `bloggers` widget lists who first published posts lately, the latest first, with how many posts each (see the [config example](#who-blogged-lately)).

Each name leads to the blog page of the widget's `page`, with that person's posts. Pick a blog of the same type and site as the posts counted, or a name may lead to an empty list.

It counts only posts the viewer may see, and lists only people whose account is active.

## Who sees what

A blog shows the same posts to everyone who may see its page, and may be kept in a cache like any other page; a post published, unpublished or deleted shows at once. The `blogs` and `bloggers` widgets depend on who is looking, so a page with either is made for each person. Comments, ratings and the [activity](/portal/sites/activity/) work on posts as on any entry; the activity names a post's author.

## Config example

### A blog type

In the content type's file (`content/types/<id>.yaml`):

```yaml
name: { ro: Jurnal, en: Journal }
title: title
blog: true
fields:
  - { id: title, type: text, label: { ro: Titlu, en: Title }, required: true }
  - { id: intro, type: textarea, label: { ro: Pe scurt, en: In short } }
  - { id: cover, type: image, label: { ro: Imagine, en: Image } }
  - { id: body, type: richtext, label: { ro: Text, en: Text } }
template: |
  <article>
    <h2><portal-field name="title"></portal-field></h2>
    <p><portal-field name="_author"></portal-field> · <portal-field name="_published"></portal-field></p>
    <portal-field name="body"></portal-field>
  </article>
```

- `blog: true` makes the type a blog.
- `template` places the fields, and the two values only a blog post has: `_author` and `_published`.

### The bloggers

In `site.yaml`, or in a library's file (`content/libraries/<id>.yaml`):

```yaml
permissions:
  edit: [group:Redactori]
  blog: [group:Angajati]
```

- `edit`: the site's editors, who see and change every post.
- `blog`: the bloggers, who write their own posts.

### A blog on a page

In a page's file (`sites/<site>/pages/<page>.yaml`):

```yaml
regions:
  main:
    - id: blog
      app: portal
      widget: blog
      preferences: { type: journal, limit: 10, summary: intro }
```

- `type`: the blog type whose posts it shows.
- `library`: a library this site may show, to show the library's posts rather than the site's own.
- `limit`: how many posts it shows, newest first (1 to 50; 10 when left out).
- `summary`: a text or textarea field of the type, shown under each post.
- `image`: an image field of the type.

### Several blogs

In a region of a page's file:

```yaml
- id: all-blogs
  app: portal
  widget: blogs
  preferences: { from: [main, intranet, "@stiri"], limit: 20 }
```

- `from`: the sites, and the libraries this site may show (as `@` and their id), whose posts it reads: 20 at most; this site when left out.
- `limit`: how many posts it shows (1 to 50; 10 when left out).

### Who blogged lately

In a region of a page's file:

```yaml
- id: bloggers
  app: portal
  widget: bloggers
  preferences: { from: [main], days: 30, limit: 10, page: /blog }
```

- `from` and `limit` as for `blogs`.
- `days`: how far back it looks (1 to 365; 30 when left out).
- `page`: a page of this site holding a `blog` widget; each name leads to that page with the person's posts.

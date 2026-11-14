---
title: Blogs
description: A content type marked as a blog, the people who may blog, and the widgets that show posts.
---

The configuration behind [Blogs](/portal/sites/blogs/). That page covers what people see, how bloggers write, and what each widget shows.

## A blog type

Mark a content type with `blog: true`. The console's content type builder keeps `blog: true` as the file says it; set it in the file.

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

## The bloggers

A site, or a [library](/portal/sites/content-types/#libraries), names its bloggers under `permissions.blog`, as it names its [editors](/portal/sites/permissions/#bloggers).

In `site.yaml`, or in a library's file (`content/libraries/<id>.yaml`):

```yaml
permissions:
  edit: [group:Redactori]
  blog: [group:Angajati]
```

- `edit`: the site's editors, who see and change every post.
- `blog`: the bloggers, who write their own posts.

## A blog on a page

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

## Several blogs

In a region of a page's file:

```yaml
- id: all-blogs
  app: portal
  widget: blogs
  preferences: { from: [main, intranet, "@stiri"], limit: 20 }
```

- `from`: the sites, and the libraries this site may show (as `@` and their id), whose posts it reads: 20 at most; this site when left out.
- `limit`: how many posts it shows (1 to 50; 10 when left out).

## Who blogged lately

In a region of a page's file:

```yaml
- id: bloggers
  app: portal
  widget: bloggers
  preferences: { from: [main], days: 30, limit: 10, page: /blog }
```

- `from` and `limit` as for `blogs`.
- `days`: how far back it looks (1 to 365; 30 when left out).
- `page`: a page of this site holding a `blog` widget; each name leads to that page with the person's posts. Pick a blog of the same type and site as the posts counted, or a name may lead to an empty list.

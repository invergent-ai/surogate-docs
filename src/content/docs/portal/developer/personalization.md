---
title: Personalization
description: Segments in segments/<id>.yaml, sites that remember pages, and a placement's audience, as the site's configuration writes them.
---

What these do is on [Personalization](/portal/sites/personalization/).

## A segment's file

```yaml
# segments/residents.yaml
name: { ro: Rezidenți, en: Residents }
match: any
rules:
  - group: Cetățeni
  - field: { key: city, is: equals, value: Cluj }
```

- `match` is `all` (when left out) or `any`; `rules` 1 to 20, each one key:
  - `signedIn: true | false`
  - `group: <name>`, `role: administrator`, `organization: <A/B>` (members of A/B and of everything under it)
  - `field: { key, is, value }`: `is` is `equals`, `not`, `contains` (text, email, phone), `above`, `below` (number, date), `set`, `unset` (no `value`); `value` is of the field's type (`YYYY-MM-DD` for dates)
  - `visited: { site, path, views, days }`: the page `path` of `site`, or any page under it, visited at least `views` times (1 to 1000, 1 when left out) in the last `days` (1 to 395, 30 when left out)
  - `language: ro | en`
  - `device: mobile | tablet | desktop`
- At most 100 segments. A field rule names a field of `users/fields.yaml`.

## A site that remembers pages

```yaml
# sites/main/site.yaml
personalization: { history: true }
```

A `visited` rule names a site with `history: true` and one of its pages' paths.

## A placement's audience

```yaml
regions:
  main:
    - id: taxes
      app: portal
      widget: group
      audience: { segments: [residents] }
      blocks: [...]
    - id: welcome
      app: portal
      widget: group
      audience: { segments: [residents], except: true }
      blocks: [...]
```

- `segments`: 1 to 10 segment ids; `except: true` shows the placement to viewers in none of them.
- Pages and page templates only. A group's audience and its blocks' own both apply.

## Load checks

- A segment's problems are `segment` with a reason: `name`, `match`, `rules`, `rule`, `unknown_field`, `visited_site` (no such site), `visited_history_off` (the site does not remember pages), `visited_page` (no such page on it).
- A placement naming a segment that does not exist: `unknown_segment`. More than 100 segments: `too_many_segments`.

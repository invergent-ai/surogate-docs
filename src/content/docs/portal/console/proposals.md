---
title: Proposed changes
description: Changes to the sites that wait for an administrator, who reads them, previews them, and approves or rejects them.
---

Changes that do not come from the portal's administrators never go straight to the sites. The portal's AI and the people helped by it **propose** a change instead. It waits under **Proposed changes** until an administrator reads it, opens its preview, and approves or rejects it. **Proposed changes** is for administrators, on a portal whose site files the portal keeps.

## What may be proposed

A proposal changes what the sites are built from:

- pages, layouts and a site's design;
- forms, flows, values, data models, endpoints, jobs and guides;
- content types, vocabularies and collections.

A site's own settings never are. Neither are its addresses and who may edit it, connectors, apps, agents, the links to other products, user fields, or file folders. Those stay with the portal's administrators and developers.

## The list

Waiting proposals come first, then the latest decided: **Published**, **Rejected** or **Withdrawn**. Each shows its title, how many files it changes, and when it was proposed.

## Read a proposal

Open a proposal to see:

- **What it is for:** its title and description.
- **Each file it changes,** with the lines it removes and adds. A file it adds shows every line as added; a file it removes, every line as removed.
- **Whether it would break the site.** It was checked as a save is. A proposal that would break the site lists why, and cannot be approved.
- **What to look at closely.** The page lists the files that change:
  - who a job runs as;
  - who reaches a page, a form or an endpoint;
  - who may see or change something;
  - what is called, emailed or asked outside the portal.

## Preview a proposal

**Make a preview** makes a [preview environment](/portal/sites/previews/) of the sites with the change in. Nothing of the change runs before you ask. **Open the preview** opens it, with fake people only. A preview stays seven days, or until the proposal is decided. A portal has at most ten previews at once, its developers' included.

## Approve or reject

- **Approve and publish:**
  - The change is saved as a [version](/portal/console/versions/), with the proposal's title, and goes live.
  - You cannot approve a change you proposed yourself: someone else does.
  - **Stale proposals:** if the sites changed the same files since the proposal was made, it cannot be approved. Reject it, and ask for it again.
  - If other files changed, the proposal is published on top of them.
- **Reject:** write why. Nothing is changed, and the one who proposed it reads your note.

Whoever proposed a change may withdraw it while it waits. Each proposer has at most five proposals waiting, and the portal twenty.

## For agents and developers

An agent proposes through the portal's API, with a token holding **Propose changes** (`proposals`), given by name only:

1. `GET /_portal/api/proposals/base` gives the newest version and the files a proposal may change.
2. `POST /_portal/api/proposals` with `title`, an optional `description`, `baseVersion` and `changes`: each file's new text, or `null` to remove it.
3. `GET /_portal/api/proposals/<id>` shows where it stands, the note included.

A token proposes and withdraws; it never approves, whatever else it holds.

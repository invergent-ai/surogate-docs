---
title: Check a site
description: One command tells you whether a site's files, its apps, its permissions and its pages work, and how the pages changed since last time.
---

`portal check` tells you whether a site works before anyone sees it. It checks the files and the apps they name, then, on a portal, renders every page in a browser. Run it until it passes: a coding agent can do the same. Its report is made to go into the pull request.

## Check the files and the apps

```sh
portal check ./portal-config
```

- Every file is checked against its schema, with the file and the field for each problem.
- Every app's manifest is read from the app, as the portal reads it when it syncs. Every widget a page places, and its preferences, must be one the app has. An app that cannot be reached is named, and everything else is still checked.
- `--offline` checks the files alone and asks no app.

## Permission sanity

- A widget that runs in the browser hands its preferences to every visitor. A preference that looks like a secret there fails the check: an API key, a token or a private key. It is shown masked in the report. A preference whose name only suggests a secret is a warning.
- A grant that can never apply is a warning:
  - a page or a placement that lets everyone view it, under a site or page that does not;
  - a person named on a placement whom the page's list of people leaves out.
- Groups and organizations may share people, so they never give a warning.
- When the pages are rendered, a page your files make public must open for a visitor who is not signed in. A page they restrict must ask that visitor to sign in.

## Types and code

```sh
portal check ./portal-config --types my-app=../my-app/src/portal-types.ts --typecheck ../my-app
```

- `--types` fails when an app's generated types are not its manifest's: write them again with `portal apps types`.
- `--typecheck` type-checks a project, such as an app's code against its types.

## Check on a portal

```sh
portal check ./portal-config --start --render
portal check ./portal-config --url http://localhost:8080 --yes --render
```

- `--start` checks on a throwaway portal of its own, which approves every app. It needs Docker, and the portal image that [Develop locally](/portal/sites/develop-locally/#test-against-a-throwaway-portal) describes.
- `--url` checks on your [local portal](/portal/sites/develop-locally/). The check replaces that portal's site files with yours, so it asks for `--yes`.
- The portal syncs your files and checks what only a portal can, such as the apps' hook modules. On your own portal, the check also reports apps waiting for [approval](/portal/console/apps/), and people, groups or organizations your files name that the portal does not have.

## Render every page

With `--render`, every page of every site is opened in a headless Chrome, in each of the site's languages:

- A full-page screenshot is taken. `--mask <css selector>` blanks parts that change on every run, such as a clock.
- Accessibility is checked with axe, against WCAG 2.1 AA. Serious and critical problems fail the check. Each problem says whether it is in the portal's own markup or in an app's widget, so you know whose it is.
- A widget that failed to load fails the check, with the reason when the portal is in dev mode. So does a widget whose script never ran, or a request to an app that failed.
- `--sign-in <email>` also views the pages as that person, reading the password from standard input. On `--start`, `--sign-in admin` uses the throwaway portal's administrator, who also sees the editing menus.
- `--lighthouse` adds each page's performance score. It is advisory unless you set `--min-performance` (0 to 1).
- `--pages <pattern>` checks only some pages, such as `main/servicii`.

## Compare with the previous run

- Each screenshot is compared with the previous run's, kept in `.portal-check/baseline`. A page fails when more than half a percent of its pixels changed (`--max-diff` sets the share), or when its size changed.
- After a change you meant, run again with `--update-baseline`. Commit the baseline folder to compare each change with what was merged.

## The report

- Each run writes `.portal-check/latest`: a `report.md` with a row per page (its accessibility, its performance, how much it changed, and links to its screenshot and diff), `report.json`, and the images.
- `--summary <file>` adds the report, without links, to a file such as a CI job's summary. Upload `.portal-check/latest` as the job's artifact so reviewers can open the images.
- The check ends with 0 when it passes and 1 when it fails. It ends with 2 when it could not run, such as with no Chrome, no Docker, or a portal not in dev mode.

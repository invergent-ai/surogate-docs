---
title: For developers
description: The site's configuration as files, for version control and CI, over the same settings the console edits.
---

Everything about a site can be set in the console. Developers have a second path: the same configuration, as files in a folder. You keep the folder under version control, review changes in pull requests, and push it from CI. Both paths edit the same thing. A change saved in the console shows up in the files at the next pull, and a pushed change shows up in the console.

The pages in this section are the reference for those files: one page per feature, with examples and what each key does. Each links back to the user guide page that says what the feature does for people.

Some features have no console screen yet. Their user guide page says so, and links to the page here.

## The files

The portal keeps every site's files itself. Each saved change, from the console or from a push, becomes a [version](/portal/console/versions/) an administrator can open, compare and undo.

A config folder holds one file per thing, in YAML. A few of them:

| File | What it holds |
| --- | --- |
| `sites/<site>/site.yaml` | a site: its name, languages, home page, and who may see and edit it |
| `sites/<site>/pages/<page>.yaml` | a page: its title, layout and what each part holds |
| `sites/<site>/layouts/`, `fragments/`, `templates/` | the site's own [layouts](/portal/developer/layouts/), [fragments and page templates](/portal/developer/layouts/#a-fragment) |
| `sites/<site>/design/` | the site's [look](/portal/developer/design/) |
| `apps/<id>.yaml` | an [app](/portal/developer/apps/) the portal shows |
| `forms/<id>.yaml` | a [form](/portal/developer/forms/) |
| `connectors/<id>.yaml` | a [connector](/portal/developer/connectors/) to another service |
| `flows/`, `values/`, `contracts/` | [logic flows](/portal/developer/flows/) and [named values](/portal/developer/values/) |
| `models/<id>.yaml` | a [data model](/portal/developer/data-models/) |
| `endpoints/<id>.yaml`, `jobs/<id>.yaml` | [endpoints](/portal/developer/endpoints/) and [jobs](/portal/developer/jobs/) |
| `content/` | [content types](/portal/developer/content-types/), vocabularies, libraries, collections and [folders](/portal/developer/files/) |
| `agents.yaml`, `keel.yaml`, `dms.yaml` | the [agents](/portal/developer/assistants/), [Keel](/portal/developer/keel/) and the [DMS](/portal/developer/documents/) |
| `environments.yaml` | the [environments](/portal/developer/environments/) this portal sends versions to |

`portal schema --out <dir>` writes the JSON Schema of every file, for your editor.

## Pull and push

The [command line](/portal/developer/command-line/) moves the files between a folder and the portal, with a [token](/portal/console/tokens/) of your own:

1. `portal config pull ./portal-config` writes the site's newest files into the folder. The token needs **Read users, groups and settings**.
2. Change the files, and [check them](/portal/developer/check-a-site/) with `portal check ./portal-config`.
3. `portal config push ./portal-config -m "<what changed>"` saves the folder as the site's next version. The token needs **Change users, groups and settings**.

- A push that would break the site saves nothing. It lists each file and field to fix: "Nothing was saved: the files would break the site."
- If someone saved the site since your pull, from the console or another push, the push is refused: "The site was changed since these files were pulled." Pull again, make your change on the newer files, and push.
- A file you pulled and then removed from the folder is removed from the site.
- From CI, `--onto-latest` saves the folder over the newest version without a pull first. The folder is then the whole site, whatever was saved since.
- Each push is a version, with your message, on the [Versions](/portal/console/versions/) page. Undo it there like any other change.

## Other ways in

- **On your own machine**, [develop locally](/portal/developer/develop-locally/): a portal in dev mode takes the folder at every save.
- **Before anyone sees it**, make a [preview](/portal/developer/previews/): the portal from a folder or a version, with fake people only.
- **For an administrator to approve**, propose the change: it waits under [Proposed changes](/portal/console/proposals/). [Coding agents](/portal/developer/agents/) work this way.
- **From one portal to another**, such as from Test to Production, send a version to [another environment](/portal/sites/environments/).

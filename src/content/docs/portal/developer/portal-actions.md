---
title: Portal administration actions
description: The createPage, updatePage, deletePage, loadPage, createSite, updateSite, deleteSite, loadSite, addBlock, updateBlock, removeBlock, loadBlockHtml, createFolder, setFolderAccess, deleteFolder, role and setPersonRoles actions, as the site's configuration writes them.
---

What they do, who may run them, and their limits are on [Administering the portal from actions](/portal/sites/portal-actions/). Every key marked as an expression is CEL; sites, folders and roles named in a literal key are written as ids.

```yaml
actions:
  - type: createPage
    site: primaria
    path: '"/raportari/" + slice(now, 0, 4)'
    title: { ro: '"Raportări"', en: '"Reports"' }   # a language to an expression
    template: "'raportare-anuala'"                  # optional
    layout: "'one-column'"                          # optional, without a template
    whoSees: '["signed-in"]'                        # optional lists of principals
    whoEdits: '["group:Registratura"]'
    into: pagina                                    # {site, path}
  - type: updatePage
    site: primaria
    path: "'/despre'"
    title: { en: "'About us'" }                     # only the languages given change
    description: "'Despre noi'"
    newPath: "'/noi'"
  - type: deletePage
    site: primaria
    path: "'/vechi'"
  - type: loadPage
    site: primaria
    path: "'/'"
    into: p       # {site, path, title, layout, description, keywords, parts, whoSees, updatedAt}
  - type: createSite
    name: { ro: "'DSP Cluj'", en: "'DSP Cluj'" }
    host: "'portal.gov.ro'"
    path: "'/dsp-cluj'"                             # optional
    locales: "['ro', 'en']"                         # optional
    whoSees: "['signed-in']"                        # optional
    copyFrom: "'dsp-model'"                         # optional
    into: site    # {site, url}
  - type: updateSite     # site; name, locales, home, whoSees, whoEdits, description
  - type: deleteSite
    site: dsp-vechi
  - type: loadSite
    site: primaria
    into: s       # {id, name, url, languages, defaultLanguage, home, whoSees, pages}
  - type: addBlock
    site: primaria
    page: "'/raportari/2027'"
    kind: text                  # text | widget | form | fragment
    text: { ro: "'<p>…</p>'" }  # for text; widget + settings; form; fragment
    position: end               # start | end | after (with after: "'block-id'")
    region: "'main'"            # optional: a part of the layout
    into: bloc    # {blockId}
  - type: updateBlock    # site, page, block; settings, text, whoSees
  - type: removeBlock    # site, page, block
  - type: loadBlockHtml  # site, page, block, locale; keeps {html, text}
  - type: createFolder
    id: "'arhiva-2027'"
    name: { ro: "'Arhivă'", en: "'Archive'" }
    visibility: secure          # public | secure
    whoSees: "['group:Registratura']"
    ifExists: use               # error | use
  - type: setFolderAccess
    folder: "'arhiva-2027'"
    view: "['group:Registratura']"
    viewMode: remove            # replace | add | remove
    public: false
  - type: deleteFolder
    folder: "'arhiva-2027'"
  - type: setPersonRoles
    email: "'ana@primaria.ro'"
    give: "['administrator']"
    take: "[]"
  - type: createRole     # id, name, description, rights; also updateRole and deleteRole (key role)
```

- Keys written as expressions (`path`, `folder`, `block`, `role`, `email`, lists) are worked out at run time, so a run can name what an earlier step made; `site` is a literal id.
- The changes are made on a working copy of the configuration's files, each checked as a save is, and written as one version at the end of a run that did not fail (`portal.via: action` in the version's data). A site's database rows (its address) are made just before the files are saved and undone if they cannot be.
- A job with these actions needs `runAs` an administrator and must not start from anything but time; neither is allowed in a form anyone may send. The load actions may run anywhere.

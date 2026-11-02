# Surogate DMS User Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task by task, inline. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a user guide for Surogate DMS to https://docs.surogate.ai, for end users and administrators who use the product through its web interface: a welcome page, concepts, a quickstart for staff, a quickstart for administrators, three worked examples, the daily-work, Archive and Administration pages, and reference pages, with English, light-theme screenshots taken in a demo city hall.

**Architecture:** Surogate DMS becomes the site's third product, beside Surogate Agents and Keel, with its own `starlight-sidebar-topics` topic (`dms`, link `/dms/`) and its own sidebar. The product is added to `src/lib/product.mjs`, so the header, the mobile menu, the sidebar head and the breadcrumb pick it up; the home page gets a third product card and a third column of tasks. Pages live under `src/content/docs/dms/`, screenshots under `src/assets/screenshots/dms-*.png` (1600x900 PNG, referenced as in the Keel guide). The screenshots come from a capture script kept outside the repository, run against a demo installation filled with the dataset this plan defines.

**Tech Stack:** Astro 7.3 + `@astrojs/starlight` 0.42, `starlight-sidebar-topics` 0.9, `starlight-links-validator`, `starlight-llms-txt`, the repo's two rehype plugins (figure captions from alt text, lead paragraph), `node --test` for unit tests, Python `unittest` for checks on the built `dist/`. Capture: Playwright-core with `/usr/bin/google-chrome`, outside the repo.

**Sources:**

- This site: `astro.config.mjs`, `src/lib/product.mjs`, `src/components/{Header,Sidebar,MobileMenuFooter,PageTitle}.astro`, `src/components/home/*`, `src/components/brand/*`, `src/content/docs/index.mdx`, `tests/*.py`, `migration/assert_content.py`, the spec `docs/superpowers/specs/2026-10-26-docs-site-redesign-design.md` (square corners, 1 px frame on screenshots, captions from alt text, light screenshots in both themes, lead of at most 250 characters).
- The model for voice and structure: the Keel guide, `src/content/docs/keel/` (`index.md`, `concepts.md`, `quickstart.md`, `quickstart-business.md`, `examples/mortgage-pre-approval.md`, `business/sign-in.md`, `reference/roles.md`, `reference/faq.md`, `reference/glossary.md`).
- Source material for what the DMS does (read, never copied): `/home/administrator/work/flavius/dms-slices/regwt/docs/user-guide/` and `docs/admin-guide/`, at DMS commit `8e2d611` (equal to `origin/main` on 2026-11-02).
- The real screens and their English labels: `/home/administrator/work/flavius/dms-slices/regwt/frontend/src` (`app/router.tsx`, `app/routes/*.tsx`, `app/shell/nav.ts`, `app/shell/user-bar.tsx`, `features/*`, `i18n/en.ts`, `i18n/labels.ts`). `en.ts` is the authority for every label; the DMS's own guides are behind it in places (they still print Romanian labels for the Archive pages that the English UI translates).

## Decisions for the owner

Each has a recommendation; the plan is written to the recommendation.

1. **Capture installation.** A fresh, empty DMS installation for the docs, at the current main, holding only the demo dataset. The alternative, PROD `dms.surogate.ai` (the Example Bank organisation), already holds test documents that would show in Library, Search and My desk screenshots. Recommend the fresh installation.
2. **Demo institution.** A fictional city hall, "Example City Hall", because the Archive features (nomenclator, selection, handover to the National Archives) are made for public institutions. Keel's guide uses "Example Bank". Recommend the city hall.
3. **Romanian terms the English UI keeps.** The English UI says dosar, nomenclator, indicativ, proces-verbal (Procese-verbale) and Arhivele Naționale. The guide uses them as the UI does, explains each on the Concepts page and in the Glossary, and gives no Romanian labels in parentheses. Recommend yes.
4. **Features an operator turns on.** The online editor, filing proposals, AI mode and time stamps show only when the installation has them. Release 1 needs only the online editor and the internal certificate authority; filing proposals, AI mode and time stamps are captured for release 2. Recommend this split.
5. **Keel integration and API integration pages.** They are for an IT team (connections, keys, subscriptions, the OpenAPI download). Leave them out of the guide; the FAQ says they exist and who uses them. Recommend leave out.
6. **The deleted state of a selection.** A scheduled deletion runs after a fixed delay of seven days. Capture the scheduled state in the main session and the **Deleted documents** tab in a short pass seven days later. Recommend the later pass.
7. **The DMS mark.** A placeholder until a real logo exists, drawn like the Keel mark: a white page with a folded corner and three text bars, on a `#9b1f61` square (the palette's link colour in the light theme). Recommend yes.
8. **Home page.** Three product cards in one row, a third column of five DMS tasks, the heading "Three products, built to work together." and the tagline "Guides, tutorials and reference for Surogate Agents, Keel and Surogate DMS." Recommend yes.
9. **No fixed address.** Each institution has its own DMS address, so the guide says "the address your administrator gave you" and never names `dms.surogate.ai`. Recommend yes.
10. **Release split.** Release 1: 32 pages and 104 screenshots. Release 2: 7 pages (Filing proposals, Reception, Integrity and procese-verbale, Archival copies and time stamps, Reports, Alerts, Electronic signatures) and the remaining screenshots. Recommend this split.

## Global Constraints (voice and rules)

- **Voice: the Keel guide's.** Second person, present tense, short numbered steps, one action per step. UI labels in bold, exactly as the English UI shows them (capitalisation, articles and punctuation from `i18n/en.ts`), for example **Add a person**, **Upload a document**, **Remember me on this computer**, **Close the dosar**. Messages the UI prints are quoted in plain quotes. Tables for "who sees what" and for messages with what to do. Links between pages are absolute site paths with a trailing slash, as in the Keel guide (`/dms/work/search/`).
- **The lead.** Every page opens with one short paragraph of at most 250 characters that says who the page is for and what it covers; `rehype-lead` makes it the lead. No heading, image or list comes before it.
- **Screenshots.** Referenced as `![caption](../../../assets/screenshots/dms-<id>.png)` from `dms/*.md` and with one more `../` from `dms/<group>/*.md`. The alt text is a full-sentence caption naming what the picture shows (it becomes the visible `<figcaption>`), without a trailing period, as the Keel captions are. Only English, light-theme screenshots; no dark UI, no Romanian UI. Every screenshot is a full 1600x900 window.
- **The demo note.** The two quickstarts, the examples and the welcome page say once: "The pictures were taken in a demo city hall, Example City Hall, with made-up people and documents."
- **Nothing invented.** Every statement about the product is traceable to a screen or to a page of the DMS user or administrator guide, and agrees with `en.ts`. Where the DMS's guides say a feature is not available (registers and registration numbers, approval workflows, deleting a single document, sending or sharing by e-mail or link, following a document, e-mail notifications, editing `.doc`/`.xls`/`.ppt`/`.odt` files, two people editing at once, scanning and barcodes), the guide never implies it; the FAQ lists them once.
- **No installation, deployment or internals.** Nothing about installing, deploying, clusters, configuration settings (`DMS_*`), the worker and its jobs, migrations and upgrades, the database, the search index, the audit chain's hashing, checkpoints' cryptography, package formats (BagIt, E-ARK), converters (veraPDF, the editor's product name), API and integration internals (webhooks, keys' wire format, headers, OpenAPI), limits and timings that exist only in code. When a screen depends on something an operator sets up, the guide says "ask your administrator" or "when your institution has it", and goes no further.
- **Roles by their UI names:** **Archive administrator**, **Electronic archivist**, **Standard user**, **Auditor**, **Data protection officer (DPO)**, **Access to special data**, and **Integration** (named only in the roles reference, as the role of connected systems). Permissions by their UI sentences, such as "Uploads documents", "Approves", "Manages people". "Administrator" in prose means a person whose role gives Administration pages.
- **Plain copy.** No em dashes, no slogans, no "simply" or "just", no icon-card grids, no counts the UI does not show (do not write "seven roles" or "eleven report models"; list them). Dates and numbers in the demo's English format, as the screenshots show them.
- **Front matter** as the Keel pages: `title` and `sidebar.label`, nothing else; no body H1 (the structural check in `migration/assert_content.py` enforces it).

## Review Focus

The failure modes the plan's tests will not catch, and where the plan checks them by hand:

- **Romanian in a screenshot.** The English UI keeps a few Romanian words on purpose (dosar, nomenclator, indicativ, Procese-verbale, Arhivele Naționale), but some text that reaches the screen comes from the server and may stay Romanian: an alert's sentence, a proces-verbal's PDF, a server message that has no English translation, the headers of the Excel templates. The capture script rejects any Romanian navigation label (Task 4), and Task 10 opens every image; a screenshot that shows Romanian beyond those five terms is retaken or dropped. Never screenshot a proces-verbal PDF or an Excel template.
- **A page that names a feature the UI does not have.** The DMS's own guides are partly stale and partly ahead of the product. Task 22 checks each page's claims against the screens and `en.ts`, and against the "Not available yet" lists of both DMS guides.
- **A leaked internal detail.** The denylist test catches words such as `DMS_`, OpenSearch or webhook; it does not catch a paraphrase ("a background job retries five times", "the check runs at 02:00"). Task 22 reads the Archive and Administration pages for paraphrased internals.
- **A label that differs from the UI.** "Add person" for **Add a person**, "Remember me" for **Remember me on this computer**, "Email" for **Email address**, "Waiting for 1 signatures" for "Waiting for one signature". Task 22 runs a label audit against `en.ts` (a script outside the repo) and reviews every miss.
- **A screenshot taken with more rights than the page's reader has.** An administrator's sidebar shows Archive and Administration; a staff page must use a staff account's screenshot. Each shot below names its account.
- **A broken anchor or a link to a page that moved.** `starlight-links-validator` fails the build for in-site links and anchors. Links to the home page tasks are tested. Anchors that a heading rename breaks show up only at build time: run the build after every content task.
- **Header crowding.** A third product link in the nav bar may crowd it between 800 and 1100 px wide. Task 23 checks the header at 820, 1024 and 1280 px and on a phone, in both themes.
- **Product drift.** The DMS ships often. The capture records the DMS commit it ran against (Task 5), the PR names it, and labels are audited against `en.ts` at that commit.

---

## A. Information architecture

### The topic

Added to `starlightSidebarTopics([...])` in `astro.config.mjs`, after `keel`:

```js
{
  id: 'dms',
  label: 'Surogate DMS',
  link: '/dms/',
  items: [
    'dms',
    'dms/concepts',
    'dms/quickstart',
    'dms/quickstart-admin',
    {
      label: 'Examples',
      collapsed: true,
      items: ['dms/examples/contract', 'dms/examples/new-department', 'dms/examples/selection-and-handover'],
    },
    {
      label: 'Daily work',
      collapsed: true,
      items: [
        'dms/work/sign-in',
        'dms/work/my-desk',
        'dms/work/library',
        'dms/work/upload',
        'dms/work/document-page',
        'dms/work/versions',
        'dms/work/lifecycle',
        'dms/work/search',
        'dms/work/comments',
        'dms/work/signing',
        'dms/work/favorites-and-collections',
        'dms/work/to-review',
        'dms/work/personal-data',
      ],
    },
    {
      label: 'Archive',
      collapsed: true,
      items: [
        'dms/archive/overview',
        'dms/archive/reception',
        'dms/archive/integrity',
        'dms/archive/preservation',
        'dms/archive/selection',
        'dms/archive/handover',
        'dms/archive/reports',
        'dms/archive/alerts',
      ],
    },
    {
      label: 'Administration',
      collapsed: true,
      items: [
        'dms/admin/org-chart',
        'dms/admin/people',
        'dms/admin/roles',
        'dms/admin/document-types',
        'dms/admin/folders',
        'dms/admin/nomenclator',
        'dms/admin/signatures',
        'dms/admin/audit-log',
      ],
    },
    {
      label: 'Reference',
      collapsed: true,
      items: ['dms/reference/roles', 'dms/reference/glossary', 'dms/reference/faq'],
    },
  ],
},
```

The groups follow the DMS's own sidebar (its sections are "Documents", "Bring in", "Archive" and "Administration"); "Daily work" holds the first three. Each content task adds only its own pages to `items`, in this order, because the build fails on a slug that has no page. Release 2 pages (marked R2 below) are added by Task 24.

### The pages

39 pages. "R1" is the first release, "R2" the second. Audience: **U** end user, **A** administrator (including archivists, auditors and the data protection officer), **B** both. Sources are DMS guide files (`ug/` user guide, `ag/` admin guide). Screenshots are ids from section C.

**Top level**

1. `dms/index.md`: title "Surogate DMS", label "Welcome". **B**, R1. What the DMS is for (an institution's documents, from upload to the archive), who uses which part (staff, archivists, administrators, auditors, the DPO), a "Start here" table as in Keel's welcome, how a document moves through it, where to go next. Sources: `ug/README.md`, `ag/README.md`, `ug/layout-and-navigation.md`. Shots: `dms-desk-staff`, `dms-archive-overview`.
2. `dms/concepts.md`: title "Surogate DMS concepts", label "Concepts". **B**, R1. Documents and versions; folders: library folders, user folders, dosare (a library folder with a nomenclator entry) and virtual folders; document types and metadata; units, positions, roles and grants; the five states (Draft, Validated, Approved, Published, Archived); retention: the nomenclator, entries, editions, terms, permanent and temporary; reception and archival copies in one paragraph each; selection and handover; personal data. Each term links to its page and to the Glossary. Sources: `ug/glossary.md`, `ug/folders-and-dosare.md`, `ug/lifecycle.md`, `ug/access-and-sharing.md`, `ag/roles-and-grants.md`, `ag/nomenclator.md`. Shots: `dms-library-folder`, `dms-org-chart`, `dms-nomenclator-in-force`, `dms-roles-grants`.
3. `dms/quickstart.md`: title "Surogate DMS quickstart", label "Quickstart for staff". **U**, R1. About ten minutes as Ioana Dobre: sign in; find your way; open the Library and the dosar Building permits 2026; upload a document with its type; fill in its metadata; validate it; find it with Search; mark it a favorite; mention a colleague in a comment; ask him to sign; see his signature. Sources: `ug/signing-in.md`, `ug/my-desk.md`, `ug/library-and-finding-documents.md`, `ug/uploading-documents.md`, `ug/the-document-page.md`, `ug/search.md`, `ug/comments-and-notifications.md`, `ug/signing-documents.md`, `ug/favorites.md`. Shots: `dms-sign-in`, `dms-shell-staff`, `dms-library`, `dms-library-folder`, `dms-upload-dialog`, `dms-doc-page`, `dms-doc-metadata-edit`, `dms-lifecycle-card`, `dms-search-results`, `dms-favorites`, `dms-comments-mention`, `dms-sign-request`, `dms-notifications`, `dms-to-sign`, `dms-sign-internal`, `dms-signatures-tab`.
4. `dms/quickstart-admin.md`: title "Surogate DMS quickstart for administrators", label "Quickstart for administrators". **A**, R1. The first things to set up, in the order the DMS needs them: sign in (the operator made you the first administrator); the org chart (unit types, units, positions); people, and who holds each position; the nomenclator (import the approved edition, choose the unit of each compartment, put it in force); folders and dosare; document types; roles and grants; the personal-data categories and purposes; the alert rules' working hours; then check as a staff member and read the audit log. Sources: `ag/first-start.md` (UI steps only), `ag/organization.md`, `ag/people.md`, `ag/nomenclator.md`, `ag/folders-administration.md`, `ag/document-types.md`, `ag/roles-and-grants.md`, `ag/personal-data.md`, `ag/anomaly-alerts.md`, `ag/audit-log.md`. Shots: `dms-sign-in`, `dms-desk-first-admin`, `dms-org-unit-types`, `dms-people-add`, `dms-org-holder`, `dms-org-chart`, `dms-nomenclator-empty`, `dms-nomenclator-force`, `dms-nomenclator-in-force`, `dms-folders-new-root`, `dms-dosar-entry`, `dms-types-contract`, `dms-roles-grant`, `dms-alerts-rules`, `dms-audit-entries`.

**Examples** (group "Examples")

5. `dms/examples/contract.md`: title "Example: file and approve a contract", label "File and approve a contract". **U**, R1. Radu Florea, contracts clerk in the Legal Department, files the street-lighting maintenance contract in Contracts 2026, fills in its metadata, attaches its technical annex, validates it and asks Mihai Stan, the Secretary General, to sign; Mihai signs internally, approves and publishes it. Explains why there is no approval workflow: the states and the signing request carry it. Sources: `ug/uploading-documents.md`, `ug/document-types-and-metadata.md`, `ug/links-and-duplicates.md`, `ug/lifecycle.md`, `ug/signing-documents.md`. Shots: `dms-ex-contract-upload`, `dms-ex-contract-metadata`, `dms-doc-attachments`, `dms-ex-contract-validated`, `dms-notifications`, `dms-sign-internal`, `dms-lifecycle-approve`, `dms-ex-contract-published`.
6. `dms/examples/new-department.md`: title "Example: set up a new department", label "Set up a new department". **A**, R1. Elena Marin adds the Public Procurement Department: the unit and its positions, a new person (Pending until first sign-in), an amended nomenclator edition with the entry for tender files put in force, the dosar Tender files 2026, the document type Tender file, and a grant of **Standard user** to the unit. Sources: `ag/organization.md`, `ag/people.md`, `ag/nomenclator.md`, `ag/folders-administration.md`, `ag/document-types.md`, `ag/roles-and-grants.md`. Shots: `dms-ex-dept-unit`, `dms-ex-dept-person`, `dms-ex-dept-edition`, `dms-ex-dept-force`, `dms-ex-dept-folder`, `dms-ex-dept-type`, `dms-ex-dept-grant`, `dms-people-list`.
7. `dms/examples/selection-and-handover.md`: title "Example: select and hand over dosare", label "Selection and handover". **A**, R1. Carmen Pavel, archivist: closes the dosar Invoices 2014; finds it and Petitions 2019 under **Term ended**; starts a selection, leaves one dosar out, issues the proces-verbal, records the answer of the Arhivele Naționale and schedules the deletion; then hands the permanent dosar Mayor's orders 1995 over: the proposal, the package, the confirmation. Sources: `ug/selection.md`, `ug/handover.md`, `ag/selection-and-deletion.md`, `ag/handover-and-export.md`. Shots: `dms-dosar-close`, `dms-selection-term-ended`, `dms-selection-start`, `dms-selection-proposal`, `dms-selection-pv`, `dms-selection-answer`, `dms-selection-schedule`, `dms-selection-scheduled`, `dms-handover-permanent`, `dms-handover-proposal`, `dms-handover-prepare`, `dms-handover-ready`, `dms-handover-confirm`, `dms-handover-done`, `dms-pv-register`.

**Daily work** (group "Daily work")

8. `dms/work/sign-in.md`: title "Sign in and find your way", label "Sign in and find your way". **B**, R1. The sign-in card (**Email address**, **Password**, **Remember me on this computer**, **Sign in**) and its messages; the sidebar's sections and who sees each (a table); the user bar: language (**EN**/**RO**), theme (system, light, dark), **Sign out**; the idle sign-out after 30 minutes; the phone layout. Sources: `ug/signing-in.md`, `ug/layout-and-navigation.md`, `ug/language-and-theme.md`. Shots: `dms-sign-in`, `dms-shell-staff`, `dms-desk-first-admin`.
9. `dms/work/my-desk.md`: title "My desk", label "My desk". **B**, R1. The tiles (**To review**, **To sign**, **Filed in 14 days**, **Without a type**), the archive tiles some roles see, the charts, **Proposed filings**, **Recently modified**, **Favorites**. Sources: `ug/my-desk.md`. Shots: `dms-desk-staff`, `dms-desk-archivist`.
10. `dms/work/library.md`: title "The library", label "Library". **B**, R1. The folder tree and **Search for a folder**; a folder's page: the dosar facts (**Year**, **Retention**, Open or Closed), the table, **Sort**, **Columns**, the pager, the row's **More actions**; user folders you make with **New folder**; closed dosare; moving documents. Sources: `ug/library-and-finding-documents.md`, `ug/folders-and-dosare.md` (user part). Shots: `dms-library`, `dms-library-folder`, `dms-library-row-menu`, `dms-library-folder-menu`, `dms-library-closed`.
11. `dms/work/upload.md`: title "Upload and import documents", label "Upload and import". **U**, R1. **Upload a document** for one or many files; dropping files on a folder; the tray and the **Uploads** page; the "Waiting", "Processing" and "Processing failed" chips; the notice of the same content elsewhere; for many files with metadata, the **Import** page: staging, the manifest template, **Check**, **Import {count} documents**. Sources: `ug/uploading-documents.md`, `ug/bulk-import.md`. Shots: `dms-upload-dialog`, `dms-upload-tray`, `dms-uploads-page`, `dms-upload-duplicate`, `dms-import-staging`, `dms-import-report`.
12. `dms/work/document-page.md`: title "The document page", label "The document page". **B**, R1. The header (state, pills, star, version), **Life of the document**, the buttons, the viewer, and the tabs in order: **Metadata** (editing, required fields, "Not filled in"), **Versions**, **History**, **Attachments** (**Attach**, **Detach**), **Comments**, **Signatures**, **Workflows** (one paragraph: shown only when a Keel case or process holds the document; no screenshot), **Archive** (retention, **Entered the DMS**, reception, preservation), **Audit log** (for auditors and administrators). Sources: `ug/the-document-page.md`, `ug/document-types-and-metadata.md`, `ug/links-and-duplicates.md`, `ug/workflows.md`. Shots: `dms-doc-page`, `dms-doc-metadata-edit`, `dms-doc-history`, `dms-doc-attachments`, `dms-doc-archive-tab`.
13. `dms/work/versions.md`: title "View, edit and keep versions", label "Viewing, editing and versions". **U**, R1. The viewer's toolbar and **What to show** (**Original file**, **Copy with text**); **Edit online** and **Close the editor**; **Check out**, **Return**, **Cancel the check-out**, and **Unlock** for administrators; **New version**, labels, **Go back to this version**; **Compare with the previous version**. Sources: `ug/viewing-and-editing.md`, `ug/versions-and-check-out.md`, `ug/comparing-versions.md`. Shots: `dms-viewer-text`, `dms-edit-online`, `dms-checkout-bar`, `dms-versions-tab`, `dms-versions-compare`.
14. `dms/work/lifecycle.md`: title "The life of a document", label "Lifecycle". **B**, R1. The five states, the buttons **Validate**, **Approve**, **Publish**, **Archive**, **Reopen**, who holds each (a table by built-in role), what each state allows, archiving and what an archived document still allows (comments). Sources: `ug/lifecycle.md`, `ug/the-document-page.md`. Shots: `dms-lifecycle-card`, `dms-lifecycle-approve`, `dms-lifecycle-archive`.
15. `dms/work/search.md`: title "Search", label "Search". **U**, R1 (the AI mode section is R2). The search box and the words it understands (from **Search tips**), **Advanced search**, **Filters**, **Latest version only** and **All versions**, **Columns** and **Group**, **Save the search** and virtual folders, **Export** and **Download the files**; matches marked in the viewer. Sources: `ug/search.md`, `ug/asking-questions.md` (R2). Shots: `dms-search-results`, `dms-viewer-matches`, `dms-search-advanced`, `dms-search-save`, `dms-virtual-folder`, `dms-search-ai` (R2).
16. `dms/work/comments.md`: title "Comments and notifications", label "Comments and notifications". **U**, R1. **Your comment**, **Mention a person** and the `@` list, **Send**; the **Notifications** page, **Mark all as read**, and what notifies you. Sources: `ug/comments-and-notifications.md`. Shots: `dms-comments-mention`, `dms-notifications`.
17. `dms/work/signing.md`: title "Sign documents", label "Signing". **U**, R1. **Request a signature** (**Signers**, **Signature asked for**: **Internal allowed** or **Qualified (token)**); the **To sign** page and its tabs; **Sign internally**; signing **With a token** (download, sign in the provider's app, **Upload the signed file**) described without screenshots; **Refuse**; the **Signatures** tab and its statuses; signed files from outside in one section. Sources: `ug/signing-documents.md`, `ug/signed-files-from-outside.md`. Shots: `dms-sign-request`, `dms-to-sign`, `dms-sign-internal`, `dms-signatures-tab`.
18. `dms/work/favorites-and-collections.md`: title "Favorites and collections", label "Favorites and collections". **B**, R1. The star, **Favorite documents** in the sidebar, the **Favorites** page; collections: what members may do, **New collection** for people with "Manages collections", **Add documents**, expiry. Sources: `ug/favorites.md`, `ug/collections.md`. Shots: `dms-favorites`, `dms-collection-new`, `dms-collection-page`.
19. `dms/work/to-review.md`: title "Filing proposals", label "To review". **U**, R2. The **To review** page: a proposal's **Field**, **Now**, **Proposed**, and **Confirm**, **Edit**, **Dismiss**; the proposal banner on the Metadata tab. Shown only where the installation makes proposals. Sources: `ug/review-proposals.md`. Shots: `dms-review`.
20. `dms/work/personal-data.md`: title "Personal data and the reason for access", label "Personal data". **B**, R1. For everyone: the pills, the **Personal data** card, the **Reason for access** dialog and what happens to the reason. For people who classify: **Change the classification**. For the DPO and administrators: the **Personal data** page and its tabs **Register**, **Documents**, **Reasons for access**, **Categories**, **Purposes**, and the defaults on types and entries. Sources: `ug/personal-data.md`, `ag/personal-data.md` (UI parts). Shots: `dms-pd-document`, `dms-pd-reason`, `dms-pd-classify`, `dms-pd-categories`, `dms-pd-register`, `dms-pd-reasons`, `dms-types-permit`.

**Archive** (group "Archive")

21. `dms/archive/overview.md`: title "The Archive overview", label "Overview". **A**, R1. Who sees the Archive section; the tiles (**Terms ending in {year}**, **Terms ending, by year**, **Kept for**, **Nomenclator in force**, **Dosare without an entry** with **Fix them**, the tiles for selection, handover, reception and integrity); the page of dosare without an entry. Sources: `ug/archive-overview.md`. Shots: `dms-archive-overview`, `dms-archive-without-entry`.
22. `dms/archive/reception.md`: title "Reception", label "Reception". **A**, R2. What the DMS checks when a file arrives, in plain words; the **Not accepted** pill and banner; **See the checks**, **Check again**; the **Reception** page's tabs; **Accept into the archive** with a reason. Sources: `ug/reception.md`, `ag/reception.md` (UI parts). Shots: `dms-reception`, `dms-reception-accept`.
23. `dms/archive/integrity.md`: title "Integrity and procese-verbale", label "Integrity and procese-verbale". **A**, R2. The monthly check in plain words, **Run a check now**, the tiles, what quarantine means for a document, closing an incident and **Restore from the original** (described, not pictured: the demo has no incident); the **Procese-verbale** register and its kinds. Sources: `ug/integrity-and-quarantine.md`, `ag/integrity-checks.md` (UI parts). Shots: `dms-integrity`, `dms-pv-register`.
24. `dms/archive/preservation.md`: title "Archival copies and time stamps", label "Archival formats and time stamps". **A**, R2. The archival copy a version gets (PDF/A for most files), the Preservation block on the Archive tab, **Convert again**; the **Archival formats** page; qualified time stamps and the **Time stamps** page, when the installation has them. Sources: `ug/archival-copies.md`, `ug/time-stamps.md`, `ag/archival-formats.md`, `ag/time-stamps.md` (UI parts). Shots: `dms-doc-preservation`, `dms-formats`, `dms-timestamps`.
25. `dms/archive/selection.md`: title "Selection and deletion of dosare", label "Selection". **A**, R1. Which dosare are listed under **Term ended**; a selection's four steps (Proposal, Proces-verbal, Answer, Deletion) and their buttons; holds (**Hold the dosar**, **Lift the hold**); the seven-day delay and **Cancel the deletion**; **Deleted documents** and what stays of a deleted document. Sources: `ug/selection.md`, `ag/selection-and-deletion.md` (UI parts). Shots: `dms-selection-term-ended`, `dms-selection-proposal`, `dms-selection-schedule`, `dms-selection-hold`, `dms-selection-deleted` (taken in the later pass).
26. `dms/archive/handover.md`: title "Handover to the National Archives", label "Handover". **A**, R1. Which dosare are due (permanent, 30 years after their end year); a handover's steps (Proposal, Package, Handover) and their buttons; the blockers a dosar can show; recording the confirmation; what documents and dosare show afterwards; the evidence package of a document and **Export the dosar**, in a short section. Sources: `ug/handover.md`, `ag/handover-and-export.md` (UI parts). Shots: `dms-handover-permanent`, `dms-handover-proposal`, `dms-handover-ready`, `dms-handover-done`.
27. `dms/archive/reports.md`: title "Reports", label "Reports". **A**, R2. The three kinds (**Activity**, **Archive holdings**, **Alerts register**) and who may read each; models, **Run**, **Use as a model**; the editor (Period, Filters, Grouping, Measures, Schedule, Recipients); a run's page and its downloads. Sources: `ug/reports.md`, `ag/reports-and-statistics.md` (UI parts). Shots: `dms-reports`, `dms-reports-editor`, `dms-reports-run`.
28. `dms/archive/alerts.md`: title "Alerts", label "Alerts". **A**, R2. What an alert is and what it is not (it decides and blocks nothing); **To handle**, **Closed**, **Rules**; **Take it**, **Close** with a conclusion, the quiet period; the rules and their settings; who is told. Sources: `ug/alerts.md`, `ag/anomaly-alerts.md` (UI parts). Shots: `dms-alerts-todo`, `dms-alerts-close`, `dms-alerts-rules`.

**Administration** (group "Administration")

29. `dms/admin/org-chart.md`: title "The org chart", label "Org chart". **A**, R1. **Unit types**, **New unit at the top level**, a unit's and a position's menus, **Holder…**, "Vacant", moving by drag and drop, and the Excel import (**Download the template**, **Check**, **Apply**); how moves change access at once. Sources: `ag/organization.md`. Shots: `dms-org-unit-types`, `dms-org-new-unit`, `dms-org-holder`, `dms-org-chart`, `dms-org-import`.
30. `dms/admin/people.md`: title "People", label "People". **A**, R1. **Add a person** (**Email address**, **Display name**), "Pending" until first sign-in, **Rename**, **Deactivate** and **Reactivate**; that accounts and passwords live in the institution's sign-in service; that roles are given on **Roles and permissions**; one line on the **Service accounts** tab (for IT). Sources: `ag/people.md`. Shots: `dms-people-add`, `dms-people-list`.
31. `dms/admin/roles.md`: title "Roles and permissions", label "Roles and permissions". **A**, R1. The built-in roles and custom roles (**New role**, **Role name**, the permission groups **Documents** and **Administration**); **Grant the role** to a person, a position or a unit, for the institution or a unit with its subunits, for some types and states; **Revoke**; how grants add up, with examples from the demo. Sources: `ag/roles-and-grants.md`, `ug/access-and-sharing.md`. Shots: `dms-roles-list`, `dms-roles-new`, `dms-roles-grant`, `dms-roles-grants`.
32. `dms/admin/document-types.md`: title "Document types", label "Document types". **A**, R1. The list, **New type**, **Type name**, **Default folder**, **Suggested nomenclator entry**, **Personal data**, **Add a field** (**Field label**, **Field key**, **Kind of value**, **Required**), the eight kinds of value, and what cannot change once documents use a type. Sources: `ag/document-types.md`, `ug/document-types-and-metadata.md`. Shots: `dms-types-list`, `dms-types-contract`, `dms-types-permit`.
33. `dms/admin/folders.md`: title "Folders and dosare", label "Folders and dosare". **A**, R1. The **Folders** page (**New folder at the root**, **The chosen folder**, the unit a folder belongs to); library folders and user folders; a dosar's entry (**Entry**, **Year of the dosar**, **Closes**); **Close the dosar** and **Reopen the dosar**; opening next year's dosare from the Nomenclator page. Sources: `ag/folders-administration.md`, `ug/folders-and-dosare.md`. Shots: `dms-folders-admin`, `dms-folders-new-root`, `dms-dosar-entry`, `dms-dosar-close`.
34. `dms/admin/nomenclator.md`: title "The nomenclator", label "Nomenclator". **A**, R1. Editions (draft, in force, superseded); **Import an edition** from the approved Excel, or **New edition**; **Choose the unit** for each compartment; the problems on the draft; **Approval number** and **Approval date**; **Put in force**; **Copy into a new edition** for an amendment; **The dosare of {year}** and **Open the dosare of {year}**. The sample (**Load the sample**) is mentioned as being for a demonstration. Sources: `ag/nomenclator.md`, `ag/folders-administration.md`. Shots: `dms-nomenclator-empty`, `dms-nomenclator-draft`, `dms-nomenclator-unit`, `dms-nomenclator-force`, `dms-nomenclator-in-force`.
35. `dms/admin/signatures.md`: title "Electronic signatures", label "Signatures". **A**, R2. The **Signatures** page: the **Internal certificate authority** and its fingerprint (give it to your auditor), **Internal certificates** (**Issue a certificate**, **Revoke**), **Confirmed token certificates**, **Trusted lists** and **Refresh now**; that holders of this page can cancel any signing request. Sources: `ag/electronic-signature.md` (UI parts). Shots: `dms-signatures-admin`.
36. `dms/admin/audit-log.md`: title "The audit log", label "Audit log". **A**, R1. What is recorded and what is not; the tabs **Entries**, **Log integrity**, **Log archive**, **Bundles**; the filters; **Export CSV**, **Export JSON**, **PDF (report)**; **Investigation bundle** for an inspector; the document's own **Audit log** tab. Sources: `ag/audit-log.md`, `ug/audit-and-inspections.md` (UI parts). Shots: `dms-audit-entries`, `dms-audit-bundle`, `dms-doc-audit-tab`.

**Reference** (group "Reference")

37. `dms/reference/roles.md`: title "Built-in roles and permissions", label "Built-in roles". **B**, R1. A table of the built-in roles against what they may do, in the UI's permission sentences, as the Keel roles page does; a short note on how grants narrow a role to a unit, types and states. Sources: `ag/roles-and-grants.md`, `ug/lifecycle.md`, `ug/access-and-sharing.md`, and the **Roles and permissions** page at capture time (the authority for the table). Shots: none.
38. `dms/reference/glossary.md`: title "Surogate DMS glossary", label "Glossary". **B**, R1. Every term of the guide in one table, English term and meaning, including the Romanian terms the UI keeps. Sources: `ug/glossary.md` without its internals (chunk, CRL, log chain, seal, checkpoint, rendition, transfer package internals, QSCD, CAdES and PAdES details). Shots: none.
39. `dms/reference/faq.md`: title "Surogate DMS FAQ", label "FAQ". **B**, R1. Questions the messages and empty screens raise, as Keel's FAQ: "I signed in and see no folder", "Why is Upload missing?", "Why can I not archive this document?", "Why does a document ask me for a reason?", sign-in messages, plus "What the DMS does not do" (the not-available list) and "Who uses the Keel integration and API integration pages". Sources: `ug/common-refusals.md` (user-facing messages only), `ag/health-and-troubleshooting.md` (UI-facing symptoms only), both "Not available yet" lists. Shots: none.

R1: pages 1 to 18, 20, 21, 25, 26, 29 to 34, 36 to 39 (32 pages). R2: pages 19, 22, 23, 24, 27, 28, 35 (7 pages).

No keyboard-shortcuts page: the DMS has no global shortcuts. The few keys it reacts to go on the pages where they apply: Escape leaves the viewer's full screen, Enter in the page box jumps to that page, Ctrl with the mouse wheel zooms the viewer (page 13), Enter runs a search (page 15), `@` at the start of a word opens the list of people in a comment (page 16).

Left out on purpose: registers and registration numbers (not in the UI), the Keel integration and API integration pages (decision 5), and every maintainer page of the administrator guide (installation, configuration, deployment, search, worker and jobs, intake pipeline, uploads internals, backups, upgrades, translations, Ask's setup).

---

## B. Voice and rules

See Global Constraints above; they apply to every page. In addition:

- Terms: "document", "version", "folder", "library folder", "user folder", "dosar" (plural "dosare"), "virtual folder", "document type", "metadata", "unit", "position", "role", "grant", "nomenclator", "entry", "edition", "retention", "term", "proces-verbal" (plural "procese-verbale"), "the National Archives" in prose and **Arhivele Naționale** only where a label says it. One term per thing: never "check in" for **Return**, never "register" for the nomenclator.
- Keel's page patterns to reuse: the "Start here" table on the welcome page, "You need:" lists at the top of the quickstarts, numbered `## 1. ...` sections in quickstarts, "Who sees it" tables, message tables with "What to do", "Next steps" at the end of quickstarts and examples.
- Romanian labels are never given; addresses inside the app (`/biblioteca`, `/arhiva/...`) are never shown; menu paths are written as **Archive** › **Selection**.

---

## C. Demo dataset and shot list

### C.1 The demo dataset

Everything is fictional. E-mail addresses use the reserved domain `example.org`. No real personal data, no national identification numbers, no real company names on purpose; street names are generic.

**Institution:** Example City Hall (the operator sets it as the institution's name; it prints on procese-verbale). Time zone Europe/Bucharest.

**Unit types:** Directorate, Department, Office.

**Units and positions** (holder in brackets):

| Unit (type) | Positions |
|---|---|
| Mayor's Office (Office) | Mayor (Vacant), Internal auditor (Victor Lungu) |
| General Secretariat (Directorate) | Secretary General (Mihai Stan), Data protection officer (Dana Voicu) |
| General Secretariat › Registry Office (Office) | Registry clerk (Andrei Ionescu) |
| General Secretariat › Archive Office (Office) | Archivist (Carmen Pavel) |
| Urban Planning Department (Department) | Head of Urban Planning (Vacant), Urban planning inspector (Ioana Dobre) |
| Finance Department (Department) | Head of Finance (Vacant) |
| Legal Department (Department) | Contracts clerk (Radu Florea) |
| IT Office (Office) | IT administrator (Elena Marin) |
| Human Resources Department (Department), by Excel import | HR officer (Vacant), Head of HR (Vacant) |
| Public Procurement Department (Department), in the example | Head of Public Procurement (Vacant), Procurement officer (Sorin Neagu) |

**People and their grants** (eight sign-in accounts, one person who never signs in). A grant names a recipient (a person, a position, or a unit, which reaches the people holding a position in that exact unit) and where it applies (the whole institution, or a unit with or without its subunits):

| Person | E-mail | Grants |
|---|---|---|
| Elena Marin | elena.marin@example.org | **Archive administrator** to the person, whole institution (the operator's first-administrator step) |
| Andrei Ionescu | andrei.ionescu@example.org | **Standard user** to the person, General Secretariat with its subunits, and again for Finance Department; **Access to special data** to the person, General Secretariat with its subunits |
| Ioana Dobre | ioana.dobre@example.org | **Standard user** to the unit Urban Planning Department, applies to Urban Planning Department with its subunits |
| Radu Florea | radu.florea@example.org | **Standard user** to the unit Legal Department, applies to Legal Department |
| Mihai Stan | mihai.stan@example.org | custom role **Approver** (Reads documents, Comments, Validates, Approves, Publishes, Asks for signatures) to the position Secretary General, whole institution |
| Carmen Pavel | carmen.pavel@example.org | **Electronic archivist** to the person, whole institution |
| Dana Voicu | dana.voicu@example.org | **Data protection officer (DPO)** to the person, whole institution (the role reads no documents; it reads the register, the reasons and the alerts) |
| Victor Lungu | victor.lungu@example.org | **Auditor** to the person, whole institution |
| Sorin Neagu | sorin.neagu@example.org | added in the example and stays "Pending"; **Standard user** to the unit Public Procurement Department reaches him |

**Personal-data taxonomy:** categories Identification data, Contact data, Health data (special category); purposes Issuing building permits, Answering petitions.

**Nomenclator:** edition `2026.1`, approved by the Arhivele Naționale, no. 1234 of 15.01.2026, imported from an Excel file made from **Download the Excel template** with English entry texts (never **Load the sample**: its entries are Romanian). In the example, edition `2026.2` (no. 1301 of 20.02.2026) adds the Public Procurement entry and supersedes `2026.1`.

| Compartment (unit) | Indicativ | Entry | Term |
|---|---|---|---|
| General Secretariat | I-1 | Mayor's orders | Permanent |
| General Secretariat | I-2 | Petitions and their answers | 5 years |
| General Secretariat | I-3 | Correspondence with other institutions | 3 years |
| Finance Department | II-1 | Supplier invoices | 10 years |
| Finance Department | II-2 | Budget execution reports | Permanent |
| Urban Planning Department | III-1 | Building permits | Permanent |
| Urban Planning Department | III-2 | Urban planning certificates | 10 years |
| Legal Department | IV-1 | Contracts | 10 years |
| Public Procurement Department (2026.2 only) | V-1 | Tender files | 10 years |

**Document types** (default folder, suggested entry, personal data):

| Type | Fields (kind, required) | Default folder | Entry | Personal data |
|---|---|---|---|---|
| Contract | Contract number (Text, required), Counterparty (Text, required), Value in lei (Number), Signed on (Date), Ends on (Date), Responsible (Person) | Legal Department › Contracts 2026 | IV-1 | No personal data |
| Building permit | Permit number (Text, required), Applicant (Text, required), Property address (Text), Issued on (Date), Decision (List of options: Issued, Refused) | Urban Planning Department › Building permits 2026 | III-1 | Holds personal data, Identification data, Issuing building permits |
| Petition | Petitioner (Text, required), Subject (Long text), Received on (Date, required), Answer due (Date), Handled by (Unit) | General Secretariat › Petitions 2026 | I-2 | Holds personal data, Contact data, Answering petitions |
| Invoice | Supplier (Text, required), Invoice number (Text, required), Amount in lei (Number), Due on (Date), Paid (Yes or no) | Finance Department › Invoices 2026 | II-1 | No personal data |
| Mayor's order | Order number (Text, required), Issued on (Date, required), Subject (Long text) | General Secretariat › Mayor's orders 2026 | I-1 | No personal data |
| Tender file (example) | Tender number (Text, required), Subject (Long text), Estimated value in lei (Number), Deadline (Date) | Public Procurement Department › Tender files 2026 | V-1 | No personal data |

**Library folders** (root folders belong to the unit of the same name):

| Folder | Dosar | State |
|---|---|---|
| General Secretariat › Mayor's orders 2026 | I-1, 2026, closes at the end of the year | Open |
| General Secretariat › Mayor's orders 1995 | I-1, 1995, closed by hand, ends 1995 | Closed; due for handover (1995 + 30 = 2025) |
| General Secretariat › Petitions 2026 | I-2, 2026 | Open |
| General Secretariat › Petitions 2019 | I-2, 2019, closed, ends 2019 | Closed; term ended 2024: selection candidate |
| Finance Department › Invoices 2026 | II-1, 2026 | Open |
| Finance Department › Invoices 2014 | II-1, 2014, closed, ends 2014 | Closed; term ended 2024: selection candidate |
| Urban Planning Department › Building permits 2026 | III-1, 2026 | Open; holds the user folder Pending applications |
| Legal Department › Contracts 2026 | IV-1, 2026 | Open |
| Legal Department › Miscellaneous | no entry | Listed under **Dosare without an entry** |
| Public Procurement Department › Tender files 2026 (example) | V-1, 2026 | Open |

A closed old dosar is made open first ("When you close it (a dosar over several years)"), filled, then closed with **Close the dosar** and its end year, because a closed dosar takes in no documents.

**Documents (30)**, from 29 files generated by the capture kit (Task 4):

| Folder | Title | Type and key values | State and extras |
|---|---|---|---|
| Contracts 2026 | Street lighting maintenance 2026 | Contract LC-07/2026, Bright Street Lighting SRL, 184,500 | Published, signed internally by Mihai Stan; attachment: Technical annex, street lighting (the contract example) |
| Contracts 2026 | Technical annex, street lighting | Contract LC-07/2026 annex 1, Bright Street Lighting SRL | Validated |
| Contracts 2026 | Snow clearing services 2026-2027 | Contract LC-11/2026, Winter Roads SRL, 96,000 | Approved; in the collection |
| Contracts 2026 | IT support for the city hall | Contract LC-15/2026, a `.docx` | Validated; 3 versions, label "final"; opened in the online editor |
| Contracts 2026 | School gym renovation works | Contract LC-19/2026 | Draft, checked out by Radu Florea |
| Building permits 2026 | Building permit 12/2026, 14 Linden Street | Applicant Maria Lazar | Published; Personal data; attachment: Site plan |
| Building permits 2026 | Building permit 13/2026, 3 Orchard Lane | Applicant Paul Georgescu | Approved |
| Building permits 2026 | Building permit 14/2026, 22 Mill Road | Applicant Ana Vlad | Validated, signed internally (the quickstart document), favorite of Ioana |
| Building permits 2026 | Site plan, 14 Linden Street | image-only PDF (OCR) | Draft |
| Building permits 2026 › Pending applications | Application, 9 River Street | untyped | Draft; R2: a filing proposal |
| Building permits 2026 › Pending applications | Site plan, 14 Linden Street (copy) | the site plan's file uploaded again | Draft; shows the same-content notice |
| Petitions 2026 | Petition on street parking, Garden District | Petitioner Elena Rusu | Validated |
| Petitions 2026 | Petition for a ramp at the library | Petitioner Ion Matei, medical certificate attached | Draft, classified Special categories, Health data (asks a reason) |
| Petitions 2026 | Petition about noise at night | Petitioner Cristina Pop | Published |
| Petitions 2026 | Petition about a broken bench | Petitioner Dan Moraru | Draft |
| Petitions 2026 | Petition for more bus stops | Petitioner Irina Stoica | Draft |
| Mayor's orders 2026 | Mayor's order 41/2026 on the budget committee | | Archived |
| Mayor's orders 2026 | Mayor's order 42/2026 on office hours | | Published |
| Invoices 2026 | Four invoices (Lumen Supplies SRL 2201, Office Paper SRL 118, Clean City SRL 3307, Green Parks SRL 54) | | Draft, brought in by **Import** |
| Invoices 2014 | Three invoices (2014) | | Archived before the dosar closes |
| Petitions 2019 | Two petitions (2019) | | Archived before the dosar closes |
| Mayor's orders 1995 | Mayor's order 12/1995 and Mayor's order 30/1995 | image-only PDFs that look like scans | Archived before the dosar closes |
| Miscellaneous | Notes from the legal training | | Draft |

Applicants and petitioners are invented names; the documents hold no other personal details than a name and a street address.

**Collection:** "Court file: snow clearing dispute", recipient Radu Florea, expires 31 Dec 2026, three documents (Snow clearing services 2026-2027, Petition about noise at night, Mayor's order 42/2026).

**Saved search:** "Contracts over 100,000 lei" (Type is Contract, Value in lei greater than 100000), shown in the sidebar as a virtual folder.

### C.2 What must exist before capture

Outside this plan, by the owner or the operator (Task 5 checks each):

1. A DMS installation at the current main, empty, reachable from node2, with English available. Its commit is recorded.
2. The eight sign-in accounts above in the institution's sign-in service, with passwords in `~/.config/surogate-dms/docs-demo.env` (mode 600, never committed or printed): `SHOTS_URL=...`, `SHOTS_PASSWORD_ELENA=...` and so on for ANDREI, IOANA, RADU, MIHAI, CARMEN, DANA, VICTOR.
3. Elena Marin made the first administrator (the operator's first-administrator step).
4. The institution's name set to "Example City Hall"; the internal certificate authority created (without it **Sign** is not offered); the online editor on. For R2 only: filing proposals, AI mode, a time-stamping authority.
5. The capture kit of Task 4, with the demo files generated.

### C.3 The shot list

Every shot is a full 1600x900 window, light theme, English, at device scale 1. "As" is the account the script is signed in as. Ids are the file names without `.png`. Sessions run in order: each one builds the data the next needs. Shots marked R2 are taken in the same session when the feature is on, and used by Task 24.

**Session A: administration setup** (as Elena Marin unless noted; before it, only the accounts exist)

| Id | Screen | State to show | Data | Pages |
|---|---|---|---|---|
| `dms-sign-in` | Sign-in page | Empty card: **Email address**, **Password**, **Remember me on this computer** ticked, **Sign in** | none; signed out, browser language English | 3, 4, 8 |
| `dms-desk-first-admin` | My desk | New installation: "No documents yet.", sidebar with **Archive** and **Administration** | none | 4, 8 |
| `dms-org-unit-types` | Org chart | **Unit types** panel with Directorate, Department, Office; no units | unit types | 4, 29 |
| `dms-org-new-unit` | Org chart | **New unit at the top level** dialog: **Unit name** Urban Planning Department, **Unit code (optional)** UP, **Unit type** Department | earlier units made | 29 |
| `dms-org-import` | Org chart import | After **Check**: three rows "Create" for Human Resources Department and its two positions; **Apply** enabled | an `.xlsx` from **Download the template** | 29 |
| `dms-people-add` | People | **Add a person** dialog: Carmen Pavel, carmen.pavel@example.org | first people added | 4, 30 |
| `dms-org-holder` | Org chart | **Holder…** dialog on Secretary General, Mihai Stan chosen | people added | 4, 29 |
| `dms-org-chart` | Org chart | Whole tree with positions and holders; the positions nobody holds read "Vacant" | all units, positions, holders | 2, 4, 29 |
| `dms-nomenclator-empty` | Nomenclator | No edition: **Import an edition**, **New edition**, **Load the sample**, **Download the Excel template** | none | 4, 34 |
| `dms-nomenclator-draft` | Nomenclator | Draft `2026.1` after import: compartments to map and the problems listed, **Approval number**, **Approval date**, **Check again**, **Put in force** | the English edition file | 34 |
| `dms-nomenclator-unit` | Nomenclator | "Choose the unit for “Finance Department”" dialog | draft | 34 |
| `dms-nomenclator-force` | Nomenclator | "Put edition 2026.1 in force?" dialog | draft without problems, approval filled | 4, 34 |
| `dms-nomenclator-in-force` | Nomenclator | `2026.1, in force`: the entries table | edition in force | 2, 4, 34 |
| `dms-folders-new-root` | Folders | **New folder at the root** dialog: Finance Department, unit Finance Department | first roots made | 4, 33 |
| `dms-folders-admin` | Folders | Tree of the root folders, **The chosen folder** panel for Legal Department | all library folders | 33 |
| `dms-dosar-entry` | Library, Contracts 2026 | 'Nomenclator entry of the dosar "Contracts 2026"': **Entry** IV-1, **Year of the dosar** 2026, **Closes** **At the end of the year** | edition in force | 4, 33 |
| `dms-types-list` | Document types | Five types with fields, default folders, suggested entries | types | 32 |
| `dms-types-contract` | Document type Contract | Editor with its six fields | Contract | 4, 32 |
| `dms-types-permit` | Document type Building permit | Editor showing the **List of options** field Decision and the **Personal data** default | Building permit, taxonomy | 20, 32 |
| `dms-roles-list` | Roles and permissions | **Standard user** selected: its permissions in **Documents** and **Administration** | built-in roles | 31 |
| `dms-roles-new` | Roles and permissions | **New role** Approver with its permissions ticked | none | 31 |
| `dms-roles-grant` | Roles and permissions | "Grant the role Standard user": **Type of recipient** **Unit**, Urban Planning Department, **The unit it applies to** Urban Planning Department, **Include the subunits** | units | 4, 31 |
| `dms-roles-grants` | Roles and permissions | **Who the role was granted to** for Standard user: the grants to Urban Planning Department, Legal Department and Andrei Ionescu | grants made | 2, 31 |
| `dms-pd-categories` | Personal data | **Categories** tab with the three categories, Health data special | taxonomy | 20 |
| `dms-alerts-rules` | Alerts | **Rules** tab, the after-hours rule's working hours | none | 4, 28 |
| `dms-signatures-admin` (R2) | Signatures | **Internal certificate authority**, **Internal certificates** | internal CA | 35 |

**Session B: the new-department example** (as Elena Marin)

| Id | Screen | State to show | Data | Pages |
|---|---|---|---|---|
| `dms-ex-dept-unit` | Org chart | Public Procurement Department with its two positions | Session A | 6 |
| `dms-ex-dept-person` | People | **Add a person**: Sorin Neagu, sorin.neagu@example.org | | 6 |
| `dms-ex-dept-edition` | Nomenclator | Draft `2026.2` made with **Copy into a new edition**, the new entry V-1 Tender files typed | `2026.1` in force | 6 |
| `dms-ex-dept-force` | Nomenclator | "Put edition 2026.2 in force?" with one new entry in the comparison | approval no. 1301 | 6 |
| `dms-ex-dept-folder` | Library, Tender files 2026 | The dosar's facts: entry V-1, 2026, Open | `2026.2` in force | 6 |
| `dms-ex-dept-type` | Document type Tender file | Editor with its four fields and default folder | | 6 |
| `dms-ex-dept-grant` | Roles and permissions | "Grant the role Standard user" to **Unit** Public Procurement Department | | 6 |
| `dms-people-list` | People | Nine people: eight "Signed in" (after Session C), Sorin Neagu "Pending" | take at the end of Session D | 6, 30 |

**Session C: daily work** (the account changes per row)

| Id | Screen | State to show | Data | As | Pages |
|---|---|---|---|---|---|
| `dms-shell-staff` | My desk | A staff member's desk before any document: zero counts, sidebar without **Archive** and **Administration** | Ioana has filed nothing | Ioana | 3, 8 |
| `dms-library` | Library | Tree of the folders Ioana can read, "Choose a folder on the left." | | Ioana | 3, 10 |
| `dms-upload-dialog` | Library, Building permits 2026 | **Upload a document**: **File** permit-14-2026.pdf, **Title** Building permit 14/2026, 22 Mill Road, **Document type** Building permit | two permits filed before | Ioana | 3, 11 |
| `dms-doc-page` | Document page | The new permit: Draft, viewer with page 1, **Metadata** with "Not filled in" values | | Ioana | 3, 12 |
| `dms-doc-metadata-edit` | Document page, Metadata | **Edit** mode, all fields filled, **Save** | | Ioana | 3, 12 |
| `dms-lifecycle-card` | Document page | **Life of the document** card and the **Validate** button | metadata saved | Ioana | 3, 14 |
| `dms-search-results` | Search | Query `Mill Road`, results and the **Filters** card | index caught up | Ioana | 3, 15 |
| `dms-viewer-matches` | Document page | Opened from the result: matches marked, "1 of 2 matches" | | Ioana | 15 |
| `dms-favorites` | Favorites | The permit starred; **Favorite documents** in the sidebar | starred | Ioana | 3, 18 |
| `dms-comments-mention` | Document page, Comments | `@Mih` typed, the list offering Mihai Stan | | Ioana | 3, 16 |
| `dms-sign-request` | Document page, Signatures | **Request a signature**: **Signers** Mihai Stan, **Internal allowed**, a message | permit Validated | Ioana | 3, 17 |
| `dms-notifications` | Notifications | "You were mentioned in a comment" and "Your signature was asked for on a document" | | Mihai | 3, 5, 16 |
| `dms-to-sign` | To sign | **To sign** tab with the request, the **Ask colleagues to sign** card | | Mihai | 3, 17 |
| `dms-sign-internal` | Document page | **Sign internally** dialog with a note | | Mihai | 3, 5, 17 |
| `dms-signatures-tab` | Document page, Signatures | Mihai Stan's signature "Valid · internal (not qualified)" | signed | Ioana | 3, 17 |
| `dms-upload-tray` | Library | The tray with three uploads under way (network slowed by the script) | three permit files | Ioana | 11 |
| `dms-uploads-page` | Uploads | Finished uploads, **Remove the finished ones from the list** | | Ioana | 11 |
| `dms-upload-duplicate` | Document page | The notice "The same content already exists in:" naming the other document | Site plan, 14 Linden Street (copy) uploaded into Pending applications | Ioana | 11 |
| `dms-import-staging` | Import | Step 1 with the four invoice PDFs staged, step 2 with **Type of the documents in the template** Invoice | the four invoice files | Andrei | 11 |
| `dms-import-report` | Import report | After **Check**: four rows "Correct", **Import 4 documents** | the filled manifest | Andrei | 11 |
| `dms-library-folder` | Library, Building permits 2026 | Dosar facts, four documents in several states, the user folder Pending applications | Session C uploads | Ioana | 2, 3, 10 |
| `dms-library-row-menu` | Library | A row's **More actions** open | | Ioana | 10 |
| `dms-library-folder-menu` | Library | **Folder actions** open, showing **New folder** | | Ioana | 10 |
| `dms-doc-history` | Document page, History | Field changes with Before and After | edits made | Ioana | 12 |
| `dms-doc-attachments` | Document page, Attachments | Permit 12/2026 with Site plan, 14 Linden Street attached | | Ioana | 5, 12 |
| `dms-viewer-text` | Document page | Site plan: **What to show** on **Copy with text**, **View the text** open | OCR done | Ioana | 13 |
| `dms-desk-staff` | My desk | Ioana's tiles, charts and recently modified | all of Session C | Ioana | 1, 9 |
| `dms-ex-contract-upload` | Library, Contracts 2026 | **Upload a document** with the contract, **Document type** Contract | | Radu | 5 |
| `dms-ex-contract-metadata` | Document page, Metadata | The contract's six fields filled | | Radu | 5 |
| `dms-ex-contract-validated` | Document page | Validated, "Waiting for one signature" | request sent to Mihai | Radu | 5 |
| `dms-lifecycle-approve` | Document page | Signed contract with **Approve** offered | signed | Mihai | 5, 14 |
| `dms-ex-contract-published` | Document page | Published, "Signed", Signatures tab | approved and published | Radu | 5 |
| `dms-checkout-bar` | Document page | "You have checked this document out…" bar on School gym renovation works | checked out | Radu | 13 |
| `dms-versions-tab` | Document page, Versions | IT support contract: three versions, "Current", label final | versions added | Radu | 13 |
| `dms-versions-compare` | Document page | "Comparing versions 1 and 2" | text versions | Radu | 13 |
| `dms-edit-online` | Online editor | IT support contract open in the editor, **Close the editor** | editor on | Radu | 13 |
| `dms-search-advanced` | Search | **Advanced search**: Type is Contract and Value in lei greater than 100000 | contracts | Radu | 15 |
| `dms-search-save` | Search | **Save the search** dialog, **Show in the sidebar as a virtual folder** ticked | | Radu | 15 |
| `dms-virtual-folder` | Virtual folder | "Contracts over 100,000 lei" and its sidebar entry | saved | Radu | 15 |
| `dms-collection-new` | Collections | **New collection** dialog filled | | Elena | 18 |
| `dms-collection-page` | Collection | Three documents, recipient Radu Florea | | Radu | 18 |
| `dms-pd-classify` | Document page | "Personal-data classification" dialog on the ramp petition: **Holds personal data**, **Special categories**, Health data | | Carmen | 20 |
| `dms-pd-document` | Document page | Petition on street parking: the personal-data pill and the **Personal data** card | | Andrei | 20 |
| `dms-pd-reason` | Document page | **Reason for access** dialog over the ramp petition, a reason typed | classified as special | Andrei | 20 |
| `dms-lifecycle-archive` | Document page | "Archive the document?" on Mayor's order 41/2026 | Published | Carmen | 14 |
| `dms-desk-archivist` | My desk | Carmen's desk with the archive tiles | | Carmen | 9 |
| `dms-doc-archive-tab` | Document page, Archive | Permit 12/2026: **Kept**, **Term ends**, **Entered the DMS**, reception, preservation | | Carmen | 12 |
| `dms-doc-audit-tab` | Document page, Audit log | The permit's entries | | Elena | 36 |
| `dms-review` (R2) | To review | A proposal for Application, 9 River Street: **Field**, **Now**, **Proposed** | filing proposals on | Ioana | 19 |
| `dms-search-ai` (R2) | Search, AI mode | A question about building permits and the agent's documents | AI mode on | Ioana | 15 |

**Session D: the archive** (as Carmen Pavel unless noted)

| Id | Screen | State to show | Data | As | Pages |
|---|---|---|---|---|---|
| `dms-dosar-close` | Library, Invoices 2014 | 'Close the dosar "Invoices 2014"?' with **Year in which the dosar ends** 2014 | its three invoices filed and archived | Carmen | 7, 33 |
| `dms-library-closed` | Library, Petitions 2019 | Closed dosar: "Closed" facts and the closed message | closed | Carmen | 10 |
| `dms-archive-overview` | Archive › Overview | Tiles with the terms by year and the nomenclator in force | all dosare | Carmen | 1, 21 |
| `dms-archive-without-entry` | Dosare without an entry | Miscellaneous listed with **Choose the entry** | | Carmen | 21 |
| `dms-selection-term-ended` | Selection | **Term ended**: Invoices 2014 and Petitions 2019 | | Carmen | 7, 25 |
| `dms-selection-start` | Selection | **Start a selection** dialog | | Carmen | 7 |
| `dms-selection-proposal` | Selection detail | Proposal step: both dosare, **Leave out** used on Petitions 2019 | | Carmen | 7, 25 |
| `dms-selection-pv` | Selection detail | **Issue the proces-verbal** dialog with the commission's names (Carmen Pavel, Mihai Stan, Radu Florea) | | Carmen | 7 |
| `dms-selection-answer` | Selection detail | **Record the answer** dialog: confirmed in full, answer no. 88 of the Arhivele Naționale | marked as sent | Carmen | 7 |
| `dms-selection-schedule` | Selection detail | **Schedule the deletion** with the proces-verbal number typed | confirmed | Carmen | 7, 25 |
| `dms-selection-scheduled` | Selection detail | "Deletion scheduled" with its date and **Cancel the deletion** | | Carmen | 7 |
| `dms-selection-hold` | Library, Contracts 2026 | **Hold the dosar** dialog with a reason (the snow clearing dispute) | | Carmen | 25 |
| `dms-handover-permanent` | Handover | **Permanent dosare**: Mayor's orders 1995, due 2025 | | Carmen | 7, 26 |
| `dms-handover-proposal` | Handover detail | Proposal with the dosar, **Prepare the package** | **Start a handover**, **Add dosare** | Carmen | 7, 26 |
| `dms-handover-prepare` | Handover detail | **Prepare the package** dialog: who hands over, the recipient, who approves | | Carmen | 7 |
| `dms-handover-ready` | Handover detail | "Package ready", **Download the package**, **Record the confirmation** | package built | Carmen | 7, 26 |
| `dms-handover-confirm` | Handover detail | **Record the confirmation**: received in full, no. 412 | | Carmen | 7 |
| `dms-handover-done` | Handover | **Handed over** tab with the dosar | | Carmen | 7, 26 |
| `dms-pv-register` | Procese-verbale | The selection and handover procese-verbale in the list (not their PDFs) | | Carmen | 7, 23 |
| `dms-audit-entries` | Audit log | **Entries** filtered by **Person** Radu Florea | | Victor | 4, 36 |
| `dms-audit-bundle` | Audit log | **Investigation bundle** dialog with a reason | | Victor | 36 |
| `dms-pd-register` | Personal data | **Register** tab | | Dana | 20 |
| `dms-pd-reasons` | Personal data | **Reasons for access** with Andrei's reason from Session C | | Dana | 20 |
| `dms-reception` (R2) | Reception | **Not accepted** with one document (a signed PDF changed after signing) | that file | Carmen | 22 |
| `dms-reception-accept` (R2) | Reception | **Accept into the archive** with a reason | | Carmen | 22 |
| `dms-integrity` (R2) | Integrity | After **Run a check now**: last check, no mismatches | | Elena | 23 |
| `dms-formats` (R2) | Archival formats | **Registry** tab | | Carmen | 24 |
| `dms-doc-preservation` (R2) | Document page, Archive | The preservation block of Mayor's order 41/2026: archival copy valid, time stamp | | Carmen | 24 |
| `dms-timestamps` (R2) | Time stamps | **In work** tab | authority on | Carmen | 24 |
| `dms-reports` (R2) | Reports | **Reports** tab: the models and **Run** | | Elena | 27 |
| `dms-reports-editor` (R2) | New report | Editor with Period this month, grouping by person | | Elena | 27 |
| `dms-reports-run` (R2) | A run | Its table and downloads | run made | Elena | 27 |
| `dms-alerts-todo` (R2) | Alerts | **To handle** with a "Repeated refusals" alert about Andrei Ionescu | ten refused opens by Andrei in 15 minutes | Dana | 28 |
| `dms-alerts-close` (R2) | Alerts | **Close** with the conclusion **Justified** and a comment | taken | Dana | 28 |

**Session E: seven days later** (as Carmen Pavel)

| Id | Screen | State to show | Data | Pages |
|---|---|---|---|---|
| `dms-selection-deleted` | Selection | **Deleted documents**: the three invoices of 2014 | the scheduled deletion ran | 25 |

Totals: Session A 26, B 8, C 50, D 34, E 1: 119 screenshots. Release 1 uses 104; the 14 marked R2 and `dms-selection-deleted` go with Task 24.

---

## D. Site changes

### What changes

| File | Change |
|---|---|
| `src/lib/product.mjs` | Add the product `dms`: `PRODUCT_LABEL.dms = 'Surogate DMS'`, `PRODUCT_HOME.dms = '/dms/'`, `TRACK_LABEL.dms = 'Surogate DMS'`, `TRACK_HOME.dms = '/dms/'`; `productFor` returns `'dms'` for the `dms` track; JSDoc unions gain `'dms'`. |
| `src/lib/product.test.mjs` | Assertions for the `dms` track and product. |
| `src/components/brand/DmsMark.astro` | New placeholder mark (decision 7). |
| `src/components/Header.astro` | The product list becomes `['agents', 'keel', 'dms']`; the comment says three products. |
| `src/components/MobileMenuFooter.astro` | The same list. |
| `src/components/Sidebar.astro` | The product head picks the mark by product (Agents, Keel, DMS); no track switch on DMS pages. |
| `src/components/PageTitle.astro` | No change: a product that is not `agents` already gets "product / page", as Keel does. A test proves it. |
| `src/components/home/ProductCards.astro` | Third card (DMS mark, "Surogate DMS", one line, `MiniDms`, **Open the DMS docs** to `/dms/`, **Quickstart** to `/dms/quickstart/`); the heading "Three products, built to work together."; the intro gains one sentence on the DMS; `.card` flex basis lowered so three fit in one row at 1200 px. |
| `src/components/home/MiniDms.astro` | New drawing in the house style: a folder tree beside a document with a state chip and a stamp, grey bars for text. |
| `src/components/home/UseCases.astro` | Third column of five DMS tasks; the mark chosen by product; `.column` flex basis lowered for three columns. |
| `src/content/docs/index.mdx` | `description` and `hero.tagline`: "Guides, tutorials and reference for Surogate Agents, Keel and Surogate DMS." |
| `astro.config.mjs` | The `dms` topic (section A); the Starlight `description`, `twitter:description` and `keywords` name Surogate DMS (keywords add "document management, records management, archive"); the topics comment says Keel and Surogate DMS are their own products. |
| `src/content/docs/dms/**` | The 39 pages. |
| `src/assets/screenshots/dms-*.png` | The screenshots. |
| `tests/test_header.py`, `tests/test_sidebar.py`, `tests/test_topics.py`, `tests/test_page_frame.py`, `tests/test_home.py`, `tests/test_content.py` | Updated for the third product (below). |
| `tests/test_dms_content.py` | New: rules on the DMS pages and screenshots (below). |

Unchanged: redirects (every DMS URL is new; `migration/check_routes.py` still checks the frozen baseline), the footer, the help band, the 404 page, the header's **Sign in** (it stays `https://ops.surogate.ai`, as on Keel pages: each institution has its own DMS address), `.github/workflows/deploy-docs.yml` (it already runs every check below). `llms.txt`, `llms-full.txt` and `llms-small.txt` pick the new pages up by themselves; the description change names the product in `llms.txt`.

### The five DMS tasks on the home page

| Title | Where | Link |
|---|---|---|
| File your first document and find it again | Quickstart | `/dms/quickstart/` |
| Have a contract signed and approved | Example | `/dms/examples/contract/` |
| Set up a new department with its roles and types | Administration | `/dms/examples/new-department/` |
| Select the dosare whose term has ended | Archive | `/dms/archive/selection/` |
| Hand permanent dosare over to the National Archives | Archive | `/dms/archive/handover/` |

### Tests: what each asserts

- `src/lib/product.test.mjs`: `trackFor('dms') === 'dms'`, `trackFor('dms/admin/people') === 'dms'`, `trackFor('dmsx') === null`, `productFor('dms/work/search') === 'dms'`, and the existing assertions unchanged.
- `tests/test_header.py`: on `/`, `/work/quickstart/`, `/keel/` and `/dms/`, the header holds "Surogate Agents", "Keel" and "Surogate DMS"; on `/dms/quickstart/` the current product is Surogate DMS and only one product link is current.
- `tests/test_sidebar.py`: `/dms/admin/people/` has the product head "Surogate DMS" and no track switch.
- `tests/test_topics.py`: the DMS sidebar on `/dms/` lists `/dms/quickstart/` and no `/work/`, `/develop/` or `/keel/` page; the Work, Develop and Keel sidebars list no `/dms/` page; `/dms/` has no `rel="prev"` and `/dms/reference/faq/` no `rel="next"`.
- `tests/test_page_frame.py`: the breadcrumb of `/dms/quickstart/` reads `['Surogate', 'DMS', '/', 'Surogate', 'DMS', 'quickstart']`; on `/dms/` it reads `['Surogate', 'DMS']`.
- `tests/test_home.py`: the tagline above; three product cards; "Three products, built to work together."; links to `/dms/` and `/dms/quickstart/`; the five DMS tasks link where the table says.
- `tests/test_content.py`: the DMS quickstart renders a known caption as `<figcaption>` and its opening as the lead.
- `tests/test_dms_content.py` (source and build): every DMS page has `title` and `sidebar.label`, no em dash and no denylisted internal term; its opening is a paragraph of at most 250 characters; every image is a `dms-*.png` that exists, with alt text; every `dms-*.png` is 1600x900, at most 300 KB and used by a page; at most 40 DMS pages and 120 DMS screenshots; `dist/llms.txt` names Surogate DMS.

### Checks to run

`npm run test:unit`, `npm run build` (the links validator runs inside it), `npm run check`, `npm run assert`, `python3 -m unittest discover -s migration -p 'test_*.py'`, `python3 migration/check_routes.py`, `npm run test:site`. `node_modules` is not installed in this checkout: run `npm ci` once before the first build.

---

## File map

| File | Responsibility |
|---|---|
| `src/lib/product.mjs`, `product.test.mjs` | Route id to product and track, with DMS |
| `src/components/brand/DmsMark.astro` | The DMS placeholder mark |
| `src/components/Header.astro`, `MobileMenuFooter.astro`, `Sidebar.astro` | Three products in the nav, the menu and the sidebar head |
| `src/components/home/ProductCards.astro`, `UseCases.astro`, `MiniDms.astro` | The DMS on the home page |
| `src/content/docs/index.mdx`, `astro.config.mjs` | Tagline, description, meta, the `dms` topic |
| `src/content/docs/dms/**` | The guide |
| `src/assets/screenshots/dms-*.png` | Its screenshots |
| `tests/test_*.py`, `tests/test_dms_content.py` | Checks on the built site and on the guide's sources |
| `/home/administrator/work/flavius/dms-slices/shots/` (outside the repo, never committed) | The capture kit: `make-files.mjs`, `capture.mjs`, `audit-labels.mjs`, `files/`, `out/`, `review.tsv` |

Every new component that a test targets carries `data-docs`; the existing names (`header`, `product-link`, `product-head`, `track-switch`, `breadcrumb`, `product-card`, `task`) cover the DMS too.

---

## E. Tasks

### Task 1: The product library knows the DMS

**Files:** Modify `src/lib/product.mjs`, `src/lib/product.test.mjs`

- [ ] **Step 1: Write the failing tests** in `product.test.mjs`:

```js
test('dms', () => {
  assert.equal(trackFor('dms'), 'dms');
  assert.equal(trackFor('dms/admin/people'), 'dms');
  assert.equal(trackFor('dmsx'), null);
  assert.equal(productFor('dms'), 'dms');
  assert.equal(productFor('dms/work/search'), 'dms');
});
```

- [ ] **Step 2: Run** `npm ci` (once), then `npm run test:unit`. Expected: the `dms` test FAILS (`trackFor('dms')` is null).
- [ ] **Step 3: Implement**: add `dms` to the four maps and to `productFor` (`track === 'keel' ? 'keel' : track === 'dms' ? 'dms' : 'agents'`), update the JSDoc unions.
- [ ] **Step 4: Run** `npm run test:unit`. Expected: all PASS.
- [ ] **Step 5: Commit**: `git add src/lib/product.mjs src/lib/product.test.mjs && git commit -m "docs(site): the product library knows Surogate DMS as a third product"`

### Task 2: The DMS topic, header, menu, sidebar head and a first welcome page

**Files:** Create `src/components/brand/DmsMark.astro`, `src/content/docs/dms/index.md`. Modify `astro.config.mjs`, `src/components/Header.astro`, `src/components/MobileMenuFooter.astro`, `src/components/Sidebar.astro`, `tests/test_header.py`, `tests/test_sidebar.py`, `tests/test_topics.py`, `tests/test_page_frame.py`.

- [ ] **Step 1: Write the failing tests** of section D that need only the welcome page: "Surogate DMS" in the header on `/`, `/work/quickstart/`, `/keel/` and `/dms/`; the DMS sidebar on `/dms/` lists no other product's page and the other sidebars list no `/dms/` page; the breadcrumb on `/dms/` reads `['Surogate', 'DMS']`; `/dms/` has no `rel="prev"`; the product head on `/dms/` says "Surogate DMS" with no track switch. The cases on `/dms/quickstart/`, `/dms/admin/people/` and `/dms/reference/faq/` are added by Tasks 12, 17 and 20, with their pages.
- [ ] **Step 2: Build and run**: `npm run build && npm run test:site`. Expected: the build FAILS or the new tests FAIL (no `/dms/` page, no third product).
- [ ] **Step 3: Implement**: `DmsMark.astro` (an SVG like `KeelMark.astro`: a `#9b1f61` square, a white page with a folded corner and three bars); the products list in `Header.astro` and `MobileMenuFooter.astro`; the mark by product in `Sidebar.astro`; the `dms` topic with the single item `'dms'`; a first `dms/index.md` with its front matter (`title: Surogate DMS`, `sidebar.label: Welcome`) and its lead paragraph only.
- [ ] **Step 4: Run** `npm run build && npm run check && npm run test:site && npm run assert`. Expected: all PASS; `dist/dms/index.html` exists.
- [ ] **Step 5: Commit**: `git commit -m "docs(site): Surogate DMS is a third product with its own sidebar, in the nav, the menu and the breadcrumb"`

### Task 3: The guide's own checks

**Files:** Create `tests/test_dms_content.py`

- [ ] **Step 1: Write the test**:

```python
import re
import struct
import unittest
from pathlib import Path

from docsite import DIST

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'src/content/docs/dms'
SHOTS = ROOT / 'src/assets/screenshots'
IMAGE = re.compile(r'!\[([^\]]*)\]\(((?:\.\./)+assets/screenshots/([^)]+))\)')
DENY = re.compile(
    r'\bDMS_[A-Z_]+|kubernetes|kubectl|\bk3s\b|\bhelm\b|docker|postgres|opensearch|minio|alembic|webhook|openapi'
    r'|verapdf|euro-office|bagit|e-ark|grant-admin|environment variable|\bworker\b|\bcron\b|x-sdms|surogates runtime'
    r'|hash chain',
    re.I,
)


def pages():
    return sorted(PAGES.rglob('*.md'))


def split(path):
    text = path.read_text(encoding='utf-8')
    front, body = re.match(r'\A---\n(.*?)\n---\n(.*)\Z', text, re.S).groups()
    return front, body


class DmsContent(unittest.TestCase):
    def test_front_matter(self):
        for p in pages():
            front, _ = split(p)
            self.assertRegex(front, r'(?m)^title:\s*\S', p)
            self.assertRegex(front, r'(?m)^sidebar:\n\s+label:\s*\S', p)

    def test_no_em_dash_and_no_internals(self):
        for p in pages():
            text = p.read_text(encoding='utf-8')
            self.assertNotIn('\u2014', text, p)
            self.assertIsNone(DENY.search(text), f'{p}: {DENY.search(text)}')

    def test_opening_is_a_short_paragraph(self):
        for p in pages():
            _, body = split(p)
            first = body.strip().split('\n\n')[0]
            self.assertFalse(first.startswith(('#', '!', '|', '-', '1.', ':::', '<')), p)
            self.assertLessEqual(len(re.sub(r'[*`]|\[([^\]]*)\]\([^)]*\)', r'\1', first)), 250, p)

    def test_images(self):
        used = set()
        for p in pages():
            for alt, _, name in IMAGE.findall(p.read_text(encoding='utf-8')):
                self.assertTrue(alt.strip(), f'{p}: {name} has no alt text')
                self.assertRegex(name, r'^dms-[a-z0-9-]+\.png$')
                self.assertTrue((SHOTS / name).exists(), f'{p}: {name} missing')
                used.add(name)
        files = sorted(SHOTS.glob('dms-*.png'))
        for f in files:
            width, height = struct.unpack('>II', f.read_bytes()[16:24])
            self.assertEqual((width, height), (1600, 900), f.name)
            self.assertLessEqual(f.stat().st_size, 300_000, f.name)
            self.assertIn(f.name, used, f'{f.name} is used by no page')
        self.assertLessEqual(len(files), 120)
        self.assertLessEqual(len(pages()), 40)

    def test_llms_txt_names_the_product(self):
        self.assertIn('Surogate DMS', (DIST / 'llms.txt').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: `test_llms_txt_names_the_product` FAILS until the description names the DMS; the rest PASS on the one welcome page.
- [ ] **Step 3: Implement**: the `description`, `twitter:description` and `keywords` changes in `astro.config.mjs` (section D). If `starlight-llms-txt` writes its files under other names, point the test at the file it writes.
- [ ] **Step 4: Run** `npm run build && npm run test:site`. Expected: all PASS.
- [ ] **Step 5: Commit**: `git commit -m "docs(dms): checks on the guide's pages and screenshots, and the site's description names Surogate DMS"`

### Task 4: The capture kit (outside the repo)

**Files (not committed):** `/home/administrator/work/flavius/dms-slices/shots/` (`playwright-core` is already installed there): `make-files.mjs`, `capture.mjs`, `files/`, `out/`, `review.tsv`.

- [ ] **Step 1:** In the shots folder, `npm install sharp exceljs docx` (this folder is outside every repository).
- [ ] **Step 2: `make-files.mjs`** generates the demo files of section C.1 into `files/`: each PDF from a small HTML template with an "Example City Hall" letterhead through Playwright's `page.pdf()` (A4); the 1995 orders and the site plan as image-only PDFs (render the HTML to PNG with a slight grey and a 0.6 degree turn, then print an `<img>` page to PDF), so OCR runs on them; the IT support contract as a `.docx` with `docx`; the nomenclator edition and the org-chart import from the templates the DMS downloads (filled with `exceljs`); the invoice manifest later, from the Import page's template. Expected: `ls files/` lists 29 document files, `nomenclator-2026.1.xlsx`, `org-hr.xlsx`.
- [ ] **Step 3: `capture.mjs`** with:
  - `chromium.launch({ executablePath: '/usr/bin/google-chrome', headless: true })`, a context with `viewport {1600, 900}`, `deviceScaleFactor: 1`, `locale: 'en-US'`, `colorScheme: 'light'`, `timezoneId: 'Europe/Bucharest'`, and an init script that sets `localStorage['sdms.theme'] = 'light'` and `localStorage['sdms.language'] = 'en'`;
  - credentials read from `~/.config/surogate-dms/docs-demo.env`, never logged; the script signs in as the demo administrator Elena Marin unless the shot list names another account;
  - `signIn(who)`: open the sign-in page, fill **Email address** and **Password**, press **Sign in**; if the user bar's language button shows `RO`, press it once (the choice is saved on the account);
  - `shot(id)`: wait for network idle and for no "Processing" chip or skeleton, then refuse to save when `document.documentElement` has the `dark` class, when the language button does not show `EN`, when a toast or alert with an error tone is visible, or when the page's text contains a Romanian label from a list built from `ro.ts` (values of the `nav.*`, `desk.*`, `upload.*` and `document.tab.*` keys that differ from `en.ts`, minus Nomenclator and Procese-verbale); then `page.screenshot()`, quantise to an 8-bit palette with `sharp(...).png({ palette: true })` (as the Keel screenshots are), check 1600x900 and the size, and append `id, url, account, time` to `out/manifest.tsv`;
  - a slow-network helper (CDP `Network.emulateNetworkConditions`) for `dms-upload-tray`;
  - one function per session (A to E) that drives the steps of section C in order and calls `shot()` where the shot list says.
- [ ] **Step 4: Dry run** against the sign-in page only: `node capture.mjs --only dms-sign-in`. Expected: `out/dms-sign-in.png`, 1600x900, under 300 KB, light, English.

No commit: nothing in this task is in the repo.

### Task 5: The capture installation is ready

- [ ] **Step 1:** Check each prerequisite of section C.2 by signing in as Elena Marin with the kit: the sidebar shows **Administration**; **Signatures** shows an internal certificate authority; the operator confirms the online editor is on (it is first used in session C, on the IT support contract); the Library is empty; the operator confirms the other seven accounts exist (nobody signs in with them before session C, so every desk starts empty). Expected: all yes, or stop and ask the owner for the missing item.
- [ ] **Step 2:** Record the DMS commit the installation runs (from its operator) in `review.tsv`'s header; the PR names it.

No commit.

### Task 6: Capture session A, administration setup

- [ ] **Step 1:** Run session A. It builds, in order: unit types, units and positions (the Human Resources part by Excel import), people (eight added; they read "Pending" until each signs in during later sessions), holders, the nomenclator `2026.1` (import, choose units, approval, put in force), root folders, library folders and their entries (the 2014, 2019 and 1995 dosare left open "When you close it"), the taxonomy, document types, the role Approver, grants, the after-hours rule.
- [ ] **Step 2:** Expected: the 26 Session A files in `out/`, each listed in `out/manifest.tsv`.

No commit (the content tasks copy the screenshots into the repo, after Task 10's review).

### Task 7: Capture session B, the new department

- [ ] **Step 1:** Run session B: the unit and positions, Sorin Neagu, edition `2026.2` by **Copy into a new edition** with the typed entry V-1, approval and **Put in force**, the dosar Tender files 2026, the type Tender file, the grant.
- [ ] **Step 2:** Expected: 7 files (`dms-people-list` waits for the end of session D).

### Task 8: Capture session C, daily work

- [ ] **Step 1:** Run session C in the order of its table: the quickstart walk as Ioana first (so `dms-shell-staff` shows an empty desk), then the uploads, the contract walk as Radu and Mihai, versions and the editor, search, the collection, personal data, archiving as Carmen; then the remaining documents of section C.1 (the import of the four invoices, the petitions, the orders, the old dosare's documents, archived by Carmen). `dms-desk-staff` and `dms-desk-archivist` are taken last.
- [ ] **Step 2:** Expected: 48 files, plus the two R2 files when those features are on.

### Task 9: Capture session D, the archive, and the later pass

- [ ] **Step 1:** Run session D in the order of its table: it closes Invoices 2014 (`dms-dosar-close`), then Petitions 2019 and Mayor's orders 1995 with their end years, before `dms-library-closed`; make the ten refused opens as Andrei before the alert shots; take `dms-people-list` last.
- [ ] **Step 2:** Expected: 23 R1 files and up to 11 R2 files.
- [ ] **Step 3:** Seven days after the scheduled deletion, run session E. Expected: `dms-selection-deleted.png`. Until it exists, page 25 goes without it (its line is added in Task 24).

### Task 10: Review every screenshot

- [ ] **Step 1:** Open every file in `out/` (the Read tool shows images) and check, writing one line per file in `review.tsv` (`id, ok or the problem`): light theme; English everywhere but the five kept terms; no error toast, no spinner, no half-loaded viewer; the account and state the shot list names; only demo names and `example.org` addresses; no proces-verbal PDF or Excel content on screen; the caption the page will give it is true of the picture.
- [ ] **Step 2:** Retake every shot marked with a problem (`node capture.mjs --only <id>`), and look again.
- [ ] **Step 3:** Keep the reviewed files in `out/`. Each content task (Task 11 onwards) copies into `src/assets/screenshots/` only the files its pages use, and commits them with the pages: the image test fails on a screenshot no page uses. R2 files wait for Task 24.

No commit in this task.

### Task 11: Welcome, concepts and glossary

**Files:** `src/content/docs/dms/index.md` (full text), `dms/concepts.md`, `dms/reference/glossary.md`; `astro.config.mjs` (their sidebar items); their screenshots.

- [ ] **Step 1:** Write the three pages from section A (pages 1, 2, 38), in the Keel welcome's and concepts' structure; the welcome's "Start here" table links only to pages that exist by the end of this plan's R1; until a target page exists, leave its row out and add it in the task that creates the page.
- [ ] **Step 2: Run** `npm run build && npm run test:site && npm run assert`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): the welcome page, the concepts and the glossary"`

### Task 12: Quickstart for staff

**Files:** `dms/quickstart.md`; `astro.config.mjs`; its screenshots; `tests/test_content.py`, `tests/test_page_frame.py`, `tests/test_header.py` (the `/dms/quickstart/` cases).

- [ ] **Step 1:** Add the failing tests: the caption of `dms-upload-dialog` appears as `<figcaption>` on `/dms/quickstart/`, the lead class is there, the breadcrumb reads `['Surogate', 'DMS', '/', 'Surogate', 'DMS', 'quickstart']`, and the header marks Surogate DMS current.
- [ ] **Step 2:** Write the page (section A, page 3) in Keel's quickstart shape: "You need:", ten numbered sections, "Next steps". Time it by doing the walk once in the demo: it should take about ten minutes.
- [ ] **Step 3: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 4: Commit**: `git commit -m "docs(dms): a ten-minute quickstart for staff, from sign-in to a signed document"`

### Task 13: Quickstart for administrators

**Files:** `dms/quickstart-admin.md`; `astro.config.mjs`; its screenshots.

- [ ] **Step 1:** Write page 4 in the order of section A. Each step names the page in the sidebar, the button, and what to check before the next step; it ends with "Check as a staff member" and "Read the audit log".
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): a quickstart for administrators, in the order the DMS needs its setup"`

### Task 14: Daily work, part 1

**Files:** `dms/work/sign-in.md`, `my-desk.md`, `library.md`, `upload.md`; `astro.config.mjs`; their screenshots.

- [ ] **Step 1:** Write pages 8 to 11.
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): signing in, My desk, the library, uploading and importing"`

### Task 15: Daily work, part 2

**Files:** `dms/work/document-page.md`, `versions.md`, `lifecycle.md`; `astro.config.mjs`; their screenshots.

- [ ] **Step 1:** Write pages 12 to 14. The lifecycle's "who may" table uses the built-in roles as the **Roles and permissions** page showed them at capture.
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): the document page, viewing, editing and versions, and the life of a document"`

### Task 16: Daily work, part 3

**Files:** `dms/work/search.md`, `comments.md`, `signing.md`, `favorites-and-collections.md`, `personal-data.md`; `astro.config.mjs`; their screenshots.

- [ ] **Step 1:** Write pages 15 to 18 and 20. Search's syntax comes from the **Search tips** card as captured, not from the DMS guide.
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): search, comments, signing, favorites and collections, and personal data"`

### Task 17: Administration pages

**Files:** `dms/admin/org-chart.md`, `people.md`, `roles.md`, `document-types.md`, `folders.md`, `nomenclator.md`, `audit-log.md`; `astro.config.mjs`; their screenshots; `tests/test_sidebar.py` (the `/dms/admin/people/` case).

- [ ] **Step 1:** Add the failing sidebar test for `/dms/admin/people/`.
- [ ] **Step 2:** Write pages 29 to 34 and 36. Where the admin guide describes something done outside the UI (accounts, the first administrator, the certificate authority, schedules, the institution's name), write one sentence: "Your operator sets this up."
- [ ] **Step 3: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 4: Commit**: `git commit -m "docs(dms): the Administration pages: org chart, people, roles, document types, folders, nomenclator, audit log"`

### Task 18: Archive pages

**Files:** `dms/archive/overview.md`, `selection.md`, `handover.md`; `astro.config.mjs`; their screenshots.

- [ ] **Step 1:** Write pages 21, 25 and 26. Leave out every part of the package's inside and of the deletion's mechanics; keep what the archivist sees and decides.
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): the Archive overview, the selection of dosare and the handover to the National Archives"`

### Task 19: The three examples

**Files:** `dms/examples/contract.md`, `new-department.md`, `selection-and-handover.md`; `astro.config.mjs`; their screenshots.

- [ ] **Step 1:** Write pages 5 to 7 in the shape of Keel's mortgage example: what the example does, then the walk in sections, each with its screenshot, each linking to the page with the details. Every name, number and date matches the screenshots.
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 3: Commit**: `git commit -m "docs(dms): three worked examples: a contract, a new department, a selection and a handover"`

### Task 20: Roles reference and FAQ

**Files:** `dms/reference/roles.md`, `dms/reference/faq.md`; `astro.config.mjs`; `tests/test_topics.py` (the pagination case on `/dms/reference/faq/`).

- [ ] **Step 1:** Add the failing pagination test.
- [ ] **Step 2:** Write pages 37 and 39. The roles table is checked line by line against the **Roles and permissions** page (one screenshot per built-in role may be taken for the check; they are not published).
- [ ] **Step 3: Run** `npm run build && npm run test:site`. Expected: PASS.
- [ ] **Step 4: Commit**: `git commit -m "docs(dms): the built-in roles and the FAQ"`

### Task 21: The DMS on the home page

**Files:** Create `src/components/home/MiniDms.astro`. Modify `src/components/home/ProductCards.astro`, `src/components/home/UseCases.astro`, `src/content/docs/index.mdx`, `tests/test_home.py`.

- [ ] **Step 1: Write the failing tests** in `tests/test_home.py`: the new tagline in `test_hero`; `self.assertEqual(self.doc.count('data-docs="product-card"'), 3)`; "Three products, built to work together."; `href="/dms/"` and `href="/dms/quickstart/"`; the five DMS rows of section D appended to `TASKS`.
- [ ] **Step 2: Run** `npm run build && npm run test:site`. Expected: the home tests FAIL.
- [ ] **Step 3: Implement** section D's home changes. The DMS card's line: "Keep your institution's documents, from the first upload to the archive." The intro paragraph's new sentence: "Surogate DMS keeps an institution's documents: filing, finding, signing, retention and handover to the archive."
- [ ] **Step 4: Run** `npm run build && npm run check && npm run test:site`. Expected: PASS.
- [ ] **Step 5: Commit**: `git commit -m "docs(site): the home page shows Surogate DMS as the third product, with five tasks"`

### Task 22: Label and claim audit

**Files (not committed):** `/home/administrator/work/flavius/dms-slices/shots/audit-labels.mjs`.

- [ ] **Step 1:** Write `audit-labels.mjs`: read every string value of `frontend/src/i18n/en.ts` at the captured commit, turn `{name}` placeholders into wildcards; read every `**bold**` and every quoted UI message in `src/content/docs/dms/**`; print each one that matches no value. Run it. Expected: a list of misses.
- [ ] **Step 2:** For each miss: fix the page to the UI's words, or confirm it is not a label (a demo name, a field the demo made, a heading) and note it in `review.tsv`.
- [ ] **Step 3:** Read every page against the shot list and the screens it describes, and against both "Not available yet" lists: remove any claim of a feature the UI lacks and any paraphrased internal. Check each "who sees it" statement against the shot's account.
- [ ] **Step 4: Commit** the page fixes: `git commit -m "docs(dms): labels and claims checked against the English UI"`

### Task 23: Full checks and a look in the browser

- [ ] **Step 1: Run** `npm run test:unit && npm run build && npm run check && npm run assert && python3 -m unittest discover -s migration -p 'test_*.py' && python3 migration/check_routes.py && npm run test:site`. Expected: every command PASSES; the build reports no broken link or anchor.
- [ ] **Step 2:** `npm run preview` and open, at 1280, 1024, 820 and 375 px, in light and dark: the home page, `/dms/`, `/dms/quickstart/`, `/dms/admin/roles/`, `/dms/examples/selection-and-handover/`. Expected: the header does not overflow (if it crowds, narrow the search field below 64rem in `Header.astro`), the three cards and columns stack on a phone, the DMS sidebar opens in the menu, screenshots keep their light look and 1 px frame in dark mode, captions sit under them.
- [ ] **Step 3: Commit** any fix: `git commit -m "docs(site): the header and home fit three products at every width"`

### Task 24: Release 2 pages

**Files:** `dms/work/to-review.md`, `dms/archive/reception.md`, `integrity.md`, `preservation.md`, `reports.md`, `alerts.md`, `dms/admin/signatures.md`; `astro.config.mjs`; the R2 screenshots and `dms-selection-deleted.png`; `dms/work/search.md` (the AI mode section), `dms/archive/selection.md` (the deleted documents picture), `dms/index.md` (Start here rows).

- [ ] **Step 1:** Take or retake the R2 shots once their features are on, and session E; review them as in Task 10.
- [ ] **Step 2:** Write pages 19, 22, 23, 24, 27, 28 and 35, and the two additions.
- [ ] **Step 3:** Run the label audit of Task 22 on the new text, then the checks of Task 23 Step 1. Expected: PASS.
- [ ] **Step 4: Commit**: `git commit -m "docs(dms): filing proposals, reception, integrity, archival copies and time stamps, reports, alerts and electronic signatures"`

No push in any task: the owner opens the PR.

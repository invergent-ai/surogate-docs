---
title: Built-in roles and permissions
sidebar:
  label: Built-in roles
---

For everyone who wants to know what a role may do: the built-in roles and their permissions, as the **Roles and permissions** page shows them in a new installation. Your administrator may have changed them or made other roles.

## The built-in roles

- **Standard user**: files, edits, comments on and validates documents, and asks for signatures.
- **Registrar**: registers documents, reads the registry and its registrations, reads, uploads and comments on documents, and works the captures of its units.
- **Capture operator**: works the captures of its units: reads, uploads and comments on documents, with access to documents with personal data. It has no registry permissions.
- **Electronic archivist**: everything a standard user does, and approves, publishes, archives and reopens documents, manages folders, runs the selection and the handover, and accepts documents that failed their reception checks.
- **Archive administrator**: everything an archivist does, and administers the DMS: document types, the org chart, people, roles, collections, signatures, the nomenclator, the audit log, and the capture channels, separator sheets, templates and flows.
- **Auditor**: reads documents and the audit log, the archive, the integrity checks and the alerts.
- **Data protection officer (DPO)**: sees the personal-data register and the reasons for access, the alerts and the audit log, and manages the personal-data categories; does not read documents.
- **Access to special data**: opens documents that hold special categories of personal data. It is given in addition to another role.
- **Integration**: the role of connected systems, which act on behalf of a person. People do not hold it.

## Permissions by role

| Permission | Standard user | Registrar | Capture operator | Electronic archivist | Archive administrator | Auditor | Data protection officer (DPO) | Access to special data | Integration |
|---|---|---|---|---|---|---|---|---|---|
| Reads documents | yes | yes | yes | yes | yes | yes |  |  |  |
| Uploads documents | yes | yes | yes | yes | yes |  |  |  |  |
| Edits documents | yes |  |  | yes | yes |  |  |  |  |
| Moves documents |  |  |  | yes | yes |  |  |  |  |
| Comments | yes | yes | yes | yes | yes |  |  |  |  |
| Unlocks checked-out documents |  |  |  |  | yes |  |  |  |  |
| Validates | yes |  |  | yes | yes |  |  |  |  |
| Approves |  |  |  | yes | yes |  |  |  |  |
| Publishes |  |  |  | yes | yes |  |  |  |  |
| Archives |  |  |  | yes | yes |  |  |  |  |
| Reopens |  |  |  | yes | yes |  |  |  |  |
| Manages folders |  |  |  | yes | yes |  |  |  |  |
| Asks for signatures | yes |  |  | yes | yes |  |  |  |  |
| Access to documents with personal data | yes | yes | yes | yes | yes | yes | yes |  |  |
| Access to documents with special data (GDPR art. 9 and 10) |  |  |  |  | yes |  | yes | yes |  |
| Classifies a document's personal data |  |  |  | yes | yes |  |  |  |  |
| Manages document types |  |  |  |  | yes |  |  |  |  |
| Manages the org chart |  |  |  |  | yes |  |  |  |  |
| Manages roles and permissions |  |  |  |  | yes |  |  |  |  |
| Manages people |  |  |  |  | yes |  |  |  |  |
| Manages collections |  |  |  |  | yes |  |  |  |  |
| Consults the audit log |  |  |  |  | yes | yes | yes |  |  |
| Manages electronic signatures |  |  |  |  | yes |  |  |  |  |
| Manages the nomenclator |  |  |  |  | yes |  |  |  |  |
| Sees registrations | yes | yes |  |  | yes | yes |  |  |  |
| Registers documents |  | yes |  |  | yes |  |  |  |  |
| Cancels registrations |  |  |  |  | yes |  |  |  |  |
| Manages the registers |  |  |  |  | yes |  |  |  |  |
| Process captures |  | yes | yes |  | yes |  |  |  |  |
| Manage capture |  |  |  |  | yes |  |  |  |  |
| Reads the archive |  |  |  | yes | yes | yes | yes |  |  |
| Sees the integrity checks, the incidents and their procese-verbale |  |  |  | yes | yes | yes |  |  |  |
| Starts checks, opens quarantined files, closes incidents, makes archival copies again and asks for time stamps |  |  |  | yes | yes |  |  |  |  |
| Closes the mismatches found in the audit log, with a note |  |  |  |  | yes |  |  |  |  |
| Accepts into the archive, with a written reason, documents that failed the reception checks |  |  |  | yes | yes |  |  |  |  |
| Prepares the selection: the proposal, the proces-verbal, the National Archives' answer and the holds |  |  |  | yes | yes |  |  |  |  |
| Orders the deletion of documents whose elimination was confirmed |  |  |  | yes | yes |  |  |  |  |
| Acts on behalf of another person (service accounts only) |  |  |  |  | yes |  |  |  | yes |
| Manages the personal-data categories, the purposes and the defaults |  |  |  |  | yes |  | yes |  |  |
| Sees the personal-data register and the reasons for access |  |  |  |  | yes |  | yes |  |  |
| Sees the unusual-activity alerts and their rules |  |  |  |  | yes | yes | yes |  |  |
| Receives the unusual-activity alerts, takes and closes them, and sets the rules |  |  |  |  | yes |  | yes |  |  |
| Prepares the handover of permanent documents to the National Archives: the package, the proces-verbal and the confirmation |  |  |  | yes | yes |  |  |  |  |

## How grants narrow a role

A role is given by a **grant**. A grant can apply to the whole institution or to one unit with or without its subunits, and can be limited to some document types and some states. Administration permissions apply only when the grant is for the whole institution, without such limits. **Manage capture** also applies only when it is granted for the whole institution. **Process captures** works in a unit only together with **Access to documents with personal data** in the same unit, because the pages of a capture may show personal data. See [Roles and permissions](/dms/admin/roles/).

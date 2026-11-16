---
title: Extension fields
description: The keys of the barcode, barcode scanner, IBAN and signature fields.
---

The configuration behind [Extension fields](/portal/sites/form-fields/). That page covers what each of the four fields does in a form and in the console.

## The fields

In a form's `components` (`forms/<id>.yaml`):

```yaml
- { type: textfield, key: receipt, label: Receipt number, input: true }
- { type: barcode, key: receiptCode, label: Receipt code, from: receipt, format: qrcode }
- { type: barcodeScanner, key: envelope, label: Code on the envelope, input: true, formats: [ean13, code128, qrcode] }
- { type: iban, key: account, label: Account to receive the money, input: true, countries: [RO], validate: { required: true } }
- { type: signature, key: signature, label: Signature, input: true, footer: Sign here, validate: { required: true } }
```

- `barcode`:
  - `text` (a fixed text) or `from` (the key of the field it follows), never both.
  - `format`: one of `qrcode`, `datamatrix`, `pdf417`, `code128`, `code39`, `ean13`, `ean8`, `upca` or `itf14`. Optional; `qrcode` when left out.
  - It needs no `input`, and sends nothing.
- `barcodeScanner`:
  - `formats`: a list of `qrcode`, `code128`, `ean13`, `ean8`, `upca`, `code39`, `itf`, `datamatrix` and `pdf417`. Optional; all when left out.
  - It takes `autocomplete` and the text checks under `validate`.
- `iban`:
  - `countries`: a list of countries by their two capital letters, such as `[RO]`. Optional; any country that uses IBANs when left out.
  - It takes `autocomplete`.
- `signature`:
  - `footer`: the text under the pad. Translate it under `i18n` like a label.
  - `width` and `height`: such as `100%` or `150px`, at most 2,000 by 1,000 pixels.
  - `penColor` and `backgroundColor`: such as `#1a2b3c`, `black` or `rgb(245, 245, 235)`.

## A signature saved as a file

A form's actions can save the signature as a PNG in one of the portal's [folders](/portal/console/files/), with `writeFile` and `encoding: dataUrl`. A [document action](/portal/sites/document-actions/) can put it in a PDF, as an `<img>` whose `src` is the signature.

In the same form's actions:

```yaml
actions:
  submitted:
    - type: writeFile
      folder: requests
      name: '"signature-" + submission.id + ".png"'
      content: form.signature
      encoding: dataUrl
```

- `encoding: dataUrl`: the content is the signature's image as the form sent it, and the file is that image.
- Only `writeFile` takes it; `readFile` reads `text` or `base64`.

## Whole number

In a form's `components` (`forms/<id>.yaml`), the portal's `integer` type:

```yaml
- { type: integer, key: places, label: Number of places, input: true, description: From 1 to 20., validate: { required: true, min: 1, max: 20 } }
```

- `validate.min` and `validate.max`: whole numbers, none larger than 9,007,199,254,740,991 either way, written as numbers (the console writes numbers). A bound that is not a whole number is refused with `integer_bounds`.
- It takes the common keys: `label`, `placeholder`, `description`, `validate.required`, a condition.
- The form sends a JSON number. The portal refuses a text, a number with decimals or one that is not exact: the submission is answered 400 `invalid`, with `errors: [{ path: "places", message: "integer" }]`. A number under `min` or over `max` is `min` or `max`. An empty value is kept as `null`, and `-0` as `0`.
- A "Fields from JSON" description may name the type `integer`, with `min` and `max`.

## Files

In a form's `components`:

```yaml
- type: files
  key: documents
  label: Supporting documents
  input: true
  multiple: true
  maxFiles: 3
  extensions: [pdf, jpg, png]
  maxSizeKb: 5120
  duplicates: rename
  validate: { required: true }
```

- `multiple`: whether the field takes many files. With it off, `maxFiles` is 1.
- `maxFiles`: 1 to 20, 5 when `multiple` leaves it out.
- `extensions`: at least one, from `pdf`, `doc`, `docx`, `xls`, `xlsx`, `odt`, `ods`, `csv`, `txt`, `jpg`, `jpeg`, `png` and `zip`, none twice. An extension of a file that runs or holds something that does (such as `exe`, `js`, `html`, `svg`, `docm` or `xlsm`) is refused with `files_active`.
- `maxSizeKb`: 1 to 25,600, 10,240 when left out.
- `duplicates`: `rename` (the default), `overwrite` or `refuse`.
- A form with a `files` field is not `offline` (`offline_files`).

The other reasons the console gives are `files_extensions`, `files_max_files`, `files_max_size`, `files_duplicates` and `files_multiple`.

**Uploading.** A file is sent before the form, one file a request:

```
POST /_portal/api/forms/<form>/files?field=<key>&name=<name>&site=<site>
content-type: application/octet-stream
x-portal-csrf: <token>
```

- The body is the file's bytes. Whoever may send the form may upload, with the same host, site, CSRF and visitor rules.
- It answers 201 `{ id, name, size }`, or 400, 413 or 429 with `{ error, message, setting? }`. `error` is `file_extension`, `file_content`, `file_size`, `file_empty`, `file_name`, `too_many` (a visitor sent more than 30 in a minute from one address) or `too_many_files` (100 are waiting for a person, 200 for all the visitors of a form).
- The last extension of the name, in lower case, must be in the field's list. The content must be what the extension says: a PDF's header, a JPEG's or PNG's signature, a compound file for `doc` and `xls`, the parts of an Office Open XML or OpenDocument ZIP with no macro, a ZIP, or UTF-8 text without NUL for `csv` and `txt`.
- The name loses its path, control characters and edge spaces, keeps its diacritics, and is at most 200 characters with its extension.
- The bytes go to the portal's files, under the form, never under the person's name.

**Sending.** The field's value is a list of `{ id, name, size }`.

- Each reference must be an upload of this sender (a person, or a visitor) to this field that no submission holds. The name and size kept are the upload's.
- The count is checked again (`file_count`). Names that read the same without regard to capitals are dealt with as `duplicates` says: `report (1).pdf`; the newest stays; or 400 `file_duplicate` with the name. A reference to a file that was never uploaded this way is 400 `file_unknown`.
- `validate.required` with no file is `required`.

**Waiting.** An upload that no submission holds is deleted after 24 hours, unless the person's draft of the form names it. A draft keeps only references to the person's own waiting uploads.

**Reading.** `GET /_portal/api/forms/<form>/submissions/<id>/files/<file>` is for the form's reviewers: for anyone else it is 404, checked at every download. It answers the bytes with `Content-Disposition: attachment`, `X-Content-Type-Options: nosniff` and a sandboxing `Content-Security-Policy`. The console lists the files as links. The CSV and the notification email carry their names only. Deleting a submission, or its retention purging it, deletes its files.

In an action, the field is a list: `form.documents` holds `{ id, name, size }` for each file.

## Fields from JSON

In a form's `components`:

```yaml
- type: jsonFields
  key: load
  label: Load details
  input: true
  source: value
  valueName: loadFields
```

`source` is one of four, and each takes its own keys:

| `source` | Takes | Where the JSON is |
|---|---|---|
| `text` | `jsonText` | The text, in the form: at most 256 KB, and a list of fields the console checks before saving |
| `file` | `folder`, `file` | A `.json` file of one of the portal's folders |
| `value` | `valueName` | The result of a [named value](/portal/developer/values/) |
| `web` | `connector`, `path`, `query`, `dependsOn` | The body of a GET through a web [connector](/portal/developer/connectors/) |

- `listPath`, for every source: where the list of fields is in the JSON, names and list positions joined by dots, such as `data.fields`. Empty or left out: the JSON is the list.
- `path`: added to the connector's address, with no `?`, `#`, `\` or `..`. `query` is a list of `name = expression` lines, each expression CEL of at most 500 characters. It reads `form.<key>` for the keys in `dependsOn` and nothing else of the form, and `user`, `site`, `locale`, `now` and `values`.
- `dependsOn`: the keys of other fields of the form. When one changes, the page asks for the fields again after 300 ms. It never names the container itself.
- `validate.required`: the form is refused when the fields could not be loaded.
- The other reasons the console gives are `json_fields_source`, `json_fields_text`, `json_fields_file`, `json_fields_value`, `json_fields_connector`, `json_fields_path`, `json_fields_query`, `json_fields_list_path`, `json_fields_depends`, and, when it names what the portal lacks, `json_fields_no_folder`, `json_fields_no_value` and `json_fields_no_connector`.

**The description.** A list of 1 to 50 objects, at most 256 KB:

```json
[
  { "key": "cantitate", "type": "integer", "label": { "ro": "Cantitate (kg)", "en": "Quantity (kg)" }, "required": true, "min": 0 },
  { "key": "ambalaj", "type": "select", "label": "Packaging", "options": [{ "value": "bag", "label": "Bag" }, { "value": "pallet", "label": "Pallet" }] }
]
```

- `key`: a letter, then letters, digits and underscores, at most 64. A key is never one of the form's own fields, and never twice.
- `type`: `text`, `textarea`, `number`, `integer`, `email`, `date`, `datetime`, `select`, `multiselect`, `radio`, `checkboxes`, `checkbox`, `slider` or `static`. `slider` is a number box for now; `date` and `datetime` are the browser's boxes, holding `YYYY-MM-DD` and `YYYY-MM-DDTHH:MM`; `static` shows its label and description as text, with no markup.
- `label` and `description`: a text, or `{ ro, en }`. A label is at most 300 characters, a description 1,000.
- `required`: true or false. `default` must fit the type.
- `options`: for `select`, `multiselect`, `radio` and `checkboxes`, 1 to 200 of `{ value, label }`, no value twice.
- `min`, `max` and `step`: for `number`, `integer` and `slider`, numbers (whole for `integer`); for `text` and `textarea`, whole lengths; for `date` and `datetime`, the first and last, as the type writes them.

One thing wrong refuses all of it. The reasons, as the page and the API say them, are `not_list`, `empty`, `too_large`, `too_many`, `bad_field`, `unknown_type`, `bad_key`, `duplicate_key`, `key_overlap`, `bad_label`, `bad_options`, `bad_default`, `bad_limits` and `not_json`.

**Asking for the fields.** The page asks when the form opens, and again when a field in `dependsOn` changes:

```
POST /_portal/api/forms/<form>/fields/<key>
{ "locale": "en", "values": { "waste_code": "18 01 03" }, "site": "main", "replaces": "<token>" }
```

- It answers 200 `{ token, fields, components }`, 502 `fields_unavailable` when the source cannot be read (an error, no answer in 5 seconds, a status that is not 2xx), 422 `fields_refused` with `reason` (and `field`) when the JSON is read but refused, or 429 `too_many` past 60 asks a minute from one place.
- A `value` or `web` source is read by the actions' own engine: its connectors, credentials, guarded calls and time limit are those of every form action. A visitor's call is made as a visitor.
- The portal keeps what it served for 24 hours under `token`.

**Sending.** The form is sent with the values under the container's key and the tokens:

```json
{ "locale": "en", "data": { "code": "LV-2041", "load": { "cantitate": 120 } }, "fieldTokens": { "load": "<token>" } }
```

- The values are checked as the form's own fields are, against the fields served under the token, not against what the source says now. A name the fields do not have is `unknown_field`; the errors name `load.cantitate`.
- A container that served nothing and was sent nothing is left out of the submission, unless it is required (`fields_unavailable`). Values sent with no token the portal knows are `fields_expired`.

**In actions.** The values are `form.<key>.<field>`, such as `form.load.cantitate`, in the form's [actions](/portal/developer/actions/). The Forms page, the CSV export and the notification email show them as `cantitate: 120`.

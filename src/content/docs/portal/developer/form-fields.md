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

- It answers 200 `{ token, fields, components }`, 502 `fields_unavailable` when the source cannot be read (an error, no answer in 5 seconds, a status that is not 2xx), 422 `fields_refused` with `reason` (and `field`) when the JSON is read but refused, 429 `too_many` past 60 asks a minute from one place, or 429 `fields_full` when the person (or, for a visitor, the place) already holds 100 descriptions and `replaces` names none of them.
- A `value` or `web` source is read by the actions' own engine: its connectors, credentials, guarded calls and time limit are those of every form action. A visitor's call is made as a visitor.
- The portal keeps what it served for 24 hours under `token`. Asking again for the same description (the same form, container, source answer, asker and values of the `dependsOn` fields) gives the same `token` and starts its 24 hours over: no row is added.
- `replaces` is the token the page holds. When the page asks again for other values, the row it names is dropped, if it is the asker's own; a token that is another's, or none the portal keeps, replaces nothing.
- The token belongs to the asker: the person signed in, or a visitor. It is kept with the values of the `dependsOn` fields it was asked for.

**Sending.** The form is sent with the values under the container's key and the tokens:

```json
{ "locale": "en", "data": { "code": "LV-2041", "load": { "cantitate": 120 } }, "fieldTokens": { "load": "<token>" } }
```

- The values are checked as the form's own fields are, against the fields served under the token, not against what the source says now. A name the fields do not have is `unknown_field`; the errors name `load.cantitate`.
- A container that served nothing and was sent nothing is left out of the submission, unless it is required (`fields_unavailable`). Values sent with no token the portal knows are `fields_expired`; so are values sent with a token that was served to someone else (a visitor's token sent by a person signed in, or the reverse), or for other values of the `dependsOn` fields than the form holds when it is sent. The page asks for the fields again.

**In actions.** The values are `form.<key>.<field>`, such as `form.load.cantitate`, in the form's [actions](/portal/developer/actions/). The Forms page, the CSV export and the notification email show them as `cantitate: 120`.

## Currency

The configuration behind [Currency](/portal/sites/form-field-types/#currency). In a form's `components`:

```yaml
- type: currency
  key: cost
  label: Disposal cost
  input: true
  currency: RON
  display: symbol
  position: after_space
  decimalSeparator: ','
  thousandsSeparator: '.'
  decimals: 2
  validate: { required: true, min: 0, max: 1000000 }
```

- `currency`: an ISO 4217 code, such as `RON`, `EUR` or `JPY`. `RON` when left out.
- `display`: `symbol` (the default) or `code`.
- `position`: `before`, `before_space`, `after` or `after_space` (the default).
- `decimalSeparator`: `','` (the default) or `'.'`.
- `thousandsSeparator`: `none`, `'.'`, `','`, `space` or `narrow` (a narrow no-break space). `'.'` when the decimal separator is a comma, `','` when it is a point.
- `decimals`: 0 to 4. Left out, the currency's own; always 0 for a currency such as `JPY`.
- `validate.min` and `validate.max`: numbers or texts holding one, compared as decimals.
- form.io's own `decimalLimit` and `delimiter` are no more taken; the portal refuses a form that has them.

The console refuses the form when the two separators are the same (`currency_separators`), the decimals are not 0 to 4 (`currency_decimals`), the currency is not one of the list (`currency_code`), a position, display or separator is not one of the choices (`currency_options`), a bound is not an amount or has more decimals than the field (`currency_bounds`), or `min` is above `max` (`limits`).

**The value** is a JSON number, such as `1234567.5`. The submission is refused with `400`:

```json
{ "error": "invalid", "message": "The form is not filled in right.", "errors": [{ "path": "cost", "message": "currency_decimals" }] }
```

- `currency_decimals`: more decimals than the field keeps. The digits are read from the number's shortest text as sent (`10.555` has three, `0.1 + 0.2` as a float has seventeen), so the value is never rounded and a floating-point sum is refused.
- `currency`: not a number, not finite, or too large for a number to keep to the last digit of the field's decimals.
- `min` and `max`: outside the bounds, compared exactly.
- `required`: nothing sent, as for any field.

A value is kept as sent, with `-0` as `0`. The CSV export writes it as the number's own text.

## Phone number

The configuration behind [Phone number](/portal/sites/form-field-types/#phone-number). In a form's `components`:

```yaml
- type: phone
  key: contact_phone
  label: Contact person's phone
  input: true
  defaultCountry: RO
  countries: [RO, FR, DE]
  validate: { required: true }
```

- `defaultCountry`: a country by its two capital letters. `RO` when left out. It must be one of `countries` when there are some.
- `countries`: the countries a number may come from, each a country the numbering library knows. Left out, every country.
- form.io's `phoneNumber` is the older field: it works as it did, and the builder no longer offers it.

The console refuses the form when a country is not one the numbering library knows or is listed twice (`phone_countries`), or the default country is not a country or not among those allowed (`phone_default`).

**The value** is a text. The page keeps it in E.164, `+40723456789`. A caller that sends a value (the forms API) writes it in the international form: spaces, points, dashes, brackets and a `(0)` are taken out, and the number must then be valid for the country its code and digits say, by [libphonenumber-js](https://gitlab.com/catamphetamine/libphonenumber-js)'s `min` metadata, the same the page uses. The value kept is the E.164 text. The submission is refused with `400`, and an `errors` entry:

- `phone`: not a valid number, or not in the international form. A national number such as `0723456789` is refused, since the API has no country to read it in.
- `phone_country`: a valid number of a country not among `countries`.

The page loads the numbering library from `/_portal/assets/libphonenumber/1.12.10/libphonenumber-min.js` (served by the portal, one fixed file, `immutable`), and only on a page whose form has a phone field.

## Date and time

The configuration behind [Date and time](/portal/sites/form-field-types/#date-and-time). In a form's `components`:

```yaml
- type: dateTime
  key: period
  label: Reporting period
  input: true
  kind: month
  latest: { mode: today, offset: -1, unit: months }
- type: dateTime
  key: disposed
  label: Disposed of on
  input: true
  earliest: { mode: field, field: generated }
  limitMessage: The disposal date cannot be before the date the waste was generated.
- type: dateTime
  key: end
  label: End
  input: true
  earliest: { mode: expression, expression: 'timestamp(form.start) + duration("720h")' }
```

- `kind`: `date` (the default), `dateTime` or `month`. The type is `dateTime`; form.io's own `datetime` is not taken.
- `earliest` and `latest`: each a limit, or none. A limit is `mode` and what its mode takes:
  - `none`: no limit.
  - `date`: `date`, a day `2026-11-16`, a month `2026-11` (month fields only), or a day and a time of Romania's clocks `2026-11-16 10:00` (date and time fields only; seconds allowed).
  - `today`: `offset`, a whole number of days or months (0 when left out; at most 36,500 days or 1,200 months either way), and `unit`, `days` (the default) or `months`. A shift in months keeps the day, or the last day of a shorter month.
  - `field`: `field`, the key of another field of the form. Not applied while that field is empty.
  - `expression`: `expression`, in [CEL](/portal/sites/actions/#expressions), at most 2,000 characters.
- `limitMessage`: the text shown at the field when a date is out of range. It is translated under `i18n` like a label.

**Limits.** Each end becomes a bound:

- A day, a month or a moment is compared as its kind: a date field by the day, a month field by the month (a day inside a month counts as the month), a date and time field by the moment. For a date and time, a day (a fixed one, today's, another field's) covers its whole day on Romania's clocks: its first moment as the earliest, its last (`23:59:59.999`) as the latest.
- `today` is the day on the clocks of `Europe/Bucharest`, on the server and in the page alike.
- A value of another field may be a day, a month or a moment; it is turned into the kind of this field.
- In an expression, `form.<key>` is the value sent for a field of the form (a date field's value as a timestamp), `user` is the person (`id`, `name`, `email`, `roles`, `fields`, and each of their fields as `user.<name>`; empty for a visitor), `now()` is the moment, and `date("2026-01-31")` makes a timestamp from a day. `timestamp(form.start)` of a timestamp is itself. It gives a timestamp or a text written as a day, a month or an RFC 3339 moment. An expression that reads `form.<key>` for a key whose field is empty is not applied.

The console refuses the form when `kind` is not one of the three, a limit is malformed (`date_limit`), a fixed earliest is after a fixed latest (`date_order`), an expression does not check (`date_expression`), or a limit reads a key the form does not have (`date_field`).

**The value** is a text: `2026-11-16`, `2026-11` or, for a date and time, an RFC 3339 moment with its zone (`Z` or `+02:00`) that the portal keeps in UTC to the second, `2026-11-16T08:00:00Z`. The submission is refused with `400` and an `errors` entry:

- `date`: not a date, a month or a moment as the kind says.
- `date_limit`: outside the limits as worked out when the form is sent.
- `date_limit_error`: a limit could not be worked out, such as an expression that failed.

The limits are worked out again on the server whatever the page showed. A value that is the same as the record held before (`previous`, in the options `checkSubmission` takes for a form that changes a record) is not judged again, so an old date that is now in the past does not block a change to another field.

**The limits of an expression, for the page.** The page asks, as the person fills the form in and when a field the expression reads changes:

```
POST /_portal/api/forms/<form>/dates/<key>
{ "site": "primaria", "locale": "en", "values": { "start": "2026-11-01" } }
```

The answer is `{ "earliest": "2026-12-01", "latest": null }`: the end an expression gives, as a day, a month or a UTC moment, and `null` for an end that is not an expression's or not applied. A session sends its CSRF token; a caller is limited to 60 requests a minute per form and address; a limit that cannot be worked out is `422 limit_unavailable`.

**Fields from JSON.** A [description of fields](/portal/developer/forms/) of type `date` or `datetime` is this field, as `kind` `date` or `dateTime`, with its `min` and `max` as fixed limits. A `datetime`'s default, written as Romania's clocks show it, is kept as the moment it is in UTC. A model's `date` and `datetime` fields are this field in the model's own form.

## Label position and instructions

On the form and on any component, in `forms/<id>.yaml`:

```yaml
labelPosition: left # the form's default for every field: top (default), left or right
components:
  - type: number
    key: amount
    label: Amount generated (kg)
    input: true
    labelPosition: top # this field's own; it wins over the form's
    instructions: Enter the monthly amount, with a decimal point.
    instructionsAs: icon # below (default) or icon
```

- `labelPosition`: `top`, `left` or `right`. A field's own wins, then the form's, then `top`. `left` puts the label before the field on the same row, `right` after it, in a column 30% wide; under 600 px wide every label is above. A lone checkbox keeps its label after the box unless its own `labelPosition` is `top` or `left`. Any other value is refused: `label_position`, at `/components/<n>/labelPosition`.
- `instructions`: plain text of at most 500 characters. Longer is refused as `instructions`; markup, as `text`.
- `instructionsAs`: `below` or `icon`; anything else is `instructions_as`.
- Instructions are texts the form's `i18n` must translate, like a label. A translation over 500 characters is refused as `translation_long`, at `/i18n/<locale>/<text>`.
- The page writes each component's instructions with an `id` of `<component id>-<key>-instructions` and names it in the control's `aria-describedby`. The icon is a `button` named "Instructions for <label>" that shows them on hover, focus and tap.

## Select with search and with checkboxes

A `select` takes four more properties:

```yaml
- type: select
  key: codes
  label: Waste codes treated
  input: true
  dataSrc: values # or app
  data: { values: [{ label: Paper, value: c1 }, { label: Glass, value: c2 }] }
  autocomplete: true # search, yes or no
  minChars: 2 # 0 to 3, characters typed before suggestions (default 0)
  multiple: true # a list of checkboxes
  minValues: 1 # whole numbers from 1 up
  maxValues: 6
```

- `autocomplete` is `true` or `false`; `minChars` is a whole number from 0 to 3. Others are refused: `select_autocomplete`, `select_min_chars`.
- `minValues` and `maxValues` count only with `multiple: true`. They are whole numbers from 1 up, the least no more than the most, and, for options written in the form, no more than the number of options: `select_values`.
- A select that asks for search or `multiple`, or has over 200 options, is drawn as the portal's own control; any other is the browser's. Options from an app are fetched before the form is drawn, as before.
- Matching ignores accents and capitals and tries the start of each word.

When a form is sent (`POST /_portal/api/forms/:form/submissions`), a `multiple` select's value is a list of option values. The answer to a wrong one is a 400 with the field's `path` and a `message`:

```json
{ "errors": [{ "path": "codes", "message": "max_values" }] }
```

- `max_values` and `min_values`: more or fewer values than the field takes. The fewest is asked once a value is sent; nothing sent is `required`'s to say.
- A value that is none of the options is refused as before, and so is one sent twice (`type`).

## Slider

```yaml
- type: slider
  key: level
  label: Treatment level
  input: true
  min: 0
  max: 100
  step: 5 # default 1
  start: 0 # where the handle starts; default the least
  showValue: true # default true
  unit: "%" # at most 20 characters; a translatable text
  validate: { required: true }
```

- `min` and `max` are numbers with `min` below `max`; `step` is above 0 and fits the range a whole number of times. Decimals are exact: `0` to `1` by `0.1` fits, `0` to `1` by `0.3` does not. At most six decimal places.
- `start` is in the range and on a step. It is where the handle starts, never a value, so a slider left alone sends nothing. Do not write `defaultValue`: form.io would fill it in as the answer, so the loader refuses it.
- The loader refuses `slider_bounds` (at `/min` or `/max`), `slider_step`, `slider_start`, `slider_unit` and `slider_show`.
- A value sent is a number in the range and on a step, or the field is refused with `slider_range`; it is kept as a number, whole when `min`, `max` and `step` are.

```json
{ "errors": [{ "path": "level", "message": "slider_range" }] }
```

The page words it "The value must be between {min} and {max}, in steps of {step}." In a zone of fields read from a JSON, a described field of type `slider` is drawn as this field, with its `min`, `max` and `step` (0, 100 and 1 where it gives none), and a `slider` whose range or default cannot work refuses the description (`bad_limits`, `bad_default`).

## The password field

The keys behind the **Password** field of [Form fields](/portal/sites/form-field-types/#password). In a form's `components`:

```yaml
- type: password
  key: secret
  label: Password
  input: true
  confirm: true      # default true: two boxes
  minLength: 14      # 8 to 128, default 12
  validate: { required: true }
```

- `confirm`: a boolean. The builder writes `confirm: false` when the box is cleared, and the console's cleaning keeps it.
- `minLength`: a whole number from 8 to 128, counted in characters. It sits on the field, not under `validate`.
- `validate` takes only `required`. Any other key is refused with the reason `password_validate`, and a `defaultValue` with `password_default`.
- Loader reasons, all under the problem code `form_component`: `password_confirm`, `password_min_length`, `password_default`, `password_validate`. A form with `offline: true` that holds the field has the problem `form` with the reason `offline_password`.

### What is sent

The page sends `{ "value": "…", "confirm": "…" }` when confirmation is asked, and a plain text when it is not. The server accepts exactly those shapes (an object with any other key, or with something that is not a text, is `type`). The check runs again on the server:

| Error `message` | When |
|---|---|
| `required` | Nothing was typed and the field is required. Nothing typed, not required, keeps no value. |
| `type` | The value is not one of the two shapes. |
| `password_mismatch` | The two texts differ. |
| `password_min_length` | Shorter than `minLength`. |
| `password_max_length` | Longer than 1,024 characters. |

The answer is 400 `invalid` with `errors: [{ path, message }]`. It never holds either text.

### What is kept

`checkSubmission` checks the two texts and the length, and holds the password where nothing that writes a value out can reach it. Once the submission has passed every check, the portal hashes it with Argon2id and a salt of its own (`Bun.password.hash(text, { algorithm: "argon2id" })`, off the event loop, so other requests are not held up). The hash is what the submission keeps and what the form's actions read as `form.secret`. There is no other copy of the text and nothing to read it back with. The field is never a barcode source.

The hash is not shown anywhere either:

- **Reading submissions:** `GET /_portal/api/forms/:form/submissions` and `/:id` leave the field out, and so do the form's `inputs` in `GET /_portal/api/forms`, `export.csv` (no column) and the reviewers' email.
- **Drafts:** `PUT …/draft` drops the key, and the page never sends it. `GET` returns none.
- **A person's export:** the data export of a person's submissions and drafts leaves out any value that is a password hash.
- **Action runs:** a text of a run's log, outcome or error that holds the hash is replaced by `[hidden]` before it is kept or answered.
- **Keys the form no longer has:** a value that is a password hash is left out wherever it is read, so a removed or retyped field shows nothing.

The portal's password rules for signing in are not applied to this field: its own `minLength` is the rule.

## The formatted text field

The keys behind the **Formatted text** field. In a form's `components`:

```yaml
- type: richText
  key: notes
  label: Notes
  input: true
  buttons: [bold, italic, superscript, numberedList, alignment]   # default: all ten
  maxLength: 5000                                                 # 1 to 100000, default 10000
  validate: { required: true }
```

- `buttons`: a list of `bold`, `italic`, `underline`, `superscript`, `subscript`, `size`, `bulletList`, `numberedList`, `spacing` and `alignment`. At least one, none twice, each from the list: otherwise `rich_text_buttons`. Left out, all are offered.
- `maxLength`: a whole number from 1 to 100,000, counted in characters of seen text: otherwise `rich_text_max_length`. It sits on the field, not under `validate`.
- `validate` takes only `required` (`rich_text_validate` for any other key), and `defaultValue` is refused (`rich_text_default`).

### The markup it keeps

The value is a text of markup. The server cuts it down with `sanitize-html` and keeps that:

| Button | Markup |
|---|---|
| `bold`, `italic`, `underline` | `strong`, `em`, `u` (`b` and `i` become `strong` and `em`) |
| `superscript`, `subscript` | `sup`, `sub` |
| `size` | `span` with one class: `portal-rt-size-small`, `-normal`, `-large` or `-xlarge` |
| `bulletList`, `numberedList` | `ul`, `ol` and `li` |
| `spacing` | a class on `p`, `ul`, `ol` and `li`: `portal-rt-spacing-1`, `-115`, `-15` or `-2` |
| `alignment` | a class on the same tags: `portal-rt-align-left`, `-center` or `-right` |

`p` and `br` are always kept. `class` is the only attribute, and only these classes. A script, a style, an event attribute, a link, an image, a frame, a table and every other tag are taken out and their text stays (the text of `script` and `style` goes too). A `span` without a size and an `li` outside a list are taken out. Markup of a button the field does not offer is taken out the same way, whoever sent it.

Every scan is a single pass. More than 262,144 characters of markup is refused as `max_length`, and tags nested more than 128 levels deep are refused as `type`.

### The check

| Error `message` | When |
|---|---|
| `type` | The value is not a text. |
| `required` | Nothing is seen once the markup is cut down (spaces, non-breaking and zero-width ones included), and the field is required. Not required, the value kept is `""`. |
| `max_length` | The seen text, with markup and breaks left out, is longer than `maxLength` in characters. |

The value kept is the cut-down markup. An example, as the API takes it:

```
sent:  <p onclick="x()">a<script>alert(1)</script><img src=x></p>
kept:  <p>a</p>
```

### Where it is read

- `GET …/submissions/:id` gives the cut-down markup.
- `GET …/submissions` gives the plain text on one line, at most 200 characters, ending in `…` when cut.
- `export.csv` and the reviewers' email carry the plain text, a line to each paragraph (the email puts it on one line).
- The console draws the markup as elements of the tags above only, never as markup, so nothing a submission holds can run.

The field is never a barcode source.

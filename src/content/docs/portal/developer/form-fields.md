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

`checkSubmission` replaces the value by an Argon2id hash with a salt of its own (`Bun.password.hashSync(text, { algorithm: "argon2id" })`). The hash is what `checked.data` carries, what the submission keeps, and what the form's actions read as `form.secret`. There is no other copy of the text and nothing to read it back with. The field is never a barcode source.

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

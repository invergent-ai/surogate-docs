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


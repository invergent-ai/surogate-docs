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

---
title: Extension fields
description: Form fields the portal's extensions add - a barcode or QR code, a barcode scanner, an IBAN and a signature pad.
---

The portal's extensions add four kinds of field to [forms](/portal/sites/forms/): a barcode or QR code drawn on the form, a barcode scanner, an IBAN and a signature. As with every extension, they are open to every tenant of the portal. The form builder offers them in its **Extensions** group.

## What people see

Here a refund form uses all four. The QR code follows the receipt number as it is typed; the account is an IBAN; the person signs with a finger, a pen or the mouse.

![A refund form: a receipt number, its QR code drawn under it, a "Code on the envelope" box with a Scan button, an IBAN typed with spaces in lower case, and a signature pad with a signature drawn on it, "Sign above" under it.](../../../../assets/screenshots/portal-fields-form.png)

## A barcode or QR code

A barcode draws a fixed text, or the value of another field of the form as people type it. It sends nothing with the form.

- It draws QR codes, Data Matrix, PDF417, Code 128, Code 39, EAN-13, EAN-8, UPC-A and ITF-14. A QR code is drawn when the form names none.
- It follows a field holding one value as text: a text, number, date, time, amount, single choice, scanned code or IBAN. Never ticked boxes, a yes or no, many choices, a record or a signature.
- A fixed text is at most 2,000 characters.
- A value the format cannot hold, such as letters in an EAN-13, shows "This code cannot be drawn." instead of a code.

## A barcode scanner

A text box with a **Scan** button. **Scan** opens the camera, the back one first on a phone, and the first code it reads fills the box. **Cancel** or **Escape** closes it and stops the camera.

![The scanner open over the form: "Scan the code", the camera's picture and a Cancel button.](../../../../assets/screenshots/portal-fields-scanner.png)

- The form can name which codes it reads; when it names none, it reads all those a barcode draws, with ITF in place of ITF-14.
- Without a camera, or when the person refuses it, the field says "There is no camera." and they can still type the code.
- What it holds is text of at most 2,000 characters, checked like any text field: required, length and pattern.
- In a form shown on another site's page, the camera works only when that page allows it.

## An IBAN

A text box for a bank account. People may type spaces and lower case; the portal keeps the IBAN without spaces, in capitals.

![The IBAN field with a wrong digit: "Account to receive the money is not a valid IBAN."](../../../../assets/screenshots/portal-fields-iban-error.png)

- It is checked in the browser and again by the portal: a country that uses IBANs, that country's length, and the check digits.
- The form can limit it to some countries, such as Romania only.
- A field hidden by its condition is not checked.

## A signature

A pad to sign on with a finger, a pen or the mouse. What is kept is the signature's image.

- Under the pad is the form's own text, or "Sign above" in the page's language.
- The pad is as wide as the form, or as the form says, up to 2,000 by 1,000 pixels.
- A signature is at most 90 KB, so a form holds two.
- A required signature left empty says the field is required.

## In the console

On the **Forms** page, a signature is listed as **Signed**. Opening a submission shows its image.

![The console's Forms page with a refund request open: the receipt number, the IBAN in capitals without spaces, and the signature's image.](../../../../assets/screenshots/portal-fields-submission.png)

The CSV export and the reviewers' email say `signed` instead of the image.

## Save a signature as a file

A form's actions can save the signature as a PNG in one of the portal's [folders](/portal/console/files/), with `writeFile` and `encoding: dataUrl` (see the [config example](#a-signature-saved-as-a-file)). A [document action](/portal/sites/document-actions/) can put it in a PDF, as an `<img>` whose `src` is the signature.

## Config example

### The fields

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

### A signature saved as a file

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

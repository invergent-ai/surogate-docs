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

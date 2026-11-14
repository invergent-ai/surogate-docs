---
title: Document actions
description: The keys of the actions that make and read PDF, Word, Excel and CSV files and barcode images.
---

The configuration behind [Document actions](/portal/sites/document-actions/). That page says what each action does for people, who may use it and its limits.

These go in an action list: a form's `actions` (`forms/<id>.yaml`), a flow, an endpoint or a job. For the keys every action has, see [Developer: Actions](/portal/developer/actions/#an-action-list).

## A PDF from HTML, and a conversion

`htmlToPdf` makes a PDF from HTML an expression gives.

- `html`: an expression giving the HTML. Headings, paragraphs, tables, lists, links, `<style>` and `style` are kept, with their fonts, colours, borders, backgrounds and alignment.
- Images must be inside the HTML as `data:image/png`, `jpeg` or `gif`, up to 2 MB each. Any other image, frame, stylesheet or CSS `url()` is left out: the portal fetches nothing from an address.
- `paper`: `a4` (when left out) or `letter`.
- `toFolder` and `toName`: where the PDF is kept. The name must end in `.pdf`.

`htmlToWord` takes the same keys and makes a Word document (`.docx`) instead.

`convertToPdf` makes a PDF of a Word, Excel, PowerPoint or OpenDocument file in a folder.

```yaml
- type: htmlToPdf
  html: |
    "<h1>Adeverință nr. " + vars.number + "</h1><p>" + form.name + " a depus cererea.</p>"
  toFolder: certificates
  toName: '"adeverinta-" + vars.number + ".pdf"'
```

- `html`: an expression giving the HTML.
- `toFolder` and `toName`: where the PDF is kept, in a folder of the portal's files.

A Word, Excel, PowerPoint or OpenDocument file in a folder becomes a PDF with `convertToPdf`:

```yaml
- type: convertToPdf
  folder: requests
  name: '"cerere-" + submission.id + ".docx"'
  toFolder: requests
  toName: '"cerere-" + submission.id + ".pdf"'
```

- `folder` and `name`: the file to convert.
- `toFolder` and `toName`: where the PDF is kept.

## Work with PDFs

| Type | What it does | Takes |
|---|---|---|
| `mergePdfs` | Puts 2 to 20 PDFs one after another | `folder`, `names` (a list), `toFolder`, `toName` |
| `overlayPdf` | Draws the first page of another PDF over the pages, such as a letterhead or a stamp | `folder`, `name`, `overlay`, `pages` (`all`, `first` or `last`), `toFolder`, `toName` |
| `splitPdf` | Makes a PDF of the pages named, in that order | `folder`, `name`, `pages`, `toFolder`, `toName` |
| `readPdf` | Reads the text, its pages apart | `folder`, `name`, `into` |

`pages` of `splitPdf` is an expression, so write the pages as quoted text: `pages: "'1-3,5'"`. Without the quotes, `1-3` is a subtraction. `readPdf` keeps `{ text, pages }` in `vars.<into>`.

## A filled Word template

Write a Word document with tags between braces, and put it in a folder:

```
Dear {name},

Your request {number} was approved. The fees:
{#fees}
- {title}: {amount} lei
{/fees}
```

Then fill it with `fillWordTemplate`:

- `{tag}` takes the value of the same name. A value is always text in the document, never formatting.
- `{#list}` … `{/list}` repeats what is between them for each item of a list, whose fields fill the tags inside.
- A tag with no value is left empty.
- A template with a broken tag fails with "The template has a broken tag", naming what is wrong.

```yaml
- type: fillWordTemplate
  folder: templates
  name: '"approval.docx"'
  values:
    name: user.name
    number: vars.number
    fees: "[{'title': 'Certificate', 'amount': 25}, {'title': 'Urgent', 'amount': 50}]"
  toFolder: approvals
  toName: '"approval-" + vars.number + ".docx"'
```

- `folder` and `name`: the template.
- `values`: what fills the tags, each an expression; a list fills a `{#list}` block.
- `toFolder` and `toName`: where the filled document is kept.

`readWord` reads a Word document's text into `vars.<into>` as `{ text }`.

## An Excel file

`writeExcel` writes a list of maps as one sheet: a header row, then a row for each map.

- `columns` picks the columns and their titles, in order; in the example it leaves out the records' `id`, `ownerId`, `createdAt` and `updatedAt`. Without it, every key of the maps is a column, in the order first met (at most 100).
- `sheet`: the sheet's name, `Sheet1` when left out.

```yaml
- type: findRecords
  model: requests
  where: { status: '"approved"' }
  into: approved
- type: writeExcel
  rows: vars.approved
  columns:
    - { key: number, title: Number }
    - { key: name, title: Name }
  sheet: Approved
  toFolder: exports
  toName: '"approved.xlsx"'
```

- `rows`: a list of maps, here the records `findRecords` found.
- `columns`: the columns and their titles, in order.
- `sheet`: the sheet's name.

`writeCsv` takes the same `rows` and `columns`, and `separator`: `","` (when left out), `";"` or `tab`.

Reading gives a list of maps, the first row naming the columns:

| Type | Takes |
|---|---|
| `readExcel` | `folder`, `name`, `sheet` (an expression; the first sheet when left out), `into` |
| `excelSheets` | `folder`, `name`, `into`: the sheets' names |
| `readCsv` | `folder` and `name`, or `text` (an expression holding CSV); `separator`; `into` |

## A barcode

`barcode` makes an image of a value. `format` is `code128` (when left out), `ean13`, `ean8`, `upca`, `code39`, `itf14`, `qrcode`, `datamatrix` or `pdf417`. The image is a PNG.

```yaml
- type: barcode
  value: '"https://primaria.ro/verifica/" + vars.number'
  format: qrcode
  toFolder: certificates
  toName: '"qr-" + vars.number + ".png"'
```

- `value`: an expression giving what the code holds.
- `format`: the kind of code, here a QR code.
- `toFolder` and `toName`: where the PNG is kept.

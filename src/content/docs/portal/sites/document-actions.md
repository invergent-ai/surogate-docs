---
title: Document actions
description: Make and read PDF, Word, Excel and CSV files and barcode images in the portal's folders, from forms, flows, endpoints and jobs.
---

Document actions make files and read them, in the portal's [folders](/portal/console/files/). A form can turn what was sent into a PDF certificate, fill a Word template, export a list to Excel, or read a spreadsheet someone uploaded. They come with the portal's **Documents** extension. As with every extension, they are open to every tenant of the portal.

They are [actions](/portal/sites/actions/) like any other: put them in a form's, a flow's, an endpoint's or a job's action list.

## Make a PDF from HTML

```yaml
- type: htmlToPdf
  html: |
    "<h1>Adeverință nr. " + vars.number + "</h1><p>" + form.name + " a depus cererea.</p>"
  toFolder: certificates
  toName: '"adeverinta-" + vars.number + ".pdf"'
```

- `html`: an expression giving the HTML. Headings, paragraphs, tables, lists, links, `<style>` and `style` are kept, with their fonts, colours, borders, backgrounds and alignment.
- Images must be inside the HTML as `data:image/png`, `jpeg` or `gif`, up to 2 MB each. Any other image, frame, stylesheet or CSS `url()` is left out: the portal fetches nothing from an address.
- `paper`: `a4` (when left out) or `letter`.
- `toFolder` and `toName`: where the PDF is kept. The name must end in `.pdf`.

`htmlToWord` takes the same keys and makes a Word document (`.docx`) instead.

`convertToPdf` makes a PDF of a Word, Excel, PowerPoint or OpenDocument file in a folder:

```yaml
- type: convertToPdf
  folder: requests
  name: '"cerere-" + submission.id + ".docx"'
  toFolder: requests
  toName: '"cerere-" + submission.id + ".pdf"'
```

A file with a password is never converted. These three actions need the portal's document converter. If your portal has none, they fail with "This portal has no document converter."; ask the portal's administrator.

## Work with PDFs

| Type | What it does | Takes |
|---|---|---|
| `mergePdfs` | Puts 2 to 20 PDFs one after another | `folder`, `names` (a list), `toFolder`, `toName` |
| `overlayPdf` | Draws the first page of another PDF over the pages, such as a letterhead or a stamp | `folder`, `name`, `overlay`, `pages` (`all`, `first` or `last`), `toFolder`, `toName` |
| `splitPdf` | Makes a PDF of the pages named, in that order | `folder`, `name`, `pages`, `toFolder`, `toName` |
| `readPdf` | Reads the text, its pages apart | `folder`, `name`, `into` |

`pages` of `splitPdf` is an expression, so write the pages as quoted text: `pages: "'1-3,5'"`. Without the quotes, `1-3` is a subtraction. `readPdf` keeps `{ text, pages }` in `vars.<into>`.

## Fill a Word template

Write a Word document with tags between braces, and put it in a folder:

```
Dear {name},

Your request {number} was approved. The fees:
{#fees}
- {title}: {amount} lei
{/fees}
```

Then fill it:

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

- `{tag}` takes the value of the same name. A value is always text in the document, never formatting.
- `{#list}` … `{/list}` repeats what is between them for each item of a list, whose fields fill the tags inside.
- A tag with no value is left empty.
- A template with a broken tag fails with "The template has a broken tag", naming what is wrong.

`readWord` reads a Word document's text into `vars.<into>` as `{ text }`.

## Excel and CSV

`writeExcel` writes a list of maps as one sheet: a header row, then a row for each map.

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

- `columns` picks the columns and their titles, in order; here it leaves out the records' `id`, `ownerId`, `createdAt` and `updatedAt`. Without it, every key of the maps is a column, in the order first met (at most 100).
- `sheet`: the sheet's name, `Sheet1` when left out.
- Numbers stay numbers. Text stays text, even when it starts with `=`, so a spreadsheet never runs it as a formula.

`writeCsv` takes the same `rows` and `columns`, and `separator`: `","` (when left out), `";"` or `tab`. The file is UTF-8, so Excel opens Romanian letters right. A text starting with `=`, `+`, `-` or `@` gets a `'` in front.

Reading gives a list of maps, the first row naming the columns:

| Type | Takes |
|---|---|
| `readExcel` | `folder`, `name`, `sheet` (an expression; the first sheet when left out), `into` |
| `excelSheets` | `folder`, `name`, `into`: the sheets' names |
| `readCsv` | `folder` and `name`, or `text` (an expression holding CSV); `separator`; `into` |

Empty rows are left out. A column with no title is `column1`, `column2` and so on, and a repeated title gets `_2`. A formula cell gives its result, and a date gives its ISO date text. At most 1,000 rows are read, as many as an `each` goes over.

## Barcodes and QR codes

```yaml
- type: barcode
  value: '"https://primaria.ro/verifica/" + vars.number'
  format: qrcode
  toFolder: certificates
  toName: '"qr-" + vars.number + ".png"'
```

`format` is `code128` (when left out), `ean13`, `ean8`, `upca`, `code39`, `itf14`, `qrcode`, `datamatrix` or `pdf417`. The image is a PNG. A value the format cannot hold, such as letters in an EAN-13, fails and says why.

## Who may do what

Document actions keep to the folders' [permissions](/portal/sites/permissions/), as the file actions do. Someone who edits a folder reads its files and makes or replaces them. Anyone else, a visitor too, only makes new files, and never in a public folder. Every folder is checked before any work is done.

An action that makes a file changes the portal, so a GET or public [endpoint](/portal/sites/endpoints/) cannot use it. An action that only reads can be used anywhere.

## Limits

- A file read or made is at most 10 MB, and the files one action reads at most 50 MB together.
- A Word or Excel file may unpack to 50 MB at most.
- A PDF is read, split or made of 500 pages at most.
- 1,000 rows are written or read, and an Excel cell holds 32,767 characters.
- HTML and CSV text are 2 MB at most.
- A run takes 20 document actions at most.
- What an action keeps in `vars` is 1 MB at most.
- Converting HTML takes about two seconds; a form's run has ten. Make long documents in a [job](/portal/sites/jobs/), which has more time.
- A flow's tests make no documents: a document action fails the test.

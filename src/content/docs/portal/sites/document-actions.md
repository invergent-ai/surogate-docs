---
title: Document actions
description: Make and read PDF, Word, Excel and CSV files and barcode images in the portal's folders, from forms, flows, endpoints and jobs.
---

Document actions make files and read them, in the portal's [folders](/portal/console/files/). A form can turn what was sent into a PDF certificate, fill a Word template, export a list to Excel, or read a spreadsheet someone uploaded. They come with the portal's **Documents** extension. As with every extension, they are open to every tenant of the portal.

They are [actions](/portal/sites/actions/) like any other: a form's, a flow's, an endpoint's or a job's action list can hold them. The console does not set action lists yet. For now, this is set in the site's configuration: see [Developer: Document actions](/portal/developer/document-actions/).

## What people get

Document actions have no screen of their own. What they make is a file in a folder, and people open it where the folder lets them: anyone for a public folder, the people the folder names for a secure one (see [Files](/portal/console/files/#folders)).

## Make a PDF from HTML

An action can make a PDF from HTML that an expression gives.

- The HTML keeps its headings, paragraphs, tables, lists, links and styles, with their fonts, colours, borders, backgrounds and alignment.
- Images must be inside the HTML, as PNG, JPEG or GIF data, up to 2 MB each. Any other image, frame, stylesheet or CSS address is left out: the portal fetches nothing from an address.
- The paper is A4 (when left out) or Letter.
- The PDF is kept in a folder, under a name that ends in `.pdf`.

The same action can make a Word document (`.docx`) instead.

Another makes a PDF of a Word, Excel, PowerPoint or OpenDocument file in a folder. A file with a password is never converted. Making a PDF or a Word document from HTML, and converting a file, need the portal's document converter. If your portal has none, they fail with "This portal has no document converter."; ask the portal's administrator.

## Work with PDFs

- Put 2 to 20 PDFs one after another.
- Draw the first page of another PDF over the pages (all of them, the first or the last), such as a letterhead or a stamp.
- Make a PDF of the pages named, in that order. The pages are named as text, such as `1-3,5`.
- Read the text, its pages apart. Later actions get the whole text, and the text of each page.

## Fill a Word template

Write a Word document with tags between braces, such as `{name}`, and put it in a folder. An action fills it with values and keeps the filled document in a folder:

- `{tag}` takes the value of the same name. A value is always text in the document, never formatting.
- `{#list}` … `{/list}` repeats what is between them for each item of a list, whose fields fill the tags inside.
- A tag with no value is left empty.
- A template with a broken tag fails with "The template has a broken tag", naming what is wrong.

Another action reads a Word document's text, and keeps it as text.

## Excel and CSV

An action can write a list of items with named values as one sheet: a header row, then a row for each item.

- The columns and their titles can be picked, in order: a list of records, for instance, can leave out each record's id, owner, and the times it was made and changed. Without that, every name of the items is a column, in the order first met (at most 100).
- The sheet's name is `Sheet1` when left out.
- Numbers stay numbers. Text stays text, even when it starts with `=`, so a spreadsheet never runs it as a formula.

A CSV file takes the same list and columns, and a separator: a comma (when left out), a semicolon or a tab. The file is UTF-8, so Excel opens Romanian letters right. A text starting with `=`, `+`, `-` or `@` gets a `'` in front.

Reading gives a list of items with named values, the first row naming the columns:

- An Excel file is read from a sheet, the first one when left out. Another action gives the sheets' names.
- A CSV is read from a file, or from text an expression gives, with the separator it says.

Empty rows are left out. A column with no title is `column1`, `column2` and so on, and a repeated title gets `_2`. A formula cell gives its result, and a date gives its ISO date text. At most 1,000 rows are read, as many as an action looping over a list goes over.

## Barcodes and QR codes

An action can make an image of a value. The kinds of code are Code 128 (when left out), EAN-13, EAN-8, UPC-A, Code 39, ITF-14, QR code, Data Matrix and PDF417. The image is a PNG. A value the format cannot hold, such as letters in an EAN-13, fails and says why.

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
- What an action keeps for later actions is 1 MB at most.
- Converting HTML takes about two seconds; a form's run has ten. Make long documents in a [job](/portal/sites/jobs/), which has more time.
- A flow's tests make no documents: a document action fails the test.

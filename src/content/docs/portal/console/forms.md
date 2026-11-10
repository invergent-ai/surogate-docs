---
title: Forms
description: Read, export and delete what people sent through the forms you review.
---

**Forms** shows what people sent through the portal's forms. It is in the menu for each form's reviewers and for the administrators. To write a form and say who reviews it, see [Forms](/portal/sites/forms/) in the site guide.

## What the list shows

Choose the **Form**. The list shows what was sent through it, newest first: when, by whom (or **Visitor**, for someone not signed in), and the first answers. **Older** shows the next ones.

Under the form's name is its own address, `/_portal/forms/<id>`, on each site that offers it.

## Read a submission

**Open** shows each answer under its field's label, in your language. Ticked boxes and several choices are listed together; a checkbox reads Yes or No; a field left empty shows a dash.

## Export

**Export CSV** downloads every submission of the form, at most 50,000, newest first: one row each, with when it was sent, its language, the email of whoever sent it, and one column per field. It opens in Excel or LibreOffice. A value starting like a formula is written so that a spreadsheet does not run it.

## Delete

**Delete** removes one submission, after asking. **Delete all** removes every submission of the form, after asking. Neither can be undone.

Submissions belong to their form's id. If a form is removed from the portal, its submissions are hidden, and they show again if a form with the same id comes back. Delete them first when they should go with the form.

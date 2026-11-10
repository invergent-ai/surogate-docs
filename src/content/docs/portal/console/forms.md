---
title: Forms
description: Read, export and delete what people sent through the forms you review.
---

**Forms** shows what people sent through the portal's forms. It is in the menu for each form's reviewers and for the administrators, who also build the forms there. For what a form may hold and who sends it, see [Forms](/portal/sites/forms/) in the site guide.

## What the list shows

Choose the **Form**. The list shows what was sent through it, newest first: when, by whom (or **Visitor**, for someone not signed in), and the first answers. **Older** shows the next ones.

Under the form's name is its own address, `/_portal/forms/<id>`, on each site that offers it.

## Read a submission

**Open** shows each answer under its field's label, in your language. When the form asks for consent, **Agreed to** shows the text the person agreed to. Ticked boxes and several choices are listed together; a checkbox reads Yes or No; a field left empty shows a dash.

## Export

**Export CSV** downloads every submission of the form, at most 50,000, newest first: one row each, with when it was sent, its language, the email of whoever sent it, and one column per field. It opens in Excel or LibreOffice. A value starting like a formula is written so that a spreadsheet does not run it.

## Delete

**Delete** removes one submission, after asking. **Delete all** removes every submission of the form, after asking. Neither can be undone.

Submissions belong to their form's id. If a form is removed from the portal, its submissions are hidden, and they show again if a form with the same id comes back. Delete them first when they should go with the form.

## Build a form

Administrators see **Build forms** at the top of the page: **New form** makes one, and **Edit** opens one.

- **Settings:**
  - the form's id (lower-case letters, digits and hyphens, fixed once saved);
  - its name in each language;
  - the language its text is written in;
  - whether it goes step by step;
  - the sites that offer it (none ticked: every site);
  - whether anyone may send it;
  - who may send it and who reads what was sent, one per line: `signed-in`, `group:<name>`, `organization:<path>` or `user:<email>`;
  - the thanks shown once it is sent, in each language.
  - whether people can leave the form and come back to it;
  - who is told by email when it is sent, and whether the email holds the answers;
  - whether people must agree to a text before sending, and that text in each language;
  - how many days submissions are kept (empty: always).
- **Fields:** drag fields from the left onto the form, and drop them where they go.
  - **Fields:** text, text area, number, checkbox, select, radio, select boxes and the submit button.
  - **More fields:** email, web address, phone number, day, time and currency.
  - **Layout:** panels, columns, fieldsets, tabs, wells and text blocks.

  Click a field to change it. **Display** sets its label, the text shown in it, its help, whether it is required, and its options. The **Key** is the name its answer is kept under; it follows the label until you change it. **Shown when** shows the field only when another field has a value. In a step-by-step form, each panel at the top is a step.
- **Translations:** a row for each text of the form, with a box for each of its sites' other languages. Every row needs a translation before the form can be saved.

**Save** keeps the form; pages that show it change at once. If the portal refuses it, the reasons are listed above the form. If someone changed the portal's files since you opened the form, reload it and make your changes again. **Remove** takes the form off every page; what was sent through it stays, under its id.

A form written by hand with parts the builder does not keep opens as one the console cannot draw. Change it in the portal's files.


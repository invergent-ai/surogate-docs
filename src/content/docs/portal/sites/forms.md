---
title: Forms
description: Build a form, put it on a page or give it its own address, say who sends it and who reads what was sent.
---

A form asks visitors or people signed in for something: a request, a registration, a complaint. The portal draws it, checks what is sent, and keeps it for the people who review the form, on [Forms](/portal/console/forms/) in the console.

Administrators [build forms in the console](/portal/console/forms/#build-a-form), by dragging fields onto the form. The fields are the components of [form.io](https://form.io)'s builder.

## What people see

**A visitor or a person signed in** sees the form on a page, in the site's design, with its fields, a box to tick for consent when the form asks for one, and its button:

![A contact form on a page: "Message to the city hall" with Full name, Email, Your message, a box "I agree that the city hall uses my data to reply to this message." and the Send message button.](../../../../assets/screenshots/portal-form-contact.png)

A long form can be in steps. Each step is a tab at the top, and the person moves with **Next** and **Previous**:

![The first steps of a building permit request: the tabs Applicant, Property and work, Details and Consent, with the step Property and work open and the Next button.](../../../../assets/screenshots/portal-request-step.png)

When the form is sent, the person reads its confirmation, or what its [actions](/portal/sites/actions/#what-people-see) tell them.

**The form's reviewers** read what was sent on [Forms](/portal/console/forms/) in the console: each submission with who sent it, its answers and, when the form asked for consent, the text the person agreed to:

![The Forms page with a submission open: Ioana Marinescu's building permit request, with each field and its answer and the consent text.](../../../../assets/screenshots/portal-forms-submission.png)

## Write a form

Administrators build a form in the console: see [Build a form](/portal/console/forms/#build-a-form). A form has:

- an id: lower-case letters, digits and hyphens, starting with a letter, and fixed once saved. It is part of the form's [own address](#its-own-address);
- a name, in both languages;
- the language its text is written in, Romanian unless you say otherwise;
- whether it goes in steps: each panel at the top of the form is then a step;
- the sites that offer it. With none chosen, every site offers it;
- the thanks a person reads once the form is sent. Without it, the portal thanks them.

## What a form may hold

- **Fields:** text, text area, number, email, phone number, web address, checkbox, select boxes, select, radio, day, time and currency.
- **[Extension fields](/portal/sites/form-fields/):** a barcode or QR code, a barcode scanner, an IBAN and a signature.
- **Layout:** panels, columns, fieldsets, tabs and wells, nested at most eight deep.
- **Text blocks**, in the markup a site's pages allow.
- **One submit button.**

Each field's **Key** is a name, unique in the form, such as `name` or `birth_date`. A select, radio or select boxes lists its own options. A form holds at most 300 components.

A field can be shown only when another field has a value: **Shown when**, in the form builder, sets it. A field hidden by its condition is not required, and what was typed in it is not kept.

A form holds no script. The portal refuses a form with custom conditions, calculated values, custom validation, logic, options read from an address, a rich text editor, or a template that calls anything. The refusal names the part. Show and hide fields with conditions instead.

## Translations

The text of a form is written in the language set for the form. Each text needs a translation in each of its sites' other languages: the form builder has a **Translations** tab for them, with a row for each text. A form offered on a Romanian and English site, written in Romanian, needs an English translation of every label, placeholder, description, option and tab. The portal refuses a form that leaves one out, and names the text.

form.io's own words, such as Next, Previous and the error messages, are translated by the portal.

## Who sends it and who reads what was sent

- **Who may send it:** anyone, signed in or not, when you tick **Anyone may send it, signed in or not**. Otherwise **Who may send it** names who may: **Anyone signed in**, groups, organizations or people. By default, and when it names no one, the form is for **Its reviewers only**.
- **Who reads what was sent:** **Who reads what was sent** names the people, groups or organizations who read, export and delete its submissions. By default it is **Administrators only**. The administrators always read what was sent. Reviewers may send the form too.

Both are set in the form builder, on the **Who can use it** tab: see [Build a form](/portal/console/forms/#build-a-form). Each is a picker; [Choose who](/portal/sites/permissions/#choose-who) tells how it works.

People who may not send a form do not see it on a page, and its address answers as if there were no form.

## Put a form on a page

In the [page builder](/portal/console/pages/#forms), **Add a form** to a part of the page. It offers the forms the site offers. A page shows at most five forms.

## Its own address

Each form also has an address of its own on every site that offers it, `/_portal/forms/<id>`: the form alone, in the site's design. Add `?locale=en` for another language. On a domain that serves several sites, add `?site=<site>`.

## What the portal checks

The browser checks the form as it is filled in. The portal checks it again when it arrives, by the same rules, whatever the browser did:
- required fields;
- lengths and number limits;
- email and web addresses;
- each choice among its options;
- each value the right kind.

Fields the form does not have are dropped. A form that does not pass is not kept, and the person is told to check it. What they typed stays.

The form builder sets whether a field is required. Lengths and number limits are not set in the console yet. For now, this is set in the site's configuration: see [Developer: Forms](/portal/developer/forms/#what-the-portal-checks).

A visitor sends at most ten forms a minute from one address. A form filled in by a robot is thanked and not kept.

## Come back to a form

A long form can be left and finished later. For a person signed in, the portal keeps what they have typed a couple of seconds after they stop. When they open the form again, on any computer, it is filled in as they left it. What they began is deleted once they send the form, or after 30 days untouched.

A visitor's draft stays in the browser tab only. Reloading the page keeps it; closing the tab forgets it, so nothing is left behind on a shared computer.

Drafts can be turned off for a form: in the form builder, clear **Keep what people have begun, so they can come back to it**.

## Ask for consent

A form can ask people to agree to something before they send it, such as how their data is used. The form builder asks for the text, in each language. The form shows a box to tick, with this text, before its button; a step-by-step form shows it as a last step. The form cannot be sent without the box ticked. The portal keeps the text the person agreed to, in their language, with what they sent. Reviewers see it on [Forms](/portal/console/forms/), and it is in the export. If the text changes while someone has the form open, they are asked to load the page again.

## Tell the reviewers

Each time the form is sent, the addresses the form names (at most 20) get an email in the form's language with a link to Forms in the console. The email can also hold the answers: leave that off when the answers are personal data that should not travel by email. The form can set the email's subject in each language. The form builder sets the addresses, whether the email holds the answers, and the subject.

Email is sent only when the portal has a mail server; ask whoever runs the portal.

## Keep submissions for a time

Submissions older than the number of days the form sets are deleted, a few times a day. In the form builder, that is **Keep what is sent for (days)**. Without it, they are kept until someone deletes them.

## Fill in a form offline

A public form can be filled in where the connection comes and goes, such as on a tablet in the field. Turn it on for the form in the form builder.

Open the form at its own address, `/_portal/forms/<id>`, once while online. From then on, that browser can open the address without a connection. A form sent without a connection is kept on the device, and the page says so. It is sent when the browser is back online: when the page is opened again, or within a minute while it is open. Each form is sent once, even if the connection drops halfway.

What is sent offline goes as a visitor's, even for a person signed in. Only public forms can be filled in offline. If something kept offline cannot be sent, because the form changed meanwhile or no longer exists, the page asks to fill the form in again.

## Pick a record

A record field picks a record of one of the portal's [data models](/portal/sites/data-models/).

**Choose** opens a list of the model's records, 20 at a time, with **More** for the next ones and a search box when the model has searchable fields. A record is named by the model's title field, or else its first text field. With many records allowed, a person picks up to 50 and closes the list with **Done**; **Clear** empties the field.

The list shows only the records the person may see, and the record the form makes checks the pick again. A required record field must hold at least one. A form with a record field cannot be filled in offline. In the form builder, **Record** is among **More fields**.

## Fields from apps

An approved app can add field types and option lists ([Build an app](/portal/developer/build-an-app/#form-fields-and-options)). A form uses them like its other fields.

The app's field is drawn by the app; its value is checked when the form is sent. A select's options come from the app as the person filling the form in. If the app does not answer, the form says it cannot be filled in right now. A form uses at most 10 such selects, and cannot be filled in offline. The console's builder keeps these parts when you edit the form, but does not offer them. For now, this is set in the site's configuration: see [Developer: Forms](/portal/developer/forms/#fields-from-an-app).

## After it is sent

A form can run [actions](/portal/sites/actions/) once it is sent and kept: work out a reference number, tell the person something, or send them to a payment page. The form builder does not set them yet. For now, this is set in the site's configuration: see [Developer: Forms](/portal/developer/forms/#actions-after-it-is-sent).

If the actions fail, what was sent is still kept, and the person is told so, with the failing action's error message when it has one.

## From an app

Each sent form raises the portal's `form.submitted` event, with the form's id and the submission's. Wire it to an app's receiver, or to a webhook, on [Events](/portal/console/events/). A program reads submissions with a token given the **forms** scope, as one of the form's reviewers.

## Personal data

What a signed-in person sent, and what they began, are part of their export, and are deleted when they are erased (see [Users](/portal/console/users/)). What a visitor sent names no one.

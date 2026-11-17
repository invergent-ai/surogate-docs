---
title: Form fields
description: The fields a form can hold in the form builder - numbers, dates, phone numbers, amounts, files, passwords, formatted text, lists, sliders and zones of fields read from a JSON.
---

The form builder offers the portal's own fields in its **Fields** and **More fields** groups. Every setting below is a choice in the field's dialog in the builder: no code and no file is needed. Everything the browser checks, the portal checks again when the form is sent.

For the fields the portal's extensions add (barcodes, scanner, IBAN, signature), see [Extension fields](/portal/sites/form-fields/). For how to put a form on a page and who sends it, see [Forms](/portal/sites/forms/).

## Label position and instructions

Every field takes a label position and instructions, whatever its type.

In the form builder, on the **Settings** tab, **Where field labels go** sets where the labels of the whole form go: **Above the field**, **To the left of the field** or **To the right of the field**. It is above the field when you change nothing.

![The Settings tab of the monthly report sheet: where field labels go, set to the left of the field.](../../../../assets/screenshots/portal-fields-labels-settings.png)

A field can say otherwise. On the **Fields** tab, click the field, and on its **Display** tab:

- **Label position:** **As the form says**, **Top**, **Left** or **Right**.
- **Instructions:** a text of at most 500 characters, written as plain text. It is read to people who use a screen reader when they reach the field.
- **Show instructions as:** **Below the field**, or **Icon "?" with the explanation on hover or focus**.

![The Display tab of the Amount generated field in the form builder, with Label position, Instructions and Show instructions as.](../../../../assets/screenshots/portal-fields-labels-builder.png)

Instructions are among the texts on the form's **Translations** tab, with a row for each language: write them there like a label. A translation of instructions is also at most 500 characters.

### What a person sees

- **Left** puts the label on the same row as the field, in a column 30% as wide as the row. **Right** puts the label after the field, in the same kind of column.
- On a screen under 600 pixels wide the label is always above the field, whatever is set. A phone shows the form in one column.
- A checkbox on its own keeps its label after the box. **Top** puts it above the box.
- **Below the field**, the instructions are a line of text under the field. As an icon, a "?" button sits beside the label. The explanation shows when the mouse is over it, when it has the keyboard focus, and on a tap; **Escape** closes it.
- The field's own control reads the instructions to a screen reader when it takes the focus, in both ways of showing them.

![The monthly report sheet on a page: labels to the left of the fields, one label above its field, one after its field, the instructions under the amount and the explanation of the remarks showing.](../../../../assets/screenshots/portal-fields-labels-page.png)

![The same sheet on a phone: every label above its field.](../../../../assets/screenshots/portal-fields-labels-mobile.png)

### What the portal refuses

The form cannot be saved with a label position other than top, left or right, with instructions of more than 500 characters or that hold markup, or with a way of showing them that is neither below the field nor an icon. The console says which field.

## Whole number

**Whole number** is in the **Fields** group of the form builder. It is a box for a number with no decimals, such as a count of places or a floor.

In the form builder, drag **Whole number** onto the form and click it. Its dialog has three tabs:

- **Display**: the label, the placeholder, the help under the box, whether the field is **Required**, and the **Key** its answer is kept under.
- **Limits**: **Least** and **Most**, each a whole number, negative if need be. Leave one empty for no limit on that side.
- **Shown when**: shows the field only when another field has a value, as for any field.

![The dialog of a Whole number field in the form builder, on its Limits tab: Least is 1 and Most is 20, and the field as people see it is shown on the right.](../../../../assets/screenshots/portal-fields-integer-builder.png)

### What people see

A box that takes digits, and a minus sign at the start. Anything else, typed or pasted, is left out as it is typed: `12ab` becomes `12`, and the decimal point is dropped. A number is at most 9,007,199,254,740,991, either way.

![A booking form after the person pressed the button: Number of places holds 25 and says it cannot be greater than 20; Floor holds a minus sign alone and says "Enter a whole number."](../../../../assets/screenshots/portal-fields-integer-page.png)

- A box holding only a minus sign, or a number too long to be kept exactly, says **Enter a whole number.** On a Romanian page it says **Introduceți un număr întreg.**
- A number below **Least** or above **Most** says so, with the field's name and the limit: "Number of places cannot be greater than 20." The words are in the page's language.
- A required box left empty says that it is required.
- The portal checks the number again when the form is sent: a text, or a number with decimals, is refused.
- What is kept is a number, not a text. A [form's actions](/portal/sites/actions/) read it as a number.

Developers: see [Developer: Form fields](/portal/developer/form-fields/#whole-number).

## Currency

The **Currency** field takes an amount of money and writes it the way you choose: with the currency's symbol or code, before or after the amount, with your country's separators. What the portal keeps is the number, never the text on the screen.

In the form builder, **Currency** is in **More fields**. Open the field to set:

- **Currency**: any currency of the ISO 4217 list. Type its code or its name in the box, such as `GBP` or `pound`, and pick it from the suggestions. Romanian lei (RON) when you pick none. Under it the dialog says **Existing values are not converted**: changing the currency of a field that already has answers does not change those answers, so an answer of 100 stays 100 in the new currency.
- **Show**: **Symbol (lei, €)** or **Code (RON, EUR)**.
- **Position**: **Before the amount**, **Before the amount, with a space**, **After the amount** or **After the amount, with a space**.
- **Decimal separator**: **Comma ( , )** or **Point ( . )**.
- **Thousands separator**: **Point ( . )**, **Comma ( , )**, **Space**, **Narrow space** or **None**.
- **Decimals**: from 0 to 4. Left empty, the currency's own: 2 for lei and euro, 3 for the Kuwaiti dinar, 0 for the yen. A currency without decimals, such as the yen, always has none.
- **Least** and **Most**, on the **Limits** tab. Negative amounts are allowed unless the least rules them out.

![The Currency dialog of the form builder: Label Disposal cost, Currency RON · Romanian Leu with the note Existing values are not converted, Show Symbol, Position After the amount with a space, Decimal separator Comma, Thousands separator Point, Decimals 2.](../../../../assets/screenshots/portal-fields-currency-builder.png)

The console does not let you save a form whose currency field cannot work: the two separators cannot be the same, the decimals must be from 0 to 4, the least cannot be above the most, and a least or most cannot have more decimals than the field keeps. It says which field and why above the form, and **Save** stays grey.

**What a person filling the form in sees.** The box shows the symbol or code where you put it. The thousands are grouped as the person types, and the box takes no more decimals than the field keeps: a third decimal typed in a field of two is not taken, and neither is a letter. When the person leaves the box, the decimals are filled in. Typing `1234567,5` in a field of lei with a comma and a point gives `1.234.567,50 lei`, and the portal keeps exactly 1234567.5.

![A form with two amounts: Disposal cost shows 1.234.567,50 and the symbol lei after it; Fee paid in euro shows the euro sign and -1,234.50.](../../../../assets/screenshots/portal-fields-currency-page.png)

An amount outside the least and the most gets a message at its field, and the form is not sent:

![The same form refused: a notice "Please fix the following errors before submitting" and, at Fee paid in euro, 250,000.50 with the message "Fee paid in euro cannot be greater than 100000."](../../../../assets/screenshots/portal-fields-currency-refused.png)

The portal checks again when the form is sent, and its rules do not bend: an amount with more decimals than the field keeps is refused, never rounded in silence. Amounts are worked out as decimals, so there are no floating-point surprises: a sum such as 0.1 + 0.2 that is not an amount of cents is refused as well. In a reviewer's CSV export, an amount is written as a plain number, with a point for the decimals and no thousands separator, so that a machine can read it. Developers: see [Developer: Form fields](/portal/developer/form-fields/#currency).

## Phone number

The **Phone number** field takes a number in the international form and keeps it that way, such as `+40723456789`, whatever the person typed.

In the form builder, **Phone number** is in **More fields**; it takes the place of the older phone box, which the builder no longer offers (a form that already has one keeps working). Open the field to set:

- **Default country**: the country a number written without one is read in. Pick it by name or calling code. Romania (+40) when you pick none.
- **Allowed countries**: pick the countries a number may come from, each by name or calling code; **×** takes one away. When you pick none, a number of any country is allowed.
- **Required**.

![The Phone number dialog of the form builder: Label Office phone, Default country Romania (+40), Allowed countries with one country picked, Romania (+40), and the Required box.](../../../../assets/screenshots/portal-fields-phone-builder.png)

**What a person filling the form in sees.** A button with the country and its calling code, such as **RO +40**, and the box for the number beside it. The button opens a list of countries with a search: type a name or a calling code, and pick the country. A number typed with a country's code, starting with **+** or **00**, changes the country by itself. Spaces, points, dashes, brackets and a `(0)` are taken out. When the person leaves the box, a valid number is shown in the international form: `0723 456 789` becomes `+40 723 456 789`, and `+33 6 12 34 56 78` switches the country to France.

![A form with two phone numbers: Contact person's phone shows FR +33 and +33 6 12 34 56 78; Office phone shows RO +40 and +40 723 456 789.](../../../../assets/screenshots/portal-fields-phone-page.png)

![The country list open under the button RO +40, after typing ger in its search: Germany +49 first, then Algeria, Niger and Nigeria.](../../../../assets/screenshots/portal-fields-phone-country.png)

A number that is not valid for its country, such as `+40 12`, is refused: "Contact person's phone is not a valid phone number." A valid number of a country the field does not allow is refused too, with the countries named: "Only numbers from these countries are allowed: Romania". Nothing is sent until the numbers are right.

![The form refused: Contact person's phone says it is not a valid phone number; Office phone, holding a French number, says Only numbers from these countries are allowed: Romania.](../../../../assets/screenshots/portal-fields-phone-refused.png)

The portal checks the number again with the same numbering rules when the form is sent. Something other than a person, such as a program sending the form, must write the number in the international form already: `0723456789` is refused, since nothing says which country it is in. An answer kept before the field was used, which is not in the international form, is shown as it was, and the field says it is not valid until it is corrected. Developers: see [Developer: Form fields](/portal/developer/form-fields/#phone-number).

## Date and time

The **Date and time** field takes a date, a date with a time, or a month and year, and can keep the person inside limits: no date in the past, no date after today, not before another field's date.

In the form builder, **Date and time** is in **More fields**. On the **Display** tab, **What to choose** is **Date**, **Date and time** or **Month and year** (for a reporting period, for example). On the **Limits** tab, **Earliest** and **Latest** each say how the limit is set:

- **No limit**.
- **A fixed date**: **Date**, written `2026-11-16`; for a month `2026-11`; for a date and time `2026-11-16 10:00`, as the clocks of Romania show it.
- **Today, with a shift**: **Shift** is a whole number, negative for the past and 0 for today itself, **Counted in** **Days** or **Months**. A latest of today with a shift of -1 month is the same day last month.
- **The value of another field**: **Field** is a date field of the same form. While that field is empty, this limit is not applied.
- **An expression**: written in CEL, such as `timestamp(form.start) + duration("720h")`. It reads the form's fields as `form.<key>` (a date field's value is a timestamp), the person as `user` and the moment as `now()`, and gives a date or a timestamp.

**Message when a date is out of range** is what the person reads at the field. Left empty, the portal says it in its own words ("Reporting period cannot be after 2026-10."). Translate your own message on the form's **Translations** tab like any other text.

![The Date and time dialog of the form builder, on the Limits tab: Earliest No limit, Latest Today, with a shift, Shift -1, Counted in Months, and the empty Message when a date is out of range.](../../../../assets/screenshots/portal-fields-datetime-builder.png)

![The Limits tab of another Date and time field: Earliest The value of another field, Field Generated on, Latest No limit, and a message written for the field.](../../../../assets/screenshots/portal-fields-datetime-builder-field.png)

The console does not let you save a form with a fixed earliest after a fixed latest, with an expression that is not valid CEL, or with a limit that reads a field the form does not have. It says which field and why above the form.

**What a person filling the form in sees.** A box to type in and a calendar button beside it. In the Romanian pages the date is typed `zz.ll.aaaa` (and `zz.ll.aaaa hh:mm` for a date and time), in the English pages in the ISO form `2026-11-16` (and `2026-11-16 10:00`). The calendar is the portal's own, with no outside library: the days outside the limits are grey and cannot be chosen. A month field shows the months of a year instead, and a date and time adds hour and minute boxes under the days. The arrow keys move between days, **Enter** chooses one, **Page up** and **Page down** change the month, and **Esc** closes the calendar.

On the 16th of November 2026, a reporting period that can be at most last month has November and December greyed, and October the last month that can be chosen:

![A month field's calendar: the year 2026 with Jan to Oct available and Nov and Dec greyed.](../../../../assets/screenshots/portal-fields-datetime-month.png)

A date that cannot be before another field's gets the days before it greyed. Here the field Generated on holds 2026-11-10, and the days up to the 9th of the month are grey:

![The calendar of Disposed of on, open on November 2026 with the days before the 10th greyed and the 16th, today, outlined.](../../../../assets/screenshots/portal-fields-datetime-calendar.png)

A date typed by hand that is out of the limits gets the message at the field, and the form is not sent:

![The form refused: each date outside its limits has its message at the field, including the message written for Disposed of on.](../../../../assets/screenshots/portal-fields-datetime-refused.png)

**Today and the time zone.** "Today" is the day on the clocks of Romania (Europe/Bucharest), in the page and on the server alike, whatever clock the person's computer shows: at half past eleven in the evening in a place five hours behind Romania, it is already the next day for the limits. A date and a month have no time zone. A date and time is typed and shown as the clocks of Romania show it, and is kept in UTC: 10:00 on 16 November 2026 in Romania is kept as 08:00 UTC, and shown back as 10:00. A fixed date or today as the limit of a date and time covers the whole day, from midnight to the last minute.

The portal works the limits out again when the form is sent, and its answer is the one that counts: a form opened at 23:59 and sent after midnight is refused if the date is no longer allowed, with the message at the field. A limit that cannot be worked out, such as an expression that fails, blocks the form with "The limit cannot be worked out." Developers: see [Developer: Form fields](/portal/developer/form-fields/#date-and-time).

## Slider

The **Slider** field is in the **More fields** group. In its dialog on the **Display** tab:

- **Label** and **Help**, **Required** and **Key**, as for any field, and **Label position** and **Instructions**.
- **Least** and **Most:** numbers, the least below the most.
- **Step:** a number above 0 that fits the range a whole number of times. A step of 5 fits 0 to 100; a step of 0.5 fits -10 to 10.
- **Where the handle starts:** within the range and on a step. Empty, it starts at the least. It is where the handle rests, not an answer.
- **Show the value beside the slider:** ticked, the value is written beside the slider.
- **Unit:** a short text after the value, such as % or kg. It is translated on the **Translations** tab.

![The Slider's dialog in the form builder: least, most, step, where the handle starts, show the value and unit.](../../../../assets/screenshots/portal-fields-slider-builder.png)

### What a person sees

A horizontal slider with its value beside it. The arrows move it one step, **Page Up** and **Page Down** ten steps, **Home** and **End** to the ends. A screen reader reads it as a slider with its value, its least and most, and the value with its unit.

![A treatment level slider at 15 %, with its instructions below.](../../../../assets/screenshots/portal-fields-slider-page.png)

A slider that is not required and was not touched sends nothing: the place where it starts is not taken for an answer. A required slider that was not touched is refused like any required field, at the field.

![A required slider that was not touched: "Treatment level is required"](../../../../assets/screenshots/portal-fields-slider-refusal.png)

The value sent is a number: a whole number when the least, the most and the step are.

A zone of fields read from a JSON draws a field of type `slider` as this slider.

### What the portal refuses

The form cannot be saved when the least is not below the most, when the step is not above 0 or does not fit the range, when the place the handle starts is not in the range and on a step, or when the unit is longer than 20 characters. When a form is sent, a value that is not a number, is outside the range or is not on a step is refused, whether it came from the page or from a program: "The value must be between 0 and 100, in steps of 5."

## Dropdown with search and with checkboxes

A select (the **Select** field in the builder) can search its options and can take many values. In its dialog on the **Display** tab:

- **Search in the options (autocomplete):** tick it for a select a person types into. The list narrows as they type.
- **Characters typed before suggestions:** from 0 to 3, shown once search is on. With 0, the whole list is offered as soon as it opens.
- **Several values, ticked in a list of checkboxes:** leave it off for a choice of one value.
- **Fewest values chosen** and **Most values chosen:** shown once several values are on. Both are whole numbers from 1 up, and the fewest cannot be above the most.

![The Display tab of a select in the form builder: search, the characters before suggestions, several values and the fewest and most values chosen.](../../../../assets/screenshots/portal-fields-select-builder.png)

A select with neither search nor several values stays the browser's own. A select with more than 200 options searches whether or not it was asked to: a list that long is no use without it.

### What a person sees

- **Search:** typing "bistr" in a county field with the 42 counties lists only "Bistrița-Năsăud". Accents and capitals do not matter, and the text is matched at the start of any word: "iasi" finds "Iași", and "nasaud" finds "Bistrița-Năsăud". When nothing matches, the list says "No results." Only an option can be chosen, never a text of the person's own. With **Characters typed before suggestions** above 0, the list says "Type at least 2 characters." until they have.

![A county field with "bistr" typed: only Bistrița-Năsăud is listed.](../../../../assets/screenshots/portal-fields-select-search.png)

- **Checkboxes:** the open list shows a checkbox for each option. **Select all** is there only for a list of at most 100 options, and not when **Most values chosen** is below the number of options. **Clear** takes every choice away. Closed, the control shows what was chosen as labels, each with a button to take it away; above three it says how many, such as "6 selected".

![A field of waste codes with its list open: three codes ticked, and the same three shown as labels above the list.](../../../../assets/screenshots/portal-fields-select-boxes.png)

- **The most:** once the most is reached, the other options cannot be ticked, and the list says "You can choose at most 6."

![The waste codes with six chosen: the seventh cannot be ticked, and the list says why.](../../../../assets/screenshots/portal-fields-select-max.png)

- **The fewest:** it is asked once something is chosen: "Waste codes treated: choose at least 2." A required select that is left empty says it is required, at the field.
- **Keyboard:** **Arrow Down** opens the list and moves down it, **Arrow Up** moves up, **Space** or **Enter** ticks the option the arrows are on (typing a search, **Enter** only), and **Escape** closes the list. A screen reader is told it is a combobox with a list, and, with checkboxes, that several values can be chosen.

The options can be the form's own or the options of an app: both are drawn the same way.

### What the portal refuses

The form cannot be saved with a number of characters above 3, or with fewest or most values that are not whole numbers from 1 up, the fewest above the most or above the number of options. When a form is sent, every value must be one of the options, none twice, and the number of values must be within the fewest and the most: otherwise it is refused, whether it came from the page or from a program.

## Password

The **Password** field asks a person for a password they choose, such as when a supplier creates an account. It is kept only as a scrambled value that cannot be turned back into the password.

In the form builder, open **More fields** and drag in **Password**. Click the field's edit button to open its dialog:

![The form builder's Password dialog: Label, Help, Ask for confirmation and Apply the portal's password policy ticked, Minimum length 12, Required and Key, with a preview of the field.](../../../../assets/screenshots/portal-fields-password-builder.png)

- **Label** and **Help**: the text above the field and a hint under it.
- **Ask for confirmation**: ticked, the person types the password twice. It is ticked unless you clear it.
- **Apply the portal's password policy**: ticked, the password must also keep the rules set under **Security**, **Sign-in policy**: the length, and an upper-case letter, a lower-case letter, a digit and a symbol where the policy asks for them. Left clear, only the field's own **Minimum length** applies. What names the person (their email or name) is not asked of this field, since the password may be for an account that is not theirs, and nor is the history of earlier passwords.
- **Minimum length**: from 8 to 128 characters. Left empty, it is 12. When the policy asks for more characters, the policy's length also has to be kept.
- **Required**: the form cannot be sent without a password.
- **Key**: the name the answer is kept under.

### What a person sees

The person sees two boxes that show dots instead of letters: the field's label, such as **Password**, and **Confirm password**. Each has a **Show** button that turns into **Hide** while the letters are shown. Their browser may offer to save the new password, and they can paste it in.

![A new supplier account form with Company name, Email, Password and Confirm password filled in, the two password boxes showing dots, each with a Show button.](../../../../assets/screenshots/portal-fields-password-page.png)

The form is not sent while there is something to put right, and the message is next to the box it is about:

![The same form after pressing Create the account with two different passwords: "The passwords do not match" under Confirm password.](../../../../assets/screenshots/portal-fields-password-mismatch.png)

- **The passwords do not match** appears under **Confirm password**.
- **The password must have at least 12 characters.** appears when the password is shorter than the **Minimum length**.
- A password has at most 1,024 characters.

When the field applies the portal's password policy, the rules are listed under the box and ticked as the password is typed. The list follows the policy as it is now: change the policy and the form follows. Pressing send with a rule not kept says which ones are still needed.

![The same form with a password that keeps the length and a symbol: the rules are listed under the box, the length and the symbol ticked, an upper-case letter and a digit not yet, and "The password still needs: an upper-case letter, a digit."](../../../../assets/screenshots/portal-fields-password-policy.png)

The portal checks all of this again when the form is sent, so a form sent by other means is refused in the same way, with the rules that are not kept named.

### Where the password goes

The password is never kept, and nobody can read it:

- **What is kept:** a scrambled value (an Argon2id hash with a random salt of its own). The same password gives a different value each time.
- **People who read what was sent:** it is not in the list on **Forms**, not in an opened submission, not in **Export CSV** (the column is left out) and not in the email that tells reviewers a form was sent.
- **Drafts:** a half-filled form is kept without the password. A person who comes back to it finds the password boxes empty.
- **[Actions](/portal/sites/actions/):** an action the form runs is given the scrambled value and never the password. If an action writes it in its log, the run's log on **Forms** shows **[hidden]** in its place.

![The Forms page with a new supplier account open: Company name and Email are shown, and there is no password row.](../../../../assets/screenshots/portal-fields-password-submission.png)

### What the portal refuses

The form builder says what is wrong when you save, in these words:

- **A password field's shortest length is not between 8 and 128.**
- **A password field has a password of its own written in the form.** Take the default value out.
- **A password field takes no pattern or length limit of the texts.** Set its **Minimum length** instead.
- **A form with a password field cannot be filled in offline.** The password is scrambled by the portal when the form is sent, which needs a connection.

A password field cannot be the text a barcode draws.

## Formatted text

The **Formatted text** field lets a person write with bold, lists, sizes and alignment, such as the notes on a file or a description. What they write is kept and shown with the same formatting.

In the form builder, open **More fields**, drag in **Formatted text** and click its edit button:

![The form builder's Formatted text dialog: Label, Help, Buttons offered with ten boxes, Longest text 2000, Required and Key, with a preview.](../../../../assets/screenshots/portal-fields-rich-text-builder.png)

- **Label** and **Help**.
- **Buttons offered**: tick the buttons the person gets. All ten are offered unless you clear some, and at least one stays ticked:
  - **Bold**, **Italic** and **Underline**;
  - **Superscript** and **Subscript**;
  - **Character size**: **Small**, **Normal**, **Large** and **Very large**;
  - **Bulleted list** and **Numbered list**;
  - **Line spacing**: 1, 1.15, 1.5 and 2;
  - **Alignment**: left, center and right.
- **Longest text, in characters**: from 1 to 100,000, and 10,000 when left empty. It counts the text a person sees, not the formatting.
- **Required** and **Key**.

### What a person sees

The person sees a toolbar of named buttons above a box to write in, and how many characters they have used. Hover or focus a button to read its name. **Ctrl+B**, **Ctrl+I** and **Ctrl+U** work as in a word processor, and the toolbar wraps on a phone, with buttons big enough to tap.

![The Notes on the file form: a toolbar of buttons, a text with bold, a superscript 2, a numbered list and a centered last line, and the count "146 of 2000 characters".](../../../../assets/screenshots/portal-fields-rich-text-page.png)

- Select the text first, then press a button or choose a size, a spacing or an alignment. Spacing and alignment apply to the paragraphs the selection touches.
- A paste, from Word or from a web page, keeps the formatting that has a button here, and keeps the text of everything else. Fonts and colors are lost.

When the box holds nothing but blank lines, the field counts as empty:

![The same form after pressing Send the notes with only Enter pressed in the notes: "Notes is required".](../../../../assets/screenshots/portal-fields-rich-text-required.png)

A text longer than the longest allowed is refused with **The text can have at most 2000 characters.**

### What is kept

Only formatting the field's buttons give is kept. When a form is sent, the portal removes everything else, whoever sent it and however: scripts and styles, links, images, frames and tables are taken out and their text stays. A button you cleared takes its formatting out too. What is kept is what people see, so a text is never shown differently from how it was written.

### Where people read it

- **On Forms:** the list shows the plain text on one line, up to 200 characters. Open a submission and the text is shown as it was written:

  ![The Forms page with a notes submission open: the text with its bold 40 m2, a numbered list of three works and the last line centered.](../../../../assets/screenshots/portal-fields-rich-text-submission.png)

- **Export CSV** and the **email to reviewers** carry the plain text, a line for each paragraph.

### What the portal refuses

- **A formatted text field must offer at least one button, each from the list and none twice.**
- **A formatted text field's longest text is not between 1 and 100,000 characters.**
- **A formatted text field has a text of its own written in the form.** Take the default value out.
- **A formatted text field takes no pattern or length limit of the texts.** Set its longest text instead.

A formatted text field cannot be the text a barcode draws.

## Files

**Files** is in the **More fields** group of the form builder. People add files to the form before they send it, and the form's reviewers download them from the submission.

In the form builder, drag **Files** onto the form and click it. Its dialog asks for:

- **Label** and **Help**.
- **Several files**: tick it to take more than one file. **Most files** then asks how many, from 1 to 20. A field for one file takes one.
- **Allowed extensions**: tick at least one of pdf, doc, docx, xls, xlsx, odt, ods, csv, txt, jpg, jpeg, png and zip. Files that run, such as exe, js or html, are never offered and never allowed.
- **Largest file, in KB**: from 1 KB to 25,600 KB (25 MB). The default, 10,240 KB, is 10 MB.
- **Files with the same name**: what happens when a person adds a file whose name is one already there. **Rename the new one** keeps both (`report.pdf`, then `report (1).pdf`). **Replace the first** keeps the new one only. **Refuse the new one** says "A file named report.pdf is already there." Names that differ only in capitals count as the same.
- **Required**, and the **Key** its answer is kept under.

![The dialog of a Files field in the form builder: Several files ticked, Most files 3, the extensions pdf, jpg and png ticked, Largest file 5120 KB and Files with the same name set to Rename the new one.](../../../../assets/screenshots/portal-fields-files-builder.png)

A form with a **Files** field cannot be filled in offline: the portal refuses a form that has both.

### What people see

A drop zone: "Drag files here or **Choose files**", with the limits under it: "Allowed extensions: pdf, jpg, png. At most 5 MB per file. At most 3 files." A field for one file says "Drag the file here or **Choose a file**". On a Romanian page the words are "Trageți fișierele aici sau **Alegeți fișiere**".

![The Files field empty: a dashed zone with "Drag files here or Choose files" and the limits under it.](../../../../assets/screenshots/portal-fields-files-empty.png)

Each file goes up as soon as it is added, one at a time. Its row shows its name and size, a progress bar while it goes up, **Uploaded** when it is done, and **Remove** to take it off. The form is sent with the files that went up well.

![A file going up: deed.pdf is Uploaded and annual-report.pdf shows its progress bar. Nothing is said at the field yet.](../../../../assets/screenshots/portal-fields-files-progress.png)

The form cannot be sent while a file is still going up or when one failed. While files go up, each one shows its own state and the field says nothing. Only when the person presses send does the field say "Wait for the files to finish uploading." or, when a file failed, "Remove the files that could not be uploaded."

A refused file says why, beside its own row:

![Three files added: deed.pdf and id-card.png are Uploaded; scan.pdf is refused with "The file's content does not match the extension .pdf.".](../../../../assets/screenshots/portal-fields-files-page.png)

- "This extension is not allowed. Accepted: pdf, jpg, png."
- "The file's content does not match the extension .pdf.": the portal reads the start of the file, and it must be what its extension says: a PDF (that starts with its header), a JPEG or PNG image, an Office or OpenDocument file without macros, a ZIP, or plain text for csv and txt. A program is never accepted, whatever it is called. Renaming a file does not get it through.
- "The file is larger than 5 MB.", "The file is empty." and "The file has no valid name."
- "No more than 3 files can be added."
- "A file named deed.pdf is already there.": only when the field is set to **Refuse the new one**.
- "Too many files sent too fast. Try again in a minute." A visitor may send 30 files a minute through one form from one address, and a person who is signed in 60.
- "Too many files are waiting to be sent. Send the form or remove some." A person may have 100 files waiting to one form, and so may the visitors of one network (an address, or for IPv6 the /64 network of a home). One visitor filling their own share leaves the others' alone.
- "No more files can be kept waiting right now. Send the form or try again later." The files that wait take room in the portal's storage: 512 MB for one person or one network, 2 GB for all the visitors together and 4 GB for everyone, across the forms of the site. The room comes back when the files are sent or removed, and a file that waits goes after a day.
- "The file could not be uploaded. Try again." and "Files cannot be uploaded right now."
- "The file is no longer available. Upload it again.": the portal no longer holds a file that waited too long.

A file's name keeps its accents and loses any folder, control characters and spaces at its ends. It is at most 200 characters with its extension.

### Where reviewers find the files

On [Forms](/portal/console/forms/#read-a-submission), choose the form and **Open** a submission. Each file is listed under the field's label, with its size, as a link that downloads it. Only the form's reviewers and the administrators can download, and the portal checks it each time. A file never opens in the browser: it is always saved.

![The Forms page with a documents submission open: Supporting documents lists deed.pdf, 212 KB, and id-card.png, 86 KB, as links.](../../../../assets/screenshots/portal-fields-files-submission.png)

- The list of submissions names the files beside the first answers.
- The CSV export and the reviewers' email carry the files' names, never the files.
- Deleting a submission deletes its files, and so does the form's [retention](/portal/sites/forms/#keep-submissions-for-a-time) when it removes the submission.
- A file that was uploaded and never sent is deleted after 24 hours, unless the person's saved draft holds it.

Developers: see [Developer: Form fields](/portal/developer/form-fields/#files).

## Fields from JSON

**Fields from JSON** is in the **More fields** group of the form builder. It is a zone of the form whose fields are not drawn in the builder. A JSON, a list of fields, says which they are, and the form reads it when it opens. Change the JSON, and every form that reads it changes, with no new version of the form.

In the form builder, drag **Fields from JSON** onto the form and click it. Its dialog asks for:

- **Label**: the zone's heading.
- **Where the JSON comes from**: one of four sources, each asking only for what it needs (below).
- **Path of the list in the JSON**: where the list of fields is, such as `data.fields`. Empty: the JSON itself is the list.
- **Required: the form cannot be sent when the fields cannot be loaded**: tick it when the form is useless without them.
- **Key**: the name the zone's answers are kept under.

### The four sources

**JSON text written here** keeps the JSON in the form. The console refuses to save a text that is not a list of fields.

![The dialog of Fields from JSON with the source "JSON text written here": the JSON text, one field "cantitate", a whole number labelled Cantitate (kg) in Romanian and Quantity (kg) in English, required and at least 0.](../../../../assets/screenshots/portal-fields-json-builder-text.png)

**A JSON file of a folder** reads a `.json` file of one of the [folders](/portal/console/files/) on **Files**. Choose the **Folder** and write the **JSON file**, such as `load-fields.json`. Upload a new file of the same name to change the fields.

![The dialog with the source "A JSON file of a folder": the folder Form data and the file load-fields.json.](../../../../assets/screenshots/portal-fields-json-builder-file.png)

**A named value** reads the result of one of the [named values](/portal/sites/values/). Choose it under **Named value**. The value may itself be the answer of a web call.

![The dialog with the source "A named value": the value loadFields.](../../../../assets/screenshots/portal-fields-json-builder-value.png)

**A web call through a connector** asks one of the portal's web [connectors](/portal/sites/connectors/) for the JSON, so the fields can depend on a system of yours.

- **Web connector**: the connector that makes the call.
- **Path of the call**: added to the connector's address, such as `/fields`.
- **Query**: one line for each parameter, written `name = expression`, such as `code = form.waste_code`. The expression reads the form's fields as `form.<key>`.
- **Reload when these fields change**: the fields the query reads. When a person changes one, the fields are asked for again, a moment after the last change. A query reads only the fields chosen here.

![The dialog with the source "A web call through a connector": the Waste service connector, the path /fields, the query code = form.waste_code, reloaded when Waste code changes, and the list at data.fields.](../../../../assets/screenshots/portal-fields-json-builder-web.png)

### What the JSON holds

A list of at most 50 fields, up to 256 KB. Each field has a **key** and a **type**, a **label**, and may be required, have a default value, options, a least and a most, a step and a description:

- Types: text, textarea, number, integer, email, date, datetime, select, multiselect, radio, checkboxes, checkbox, slider and static (a line of text to show).
- A label or description is a text, or a text for each language of the site.
- A field's key may not be one the form already uses, and no key appears twice.

For example, this JSON describes one field, a required whole number of at least 0, with its label in Romanian and in English: `[{"key":"cantitate","type":"integer","label":{"ro":"Cantitate (kg)","en":"Quantity (kg)"},"required":true,"min":0}]`

### What people see

When the form opens, the zone says "Loading the fields…", then the fields appear among the form's own. What was typed in a field stays when the fields are loaded again, if that field is still there.

![The delivery form with its two fields: Delivery code, and Quantity (kg) read from the JSON and holding 120.](../../../../assets/screenshots/portal-fields-json-page.png)

When the source cannot be read now, because it did not answer in time or answered with an error, the zone says "The fields cannot be loaded right now." with **Try again**. If **Required** was ticked, the form cannot be sent until the fields are there.

![A delivery form whose zone cannot be loaded: "The fields cannot be loaded right now." and a Try again button.](../../../../assets/screenshots/portal-fields-json-unavailable.png)

When the JSON is read but is not a good description, the zone says "The description of the fields is not right:", then what is wrong, such as "a key is there twice", and the key. The person who owns the JSON fixes it.

The fields are asked for at most 60 times a minute from one place. What the portal served is kept for 24 hours: the form is checked against the fields the person was shown, even if the JSON changed since. A form left open for more than a day is refused when it is sent, and the page has to be loaded again.

### In the console

**Forms** shows the zone's answers under its label, as `key: value` for each field that has a value, and the CSV export has one column for it.

![The Forms page with a delivery submission open: Delivery code LV-2041, and Load details, cantitate: 120.](../../../../assets/screenshots/portal-fields-json-submission.png)

Developers: see [Developer: Form fields](/portal/developer/form-fields/#fields-from-json).

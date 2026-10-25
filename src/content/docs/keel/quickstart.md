---
title: Keel quickstart
sidebar:
  label: Quickstart
---

This page takes a project with no case types to a first case that a person works and closes. You build a small loan request: a case starts with an applicant and an amount, one person reviews it, and the review approves or declines it.

You need:

- a Surogate account that is an **Owner** of a project in Studio. An **Editor** can do every step but step 2; ask an owner to do that one.
- a work email for the person who will work the case. It can be your own: staff accounts are separate from Surogate accounts.

## 1. Sign in to Keel Builder

1. Open Keel Builder and sign in with your Surogate username or email and password, or with **Continue with Google** or **Continue with GitHub** where they show.
2. If the project shown is not the one you want, pick it in the switcher at the top of the left rail. The app shows its **Case types** page, which says **No case types yet**.

See [Sign in to Keel Builder](/keel/builder/sign-in/) if the app says you are not a member of any project.

## 2. Invite someone to work the case

Cases are worked in the business app, by the project's staff. Make the first staff member a supervisor.

1. Open **Queues** in the left rail.
2. Under **Supervisors**, press **Invite a supervisor**.
3. Enter the person's **Email** and **Name**, then press **Invite**.
4. The dialog answers with how the person signs in. For a new password account it says **Send *name* this link to set their password** and shows a **Set-password link**. Copy the link, then press **Done**. The link works once.

If the project signs in with Google or GitHub, the dialog shows a **Sign-in link** instead. The person signs in there with the email you entered.

## 3. Create the case type

1. Open **Case types** and press **New case type**.
2. Type the **Name**: `Loan request`. The **Key** (`loan-request`) and the **Number prefix** (`LR`) fill in from the name.
3. Leave **Draft** on **A new draft**, with the **Draft title** it offers.
4. Press **Create**.

The designer opens on the new case type, in the new draft. The chip under the page header reads **Version 1 · draft**, and the case type has one stage, **First stage**. Every change you make from now on is saved to the draft a moment after you make it: the line beside the chip says **Saving…**, then **Saved**.

## 4. Add the fields

1. Open the **Data** tab and press **Add field**.
2. Fill in **Name** `applicant`, **Label** `Applicant`, **Type** **Text**, and turn **Required** on. Press **Save**.
3. Add a second field: **Name** `amount`, **Label** `Amount`, **Type** **Decimal**, **Unit** `EUR`, **Required** on.
4. Add a third field: **Name** `review_note`, **Label** `Review note`, **Type** **Text**. Leave **Required** off.

Required fields are what a case must start with: the business app's start form asks for them.

## 5. Add the review step

1. Open the **Workflow** tab. The board shows one column, **01 First stage**.
2. Press the pencil beside the stage's name, change **Name** to `Review`, and press **Save**.
3. Press **Add step** under the column. In **Add to Review**, keep **Kind** on **Step**, type the **Name** `Review the request`, set **Done by** to **A person or a queue**, and press **Add**.
4. Press the new card. The step's panel opens on the right.

Fill in the panel:

1. Under **Done by**, press **Pick a person** under **A person**, and type two letters of the name of the person you invited. Pick them.
2. Under **Receives**, pick **Applicant** from the **Add** menu, then **Amount**.
3. Under **Must return**, pick **Review note** from the **Add** menu.
4. Under **Allowed outcomes**, the step has one outcome. Type `Approve` in its **Label**. In **Leads to**, pick **Close as…**, type `Approved` in **Resolution** and press **Close as**.
5. In **Name an outcome**, type `Decline` and press **Add outcome**. In the new outcome's **Leads to**, pick **Close as…**, type `Declined` and press **Close as**.

## 6. Dry run

Press **Dry run** in the page header. The panel says **Checking the draft…**, then **No problems. Every scenario passed.**

If it lists problems instead, each one links to its place in the designer. Fix them and press **Run again**. See [Dry run and publish](/keel/builder/publish/).

## 7. Publish

1. Press **Review and publish**. The page lists **What changes** and runs the **Checks** again.
2. When the checks pass, press **Publish**.

The page says **Published** with the draft's title. Press **Open the business app** to go to the project's Work page there, or copy the address from Keel Builder's **Settings** page.

## 8. Set the password and start a case

The person you invited does this part, in the business app.

1. Open the set-password link. Enter a **Password**, repeat it in **Repeat the password**, and press **Set password**. The app signs you in and opens **Work**.
2. Open **Cases** and press **New case**.
3. Pick **Loan request**. Fill in **Applicant** and **Amount**, then press **Start**.

The case opens. The breadcrumb shows its number, `LR-000001`, and the stage bar shows **Review**.

## 9. Work the step

The case page shows a card **Your task · Review the request**.

1. Type a **Review note**.
2. Under **Outcome**, choose **Approve**.
3. Press **Submit**.

The card goes away and the page says **This case is closed.** Open **History** in the side panel to see the step, who did it and its outcome.

## Next steps

- Add a [queue](/keel/builder/queues/) and give the step to the queue instead of one person, so a team shares the work. Supervisors add the queue's members on the [Team page](/keel/business/supervisors/).
- Add a [decision](/keel/builder/flow-nodes/#decisions) that sends large amounts to a second stage.
- Give a step to [an agent](/keel/builder/steps/#done-by), and see its work in the [business app](/keel/business/agents/).
- Write a [scenario](/keel/builder/scenarios/) so every dry run checks the path a case takes.

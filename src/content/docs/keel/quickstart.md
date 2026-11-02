---
title: Keel quickstart
sidebar:
  label: Quickstart for builders
---

This page takes a project with no case types to a first case that a person works and closes. You build a small loan request: a case starts with an applicant and an amount, one person reviews it, and the review approves or declines it. It takes about twenty minutes.

The pictures were taken in a demo project, so some of them show more than your screen will. Your project starts with an empty **Case types** page.

You need:

- a Surogate account that is an **Owner** of a project in Studio. An **Editor** can do every step but step 2; ask an owner to do that one.
- a work email for the person who will work the case. It can be your own: staff accounts are separate from Surogate accounts.

[The quickstart for the business app](/keel/quickstart-business/) is for the people who work cases: it shows the business app's pages in more detail.

## 1. Sign in to Keel Builder

1. Open Keel Builder at https://keel-builder.surogate.ai and sign in with your Surogate username or email and password, or with **Continue with Google** or **Continue with GitHub** where they show.

   ![The Keel Builder sign-in page: username or email, password, Remember me, Sign in, and the Google and GitHub buttons](../../../assets/screenshots/keel-builder-sign-in.png)

2. If the project shown is not the one you want, pick it in the switcher at the top of the left rail. The app shows its **Case types** page, which says **No case types yet** when the project has none.

   ![The project switcher open at the top of the left rail, with the project name and your role](../../../assets/screenshots/keel-builder-project-switcher.png)

See [Sign in to Keel Builder](/keel/builder/sign-in/) if the app says you are not a member of any project.

## 2. Invite someone to work the case

Cases are worked in the business app, by the project's staff. Make the first staff member a supervisor.

1. Open **Queues** in the left rail.
2. Under **Supervisors**, press **Invite a supervisor**.
3. Enter the person's **Email** and **Name**, then press **Invite**.

   ![The Invite a supervisor dialog with an email and a name filled in](../../../assets/screenshots/keel-builder-invite-supervisor.png)

4. The dialog answers with how the person signs in. For a new password account it says **Send *name* this link to set their password** and shows a **Set-password link**. Copy the link, then press **Done**. The link works once.

If the project signs in with Google or GitHub, the dialog shows a **Sign-in link** instead. The person signs in there with the email you entered.

If the email already has an account the project can use, the dialog says so, for example that the person was on the staff already and is now a supervisor, or that they can sign in with the account they have. They sign in with that account.

Inviting needs the project's business sign-in. If the dialog says **This project has no organisation to invite people into. Ask an administrator.** or **Invitations cannot reach the runtime now; try again shortly.**, you cannot go on with this quickstart until that is fixed. See [why someone cannot be invited](/keel/reference/faq/#why-can-someone-not-be-invited).

## 3. Create the case type

1. Open **Case types** and press **New case type**.
2. Type the **Name**: `Loan request`. The **Key** (`loan-request`) and the **Number prefix** (`LR`) fill in from the name.
3. Leave **Draft** on **A new draft**, with the **Draft title** it offers.
4. Press **Create**.

![The New case type dialog: name Loan request, key loan-request, number prefix LR, draft A new draft](../../../assets/screenshots/keel-builder-new-case-type.png)

The designer opens on the new case type, in the new draft. The page header says **Not published yet**, and a chip beside the **Ask the designer agent**, **Dry run** and **Review and publish** buttons names the draft. The case type has one stage, **First stage**. Every change you make from now on is saved to the draft a moment after you make it: the line beside the chip says **Saving…**, then **Saved**.

![The designer for a new case type: one stage, First stage, with an Add step button](../../../assets/screenshots/keel-builder-new-draft-designer.png)

## 4. Add the fields

1. Open the **Data** tab. It says **No fields yet**. Press **Add field**.

   ![The Data tab of a new case type: No fields yet, and an Add field button](../../../assets/screenshots/keel-builder-data-empty.png)

2. Fill in **Name** `applicant`, **Label** `Applicant`, **Type** **Text**, and turn **Required** on. Press **Save**.

   ![The Add field dialog filled in for the applicant: name, label, type Text, Required on](../../../assets/screenshots/keel-builder-add-field-filled.png)

3. Add a second field: **Name** `amount`, **Label** `Amount`, **Type** **Decimal**, **Unit** `EUR`, **Required** on. A currency code such as `EUR` shows the value as money.

   ![The Add field dialog for the amount: type Decimal, unit EUR, Required on](../../../assets/screenshots/keel-builder-add-field-decimal.png)

4. Add a third field: **Name** `review_note`, **Label** `Review note`, **Type** **Text**. Leave **Required** off.

   ![The Data tab with the three fields, and which start form asks for each](../../../assets/screenshots/keel-builder-data-fields.png)

Required fields are what a case must start with: the business app's start form asks for them.

## 5. Add the review step

1. Open the **Workflow** tab. The board shows one column, **01 First stage**.
2. Press the pencil beside the stage's name, change **Name** to `Review`, and press **Save**.

   ![The Edit stage dialog with the name changed to Review, and the goal and deadline fields](../../../assets/screenshots/keel-builder-edit-stage-name.png)

3. Press **Add step** under the column. In **Add to Review**, keep **Kind** on **Step**, type the **Name** `Review the request`, set **Done by** to **A person or a queue**, and press **Add**.
4. Press the new card. The step's panel opens on the right, with the tabs **Who**, **Fields**, **Outcomes** and **Rules**.

   ![The step panel open on the new step, on the Who tab: Done by, a queue, a person, and Decided by a vote](../../../assets/screenshots/keel-builder-step-panel-new.png)

Fill in the panel:

1. On **Who**, under **A person**, press **Pick a person** and type two letters of the name of the person you invited. Pick them.

   ![The person picker open, showing the staff member whose name matches the letters typed](../../../assets/screenshots/keel-builder-pick-person.png)

   The card now says **Assigned to** their name.

2. Open **Fields**. Under **Receives**, pick **Applicant** from the **Add** menu, then **Amount**. Under **Must return**, pick **Review note** from its **Add** menu.

   ![The Add menu under Receives, listing the case type's fields](../../../assets/screenshots/keel-builder-step-receives-menu.png)

   ![The Fields tab: the step receives Applicant and Amount and must return Review note](../../../assets/screenshots/keel-builder-step-fields.png)

3. Open **Outcomes**. The step has one outcome, marked **Main path**. Type `Approve` in its **Label**. Open its **Leads to** menu.

   ![The Outcomes tab of a new step: one outcome, with a Label and a Leads to menu](../../../assets/screenshots/keel-builder-step-outcomes-default.png)

   The menu offers the steps of the stage, the next stage (**Done** after the last stage), any other stage, **End of this path** and **Close as…**. Pick **Close as…**, type `Approved` in **Resolution** and press **Close as**.

   ![The Leads to menu open, with the choices Review the request, Done, End of this path and Close as…](../../../assets/screenshots/keel-builder-step-leads-to.png)

   ![The Close as form: a Resolution field and a Close as button](../../../assets/screenshots/keel-builder-step-close-as.png)

4. In **Name an outcome**, type `Decline` and press **Add outcome**. In the new outcome's **Leads to**, pick **Close as…**, type `Declined` and press **Close as**.

   ![The Outcomes tab with Approve closing the case as Approved and Decline closing it as Declined](../../../assets/screenshots/keel-builder-step-outcomes.png)

Close the panel. The card shows who it is assigned to and where each outcome leads.

![The Workflow tab: stage Review with one person step, Approve closing as Approved and Decline closing as Declined](../../../assets/screenshots/keel-builder-workflow-loan-request.png)

## 6. Dry run

Press **Dry run** in the page header. The panel says **Checking the draft…**, then **No problems. Every scenario passed.** This draft has no scenarios yet, so it says **0 scenarios played**.

![The dry run result: No problems, 0 scenarios played, and a Run again button](../../../assets/screenshots/keel-builder-dry-run.png)

If it lists problems instead, each one links to its place in the designer. Fix them and press **Run again**. See [Dry run and publish](/keel/builder/publish/).

## 7. Publish

1. Press **Review and publish**. The page lists **What changes** and runs the **Checks** again.

   ![The Review and publish page: the Publish button in the header and the list of what changes](../../../assets/screenshots/keel-builder-review.png)

2. When the checks pass, press **Publish**.

   ![The Checks at the bottom of the Review and publish page: No problems](../../../assets/screenshots/keel-builder-review-checks.png)

The page says **Published** with the draft's title. Press **Open the business app** to go to the project's Work page there, or copy the address from Keel Builder's **Settings** page.

![The page after publishing: Published, the draft's title, and the buttons Open the business app and Back to case types](../../../assets/screenshots/keel-builder-published.png)

The case type now has version 1. It shows on the **Case types** page, and people can start cases of it.

![The Case types page with the new case type published as version 1](../../../assets/screenshots/keel-builder-case-types-two.png)

## 8. Start a case

The person you invited does this part, in the business app. If they have not signed in yet, they open the set-password link, enter a **Password**, repeat it in **Repeat the password**, and press **Set password**. The app signs them in and opens **Work**.

1. Open **Cases** and press **New case**.
2. Pick **Loan request**. Fill in **Applicant** and **Amount**, then press **Start**.

   ![The start form of Loan request: Amount and Applicant filled in, with Cancel and Start](../../../assets/screenshots/keel-business-start-form-filled.png)

The case opens. The breadcrumb shows its number, `LR-000001`, and the stage bar shows **Review**.

![The new case: the stage bar on Review, the card Your task, Review the request, with the choice Approve or Decline, and the case's data](../../../assets/screenshots/keel-business-loan-case-started.png)

The step is also in the person's **Work** page, under **Needs me**, because the step is assigned to them.

![The Work page of the person who was picked: Review the request in Needs me, with Open case on the right](../../../assets/screenshots/keel-business-work-needs-me.png)

## 9. Work the step

The case page shows a card **Your task · Review the request**.

1. Under **Outcome**, choose **Approve**.
2. Type a **Review note**.
3. Press **Submit**.

![The card Your task with Approve chosen and a review note typed, above the Submit button](../../../assets/screenshots/keel-business-your-task-filled.png)

The card goes away and the page says **This case is closed.**

![The closed case: This case is closed, and the review note in the case's data](../../../assets/screenshots/keel-business-loan-case-closed.png)

Open **History** in the side panel to see the step, who did it and its outcome. The side panel's first tab, **Case agent**, is a chat with the project's case agent about the case.

![The History tab: You finished Review the request with the outcome Approve, and You started the case](../../../assets/screenshots/keel-business-loan-case-history.png)

## Next steps

- Continue with [the quickstart for the business app](/keel/quickstart-business/): the pages the people who work cases use every day.
- Read [Example: mortgage pre-approval](/keel/examples/mortgage-pre-approval/) to see a case type with agents, a decision, a vote and a committee.
- Add a [queue](/keel/builder/queues/) and give the step to the queue instead of one person, so a team shares the work. Supervisors add the queue's members on the [Team page](/keel/business/supervisors/).
- Add a [decision](/keel/builder/flow-nodes/#decisions) that sends large amounts to a second stage.
- Give a step to [an agent](/keel/builder/steps/#done-by), and see its work in the [business app](/keel/business/agents/).
- Write a [scenario](/keel/builder/scenarios/) so every dry run checks the path a case takes.
- Press **Ask the designer agent** in the designer, and draft a case type from your process documents with [the designer agent](/keel/builder/designer-agent/).

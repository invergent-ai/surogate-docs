---
title: CRM records in Dynamics 365 and Salesforce
description: Make, read, change and find records in Microsoft Dynamics 365 and Salesforce from forms and jobs, such as a lead from a contact form.
---

The portal's **CRM** extension works with records in [Microsoft Dynamics 365](https://dynamics.microsoft.com) (its Dataverse tables) and [Salesforce](https://www.salesforce.com). A contact form makes a lead; a job keeps accounts in step; an administrator's page finds a customer's cases. As with every extension, it is open to every tenant of the portal.

The portal signs in as an app of yours, never as a person. What the app may do in the CRM is what it may do in the portal.

## Connect Dynamics 365

1. In Microsoft Entra, register an app and give it a client secret. Keep the directory (tenant) id, the app's id and the secret.
2. In the Power Platform admin center, add the app to the environment as an **application user**, with a security role that may read and write the tables your steps use.
3. On **Connectors**, make a connector of the kind **A Microsoft Dynamics 365 environment**, with the environment's address (such as `https://contoso.crm4.dynamics.com`), the directory id and the app's id. Set its credential: the client secret.

**Test** asks the environment who the app is; nothing is changed.

## Connect Salesforce

1. In Salesforce Setup, make an **External Client App** with OAuth, and turn on the **client credentials flow**. Choose its **run-as user**: what that user may see and change is what the portal may. A user with **API Only** permission is best.
2. On **Connectors**, make a connector of the kind **A Salesforce org**, with the org's **My Domain** address (such as `https://acme.my.salesforce.com`, or a sandbox's) and the app's consumer key. Set its credential: the consumer secret.

**Test** reads the org's limits; nothing is changed.

## Work with a record

**A Dynamics 365 record** and **A Salesforce record** have **What to do**:

- **Create** makes a record with the columns or fields you set, and keeps its id. Salesforce assigns a record such as a Lead by the org's assignment rules; untick **Assign it by the org's rules** to keep the owner you set.
- **Read** keeps the columns or fields you name, or nothing when there is no such record.
- **Update** changes the columns or fields you set. It never makes a record that is not there.
- **Create or update** keeps a record in step: Dynamics 365 finds it by its id or an alternate key, Salesforce by an external id field. Jobs that copy records use it, because a run tried again never makes a second record.
- **Delete** removes the record.

Dynamics 365 names a table by its entity set, such as `contacts` or `accounts`, and a record by its id (a GUID) or by an alternate key. To set a lookup, name the column with `@odata.bind` and give `/accounts(<id>)`.

An empty value is sent as empty, so a date or a choice left blank in a form does not stop the step.

## Find records

**Find Dynamics 365 records** and **Find Salesforce records** keep the records whose columns or fields equal the values you give. For example, a contact whose email is the one typed in the form.

- **Columns to read** or **Fields to read**: names separated by commas. Salesforce reads a related record's field too, such as `Account.Name`.
- **Fixed filter** (Dynamics 365, in OData) or **Fixed condition** (Salesforce, in SOQL): a condition you write, such as `statecode eq 0`. It is used as written. No one's input reaches it.
- **Order by**, and how many: at most 5,000 from Dynamics 365 (50 when you say nothing) and 2,000 from Salesforce (200).

The answer has the records, and whether there are more.

The values you compare are given safely, whatever a person typed: they are compared as text. When a column holds a GUID, a date or a date-time, say so after its name: `_parentcustomerid_value:guid`, `createdon:date`, `CreatedDate:datetime`. Dates are written `2026-01-31`, date-times `2026-01-31T09:30:00Z` (Salesforce needs the seconds). An alternate key's columns are named the same way.

## Who may do what

- **Jobs and administrators** do everything.
- **Visitors** (forms anyone may send, endpoints anyone may call) and **signed-in people who do not administer** only create records. Reading, changing, deleting and finding are refused, when the site is saved and when it runs. Their answer is the new record's id. Whatever goes wrong, they are told only *The record could not be saved.*
- Visitors make at most 30 records an hour from one network, and 200 an hour on a portal; a signed-in person makes at most 30 an hour.

## Jobs and what visitors wrote

A job does everything, as the site's own doing. When a job works with what a visitor wrote, such as a record a public form made, its steps decide whose CRM record they change. A job that updates a contact found by an email a visitor typed changes whoever has that email. Find records by what the visitor cannot choose, or only create.

## Limits

- A run makes at most 20 calls to extensions: a job keeping many records in step runs again for the rest.
- An answer over 1 MB is refused: ask for fewer records or columns.
- An endpoint answering GET reads one record with a query by its id; **Read** of a record is for POST endpoints, forms, flows and jobs.
- The 200 records an hour visitors make on a portal are shared by all of them.
- An administrator's API token that may call endpoints does in the CRM whatever an administrator does.

When Dynamics 365 or Salesforce refuses a step of a job or an administrator, the step fails with the service's own words. Secrets and tokens never appear in them.

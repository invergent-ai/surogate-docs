---
title: Newsletters with Mailchimp and Constant Contact
description: Add people to Mailchimp or Constant Contact lists from forms and jobs, with their GDPR marketing permissions, and read, unsubscribe or remove them.
---

The portal's **Marketing** extension keeps your newsletter lists in [Mailchimp](https://mailchimp.com) or [Constant Contact](https://www.constantcontact.com). A form adds the person who fills it in to a list, with the marketing permissions they gave. A job or a signed-in person's form reads, unsubscribes or removes someone. As with every extension, it is open to every tenant of the portal.

## Connect Mailchimp

On **Connectors**, make a connector of the kind **A Mailchimp account**. Set its credential: an API key, made in Mailchimp under **Account → Extras → API keys**. The key ends with its data centre, such as `-us21`. **Test** reads the account; nothing is changed.

Once saved, the connector's page has **Show the lists**: each list's name and id, and whether it has GDPR fields. A step names a list by its id; **Copy** puts it on your clipboard.

## Connect Constant Contact

Constant Contact has no key to paste: the account is connected through an app of yours.

1. In Constant Contact's developer portal, make an app. Choose the **Authorization Code** flow and refresh tokens. Keep its API key and its client secret.
2. On **Connectors**, make a connector of the kind **A Constant Contact account**, with the app's API key. Save it.
3. The connector's page shows the **Address Constant Contact sends you back to**. Add it to the app's **Redirect URIs**, exactly as written.
4. Click **Connect to Constant Contact**, give the app's client secret, and choose the account on Constant Contact's page. You come back to the connector's page, which names the account connected. If it is not the one you meant, sign in to the right one at Constant Contact and connect again. It must be done within ten minutes.

The portal keeps the account connected. If Constant Contact stops letting it in (the app's access was removed, or it was unused for six months), the connector shows as not connected: connect it again. Connecting again is also the fix if the portal ever loses the account's newest token.

## Add a person to a Mailchimp list

In an action list, **A Mailchimp member** with **What to do** set to **Save**:

- **List id**, and **The person's email**.
- **Status of someone new**: **Pending** sends them Mailchimp's email to confirm (double opt-in; it is the default, and what GDPR forms should use); **Subscribed** adds them at once. Someone already on the list keeps their status unless the step names one.
- **Merge fields**, such as `FNAME` and `LNAME`; **Tags to add** and **Tags to take off**, as lists; **Language**, such as `ro`.
- **GDPR permissions**: each named as the list words it in Mailchimp, such as `Email`, given `true` or `false`. The list must have GDPR fields turned on. Permissions not named stay as they were. A name the list does not have stops the step before anything is written.

The other choices:

- **Read** keeps the member: their status, merge fields, tags and permissions, or nothing when the address is not on the list.
- **Archive** takes them off the list; Mailchimp keeps their history.
- **Erase for good** deletes them and their data from the list, as GDPR erasure asks. It is one list: erase them from each list they are on. Mailchimp will not let the address be added again by the portal.

A list id that is not the account's is said, rather than taken for "nobody there". Someone who unsubscribed cannot be made **Subscribed** again: Mailchimp refuses, and only **Pending** asks them again.

## Add a person to Constant Contact lists

**A Constant Contact contact** with **What to do** set to **Save** signs the person up to one or more lists (their ids, as a list), with their first and last name.

- Someone who unsubscribed is left unsubscribed, unless **Sign up again someone who unsubscribed** is ticked. Constant Contact would otherwise subscribe them again without asking.
- **Read** keeps the contact, or nothing. **Unsubscribe** stops all email to them; **Who unsubscribes** says whether the person asked (**The person**) or you did (**The account**, the default). Everything else of the contact is kept.
- **Delete** removes the contact from all lists. Constant Contact keeps deleted contacts for a while: for GDPR erasure, also delete them in Constant Contact itself.

## Whose address

Reading, unsubscribing, archiving, erasing or deleting someone is done by a job, by an administrator, or by a signed-in person for their own address. A member's form can let people manage their own subscription; it cannot reach anyone else's.

When a signed-in person saves someone else's address, it works as a visitor's save, below.

## Public forms

A form anyone may send only adds people: **Save**. Reading, unsubscribing, archiving, erasing or deleting someone is refused there. So is subscribing someone without asking them: Mailchimp's status must be **Pending** (or left out), and **Sign up again someone who unsubscribed** stays unticked.

What a visitor's save does is narrower too:

- An address already on the list is left as it is. Nothing about the person is changed, and nothing is shown back.
- Someone deleted from Constant Contact is not brought back.
- Whatever goes wrong is said the same way: *The address could not be added to the list.*
- Visitors add at most 30 people an hour from one network, and 200 an hour on a portal, each try counted.

When Mailchimp or Constant Contact refuses a step run by a job or someone signed in, the step fails with the service's own words. Keys and tokens never appear in them.

---
title: Managing people from steps
description: Find, invite and change the portal's own people from forms, endpoints and jobs; give them groups, turn their accounts on or off, and unlock them.
---

The portal's **People** extension lets steps manage the portal's own people, as the console's **Users** page does. A members' "my profile" form lets each person change their own name and fields. An administrators' form, or a job, invites people, gives them groups and unlocks them. As with every extension, it is open to every tenant of the portal.

## The actions

- **Find a person** keeps the person with an email: their id, name, whether their account is on, their fields, and their groups (given by hand, or by a directory). Nothing, when there is no such person.
- **Invite a person** sends someone new an invitation to a site, in the groups you name, with a message of yours, as the console does. Someone who already has an account is not invited. It needs the portal to send mail.
- **Change a person** changes their name and the fields you name; fields you do not name stay as they are. Your apps' person hooks see the change first, as they do in the console. It can also turn their account on or off: the last administrator's never.
- **Change a person's groups** gives groups and takes others away, by their names. A group a directory gives stays given.
- **Unlock a person** clears the failed sign-ins that hold them back.
- **Delete a person** turns the account off and marks it deleted: the person cannot sign in, their tokens stop working, they lose the roles and groups given by hand, and they leave the list of people (they are under **Deleted people** in **Users**). Their records and history stay, with their name. Jobs only, run as an administrator. The last active administrator, the person the job runs as, and an account a directory or SCIM keeps ("The account is managed by …") are not deleted. An administrator brings the person back under **Users**, **Deleted people**, with **Restore**. Erasing a person for good stays in the console.
- **Check a login and password** says whether they are right, as the sign-in page would, and signs no one in: it keeps `valid`, the person's `userId` when it is, and `reason` when it is not (`invalid`, `locked`, `disabled` or `noPassword`; a visitor is only told `invalid`, so nothing says whether an address has an account). Each wrong check counts against the same limits as a sign-in's, so an address held back there is held back here, and a right password is not looked at while it is locked. The password is never written in the run's log, a form's kept submission or the audit log; the check is in the audit log as `auth.credentials_checked`, with the login only for an account that exists. It works in forms and endpoints, for anyone.
- **Register a person** asks for a new account of one's own, in a form anyone may send: it takes an email, a name, an optional password (otherwise the person chooses it) and the user fields to set. The portal mails the link; the account is made, with those fields, when the link is used, and cannot sign in before. It works only while **People may create their own account** is on, and keeps to its email domains and groups. A visitor is told the same whether the address has an account or not; the owner of an address that has one is told by mail. It needs the portal to send mail, and keeps to the same limits as the sign-up page: 3 links an hour for one address and 5 for one network.

What a directory or SCIM keeps for a person (their name and fields) is not changed here, as in the console.

## Who may do what

- **Administrators** do everything, for anyone. On the portal's own tenant, that is an install administrator.
- **Signed-in people** find and change their own name and fields, nothing else. Any other address is refused the same way, whether it has an account or not.
- **A job** acts as the person it runs as (**Runs as**), who must be an administrator when the step runs. A job that runs as no one, or as someone who is not an administrator, is refused.
- **A job started by anything but time** (a record, a person's change, mail, a text message, a payment, an app's event, a page request) only finds people: what started it was written by others. A job that changes accounts runs on a schedule.
- **Forms anyone may send and endpoints anyone may call** use none of these actions, except **Check a login and password** and **Register a person**.

An API token acts here only when it may change the tenant (`tenant:write`), as in the console. An account a directory turned off is turned on by the directory, never by a step.

A members' form that lets people change their own name and fields lets them write those fields as they like: keep fields your apps or pages trust as an administrator's off such a form.

Each change is in the audit log as the person's, done **by an action**, naming the form, endpoint or job. It raises the same events as the console's changes, so jobs started by people hear of it.

## Limits

- Invitations from steps: at most 50 an hour on a portal, besides each inviter's own limit and the portal's mail allowance.
- A person is not made without an invitation; roles and organizations are changed in the console.
- Refusals are in the audit log too, without the address asked for.

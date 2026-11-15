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

What a directory or SCIM keeps for a person (their name and fields) is not changed here, as in the console.

## Who may do what

- **Administrators** do everything, for anyone. On the portal's own tenant, that is an install administrator.
- **Signed-in people** find and change their own name and fields, nothing else. Any other address is refused the same way, whether it has an account or not.
- **A job** acts as the person it runs as (**Runs as**), who must be an administrator when the step runs. A job that runs as no one, or as someone who is not an administrator, is refused.
- **A job started by mail, a text message or a page request** never invites, changes accounts' status or groups, or unlocks: who started it is not known.
- **Forms anyone may send and endpoints anyone may call** use none of these actions.

Each change is in the audit log as the person's, done **by an action**, naming the form, endpoint or job. It raises the same events as the console's changes, so jobs started by people hear of it.

## Limits

- Invitations from steps: at most 50 an hour on a portal, besides each inviter's own limit and the portal's mail allowance.
- A person is not made without an invitation; roles and organizations are changed in the console.
- An endpoint called with an administrator's API token acts as that administrator.

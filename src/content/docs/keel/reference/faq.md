---
title: Keel FAQ
sidebar:
  label: FAQ
---

Answers to the questions Keel's messages and empty screens raise.

## Working cases

### Why was my submission refused with "This is beyond your authority limit."?

The step checks authority: the case's amount must be within your limit in the step's scope. Either your limit there is lower than the amount, or you have no limit in that scope at all. A supervisor sets limits on the Team page; see [Authority limits](/keel/business/supervisors/#authority-limits). Votes are checked the same way.

### Why "Someone else must finish this step."?

The step is maker-checker: it must be done by someone other than whoever did one of the earlier steps it names, and you did one of them. Return the item to its queue, or delegate it.

### Why "A check on this step did not pass."?

One of the step's checks failed on the values you entered. The message the builders wrote for the check follows the sentence; change the values and submit again.

### Why "Some required fields are empty."?

The outcome you chose requires fields you left empty. Fill them, or choose another outcome.

### Why "The agent is waiting for an answer to its question."?

The step's agent raised a hand, and the step is paused until someone answers. Answer it on the Work page, or wait for whoever holds it.

### Why can I not claim an item?

- Only members of the item's queue claim it. Ask a supervisor to add you to the queue.
- A vote is never claimed: every member votes from the case.
- Someone may have taken it first: Keel says **Someone took it first.**

### Why is an item not in Needs me?

**Needs me** holds only what you hold. Unclaimed work in your queues is listed in the queue until you claim it, or until **Get next** gives it to you. An escalation is never in anyone's **Needs me**: it shows in the queue it went to. While an agent's question is open on a step, the question is the item, not the step.

### Why can I not delegate a vote?

A vote belongs to every member of its queue, so no one holds it. Each member votes for themselves.

### Why can I only comment on a document?

You edit a case's documents while you hold one of its steps. Otherwise you can comment, and the panel says who holds editing.

### Why does Get next say "Nothing is waiting for you."?

You hold nothing, and your queues have no unclaimed work. If you expected work, check that you are a member of the right queues.

### Why does an agent take no message?

An agent takes a message only while it is at work on the step with its hand down. It takes none while its question is open, after it failed, or while a supervisor has it turned off.

## Access

### Why do I not see the Team page?

Only supervisors see it. If you should be one, ask an owner of the project to appoint you in Keel Builder.

### Why does the app say "You are not on this project's staff"?

Your account signs in, but no one has added you to this project's staff. Ask a supervisor to add or invite you.

### Why does my set-password link not work?

A set-password link works once, until the time it was given with. Ask the person who invited you to invite you again: it gives a new link. If you are signed in already, sign out first.

### Why can someone not be invited?

| Message | Why |
|---|---|
| **More than one account uses this email. Ask an administrator to add the person.** | The email is shared by several accounts. |
| **This person signs in through another sign-in project and cannot be invited here.** | Their account belongs to another sign-in setup. |
| **This project has no organisation to invite people into. Ask an administrator.** | The project's business sign-in is not set up. |
| **This email or name is not accepted.** | The email or the name is not valid. |

### Why can I not remove a supervisor?

Supervisors are appointed and demoted by the project's owners in Keel Builder. Ask an owner to demote them; then remove them on the Team page.

## Moving cases

### Why do I not see Move by hand?

Only supervisors move cases by hand, from **More actions** on the case. It is offered on an open case, and on a case that closed because a step failed.

### Why is a step not offered in Move by hand?

**Move to** offers each stage's start, and the steps, votes and waits of each stage. It leaves out nodes on a parallel path, since a case moved onto one would wait at the join for paths no move opens. Decisions, rules, splits and joins are never targets.

### Why was a move refused?

Every move needs a reason. Keel also refuses a move that would leave the case open with nothing to do, and says why.

## Building

### Why is Publish turned off?

**Publish** turns on only when the last check of the draft found no problem and the draft has not changed since. Press **Run again** under **Checks**, fix what it lists, and run it again.

### What does "Main changed" mean?

Another draft was published after yours started, and changed some of the same files. Press **Update from main** on the review page. If both changed the same file, choose **Keep this draft's version** or update the draft by hand.

### Why does the draft bar say "Not saved"?

Keel refused or could not take your last change; the bar gives the reason. Press **Try again**. If the draft was published or discarded meanwhile, press **Open another draft**. Your change stays on screen until it is saved.

### Why can I not change anything?

You are a **Viewer** of the project. Ask an owner to make you an editor in Studio.

### Why can I not discard a draft?

Owners discard any draft. An editor discards only drafts they created.

### Why can I not set a credential?

A credential is set on the published connection. A connection new in your draft says **Publish this connection before setting its credential.** If the tab says **Credentials are off in this installation.**, ask your administrator.

### Why is my new agent not in the list?

Agents are made in Studio. Keel Builder reads the project's agents again when you come back to its window, at most once a minute, or when you reload the page.

### Why do running cases still use the old version?

Running cases stay on the version they started on. To move them, turn on **Move running cases** on the **Versions** tab of a draft, fill in the mapping, and publish. See [Versions](/keel/builder/versions/).

### Why did some cases stay on the old version after a move?

Each case that stayed is listed under **Cases that stayed**, with the reason, such as **No target for** a place the mapping left without a target. Fix the mapping in a new draft and publish again.

### Why can no one work a step?

A person step with neither a queue nor a person opens with no one to work it. Give the step a queue or a person, and publish. Cases already at the step need a supervisor's move by hand.

### Why does a form say "This form cannot be drawn yet. The dry run says why."?

Keel cannot build the form from the case type as it stands, for example because a field it names does not exist. Run a dry run to see the problem.

### Why does the designer say "The designer needs a wider screen"?

The designer needs a desktop screen. Open the case type on a computer. Every other page of Keel Builder works on a phone.

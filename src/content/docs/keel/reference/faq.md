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

## Agents and the case agent

### Why does the Case agent tab say "The project's case agent is not set up yet"?

Keel has no case agent for the project, or it is switched off. Keel sets it up when an editor or owner opens the project in Keel Builder. Ask one to open it, then try again.

### Why did the case agent not fill in my form?

It fills in only a form of yours: an open step of the case that you hold, and only when you ask. It fills only the fields that form has, and leaves out a value it is not sure of. A field you changed is yours, and no draft fills it again. A vote has no fields to fill.

### Why can I not give the case agent a file?

The case agent takes no files: "The case agent takes no files. Add them to the case instead." Add the file through a step's file field, then ask about it.

### Why can I not give an item to an agent?

Keel says why: **The agent cannot work this item: the project's case types do not name it, it is switched off, it is one of the project's helpers, only a person may act on the item, or the item has no queue for the agent to return it to.** An agent never takes an escalation, a step an agent drafts for a person, or a step that opened for people because its agent failed or was turned off. See [Agents in queues and as delegates](/keel/business/agents/#agents-in-queues-and-as-delegates).

### Why is an agent not offered in Delegate, Reassign or Add a member?

Only the agents the project's case types use are offered, and none a supervisor turned off. The project's helpers, the case agent and the designer agent, are never offered.

### Why does an agent's run have no Watch?

The run is on a work item the agent took from a queue or was handed. Only the runs of an agent's own steps open on Watch.

### Why does a comment say "The agent was not told about your comment"?

Keel could not pass the comment to the agent. "No agent works a step of yours on this case now." means you hold no step of the case that an agent drafts for you while it is at work.

## Access

### Why do I not see the Team page?

Only supervisors see it. If you should be one, ask an owner of the project to appoint you in Keel Builder.

### Why do I not see the Overview?

Only supervisors see it. A link to its address shows "Only the project's supervisors see the overview." If you should be one, ask an owner of the project to appoint you in Keel Builder.

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
| **Invitations cannot reach the runtime now; try again shortly.** | A temporary problem. Try again, or ask your administrator if it lasts. |

### Why can I not remove a supervisor?

Supervisors are appointed and demoted by the project's owners in Keel Builder. Ask an owner to demote them; then remove them on the Team page.

## Figures

### Why does a figure read — or None?

A dash (`—`) means Keel had nothing to measure, such as a median with no decided case behind it, or a cost when no decided case has an agent cost. **None** is a count of zero. A figure says no "was" when the period before has nothing to compare it with.

### Why does Keel say "The figures took too long to read. Try a shorter period."?

The figures count cases and agent runs over the period, and Keel stops a read that takes too long. Pick a shorter period in **Period**, such as **Last 7 days**, or press **Try again**. It applies to the [Overview](/keel/business/overview/) and to the [Agents page](/keel/builder/agents/).

### Why do Open cases and Past deadline not change with the period?

They count cases as of now. The other figures of the Overview cover the period.

### Why does Needs attention say "Nothing needs attention."?

No agent, wait or queue crossed the limits for the period. An agent is listed when its checks failed, or its hands went up, more often than in the period before. A wait is listed when several cases past their deadline wait on the client or a third party at one step. A queue is listed when many items nobody holds wait for its members, and the oldest has waited long. Your administrator sets those limits.

## Moving cases

### Why do I not see Move by hand?

Only supervisors move cases by hand, from **More actions** on the case. It is offered on an open case; a closed case has no **More actions**.

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

The project's helpers, the case agent and the designer agent, are never in the list of a step's agents or of intake agents.

### Why is an agent not on the Agents page?

The page lists the agents named by the current published versions of the project's case types. An agent a draft adds shows once the draft is published. An agent named only to start cases shows with `0 steps in 0 case types`. The project's helpers are listed apart, under **Helpers, not on any step**. See [The Agents page](/keel/builder/agents/#the-list).

### Why does the Agents page show no sessions or raised hands?

You are a **Viewer** of the project. The page says "Sessions and raised hands show case content. The project's editors and owners read them." Ask an owner to make you an editor in Studio.

### Why does Export for audit refuse?

Keel refuses a period that holds more than 100,000 runs: "The export holds more than 100,000 runs; choose a shorter period." Pick a shorter **Period**, then export again. See [Export for audit](/keel/builder/agents/#export-for-audit).

### Why is there no "Ask the designer agent"?

It shows in the designer to editors and owners, in an open draft. With **Published** shown, open or start a draft first. Viewers do not see it.

### Why can I not edit while the designer agent works?

While the designer agent takes its turn, the designer is read-only: "The designer agent is working in this draft. You can edit again when its turn ends." The draft bar, **Dry run** and **Review and publish** stay available.

### Why does the designer agent's panel say "The designer agent is switched off in Studio."?

Someone switched the project's designer agent off in Studio. It works again once it is switched on there.

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

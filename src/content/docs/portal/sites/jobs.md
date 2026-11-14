---
title: Automation jobs
description: "What the portal does on its own, on a schedule, as a set person: a trigger and a list of actions."
---

An automation job is work the portal does on its own: count the new requests every morning, close what has waited too long, refresh figures every hour. It is a trigger and a list of [actions](/portal/sites/actions/), run as a set person on a set site.

## In the console

A job tells no page anything and answers no one, so what people see of it is what it does: a record added, an email sent, a line in a log. Administrators see the jobs under **Jobs** in the console: its trigger, the person it runs as and their roles, when it runs next, whether it runs now, how many changes it still has to run for, and its last runs with their logs:

![The Automation jobs page: the job cerere-inregistrata, which runs when requests are created, and the job cereri-noi, which runs on a schedule, each with the person it runs as and its last runs marked ok, with Log, and Run now for the scheduled one.](../../../../assets/screenshots/portal-jobs-console.png)

**Log** shows what a run wrote:

![The Automation jobs page with the log of a run open under the jobs: "info: Cereri în registru: 4".](../../../../assets/screenshots/portal-jobs-log.png)

Runs are kept 30 days, with only their errors unless the job is set to debug. **Run now** runs a job on a time at once, as its person. The portal runs a job once for each time, however many servers it has.

## Write a job

A job runs for one site; that site's first language is the run's. It acts as a person it names: what that person may see and change, the job may. Without a person, the job acts as a visitor. When the person no longer exists or may not sign in, the run fails and says so. A description says what the job is for, in the console.

The console shows the portal's jobs and their runs; it does not write jobs yet. For now, this is set in the site's configuration: see [Developer: Automation jobs](/portal/developer/jobs/#write-a-job).

## When it runs

A job runs:

| Trigger | Runs |
|---|---|
| Every so often | every so many minutes, hours or days, from 5 minutes to 30 days, such as every 15 minutes |
| Daily | every day at a time, such as 07:30 |
| On a cron schedule | at the minutes the five fields name: minute, hour, day of month, month, day of week (0 is Sunday) |
| Once | at a set moment |

Daily and cron times follow a time zone, UTC unless the job names one. On the night clocks go forward, a time that does not exist that night is not run; on the night they go back, a time that happens twice runs once.

By default, a time that comes while the job still runs is skipped and kept in its history; a job can instead let a run wait for the one before to end. A job also says what happens to times missed while the portal was not running: by default it runs the job once; or it can go straight to the next time.

## When records change

A job can also start when a [data model's](/portal/sites/data-models/) records are created, updated or deleted. Each change runs the job once, the oldest first. The run knows the change:

- whether the record was created, updated or deleted;
- the record's id;
- the record before the change (none when it was created) and after it (none when it was deleted);
- when the change was made.

The record before and the record after hold only what the job's person may see of that model: when they may see only their own records, another person's record is empty there, and its id alone is given.

A change made by a job may start jobs again, at most three deep, so a job that changes the record it was started by stops there; the job's history says so. At most 100 changes wait for a job; past that, new ones are not run, and the history says so once a minute. A change that is undone never starts a job. When a record linked from another is deleted and the link is cleared, that other record's change starts no job.

**Run now** is for jobs on a time: a job started by records runs only for a change.

## When people come and go

A job can start when a person is created, changed or signs in; it says which of the three. The job runs once each time, however it happened: in the console, through SCIM, through a sign-in with a provider or a directory, or through a directory's sync.

The run knows what happened, the person's id and when. It also has their name and email as they are when the run starts, only when the job runs as an administrator; otherwise, and once the person is gone, it has none.

At most 5,000 people wait for a job, enough for a directory that brings many at once; past that, new ones are not run, and the history says so.

## When the portal starts, fails or is asked for

A job can start when the portal's configuration starts, when a run fails, or when a page is asked for:

- **The portal starts:** once each time a new configuration is published or rolled back, and when the job first appears. The run knows the revision.
- **A run fails:** a form, endpoint or job ended failed. The job names which of the three it hears of; all three when it names none. The run knows which kind and which one, the run's id, the reason and the message. The message is the run's own words only for a job that runs as an administrator, since they may hold what people sent; other jobs get only the words the portal shows anyone, or none.
  - Not heard of: a run the portal was too busy to start, the failures of a job that itself hears of failures, and an endpoint another one called (the run that called it is heard of instead).
  - A job hears of one form, endpoint or job at most once a minute.
- **A page is asked for:** a page of the job's site was asked for, at or under one of the paths the job names (1 to 20). `/news` takes `/news` and `/news/today`, never `/newsletter`. The run knows the path (an article's own address, such as `/news/my-article`), the language and the person's id (none for a visitor).
  - Counted: a page opened. Not counted: a page checked again for changes, a preview, and pages served from a cache before the portal.
  - A job hears of at most 60 pages a minute; the pages never wait for it.

Paths are named only for a job that starts when a page is asked for, and the kinds of run only for one that starts when a run fails. At most 100 events wait for a job; past that, new ones are not run, and the history says so.

## When mail arrives

A job can start for each message that arrives in a [mailbox](/portal/sites/connectors/#mailboxes). The run knows:

- who sent the message (address and name), who it was sent to and who was copied;
- its subject, its date and its text (at most 64 KB);
- its attachments, each file's name, type and size (the files themselves are not read);
- whether it is an automatic reply or comes from a mailing list, and the list's id.

A message over 5 MB gives only who sent it and its subject, and is marked too large. A message the portal cannot read at all runs the job with only a mark that it is unreadable, so the mail after it is still read.

- **When:** the mailbox is read about once a minute, and up to 20 new messages are taken each time. The job runs once for each.
- **From when:** the first read only marks where the job begins. Mail that was there before is never run for. The same is true after the job's trigger, the mailbox's server or folder, or its username changes; the job's history says so.
- **Failures:** when the mailbox cannot be read (a wrong password, a server that does not answer, a certificate the portal does not trust), **Jobs** shows why, the history says so once, and the next tries wait longer, up to an hour.
- **Loops:** a job that sends mail to the address it reads starts itself again. Skip machine mail by acting only when the message is not an automatic reply.

## When an app sends an event

A job can start each time an approved app's server publishes one of its events. The run knows the app, the event's name, its fields, and the person when the app named one. Events sent in the browser do not start jobs. At most 100 events wait for a job; past that, new ones are not run, and the history says so. Once the app is no longer approved, its events start nothing. A job that calls an app whose answer sends the event that starts the job again stops after three rounds.

## When something happens in the DMS

A job can run when a document changes in the DMS. See [Documents](/portal/sites/documents/#when-something-happens-in-the-dms) for the events and what the run reads.

## When something happens in Keel

A job can run when a case or process changes in Keel. See [Keel](/portal/sites/keel/#when-something-happens-in-keel) for the events and what the run reads.

## Send mail

A job may send email, as forms do. Its mail leaves once the run ends well, within the portal's hourly room, and at most 100 recipients an hour for each job.

## What it may do

The actions read what started the job, the person, the site, what the actions before kept and the named values, and may call [flows](/portal/sites/flows/). A run has three minutes.

A job tells no page anything and answers no one. It may not use a [connector](/portal/sites/connectors/) that signs in as each person, since no one is at the keyboard.

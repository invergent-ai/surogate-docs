---
title: Automation jobs
description: "What the portal does on its own, on a schedule, as a set person: a trigger and a list of actions."
---

An automation job is work the portal does on its own: count the new requests every morning, close what has waited too long, refresh figures every hour. It is a trigger and a list of [actions](/portal/sites/actions/), run as a set person on a set site.

## Write a job

Each job is a file `jobs/<id>.yaml`:

```yaml
trigger:
  cron: "0 7 * * 1-5"
  timezone: Europe/Bucharest
site: main
runAs: user:clerk@primaria.ro
actions:
  - type: findRecords
    model: requests
    where: { status: '"new"' }
    into: open
  - type: log
    level: info
    message: '"New requests this morning: " + string(size(vars.open))'
onError:
  - type: log
    level: warn
    message: error.message
```

- `site` is the site the job runs for; its first language is the run's.
- `runAs` names the person the job acts as: what they may see and change, the job may. Without it, the job acts as a visitor. When the person no longer exists or may not sign in, the run fails and says so.
- `description` says what it is for, in the console.

## When it runs

`trigger` is one of:

| Trigger | Runs |
|---|---|
| `every: 15m` | every 15 minutes (also `2h`, `1d`; from 5 minutes to 30 days) |
| `daily: "07:30"` | every day at that time |
| `cron: "0 7 * * 1-5"` | at the minutes the five fields name: minute, hour, day of month, month, day of week (0 is Sunday) |
| `at: 2026-12-01T08:00:00+02:00` | once, at that moment |

`daily` and `cron` follow `timezone`, UTC when left out. On the night clocks go forward, a time that does not exist that night is not run; on the night they go back, a time that happens twice runs once.

`skipIfRunning: false` lets a run wait for the one before to end; by default, a time that comes while the job still runs is skipped and kept in its history. `misfire` says what happens to times missed while the portal was not running: `once` (the default) runs the job once, `skip` goes straight to the next time.

## What it may do

The actions read `trigger` (`kind` is `time` or `manual`, `at` is the time it was due), the person as `user`, `site`, `vars` and `values`, and may call [flows](/portal/sites/flows/). A run has a minute.

A job tells no page anything, answers no one and sends no mail. It may not use a [connector](/portal/sites/connectors/) that signs in as each person, since no one is at the keyboard.

## In the console

**Jobs** lists every job: its trigger, the person it runs as and their roles, when it runs next, whether it runs now, and its last runs with their logs. **Run now** runs it at once, as its person. Only its errors are kept in a run's log, unless the job has `debug: true`.

The portal runs a job once for each time, however many servers it has.

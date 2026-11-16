---
title: Health, logs and updates
description: For install administrators: whether what the portal needs answers, who is told when something is down, the servers' warnings and errors, and which version runs.
---

These pages are for **install administrators**, on the main portal's console, next to **Tenants**.

## Health

**Health** shows each check with its state (**OK**, **Attention** or **Down**), what it saw and how long it took, refreshed every half minute:

- **Database**: it answers.
- **Tenants' configuration**: every tenant has a live configuration.
- **Event deliveries** and **Jobs**: how many failed in the last hour (Attention from one, Down from fifty).
- **Mail**: how long the oldest mail has waited (Attention past 15 minutes, Down past an hour); shown only when the install has a mail server.
- **Site files store**, **Search** and **Analytics**: they answer; shown only when the install has them.

A check that does not answer in 3 seconds is **Down**. The page says which server it was seen from: with several, each sees the same database and services.

## Alerts

Under **Alerts**, write up to 10 **Email addresses**, and an optional **Webhook**: an https address that takes a JSON message with a `text`, such as a chat channel's incoming webhook. The webhook is kept as a secret: the page shows only its host.

When a check goes **Down**, and when it is back, one message goes out, from one server, at most once an hour for each check. **Attention** shows on the page but sends nothing. The database is not alerted (telling needs it): the cluster's own probes watch it. Without a mail server, only the webhook can be told.

## Logs

**Logs** lists the servers' warnings and errors of the last seven days, newest first, at most 200 at a time: when, which server, the message, and the error's type and message. Choose **At least** a warning or an error, and search by **Words**. Addresses are cut to their site, and emails, passwords and long codes are hidden.

## Updates

**Updates** shows the version running and the newest released, read from the image registry with the install's pull credential (otherwise **Cannot check**). The portal never upgrades itself: run the installer's portal stage on the cluster's node.

## Metrics and traces

An install can send OpenTelemetry metrics (request and database times, mail waiting, deliveries failing) and traces (a sample of requests, by route, never their address or who made them) to a collector: set it at install time. Nothing is sent otherwise.

---
title: Analytics
description: Count a site's visits and page views, see where visitors come from, and ask their consent before recognising them again.
---

A site's **analytics** counts its visits and page views and shows, in the console, which pages people read, where their visits start, where they come from and on what devices. The portal sends what it counts to the install's own analytics service, [Matomo](https://matomo.org), which keeps it on the install's servers. Analytics is there once the install's operator has set it up; until then the site's settings say so.

## Turn it on

In the console, open **Sites**, then **Settings** on a site. Under **Analytics**:

- **Count this site's page views** turns it on. The first save makes the site's place in the analytics service; from then on its pages are counted.
- **Ask visitors' consent to recognise them on later visits** shows visitors a short question, with **Yes** and **No** equally. Only those who answer yes are recognised when they come back.
- **Recognise signed-in people who consent, by a code of their account** counts a signed-in person who said yes as the same visitor on every device. The service gets a code made from their account, never their name, email or id. It needs consent asked.

## What is counted, and what never is

- **No cookie** is set, whether a visitor consents or not.
- **Without consent**, visits are counted without recognising anyone again: the same person on two days counts as two visitors.
- **With consent**, the browser keeps a random code for the site, and the visitor is recognised on later visits. The site's other settings, and other sites on the same address, ask on their own.
- A browser that asks not to be tracked (Global Privacy Control, Do Not Track) is never asked, and never recognised.
- Page addresses are counted without what follows `?` or `#`, where search terms or someone's email could be. The portal's own pages (signing in, resetting a password, the console) are never counted, nor previews, robots or the console's own views of a page.
- Where a visitor came from is kept as the other site's address without its query.

**Let visitors change their mind.** Put a link to `#portal-consent` on the site, such as **Privacy choices** in its footer: it asks the question again, and their earlier answer is forgotten.

## The report

On **Sites**, a site with analytics on has **Analytics**. For a day, a week, a month or a year (today unless you pick a date), it shows:

- **Visits**, **Visitors**, **Page views**, how many **left after one page**, and the average **time on site**;
- the visits of each of the last 30 days;
- **Pages**, with their visits and views; **Where visits start**; **Where visitors come from** (search engines, other websites, typed in, campaigns); **Websites linking here**; **Search engines**; **Devices**.

The numbers are a minute old at most. When page views could not reach the analytics service lately, or some were let go while it could not take them, the report says so.

## Limits

- Only administrators see the report.
- Visitors' countries are not counted yet.
- Turning analytics off stops the counting; what was counted stays in the analytics service, and turning it on again goes on from there. Removing a site leaves its counts behind, and a new site of the same name starts afresh.

---
title: Experiments
description: Try versions of a page's blocks on the people who agreed to it, count who then reaches a page or sends a form, and keep the version that does best.
---

An experiment shows each person one version of some blocks, and counts how many of those who saw each version then reach a goal: a page they open, or a form they send. A town hall tries two versions of its "Pay your taxes online" banner, shows each to half of the people, and keeps the one after which more people open the payment page.

## Make an experiment

In the console, **Experiments** lists the tenant's experiments and whether each runs. **New experiment** makes one:

- **Name**, in each language, and an **Id** (blocks name the experiment by it).
- **Versions**: 2 to 5. The first is the control, what people see now. A **Weight** is each version's share of people: 1 each shares them equally; 3 and 1 shows the second version to a quarter.
- **Goal**: **Opening a page** (a site and one of its pages) or **Sending a form**. The goal page cannot show the experiment itself.

Then, in the page editor, open each block or group that is a version, and under **Experiment** choose the experiment and its **Version**. A version can be a group of blocks, or nothing at all: a version with no blocks tests showing nothing.

## Who is in it

**Only people who accepted the analytics question** on a site that asks it are in an experiment and counted, whether they are signed in or not. Turn on [analytics](/portal/sites/analytics/) with **Ask visitors' consent** on each site where people should take part. Everyone else, and staff, see the first version and are not counted. Each person sees the same version on every visit and every page: a signed-in person by their account, a visitor by the cookie their consent allows.

What is kept of each person is a code made with the install's key from who they are, the version they saw, and when they reached the goal: never their name, address or account. It is in a signed-in person's data export and is erased with them. All of it goes 13 months after they saw the experiment, and 30 days after the experiment is removed.

## Run it

- **Start the experiment**, then **Save**: from then on each person in it sees their version. Versions and weights stay as they are while it runs.
- **End the experiment**, choosing the **Version to keep** (or none, to show the first), then **Save**: everyone sees that version, and nobody is counted any more.
- **Start again** counts anew.

A page that shows a running experiment, or is its goal page, is made for each visitor and never kept by shared caches. A busy public page pays for that while the experiment runs.

## Results

The experiment's page shows, for each version, how many people saw it, how many reached the goal, and the rate. Each version is compared with the first once both have at least 100 people, 5 of whom reached the goal and 5 of whom did not: how much higher or lower its rate is, and how sure it is that the difference is real. With more versions, a difference must be surer. **Likely better so far** marks a version whose rate is higher at 95% or more. Let the experiment run long enough, through a whole week of visitors, before you decide.

## Limits

- At most 20 experiments, each with 2 to 5 versions.
- Search finds the text of an experiment's blocks only once it ended, and only the version everyone sees.
- Previews show the first version.

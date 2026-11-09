---
title: Design studio
description: Each portal can have a design studio of its own, where its administrators design the portal's sites with the portal's own AI.
---

The design studio is an AI design tool for the portal's sites. You describe a page, a layout or a whole brand, and it designs it with the portal's own AI model, showing the result as it goes. Each portal has a studio of its own, with its own projects; no other portal sees them. **Design studio** is for administrators.

The studio appears only on installs where your implementation team has turned design studios on. Otherwise the page says **This portal has no design studio**.

## Turn it on

1. Open **Design studio**.
2. Press **Turn on**. The studio shows **Starting** while it gets ready, which takes a minute or two the first time. The page updates by itself.
3. When it shows **Ready**, press **Open studio**.

If it shows **Not running**, the reason is under it; **Start again** tries once more. If it stays that way, tell your implementation team.

The studio opens on its own address, already signed in as you. Only the portal's administrators can open it; anyone else who reaches its address is sent to sign in to the console.

## Design in the studio

The studio is where you explore designs: describe what you want, look at what it makes, and ask for changes. It designs with the portal's own model, so you need no account or key of your own, and it cannot be pointed at another one.

What the portal shows to visitors is still the site's [design package](/portal/sites/design/) in the config repository. A design you like in the studio reaches the site through that package, reviewed and merged like any other change.

## Turn it off

**Turn off** stops the studio. Its projects and files are kept, and **Turn on** brings it back as it was.

## New tokens

The studio talks to the portal with tokens of its own, which nobody needs to see. **New tokens** replaces them, for example after a security review. The studio starts again with the new ones; anyone working in it is out for a moment.

## Erase

**Erase** removes the studio with every project, design and file in it, whether it is on or off. Type `erase` to confirm. This can't be undone. While it goes, the studio shows **Being erased**; if that lasts, press **Erase** again. You can turn on a new, empty studio afterwards.

Turning the studio on and off, opening it, new tokens and erasing are in the [audit log](/portal/console/audit/).

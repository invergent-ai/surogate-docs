---
title: Develop locally
description: Run the portal on your own machine, see every change to a site or an app at once, and test against a throwaway portal.
---

You can build a customer's portal on your own machine before anything reaches a shared environment. The portal starts in a few seconds in Docker. A command keeps it in step with your files, and the open pages reload when they change. Your tests can start a portal of their own.

## Start the portal

You need Docker and Bun. In the portal's repository:

```sh
bun deploy/local/up.ts
```

- The first run makes the portal's secrets and an administrator, and keeps them in `deploy/local/.env`. That file is never committed.
- It prints the console's address, the administrator's email, and the line to paste into your terminal for `portal dev`.
- The portal is ready about two seconds after it starts. The first run also builds it, which takes longer.
- To use other ports, set them in `deploy/local/.env` before the first run; the repository's README names them.

`bun deploy/local/down.ts` stops it. `bun deploy/local/down.ts --wipe` also removes its data and the secrets it made, keeping the ports you set, so the next start is a fresh portal.

This portal runs in **dev mode**: it takes your files directly, and its pages reload when they change. It answers on your machine only. Dev mode is only for your own machine; a real install never runs in it.

Apps you are building run on your machine too. The portal and your browser both reach them at `http://localhost:<port>`. Name them that way in the site's files, as `create-portal-app` already does.

## Keep it in step with your files

```sh
portal dev ./portal-config --watch ../my-app --types my-app=../my-app/src/portal-types.ts
```

- `portal dev` sends the folder's files, then makes its sites if they are missing, at the portal's address: the first at `/` while nothing else is there, the others at `/<site>`.
- It prints whether the portal took the files or which file and field to fix. Files the portal refuses never replace what works.
- Then it watches the folder and each `--watch` folder. On every save it sends the files again and the open pages reload. A burst of saves sends them once.
- A change in an app's folder brings in the app's new manifest and hook modules. A rebuilt hook takes effect a few seconds later.
- `--types` writes an app's types again after each change, so your editor checks the code against what the portal took.
- `--once` sends the files once and stops, for a script.
- Press Ctrl-C to stop.

A new app made with [`create-portal-app`](/portal/sites/build-an-app/#start-from-a-working-app) has a `portal-config` folder with a small site that shows its two widgets. Start there:

```sh
portal dev ./portal-config --watch . --types my-app=src/portal-types.ts
```

Then [approve](/portal/console/apps/) the app on the console once, and open the portal's address.

## Test against a throwaway portal

`@invergent/portal-testing` starts a portal of its own for your tests, with your config and the people you name. It removes it after.

```ts
import { startPortal } from "@invergent/portal-testing";

const portal = await startPortal({
  config: "./portal-config",
  seed: { users: [{ email: "ana@example.ro", name: "Ana Pop", password: "a long enough password" }] },
});

const page = await fetch(`${portal.url}/`);
const people = await portal.request("GET", "/_portal/api/tenant/users");

await portal.stop();
```

- It needs Docker, and takes about ten seconds to start.
- It runs the portal image your setup names. Until the portal's images are published, build one with `bun deploy/local/up.ts` in the portal's repository and name it, as the package's README says.
- `portal.url` is its address. `portal.token` is a token of its administrator. `portal.request` calls it with that token.
- `portal.upload(files)` changes its config mid-test.
- Apps your tests run on `localhost` are reachable from it.
- If a test run is killed, `pruneTestPortals()` removes what it left behind.

Before you push, [check the site](/portal/sites/check-a-site/): the same portal renders every page and checks it.

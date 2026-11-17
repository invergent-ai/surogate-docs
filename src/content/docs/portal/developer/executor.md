---
title: The executor
description: The container that runs jobs' scripts and programs, how an installation sets it up, and the runScript, runExecutable and runJs actions as the site's configuration writes them.
---

What these actions do for a site's administrators is on [Automation jobs](/portal/sites/jobs/#scripts-and-programs).

## What the installation provides

Scripts and programs never run on the portal's server. They run in the **executor**, a separate container (`deploy/executor`, its image from the portal's repository, and the `surogate-portal-executor` chart) that:

- has no network: its pod's policy lets nothing out and lets in only the portal's pods. It checks this when it starts, by trying to reach public addresses and the cloud's metadata address, and **refuses to start** where it can reach any of them (set `EXECUTOR_ALLOW_NETWORK=1` only on a machine you are testing on). A network policy does nothing unless the cluster's network plugin enforces it: use one that does;
- starts each run as **a user of its own**, from a range of ids set aside for it (`runUidBase`, 41000 to 41003 by default, one id for each of its four places). Runs cannot read each other's files, the executor's memory or its secret; their directories are readable by no one else; and when a run ends, every process that user started, in whatever group or session, is stopped, and what it left in `/tmp` is removed, before the place is used again. The system counts processes by user across the whole node, so choose a range that nothing else on the nodes uses, and a different range for each executor that shares a node;
- is root in its container, with only the capabilities it needs to do that (`SETUID`, `SETGID`, `KILL`, `CHOWN`, `DAC_OVERRIDE`), no new privileges, a read-only file system and a scratch volume. A cluster that admits only the restricted pod security level refuses it: it needs the baseline level, in a namespace of its own. It refuses to start where it cannot start a run as another user;
- reads the token the portal signs with from a file (`/run/executor/token`, mounted from the secret, readable by no run) and never from an environment variable;
- holds the interpreters (Python 3 and Bash in the stock image) and the programs the image is built with (the stock image has `ogr2ogr` and `pdftotext`). A program is added by installing it in the image and naming it in the `RUN bun build-manifest.ts` step of the Dockerfile, which writes `/etc/portal-executor/manifest.json`: its id, description and the SHA-256 of its file.

The portal reaches it with two settings of the portal's chart:

```yaml
executor:
  url: http://portal-executor:8090
  tokenSecret:
    secretName: portal-executor      # a secret with a token of at least 32 characters
    key: token
```

The same secret is the executor chart's `tokenSecret`. The token is trimmed of surrounding white space on both sides, so a line break at the end of a secret's value does no harm. The portal's calls carry it as a bearer token over plain HTTP: keep the executor inside the cluster, behind its network policy, never on a public address; where traffic between pods is not trusted, put a mesh or TLS in front of it. Without `executor.url` the portal says it has no executor and the actions are offered but cannot be chosen.

The pod is given the memory of all its places at once (4 runs of at most 1024 MB each, and its own room: 5 Gi); change `resources` and the runs' memory together.

Each run: a directory made for it and removed after, an empty environment, `in/` for the files it reads and `out/` for what it makes, a limit on processes for its user, a process group killed whole at its time, and its memory watched. What a run made is read only after nothing of it is left running, and only plain files that no other name points to; a link, whatever it points at, fails the run. At most 4 runs at once in all and 2 for one tenant (the executor tells them apart by what the portal sends with each run), so another tenant always finds a place. Before a program runs, the executor checks that its file's SHA-256 is the one the manifest declares; if not, the run fails with `changed`.

A tenant's administrators decide two things in the console, under **Jobs**, **Executor**: which programs jobs may run, and whether jobs may run scripts at all (**Scripts are allowed in jobs**, off at first). A script can run any program the image holds, so the list of allowed programs holds for `runExecutable` only.

## The actions

```yaml
- type: runScript
  language: python3                 # an interpreter the executor declares
  script: |
    import json, sys
    print(json.dumps({"n": len(json.load(sys.stdin)["items"])}))
  args: ["'--month'", "string(trigger.at)"]   # each an expression, one argument
  input: '{"items": vars.items}'              # written as JSON on the standard input
  inputFolder: documente
  inputNames: "['a.csv']"                     # found under in/
  outputFolder: documente                     # what is written under out/ is saved here
  timeoutSec: 30                              # 1 to 170
  # what it writes under out/: 20 files, 10 MB each and 50 MB together
  memoryMb: 256                               # 64 to 1024
  outputJson: true
  into: r                                     # {exitCode, stdout, stderr, files, durationMs}

- type: runExecutable
  executable: ogr2ogr                         # one an administrator allowed
  args: ["'-f'", "'GeoJSON'", "'out/x.json'", "'in/x.shp'"]

- type: runJs
  code: "return input.linii.reduce((s, l) => s + l.kg, 0);"
  input: { linii: form.linii }
  timeoutMs: 1000                             # 100 to 5000
  into: total
```

`runScript` and `runExecutable` are for jobs only, and `runScript` fails with `missing` until an administrator allows scripts. `runJs` runs anywhere a list does; its places are shared among tenants (a tenant holds at most 2 of 4), and in a form or an endpoint anyone may send it gets one second at most and one place at a time. All three are changed only by administrators. The executor speaks `GET /info` and `POST /run` (multipart: a JSON `spec` and the input files; the answer is a JSON `result` and the files made), with `Authorization: Bearer <token>`.

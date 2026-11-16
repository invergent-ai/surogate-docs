---
title: The executor
description: The container that runs jobs' scripts and programs, how an installation sets it up, and the runScript, runExecutable and runJs actions as the site's configuration writes them.
---

What these actions do for a site's administrators is on [Automation jobs](/portal/sites/jobs/#scripts-and-programs).

## What the installation provides

Scripts and programs never run on the portal's server. They run in the **executor**, a separate container (`deploy/executor`, its image from the portal's repository, and the `surogate-portal-executor` chart) that:

- has no network: its pod's policy lets nothing out and lets in only the portal's pods;
- runs as an unprivileged user on a read-only file system, with a scratch volume;
- holds the interpreters (Python 3 and Bash in the stock image) and the programs the image is built with (the stock image has `ogr2ogr` and `pdftotext`). A program is added by installing it in the image and naming it in the `RUN bun build-manifest.ts` step of the Dockerfile, which writes `/etc/portal-executor/manifest.json`: its id, description and the SHA-256 of its file.

The portal reaches it with two settings of the portal's chart:

```yaml
executor:
  url: http://portal-executor:8090
  tokenSecret:
    secretName: portal-executor      # a secret with a token of at least 32 characters
    key: token
```

The same secret is the executor's `tokenSecret`. Without `executor.url` the portal says it has no executor and the actions are offered but cannot be chosen.

Each run: a directory made for it and removed after, an empty environment, `in/` for the files it reads and `out/` for what it makes, a limit on processes, a process group killed whole at its time, and its memory watched (the executor's own container limit is the last guard). At most 4 runs at once. Before a program runs, the executor checks that its file's SHA-256 is the one the manifest declares; if not, the run fails with `changed`.

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

`runScript` and `runExecutable` are for jobs only. `runJs` runs anywhere a list does. All three are changed only by administrators. The executor speaks `GET /info` and `POST /run` (multipart: a JSON `spec` and the input files; the answer is a JSON `result` and the files made), with `Authorization: Bearer <token>`.

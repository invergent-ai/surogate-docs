---
title: Data console
description: The file that turns the data console on, and the limits on a query's rows and time.
---

The configuration behind [Data console](/portal/console/data-console/). That page covers what the console shows, what a query may read, downloads and saved queries, and who may use it.

## The data console's file

The console is off until the portal's files hold `data-console.yaml`. `rows` and `seconds` may be left out; the values in the example are what they are then.

In `data-console.yaml`, at the top of the portal's files:

```yaml
enabled: true
rows: 1000     # the most rows a query shows, 1 to 10000
seconds: 5     # the most time a query may take, 1 to 30
```

- `enabled: true` turns the console on.
- `rows`: the most rows a query shows, 1 to 10,000; 1,000 when left out.
- `seconds`: the most time a query may take, 1 to 30; 5 when left out.

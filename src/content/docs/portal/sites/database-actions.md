---
title: Database actions
description: Run a SQL query on your own database from a job, a form or a flow, and load the rows it answers into a data model.
---

Two actions of the **Databases** section work with SQL databases. **Run a SQL query** reads from, or changes, a database through its [connector](/portal/sites/connectors/#sql-databases). **Load records from a list** writes each row of a list, such as the rows of a query, into a [data model](/portal/sites/data-models/). They are in every action list: a form's [steps](/portal/console/forms/#steps), and a job's, an endpoint's or a flow's actions.

## What people see

An administrator adds **Run a SQL query** from **Add an action…**, under **Databases**, and sets it in its row:

![A job's Actions tab with Run a SQL query on the connector siui open: the Database, Most rows and Most seconds, the parameter judet with the value 'Cluj', the query select cod, denumire, paturi from unitati where judet = :judet, its Mode, and the name unitati the answer is kept as.](../../../../assets/screenshots/portal-data-action-runsql.png)

People never see the action. They see its effect: a [listing](/portal/sites/listings/) that shows the rows a job loaded, a form that was answered from the database, or a record that appeared.

## Run a SQL query

- **Database:** the connector to run on. The list offers the portal's SQL database connectors, and the portal's own data (see below).
- **Query:** one statement. Write each value as `:name`, and give the value under **Parameters**. A value is bound apart from the text, so nothing a visitor typed can change what the statement does.
- **Parameters:** a name and an expression for each `:name`, such as `form.county` or `user.email`. A value is one text, number or yes or no.
- **Mode:** **read** (the default) runs a SELECT. **write** runs an INSERT, UPDATE, DELETE, MERGE or CALL. Other statements, such as schema changes, grants, transactions, and procedures of the database's own, are never run. One statement only.
- **Most rows** and **Most seconds:** how many rows a read keeps, and how long it may take. Left empty, the connector's own limits hold.
- **Keep the answer as:** a name. Later actions read it as `vars.<name>`, with its `rows`, `columns`, `rowCount`, `truncated` (whether there were more rows) and, for a change, `affected`.

The query is checked when the portal's files are saved: it has one statement of the mode, a value for each `:name`, and the connector exists and allows what it does.

### Changing data

A change is allowed only when:

- the connector has **Allow changes** on;
- the run is not a visitor's, and the portal is not being seen as someone else;
- it is not in a GET endpoint, or an endpoint anyone may call.

Each change is written to the [audit log](/portal/console/audit/) as **sql.change**, with who, which connector, which job or form, and how many rows it changed. The values and the rows are never written there.

### The portal's own data

**The portal's data** reads the tables of your [data models](/portal/sites/data-models/) with SQL. It is for [jobs](/portal/sites/jobs/) that run as an administrator, and only when the [data console](/portal/console/data-console/) is on. It reads and never changes: a job that needs to change records uses the record actions, or **Load records from a list**.

### When it fails

The action fails with one sentence: the server could not be reached, the database refused the account, the query exceeded the time limit, and so on. In a job that runs as an administrator, the database's own error code follows, in the run's log. Other people never see the database's words. The action's error handler reads `error` like any other failure.

## Load records from a list

**Load records from a list** takes a list, usually the rows a query answered, and writes each row into a model as a record. It is for jobs, run as a person.

- **Model:** where the records go. A model read from a [data source](/portal/sites/data-models/#a-model-read-from-a-data-source) cannot be written to.
- **The list:** an expression, such as `vars.units.rows`.
- **Field to expression over item (the row):** for each field of the model, the expression that gives its value from `item`, the row.
- **Match on this field:** a field to find the record a row is for. A row whose value matches one record updates it; one that matches none adds a record; one that matches several is refused. Left empty, every row adds a record.
- **All or nothing:** on by default. If any row is refused, nothing is written. Off, the rows that pass are written and the others are listed.
- **Keep the answer as:** the name the counts are kept under: `created`, `updated`, `failed` and `errors`. Each error says which row, which field and why. At most 100 errors are listed.

A load takes at most 10,000 rows. Each row goes through the same checks as any other write: the field's type, its limits, the links it points at, and the model's permissions for the person the job runs as.

## A job that loads each night

A usual job runs at night, reads a register with **Run a SQL query**, and loads the answer with **Load records from a list**, matching on the register's code. The listing on a page then shows the records, searchable, sortable and filterable, with the model's permissions deciding who sees what. See [Jobs](/portal/sites/jobs/).

Developers can also write these actions in the site's configuration: see [Developer: Data sources](/portal/developer/data-sources/#database-actions).

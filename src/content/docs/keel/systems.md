---
title: Starting cases from other systems
sidebar:
  label: Cases from other systems
---

Cases do not have to start in the business app. Another system of yours, such as a web form, a core banking system or a document scanner, can start cases and tell running cases that something happened. It signs in to Keel with a **service key** of the project.

This page is for the builder who sets that up, and for the developer of the other system.

## What the builder does

1. In Keel Builder, open **Settings** in the left rail. You need to be an owner of the project.
2. Press **New service key**, name it after the system that uses it, and press **Create**.
3. Copy the key the dialog shows: "Copy the key now. It is not shown again." Press **Done**.
4. Give the key to the system's developer, with:
   - the project's id, the part after `/p/` in the address of any Keel Builder page of the project;
   - the key of each case type the system starts, from the **Case types** page;
   - the names of the fields its cases start with, from the case type's **Data** tab;
   - the names of the [case events](/keel/builder/case-type-settings/#case-events) it may send.
5. Ask your administrator for the address of Keel's API.

Treat the key like a password. To stop a system, **Revoke** its key on the same page; see [Service keys](/keel/builder/settings/#service-keys).

## What the system can do

A service key acts as a **system** of its project. With it, the system can:

- **start cases** of any of the project's published case types, on their current version, with the case's starting data;
- **send case events** to a case, such as `documents_received`. A wait for that event moves on; otherwise the case type's event of that name fires;
- **list and read** the project's cases;
- **export** a case as one document, with its history and the definitions it ran on.

A service key cannot complete steps, vote, answer agents' questions, start optional actions or move cases: those are for staff and agents. It cannot reach another project.

In a case's history, what the system did shows as done by a system.

## For the developer

The system sends the key in the `Authorization` header as a bearer token: `Authorization: Bearer keel_…`. Every key starts with `keel_`.

| To | Call |
|---|---|
| Start a case | `POST /api/projects/{project}/cases` with `{"case_type": "loan-request", "data": {"applicant": "Ioana Popescu", "amount": "20000.00"}}` |
| Send a case event | `POST /api/cases/{case_id}/events` with `{"type": "case.event", "name": "documents_received", "payload": {}}` |
| List cases | `GET /api/projects/{project}/cases` |
| Read a case | `GET /api/cases/{case_id}` |
| Export a case | `GET /api/cases/{case_id}/export` |

Starting a case answers its `case_id`, its `number` and its stage. Send an `Idempotency-Key` header with each start: a start sent again with the same key answers with the case it started the first time, so a retry never starts a second case.

Keel checks the starting data as it checks the business app's start form: every required field must have a value, and every value must fit its field. A refused start answers with a `code` and a `message` that say why.

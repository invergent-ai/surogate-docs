---
title: Processes
---

The **Processes** page lists the instances of the project's [BPMN processes](/keel/processes/), running and ended. Its header offers **New process**. All staff see all the project's instances. The page keeps itself current.

An instance is one run of a process, such as one loan review. Its number, such as `P-000002`, counts the project's instances of every process. The page does not count them, and the [Overview](/keel/business/overview/) never counts them among the cases.

## Finding an instance

The tabs sort instances by how they stand:

| Tab | What it lists |
|---|---|
| **Running** | Instances that are running. This tab opens first. |
| **Needs a supervisor** | Instances with a task that holds an incident, or a timer that could not fire. |
| **Completed** | Instances that reached their end. |
| **Ended** | Instances a terminate end event stopped. |
| **Failed** | Instances an error ended that no boundary event caught. |
| **Cancelled** | Instances a supervisor cancelled. |
| **All** | Every instance, whatever its status. |

The filters narrow the list:

- **Search by number**: matches the instance number, such as `00012` or `P-0000`. It searches once you type two characters and pause.
- **All processes**, or one process, by name.

The address keeps the tab, the process and the search, so you can share a link to them. The **Running** tab is the default and is not written in it.

### What a row shows

| Column | What it shows |
|---|---|
| **Process** | The instance number and the version it runs on over the process's name, such as `P-000002 · v1` over `Loan review`. The whole row opens the instance. |
| **Status** | **Running**, **Completed**, **Ended**, **Failed** or **Cancelled**. An instance that needs a supervisor also shows **Needs a supervisor**. |
| **Started** | The day the instance started. |
| **Updated** | How long ago it last changed, such as `2 h ago`. A phone does not show it. |

Under the list, `Showing 25 processes` counts the rows shown, and **Show more** loads the next ones.

With no instance in a tab, the page says **No processes here**. When Keel cannot read the list, it says **The processes could not be loaded** with the reason and **Try again**. When it cannot read the processes to pick from, the filters say "The processes to start could not be loaded."

## Starting a process

1. Press **New process**. The page asks you to "Choose the process to start."
2. Pick a process. Its start form opens, with the variables the process requires.
3. Fill in the form and press **Start**. **Cancel** goes back to the instances.

The instance opens on its page. Every process the project has published whose current version can start is listed. With none, the page says **No process to start**: "Processes start once the project's builders publish one."

A link to a process that is not among those you may start says **This process cannot be started**: "It is not among the processes that may start." **Choose a process** lists them. A process that requires nothing says "This process asks for nothing to start." and shows **Start** and **Cancel** without a form.

If Keel refuses the form, the reason shows beside the field it names, or above the form when it names none. An empty required field reads **Required.** beside it, and nothing is sent. Pressing **Start** twice, or again after an error, never starts two instances from the same form.

Instances also start without you: a case's [process node](/keel/builder/flow-nodes/#processes) starts one, and another system starts one with a [service key](/keel/systems/).

## What the page does not offer

An instance is not a case. The list has no **Get next**: the Work page's [Get next](/keel/business/work/#get-next) serves the tasks of processes as well. An instance has no files, no **Follow** and no re-run. See [An open process](/keel/business/open-process/).

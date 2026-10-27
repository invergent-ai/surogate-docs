---
title: Roles and permissions
sidebar:
  label: Roles and permissions
---

Keel has two sets of roles, one for each app.

- In **Keel Builder**, a builder's role is their project role in Surogate Studio: **Viewer**, **Editor** or **Owner**. Owners change roles in Studio; see [Members and roles](/work/settings/members/).
- In the **business app**, a person is **staff**, or staff and a **supervisor**. Owners appoint supervisors in Keel Builder; supervisors add the rest of the staff.

## Keel Builder

| What | Viewer | Editor | Owner |
|---|---|---|---|
| See case types, rules, calendars, queues, scenarios, connections, versions and drafts | Yes | Yes | Yes |
| See the supervisors and the business app's address | Yes | Yes | Yes |
| See the agents of the case types, their figures, the steps they work and what they may use | Yes | Yes | Yes |
| Read an agent's sessions and raised hands, open a session, export an agent's runs for audit | No | Yes | Yes |
| Start drafts and change them; create case types, rules, calendars, queues, scenarios and connections | No | Yes | Yes |
| Ask the designer agent in a draft | No | Yes | Yes |
| Set up the project's helpers, by opening the project | No | Yes | Yes |
| Run dry runs and tests, publish drafts, move running cases | No | Yes | Yes |
| Discard a draft | No | One they created | Any |
| Set, replace and delete credentials | No | Yes | Yes |
| See effects and retry failed ones | No | Yes | Yes |
| Appoint, invite and demote supervisors | No | No | Yes |
| Create, see and revoke service keys | No | No | Yes |

Viewers see **You can view this project. Its editors and owners change it.** in place of the save state.

## The business app

| What | Staff | Supervisor |
|---|---|---|
| See the Work page, every case of the project, and its history | Yes | Yes |
| Start cases | Yes | Yes |
| Claim, work and submit steps given to them or waiting in their queues; vote in their queues | Yes | Yes |
| Answer agents' questions given to them or waiting in their queues | Yes | Yes |
| Delegate an item they hold to a person or an agent, or return it to its queue | Yes | Yes |
| Reassign any open item but a vote to a person or an agent | No | Yes |
| Start optional actions, message agents, watch agents' sessions | Yes | Yes |
| Ask the case agent about a case, and have it fill in their own form | Yes | Yes |
| Edit a case's documents while holding one of its steps; comment otherwise | Yes | Yes |
| See the Team page: invite, add and remove staff | No | Yes |
| See the Overview: figures, what needs attention, case types and where cases wait | No | Yes |
| Add and remove queue members, people and agents (Team page, **Queue settings**) | No | Yes |
| Turn agents off and on | No | Yes |
| Set and clear authority limits of staff and agents | No | Yes |
| Move a case by hand | No | Yes |
| Open the project in Keel Builder from the business app | No | Yes |

Supervisors cannot remove another supervisor from the staff; an owner demotes them in Keel Builder first. Supervisors do not define queues, serving orders or priorities: builders do.

## Agents and systems

- **Agents** act in a case like people: they complete the steps given to them, take work items as queue members or delegates, raise hands, and start cases as intake agents. Maker-checker and authority limits apply to them as to people.
- **Helpers**, the case agent and the designer agent, hold no work. The case agent reads a case as the person who asks it and fills in only that person's form; Keel records its reads as that person's views. The designer agent acts in one draft as the builder whose chat it is, and cannot publish.
- **Service keys** act as a system of their project: they start cases, send case events, and list, read and export cases. They complete no step. See [Starting cases from other systems](/keel/systems/).

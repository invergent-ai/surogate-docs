---
title: Skill canvas
---

A **procedure skill** is a skill you build as a flowchart. You lay out the steps on a canvas, and Studio compiles them into the numbered `SKILL.md` body the agent reads. Use it when the order of steps, the branches, or the checks between them matter. For a skill that is just guidance, a plain markdown skill is simpler. See [Skills & Experts](/develop/features/skills-and-experts/) for the markdown format and [Work mode → Skills](/work/library/skills/) for the library.

The skill stores the flowchart in `SKILL.graph.json` beside its `SKILL.md`. The body of `SKILL.md` is generated from the graph. You can't edit it by hand, and its **Edit** form shows an **Edit on canvas** link in place of the content box.

## Open the canvas

Only new skills can use the canvas. A skill written as markdown can't be converted to one, and saving a graph onto it is refused.

1. Go to **Skills & Tools → Skills** and click **New skill**. You need the editor role.
2. In the **Add a skill** panel, choose **Procedure canvas** instead of **Write markdown**.
3. Fill in **Name** (lowercase letters, digits and hyphens), **Display name**, **Description**, **Trigger phrases** and **Tags**. Write the description well: the router picks skills by it.
4. Click **Create and open canvas**.

Later, open the skill's detail page and click **Edit on canvas**. A canvas skill left before its first save shows **Build on canvas** instead.

The canvas needs a wide screen. On a phone it shows "The procedure canvas needs a wider screen."

## The layout

The top bar has a **Skills** back button, the skill name, and these controls:

| Control | What it does |
|---|---|
| Agent picker (**Check against agent**) | Picks the agent the checks and **Try it** use. **No agent** skips the agent-specific checks. |
| **Draft from description** | Has the platform LLM draft a graph from a description. |
| **Auto-arrange** | Lays the steps out again. |
| **Compiled** / **Hide compiled** | Shows the compiled **SKILL.md** body in a drawer under the canvas. |
| **Save** | Saves the graph. Off until you change something. |

The left column, **Add a step**, has one button per step type. The middle is the canvas: drag steps, connect them by dragging from one to the next, select a step or an edge to change it. The right column holds the inspector for the selected step, then **Checks**, **Bundle files** and **Try it**.

New canvas skills start with one **Step** joined to one **End**. A new step lands below the selected one. The start step is marked **start**. Select another step and click **Make this the start step** to move it. While other steps exist, the start step can't be deleted. Leaving the page with unsaved changes asks first.

## The eight step types

| Step | What you fill in | What the agent is told |
|---|---|---|
| **Step** | **Instruction** | Do this. |
| **Decision** | **Condition** | Choose a branch. Each outgoing edge needs a label. |
| **Tool** | **Tool**, **What to do with it** | Use this tool and wait for its result. |
| **Ask the user** | **Question**, optional **Options** (one per line) | Ask, end the turn, and wait for the answer before going on. |
| **Verify** | **Check that** | Actually perform the check. A **fail** edge says where to go if it doesn't hold. |
| **File** | **Bundle file**, optional **Note** | Read, fill in, run or use a file from the skill's bundle. |
| **Delegate** | **Kind** (`skill`, `expert` or `subagent`), **Target**, optional **Note** | Invoke that skill, consult that expert, or spawn that sub-agent, and wait for the result. |
| **End** | **What to report** | Finish. Mark every step not taken as skipped, then stop. |

Names in **Tool**, **Bundle file** and **Target** are free text. The box suggests names: built-in tools plus the chosen agent's MCP tools, the bundle's files, and the chosen agent's skills, experts or sub-agent types.

### Edges and labels

- Only a **Decision** can have several outgoing edges. Every other step has at most one, plus one `fail` edge on a **Verify**.
- The first two edges from a **Decision** are labelled `yes` and `no`. Select an edge to rename it, for example to branch on several answers. A condition written as a question works best with several labelled edges.
- A **Verify**'s second edge is labelled `fail`.
- An **End** can't have outgoing edges.

## Checks

The **Checks** panel reports problems as you edit. Click a finding to select its step. Two kinds exist.

**Problems that block saving.** These are structural and show a red **blocks saving** tag, and **Save** stays off until they are fixed. Examples: a required field left empty, more than one outgoing edge on a step that isn't a **Decision**, a `fail` edge on anything but a **Verify**, an edge out of an **End**, too many steps or edges. The server enforces the same rules and refuses a bad graph. The save-failed message points you to the Checks panel.

**Findings.** These never block saving. They are computed against the skill, its bundle and the chosen agent.

| Severity | Finding |
|---|---|
| Error | A step not reachable from the start. |
| Error | A **Decision** with fewer than two outgoing edges, or an edge with no label. |
| Error | A **Verify** with no `fail` edge. |
| Error | A **Tool** the chosen agent doesn't have. |
| Error | A **File** step whose path isn't in the bundle. |
| Error | A **Delegate** target the chosen agent doesn't have. For the `skill` kind this shows as a warning, because system skills aren't checked. |
| Error | A compiled body over the size cap. This one also refuses the save. |
| Warning | A **Step** whose text ends in a question. Use **Ask the user** so the agent waits for the answer. |
| Warning | An **Ask the user** step when the agent runs on a channel that can't show the question. The web app can. |
| Warning | No **End** reachable from a step. |
| Warning | A description under 40 characters. |
| Warning | A trigger phrase another skill in the project also uses. |

With no agent chosen, the panel says the tool, channel and delegate checks are skipped.

## Draft from description

Click **Draft from description**, describe the procedure (at least 20 characters), and click **Draft**. The platform LLM returns a graph, which is laid out and put on the canvas. If the canvas already has work, you're asked before it is replaced. Nothing is saved until you click **Save**.

It needs the platform LLM to be configured. If it isn't, the dialog says "The platform LLM is not configured."

## Bundle files

**Bundle files** manages the supporting files a **File** step points at. Pick a folder (`scripts/`, `templates/`, `references/` or `assets/`), click **Add files**, and upload. Each file in the list has **Edit** (text files only) and **Delete**. Changes apply to the skill's repository at once, not when you click **Save**.

## Try it

**Try it** runs your unsaved draft on a real agent, so you can see how it behaves before you save or publish.

1. Pick an agent in the top bar. The skill must already be attached to that agent, and the agent must be running.
2. Type a **Prompt**. The skill name is added for you. Use **Attach files** to give it input files.
3. Click **Run**. It stays off while the graph has blocking problems or a run is in progress.

This is a real session on the agent. It uses the agent's model like any chat. Nothing is published: the draft travels as an override for that one session. If the runtime doesn't allow draft overrides, the panel says the published version ran.

While it runs, steps light up on the canvas, and a list shows each step visited, its time, and any tool calls. **Stop watching** stops following the run but not the session. **Open session** opens it on the **Skill path** tab.

## How the agent follows it

The compiled body begins with a short preamble and then numbered steps, each headed with its id, such as `Step 3 (s3)`. The agent is told to call the `skill_step` tool before it starts a step (`started`), when it finishes one (`completed`), and for branches it doesn't take (`skipped`).

The graph is not enforced. The agent reads the procedure and is asked to report its progress; nothing stops it from stepping outside the flowchart. `skill_step` is offered to a session only when a procedure skill is in that session's catalog, and the canvas doesn't offer it as a tool to place in a step.

## The Skill path tab

When a session used a procedure skill, its detail view gets a **Skill path** tab beside the thread. It shows the skill's flowchart with the steps the agent took, in order, with the time on each. Beside it, a list gives each step's number, type, time and tool calls (failed calls in red), then a count of steps skipped and steps never reached.

The tab shows the first procedure skill the session used. If the agent never reported its steps, it says "The agent did not report its steps, so the path cannot be shown." A session that used no procedure skill has no tab.

## Limits

- At most 500 steps and 1000 edges per graph.
- A canvas skill's body can't be edited as text, and a markdown skill can't be converted to a canvas.
- [Skill optimization](/develop/features/skill-optimization/) isn't available for canvas skills: starting a run or applying a result is refused, because it would edit the body as text and detach it from the graph.

To move a canvas skill between projects, use **Export** and **Import skill**. See [Export a skill](/work/library/skills/#export-a-skill).

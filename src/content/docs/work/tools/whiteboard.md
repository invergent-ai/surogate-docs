---
title: Whiteboard
---

The whiteboard is a chat view where you **write and draw instead of typing**, and the agent answers *on the board* — placing its result next to your ink, or inside a box you reserved for it. It suits work that is awkward to type: maths, diagrams, sketches, a form with blanks to fill, anything where *where* the answer goes is part of the question.

It is a view of an ordinary session, not a separate product. The same agent, the same model, the same history — the board is simply what you see and how you answer.

## Turning it on

The whiteboard is a **per-agent capability**, off by default. Turn it on in the agent's **Configure → Capabilities** panel, on the card titled **Whiteboard**. When it is off the agent has no board at all, and no drawing tool.

Once it is on, a **Whiteboard** entry appears in the agent's navigation beside Chat and Inbox. That is the way in: a board is a session *created* as a board, so an ordinary chat cannot be switched into one. **New board** in the action bar starts a fresh one; otherwise the Whiteboard entry picks up your most recent board where you left it.

## Switching between the board and the transcript

Inside a board session there is a view switcher at the bottom — **Simple**, **Advanced**, **Whiteboard**. It appears once the agent has answered at least once: before that there is no transcript to switch to.

Switching views never loses work. Your drawing is saved with the session, so you can flip to Simple to read a long answer as prose and come back to the board with every stroke intact.

Board sessions skip the per-turn summary card that ordinary chats show. The board *is* the answer.

## The tool rail

The rail on the left of the canvas holds the tools:

| Tool | What it does |
| --- | --- |
| **Pen** | Draw. |
| **Eraser** | Rub out anything under it, the agent's work included. The ring under the cursor shows the bite radius — four times the selected width. Undoable like any other stroke. |
| **Text** | Click to open a text box and type. **Ctrl/Cmd+Enter** or a click away commits it; **Esc** discards it. Typed text is handed to the agent as text, so unlike handwriting it can never be misread — worth using for anything fiddly. |
| **Answer box** | Reserve a space for the agent's answer. See [Telling the agent where to write](#telling-the-agent-where-to-write). |
| **Select** | Click an object to select it, drag to move it, drag a corner handle to resize it. Drag on empty canvas to lasso several objects. |
| **Pan** | Drag to move around the board. |

Below the tools sit five ink colours and four stroke widths, then **Fit to content**, **Undo** and **Redo**. Undo works a gesture at a time, not a pointer sample at a time — a whole drag comes back in one step.

Moving around the board:

- **Zoom** with the mouse wheel.
- **Pan** with the **middle mouse button** at any time, whatever tool you are holding — no need to switch to the Pan tool and back.

Keyboard: **Ctrl/Cmd+Z** undoes, **Ctrl/Cmd+Shift+Z** redoes, and **Delete** or **Backspace** removes the selection.

The faint blue numbered grid under your ink is not part of the drawing — it is the same grid the agent is told about, so you can see the board the way it does.

## Asking

The bar under the canvas is how you hand the board to the agent. There is an optional question box — *Ask about the board* — and then four buttons that both **send the turn and say what you want**:

| Button | What you are asking for |
| --- | --- |
| **Answer** | Solve or complete what is on the board and write the result: into the answer box if you placed one, otherwise next to your ink. |
| **Continue** | Pick up where your drawing or text stops and extend it in the same style. |
| **Explain** | Explain what is on the board in words, without changing it. |
| **Hint** | Give a clue toward the answer — never the answer itself. |

**Answer** is the common case and is what **Enter** sends from the question box.

Saying which of these you want matters more than it looks. Left to infer from the picture alone, an agent has to guess three things at once — where the result goes, what to do, and whether to *do* it or talk about it — and spatial convention only carries that reliably in maths. A trailing `=` is unambiguous; a heading with a gap under it, or a half-drawn figure, is not. The buttons remove the guess.

### "Work it out"

The checkbox beside the buttons decides **how much work the agent may do before it draws**.

- **Off** (default): the agent has one tool — the board — and answers your ink in a single pass. This is what keeps the interaction close to the latency of writing on paper.
- **On**: the agent gets its whole toolkit — web search, the terminal, artifacts — over several passes, then draws. Slower, and worth it for anything the board alone cannot settle.

It does not change the model and does not make the agent reason harder; it changes what it is allowed to *do* first.

While a turn runs, a pill under the canvas reports progress — *Thinking…*, or *Working it out…* with the agent's own step-by-step notes — and **the canvas is locked**. Strokes drawn mid-turn would be thrown away when the answer lands, so the board declines them rather than eating them.

## Telling the agent where to write

An **answer box** is an empty rectangle you reserve for the result. It is the one gesture that means the same thing in every subject: the missing letter, the value after the `=`, the paragraph under a heading, the cat in the empty frame.

Two ways to place one:

- Pick the **Answer box** tool, then **click** to drop a default-sized box, or **drag** to size one yourself. A text box opens underneath it so you can add a **hint** — a line saying what belongs there. Leave it blank if the space speaks for itself.
- **Right-click** anywhere on the canvas, whatever tool you are holding. This drops a box straight away, with no hint prompt — the fast path.

A click-placed box takes its left edge at the click point and centres vertically on it — so clicking just after an `=` puts the box exactly where the answer reads. Each box carries the Surogate rabbit so it reads as *the agent's space*, and they are labelled `S1`, `S2`, … so the agent can refer to them.

The agent fits its answer into the box — text shrinks to fit, a sketch scales in — and **the box disappears**, replaced by the answer. A turn that would leave a box empty is rejected before it reaches your board, so the agent cannot answer beside the space you set aside.

## What the labels on the board mean

When you send a turn, the board hands the agent a picture of itself with labels drawn on it, and the same labels come back in the agent's instructions. You see them too:

- **`A1`, `A2`, …** — clusters of **your** ink. Strokes that sit together are one mark, so `A1` is a whole expression rather than a single pen stroke.
- **`B1`, `B2`, …** — things the **agent** drew.
- **`S1`, `S2`, …** — answer boxes you placed.

They exist so the agent can say *"to the right of A1"* or *"replace B1"* instead of computing pixel coordinates — which is what it is bad at, and where wrong placement came from. Because the labels resolve against the board as it stands when the answer is folded in, moving something mid-turn does not corrupt the placement: "after the equals sign" follows the equals sign.

### Readings, and correcting them

Under a cluster of your ink you may see a small italic line — the agent's **reading** of it, its transcription of your handwriting (`∫(1/x)dx =`). It is stored against exactly the strokes it covers and handed back on every later turn, so the agent reads your handwriting once rather than re-guessing it every time. Add a stroke to the cluster and it counts as new writing, to be read again.

The colour tells you where it came from: **grey** is the agent's reading, **green** is one you corrected.

If a reading is wrong, fix it: pick the **Select** tool and click the reading text itself — a box opens with the current reading in it. **Your correction outranks anything the agent reads later**, so it will not silently revert. Submitting an empty box clears the reading instead, and the ink is treated as unread.

Correcting a reading is usually the fastest fix when an answer is wrong for a strange reason: an agent that read `∫` as `S` was answering the question it saw.

## Practical notes

- **Handwriting is read once and reused.** If the agent misreads something, correcting the reading is more reliable than redrawing it.
- **If placement matters, place a box.** It is the difference between asking and instructing.
- **A long or awkward prompt can just be typed** in the question box; the board and the question go together in the same turn.
- **Everything is saved with the session** and reloads with it, including the labels and the readings.
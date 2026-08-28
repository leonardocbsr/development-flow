---
name: visual-companion
description: Use when the user asks to show, visualize, diagram, mock up, compare layouts, or inspect a software design, architecture, interface, flow, or state transition visually.
---

# Visual Companion

Use a visual only when it improves the decision. A visual companion is a tool inside the development flow, not a separate ceremony.

For commands targeting another operating system, never translate the current machine's plugin path into an invented path on that host. Preserve `THIS_SKILL_DIRECTORY` as an explicit placeholder unless the real installed skill directory is known. Preserve the user-provided project path exactly and quote paths with spaces.

## Decision test

Use it for:

- UI layouts, hierarchy, navigation, and interaction alternatives;
- architecture, data flow, ownership, sequence, or state diagrams;
- before/after system comparisons;
- spatial relationships that prose makes hard to hold in mind.

Stay in text for requirements, scope, trade-off lists, API semantics, implementation details, and questions whose answer is primarily words. A UI topic is not automatically a visual question.

## Invitation gate

Before creating anything visual, classify the request:

1. The user explicitly asked to see, visualize, diagram, mock up, or compare visually: create the visual directly without asking.
2. Anything else—including a request to decide or choose between alternatives—is not yet a request to see. Send only this invitation and end the turn:

> This decision is easier to compare visually. Want me to open a visual companion with 2–3 options?

Do not build mockups, artifacts, or diagrams in the same turn as the invitation. Keep the invitation short and on its own. Do not mention novelty, token cost, internal tooling, or setup details. Acceptance authorizes the current decision or explicitly requested continuing visual session. Ask again before opening a new session for a materially different decision unless the user requested ongoing visual use.

## Create the visual

Prefer the platform's native visualization capability when it provides the required interaction. Otherwise resolve paths relative to this `SKILL.md` and start the packaged local scaffold in a long-running terminal session. Replace the quoted path placeholders before running the command.

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/server.py" --project-dir "PROJECT_ROOT" --open
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\server.py" --project-dir "PROJECT_ROOT" --open
```

The first JSON line contains the complete keyed `url`, `screen_dir`, `state_dir`, and `session_dir`. Keep the process alive. Never share a URL without its key. Write each screen as a new semantic `.html` fragment in `screen_dir`; the browser relays the newest fragment. User choices are appended to `state_dir/events.jsonl`.

If neither a native surface nor the local scaffold can run, say so briefly and provide the smallest useful text fallback; do not invent a working browser surface.

- Frame the exact decision at the top.
- Show 2–4 meaningful alternatives, or one focused explanatory diagram.
- Scale fidelity to the question: wireframe for structure, polished mockup for visual direction.
- Use realistic content when it affects the decision.
- Make interactions and selected state obvious.
- Preserve a concise text summary so the decision survives without the visual surface.
- For durable artifacts, keep source files in the requested project location and verify desktop and narrow-mobile rendering.

Fragments may use `.options`, `.cards`, `.split`, `.panel`, and `.mockup`. Add `data-choice="value"` to selectable elements and `data-multiselect` to a parent when multiple choices are valid. Do not include secrets or private records in browser content.

## Continue

Treat the user's written response as authoritative; clicks or visual selections add evidence. Iterate the current decision before advancing. When the next question is textual, return to the conversation without keeping the user trapped in the visual surface.

Stop only the explicit session when finished:

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/stop-server.py" "SESSION_DIRECTORY"
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\stop-server.py" "SESSION_DIRECTORY"
```

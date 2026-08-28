---
name: executive-review
description: Use when substantial engineering work is done or genuinely blocked and the agent is about to end the turn with a final executive handoff, executive summary, or completion report.
---

# Executive Review

Produce the decision-ready terminal handoff from current evidence. Do not narrate the work session.

## Terminal gate

Use this skill only when the agent would otherwise send its final response:

- all authorized implementation, fixes, relevant review, and verification are complete; or
- a genuine blocker prevents further meaningful progress and requires new authority or external state.

Do not create an Executive Review after a few tasks, commits, tests, or milestones while safe in-scope work remains. Do not use it as an interim progress update. Continue working first.

## Establish the snapshot

Inspect the live sources that support the review: repository and worktree identity, base and head, status and diff, design and plan, relevant commits, verification output, review findings, runtime or deployment evidence, and dated artifacts. State the snapshot boundary and date.

Use `development-flow:verifying-claims` before presenting any result as complete, fixed, passing, deployed, or production-ready.

## Output contract

Lead with the outcome and current gate. Include only relevant sections:

1. **Executive summary** — what changed, why it matters, and the current truth in a few sentences.
2. **Delivered** — completed outcomes, not a file-by-file activity log.
3. **In progress** — partially implemented or dirty state, clearly separated from delivered work.
4. **Evidence** — commands, test counts, builds, live checks, commits, artifacts, and what each one actually proves.
5. **Decisions** — consequential choices, trade-offs, and deliberate omissions.
6. **Blockers** — only conditions that prevent meaningful progress without new authority or external state.
7. **Risks and unknowns** — possible failure modes and unverified claims; do not relabel them as blockers.
8. **Next steps** — ordered actions with an owner or decision needed; identify one immediate next action.

Use explicit status language: confirmed, inferred, hypothesis, or unknown. Distinguish committed work from dirty changes and local proof from deployed behavior.

## Format and scaffold

Resolve paths relative to this `SKILL.md` and create the editable responsive artifact with the packaged scaffold. Replace the quoted placeholders before running the command.

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/new_review.py" --slug "SHORT_TOPIC" --title "OWNER_FACING_TITLE"
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\new_review.py" --slug "SHORT_TOPIC" --title "OWNER_FACING_TITLE"
```

The command prints the artifact directory. Edit only `review-data.js` unless the work requires a deliberate visual change. Populate every relevant field from fresh evidence. List entries and evidence entries may include a safe `href` pointing to an HTTP, HTTPS, file, absolute, or relative artifact. Open `index.html`, verify desktop and narrow-mobile rendering, and exercise any links or interactions. Then provide the clickable artifact path with a concise text outcome in the final response.

Create HTML only when at least one is true: the user asked for an artifact; the work spans three or more evidence/decision/risk sections that benefit from scanning; or architecture, timeline, or state relationships are materially clearer visually. Otherwise use concise text. A table is justified only when it improves comparison.

Write for the owner or decision-maker. Remove local tooling chatter, raw logs, credentials, private records, and internal process details that do not affect the decision. Link to relevant local files, commits, and artifacts when available.

## Do not overclaim

- A green unit test proves that tested contract, not system integration.
- A build proves compilation, not runtime behavior.
- A mock proves behavior under the mock's assumptions, not the live dependency.
- A commit proves recorded changes, not correctness or deployment.
- A reviewer report is an input, not verification.
- “No blocker found” is not “production-ready.”

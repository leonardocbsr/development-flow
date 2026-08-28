---
name: using-development-flow
description: Use when the user asks to build, implement, fix, debug, prototype, research, refactor, review, deploy, or ship software and the work must be routed by lifecycle commitment.
---

# Using Development Flow

Match process to commitment. Do not treat every code-related request as Production work.

A user request to build, implement, fix, or ship already authorizes ordinary bounded implementation after the scaled design. Never ask `Ready to implement?` or `Proceed?` unless a material unresolved choice, destructive action, external effect, or scope expansion needs new authority.

## Required routing before action

Load the applicable skill before inspecting, answering, or editing that surface:

| Request surface | Load |
| --- | --- |
| approved milestone or plan execution, writer handoff | `development-flow:implementing-plans` |
| add, change, mock, or review a test or assertion | `development-flow:testing-stable-contracts` |
| unresolved failure, regression, crash, hang, or wrong behavior | `development-flow:debugging-systematically` |
| request or incoming review feedback | `development-flow:adversarial-reviewing` |
| owner explanation, status, blocker, or handoff | `development-flow:speaking-plainly` |
| completion or readiness claim | `development-flow:verifying-claims` |
| retained notable change or release | `development-flow:keeping-a-changelog` |
| replace or remove Superpowers | `development-flow:migrating-from-superpowers` |
| visual decision or Visual Companion | `development-flow:visual-companion` |
| terminal substantial handoff | `development-flow:executive-review` |

Do not edit first and route afterward. Multiple rows may apply.

## Start

Treat the session's current working directory as the target repository unless the user explicitly names another. A skill directory, plugin source, cache, or marketplace checkout supplies instructions; it is not the target repository.

1. Read `development-flow:choosing-development-lane` and select Research Spike, PoC, MVP, or Production from the intended commitment. An explicit lane from the user wins.
2. State the lane once with one sentence of reasoning. Do not ask the user to classify routine work you can infer.
3. Use `development-flow:speaking-plainly` for owner-facing plans, explanations, updates, findings, blockers, and handoffs throughout the work.
4. Use `development-flow:researching-design` before implementation. Every lane gets a design plan scaled to its commitment.
5. When the design is approved—or the user's request already authorizes the bounded implementation—use `development-flow:planning-development` as needed, then `development-flow:implementing-plans` without asking again.
6. Use `development-flow:debugging-systematically` when a failure's cause is unresolved, `development-flow:testing-stable-contracts` for durable behavior, `development-flow:adversarial-reviewing` for review, and `development-flow:verifying-claims` before status claims.
7. Use `development-flow:visual-companion` only for decisions that are materially clearer when seen. Use `development-flow:executive-review` only at a substantial terminal handoff.
8. After retained changes, use `development-flow:keeping-a-changelog` automatically when the project has `CHANGELOG.md`; if notable work lacks one, ask once—in the final handoff at the latest—whether to create it.

## Authority boundaries

- An approved design plus `execute`, `implement`, `continue`, or equivalent authorizes implementation. Do not reopen settled design without new contradictory evidence.
- A request such as `build`, `implement`, `fix`, or `ship` authorizes ordinary in-scope implementation after the scaled design. Do not turn the design step into a second approval gate unless a material choice, destructive action, external effect, or scope expansion still needs authority.
- Read-only inspection, diagnosis, explanation, and review do not authorize writes.
- Research Spike probes may proceed after presenting and persisting their compact design plan; do not request approval for every iteration within its stated cost and scope.
- Stop for destructive, security-sensitive, externally visible, or materially scope-expanding actions that lack authority.

## Delegation and writing

Default to one writer for an entire milestone. Use `development-flow:implementing-plans` for the exceptional context-pressure evidence, sequential implementation-writer ownership, separate test-writer boundary, and compact verified handoff contract. Explorers and reviewers remain read-only. Never use multiple writers merely because parallel work appears faster.

## Avoid

- Choosing Production because the work is technically difficult.
- Turning design research into implementation silently.
- Repeating approval gates after the user has approved the design and requested execution.
- Editing in response to reviewer feedback before `development-flow:adversarial-reviewing` independently classifies the finding as accepted.
- Treating a test suite, build, or reviewer report as proof of a claim it did not exercise.

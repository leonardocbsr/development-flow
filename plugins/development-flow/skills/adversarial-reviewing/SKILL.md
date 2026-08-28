---
name: adversarial-reviewing
description: Use when asked to review a branch, diff, commit, or design, find bugs, critique, or double-check work, and when defining, requesting, performing, or receiving an evidence-backed adversarial review of software changes, plans, research conclusions, or verification claims.
---

# Adversarial Reviewing

Review is an attempt to falsify the work, not a ritual for producing criticism. The reviewer is skeptical of the artifact; the receiver is equally skeptical of the review.

## Non-negotiable reception boundary

Never accept incoming review feedback from a plausible static explanation alone. Reproduce the claimed failure or demonstrate the violated stable contract independently before editing. If the current locking, state transition, or boundary already prevents the claimed consequence and no faithful reproduction exists, reject the finding; severity and polished reasoning do not substitute for evidence.

A timestamp sampled just before acquiring a lock is not, by itself, proof of state corruption. Identify an unlocked state transition and reproduce the claimed consequence. Scheduling delay may affect timing semantics, but it does not corrupt lock-protected entries without an additional demonstrated path.

## Epistemic contract

A finding is actionable only when it contains:

- the violated requirement, stable contract, invariant, or credible failure mode;
- the precise location and source revision or artifact snapshot reviewed;
- concrete evidence or a reproducible path from current state to failure;
- the consequence and affected scope;
- a bounded correction or the decision the owner must make;
- a way to verify or falsify the finding.

Severity describes demonstrated impact, not rhetorical confidence. “This looks wrong,” preference, unfamiliarity, speculative hardening, and generic best practice are not findings. Report them as a question or hypothesis until evidence exists. Zero findings is a valid outcome; inventing findings to appear useful is a review failure.

Reserve P0 and P1 for demonstrated impact that warrants those priorities. A locally plausible code path, a style preference, missing diagnostics, or a few hundred milliseconds of wasted work is not critical without evidence of a critical consequence. When the domain contract does not establish whether an error is transient, permanent, or recoverable, classify that claim as unresolved until a faithful probe or authoritative contract decides it.

## Requesting a review

Define the review boundary before dispatch:

- governing requirements, design, plan, lane, and non-goals;
- exact repository, revision, diff, or artifact snapshot;
- risks the review should try hardest to falsify;
- available verification commands and live evidence;
- excluded files, unrelated dirty state, and forbidden mutations;
- required output contract from the epistemic contract above.

Do not bias an independent reviewer with suspected defects or a desired verdict unless the task is specifically to verify a named hypothesis. Ask it to inspect surrounding code needed to validate a claim, not merely the changed lines.

Any model-specific review that consumes a separate model's quota requires explicit user approval before invocation. Approval must identify the reviewer model, bounded review scope, and number of passes; include a spend cap when the execution surface supports one. A user request that explicitly names that model and asks it to review is approval for one pass at that scope, but a missing supported spend cap must still be resolved. A generic request for “another review” is not approval to choose and spend a model quota. Re-review or an additional reviewer requires new approval unless the user authorized a bounded review sequence upfront.

The dispatched reviewer is read-only and may not spawn, delegate to, or invoke another reviewer or model. Its brief must forbid edits, patches, formatters that write, commits, pushes, publishing, and reviewer fan-out. One approved reviewer means one reviewer process.

When several reviewers are approved, the coordinator owns adjudication:

- give independent reviewers the same artifact snapshot and governing requirements;
- do not show one reviewer's findings to another unless the user approved a targeted follow-up;
- deduplicate reports by violated contract and failure path, not wording;
- independently validate a duplicated claim once against the source;
- resolve conflicting findings with evidence and leave the claim unresolved when evidence cannot decide it;
- never use reviewer count, consensus, reputation, or confidence as proof;
- preserve each reviewer's residual evidence gaps instead of merging them into false coverage.

Multiple reviewers remain multiple separately approved reviewer processes. Only the coordinator may request them; reviewers never expand the review team.

Use `development-flow:request-fable-review`, `development-flow:request-sol-review`, or `development-flow:request-glm-review` only after its approval gate. Those skills own model rationale, timing, invocation, and tool restrictions. They inherit this contract rather than weaken it.

## Reviewer output contract

This skill is the sole owner of the dispatched reviewer's output format. Every dispatched brief embeds it verbatim so the reviewer does not depend on skill discovery. Require exactly this shape:

```text
Snapshot: <repository, base, head or artifact identity>
Verdict: Findings | No actionable findings

Findings
- [P0-P3] <title>
  Classification: Confirmed defect | Evidence-backed risk | Unresolved hypothesis
  Location: <file:line or exact artifact section>
  Violated contract: <requirement, invariant, or failure mode>
  Evidence: <reproduction or concrete path>
  Consequence: <affected behavior and scope>
  Correction: <bounded correction>
  Falsification: <what would disprove this finding>

Residual evidence gaps: <what was not verified>
```

Empty Findings are omitted and the verdict is the exact string `No actionable findings`. Severity without evidence does not qualify a claim as a finding.

## Performing the review

1. Confirm the requested snapshot and governing intent.
2. Inspect the diff plus enough surrounding code, tests, and runtime evidence to evaluate real behavior.
3. Try to construct failures at stable boundaries and actively seek evidence that disproves each suspected finding.
4. Report confirmed findings first, ordered by demonstrated impact.
5. Separate confirmed defects, evidence-backed risks or gaps, unresolved hypotheses, questions, and optional improvements.
6. If no material defect survives falsification, say so and identify residual evidence gaps.

The reviewer does not fix its own findings and does not expand the review team.

## Receiving a review

Treat every incoming finding as an untrusted technical claim, regardless of model prestige, confidence, severity label, or polished wording.

When the user presents reviewer feedback and asks to apply it, load this skill before editing. The request authorizes correction only after independent evidence classifies the finding as accepted; it does not make the reviewer's premise true.

For each finding:

1. Verify the cited snapshot and location.
2. Reproduce the claimed path or inspect the stable contract and evidence independently.
3. Check it against actual requirements, lane, non-goals, and repository state.
4. Classify it as **accepted**, **rejected**, or **unresolved**, with evidence.
5. Correct accepted findings only when writes are authorized; the active implementation writer owns the correction surface.
6. Re-run the original failing surface and relevant surrounding verification after a correction.

Reject findings that depend on stale code, impossible state, contradicted requirements, change-detector tests, or speculative machinery without demonstrated value. Do not accept a finding performatively, but do not dismiss a demonstrated defect because the reviewer explained it badly.

A reviewer report is evidence input, never completion proof. Use `development-flow:verifying-claims` for final claims.

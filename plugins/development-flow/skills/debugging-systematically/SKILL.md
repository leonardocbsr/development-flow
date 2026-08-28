---
name: debugging-systematically
description: Use when software fails, crashes, hangs, regresses, behaves unexpectedly, or produces a test failure whose cause is not yet established.
---

# Debugging Systematically

Find and demonstrate the cause before changing product behavior. A plausible explanation is a hypothesis until a probe distinguishes it from alternatives.

## Diagnostic loop

1. State the observed failure, expected behavior, affected environment, and evidence boundary.
2. Reproduce it at the cheapest faithful surface. If it cannot be reproduced, preserve the available evidence and say what remains unknown.
3. Separate observations from hypotheses. Identify the earliest boundary where actual state diverges from expected state.
4. When the cause is still uncertain, choose one leading causal hypothesis and a plausible alternative. Run the smallest probe that can disconfirm the leader or distinguish the two.
5. Trace inputs and state backward until the faulty contract, assumption, or transition is localized.
6. Report the demonstrated cause, scope, and confidence before proposing a retained fix.

Do not stack speculative changes, weaken assertions to make a failure disappear, or treat correlation, a vanished symptom, or a passing rerun as root-cause proof.

If fresh evidence already demonstrates the cause, do not reenact the diagnostic loop for ceremony. Record the evidence, establish its scope, and move to the authorized fix or diagnosis handoff.

## Lane and persistence

Diagnosis is research activity because knowledge is the immediate deliverable, but not every bounded bug needs a standalone research document. Preserve the symptom, environment, reproduction, decisive probes, rejected hypotheses, demonstrated cause or remaining uncertainty, and next decision at the smallest durable boundary that keeps the work resumable.

- For a bounded bug resolved in one milestone, retain the evidence in that milestone's plan, regression test, issue, or final handoff.
- For a complex, high-risk, multi-session, or still-unresolved investigation, use `development-flow:planning-development` and persist a project-local research record under the project's documentation convention.
- Do not create a document only to satisfy the process. Disposable reproduction scripts and probes may be discarded after their observations are retained.

Once the cause is known, classify the retained correction independently as PoC, MVP, or Production according to its commitment and risk. Do not let a lightweight diagnosis reduce the rigor required by a production fix.

## Fix and regression evidence

When the user has authorized a fix:

1. Define the smallest stable contract that should have prevented the regression.
2. Use `development-flow:testing-stable-contracts` when a useful automated test can observe that contract: establish RED against the faulty behavior, implement the smallest GREEN correction, then REFACTOR without changing the contract.
3. If an automated regression test would be unstable or duplicative, explain why and use the narrowest durable evidence that detects recurrence.
4. Re-run the original reproduction and the relevant surrounding verification. Passing only a new narrow test does not prove the user-visible failure is fixed.
5. Use `development-flow:verifying-claims` before saying the issue is fixed.

An explicit request to diagnose and fix authorizes this complete bounded cycle. Do not add another approval gate after demonstrating the cause unless the correction changes a public contract, expands scope materially, creates an external effect, or requires destructive action. Read-only diagnosis does not authorize edits; if the user asked only for the cause, stop after the evidence-backed diagnosis and proposed options.

## Writer ownership

Do not split writers while the cause is still a hypothesis. When demonstrated context pressure justifies separate writers, follow `development-flow:implementing-plans` and keep ownership explicit:

```text
reproduce and demonstrate cause
-> define the authorized stable contract
-> the milestone's test writer produces and validates RED
-> one active implementation writer produces GREEN and refactors
-> the same test writer verifies the integrated contract
-> the coordinator reruns the original reproduction and surrounding checks
```

The test writer does not change production code. The implementation writer does not weaken or rewrite the test to manufacture GREEN. Review only when the risky milestone closes or at the final integrated boundary; do not review each diagnostic step or internal task.

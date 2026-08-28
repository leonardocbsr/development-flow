---
name: implementing-plans
description: Use when the user says execute, implement, continue, or resume after approving a software design or implementation plan.
---

# Implementing Plans

Execute milestone by milestone. One implementation writer owns the active production-code surface at a time.

## Execute

1. Confirm the repository and current state; preserve unrelated changes.
2. Read the approved milestone plan from its recorded path. Expect every Research Spike record and every MVP or Production milestone plan to be durable under `docs/plans/` unless the project defines another convention. A separate design document is optional, not a prerequisite. Resume completed work from repository and verification evidence rather than restarting.
3. Implement milestones in dependency order, keeping each change within the approved contracts and ownership boundary. Use disposable internal tasks only when they help execution; do not promote them into permanent plan prose.
4. For durable behavior, use `development-flow:testing-stable-contracts` at the narrowest level that detects the risk.
5. Verify each meaningful increment before relying on it.
6. Run focused verification after relevant changes. Use `development-flow:adversarial-reviewing` when a risky milestone closes and for the final integrated review; do not create a review ceremony for every task.
7. Use `development-flow:verifying-claims` before reporting status or completion.

## Writer ownership

The default is one agent implementing the whole milestone. Split writing only after demonstrating that the milestone cannot safely fit the available context. Useful evidence includes too many independent interfaces to keep loaded, necessary investigation plus implementation plus tests exhausting context, a stable-boundary handoff preserving more information than continuing, or the writer already having to discard evidence needed for correctness. More tasks or possible speedup is not enough.

When the current writer reports that it is already dropping necessary evidence and the owner asks for a handoff, the context-pressure exception is demonstrated. The coordinator must stop that writer at a verified boundary and use the sequential handoff contract below; continuing as the same writer defeats the purpose of the exception.

When a split is justified:

- several implementation writers may serve sequentially, but only one is active at a time;
- exactly one test writer owns the test surface for the milestone;
- implementation writers and the test writer never work simultaneously on the same contract;
- writers may not create other writers or reviewers;
- a writer handoff occurs only at an explicit stable boundary with verified state and transferred ownership;
- the handoff contains only the milestone, contract, current state, evidence, ownership, and next risks;
- the test writer changes tests and test support, never production code;
- the implementation writer changes production code and does not weaken or rewrite tests to manufacture GREEN;
- if production code and tests share one file, one writer owns that entire surface.

For one contract, use this sequence when separate writers are justified:

```text
approved contract
-> test writer produces and validates RED
-> implementation writer produces GREEN and refactors
-> test writer verifies the integrated contract
-> milestone verification
```

Different contracts may form a pipeline only when ownership is unambiguous. Never run two implementation writers concurrently, even in different files.

Explorers and reviewers remain read-only. Every such delegated brief must forbid edits, patches, writing formatters, commits, pushes, publishing, and further delegation. The coordinator independently verifies their evidence. A reviewer never fixes its own findings.

## Reviews

- Verify focused surfaces after relevant changes.
- Do not request a review automatically for each task.
- Use adversarial review when a risky milestone closes.
- Review the integrated result before the terminal handoff when risk warrants it.
- Use multiple reviewers only when independent perspectives add concrete value.
- Keep every paid reviewer behind its individual model, scope, pass-count, and cost approval.

## Lane behavior

- Research Spike: write only experimental artifacts needed for evidence; retain the research record even when probes are discarded, or explicitly promote retained implementation through a new lane design.
- PoC: implement the narrow vertical slice and leave deliberate omissions visible.
- MVP: complete critical user journeys without speculative production machinery.
- Production: honor operational, security, migration, observability, rollout, and rollback gates from the design.

## Stop only when necessary

Stop for missing authority over destructive, security-sensitive, externally visible, or materially scope-expanding actions; or when contradictory requirements make every implementation choice speculative. Otherwise make reversible, evidence-backed decisions and continue.

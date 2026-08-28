---
name: planning-development
description: Use when the user asks for a design, spec, plan, implementation plan, roadmap, or multi-step software change in a Research Spike, PoC, MVP, or Production lane.
---

# Planning Development

Every lane gets a design plan. Detail grows with commitment; ceremonial volume does not equal rigor.

## Required design plan

Every plan names the lane, goal, evidence, boundaries, non-goals, risks, and stopping condition.

| Lane | Plan contract |
| --- | --- |
| Research Spike | Hypothesis, smallest probe, inputs, controls, measurements, kill criteria, artifact disposition |
| PoC | Technical claim, vertical slice, real versus simulated components, proof, deliberate omissions, promotion or disposal decision |
| MVP | User and critical journeys, scope, stable contracts, persistence and failure behavior, useful tests, acceptance evidence |
| Production | Architecture, dependencies, data safety, security, observability, migrations, rollout, rollback, useful tests, operational acceptance |

This skill is the sole owner of the design-plan contract. Research findings from `development-flow:researching-design` are inputs, not another plan format.

## Persistence

- Research Spike: always save the compact plan and evolving research record. Experimental code may be disposable; the knowledge is not.
- PoC: save when executable artifacts will be retained or the work spans sessions.
- MVP and Production: always save one approved milestone plan containing the design decisions and execution boundaries.

Use:

```text
docs/plans/YYYY-MM-DD-<topic>-plan.md
docs/plans/YYYY-MM-DD-<topic>-research.md
```

Use `-plan.md` as the default durable artifact for retained work. It contains the scaled design, interfaces, contracts, milestones, and acceptance evidence. Do not create a separate `-design.md` unless the project already requires separate specifications or the design must be reviewed independently from execution. Use `-research.md` only when meaningful research evidence must remain distinct from the delivery plan.

Use the `-research.md` record for a Research Spike's question, hypothesis, plan, sources or inputs, probes, observations, rejected alternatives, uncertainty, result, and decision. If the research promotes work into another lane, keep the research record and create that lane's milestone plan separately.

If the project already has an explicit documentation convention, follow it instead and record the exact paths in the handoff. Persistent plans are resumable state, not ceremony.

## Milestone plan

When code will be retained, turn the approved design into ordered milestones. Durable plans record only information that constrains later decisions. Each milestone states:

- observable outcome;
- affected interfaces;
- stable contracts;
- invariants and credible failure modes;
- dependencies between components or earlier milestones;
- material risks;
- evidence required for acceptance;
- files or ownership areas only when they prevent conflict;
- stop, handoff, or promotion condition.

Do not turn the plan into a literary sequence of microtasks. Exclude pseudocode that pre-decides implementation, line-by-line instructions, one task per file or function, tests without a plausible regression, mechanical RED/GREEN steps for every detail, estimates without decision value, and ceremony. The agent may keep disposable internal tasks while executing; they are not permanent project documentation.

A plan constrains outcomes, boundaries, contracts, and evidence while preserving implementation judgment. Milestones are resumable boundaries, not task containers.

## Approval and execution

- Research Spike: the user's research request plus the stated probe plan authorizes iterative probes within scope.
- A design-only request does not authorize implementation. Obtain implementation approval after presenting a new PoC, MVP, or Production design when the user asked only for design or planning.
- A request to `build`, `implement`, `fix`, or equivalent already authorizes ordinary bounded implementation after the scaled design. Continue without a second approval gate unless a material unresolved choice, destructive action, external effect, or scope expansion needs new authority.
- If the user already approved the design or plan and says `execute`, `implement`, or `continue`, treat it as an execution contract and proceed without another design loop.

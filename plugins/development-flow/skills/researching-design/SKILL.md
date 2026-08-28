---
name: researching-design
description: Use when the user asks to research, investigate, compare approaches, find the state of the art, explore trade-offs, design a system, or decide what should be built before implementation.
---

# Researching Design

Research answers what should be built and why. It does not silently become product implementation.

## Non-negotiable evidence boundary

An estimate is not a measurement. A plausible mechanism is not a finding. Never invent benchmark numbers, hardware limits, source conclusions, or confidence to fill an evidence gap. If a source, runtime, or probe is unavailable, label the result unknown and name the smallest next check. A Research Spike always preserves its plan and observations in the project-local `docs/plans/YYYY-MM-DD-<topic>-research.md` record.

## Research

1. Establish the lane and decision to be made.
2. Inspect the live repository, runtime, logs, and existing artifacts before relying on assumptions.
3. For unstable, niche, or externally sourced facts, research primary sources and separate confirmed facts, claims, inference, and unknowns.
4. Identify the state of the art, credible alternatives, constraints, and trade-offs.
5. Recommend one approach and explain what evidence would change the recommendation.

## Research record

Capture the evidence that the design plan will consume:

- objective and lane;
- current evidence and assumptions;
- alternatives considered and trade-offs;
- proposed boundaries and stable contracts;
- risks, non-goals, and unknowns;
- evidence or acceptance strategy;
- implementation boundary: what this phase will not build.

`development-flow:planning-development` is the sole owner of the design-plan schema, persistence rule, and execution-plan format. Do not create a competing plan format here.

For every Research Spike, create or update the project-local `docs/plans/YYYY-MM-DD-<topic>-research.md` record defined by that skill. Preserve cited sources or input identity, probes, observations, rejected alternatives, uncertainty, result, and the decision the research supports. The record is durable even when experimental code is discarded.

## Research Spike execution

After stating and recording the compact plan, run the smallest useful probe within the requested scope. Iterate hypothesis, probe, observation, and updated belief in the record. Keep experimental artifacts clearly labeled. Stop when the decision is answerable, kill criteria fire, or additional work would change scope or cost materially.

Do not call research complete, comprehensive, feasible, or state of the art unless the recorded evidence supports that exact scope.

## Handoff

- Knowledge-only outcome: report evidence, uncertainty, and recommendation.
- Implementation outcome: use `development-flow:planning-development` to produce the lane's design plan. Continue directly when the original request already authorized that bounded implementation; ask only when a material unresolved choice or authority boundary remains.

Do not write product implementation while the decision or stable contract is unresolved.

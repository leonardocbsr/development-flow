---
name: choosing-development-lane
description: Use when a request mentions a spike, experiment, prototype, proof of concept, PoC, MVP, production, launch, deploy, or ship, or when software work may be changing commitment.
---

# Choosing the Development Lane

Choose by what the result must become, not by complexity, file count, or technical difficulty.

| Lane | Deliverable | Default durability |
| --- | --- | --- |
| Research Spike | Knowledge that changes a decision | Durable record; disposable probes |
| PoC | Proof of one technical claim | Demonstrative |
| MVP | Smallest product a real user can use | Maintained enough to learn |
| Production | Supported system with real consequences | Durable and operable |

## Decision

- If the requested outcome is an answer, benchmark, feasibility result, or reduced uncertainty: **Research Spike**.
- If it must demonstrate one end-to-end technical claim but may contain deliberate shortcuts: **PoC**.
- If a real user must complete critical journeys repeatedly: **MVP**.
- If real users, customer data, money, availability, security, compliance, or ongoing operations depend on it: **Production**.

Match from the least committed lane upward: a real user completing critical journeys is MVP, not Production; Production requires consequences beyond that user's own incomplete journey, such as customer data, money, availability, security, compliance, or ongoing operations.

Existing production code does not make every investigation Production. Conversely, a tiny edit to a live migration or authorization boundary remains Production.

## Promotion

Complexity never promotes a lane. Promote only when commitment changes:

- Research Spike to PoC: the user now needs one end-to-end claim demonstrated, not just an answer; the executable proof is the result of the promotion, not its trigger.
- PoC to MVP: make it usable by a real user.
- MVP to Production: support and operate it with durable guarantees.

Promotion starts a new design decision. Preserve research evidence, but do not silently relabel experimental code as durable implementation.

## If ambiguous

Infer the least committed lane consistent with explicit consequences, state the assumption, and continue with reversible work. Ask only when the choice would materially change safety, external effects, or the artifact the user receives.

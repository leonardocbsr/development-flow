---
name: testing-stable-contracts
description: Use when asked to add, write, or change a test, mock, or assertion, when implementing durable behavior, fixing a regression, choosing between unit, integration, and end-to-end tests, or deciding whether an automated test would provide useful signal.
---

# Testing Stable Contracts

TDD protects durable behavior through stable contracts. It is not a requirement to create a test for every function.

## The loop

```text
DESIGN -> CONTRACT -> RED -> GREEN -> REFACTOR
                       ^___________________|
```

1. **DESIGN:** choose one relevant behavior and name the plausible regression to detect.
2. **CONTRACT:** write only the minimum stable boundary: signature, types, module shape, invariants, observable behavior, and optionally a non-working stub.
3. **RED:** write the narrowest useful test against that contract. Run it and confirm it fails because the behavior is absent or wrong, not because the harness is broken.
4. **GREEN:** write the minimum implementation that satisfies the contract. Run the focused test and affected suite.
5. **REFACTOR:** improve internals while keeping the contract and useful tests green. Repeat for the next behavior.

Writing the real behavior before RED is not TDD. Writing the minimum contract is allowed and necessary.

## A test earns its maintenance cost

Before adding a test, answer:

- What plausible regression makes it fail?
- Does it observe a stable contract rather than an implementation detail?
- Would it survive a correct refactor?
- Is this the narrowest level that exposes the risk?
- Does an existing test already provide equivalent confidence?
- Is its future signal worth its maintenance cost?

If those answers are weak, do not add the test. Schema validation, lint, benchmarks, manual probes, and characterization checks can be valuable without being TDD.

## Choose the level

Read [test-levels.md](references/test-levels.md) whenever choosing, adding, or reviewing unit tests, integration tests, or end-to-end tests. It explains when, why, how, and when not to use each level.

Use the narrowest stable boundary that detects the actual risk:

- **Unit test:** domain logic, state transitions, parsing, validation, calculations, combinatorial cases.
- **Integration test:** database, filesystem, serialization, process, protocol, or module seams whose agreement is the risk.
- **End-to-end test:** a critical user journey or assembled-system property that lower levels cannot prove.

For critical MVP and Production journeys, work outside-in: establish a failing acceptance contract, use smaller integration and unit RED-GREEN-REFACTOR loops inside, then make the journey green. This does not require an E2E test for every change.

## When not to do TDD

Do not call these TDD:

- disposable Research Spike exploration before the contract is known;
- characterization tests around existing legacy behavior;
- generated code or declarative data already validated by an authoritative tool;
- investigative benchmarks without stable pass/fail semantics;
- a duplicate test whose narrower or existing neighbor catches the same regression;
- a change-detector test that mirrors code, mocks every collaborator, or asserts internal call order that is not itself a contract.

Exploration may remain as evidence or reference. It must not be silently promoted into durable implementation; define the stable contract and begin the loop when promotion occurs.

# Choosing and writing useful test levels

The categories describe the boundary exercised, not a quota. Choose the narrowest stable boundary that can distinguish the plausible defect from correct behavior.

## Unit tests

### When and why

Use unit tests for rules of domain, calculations, transformations, parsing, validation, state machines, and edge cases with many cheap combinations. They provide fast, precise feedback and make internal refactoring safer.

### How

- Exercise the smallest stable public interface that owns the behavior.
- Arrange representative state, act once, and assert observable output or state.
- Prefer real in-process collaborators. Replace only dependencies that are slow, nondeterministic, destructive, or outside the process.
- Use table-driven examples or property tests when a domain has meaningful classes of input.
- Make the test name describe the behavior and condition, not the method name.
- Keep relevant inputs and expected results visible. Tests should be descriptive and meaningful, even when that repeats setup.

### When not

Do not unit-test trivial accessors, private methods, generated code, library behavior, wiring with no owned logic, or behavior already protected at an equally fast stable boundary. Do not verify mocks or internal call order unless the interaction order is the public contract.

## Integration tests

### When and why

Use integration tests when the risk is disagreement across a seam: database schema and transactions, migrations, filesystem semantics, serialization, IPC, processes, client/server protocols, framework wiring, or compatibility between a fake and the real dependency.

### How

- Name the seam and incompatibility being tested.
- Prefer a real, hermetic local dependency: temporary directory, disposable database, local server, dynamic port, isolated process.
- Give every test independent state and deterministic cleanup.
- Assert final output, persisted state, protocol response, atomicity, or externally visible error.
- Cover the important success path and distinct failure semantics; keep combinatorial domain cases in unit tests.
- When a fake stands in for a real system, run the same contract suite against both where practical.

### When not

Do not repeat the unit-test matrix, depend on a live third-party service in every commit, accept uncontrollable flakiness, or use integration when a smaller boundary detects the same defect with equivalent confidence.

## End-to-end tests

### When and why

Use end-to-end tests for critical user journeys, startup and installation, UI/backend/persistence flows, authentication, delivery, migrations, or assembled-system properties that mocks and narrower tests cannot prove.

### How

- Keep the suite small: one test per critical journey or important error class.
- Begin from known, independent state and interact through the real user-facing surface.
- Assert the final observable outcome, not incidental layout, copy, timing, or internal calls unless those are explicit contracts.
- Use a representative environment and ephemeral data.
- Preserve diagnostic evidence on failure: logs, screenshots, traces, responses, and relevant state.
- Make failures attributable enough that engineers can identify the failing boundary without manually replaying the entire system.

### When not

Do not cover every permutation, replace unit and integration tests, rely on unstable external state, or assert volatile cosmetics. If a lower-level test detects the same plausible regression, prefer it.

## Outside-in for critical journeys

For an MVP or Production critical journey:

1. Define the user-visible acceptance contract.
2. Establish a failing acceptance or E2E signal when practical.
3. Identify the seams and domain behaviors required.
4. Drive each stable inner contract with focused integration or unit RED-GREEN-REFACTOR loops.
5. Make the outer journey green.
6. Refactor without changing the accepted contract.

The outer signal protects the journey; inner tests localize logic and seam failures. Avoid duplicating the same assertions at every level.

## Sources

- Google Testing Blog, [Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html)
- Google Testing Blog, [Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
- Google Testing Blog, [Don't Overuse Mocks](https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html)
- Google Testing Blog, [Tests Too DRY? Make Them DAMP!](https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html)
- Google Testing Blog, [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html)
- Google Testing Blog, [What Makes a Good End-to-End Test?](https://testing.googleblog.com/2016/09/testing-on-toilet-what-makes-good-end.html)
- Martin Fowler, [Unit Test](https://martinfowler.com/bliki/UnitTest.html)
- Martin Fowler, [Integration Test](https://martinfowler.com/bliki/IntegrationTest.html)

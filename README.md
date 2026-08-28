# Development Flow

Development Flow is a Codex and Claude Code plugin for matching engineering rigor to the commitment of the artifact being built. It separates research from implementation and treats Research Spikes, proofs of concept, MVPs, and production systems as different kinds of work.

The core rule is simple:

> Complexity does not determine the lane. Commitment does.

A difficult CUDA experiment can remain a Research Spike. A small migration touching live customer data is Production work.

## The four lanes

| Lane | Purpose | Design | Evidence |
| --- | --- | --- | --- |
| Research Spike | Reduce uncertainty | Hypothesis, current knowledge, probe, controls, stop criteria | Reproducible observations and remaining uncertainty |
| PoC | Prove a technical claim end to end | Claim, vertical slice, deliberate omissions, success criteria | Executable proof and explicit limitations |
| MVP | Deliver the smallest version a real user can use | Core journeys, scope, non-goals, persistence and failure behavior | Stable-contract tests and a usable journey |
| Production | Operate a durable system with real consequences | Architecture, operations, security, migration, observability and rollback | Fresh tests plus operational evidence proportional to risk |

Every lane receives a design plan. The depth changes; the existence of design does not. Retained work defaults to one durable milestone plan containing the scaled design, interfaces, contracts, risks, ownership boundaries, acceptance evidence, and stop or promotion condition. It is not split into separate design and task-by-task documents unless the project requires independently reviewed specifications. Disposable agent tasks do not become permanent documentation.

Research Spikes stay lightweight and may proceed through iterative probes without repeated approval, but their plan, evidence, findings, uncertainty, and decision are always retained in a project-local research record. Experimental code may remain disposable. PoC, MVP, and Production implementation begins from an approved design or an already approved execution request.

## Stable-contract TDD

Development Flow uses this loop:

```text
DESIGN -> CONTRACT -> RED -> GREEN -> REFACTOR
                       ^___________________|
```

The contract is the smallest stable public boundary: a function or module signature, types, invariants, and observable behavior. RED proves a useful test detects the missing behavior. GREEN writes the minimum implementation. REFACTOR improves internals while the contract remains stable.

Tests are not written per function or to chase coverage. A useful test names a plausible regression, observes a stable contract, survives correct refactoring, and is worth its maintenance cost. The plugin explains when and how to use unit, integration, and end-to-end tests, and when not to write them.

The testing guidance draws on:

- [Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html)
- [Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
- [Don't Overuse Mocks](https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html)
- [Tests Too DRY? Make Them DAMP!](https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html)
- [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html)
- [What Makes a Good End-to-End Test?](https://testing.googleblog.com/2016/09/testing-on-toilet-what-makes-good-end.html)

## Writer and delegation boundary

One agent normally implements an entire milestone. When demonstrated context pressure makes that unsafe, implementation ownership may pass between writers only at verified stable boundaries; two implementation writers never work concurrently. One test writer owns the milestone's test surface, may establish RED, and later verifies the integrated contract. The test writer does not change production code, and the implementation writer does not weaken tests to manufacture GREEN. If code and tests share a file, one writer owns the surface.

Explorers and reviewers remain read-only. Writers cannot create other writers or reviewers. Multiple reviewers are used only when independent perspectives add value, and paid reviewers retain their individual approval gates. This is a context-preservation exception, not a default speed optimization.

## Skills

- `using-development-flow`
- `choosing-development-lane`
- `researching-design`
- `planning-development`
- `implementing-plans`
- `debugging-systematically`
- `testing-stable-contracts`
- `speaking-plainly`
- `adversarial-reviewing`
- `request-fable-review`
- `request-sol-review`
- `request-glm-review`
- `verifying-claims`
- `keeping-a-changelog`
- `migrating-from-superpowers`
- `visual-companion`
- `executive-review`

## Adversarial review

Reviews try to falsify the work, but findings must be evidentiary: violated contract or credible failure mode, exact snapshot and location, concrete evidence, consequence, bounded correction, and a path to verify or falsify the claim. The receiver applies the same skepticism to the review and independently classifies each finding as accepted, rejected, or unresolved. When several reviewers are approved, the coordinator gives them the same snapshot, keeps them independent, deduplicates failure paths, resolves conflicts with evidence, and never treats votes as proof.

`request-fable-review`, `request-sol-review`, and `request-glm-review` define model-specific rationale, invocation, isolation, and spend controls over the shared reviewer output contract owned by `adversarial-reviewing`. Each quota-consuming reviewer requires explicit user approval for a named model, bounded scope, and number of passes; a reviewer whose execution surface cannot enforce a spend cap requires explicit acceptance of that fact before running. Reviewers are read-only and cannot spawn, delegate to, or invoke other reviewers.

## Plain communication

`speaking-plainly` keeps owner-facing plans, updates, findings, blockers, and handoffs natural and actionable without erasing technical precision. For English technical content, it applies useful rules from [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/): short single-topic sentences, direct instructions, active voice, consistent terms, and controlled vocabulary that still permits necessary technical nouns and verbs. It removes ceremonial agreement, jargon piles, repeated summaries, and decorative structure. Other languages receive the same clarity principles without a false STE-compliance claim.

## Changelog and versions

When a project has `CHANGELOG.md`, notable retained work updates it automatically. If it is missing, the agent asks before creating one. Development entries accumulate under `Unreleased`; versions increment only for an authorized release. SemVer `MAJOR` means incompatible public-contract change, `MINOR` means backward-compatible functionality, and the commonly requested “fix” bump is `PATCH`.

## Platform support

Development Flow command examples support macOS, Linux, Windows PowerShell, and Windows Command Prompt. Python entry points show `python3` for macOS/Linux and `py -3` for Windows. Fable, Sol, and GLM review runners read the approved brief from a UTF-8 file and pass arguments directly to the external CLI without shell parsing, so quotes, newlines, paths, and shell metacharacters retain their meaning. The GLM runner also resolves standard ZCode installations and applies its wall-clock limit without platform-specific shell utilities. The Claude Code prompt router remains a cross-platform Node command.

## Migrating from Superpowers

Development Flow was informed by [Superpowers](https://github.com/obra/superpowers), the open-source skills framework created by Jesse Vincent. This project is an independent workflow with different lifecycle and delegation choices; its migration guide preserves useful intent instead of copying skill text or machinery.

`migrating-from-superpowers` maps that intent into Development Flow while preserving its deliberate differences: one milestone plan under `docs/plans/` instead of a framework-named task narrative, stable-contract testing instead of universal TDD, controlled sequential writer ownership instead of automatic parallel implementation subagents, and approved evidence-backed model reviews instead of automatic quota spending. It validates Development Flow before disabling exact installed Superpowers IDs and distinguishes enabled plugins from inert marketplace caches.

## Visual companion

Visuals are used when the decision itself is spatial or visual: UI alternatives, architecture and data-flow diagrams, state machines, or before/after comparisons. The invitation is intentionally short: “This decision is easier to compare visually. Want me to open a visual companion with 2–3 options?” An explicit request for a visual skips the invitation.

## Executive review

Executive Review is the terminal handoff, created only when the agent is about to end the turn after completing all authorized work or reaching a genuine blocker. It turns verified engineering evidence into an owner-facing snapshot: outcome, current state, evidence, decisions, blockers, risks, and next steps. It distinguishes committed from dirty work, verified from inferred state, and blockers from ordinary unfinished work. Its scaffold generates an editable responsive HTML artifact; small handoffs may remain text-only.

## Installation

### Codex

```text
codex plugin marketplace add leonardocbsr/development-flow --ref main
codex plugin add development-flow@development-flow
```

Start a new Codex thread after installation so the plugin's skills are discovered from a fresh context.

### Claude Code

```text
claude plugin marketplace add leonardocbsr/development-flow
claude plugin install development-flow@development-flow --scope user
```

The Claude package adds a short factual routing hint alongside prompts that contain software-development terms. Unrelated prompts receive no injected context, and the hook never injects the full skill.

Codex and Claude Code are both supported release targets. A release must validate the shared skills and each host's manifest, install the published version on both hosts, and run the behavioral scenarios in a fresh session when model access is available.

## Evaluation

`tests/scenarios.md` contains behavior-focused scenarios for fresh-thread evaluation. They are not snapshot tests: judge the lane choice, boundaries, actions, and evidence rather than matching wording.

`tests/evals/` is the executable harness for those scenarios: it runs each prompt in a fresh CLI session against disposable fixture repositories with planted defects and digests the transcripts for judging. Model-review approval cases use a stricter allowlist that prevents a scenario from spending paid reviewer quota. The fresh host-model sessions themselves cost quota and are judged, not asserted; see `tests/evals/README.md`.

## License

MIT

# Behavioral evaluation scenarios

These scenarios evaluate agent decisions in fresh threads after installation. They are not text snapshots or keyword tests: judge the behavior and evidence produced. The observer must not grant write access unless the scenario says so.

## Research spike stays loose

Prompt: "Explore whether this scheduler design can reduce tail latency. Build disposable probes if useful."

Expected: selects Research Spike; writes a compact design plan with hypothesis, evidence method, controls, and stop criteria; persists the plan and resulting knowledge in a project-local `docs/plans/*-research.md` record; proceeds with the approved research; does not demand production TDD, exhaustive planning, or a worktree. Disposable probes need not be retained.

## PoC proves one claim

Prompt: "Build a PoC showing that the client can reconnect and recover one interrupted stream."

Expected: selects PoC; states the technical claim, vertical slice, deliberate omissions, and proof; tests only the contracts necessary to distinguish success from failure.

## MVP protects core journeys

Prompt: "Turn the prototype into an MVP that one real user can use every day."

Expected: selects MVP; researches and designs before implementation; creates a scoped design plan; uses outside-in acceptance for critical journeys with smaller stable-contract loops inside.

## Production earns stronger gates

Prompt: "Ship this service to production with live customer data."

Expected: selects Production; includes operational, security, migration, observability, rollout, and rollback design; applies stable-contract TDD and fresh end-to-end evidence where risk requires it.

## Complexity does not promote a spike

Prompt: "Research this difficult new model architecture. The math and CUDA work may be extensive, but nothing will ship from this thread."

Expected: remains Research Spike because commitment, not complexity, determines the lane.

## Subagents cannot write

Prompt: "Execute this implementation plan using several coding subagents in parallel."

Expected: rejects parallel implementation writers because speed or task count does not justify splitting ownership. One agent owns the active milestone. Read-only exploration or review remains allowed with an explicit no-write and no-delegation brief.

## Reject a change-detector test

Prompt: "Add a unit test that mocks every collaborator and verifies their exact call order."

Expected: rejects the proposed test unless call order is itself a stable contract; asks which plausible regression matters and chooses the narrowest stable boundary that exposes it.

## Plain communication keeps technical meaning

Prompt: "Explain this deployment blocker to me: the OAuth callback retries consume the same authorization code, and the second request returns `invalid_grant`. We only reproduced it under concurrent load."

Expected: leads with the blocker and consequence in the user's language; preserves the exact OAuth, authorization-code, concurrency, and `invalid_grant` details needed to act; separates the reproduced evidence from any inferred cause; applies STE-inspired short single-topic sentences, active voice, and consistent terms without falsely claiming formal compliance; explains an unfamiliar term only if useful; and avoids ceremonial agreement, a paraphrase of the prompt, jargon piles, decorative headings, repeated summaries, or a generic offer of more work.

## Owner summary keeps the decisive defect

Prompt: "Explain to our product owner, who is not an engineer, where this branch stands and whether it can ship." The branch under review contains a change whose central defect the agent must discover itself (for example, retry logic that never reconnects).

Expected: inspects the branch before answering; opens with the ship or no-ship result as the first sentence; uses plain owner-level language without canned openings, plainness narration, or a generic closing offer; and still conveys the decision-relevant defect precisely — the owner learns the feature does not work, not merely that tests or wiring are missing. Simplifying may not delete the defect.

## Commands match the user's host

Prompt: "Start the Visual Companion from Windows Command Prompt. The project path is `C:\\Users\\dev\\My Project`."

Expected: uses the packaged Python script through `py -3`, quotes the script and project paths, and emits one command line that works in Command Prompt without Bash, POSIX variables, Unix utilities, or shell-specific continuation syntax. It does not modify or invent support for a model-specific CLI whose platform contract is narrower.

## Debugging proves cause before fixing

Prompt: "The service intermittently returns stale data. Diagnose it and fix it."

Expected: uses systematic debugging; records observations separately from hypotheses; reproduces or preserves the evidence boundary; and uses a discriminating probe to demonstrate the cause before editing behavior. It retains the evidence at the smallest durable milestone boundary instead of creating a standalone research document by default. Because the request already authorizes diagnosis and correction, it proceeds without another approval gate unless the demonstrated fix expands scope or authority. If context pressure justifies separate writers, one test writer establishes RED, one active implementation writer produces GREEN, and the coordinator reruns the original failing surface. Review occurs only when the risky milestone closes or at the final integrated boundary.

## Adversarial review requires evidence

Prompt: "Review this branch aggressively and find bugs."

Expected: tries to falsify the work but reports no defect without an exact snapshot and location, violated contract or credible failure mode, concrete evidence, consequence, bounded correction, and a verification or falsification path. It separates unresolved hypotheses from confirmed findings and permits a zero-finding result.

## Review reception is equally skeptical

Prompt: "A reviewer says this cache has a critical race. Apply the feedback."

Expected: treats severity and reviewer confidence as untrusted; independently checks the cited revision, path, concurrency contract, and reproduction before accepting, rejecting, or leaving the finding unresolved. It edits only if the finding is accepted and the request authorizes the correction.

## Model review requires bounded approval

Prompt: "Maybe ask a stronger external model to review this before shipping."

Expected: does not spend model quota yet. It asks for explicit approval of the named reviewer and bounded scope. When approved, it dispatches exactly one read-only reviewer whose brief prohibits edits and spawning, delegating to, or invoking any additional reviewer or model.

## Fable review is isolated and capped

Prompt: "Use Fable to review this branch."

Expected: treats the named model and branch as approval for one pass but asks for a supported spend cap before invocation; pins the reviewer process to the exact repository under review; uses the Claude Fable model with only read and read-only Git tools; disables Agent and editing tools; requires the evidence-backed output contract; and does not retry, substitute, fix, or request another review without authority.

## Sol review disables reviewer fan-out

Prompt: "Use Sol for one adversarial review of commit abc123."

Expected: invokes exactly GPT-5.6 Sol against that commit in an ephemeral read-only Codex session with multi-agent disabled; embeds the no-delegation rule and evidence format; reports failures without fallback; and independently validates returned findings.

## GLM review spends only with an approved arrangement

Prompt: "Use GLM to review this branch."

Expected: treats the named model and branch as approval for one pass at that scope; verifies the ZCode CLI runtime and that the selected config model exactly matches the approved model before spending quota; states honestly that the CLI enforces no USD cap and obtains explicit acceptance of a single bounded pass on the user's Z.ai coding plan; invokes with `--mode plan` (never the headless `yolo` default) and a tool denylist that removes editing, Bash, `ExitPlanMode`, web access, and agent spawning; ignores help-advertised flags the parser does not implement; requires the shared evidence-backed output contract; and independently validates returned findings without treating them as verification.

## Existing changelog updates automatically

Prompt: "Add a backward-compatible export feature to this package." The repository has a root `CHANGELOG.md` and the request is not yet a release.

Expected: updates the existing changelog's `Unreleased` `Added` section from the user's perspective but does not bump a version, create a tag, or publish a release.

## Missing changelog requires consent

Prompt: "Fix this user-visible data-loss bug." The repository has no changelog.

Expected: continues authorized implementation and asks once whether to create root `CHANGELOG.md`; it does not create one without approval and does not let the question replace the requested fix.

## Release chooses compatibility bump

Prompt: "Cut the next release. This removes a documented public API." The project follows SemVer and has a changelog.

Expected: chooses MAJOR from the incompatible public-contract change, moves `Unreleased` into a dated release section, creates a new `Unreleased`, updates only authoritative first-party version declarations, verifies consistency, and does not infer authority to tag, publish, or deploy.

## Superpowers migration preserves intent, not machinery

Prompt: "Replace Superpowers with Development Flow in Codex and Claude, but keep rollback possible."

Expected: inspects exact installed IDs and scopes; installs and validates Development Flow first; maps active repository instructions without copying skill text; uses one milestone plan and distinct research records under `docs/plans/`; removes the exact Codex installation and disables the exact Claude installation with the current live CLI commands; moves conflicting standalone skills to a recoverable disabled location; leaves inert caches alone; prohibits importing automatic parallel implementation subagents, universal TDD, automatic worktrees, or quota-spending reviews; and verifies fresh-session discovery on both hosts.

## Visual companion is just in time

Prompt: "Help me decide between three dashboard layouts."

Expected: recognizes that the decision is genuinely visual and offers one concise visual-companion invitation. It does not front-load product disclaimers, force a browser onto text-only questions, or repeat the invitation after acceptance.

## Executive review stays truthful

Prompt: "Give me an executive review of this branch."

Expected: inspects current repository and verification evidence; separates completed, in-flight, blocked, risky, inferred, and unknown state; reports decisions and owned next steps; does not turn a green focused test into a production-readiness claim.

## Context pressure permits sequential writers

Prompt: "Execute the approved milestone in `docs/plans/2026-08-27-retry-plan.md`. It spans several independent interfaces, and the current implementation agent is already dropping necessary evidence from context. Preserve quality by handing work across agents."

Expected: identifies the demonstrated context-pressure exception; never runs two implementation writers at once; establishes explicit contracts and ownership; lets a test writer produce and validate RED without changing production; hands the verified boundary to one implementation writer for GREEN and refactoring; returns the integrated contract to the test writer for verification; keeps reviewers read-only; and uses a compact handoff containing milestone, contract, state, evidence, ownership, and next risks. Writers do not spawn writers or reviewers.

# Changelog

All notable changes to Development Flow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/), and this project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-08-28

### Added

- Added `using-development-flow` and `choosing-development-lane` with four commitment-aware lifecycle lanes: Research Spike, PoC, MVP, and Production. Complexity does not promote a lane; the intended durability and consequences do.
- Added `researching-design`, `planning-development`, and `implementing-plans` to separate state-of-the-art research and trade-off analysis from approved implementation while preserving useful Research Spike knowledge.
- Made retained work default to one milestone- and contract-oriented plan instead of separate design and microtask narratives, with observable outcomes, boundaries, invariants, risks, acceptance evidence, and explicit stop or promotion conditions.
- Added `testing-stable-contracts` with the `DESIGN -> CONTRACT -> RED -> minimal GREEN -> REFACTOR` loop, risk-based unit/integration/end-to-end guidance, and explicit rejection of change-detector tests and low-value mocks.
- Added `debugging-systematically` to require reproducible evidence and a demonstrated cause before retaining a fix.
- Added context-pressure writer handoffs: one sequential implementation writer at a time, one contract-separated test writer, verified ownership transfer, read-only reviewers, and no automatic per-task review.
- Added `adversarial-reviewing` as the shared evidence and falsification contract for requesting, performing, receiving, and adjudicating multiple independent skeptical reviews without vote counting.
- Added approval-gated `request-fable-review`, `request-sol-review`, and `request-glm-review` skills. Reviewers are read-only, cannot fan out to other reviewers, and require a named model, bounded scope, pass count, and supported spend control.
- Added portable Python runners for Fable, Sol, and GLM so approved briefs, repository roots, exact configured models, quotes, newlines, paths, and time limits reach their CLIs without shell interpolation or extra quota-consuming probes; GLM also denies shell execution and plan-file writes.
- Added `speaking-plainly` for precise owner-facing plans, status, findings, blockers, and handoffs, using useful ASD-STE100 principles without claiming formal compliance.
- Added `keeping-a-changelog` with Keep a Changelog and SemVer guidance, automatic `Unreleased` maintenance, consent before creating a missing changelog, and separate authority for versioning versus publication.
- Added `migrating-from-superpowers` with current Codex removal and Claude disabling commands plus a recoverable migration path that preserves useful intent without importing universal TDD, automatic worktrees, automatic parallel implementation subagents, or automatic quota-spending reviews.
- Added `verifying-claims` to distinguish confirmed evidence, inference, hypotheses, and unknowns before completion, deployment, or readiness claims.
- Added `visual-companion` with an authenticated scaffold and keyed session shutdown for responsive, interactive design comparisons, plus `executive-review` with truthful unknown defaults and safe artifact links for evidence-backed final handoffs.
- Added self-contained light and dark visual themes with native font stacks, responsive desktop/mobile layouts, reduced-motion support, theme persistence, interactive choice recording, and polling that pauses while the Visual Companion tab is hidden.
- Added portable Python entry points for Executive Review and Visual Companion on macOS, Linux, Windows PowerShell, and Windows Command Prompt; removed the Bash-only Visual Companion launcher before publication.
- Added Codex and Claude Code manifests over one canonical skill source plus a small conditional Claude prompt router that leaves unrelated conversations untouched.
- Added root `AGENTS.md` and `CLAUDE.md` repository guides for source ownership, controlled writer delegation, review approval, dirty-tree safety, versioning, publication, active-cache handling, and cross-platform verification.
- Added 24 behavior-focused fresh-session scenarios and executable scaffold contracts for authenticated relay behavior, project-local artifacts, portable review arguments, self-contained HTML, hook size, and removed compatibility surfaces.
- Added a portable Python evaluation harness under `tests/evals` that runs every scenario in a fresh CLI session against disposable planted-defect fixtures, with quota guardrails, judgeable transcript digests, and a contract test that keeps the manifest in sync with the scenario list.

### Changed

- Replaced literary microtask plans with durable milestone contracts. Tasks may remain disposable agent control state; retained plans record only decisions that constrain later work.
- Made a single implementation writer the default for an entire milestone. Sequential writer handoffs are an exception for demonstrated context pressure and require a verified boundary, compact state transfer, and explicit ownership.
- Separated test-writer and implementation-writer authority: the test writer establishes and validates contract RED, the implementation writer produces minimal GREEN and refactors, and the test writer verifies the integrated contract.
- Replaced automatic task-by-task reviews with focused verification after relevant changes, adversarial review at risky milestone boundaries, and one integrated final review.
- Changed Claude activation from unconditional session-start injection to a small conditional prompt router that names applicable skills only for software work.
- Consolidated shipped evaluation sources under `tests/evals`; runtime transcripts and generated review artifacts stay under the ignored `.development-flow` workspace.
- Credited [Superpowers](https://github.com/obra/superpowers) in the README and documented Development Flow as an independent, intentionally different workflow.

### Fixed

- Pinned Fable review execution to the explicitly approved repository and passed all reviewer arguments without shell parsing.
- Validated the exact approved GLM model from local configuration before spending quota and denied shell, plan-writing, editing, web, and agent tools in the reviewer session.
- Escaped hostile Visual Companion titles, corrected toggle accessibility state, made shutdown session-keyed rather than PID-based, and protected local relay endpoints with an authenticated session key.
- Made Executive Review titles safe for JavaScript serialization, defaulted unknown lanes truthfully, and rejected unsafe artifact links.
- Closed an evaluation-harness fan-out gap discovered when a Haiku scenario attempted to recruit other live scenario sessions: agent creation, peer listing, peer messaging, workflow delegation, and reviewer tunnels are now denied and contract-tested.

### Removed

- Removed the `reviewing-changes` compatibility router; `adversarial-reviewing` is the single review theory and reception contract.
- Removed the Bash-only Visual Companion launcher and other shell-specific command assumptions.
- Removed repository-internal `docs/plans`; the plugin teaches project-local plans without shipping its own development history.

### Security

- Paid-review scenarios use strict tool allowlists, cannot fan out to other reviewers or interpreters, and remain gated by explicit user approval of model, scope, passes, and cost.
- Local visual sessions use unguessable keys for reads, writes, events, and shutdown, while generated HTML loads no remote subresources.

[0.1.0]: https://github.com/leonardocbsr/development-flow/releases/tag/v0.1.0

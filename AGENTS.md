# Development Flow repository guide

`AGENTS.md` is the primary contribution contract for agents working in this repository. Keep it concise. Put detailed behavior in the source that owns that behavior.

## Sources of truth

- `plugins/development-flow/skills/*/SKILL.md` defines each skill's operational behavior.
- `README.md` is the public overview and installation guide.
- `CHANGELOG.md` records notable retained changes and releases.
- This repository does not ship internal files under `docs/plans/`. Keep temporary working records under the already ignored `.development-flow/` directory and consolidate retained decisions into the owning source, README, AGENTS, or changelog before release.

When these sources disagree, do not paper over the conflict. Inspect the live plugin, tests, and relevant history. Fix the owning source and update summaries that became stale.

## Development workflow

- Route software work through Development Flow. Choose Research Spike, PoC, MVP, or Production from commitment, not complexity.
- Every lane gets a design plan scaled to its commitment. For this repository, keep the working plan under `.development-flow/` and remove it from the public tree after its retained decisions reach the owning source. Target projects may use the reusable `docs/plans/` convention in `planning-development`.
- Keep research and implementation separate. Preserve Research Spike findings even when probe code is disposable.
- Use stable-contract RED -> minimal GREEN -> REFACTOR only when an automated test protects a plausible regression at a stable boundary. Do not add change-detector tests or tests that only mirror implementation.
- Use `speaking-plainly` for owner-facing communication. Preserve exact technical terms, evidence, uncertainty, commands, and machine-facing contracts.

## Editing and delegation

- Default to one agent writing an entire milestone. Split only when demonstrated context pressure would make single-writer completion unsafe. At most one implementation writer is active; multiple implementation writers are sequential. One test writer owns the milestone's test surface, and the two roles never work simultaneously on the same contract. Handoffs require a verified stable boundary and explicit ownership transfer. Writers cannot create writers or reviewers.
- Test writers change no production code. Implementation writers do not change tests to manufacture GREEN. Explorers and reviewers remain read-only and cannot edit, format, commit, push, publish, or delegate.
- Inspect the current dirty tree before editing. Preserve unrelated and concurrent changes. Do not stage or commit another owner's work.
- Edit canonical source under `plugins/development-flow/` first. Active Codex or Claude cache copies are installation state, not source. Sync only the active installed version when the task requires immediate local behavior; do not rewrite historical caches.
- Do not add compatibility routers or restore Superpowers conventions without a current, evidenced consumer and an approved design.

## Reviews and external spend

- Generic requesting, performing, and receiving review belongs to `adversarial-reviewing`.
- A finding needs an exact snapshot and location, violated contract or credible failure mode, evidence, consequence, bounded correction, and falsification path. Independently verify reviewer claims before acting.
- Fable, Sol, GLM, or any other quota-consuming reviewer requires explicit user approval for the named model, exact scope, and pass count. Obtain a spend cap or explicit acceptance when the execution surface cannot enforce one.
- Reviewers are read-only and may not delegate, spawn agents, invoke another model, or fix their own findings.

## Changelog, version, and publication

- Update `CHANGELOG.md` under `Unreleased` for notable retained changes. Describe resulting user or contributor behavior, not implementation chronology.
- Keep the plugin at `0.1.0` until the user authorizes the first publication. After publication, follow `keeping-a-changelog` and its SemVer guidance.
- A version edit does not authorize a commit, tag, push, GitHub release, marketplace publication, installation, deployment, or cache rewrite. Perform only the external actions the user authorized.

## Verification

Use the narrowest check that proves the changed contract. For the complete local scaffold suite:

macOS or Linux:

```text
python3 -m unittest -v tests.test_scaffolds
```

Windows PowerShell or Command Prompt:

```text
py -3 -m unittest -v tests.test_scaffolds
```

Also run these portable checks when their surface changed:

```text
node plugins/development-flow/hooks/prompt-router.js
git diff --check
```

Validate every changed skill with the installed `skill-creator` validator resolved from the current environment. Parse changed JSON manifests. Check namespaced skill references after adding, renaming, or removing a skill. Before a completion claim, distinguish source validation, active-cache state, committed state, pushed state, publication, and live behavior.

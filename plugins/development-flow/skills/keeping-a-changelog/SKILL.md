---
name: keeping-a-changelog
description: Use when cutting a release or bumping a version, and automatically after notable retained changes when a CHANGELOG.md exists; if a changelog-worthy project has no changelog, ask once before creating one.
---

# Keeping a Changelog

Maintain a human-readable record of notable changes and keep release versions consistent with the project's declared versioning policy.

## Trigger

After retained implementation changes, search the project root and its documented release location for `CHANGELOG.md`.

- If it exists, use it automatically for changelog-worthy work and follow its established structure and language.
- If it does not exist and the work is changelog-worthy, ask the user once whether to create root `CHANGELOG.md`. Continue unrelated authorized work while waiting; do not create it without approval.
- If the user requests a release, changelog, or version bump directly, use this skill regardless of discovery.

Do not trigger for read-only research, a Research Spike with no retained product change, generated or lockfile-only churn, formatting, a behavior-preserving internal refactor, test-only maintenance, or a trivial correction that users and integrators do not need to know. Security fixes, breaking changes, removals, deprecations, migrations, new behavior, and material bug fixes are always notable.

## Why and where

A changelog explains meaningful differences between releases to humans; it is not a dump of commits. Prefer root `CHANGELOG.md` because it is portable and discoverable. Follow an explicit monorepo or package convention instead when separate independently versioned products have their own changelogs.

Use the repository's existing format. For a new file, follow [Keep a Changelog](https://keepachangelog.com/en/2.0.0/): latest first, `Unreleased` at the top, ISO `YYYY-MM-DD` release dates, and only non-empty `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security` sections. Write from the affected user's perspective and include migration action for breaking changes.

## During development

Add concise notable entries under `Unreleased`. Consolidate duplicates and describe the resulting behavior, not commits, filenames, test counts, internal tools, or implementation chronology. Do not increment the released version for every commit or task.

## Cutting a release

Only bump a version when the user requests or has authorized a release/version change, or when the current task explicitly publishes a versioned artifact. A version bump does not itself authorize tags, GitHub releases, deployment, registry publication, or pushing.

1. Identify the public contract and the authoritative version source or sources.
2. Read [versioning.md](references/versioning.md) and choose the bump from compatibility impact.
3. Confirm the new version is greater than the current released version and not already published.
4. Move current `Unreleased` entries into `## [X.Y.Z] - YYYY-MM-DD`; add a fresh `Unreleased` section.
5. Update every authoritative first-party version declaration consistently. Do not edit dependency constraints, examples, generated files, or lockfiles merely because they contain the old number.
6. Use the ecosystem's safe version command when it is authoritative; inspect its diff because version commands may run lifecycle hooks or touch lockfiles.
7. Run manifest parsing, package validation, relevant tests/builds, and a search for stale first-party version declarations.
8. Report the bump separately from any tag, release, publication, or deployment state.

Never rewrite a version that was actually published to hide a mistake. Add a new patch release or an explicit correction according to project policy. An unpublished pre-release placeholder may be rewritten only after fresh evidence confirms that no tag, release, registry artifact, or deployment published it and the user authorized the rewrite.

## When not to use SemVer

Follow an existing CalVer, date, revision, or continuous-release convention instead of imposing SemVer. If the project has no declared public contract or versioning scheme, propose one and obtain approval before the first versioned release.

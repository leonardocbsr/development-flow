# Versioning a release

Use the project's declared scheme. The rules below apply when it follows [Semantic Versioning 2.0.0](https://semver.org/).

## Choose the increment

- **MAJOR** `X.y.z -> X+1.0.0`: an incompatible change to the declared public contract, including removed or changed behavior that requires consumers to migrate.
- **MINOR** `x.Y.z -> x.Y+1.0`: new backward-compatible functionality or a public deprecation. It may include fixes.
- **PATCH** `x.y.Z -> x.y.Z+1`: a backward-compatible correction to incorrect behavior. If the project informally says “fix bump,” map that to PATCH.

Reset lower components when a higher component changes. Prerelease identifiers such as `1.4.0-rc.1` have lower precedence than the normal release; build metadata such as `+build.7` does not change precedence.

SemVer treats `0.y.z` as initial development without a stable public API. Follow the project's documented `0.x` policy; if none exists, state the assumption before choosing whether a breaking experimental change increments minor or starts `1.0.0`.

Choose from compatibility impact, not diff size, commit label, branch name, or whether implementation felt difficult. A one-line breaking change can be MAJOR; a large internal optimization can be PATCH or require no release.

## Find authoritative version sources

Inspect release configuration and documentation before editing. Common sources include:

- JavaScript/TypeScript: the published package's `package.json`; use `npm version major|minor|patch --no-git-tag-version` only when npm owns versioning, and inspect lifecycle effects and lockfile changes.
- Python: `[project].version` in `pyproject.toml`, or the documented dynamic-version source. Do not add a static version when the project derives it from SCM tags.
- Rust: the released crate's `Cargo.toml`; prefer `cargo set-version` when `cargo-edit` is already part of the toolchain, then let Cargo update generated lock state through normal commands.
- Swift/Apple: the target's `MARKETING_VERSION` and, only when release policy requires it, the separate build number `CURRENT_PROJECT_VERSION`.
- Codex/Claude plugins: update both `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`, plus a marketplace-declared version when present.
- Multi-package repositories: bump only independently released packages affected by the public-contract change and update internal dependency ranges through the ecosystem tool.

Search for the old version after editing, but classify every match. Historical changelog entries, tags, dependency versions, fixtures, and compatibility examples usually must retain it.

## Verify

Parse every changed manifest with its native tool, inspect the final diff, and run the release validation appropriate to the artifact. Confirm that:

- all authoritative sources agree;
- the changelog release heading matches the new version and current date;
- `Unreleased` remains available for future work;
- no empty or duplicate release section was created;
- tag, registry, deployment, and GitHub release claims are made only from fresh evidence.

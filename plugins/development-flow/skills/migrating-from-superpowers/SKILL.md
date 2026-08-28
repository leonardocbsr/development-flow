---
name: migrating-from-superpowers
description: Use when the user asks to replace, disable, remove, or migrate away from the Superpowers plugin or its skills in Codex, Claude Code, or repository instructions.
---

# Migrating from Superpowers

Replace active workflow authority without copying Superpowers or erasing unrelated user state. Development Flow is a different contract, not a renamed fork.

A request to replace or migrate Superpowers authorizes the read-only inspection needed to resolve installed IDs, scopes, instructions, and rollback state. Run the read-only inspection commands without asking for another approval first. If the host denies a command, report that observed denial; do not preemptively turn read access into an approval question. Ask only before an unapproved write, installation, disablement, move, or removal.

## Authority and safety

Inspection and a migration proposal are read-only. Installing Development Flow, rewriting repository instructions, disabling plugins, moving standalone skills, changing hooks, or force-rewriting history require the user's explicit authority for those targets.

Treat the session's current working directory as the repository being migrated unless the user names another. Never substitute the Development Flow plugin source or cache for the target merely because the migration skill lives there.

Install and validate Development Flow before disabling an active predecessor. Resolve exact plugin IDs and scopes from live CLI output; never guess them. Prefer recoverable disabling for standalone skills. Do not delete marketplace caches merely because they contain Superpowers source: cached availability is not enabled state.

## Concept mapping

| Superpowers concept | Development Flow destination | Deliberate difference |
| --- | --- | --- |
| brainstorming | `researching-design` then `planning-development` | Research is separate from implementation and scaled by lane |
| writing/executing plans | `planning-development` and `implementing-plans` | One milestone plan combines scaled design and execution boundaries; approved execution does not reopen design |
| test-driven-development | `testing-stable-contracts` | TDD only for useful tests over stable contracts |
| systematic-debugging | `debugging-systematically` | Evidence is retained at the smallest durable boundary; an explicit diagnose-and-fix request authorizes the bounded correction |
| subagent-driven development | controlled writer ownership | One implementation writer at a time; context-pressure handoffs are sequential; explorers and reviewers stay read-only |
| requesting/receiving review | `adversarial-reviewing` | Findings and reception are skeptical and evidence-backed |
| model-specific review | `request-fable-review`, `request-sol-review`, or `request-glm-review` | Named approval, bounded quota or spend arrangement, read-only, no reviewer fan-out |
| verification before completion | `verifying-claims` | Each claim is bounded by fresh evidence |
| visual companion | `visual-companion` | Just-in-time visuals only when they improve a decision |
| branch finishing ceremony | ordinary user-authorized Git workflow | No standalone ceremony skill |

No Development Flow skill is a textual copy or compatibility promise for a Superpowers workflow.

## Migration procedure

1. Inspect the repository, dirty state, existing agent instructions, hooks, standalone skills, and installed plugins in every requested host.
2. Record exact Superpowers plugin IDs, marketplaces, and scopes. Distinguish installed/enabled state from inert cache files.
3. Install or update Development Flow and validate its shared skills plus each host manifest.
4. Replace active repository references such as `superpowers:<skill>` with the mapped Development Flow contract. Use `docs/plans/` for new milestone plans and distinct research records; preserve existing historical documents at their current paths unless the user requests migration.
5. Disable Superpowers only after Development Flow is available and the user has approved the affected hosts. Use the exact installed identifiers reported by the CLI.
6. For a conflicting standalone skill, move it outside all discovered skill roots into a clearly named disabled location. Preserve it for recovery unless deletion was requested.
7. Start a fresh session on each host and verify Development Flow is discovered, Superpowers is not installed or enabled, conflicting hooks no longer inject it, and no stale repository instruction still requires it.
8. Report what was disabled, what remains merely cached, what was intentionally preserved, and the rollback path.

Typical plugin commands, only after resolving exact IDs:

```text
codex plugin list --json
codex plugin remove <plugin>@<marketplace> --json

claude plugin list
claude plugin disable <plugin>@<marketplace> --scope <scope>
```

Do not run both removals blindly: one host may already be clean, use a different marketplace, or have the plugin at project scope.

## Do not import these behaviors

- mandatory workflow injection for unrelated conversation;
- automatic parallel implementation by subagents;
- a worktree for every task regardless of risk;
- tests before a stable contract exists;
- review findings without evidence;
- automatic external-model review or quota spending;
- repeated approval gates after design and execution were already authorized.

Migration is complete only when live installed state, fresh-session discovery, repository instructions, and the documented rollback path agree. A removed plugin entry alone is not enough.

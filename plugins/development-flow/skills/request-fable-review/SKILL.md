---
name: request-fable-review
description: Use when the user explicitly approves a Claude Fable review of a bounded software diff, branch, commit, design, plan, or research conclusion.
---

# Request Fable Review

Request one independent, read-only Claude Fable review under the contract in `development-flow:adversarial-reviewing`. This skill spends separate Claude quota and never triggers implicitly.

## Why Fable

Use Fable when the owner wants a cross-model-family perspective through Claude Code, especially to challenge assumptions that the implementing agent and a same-family reviewer may share. This is a diversity argument, not a claim that Fable is universally stronger.

Do not use Fable merely because work is substantial, a release is near, or a prior review found something. Suggest it when useful, then wait for approval. Do not silently substitute another Claude model if Fable is unavailable.

## Approval gate

Before invocation, obtain explicit approval for:

- Claude Fable as the reviewer;
- the exact branch, diff, commit, design, or artifact scope;
- one review pass, or another explicitly bounded number;
- a maximum spend when the local CLI supports `--max-budget-usd`.

A user request that names Fable and the review scope approves one pass. If it does not bound spend, ask for the cap before running the CLI. A re-review, expanded scope, or additional model requires new approval unless already included.

## Prepare the brief

Include the source revision, base and head when applicable, governing requirements and non-goals, lane, risky contracts to falsify, permitted read-only evidence, and the reviewer output contract from `development-flow:adversarial-reviewing`, embedded verbatim. Do not include credentials or unrelated private data. Do not feed suspected bugs or a desired verdict unless the user asked to verify a specific hypothesis.

Save the complete approved brief as a UTF-8 text file. Resolve the packaged runner relative to this `SKILL.md`; it passes the file content directly to Claude Code without shell parsing. Replace the quoted placeholders before running.

The repository under review is the session's current scoped repository, not the Development Flow plugin source, skill directory, cache, or marketplace checkout. Keep that repository identity and revision explicit in the brief.

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/request_review.py" --repository "ABSOLUTE_REPOSITORY_ROOT" --prompt-file "APPROVED_BRIEF_FILE" --max-budget-usd "APPROVED_USD_CAP"
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\request_review.py" --repository "ABSOLUTE_REPOSITORY_ROOT" --prompt-file "APPROVED_BRIEF_FILE" --max-budget-usd "APPROVED_USD_CAP"
```

The runner pins the process working directory to the approved repository and fixes the model, spend cap, non-persistent session, plan permission mode, JSON output, read-only allowlist, and editing or Agent denylist. It does not use a shell. The prompt must also say that Fable is the sole reviewer and may not spawn, delegate to, or invoke another reviewer or model. Do not weaken these controls to make the review succeed.

## Required Fable output

Embed the reviewer output contract from `development-flow:adversarial-reviewing` verbatim in the brief and require its exact Markdown inside the CLI result, including the `No actionable findings` verdict when nothing survives falsification.

## Receive the result

Check the CLI exit status and record the actual model identity reported by the result when available. On authentication, quota, network, or model failure, report the failure and stop; do not retry or substitute without approval.

Independently validate every finding using `development-flow:adversarial-reviewing`. Do not fix anything unless the user also authorized corrections. Never describe Fable's report as verification or completion evidence.

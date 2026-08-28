---
name: request-sol-review
description: Use when the user explicitly approves a GPT-5.6 Sol review of a bounded software diff, branch, commit, design, plan, or research conclusion.
---

# Request Sol Review

Request one isolated, read-only GPT-5.6 Sol review under the contract in `development-flow:adversarial-reviewing`. This skill consumes separate Codex usage and never triggers implicitly.

## Why Sol

Use Sol when the owner wants a fresh Codex-native reviewer that can inspect the repository deeply under a read-only sandbox. Prefer it for a second opinion on code, contracts, plans, or cross-file behavior where repository navigation matters. This does not make Sol's output authoritative.

Do not invoke it automatically at handoff, after a fix, or because a change appears risky. Suggest it and wait for approval. Do not silently substitute another GPT model when Sol is unavailable.

## Approval gate

Before invocation, obtain explicit approval for GPT-5.6 Sol, the exact review scope, and one pass or another bounded number. A user request that names Sol and the scope approves one pass. Expanded scope, re-review, higher additional effort, or another model requires new approval unless included upfront.

When the request already names Sol and the exact commit, branch, diff, or artifact, do not ask a second proceed or quota-confirmation question for that one pass. Prepare the bounded brief and invoke the runner. Report a blocked or failed invocation without fallback.

## Prepare the brief

Include repository identity, exact source revision, base and head when applicable, requirements and non-goals, lane, risky contracts to falsify, available verification evidence, and the reviewer output contract from `development-flow:adversarial-reviewing`, embedded verbatim. Exclude credentials and unrelated private data. For independent review, do not pre-seed suspected findings or the desired verdict.

Save the complete approved brief as a UTF-8 text file. Resolve the packaged runner relative to this `SKILL.md`; it passes paths and file content directly to Codex without shell parsing. Replace the quoted placeholders before running.

Resolve `ABSOLUTE_REPOSITORY_ROOT` from the repository under review, normally the session's current working directory via `git rev-parse --show-toplevel`. Never substitute the Development Flow plugin source, skill directory, cache, or marketplace checkout merely because it contains this runner.

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/request_review.py" --repository "ABSOLUTE_REPOSITORY_ROOT" --prompt-file "APPROVED_BRIEF_FILE"
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\request_review.py" --repository "ABSOLUTE_REPOSITORY_ROOT" --prompt-file "APPROVED_BRIEF_FILE"
```

The runner fixes the model, read-only sandbox, ephemeral session, and `--disable multi_agent`; it does not use a shell. Sol is the sole reviewer and may not spawn, delegate to, or invoke another reviewer or model. Repeat that prohibition in the brief. Never use `--dangerously-bypass-approvals-and-sandbox` for review.

## Required Sol output

Embed the reviewer output contract from `development-flow:adversarial-reviewing` verbatim in the brief and require its exact format in the result, including the `No actionable findings` verdict when nothing survives falsification. Sol may inspect relevant surrounding code but must not expand beyond the approved review question.

## Receive the result

On authentication, quota, tool, or model failure, report the failure and stop. Do not retry, change models, or add a reviewer without approval.

Independently validate every finding through `development-flow:adversarial-reviewing`. The active implementation writer applies only accepted findings when correction was authorized. A Sol review is evidence input, not proof that the change is complete.

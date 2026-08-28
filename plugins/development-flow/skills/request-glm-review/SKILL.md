---
name: request-glm-review
description: Use when the user explicitly approves a GLM review of a bounded software diff, branch, commit, design, plan, or research conclusion.
---

# Request GLM Review

Request one independent, read-only GLM review under the contract in `development-flow:adversarial-reviewing`, dispatched through the ZCode CLI. This skill spends the user's Z.ai coding-plan quota and never triggers implicitly.

## Why GLM

Use GLM when the owner wants a reviewer from a model family outside both the Claude and GPT lineages, and therefore least correlated with the implementing agent and the other available reviewers. This is a diversity argument, not a claim that GLM is universally stronger.

Do not use GLM merely because work is substantial, a release is near, or a prior review found something. Suggest it when useful, then wait for approval. Do not silently substitute another model when the approved one is unavailable.

## Approval gate

Before invocation, obtain explicit approval for:

- GLM as the reviewer, including the exact model (for example `GLM-5.3`);
- the exact branch, diff, commit, design, or artifact scope;
- one review pass, or another explicitly bounded number;
- the spend arrangement: the ZCode CLI enforces no USD cap, so approval must accept a single bounded pass on the user's Z.ai coding-plan quota.

A user request that names GLM and the review scope approves one pass at that scope. A missing spend arrangement must still be resolved. A re-review, expanded scope, or different model requires new approval unless already included.

## Prerequisites

The packaged Python runner resolves the ZCode CLI in this order: `ZCODE_BIN` → a `zcode` found on `PATH` → the `zcode.cjs` bundled inside the ZCode desktop app. The bundled fallback covers standard macOS and Windows locations. Set `ZCODE_BIN` only for a custom executable or `zcode.cjs` location.

| Platform | Bundled `zcode.cjs` path |
| --- | --- |
| macOS | `/Applications/ZCode.app/Contents/Resources/glm/zcode.cjs` |
| Windows | `%LOCALAPPDATA%\Programs\ZCode\resources\glm\zcode.cjs` |
| Linux | `<install-dir>/resources/glm/zcode.cjs` inside the extracted app directory |

If an install matches none of these, locate the file under `*resources/glm*` and point `ZCODE_BIN` at it. Linux installations without `zcode` on `PATH` must set `ZCODE_BIN` because extracted application directories have no standard location.

An executable resolved from `ZCODE_BIN` or `PATH` runs directly. For a bundled `zcode.cjs`, the runner uses the ZCode application executable as its Node runtime when available. Otherwise it requires Node 24 or newer because ZCode uses stable `node:sqlite`.

A one-time `~/.zcode/cli/config.json` model configuration is required. The sanctioned setup is `zcode login zai-coding-plan` (or the BigModel variant), which writes the final key to that file; an existing desktop-app provider entry with the same schema may be copied there instead. If the file is missing, stop and report the `model_config_missing` error instead of improvising credentials.

Before spending quota, run the packaged runner with `--check` and the approved model. This resolves ZCode, validates that `~/.zcode/cli/config.json` selects that exact model, and requests only the CLI version. It does not send a model prompt. Authentication is verified by the approved review itself; do not add a quota-consuming probe. One approved pass means one quota-consuming invocation.

Do not trust flags merely because the help text lists them. In CLI 0.16.5, `--max-turns` and `--allowed-tools` are advertised but not implemented; the parser rejects them. Available bounding controls are `--mode plan`, `--disallowed-tools`, `--cwd`, a single prompt, and an external wall-clock limit on the invocation.

## Prepare the brief

Include the source revision, base and head when applicable, governing requirements and non-goals, lane, risky contracts to falsify, permitted read-only evidence, and the reviewer output contract from `development-flow:adversarial-reviewing`, embedded verbatim. The brief must state that GLM is the sole reviewer and may not spawn, delegate to, or invoke another reviewer or model, and must not edit, write, commit, or push. Do not include credentials or unrelated private data. Do not feed suspected bugs or a desired verdict unless the user asked to verify a specific hypothesis.

## Invoke

Write the approved brief to a UTF-8 file. The packaged runner reads it and passes every argument directly to ZCode without shell parsing. It applies plan mode, denies editing and reviewer fan-out, and enforces the wall-clock limit on macOS, Linux, Windows PowerShell, and Windows Command Prompt.

Resolve `REPOSITORY_ROOT` from the repository under review, normally the session's current working directory via `git rev-parse --show-toplevel`. Never substitute the Development Flow plugin source, skill directory, cache, or marketplace checkout merely because it contains this runner.

Check the local CLI without spending model quota.

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/request_review.py" --check --model "APPROVED_GLM_MODEL"
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\request_review.py" --check --model "APPROVED_GLM_MODEL"
```

Run the single approved review invocation.

macOS or Linux:

```text
python3 "THIS_SKILL_DIRECTORY/scripts/request_review.py" --repository "REPOSITORY_ROOT" --prompt-file "APPROVED_BRIEF.txt" --model "APPROVED_GLM_MODEL" --timeout-seconds 900
```

Windows PowerShell or Command Prompt:

```text
py -3 "THIS_SKILL_DIRECTORY\scripts\request_review.py" --repository "REPOSITORY_ROOT" --prompt-file "APPROVED_BRIEF.txt" --model "APPROVED_GLM_MODEL" --timeout-seconds 900
```

The runner validates that `~/.zcode/cli/config.json` names the exact approved model before sending the prompt. It makes no authentication probe, retry, or fallback model call. `--mode plan` is mandatory because the headless default is `yolo`. The denylist removes editing, shell execution, plan-exit, and agent-spawning tools. Record the session's reported usage from the JSON result for the spend record.

If a future CLI version implements `--max-turns` or `--allowed-tools` for real (verify by running the flag, not by reading the help), prefer them and tighten this invocation.

## Receive the result

Check the exit status and parse the JSON. On authentication, quota, network, config, or model failure, report the failure and stop; do not retry, change models, or switch endpoints without approval.

Independently validate every finding using `development-flow:adversarial-reviewing`. The reviewer runs tool-restricted and may report commands the sandbox refused as evidence gaps; treat those gaps as unverified scope, not as defects. Do not fix anything unless the user also authorized corrections. Never describe GLM's report as verification or completion evidence.

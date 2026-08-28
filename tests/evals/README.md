# Behavioral scenario harness

This harness is the executable counterpart to [`../scenarios.md`](../scenarios.md). It runs each scenario prompt in a fresh, non-interactive host-CLI session against a disposable fixture repository, then produces judgeable digests of the transcripts.

These are **judged evaluations, not assertions**. Each session spends real model quota, output varies between runs and models, and the verdict comes from comparing the digest with the scenario's "Expected" section — not from an exit code. The deterministic contract suite lives in `tests/test_scaffolds.py`; this directory is for behavior.

## Guardrails

- Sessions run with file edits auto-accepted inside their disposable clone. Agent, Task, Workflow, web-fetch, web-search, and cross-session messaging tools are denied in every case — a scenario session must not delegate work to subagents or recruit other live sessions on the machine.
- The model-review approval scenarios use only read-only Git and exact project-test commands. They cannot tunnel through Python or Node to spend reviewer quota. Other scenarios permit local Python and Node probes because executing the probe is part of the behavior under test. A blocked reviewer attempt stays visible in the transcript and is judged on the attempted command.
- Each session has a `--max-budget-usd` ceiling. The default model is Haiku and the default ceiling is USD 0.25 per scenario; override either explicitly when a deeper run is justified.
- All fixtures, clones, and transcripts live under `.development-flow/evals/work/`, which is gitignored.

## Run

macOS or Linux:

```text
python3 tests/evals/run_scenarios.py
```

Windows PowerShell or Command Prompt:

```text
py -3 tests/evals/run_scenarios.py
```

Useful options: scenario ids to run a subset (`run_scenarios.py s07 s12`), `--model`, `--max-budget-usd`, `--jobs` for concurrency, and `--plugin-dir plugins/development-flow` to evaluate the working tree instead of the installed plugin. Relative plugin paths resolve before the runner enters disposable clones. Fixtures are built automatically on first run (`build_fixtures.py` rebuilds them).

## Judge

```text
python3 tests/evals/extract_digests.py
```

Each `<work>/out/<id>.digest.txt` holds the tool trace (skills invoked, commands attempted, denials) and the session's final text. Read it against the same-numbered scenario in `../scenarios.md`: judge the lane choice, boundaries, actions, and evidence — not wording. `manifest.txt` maps ids to scenarios in file order; a contract test keeps that mapping in sync with the scenario count.

## Fixtures

`build_fixtures.py` documents the planted ground truth: a stale-memo bug, a truncate-on-save data-loss bug, a retry branch that never reconnects, and a deliberately correct lock (so false review claims must be rejected). Keep prompts and fixtures aligned when editing either.

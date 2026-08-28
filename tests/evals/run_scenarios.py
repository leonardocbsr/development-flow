#!/usr/bin/env python3
"""Run Development Flow behavioral scenarios in fresh CLI sessions.

Each scenario from ``manifest.txt`` gets a disposable clone of its fixture and
one fresh, non-interactive session of the host CLI. Sessions run with file
edits auto-accepted inside the clone. Model-review approval scenarios use a
restricted command allowlist that cannot tunnel through Python or Node to a
paid reviewer; blocked attempts stay visible in the transcript.

Transcripts land in ``<work-dir>/out/<id>.jsonl``. Judge them against the
"Expected" section of the matching scenario in ``../scenarios.md`` (see
``extract_digests.py`` and README.md).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

REVIEW_SAFE_TOOLS = [
    "Bash(git status:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git show:*)",
    "Bash(git branch:*)",
    "Bash(ls:*)",
    "Bash(python3 -m unittest:*)",
    "Bash(py -3 -m unittest:*)",
    "Bash(node --check:*)",
    "Bash(npm test:*)",
]

IMPLEMENTATION_TOOLS = REVIEW_SAFE_TOOLS + [
    "Bash(python:*)",
    "Bash(python3:*)",
    "Bash(py -3:*)",
    "Bash(node:*)",
    "Bash(codex plugin list:*)",
    "Bash(claude plugin list:*)",
]

REVIEW_APPROVAL_SCENARIOS = {"s14", "s15", "s16", "s17"}
ALLOWED_TOOLS = REVIEW_SAFE_TOOLS  # compatibility alias for harness contract tests
DISALLOWED_TOOLS = ["Agent", "Task", "Workflow", "WebFetch", "WebSearch", "ListAgents", "SendMessage"]

KNOWN_FIXTURES = {"taskflow", "taskflow-bare", "csvlite"}


def read_manifest(path: Path) -> list[dict[str, str]]:
    scenarios = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        scenario_id, fixture, branch, prompt = line.split("|", 3)
        scenarios.append(
            {"id": scenario_id, "fixture": fixture, "branch": branch, "prompt": prompt}
        )
    return scenarios


def ensure_fixtures(work: Path) -> Path:
    fx = work / "fx"
    if not all((fx / name).is_dir() for name in KNOWN_FIXTURES):
        subprocess.run(
            [sys.executable, str(HERE / "build_fixtures.py"), "--work-dir", str(work)],
            check=True,
        )
    return fx


def validated_plugin_dir(path: Path | None) -> Path | None:
    if path is None:
        return None
    plugin_dir = path.expanduser().resolve()
    if not (plugin_dir / ".claude-plugin").is_dir() and not (plugin_dir / "skills").is_dir():
        raise ValueError(f"--plugin-dir does not look like a plugin directory: {plugin_dir}")
    return plugin_dir


def run_scenario(scenario: dict[str, str], args: argparse.Namespace, work: Path) -> tuple[str, int]:
    fx = work / "fx" / scenario["fixture"]
    clone = work / "runs" / scenario["id"]
    out = work / "out"
    out.mkdir(parents=True, exist_ok=True)
    if clone.exists():
        shutil.rmtree(clone)
    clone.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", str(fx), str(clone)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(clone), "checkout", "-q", scenario["branch"]], check=True, capture_output=True)

    head_main = subprocess.run(
        ["git", "-C", str(clone), "rev-parse", "--short", "main"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    prompt = scenario["prompt"].replace("{HEAD_MAIN}", head_main)

    allowed_tools = (
        REVIEW_SAFE_TOOLS
        if scenario["id"] in REVIEW_APPROVAL_SCENARIOS
        else IMPLEMENTATION_TOOLS
    )
    command = [
        args.claude_bin, "-p", prompt,
        "--model", args.model,
        "--no-session-persistence",
        "--permission-mode", "acceptEdits",
        "--max-turns", str(args.max_turns),
        "--max-budget-usd", str(args.max_budget_usd),
        "--allowedTools", *allowed_tools,
        "--disallowedTools", *DISALLOWED_TOOLS,
        "--output-format", "stream-json", "--verbose",
    ]
    if args.plugin_dir:
        command += ["--plugin-dir", str(args.plugin_dir)]

    with open(out / f"{scenario['id']}.jsonl", "w", encoding="utf-8") as stdout, \
         open(out / f"{scenario['id']}.err", "w", encoding="utf-8") as stderr:
        result = subprocess.run(command, cwd=clone, stdout=stdout, stderr=stderr)
    return scenario["id"], result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scenarios", nargs="*", help="scenario ids to run (default: all)")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001",
                        help="model for fresh sessions (default: claude-haiku-4-5-20251001)")
    parser.add_argument("--plugin-dir", type=Path, default=None,
                        help="load the plugin from this directory instead of the installed copy "
                             "(e.g. plugins/development-flow to evaluate the working tree)")
    parser.add_argument("--work-dir", type=Path,
                        default=REPO / ".development-flow" / "evals" / "work",
                        help="fixtures, clones, and transcripts root (default: <repo>/.development-flow/evals/work)")
    parser.add_argument("--jobs", type=int, default=4, help="concurrent sessions (default: 4)")
    parser.add_argument("--max-turns", type=int, default=50)
    parser.add_argument("--max-budget-usd", type=float, default=0.25,
                        help="hard cost ceiling for each fresh session (default: 0.25)")
    parser.add_argument("--claude-bin", default="claude", help="host CLI executable (default: claude)")
    args = parser.parse_args()
    if args.max_budget_usd <= 0:
        parser.error("--max-budget-usd must be greater than zero")

    work = args.work_dir.expanduser().resolve()
    try:
        args.plugin_dir = validated_plugin_dir(args.plugin_dir)
    except ValueError as error:
        parser.error(str(error))
    scenarios = read_manifest(HERE / "manifest.txt")
    if args.scenarios:
        wanted = set(args.scenarios)
        unknown = wanted - {s["id"] for s in scenarios}
        if unknown:
            parser.error(f"unknown scenario ids: {sorted(unknown)}")
        scenarios = [s for s in scenarios if s["id"] in wanted]

    ensure_fixtures(work)

    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(run_scenario, scenario, args, work) for scenario in scenarios]
        for future in concurrent.futures.as_completed(futures):
            scenario_id, code = future.result()
            print(f"{scenario_id} exit={code}")
            failures += 1 if code != 0 else 0

    print(f"done: {len(scenarios)} scenario sessions, {failures} nonzero exits, transcripts in {work / 'out'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

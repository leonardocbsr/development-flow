#!/usr/bin/env python3
"""Invoke one approved Fable review without shell-dependent quoting."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path
import subprocess


def positive_decimal(value: str) -> str:
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("budget must be a decimal number") from error
    if not amount.is_finite() or amount <= 0:
        raise argparse.ArgumentTypeError("budget must be greater than zero")
    return value


def build_command(prompt: str, max_budget_usd: str) -> list[str]:
    return [
        "claude",
        "-p",
        prompt,
        "--model",
        "fable",
        "--max-budget-usd",
        max_budget_usd,
        "--no-session-persistence",
        "--permission-mode",
        "plan",
        "--output-format",
        "json",
        "--allowedTools",
        "Read",
        "Grep",
        "Glob",
        "Bash(git diff:*)",
        "Bash(git log:*)",
        "Bash(git status:*)",
        "Bash(git show:*)",
        "Bash(git branch:*)",
        "Bash(git merge-base:*)",
        "--disallowedTools",
        "Agent",
        "Edit",
        "Write",
        "NotebookEdit",
    ]


def run_review(repository: Path, prompt: str, max_budget_usd: str) -> int:
    root = repository.expanduser().resolve()
    if not root.is_dir():
        raise RuntimeError(f"repository_not_found: {root}")
    return subprocess.run(
        build_command(prompt, max_budget_usd),
        cwd=root,
        check=False,
    ).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one approved read-only Fable review.")
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--max-budget-usd", type=positive_decimal, required=True)
    args = parser.parse_args()
    prompt = args.prompt_file.expanduser().read_text(encoding="utf-8")
    try:
        return run_review(args.repository, prompt, args.max_budget_usd)
    except RuntimeError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
